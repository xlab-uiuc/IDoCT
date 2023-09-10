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
        "RESULT(PASS|FAIL)",
        "COVERAGE_CHANGE(YES|NO)",
    ],
    "Type": [
        "GOOD",
        "BAD",
    ],
    "Result": [
        "PASS",
        "FAIL",
    ],
    "Coverage change": [
        "YES",
        "NO",
    ],
}


def check_type(filename, row, i, log):
    """Check validity of Type."""

    if not row["TYPE(GOOD|BAD)"] in meta_data["Type"]:
        log_std_error(filename, log, i, row, "TYPE(GOOD|BAD)")


def check_result(filename, row, i, log):
    """Check validity of Expectation."""

    if not row["RESULT(PASS|FAIL)"] in meta_data["Result"]:
        log_std_error(filename, log, i, row, "RESULT(PASS|FAIL)")


def check_coverage(filename, row, i, log):
    """Check validity of Expectation."""

    if not row["COVERAGE_CHANGE(YES|NO)"] in meta_data["Coverage change"]:
        log_std_error(filename, log, i, row, "COVERAGE_CHANGE(YES|NO)")
        
def run_checks_pr(log, filename):
    """Checks that pr-data.csv is properly formatted."""

    checks = [
        check_row_length,
        check_common_rules,
        check_type,
        check_result,
        check_coverage,
    ]
    run_checks(filename, meta_data, log, checks)
