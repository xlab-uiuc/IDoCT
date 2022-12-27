"""Contains helper functions used in other modules."""

import os
import re
import subprocess

checker_path = os.path.dirname(os.path.abspath(__file__))
root_path = os.path.join(checker_path, "..")

def log_info(filename, log, message):
    """Logs a merely informational message."""

    log.info("INFO: On file " + filename + ": " + message)


def log_std_error(filename, log, line, row, key):
    """Logs a standard error."""

    log_std_error.tracker += 1
    log.error(
        "ERROR: On file "
        + filename
        + ", row "
        + line
        + ":\n"
        + "Invalid "
        + key
        + ': "'
        + row[key]
        + '"'
    )


def log_esp_error(filename, log, message):
    """Logs a special error."""

    log_esp_error.tracker += 1
    log.error("ERROR: On file " + filename + ": " + message)


def log_warning(filename, log, line, message):
    """Logs a warning."""

    log_warning.tracker += 1
    log.warning(
        "WARNING: On file " + filename + ", row " + line + ": \n" + message
    )
