#!/usr/bin/python
import subprocess
import os
import sys

"""
This file do the following
1. Parses the video files and extracts audio from the video files.
2. This will copy the folder structure with all videos and create similar folder structure with generated audio files.
3. It generates mono audio because Yamnet needs only mono.
4. It generates sampling rate of 16k based on Yamnet's requirements.
"""

INPUT_VIDEO_PATH = sys.argv[1]
OUTPUT_AUDIO_PATH = sys.argv[2]
OUTPUT_AUDIO_FORMAT = sys.argv[3]
INPUT_VIDEO_FORMAT = sys.argv[4]
LOGS = sys.argv[5]


# INPUT_VIDEO_PATH = "abc.mp4" #"sample_redhen_files/" #"abc.mp4" #"/mnt/rds/redhen/gallina/tv/2022"
# OUTPUT_AUDIO_PATH = "." #"output_files/" #"/home/sxg1263/sxg1263gallinahome/audio_output_files"
# OUTPUT_AUDIO_FORMAT = "wav"
# INPUT_VIDEO_FORMAT = "mp4"
# LOGS = 1

# python VideoProcessor.py "/mnt/rds/redhen/gallina/tv/2022" "/home/sxg1263/sxg1263gallinahome/audio_output_files"

class AudioProcessor:
    def __init__(self):
        self.cmd = "ffmpeg"

    def extract_audio(self, input_video_path_with_file_name, output_audio_file_with_file_name, output_ext, logs):
        subprocess.call([self.cmd, "-i", input_video_path_with_file_name, "-vn", "-f", output_ext, "-ar", "16000",
                         "-ac", "1", output_audio_file_with_file_name],
                        stdout=subprocess.DEVNULL,
                        stderr=subprocess.STDOUT)
        if logs:
            print("Input Video File " + input_video_path_with_file_name)
            print("Generation of audio files complete with filename ", output_audio_file_with_file_name)

    def extract_audio_files(self, video_input_folder_path, audio_output_folder_path,
                            video_file_extensions="mp4", output_ext="wav", logs=0):
        # For input as a single file
        if "." + video_file_extensions in video_input_folder_path:
            filename = os.path.splitext(video_input_folder_path)[0] + "." + output_ext
            self.extract_audio(os.path.join(audio_output_folder_path, video_input_folder_path),
                               os.path.join(audio_output_folder_path, filename), output_ext, logs)
        # Only for directories as input
        else:
            for dirpath, dirnames, filenames in os.walk(video_input_folder_path):
                output_structure = os.path.join(audio_output_folder_path, dirpath[len(video_input_folder_path):])
                input_structure = os.path.join(video_input_folder_path, dirpath[len(video_input_folder_path):])
                if not os.path.isdir(output_structure):
                    os.mkdir(output_structure)
                for filename in [f for f in filenames if f.endswith("." + video_file_extensions)]:
                    output_file_name = os.path.join(output_structure, filename)
                    output_file_name = os.path.splitext(output_file_name)[0] + "." + output_ext
                    input_file_name = os.path.join(input_structure, filename)
                    self.extract_audio(input_file_name, output_file_name, output_ext, logs)


if __name__ == '__main__':
    vp = AudioProcessor()
    print("Starting generation of audio files from ", INPUT_VIDEO_PATH, " to ", OUTPUT_AUDIO_PATH
          + " with format " + OUTPUT_AUDIO_FORMAT)
    vp.extract_audio_files(INPUT_VIDEO_PATH, OUTPUT_AUDIO_PATH, INPUT_VIDEO_FORMAT, OUTPUT_AUDIO_FORMAT, int(LOGS))
