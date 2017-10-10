from os import listdir
from os.path import isfile, join

import glob


def get_files(directory):
    onlyfiles = [f for f in listdir(directory) if isfile(join(directory, f))]
    print(onlyfiles)


def get_pattern(directory, pattern):
    if pattern:
        file_path = directory + pattern
        print(glob.glob(file_path))
    else:
        print(glob.glob(directory + "*.*"))


if __name__ == '__main__':
    FILE_PATH = "/Users/labattula/Documents/lakshman/Personal Folders/pythonWork/project37/awsiotcerts/"
    get_files(FILE_PATH)

    get_pattern(FILE_PATH, pattern='*.pem')
    get_pattern(FILE_PATH, pattern='*-private.pem.key')
    get_pattern(FILE_PATH, pattern='*-certificate.pem.crt')
