#!/usr/bin/python
import numpy as np
import csv
import os

""" This file will parse the data and show in the required formats
The data will be frame by frame scores which is received by YaMNet model
This frame scores will be parsed in the required formats needed by Red Hen for reporting
"""


def generate_legend():
    legend_info = "SFX_01|FileName: audio_file_convertor.py|Source Person: Sabyasachi Ghosal" + "\n"
    legend_info += "FFS|AudioCodebook=Model_Putput_Index|Machine_Identifier|Class_Description" + "\n"
    return legend_info


class DataParser:
    def __init__(self, scores, input_file_name_with_path, output_file_name_with_path, class_names, audio_format, duration, sample_rate,
                 patch_hop_seconds, patch_window_seconds,
                 stft_hop, stft_window, parsing_format="DEFAULT"):
        self.scores = np.array(scores)
        self.parsing_format = parsing_format
        self.class_names = class_names
        self.input_file_name_with_path = input_file_name_with_path
        self.output_file_name_with_path = output_file_name_with_path
        self.audio_format = audio_format
        self.duration = duration
        self.patch_hop_seconds = patch_hop_seconds
        self.patch_window_seconds = patch_window_seconds
        self.stft_hop = stft_hop
        self.stft_window = stft_window
        self.sample_rate = sample_rate
        self.round_val = 4

    def process_scores(self):
        derived_classes = []
        for row in self.scores:
            derived_classes.append({self.class_names[i]: np.round(x, self.round_val)
                                    for i, x in enumerate(row) if np.round(x, self.round_val) > 0.0})
        return derived_classes

    def parse_dump_scores(self):
        """
        The data in the text files is structured as follows:
            - A header with file-level information
            - A legend with information about the different modules that have been run on the file
            - The data section
        :return: None
        """
        derived_classes_with_scores = self.process_scores()
        frame_start_times = [0.4 * i for i in range(0, len(derived_classes_with_scores))]
        sfx_tags = ["SFX_01" for i in range(0, len(derived_classes_with_scores))]
        frame_length = self.patch_window_seconds + (self.stft_window - self.stft_hop)
        frame_end_times = np.array(frame_start_times) + frame_length

        # Appending file names to the seconds
        file_name = os.path.split(self.output_file_name_with_path)[1]
        file_name_frame_header = "-".join(file_name.split("_", 2)[:2]).replace("-", "")
        frame_start_times_with_filename = [file_name_frame_header + str(format(s, '07.03f')) for s in frame_start_times]
        frame_end_times_with_filename = [file_name_frame_header + str(format(s, '07.03f')) for s in frame_end_times]

        if self.parsing_format == "DEFAULT":
            os.makedirs(os.path.dirname(self.output_file_name_with_path + '.sfx'), exist_ok=True)
            with open(self.output_file_name_with_path + '.sfx', 'w') as f:
                # Create Header of the file
                file_header = self.generate_header()
                f.write(file_header)
                legend_info = generate_legend()
                f.write(legend_info)
                # Write data section
                writer = csv.writer(f, delimiter="|")
                writer.writerows(
                    zip(frame_start_times_with_filename, frame_end_times_with_filename,
                        sfx_tags, derived_classes_with_scores))

        elif self.parsing_format == "ELAN_EAF":
            # ToDO:// For future
            pass
        else:
            print("Please use specified formats")

    def generate_header(self):
        N = 30  # read first 20 lines of the seg file
        with open(self.input_file_name_with_path + ".seg", "r") as fi:
            head = [next(fi) for x in range(N)]
            id = ""
            for ln in head:
                if ln.startswith("TOP"):
                    id += ln
                elif ln.startswith("COL"):
                    id += ln
                elif ln.startswith("UID"):
                    id += ln
                elif ln.startswith("SRC"):
                    id += ln
                elif ln.startswith("TTL"):
                    id += ln
                elif ln.startswith("PID"):
                    id += ln
                elif ln.startswith("CMT"):
                    id += ln
                elif ln.startswith("DUR"):
                    id += ln
                elif ln.startswith("VID"):
                    id += ln
                elif ln.startswith("CC1"):
                    id += ln
                elif ln.startswith("LBT"):
                    id += ln
        file_header = id
        file_header += "AUDIO_FORMAT|" + self.audio_format + "\n"
        file_header += "SAMPLING_RATE|" + str(self.sample_rate) + "\n"
        file_header += "PATCH_WINDOW_SECONDS|" + str(self.patch_window_seconds) + "\n"
        file_header += "PATCH_HOP_SECONDS|" + str(self.patch_hop_seconds) + "\n"
        return str(file_header)
