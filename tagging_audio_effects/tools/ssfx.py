import sys
import json
from collections import OrderedDict

def get_time_interval_tags(scores_dict, tag_combinations, time_windows_indices, logic):
    result = []
    for index, window in enumerate(time_windows_indices):
        if logic == "and":
            search_not_found = False
            for tag in tag_combinations:
                matching_idx = [idx for idx, s in enumerate(list(scores_dict.values())[window[0]:window[1]]) if tag in s]
                if len(matching_idx) == 0:
                    break
                else:
                    scores_dict.keys()

                # if tag not in list(scores_dict.values())[window[0]:window[1]]:
                #     search_not_found = True
                #     break
                # else:
                #    result.append(index)


# ssfx -r —files /tv/2022/2022-03/20220305 —effects{{drum|percussion}&{laughter}} —within 5

if __name__ == '__main__':
    # FILE_LOCATION = sys.argv[1]
    # START_DATE = sys.argv[2]
    # END_DATE = sys.argv[3]
    # EFFECTS = sys.argv[4]
    # TIME_DURATION = sys.argv[5]
    # LOGS = sys.argv[6]

    FILE_LOCATION = "/Users/saby/Documents/RedHen/Baselining/TaggedAudioFiles/2010-01-01_2335_US_CSPAN2_World_War_II.sfx"
    START_DATE = "2010-01-01"
    END_DATE = "2010-01-01"
    EFFECTS = ["Narration", "Child speech"]
    TIME_DURATION = 5
    LOGS = 1
    starting_line = 13
    line_split_separator = "SFX_01"
    file_name_text = "201001012335"
    print("Starting the filtering script ...")
    score_data = []
    times = []
    dict_times_score = OrderedDict()
    with open(FILE_LOCATION) as f:
        lines = f.readlines()
        for line in lines[13:]:
            split_line = line.split(line_split_separator)
            dict_times_score[split_line[0].rstrip("|").split("|")[1].replace(file_name_text, '')] = split_line[1].lstrip("|")

    # Creating time windows
    time_windows_indices = [(i, TIME_DURATION + i) for i in range(0, int(float(list(dict_times_score.keys())[-1])))]

    #ToDo:// create tags
    tag_combinations = ["Narration, Child speech"] #[["Narration", "Child speech"], ["Narration", "kid speaking"]]
    selected_tags = []

    # For each window find the tags
    time_intervals = get_time_interval_tags(dict_times_score, tag_combinations, time_windows_indices, "and")
    # for index, window in enumerate(time_windows_indices):
    #     filtered_scores = score_data[window[0] : window[1]]
    #     found = False
    #     # For And logic
    #     indices, times = verify_tag_presence(filtered_scores, tag_combinations, "and")

    # Extract Data

    #ToDo:// Write Data in csv
    print("All Done ...")