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


def check_header(header, valid_dict, filename, log):
    """Validates that the header is correct."""

    if not header == valid_dict["columns"]:

        # Check that columns are properly formatted
        log_esp_error(filename, log, "The header is improperly formatted")


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


def check_row_length(header_len, filename, row, i, log):
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


def run_checks(file, data_dict, log, checks):
    """Checks rule compliance for any given dataset file."""

    with open(file, newline="") as csvfile:
        info = csv.DictReader(csvfile, data_dict["columns"])
        header = next(info)
        check_header(list(header.values()), data_dict, file, log)
        for i, row in enumerate(info):
            i += 2
            line = str(i)

            params = [file, row, line, log]
            for check_rule in checks:
                if check_rule.__name__ == check_row_length.__name__:
                    check_rule(len(header), *params)
                    continue
                check_rule(*params)


    with open(file, 'rb') as fp:
        for line in fp:
            if line.endswith(b'\r\n'):
                log_esp_error(file, log, "Incorrect End of Line encoding")
                break
