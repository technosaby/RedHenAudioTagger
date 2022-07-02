#!/usr/bin/python
"""
This file do the following
1. Take the input as a folder with audio files (wav, mono, 16k sampling rate) files
2. Take each file and check if they are compatible to the model, else throw error and proceed to the next file
3. Run Yamnet model on that
4. Generate out in the format suitable for RedHen
"""
import tensorflow as tf
import tensorflow_hub as hub
import numpy as np
import csv
import matplotlib.pyplot as plt
from scipy.io import wavfile
import scipy.signal
import os
import sys
from data_parser import DataParser


def ensure_sample_rate(original_sample_rate, waveform, desired_sample_rate=16000):
    """Resample waveform to ensure sampling rate is as expected
    : original_sample_rate: The original sampling rate of the audio file
    : waveform: The actual waveform
    : desired_sample_rate: The desired sampling rate, 16K for YaMNet model
    """
    if original_sample_rate != desired_sample_rate:
        if LOGS: print("Sampling rate mismatch, Converting to 16k sampling rate")
        desired_length = int(round(float(len(waveform)) /
                                   original_sample_rate * desired_sample_rate))
        waveform = scipy.signal.resample(waveform, desired_length)
    else:
        if LOGS:
            print("Sampling rate is 16k, hence no conversion required")
    return waveform


def convert_to_compatible_file(audio_path):
    """
    YaMNet expects the audio files should be
    a) mono
    b) wav file
    c) with sampling rate of 16k
    This function ensures the audio files are in this format, if not it will try to convert into the compatible format.
    If it fails in any step it will return -1 (ERROR)

    :param audio_path: Gets the audio path where a single audio file is present
    :return: (Error (-1) OR Success (0) Code, converted audio file)
    """
    ret = 0
    # Check if the audio file is having correct sampling rate
    sample_rate, wav_data = wavfile.read(audio_path)
    wav_data = ensure_sample_rate(sample_rate, wav_data)
    # ToDo:// Check if the audio is mono else convert to mono, any failure in comparison return -1
    # wav_data = ensure_mono_channel(wav_data)
    # ToDo:// Check if audio format is wav, any failure will return -1
    # wav_data = ensure_wav_format(wav_data)
    # needs to be normalized to values in [-1.0, 1.0]
    waveform = wav_data / tf.int16.max

    if LOGS:
        # Show some basic information about the converted audio.
        duration_audio = len(wav_data) / sample_rate
        print(f'Sample rate: {sample_rate} Hz')
        print(f'Total duration: {duration_audio:.2f}s')
        print(f'Size of the input: {len(wav_data)}')
        # Show some basic information about the audio.
        duration = len(wav_data) / sample_rate
        print(f'Sample rate: {sample_rate} Hz')
        print(f'Total duration: {duration:.2f}s')
        print(f'Size of the input: {len(wav_data)}')
    return ret, waveform, duration_audio, sample_rate


def get_file_paths(folder_path, audio_format):
    """
    This gets the file paths and gets the audio file names along with the path in an array

    :param folder_path: The folder path where
    :param audio_format: Audio format which
    :return: An array of audio file paths
    """
    audio_file_paths = []
    for dir_path, dir_names, file_names in os.walk(folder_path):
        for file_name in [f for f in file_names if f.endswith("." + audio_format)]:
            audio_file_paths.append(os.path.join(dir_path, file_name))
    return audio_file_paths


def class_names_from_csv(class_map_csv_text):
    """Returns list of class names corresponding pip install numpy --upgradeto score vector."""
    class_names = []
    with tf.io.gfile.GFile(class_map_csv_text) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            class_names.append(row['display_name'])
    return class_names


def plot_graph(scores, spectrogram, waveform, class_names, output_path, file_name="dummy.jpg"):
    scores_np = scores.numpy()
    spectrogram_np = spectrogram.numpy()
    plt.figure(figsize=(10, 6))

    # Plot the waveform.
    plt.subplot(3, 1, 1)
    plt.plot(waveform)
    plt.xlim([0, len(waveform)])

    # Plot the log-mel spectrogram (returned by the model).
    plt.subplot(3, 1, 2)
    plt.imshow(spectrogram_np.T, aspect='auto', interpolation='nearest', origin='lower')

    # Plot and label the model output scores for the top-scoring classes.
    mean_scores = np.mean(scores, axis=0)
    top_n = 10
    top_class_indices = np.argsort(mean_scores)[::-1][:top_n]
    plt.subplot(3, 1, 3)
    plt.imshow(scores_np[:, top_class_indices].T, aspect='auto', interpolation='nearest', cmap='gray_r')

    # patch_padding = (PATCH_WINDOW_SECONDS / 2) / PATCH_HOP_SECONDS
    # values from the model documentation
    patch_padding = (0.025 / 2) / 0.01
    plt.xlim([-patch_padding - 0.5, scores.shape[0] + patch_padding - 0.5])
    # Label the top_N classes.
    yticks = range(0, top_n, 1)
    plt.yticks(yticks, [class_names[top_class_indices[x]] for x in yticks])
    _ = plt.ylim(-0.5 + np.array([top_n, 0]))
    plt.savefig(os.path.join(output_path, file_name))


class TagAudioEffects:
    def __init__(self):
        # Model is extracted from Tensorflow hub as sometimes hub does not work.
        self.model = hub.load('models')

    # Find the name of the class with the top score when mean-aggregated across frames.
    def run_model(self, waveform):
        scores, embeddings, spectrogram = self.model(waveform)
        return scores, embeddings, spectrogram

    def get_class_map_path(self):
        return self.model.class_map_path().numpy()


if __name__ == '__main__':
    INPUT_AUDIO_PATH = sys.argv[1]
    INPUT_AUDIO_FORMAT = sys.argv[2]  # "wav
    OUTPUT_DATA_FORMAT = sys.argv[3]  # "default"
    OUTPUT_DATA_PATH = sys.argv[4]
    LOGS = sys.argv[5]
    # All these values (in sec) are from parameter.py of YaMNet
    PATCH_HOP_SECONDS = 0.48
    PATCH_WINDOW_SECONDS = 0.96
    STFT_WINDOW = 0.025
    STFT_HOP = 0.010

    print("Tagging Audio Effects using Yammnet... ")
    tagging_audio_effects = TagAudioEffects()

    # Load Audio Files
    for file_path in get_file_paths(INPUT_AUDIO_PATH, INPUT_AUDIO_FORMAT):
        print("Processing file " + file_path)
        result, converted_wav_data, duration, sample_rate = convert_to_compatible_file(file_path)
        if result == -1:
            print("Error: File not compatible to be processed by model")
            continue
        #ToDo://Check if all supported .seg files are present for output generation

        scores, embeddings, spectrogram = tagging_audio_effects.run_model(converted_wav_data)
        file_path_head, file_name = os.path.split(file_path)
        class_names = class_names_from_csv(tagging_audio_effects.get_class_map_path())
        plot_graph(scores, spectrogram, converted_wav_data, class_names, OUTPUT_DATA_PATH,
                                         os.path.splitext(file_name)[0] + ".jpg")
        data_parser = DataParser(scores, os.path.join(OUTPUT_DATA_PATH,
                                                      os.path.splitext(file_name)[0]),
                                 class_names, INPUT_AUDIO_FORMAT, duration, sample_rate, PATCH_HOP_SECONDS,
                                 PATCH_WINDOW_SECONDS, STFT_HOP, STFT_WINDOW, "DEFAULT")
        data_parser.parse_dump_scores()
        if LOGS: print("Operation complete for file ", file_name)
    print("All operations done ...")
