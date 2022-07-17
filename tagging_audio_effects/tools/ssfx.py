"""
This file parsers the metadata file (.sfx) file to filter tags.
 - It filters only single tags and gives the timestamp with the scores for that tag.
 - Currently, it only filters a single tag within a timeframe.
 - In the future, we need to implement an advanced filtering mechanism using logical operations (&, | etc).
"""

import collections
import sys
import os
from collections import OrderedDict
import numpy as np
import pandas as pd
from subprocess import PIPE, run
import json
import sh

def process_tag_result(result_dictionary, scores_dict):
    for tag in result_dictionary:
        result_dictionary[tag] = sorted(set([elem for sublist in result_dictionary[tag] for elem in sublist]))
    df = pd.DataFrame(columns=['Tags', 'Time', 'Score'])
    for tag, times in result_dictionary.items():
        for time in times:
            df.loc[len(df.index)] = [tag, time, [score for score in scores_dict[time].split(",") if tag in score][0]]
    return df


def get_time_interval_tags(scores_dict, tag_query):
    df = pd.DataFrame(columns=['Score'])
    for time, scores in scores_dict.items():
        json_data = json.loads(scores)
        temp_dict = {}
        ##ToDo:// Find correct way of doing this using jq (get the key for the filter).
        # Current way is crude
        for data in json_data:
            temp_dict[data] = "{" + data + ":" + json_data[data] + "}"
            # json_data[data] = "{" + data + ":" + json_data[data] + "}"
        result = run(["jq", "-cn", json.dumps(temp_dict) + '|' + tag_query, ], stdout=PIPE, stderr=PIPE,
                     universal_newlines=True)
        if result.stdout:
            df.loc[time] = result.stdout

    # matching_idx = [idx for idx, s in enumerate(list(scores_dict.values())[window[0]:window[1]]) if
    #                 tag in s]
    # if len(matching_idx) != 0:
    #     result[tag].append(np.array(list(scores_dict.keys())).take(np.array(matching_idx) + window[0]))
    # df = process_tag_result(result, scores_dict)
    return df


def get_sfx_files(folder_path, date, sfx_files_with_path):
    sfx_format = "sfx"
    for dir_path, dir_names, file_names in os.walk(folder_path):
        for file_name in [f for f in file_names if f.endswith("." + sfx_format) and f.startswith(str(date).split()[0])]:
            sfx_files_with_path.append(os.path.join(dir_path, file_name))
    return sfx_files_with_path


# ToDo:// create tags
def get_tag_combinations(audio_effects):
    return audio_effects


def is_starting_line(line):
    if line.startswith("FFS"):
        return True


def filter_sfx_file(sfx_file, tags_query):
    dict_times_score = OrderedDict()
    with open(sfx_file) as f:
        lines = f.readlines()
        start_read = False
        for line in lines:
            if not start_read and is_starting_line(line):
                start_read = True
                continue
            if start_read:
                split_line = line.split(line_split_separator)
                dict_times_score[split_line[0].rstrip("|").split("|")[1].replace(file_name_text, '')] = split_line[
                    1].lstrip("|")
    # For each window find the tags
    df = get_time_interval_tags(dict_times_score, tags_query)
    return df


# ssfx -r —files /tv/2022/2022-03/20220305 —effects{{drum|percussion}&{laughter}} —within 5

if __name__ == '__main__':
    FILE_LOCATION = sys.argv[1]
    START_DATE = sys.argv[2]
    END_DATE = sys.argv[3]
    EFFECTS_QUERY = sys.argv[4]
    LOGS = int(sys.argv[5])

    # FILE_LOCATION = "/Users/saby/Documents/RedHen/Baselining/TaggedAudioFiles/"
    # START_DATE = "2022-01-01"
    # END_DATE = "2022-11-01"
    # EFFECTS_QUERY = '(.Music // .song //.background), (.Television // .Tv)'
    # LOGS = 1

    # Code Starts from here ....
    line_split_separator = "SFX_01"

    date_range = pd.date_range(start=START_DATE, end=END_DATE)
    sfx_files_with_path = []
    for date in date_range:
        sfx_files_with_path = get_sfx_files(FILE_LOCATION, date, sfx_files_with_path)  # Get SFX files

    for index, sfx_file in enumerate(sfx_files_with_path):
        csv_file_name = os.path.split(sfx_files_with_path[index])[1].replace(".sfx", ".csv")
        file_name = os.path.split(sfx_files_with_path[index])[1].replace(".sfx", "")
        file_name_text = "-".join(file_name.split("_", 2)[:2]).replace("-", "")
        if LOGS: print("Starting the filtering script for filename ", sfx_file)
        df = filter_sfx_file(sfx_file, EFFECTS_QUERY)
        # Dump Dataframe to CSV
        df.to_csv(csv_file_name)
        if LOGS: print("Operation completed for sfx file ", sfx_file)
    if LOGS: print("All Done ...")
