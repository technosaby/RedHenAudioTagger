#!/usr/bin/python
"""
This file do the following
1. Take the input as a folder with audio files (wav, mono, 16k sampling rate) files
2. Take each file and check if they are compatible to the model, else throw error and proceed to the next file
3. Run YaMNet model on that
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
import getopt
from data_parser import DataParser


def ensure_sample_rate(original_sample_rate, waveform, desired_sample_rate=16000):
    """Resample waveform to ensure sampling rate is as expected
    : original_sample_rate: The original sampling rate of the audio file
    : waveform: The actual waveform
    : desired_sample_rate: The desired sampling rate, 16K for YaMNet model
    """
    if original_sample_rate != desired_sample_rate:
        if LOGS:
            print("Sampling rate mismatch, Converting to 16k sampling rate")
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
    sample_rate_wav, wav_data = wavfile.read(audio_path)
    wav_data = ensure_sample_rate(sample_rate_wav, wav_data)
    # ToDo:// Check if the audio is mono else convert to mono, any failure in comparison return -1
    # wav_data = ensure_mono_channel(wav_data)
    # ToDo:// Check if audio format is wav, any failure will return -1
    # wav_data = ensure_wav_format(wav_data)
    # needs to be normalized to values in [-1.0, 1.0]
    waveform = wav_data / tf.int16.max
    duration_audio = len(wav_data) / sample_rate_wav
    total_duration = len(wav_data) / sample_rate_wav

    if LOGS:
        # Show some basic information about the converted audio.
        print(f'Sample rate: {sample_rate_wav} Hz')
        print(f'Total duration: {duration_audio:.2f}s')
        print(f'Size of the input: {len(wav_data)}')
        # Show some basic information about the audio.
        print(f'Sample rate: {sample_rate_wav} Hz')
        print(f'Total duration: {total_duration:.2f}s')
        print(f'Size of the input: {len(wav_data)}')
    return ret, waveform, duration_audio, sample_rate_wav


def get_audio_file_paths(folder_path, audio_format):
    """
    This gets the file paths and gets the audio file names along with the path in an array

    :param folder_path: The folder path where
    :param audio_format: Audio format which
    :return: An array of audio file paths, directory names for the audio files
    """
    audio_file_paths = []
    dir_names_date = []
    for dir_path, dir_names, file_names in os.walk(folder_path):
        for file_name_audio_format in [f for f in file_names if f.endswith("." + audio_format)]:
            dir_names_date.append(dir_path.replace(folder_path, ''))
            audio_file_paths.append(os.path.join(dir_path, file_name_audio_format))
    return audio_file_paths, dir_names_date


def class_names_from_csv(class_map_csv_text):
    """Returns list of class names corresponding pip install numpy --upgrade to score vector."""
    class_names_model = []
    with tf.io.gfile.GFile(class_map_csv_text) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            class_names_model.append(row['display_name'])
    return class_names_model


def plot_graph(scores_graph, spectrogram_graph, waveform, class_names_graph, output_path):
    scores_np = scores_graph.numpy()
    spectrogram_np = spectrogram_graph.numpy()
    plt.figure(figsize=(10, 6))

    # Plot the waveform.
    plt.subplot(3, 1, 1)
    plt.plot(waveform)
    plt.xlim([0, len(waveform)])

    # Plot the log-mel spectrogram (returned by the model).
    plt.subplot(3, 1, 2)
    plt.imshow(spectrogram_np.T, aspect='auto', interpolation='nearest', origin='lower')

    # Plot and label the model output scores for the top-scoring classes.
    mean_scores = np.mean(scores_graph, axis=0)
    top_n = 10
    top_class_indices = np.argsort(mean_scores)[::-1][:top_n]
    plt.subplot(3, 1, 3)
    plt.imshow(scores_np[:, top_class_indices].T, aspect='auto', interpolation='nearest', cmap='gray_r')

    # patch_padding = (PATCH_WINDOW_SECONDS / 2) / PATCH_HOP_SECONDS
    # values from the model documentation
    patch_padding = (0.025 / 2) / 0.01
    plt.xlim([-patch_padding - 0.5, scores_graph.shape[0] + patch_padding - 0.5])
    # Label the top_N classes.
    yticks_graph = range(0, top_n, 1)
    plt.yticks(yticks_graph, [class_names_graph[top_class_indices[x]] for x in yticks_graph])
    _ = plt.ylim(-0.5 + np.array([top_n, 0]))
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    plt.savefig(output_path)


class TagAudioEffects:
    def __init__(self):
        # Model is extracted from Tensorflow hub as sometimes hub does not work.
        self.model = hub.load('https://tfhub.dev/google/yamnet/1')

    # Find the name of the class with the top score when mean-aggregated across frames.
    def run_model(self, waveform):
        return self.model(waveform)

    def get_class_map_path(self):
        return self.model.class_map_path().numpy()


def process_args(argv):
    """
    Process arguments passed to the file
    :param argv: The arguments passed to the file
    :return: Returns the processed variables
    """
    arg_audio_input = ""
    arg_audio_input_format = "wav"
    arg_output = "."
    arg_decimal_places = "2"
    arg_logs = "0"
    arg_plot_graphs = "0"

    arg_help = "{0} -i <audio input path> -a <audio input format (default: wav)> -o <output data path (default: .)> " \
               "-d <decimal places for scores filtering (default : 2)> " \
               "-g <plot graphs(default: 0)> -l <logs enabled (default 0) >".format(argv[0])
    try:
        opts, args = getopt.getopt(argv[1:], "hi:a:o:d:g:l:", ["help", "audio input path=", "audio input format=",
                                                               "output path=", "score round-off=",
                                                               "plot graphs=", "logs="])
    except:
        print(arg_help)
        sys.exit(2)

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print(arg_help)  # print the help message
            sys.exit(2)
        elif opt in ("-i", "--audio input path"):
            arg_audio_input = arg
        elif opt in ("-a", "--audio input format"):
            arg_audio_input_format = arg
        elif opt in ("-o", "--output path"):
            arg_output = arg
        elif opt in ("-d", "--score round-off"):
            arg_decimal_places = arg
        elif opt in ("-g", "--plot graphs"):
            arg_plot_graphs = arg
        elif opt in ("-l", "--logs"):
            arg_logs = arg

    return arg_audio_input, arg_audio_input_format, \
           arg_output, int(arg_decimal_places), int(arg_plot_graphs), int(arg_logs)


if __name__ == '__main__':
    INPUT_AUDIO_PATH, INPUT_AUDIO_FORMAT, OUTPUT_DATA_PATH, SCORE_FILTERING_DECIMAL_PLACES, PLOT_GRAPHS, LOGS = \
        process_args(sys.argv)

    # All these values (in sec) are from parameter.py of YaMNet
    PATCH_HOP_SECONDS = 0.48
    PATCH_WINDOW_SECONDS = 0.96
    STFT_WINDOW = 0.025
    STFT_HOP = 0.010

    if LOGS:
        print("Tagging Audio Effects using YaMNet... ")
        os.environ['TF_CPP_MIN_LOG_LEVEL'] = '0'
    else:
        os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

    tagging_audio_effects = TagAudioEffects()

    # Load Audio Files
    audio_file_path, dir_names_dates = get_audio_file_paths(INPUT_AUDIO_PATH, INPUT_AUDIO_FORMAT)
    # Check if all supported .seg files are present for output generation
    for index, audio_file in enumerate(audio_file_path):
        is_seg_file_present = False
        file_path_head, file_name = os.path.split(audio_file)
        # Check if seg files are present
        seg_file_path = os.path.join(file_path_head, os.path.splitext(file_name)[0] + ".seg")
        if not os.path.exists(seg_file_path):
            if LOGS:
                print(".seg file not present in path " + seg_file_path)
        else:
            is_seg_file_present = True
            if LOGS:
                print(".seg file present, Audio Processing file " + audio_file)

        result, converted_wav_data, duration, sample_rate = convert_to_compatible_file(audio_file)
        if result == -1:
            if LOGS:
                print("Error: File not compatible to be processed by model")
            continue
        scores, embeddings, spectrogram = tagging_audio_effects.run_model(converted_wav_data)

        class_names = class_names_from_csv(tagging_audio_effects.get_class_map_path())

        if PLOT_GRAPHS:
            plot_graph(scores, spectrogram, converted_wav_data, class_names,
                       os.path.join(OUTPUT_DATA_PATH, dir_names_dates[index],
                                    os.path.splitext(file_name)[0] + ".jpg"))
        data_parser = DataParser(scores,
                                 os.path.join(file_path_head,
                                              os.path.splitext(file_name)[0]),
                                 os.path.join(OUTPUT_DATA_PATH, dir_names_dates[index],
                                              os.path.splitext(file_name)[0]),
                                 class_names, INPUT_AUDIO_FORMAT, duration, sample_rate,
                                 SCORE_FILTERING_DECIMAL_PLACES,
                                 is_seg_file_present,
                                 PATCH_HOP_SECONDS,
                                 PATCH_WINDOW_SECONDS, STFT_HOP, STFT_WINDOW, "SFX", LOGS)
        data_parser.parse_dump_scores()
        if LOGS:
            print("Operation complete for file ", file_name)
    if LOGS:
        print("All operations done ...")
