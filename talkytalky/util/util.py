import os
import errno
import pathlib


def exists(record, field_name):
    """
    Our definition of whether a field exists in a Python dict
    """
    return field_name in record and record[field_name] is not None and record[field_name] != ''


def make_dir(path_name):
    """
    Make a directory and any parent directories.
    Do nothing if already exists.
    :param path_name:
    :return:
    """
    if not os.path.exists(os.path.dirname(path_name)):
        try:
            os.makedirs(os.path.dirname(path_name))
        except OSError as exc:  # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise

def get_project_root():
    """
    It can be problematic to get relative paths depending on where you are running your Python program;
    this will find the root of the project based on the directory name.
    :return:
    """
    project_dir = 'TalkyTalky'
    current_path = str(pathlib.Path().absolute())
    root_path = current_path[:current_path.index(project_dir) + len(project_dir)]
    return root_path

def get_test_root():
    return get_project_root() + "/talkytalky/test"