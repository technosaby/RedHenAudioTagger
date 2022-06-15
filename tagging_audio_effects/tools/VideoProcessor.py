#!/usr/bin/python
import subprocess
import os
import sys

INPUT_VIDEO_PATH = sys.argv[1]
OUTPUT_AUDIO_PATH = sys.argv[2]


# INPUT_VIDEO_PATH = "/mnt/rds/redhen/gallina/tv/2022"
# OUTPUT_AUDIO_PATH = "/home/sxg1263/sxg1263gallinahome/audio_output_files"
# python VideoProcessor.py "/mnt/rds/redhen/gallina/tv/2022" "/home/sxg1263/sxg1263gallinahome/audio_output_files"

class VideoProcessor:
    def __init__(self):
        self.cmd = "ffmpeg"

    def extract_audio(self, video_file, input_video_path, output_audio_file):
        print("Video File " + video_file)
        print("Input Video File " + input_video_path)
        print("Output Video File " + output_audio_file)
        subprocess.call([self.cmd, "-i", input_video_path, "-vn", "-f", "wav", "-ar", "16000",
                         "-ac", "1", output_audio_file],
                        stdout=subprocess.DEVNULL,
                        stderr=subprocess.STDOUT)

    def extract_audio_files(self, video_input_folder_path, audio_output_folder_path,
                            video_file_extensions=".mp4", output_ext=".mp3"):
        for dirpath, dirnames, filenames in os.walk(video_input_folder_path):
            output_structure = os.path.join(audio_output_folder_path, dirpath[len(video_input_folder_path):])
            input_structure = os.path.join(video_input_folder_path, dirpath[len(video_input_folder_path):])
            if not os.path.isdir(output_structure):
                os.mkdir(output_structure)
            for filename in [f for f in filenames if f.endswith(video_file_extensions)]:
                output_file_name = os.path.join(output_structure, filename)
                output_file_name = os.path.splitext(output_file_name)[0] + output_ext
                input_file_name = os.path.join(input_structure, filename)
                self.extract_audio(filename, input_file_name, output_file_name)


if __name__ == '__main__':
    vp = VideoProcessor()
    print("Starting generation of audio files from ", INPUT_VIDEO_PATH, " to ", OUTPUT_AUDIO_PATH)
    vp.extract_audio_files(INPUT_VIDEO_PATH, OUTPUT_AUDIO_PATH)
    print("Generation of audio files complete...")
