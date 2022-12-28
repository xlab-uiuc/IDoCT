"""Implements rule checks for the ctest_metadata.csv file."""

import re
from utils import log_std_error, log_warning
from common_checks import (
    check_common_rules,
    check_row_length,
    run_checks,
)


# Contains information and regexes unique to ctest_metadata.csv
meta_data = {
    "columns": [
        "REPO",
        "SHA",
        "CONFIG_PARAMETER",
        "TEST_NAME",
        "VALUE",
        "TYPE(GOOD|BAD)",
        "EXPECTATION(PASS|FAIL)",
    ],
    "Type": [
        "GOOD",
        "BAD",
    ],
    "Expectation": [
        "PASS",
        "FAIL",
    ],
}


def check_type(filename, row, i, log):
    """Check validity of Type."""

    if not row["TYPE(GOOD|BAD)"] in meta_data["Type"]:
        log_std_error(filename, log, i, row, "TYPE(GOOD|BAD)")


def check_expectation(filename, row, i, log):
    """Check validity of Expectation."""

    if not row["EXPECTATION(PASS|FAIL)"] in meta_data["Expectation"]:
        log_std_error(filename, log, i, row, "EXPECTATION(PASS|FAIL)")


def run_checks_pr(log, filename, begin_line, end_line):
    """Checks that the PR is properly formatted."""

    checks = [
        check_row_length,
        check_common_rules,
        check_expectation,
    ]
    run_checks(filename, begin_line, end_line, meta_data, log, checks)
