import constants
import os
import json

res = {}

def params_in_report(report_path):
    params = []
    report = open(report_path, 'r')
    Lines = report.readlines()
    for line in Lines:
        line = line.strip()
        info = line.split(',')
        params.append(info[constants.PRAM_IDX])
    return params



def parse_and_run_test(test_path):
    test = open(test_path, 'r')
    Lines = test.readlines()
    cur_test_file = None
    report_path = None
    for i, line in enumerate(Lines):
        # remove line breaks
        line = line.strip()
        if i == 0:
            cur_test_file = line
        elif i == 1:
            report_path = line
        else:
            cur_test_name = cur_test_file+"#"+line
            # run the test
            command = constants.CD_NIFI_PATH
            command += constants.MVN_INSTALL_NIFI_COMMONS
            command += 'mvn -pl nifi-commons/nifi-properties/ test -Dtest="'+cur_test_name+'"'
            os.system(command)

            # get params
            params = params_in_report(report_path)
            res[cur_test_name] = params.copy()
    
def output_res(output_path):
    json.dump(res, open(output_path, "w"), indent=2)

if __name__ == "__main__":
    parse_and_run_test(constants.TEST_INFO_PATH)
    output_res(constants.OUTPUT_PATH)
