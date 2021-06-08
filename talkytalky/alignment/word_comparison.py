"""
Word comparison methods: string equality, Levenshtein distance, and soundex
"""
from libindic.soundex import Soundex
from nltk import edit_distance


def words_equal(word1, word2):
    return str.lower(word1.strip()) == str.lower(word2.strip())


def acceptable_levenshtein(word1, word2):
    """
    Generic fuzzy string matcher, looks at number of edits to get from one string to another
    :param word1:
    :param word2:
    :return:
    """
    if words_equal(word1, word2):
        return True
    return edit_distance(str.lower(word1),str.lower(word2)) < 3


def soundex(word1, word2):
    """
    See https://libindic.org/Soundex
    :param word1:
    :param word2:
    :return:
    """
    if words_equal(word1, word2):
        return True
    comparator = Soundex()
    # Result of 1 means sounds the same
    if comparator.compare(word1,word2) == 1:
        return True
    return False

