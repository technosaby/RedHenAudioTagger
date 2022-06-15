import subprocess
import os
import sys
import glob
from concurrent.futures import ProcessPoolExecutor as Executor
from scipy.io import wavfile

class VideoProcessor:
    def __init__(self):
        self.cmd = "ffmpeg"

    def extract_audio(self, video_file, output_ext="mp3"):
        try:
            filename, ext = os.path.splitext(video_file)
            subprocess.call([self.cmd, "-i", video_file, "-vn", "-f", "wav", "-ar","16000",
                             "-ac", "1", f"{filename}.{output_ext}"],
                            stdout=subprocess.DEVNULL,
                            stderr=subprocess.STDOUT)
        except:
            print("Error in converting ", video_file)
            raise

    def extract_audio_files(self, video_input_folder_path, audio_output_folder_path):
        mp4_filenames = map(lambda x: x.split('.')[0], glob.iglob('*.mp4'))
        POOL_SIZE = os.cpu_count()  # number of cores
        with Executor(max_workers=POOL_SIZE) as executor:
            executor.map(self.extract_audio, mp4_filenames)

if __name__ == '__main__':
    vp = VideoProcessor()
    print("Starting generation of audio files ....")
    INPUT_VIDEO_PATH = "/Users/saby/Documents/RedHen/SampleCode/sample_redhen_files/"
    OUTPUT_AUDIO_PATH = "/Users/saby/Documents/RedHen/SampleCode/output_files/"
    #vp.extract_audio_files(INPUT_VIDEO_PATH, OUTPUT_AUDIO_PATH)"
    vp.extract_audio(INPUT_VIDEO_PATH + "abc.mp4",output_ext="wav")
    print("Generation of audio files complete...")
    ##Analyse the output audio
    sample_rate, wav_data = wavfile.read(INPUT_VIDEO_PATH + "abc.wav", 'rb')
    print(f'Sample rate: {sample_rate} Hz')
    print(f'Size of the input: {len(wav_data)}')

