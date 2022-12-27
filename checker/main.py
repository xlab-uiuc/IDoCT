"""Runs the checkers and handles related errors and warnings."""

import sys
import os
import logging
import errorhandler
from pr_checker import run_checks_pr
from utils import log_std_error, log_esp_error, log_warning
from all_parameter_checks import check_whole_parameters
from result_checks import check_result

if __name__ == "__main__":
    # if len(sys.argv) != 4:
    #     print("Usage: python3 main.py <filename> <begin_line> <end_line>")
    #     sys.exit()
    # if int(sys.argv[2]) <= 1:
    #     print("<begin_line> should be greater than 1")
    #     sys.exit()
    # if int(sys.argv[3]) < int(sys.argv[2]):
    #     print("<end_line> should be greater than or equal to <begin_line>")
    #     sys.exit()
    
    error_handler = errorhandler.ErrorHandler()
    stream_handler = logging.StreamHandler(stream=sys.stderr)
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    logger.addHandler(stream_handler)
    log_std_error.tracker = 0
    log_esp_error.tracker = 0
    log_warning.tracker = 0
    checks = [run_checks_pr, check_whole_parameters, check_result]
    for check in checks:
        check(logger, "../new.csv", 2, 3)
    ERROR_COUNT = str(log_std_error.tracker + log_esp_error.tracker)

    if error_handler.fired:
        logger.critical(
            "Failure: Exiting with code 1 due to %s logged %s",
            ERROR_COUNT,
            ("error" if ERROR_COUNT == "1" else "errors"),
        )
        raise SystemExit(1)

    if log_warning.tracker != 0:
        logger.info(
            "%s %s",
            str(log_warning.tracker),
            " warnings generated"
            if log_warning.tracker != 1
            else " warning generated",
        )
    logger.info("Success: Exiting with code 0 due to no logged errors")
