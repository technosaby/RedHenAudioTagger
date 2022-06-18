import numpy as np
import csv
# This file will parse the data and show in the required formats
# The data will be frame by frame scores which is received by Yamnet model
# This frame scores will be parsed in the required formats needed by Redhen for reporting

class DataParser:
    def __init__(self, scores, file_name, class_names, format="DEFAULT"):
        self.scores = np.array(scores)
        self.format = format
        self.class_names = class_names
        self.file_name = file_name

    def parse_dump_scores(self):
        derived_classes = [self.class_names[i] for i in np.argmax(self.scores, axis=1)]
        derived_class_timings = [0.96*i for i in range(1, len(derived_classes))]

        if self.format == "DEFAULT":
            with open(self.file_name + '.sfx', 'w') as f:
                f.write("File Name " + self.file_name +"\n")
                f.write("==============================================")
                writer = csv.writer(f)
                writer.writerows(zip(derived_class_timings, derived_classes))

        elif self.format == "ELAN_EAF":
            #ToDO:// Discuss with mentors about this
            pass
        else:
            print("Please use specified formats")
