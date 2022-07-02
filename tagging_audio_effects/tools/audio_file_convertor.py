#!/usr/bin/python
import subprocess
import os
import sys
import shutil

"""
This file do the following
1. Parses the video files and extracts audio from the video files.
2. This will copy the folder structure with all videos and create similar folder structure with generated audio files.
3. It generates mono audio because YaMNet needs only mono.
4. It generates sampling rate of 16k based on YaMNet's requirements.
5. If the video contains seg files, this parser also copies them and put it in the audio folders.
"""


class AudioFileConvertor:
    def __init__(self):
        self.ffmpeg_cmd = "ffmpeg"

    def extract_audio(self, input_video_path_with_file_name, output_audio_file_with_file_name, output_ext, logs):
        """
        This file extracts a single audio file from a video file using ffmpeg

        :param input_video_path_with_file_name: The file path of a single video file
        :param output_audio_file_with_file_name: The file path in which the single audio file is generated
        :param output_ext: The output format of the audio file, default is wav
        :param logs: Decides whether logs should be enabled or not
        :return: None
        """
        subprocess.call([self.ffmpeg_cmd, "-i", input_video_path_with_file_name, "-vn", "-f", output_ext, "-ar", "16000",
                         "-ac", "1", output_audio_file_with_file_name],
                        stdout=subprocess.DEVNULL,
                        stderr=subprocess.STDOUT)
        if logs:
            print("Input Video File " + input_video_path_with_file_name)
            print("Generation of audio files complete with filename ", output_audio_file_with_file_name)

    def extract_audio_files(self, video_input_folder_path, audio_output_folder_path,
                            video_file_extensions="mp4",
                            output_ext="wav",
                            seg_file_available=0, seg_file_extension=".seg", logs=0):
        """
        This file takes a folder with multiple video files and generates audio files as inputs. The audio file
        generation will follow the same folder structure as that of the video file. It can also process a single
        video file.

        :param video_input_folder_path: The path from which video files will be read
        :param audio_output_folder_path: The path in which audio files will be generated
        :param video_file_extensions: The input video file format, default is mp4
        :param output_ext: The output format in which audio files need to be extracted, default is wav
        :param logs: Determines whether logs should be enabled
        :param seg_file_extension: Extension of the segmentation file
        :param seg_file_available: If segmentation file is available
        :return: None
        """
        # For input as a single file
        if "." + video_file_extensions in video_input_folder_path:
            filename = os.path.splitext(video_input_folder_path)[0] + "." + output_ext
            self.extract_audio(os.path.join(audio_output_folder_path, video_input_folder_path),
                               os.path.join(audio_output_folder_path, filename), output_ext, logs)
            if seg_file_available:
                filename_seg = os.path.splitext(video_input_folder_path)[0] + "." + seg_file_extension
                shutil.copyfile(os.path.join(audio_output_folder_path, video_input_folder_path),
                            os.path.join(audio_output_folder_path, filename_seg))
        # Only for directories as input
        else:
            for dir_path, dir_names, filenames in os.walk(video_input_folder_path):
                output_structure = os.path.join(audio_output_folder_path, dir_path[len(video_input_folder_path):])
                input_structure = os.path.join(video_input_folder_path, dir_path[len(video_input_folder_path):])
                if not os.path.isdir(output_structure):
                    os.mkdir(output_structure)
                for filename in [f for f in filenames if f.endswith("." + video_file_extensions)]:
                    output_file_name = os.path.join(output_structure, filename)
                    output_file_name = os.path.splitext(output_file_name)[0] + "." + output_ext
                    input_file_name = os.path.join(input_structure, filename)
                    self.extract_audio(input_file_name, output_file_name, output_ext, logs)

                # Copy the .seg files from the same path as the video files and place it in along with the audio files
                if seg_file_available:
                    for filename in [f for f in filenames if f.endswith("." + seg_file_extension)]:
                        input_file_name = os.path.join(input_structure, filename)
                        output_file_name = os.path.join(output_structure, filename)
                        shutil.copyfile(input_file_name, output_file_name)

if __name__ == '__main__':
    INPUT_VIDEO_PATH = sys.argv[1]
    OUTPUT_AUDIO_PATH = sys.argv[2]
    OUTPUT_AUDIO_FORMAT = sys.argv[3]
    INPUT_VIDEO_FORMAT = sys.argv[4]
    SEG_FILES_AVAILABLE = sys.argv[5]
    LOGS = sys.argv[6]

    audio_processor = AudioFileConvertor()
    print("Starting generation of audio files from ", INPUT_VIDEO_PATH, " to ", OUTPUT_AUDIO_PATH
          + " with format " + OUTPUT_AUDIO_FORMAT)
    audio_processor.extract_audio_files(INPUT_VIDEO_PATH, OUTPUT_AUDIO_PATH, INPUT_VIDEO_FORMAT, OUTPUT_AUDIO_FORMAT,
                                        int(SEG_FILES_AVAILABLE), "seg", int(LOGS))




