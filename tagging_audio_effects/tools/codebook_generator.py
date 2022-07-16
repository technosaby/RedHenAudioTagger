"""
This file will take the class map of YaMNet and generate a codebook for RedHen's reference.
"""
import csv

if __name__ == '__main__':
    YAMNET_CLASS_MAP_FILE = "../models/assets/yamnet_class_map.csv"
    OUTPUT_FILE = "../codebook/codebook_yamnet_1.0.csv"
    print("Generating codebook from ", YAMNET_CLASS_MAP_FILE)
    input_file = open(YAMNET_CLASS_MAP_FILE, 'r')
    output_file = open(OUTPUT_FILE, 'w')
    data = csv.reader(input_file)
    writer = csv.writer(output_file)

    for line in data:
        line.pop(1)  # For removing the 'mid' field as it is not required in codebook
        line = [value.replace(',', ' |') for value in line]
        writer.writerow(line)

    # Closing the files
    input_file.close()
    output_file.close()

    print("Codebook generation complete at ", OUTPUT_FILE)
