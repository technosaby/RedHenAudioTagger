"""
This file parsers the metadata file (.sfx) file to filter tags.
 - It filters only single tags and gives the timestamp with the scores for that tag.
 - Currently, it only filters a single tag within a timeframe.
 - It takes a JQ query and filters the scores based on the query
"""
import getopt
import json
import os
import sys
from collections import OrderedDict
from subprocess import PIPE, run

import pandas as pd


def filter_scores_on_tag_query(scores_dict, tag_query):
    """
    This block uses jq query and run it on single line of scores in SFX file to get the filtered tags and
    scores based on the tag query

    :param scores_dict: The scores in the form of a JSON
    :param tag_query: The query in the form of a JQ query
    :return: Filtered tags in a dataframe
    """
    df_score = pd.DataFrame(columns=['Score'])
    for time, scores in scores_dict.items():
        json_data = json.loads(scores)
        temp_dict = {}
        # ToDo:// Find correct way of doing this using jq (get the key for the filter). Current way is crude
        for data in json_data:
            temp_dict[data] = "{" + data + ":" + json_data[data] + "}"
        result = run(["jq", "-cn", json.dumps(temp_dict) + '|' + tag_query, ], stdout=PIPE, stderr=PIPE,
                     universal_newlines=True)
        # Removing nulls and new lines from filtered results
        processed_result = result.stdout.replace("null", '')
        processed_result = processed_result.replace("\n", '')
        if processed_result:
            df_score.loc[time] = processed_result
    return df_score


def get_sfx_files(folder_path, sfx_files, date_filter=None, sfx_format="sfx"):
    """
    This function filters all the sfx files based on dates present in a folder

    :param sfx_files: The filtered list where filtered data is appended
    :param folder_path: Path of the folder where sfx files are present
    :param date_filter: The date based on which filtering is done
    :param sfx_format: The extension of the sfx file
    :return: The list of sfx files
    """

    for dir_path, dir_names, file_names in os.walk(folder_path):
        if date_range == None:
            for file_name_sfx in [f for f in file_names if f.endswith("." + sfx_format)]:
                sfx_files.append(os.path.join(dir_path, file_name_sfx))
        else:
            for file_name_sfx in [f for f in file_names if f.endswith("." + sfx_format) and
                                                           f.startswith(str(date_filter).split()[0])]:
                sfx_files.append(os.path.join(dir_path, file_name_sfx))
    return sfx_files


def is_starting_line(line):
    """
    Based on this tag the SFX file filtering starts and scores are collected after this line
    :param line: A line from the SFX file
    :return: If the line contains FFS tag
    """
    if line.startswith("FFS"):
        return True


def filter_sfx_file(sfx_file_for_filter, tags_query):
    """
    This function takes an SFX file abd processes each line, extracts the scores in JSON format and prepares it for
    further processing for the filtration based on tag query
    :param sfx_file_for_filter: The sfx file which needs to be processed
    :param tags_query: The tag query in JQ format
    :return:
    """
    dict_times_score = OrderedDict()
    with open(sfx_file_for_filter) as f:
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
    df_filtered_result = filter_scores_on_tag_query(dict_times_score, tags_query)
    return df_filtered_result


def process_args(argv):
    """
    Process arguments passed to the file
    :param argv: The arguments passed to the file
    :return: Returns the processed variables
    """
    arg_input = ""
    arg_query = ""
    arg_start_date = ""
    arg_end_date = ""
    arg_logs = "0"

    arg_help = "{0} -i <tagged files> -s <start date> -e <end date> -q <JQ Query> " \
               "-l <logs enabled (default 0) >".format(argv[0])
    try:
        opts, args = getopt.getopt(argv[1:], "hi:s:e:q:l:", ["help", "tagged files path=", "start date=",
                                                             "end date=", "query=", "logs="])
    except:
        print(arg_help)
        sys.exit(2)

    if len([ext for ext in opts if "-q" in ext]) > 0: # If query is not given don't continue
        for opt, arg in opts:
            if opt in ("-h", "--help"):
                print(arg_help)  # print the help message
                sys.exit(2)
            elif opt in ("-i", "--tagged files path"):
                arg_input = arg
            elif opt in ("-s", "--start date"):
                arg_start_date = arg
            elif opt in ("-e", "--end date"):
                arg_end_date = arg
            elif opt in ("-q", "--query"):
                arg_query = arg
            elif opt in ("-l", "--logs"):
                arg_logs = arg
    else:
        print(arg_help)
        sys.exit(2)

    return arg_input, arg_start_date, arg_end_date, arg_query, int(arg_logs)


if __name__ == '__main__':
    FILE_LOCATION, START_DATE, END_DATE, EFFECTS_QUERY, LOGS = process_args(sys.argv)

    # Code Starts from here ....
    line_split_separator = "SFX_01"
    sfx_files_with_path = []
    if START_DATE == '' and END_DATE == '':
        date_range = None
        sfx_files_with_path = get_sfx_files(FILE_LOCATION, sfx_files_with_path)
    else:
        date_range = pd.date_range(start=START_DATE, end=END_DATE)
        for date in date_range:
            sfx_files_with_path = get_sfx_files(FILE_LOCATION, sfx_files_with_path, date)  # Get SFX files

    for index, sfx_file in enumerate(sfx_files_with_path):
        csv_file_name = os.path.split(sfx_files_with_path[index])[1].replace(".sfx", ".csv")
        file_name = os.path.split(sfx_files_with_path[index])[1].replace(".sfx", "")
        file_name_text = "-".join(file_name.split("_", 2)[:2]).replace("-", "")
        if LOGS:
            print("Starting the filtering script for filename ", sfx_file)
        df = filter_sfx_file(sfx_file, EFFECTS_QUERY)
        # Dump Dataframe to CSV
        df.to_csv(csv_file_name)
        if LOGS:
            print("Operation completed for sfx file ", sfx_file)
    if LOGS:
        print("All Done ...")
