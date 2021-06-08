import itertools
import re

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

