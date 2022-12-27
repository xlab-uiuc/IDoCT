import csv
import json
import os
import sys
from collections import defaultdict
from utils import log_esp_error, root_path

test_parameter_mapping = defaultdict(set)

def check_whole_parameters(log, filename, begin_line, end_line):
    with open(filename, 'r') as csvfile:
        csv_reader = list(csv.reader(csvfile, delimiter='\t'))
        for i in range(begin_line-1, end_line):
            line = csv_reader[i]
            if len(line) != 0:
                test_parameter_mapping[line[3]].add(line[2])

    with open(os.path.join(root_path, "generate_mapping/results/hadoop-common/param_unset_getter_map.json")) as f:
        mapping = json.load(f)
        for i in test_parameter_mapping.keys():
            if len(test_parameter_mapping[i]-set(mapping[i])) != 0:
                log_esp_error(filename, log, f"For test {i}, these parameters are not in the mapping: " + str(test_parameter_mapping[i]-set(mapping[i])))
            if len(set(mapping[i])-test_parameter_mapping[i]) != 0:
                log_esp_error(filename, log, f"For test {i}, these parameters are missed in the result: " + str(set(mapping[i])-test_parameter_mapping[i]))
