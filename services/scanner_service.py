import json
import logging
import operator
import os
import yaml

from yaml.loader import SafeLoader

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ScannerService:
    """
    Files scanning service
    """

    @staticmethod
    def find_files_names(path: str) -> list:
        """
        Finds all files names in the directory tree
        Parameters
        ----------
        path - path to scan

        Returns
        -------
        list of all files names in the directory tree
        """
        logger.info(f'Looking for file names in: {path}')
        return [os.path.join(dir_path, file) for dir_path, dir_names, filenames in os.walk(path) for file in filenames]

    @staticmethod
    def find_extension(path: str) -> dict:
        """
        Finds all exists extensions in the directory tree
        Parameters
        ----------
        path - path to scan

        Returns
        -------
        dictionary of the existing extension and there amounts, sorted from high to low.
        Exam: {.py: 5, .json: 3, etc.}
        """
        files = ScannerService.find_files_names(path)
        ext_types = {}

        logger.info(f'Looking for extensions in: {path}')

        for file_name in files:
            if os.path.splitext(file_name)[1] not in ext_types:
                ext_types[os.path.splitext(file_name)[1]] = 1
            else:
                ext_types[os.path.splitext(file_name)[1]] += 1

        sorted_tuples = sorted(ext_types.items(), key=operator.itemgetter(1), reverse=True)
        return dict(sorted_tuples)

    @staticmethod
    def find_string(target_string: str, path: str) -> list:
        """
        Searches for the target string

        Returns
        -------
        a list includes desired results | Empty list
        """
        mode = 'r'
        files = ScannerService.find_files_names(path)
        target = []

        logger.info(f'Looking for the word "{target_string}" in: {path}')

        for file in files:
            file_ext = os.path.splitext(file)[1][1:]

            try:
                with open(file, mode) as fp:

                    if file_ext in ['', 'py', 'txt', 'ini', 'lock', 'md', 'cfg']:
                        contents = fp.readline()

                    elif file_ext in ['json']:
                        contents = json.load(fp)

                    elif file_ext in ['yml', 'yaml']:
                        contents = yaml.load(fp, Loader=SafeLoader)

                    # elif file_ext in ['png']:
                    #     img = cv2.imread(file)
                    #     cv2.imshow('image', img)

                    while contents != "":
                        if target_string in contents:
                            target.append(contents.strip())
                        contents = fp.readline()

            except (EOFError, IOError) as e:
                logger.error(f'Error occurred: {str(e)}')
                raise {"ScannerService - scan file failed": str(e)}

        return target
