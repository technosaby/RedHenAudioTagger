#!/usr/bin/python
import csv
import json
import os
import sys

import numpy as np
import pandas as pd

""" This file will parse the data and show in the required formats
The data will be frame by frame scores which is received by YaMNet model
This frame scores will be parsed in the required formats needed by Red Hen for reporting
"""


def generate_legend():
    legend_info = "SFX_01|FileName: audio_file_convertor.py|Source Person: Sabyasachi Ghosal" + "\n"
    legend_info += "FFS|Codebook=Model_Output_Index|Class_Description" + "\n"
    return legend_info


class DataParser:
    def __init__(self, scores, input_file_name_with_path, output_file_name_with_path, class_names,
                 audio_format, duration, sample_rate, score_filtering_decimal_places,
                 is_seg_file_present, patch_hop_seconds, patch_window_seconds,
                 stft_hop, stft_window, parsing_format, filter_csv_score, logs=0):
        self.scores = np.array(scores)
        self.parsing_format = parsing_format
        self.class_names = class_names
        self.input_file_name_with_path = input_file_name_with_path
        self.output_file_name_with_path = output_file_name_with_path
        self.audio_format = audio_format
        self.duration = duration
        self.is_seg_file_present = is_seg_file_present
        self.patch_hop_seconds = patch_hop_seconds
        self.patch_window_seconds = patch_window_seconds
        self.stft_hop = stft_hop
        self.stft_window = stft_window
        self.sample_rate = sample_rate
        self.round_val = score_filtering_decimal_places
        self.is_logs_enabled = logs
        self.filter_csv_score = filter_csv_score

    def parse_dump_scores(self):
        """
        The data in the text files is structured as follows:
            - A header with file-level information
            - A legend with information about the different modules that have been run on the file
            - The data section
        :return: None
        """
        # process all record on tag basis for SFX
        if self.parsing_format == "SFX":
            self.create_sfx_file()
        elif self.parsing_format == "CSV":
            self.create_csv_file()
        elif self.parsing_format == "BOTH":
            self.create_csv_file()
            self.create_sfx_file()
        else:
            if self.is_logs_enabled:
                print("Please use specified formats SFX/CSV")

    def create_csv_file(self):
        audio_tag_prefix_str = "Audio_Tag_"
        df = pd.DataFrame(self.scores, columns=self.class_names)
        df = df.round(self.round_val)
        frame_start_times = [self.patch_hop_seconds * i for i in range(0, len(df[df.columns[0]]))]
        frame_length = self.patch_window_seconds + (self.stft_window - self.stft_hop)
        frame_end_times = np.array(frame_start_times) + frame_length
        os.makedirs(os.path.dirname(self.output_file_name_with_path + '.csv'), exist_ok=True)
        # Now writing the data
        # ToDo:// This can be improved, can be made more faster
        with open(self.output_file_name_with_path + '.csv', 'w') as f:
            for column in df:
                frame_start_time = frame_start_times[0]
                for index, score in enumerate(df[column][:-1]):
                    if np.round(score, self.round_val) == 0:
                        frame_start_time = frame_start_times[index + 1]
                        continue
                    if np.round(score, self.round_val) < self.filter_csv_score:
                        continue
                    if np.isclose(score, df[column][index + 1], rtol=1e-05, atol=1e-08, equal_nan=False):
                        continue
                    f.write(audio_tag_prefix_str + column.replace(",", "|") + "," + str(frame_start_time) + "," +
                            str(frame_end_times[index]) + "," + str(score) + "\n")
                    frame_start_time = frame_start_times[index + 1]

    def process_scores_for_sfx(self):
        derived_classes = []
        score_data = {}
        for row in self.scores:
            for i, x in enumerate(row):
                if np.round(x, self.round_val) > 0.0:
                    score_data[self.class_names[i]] = str(np.round(x, self.round_val))
            derived_classes.append(json.dumps(score_data))
        return derived_classes

    def create_sfx_file(self):
        derived_classes_with_scores = self.process_scores_for_sfx()
        frame_start_times = [self.patch_hop_seconds * i for i in range(0, len(derived_classes_with_scores))]
        frame_length = self.patch_window_seconds + (self.stft_window - self.stft_hop)
        frame_end_times = np.array(frame_start_times) + frame_length

        # Appending file names to the seconds
        file_name = os.path.split(self.output_file_name_with_path)[1]
        file_name_frame_header = "-".join(file_name.split("_", 2)[0]).replace("-", "")
        frame_start_times_with_filename = [file_name_frame_header + str(format(s, '07.03f')) for s in
                                           frame_start_times]
        frame_end_times_with_filename = [file_name_frame_header + str(format(s, '07.03f')) for s in frame_end_times]
        # frame_start_times_with_filename = [str(format(s, '07.03f')) for s in
        #                                    frame_start_times]
        # frame_end_times_with_filename = [str(format(s, '07.03f')) for s in frame_end_times]
        sfx_tags = ["SFX_01" for i in range(0, len(derived_classes_with_scores))]
        os.makedirs(os.path.dirname(self.output_file_name_with_path + '.sfx'), exist_ok=True)
        with open(self.output_file_name_with_path + '.sfx', 'w') as f:
            # Create Header of the file, read if seg file present else create Top header
            if self.is_seg_file_present:
                file_header = self.generate_header()
            else:
                file_header = self.generate_top_header()
            f.write(file_header)

            # Write audio model properties
            audio_model_properties = self.generate_audio_model_properties()
            f.write(audio_model_properties)
            legend_info = generate_legend()
            f.write(legend_info)
            # Write data section
            writer = csv.writer(f, delimiter="|", quoting=csv.QUOTE_NONE, quotechar='')
            writer.writerows(
                zip(frame_start_times_with_filename, frame_end_times_with_filename,
                    sfx_tags, derived_classes_with_scores))

    def generate_top_header(self):
        file_header_top = "TOP"
        file_name = os.path.normpath(self.input_file_name_with_path).split(os.sep)[-1]
        file_header_top += "|" + file_name + "\n"
        return file_header_top

    def generate_header(self):
        first_lines_seg_file_count = 30  # read first 20 lines of the seg file
        file_header = None
        try:
            with open(self.input_file_name_with_path + ".seg", "r") as fi:
                head = [next(fi) for _ in range(first_lines_seg_file_count)]
                id_sfx = ""
                for ln in head:
                    if ln.startswith("TOP"):
                        id_sfx += ln
                    elif ln.startswith("COL"):
                        id_sfx += ln
                    elif ln.startswith("UID"):
                        id_sfx += ln
                    elif ln.startswith("SRC"):
                        id_sfx += ln
                    elif ln.startswith("TTL"):
                        id_sfx += ln
                    elif ln.startswith("PID"):
                        id_sfx += ln
                    elif ln.startswith("CMT"):
                        id_sfx += ln
                    elif ln.startswith("DUR"):
                        id_sfx += ln
                    elif ln.startswith("VID"):
                        id_sfx += ln
                    elif ln.startswith("CC1"):
                        id_sfx += ln
                    elif ln.startswith("LBT"):
                        id_sfx += ln
            file_header = id_sfx
        except:
            print("WARNING: SEG File format not correct, SFX could not be generated properly")

        # Generate top block separately
        if file_header is None:
            file_header = "TOP|" + os.path.normpath(self.input_file_name_with_path).split(os.sep)[-1]
        return str(file_header)

    def generate_audio_model_properties(self):
        data_audio_model_properties = "AUDIO_FORMAT|" + self.audio_format + "\n"
        data_audio_model_properties += "SAMPLING_RATE|" + str(self.sample_rate) + "\n"
        data_audio_model_properties += "PATCH_WINDOW_SECONDS|" + str(self.patch_window_seconds) + "\n"
        data_audio_model_properties += "PATCH_HOP_SECONDS|" + str(self.patch_hop_seconds) + "\n"
        return data_audio_model_properties
