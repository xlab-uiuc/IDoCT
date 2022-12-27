import os, sys, csv, subprocess
from utils import root_path

def check_result(log, filename, begin_line, end_line):
    with open(filename, 'r') as csvfile:
        csv_reader = list(csv.reader(csvfile, delimiter='\t'))
        for i in range(begin_line-1, end_line):
            line = csv_reader[i]
            if len(line) != 0:
                if (run_ctest(line[3], line[2], line[4], line[6]) == False):
                    log_std_error(filename, log, i, line, "RESULT")

def run_ctest(testName, ParameterName, Value, Result):
    os.chdir(os.path.join(root_path, "run_ctest"))
    cmd = "python3 run_single_ctest.py " + testName + " " + ParameterName + "=" + Value
    try:
        result = subprocess.check_output(cmd, shell=True, executable='/bin/bash').decode("utf-8")
        if Result not in result:
            return False
    except subprocess.CalledProcessError:
        return False
