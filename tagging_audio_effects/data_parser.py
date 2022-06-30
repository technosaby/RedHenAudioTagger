#!/usr/bin/python
import numpy as np
import csv
import os

""" This file will parse the data and show in the required formats
The data will be frame by frame scores which is received by YaMNet model
This frame scores will be parsed in the required formats needed by Red Hen for reporting
"""


class DataParser:
    def __init__(self, scores, file_name_with_path, class_names, audio_format, duration,
                 patch_hop_seconds, patch_window_seconds,
                 stft_hop, stft_window, parsing_format="DEFAULT"):
        self.scores = np.array(scores)
        self.parsing_format = parsing_format
        self.class_names = class_names
        self.file_name_with_path = file_name_with_path
        self.audio_format = audio_format
        self.duration = duration
        self.patch_hop_seconds = patch_hop_seconds
        self.patch_window_seconds = patch_window_seconds
        self.stft_hop = stft_hop
        self.stft_window = stft_window

    def parse_dump_scores(self):
        """
        The data in the text files is structured as follows:
            - A header with file-level information
            - A legend with information about the different modules that have been run on the file
            - The data section
        :return: None
        """
        derived_classes = [self.class_names[i] for i in np.argmax(self.scores, axis=1)]
        frame_start_times = [0.4 * i for i in range(0, len(derived_classes))]
        frame_length = self.patch_window_seconds + (self.stft_window - self.stft_hop)
        frame_end_times = np.array(frame_start_times) + frame_length

        if self.parsing_format == "DEFAULT":
            with open(self.file_name_with_path + '.sfx', 'w') as f:
                file_name = os.path.split(self.file_name_with_path)[1]
                # Create Header of the file
                file_header = "TOP|" + file_name.translate({ord('-'): None}).translate({ord('_'):None})[0:12] +\
                              "|" + file_name + "\n"
                file_header += "FORMAT|" + self.audio_format + "\n"
                file_header += "DURATION|" + str(self.duration) + "\n"
                file_header += "PATCH_WINDOW_SECONDS|" + str(self.patch_window_seconds) + \
                               " PATCH_HOP_SECONDS|" + str(self.patch_hop_seconds) + "\n"

                f.write(file_header)
                # Write content
                writer = csv.writer(f)
                writer.writerows(zip(frame_start_times, frame_end_times, derived_classes))

        elif self.parsing_format == "ELAN_EAF":
            # ToDO:// Discuss with mentors about this
            pass
        else:
            print("Please use specified formats")
