import itertools
import os
import errno
import pathlib
import re


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
    project_dir = 'talkytalky'
    current_path = str(pathlib.Path().absolute())
    root_path = current_path[:current_path.index(project_dir) + len(project_dir)]
    return root_path

control_chars = ''.join(map(chr, itertools.chain(range(0x00,0x20), range(0x7f,0xa0))))
control_char_re = re.compile('[%s]' % re.escape(control_chars))

def remove_control_chars(s):
    """
    Remove non-printable characters
    Author: Ants Aasma
    https://stackoverflow.com/questions/92438/stripping-non-printable-characters-from-a-string-in-python
    :param s: String to clean
    :return:
    """
    return control_char_re.sub('', s)


def clean_string(s):
    """
    Remove whitespace from front and back as well as control characters
    :param s:
    :return:
    """
    return remove_control_chars(s.strip())


def contains_interesting_text(s):
    """
    Does the text contain some non-control characters?
    :param s:
    :return:
    """
    if s and clean_string(s):
        return True
    return False


def contains_letters(s):
    if s:
        t = re.sub(r'[^A-Za-z0-9]+', '', s)
    return s and t


def normalize_space(s):
    return " ".join(s.split())

