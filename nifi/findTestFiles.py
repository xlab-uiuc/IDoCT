import os
import constants

def is_test_file(path):
    return path.endswith("Test.java")

def find_all_tests_path():
    res = []
    directory = constants.NIFI_COMMONS_PATH
    for root, dirs, files in os.walk(directory):
        for filename in files:

            if is_test_file(filename):
                res.append(os.path.join(root, filename))
    with open(constants.ALL_TESTS_PATH, 'w') as fp:
        for item in res:
            # write each path on a new line
            fp.write("%s\n" % item)


if __name__ == "__main__":
    find_all_tests_path()