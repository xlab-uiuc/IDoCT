"""Contains implementations of rules that are common to all dataset files"""

import re
import csv
import subprocess
from utils import (
    log_info,
    log_std_error,
    log_esp_error,
)

# Contains regexes for columns that are commmon to ctest_metadata
common_data = {
    "REPO": re.compile(r"^https://github.com/apache/hadoop.git$"),
    "SHA": re.compile(r"^a3b9c37a397ad4188041dd80621bdeefc46885f2$"),
    "TEST_NAME": re.compile(r"^.*#.*$"),
}

def check_common_rules(filename, row, i, log):
    """
    Checks validity of REPO, SHA,
    TEST_NAME (packageName.className#methodName).
    """

    if not common_data["REPO"].fullmatch(row["REPO"]):
        log_std_error(filename, log, i, row, "REPO")
    if not common_data["SHA"].fullmatch(row["SHA"]):
        log_std_error(filename, log, i, row, "SHA")
    if not common_data["TEST_NAME"].fullmatch(row["TEST_NAME"]):
        log_std_error(filename, log, i, row, "TEST_NAME")


def check_row_length(filename, row, i, log, header_len=7):
    """Checks that each row has the required length."""

    if len(row) != header_len:
        log_esp_error(
            filename,
            log,
            "On row "
            + str(i)
            + ", row length should be "
            + str(header_len)
            + " but is "
            + str(len(row)),
        )


def check_REPO(filename, row, i, log):
    """Checks that the REPO is correct."""

    if row["REPO"] != "https://github.com/apache/hadoop.git":
        log_std_error(filename, log, i, row, "REPO")


def check_SHA(filename, row, i, log):
    """Checks that the SHA is correct."""

    if row["SHA"] != "a3b9c37a397ad4188041dd80621bdeefc46885f2":
        log_std_error(filename, log, i, row, "SHA")


def check_repeat(filename, log, data_dict, begin_line, end_line):
    """Checks that no {test, parameter} is repeated in the file."""
    exist_map = set()
    with open(filename, newline="") as csvfile:
        info = csv.DictReader(csvfile, data_dict["columns"], delimiter='\t')
        for j in range(2, begin_line-1):
            content = next(info)
            exist_map.add((content["TEST_NAME"], content["CONFIG_PARAMETER"]))
        for j in range(begin_line, end_line+1):
            content = next(info)
            if (content["TEST_NAME"], content["CONFIG_PARAMETER"]) in exist_map:
                log_esp_error(
                    filename,
                    log,
                    "Test "
                    + content["TEST_NAME"] 
                    + " with parameter "
                    + content["CONFIG_PARAMETER"]
                    + " is repeated",
                )
            else:
                exist_map.add((content["TEST_NAME"], content["CONFIG_PARAMETER"]))


def run_checks(file, begin_line, end_line, data_dict, log, checks):
    """Checks rule compliance for any given dataset file."""

    with open(file, newline="") as csvfile:
        info = csv.DictReader(csvfile, data_dict["columns"], delimiter='\t')
        for i in range(begin_line-1):
            next(info)

        for i in range(end_line-begin_line+1):
            line = str(begin_line+i)
            content = next(info)
            params = [file, content, line, log]
            for check_rule in checks:
                check_rule(*params)

    check_repeat(file, log, data_dict, begin_line, end_line)

    with open(file, 'rb') as fp:
        for line in fp:
            if line.endswith(b'\r\n'):
                print(line)
                log_esp_error(file, log, "Incorrect End of Line encoding")
                break
