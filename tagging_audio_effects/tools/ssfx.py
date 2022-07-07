import collections
import sys
import os
from collections import OrderedDict
import numpy as np
import pandas as pd
from datetime import datetime


def process_tag_result(result_dictionary, scores_dict):
    for tag in result_dictionary:
        result_dictionary[tag] = sorted(set([elem for sublist in result_dictionary[tag] for elem in sublist]))
    df = pd.DataFrame(columns=['Tags', 'Time', 'Score'])
    for tag, times in result_dictionary.items():
        for time in times:
            df.loc[len(df.index)] = [tag, time, scores_dict[time]]
    return df


def get_time_interval_tags(scores_dict, tag_combinations, time_windows_indices, logic):
    result = collections.defaultdict(list)
    for index, window in enumerate(time_windows_indices):
        if logic == "and":
            for tag in tag_combinations:
                matching_idx = [idx for idx, s in enumerate(list(scores_dict.values())[window[0]:window[1]]) if
                                tag in s]
                if len(matching_idx) == 0:
                    break
                else:
                    result[tag].append(np.array(list(scores_dict.keys())).take(np.array(matching_idx) + window[0]))
    df = process_tag_result(result, scores_dict)
    return df


def get_sfx_files(folder_path, date,  sfx_files_with_path, dir_names_date):
    sfx_format = "sfx"
    for dir_path, dir_names, file_names in os.walk(folder_path):
        for file_name in [f for f in file_names if f.endswith("." + sfx_format) and f.startswith(str(date).split()[0])]:
            sfx_files_with_path.append(os.path.join(dir_path, file_name))
            dir_names_date.append(dir_path.replace(folder_path, ''))
    return sfx_files_with_path, dir_names_date

# ssfx -r —files /tv/2022/2022-03/20220305 —effects{{drum|percussion}&{laughter}} —within 5

if __name__ == '__main__':
    # FILE_LOCATION = sys.argv[1]
    # START_DATE = sys.argv[2]
    # END_DATE = sys.argv[3]
    # EFFECTS = sys.argv[4]
    # TIME_DURATION = sys.argv[5]
    # LOGS = sys.argv[6]

    FILE_LOCATION = "/Users/saby/Documents/RedHen/Baselining/TaggedAudioFiles/"
    START_DATE = "2011-01-01"
    END_DATE = "2021-01-01"
    EFFECTS = ["Narration", "Child speech"]
    TIME_DURATION = 500
    LOGS = 1

    # Code Starts from here ....
    starting_line = 13
    line_split_separator = "SFX_01"

    date_range = pd.date_range(start=START_DATE, end=END_DATE)
    sfx_files_with_path = []
    dir_names_date = []
    for date in date_range:
        sfx_files_with_path, dir_names_date = get_sfx_files(FILE_LOCATION, date, sfx_files_with_path, dir_names_date)  # Get SFX files

    for index, sfx_file in enumerate(sfx_files_with_path):
        pass
    csv_file_name = "2010-01-01_2335_US_CSPAN2_World_War_II_TAGS.csv"
    file_name_text = "201001012335"
    print("Starting the filtering script ...")
    score_data = []
    times = []
    dict_times_score = OrderedDict()
    with open(FILE_LOCATION) as f:
        lines = f.readlines()
        for line in lines[starting_line:]:
            split_line = line.split(line_split_separator)
            dict_times_score[split_line[0].rstrip("|").split("|")[1].replace(file_name_text, '')] = split_line[
                1].lstrip("|")

    # Creating time windows
    time_windows_indices = [(i, TIME_DURATION + i) for i in range(0, int(float(list(dict_times_score.keys())[-1])))]
    # ToDo:// create tags
    tag_combinations = []
    tag_combinations.append("Narration")
    tag_combinations.append("Child speech")  # [["Narration", "Child speech"], ["Narration", "kid speaking"]]
    selected_tags = []
    # For each window find the tags
    df = get_time_interval_tags(dict_times_score, tag_combinations, time_windows_indices, "and")
    # Dump to CSV
    df.to_csv(csv_file_name)
    print("All Done ...")
