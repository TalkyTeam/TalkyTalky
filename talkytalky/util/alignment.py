from typing import List

from libindic.soundex import Soundex
from nltk import edit_distance
from nltk.translate.gale_church import align_blocks

from talkytalky.util import html, asr_json
from talkytalky.util.util import contains_letters

WORD_LENGTH = 1
CHAR_LENGTH = 2

def align_trans_to_html_files(trans_in_file_path, html_in_file, html_out_file, match_criteria=WORD_LENGTH):
    """
    Given a transcription file and an HTML file, return the sentences aligned and write the span-id labelled
    sentence HTML file to a new file
    :param trans_in_file_path:
    :param html_in_file:
    :param html_out_file:
    :return: List of tuples, HTML Sentence to Transcript Sentence
    """
    with open(trans_in_file_path, 'r') as trans_in_file:
        transcript = asr_json.load(trans_in_file)
        html_document = html.assign_sentence_ids(html_in_file, html_out_file)
        return align_trans_to_html_sentences(transcript.sentences, html_document.sentences, match_criteria=match_criteria)


def align_trans_to_html_sentences(transcript_sentences, html_sentences, match_criteria=WORD_LENGTH):
    """
    Does sentence-level alignment on the transcript and html file.
    Susceptible to inaccurate sentence boundaries.
    :param transcript_sentences: List of sentences in the transcript
    :param html_sentences: List of sentences in the HTML
    :param match_criteria: Length-based, # of words in a sentence, or # of characters? (WORD_LENGTH or CHAR_LENGTH)
    :return:
    """
    if match_criteria == CHAR_LENGTH:
        transcript_lengths = list(map(lambda s: s.word_count, transcript_sentences))
        html_sentence_lengths = list(map(lambda s: s.word_count, html_sentences))
    else:
        transcript_lengths = list(map(lambda s: s.character_count, transcript_sentences))
        html_sentence_lengths = list(map(lambda s: s.character_count, html_sentences))

    result = align_blocks(html_sentence_lengths, transcript_lengths)
    print(transcript_lengths)

    print(html_sentence_lengths)

    print(result)
    sentence_pairs = []
    for sentence_index_pair in result:
        sentence_pair = (html_sentences[sentence_index_pair[0]],
                         transcript_sentences[sentence_index_pair[1]])
        sentence_pairs.append(sentence_pair)

    return sentence_pairs


def align_using_lcs_words(trans_in_file, html_in_file, html_out_file, string_comparison):
    html_document = html.assign_sentence_ids(html_in_file, html_out_file)
    transcript = asr_json.loadf(trans_in_file)
    return html_document, lcs(html_document, transcript, string_comparison)


def lcs(html_document, transcript, string_equality):
    """
    Set up and call the longest common subsequence method to get the common words in
    the transcript and HTML document
    :param html_document:
    :param transcript:
    :param string_equality:
    :return: List of LCS objects that contain paired words
    """
    memo_table = lcs_memo(html_document, transcript, string_equality)
    #print([memo_table, html_document, transcript, len(html_document.items), len(transcript.items)])
    aligned_word_list = backtrack(memo_table, html_document, transcript, len(html_document.items), len(transcript.items), string_equality)
    return aligned_word_list


def lcs_memo(html_document, transcript, string_equality):
    """
    Canonical example of dynamic programming
    Literally taken from Wikipedia, although they chose C# for some reason:
    https://en.wikipedia.org/wiki/Longest_common_subsequence_problem
    and here
    https://www.geeksforgeeks.org/longest-common-subsequence-dp-4/
    :param html_document: Data structure with sentences and items (words)
    :param transcript:
    :param string_equality:
    :return:
    """
    # find the length of the strings 
    html_num_words = len(html_document.items)
    print("# HTML words " + str(html_num_words))
    transcript_num_words = len(transcript.items)
    print("# transcript words " + str(transcript_num_words))

    # Create the dynamic programming table
    lcs_memo_table = [[0] * (transcript_num_words + 1) for html_word_index in range(html_num_words + 1)]
    # print(lcs_memo_table)

    '''
    Following steps build lcs_memo_table[html_num_words + 1][transcript_num_words + 1] in bottom up fashion 
    Note: lcs_memo_table[html_word_index][transcript_word_index] contains length of LCS of X[0..html_word_index-1] 
    and Y[0..transcript_word_index-1]
    '''
    for i in range(1,html_num_words):
        for j in range(1,transcript_num_words):
            if i == 0 or j == 0:
                lcs_memo_table[i][j] = 0
            elif not(contains_letters(html_document.items[i - 1].content)) \
                     or not(contains_letters(transcript.items[j - 1].content)):
                lcs_memo_table[i][j] = \
                    max(lcs_memo_table[i][j - 1],
                    lcs_memo_table[i - 1][j])
            elif string_equality(html_document.items[i - 1].content,
                             transcript.items[j - 1].content):
                lcs_memo_table[i][j] = \
                    (lcs_memo_table[i - 1][j - 1]) + 1
            else:
                # lcs_memo_table[html_num_words][transcript_num_words] contains the length of LCS of
                # html_document.items[0..transcript_num_words-1] transcript.items Y[0..html_num_words-1]
                lcs_memo_table[i][j] = \
                    max(lcs_memo_table[i][j - 1],
                        lcs_memo_table[i - 1][j])

    print("Longest substring has number terms: %s", str(lcs_memo_table[html_num_words - 1][transcript_num_words - 1]))
    return lcs_memo_table


def backtrack(lcs_memo_table, html_document, transcript, html_num_words, transcript_num_words, string_equality):
    """
    Because the recursive backtrack literally ran out of Python stack...
    See https://www.geeksforgeeks.org/printing-longest-common-subsequence/
    :param lcs_memo_table: Table generated by lcs_memo
    :param html_document: Data structure containing HTML doc sentences and items (words)
    :param transcript: Data structure containing transcript sentences and items
    :param html_num_words: # of words in the HTML
    :param transcript_num_words: # of words in the transcripts
    :param string_equality: A function that tells you whether 2 strings are equal (can be fuzzy)
    :return: A list of LCS objects which pair words between the transcript and HTML
    """
    i = html_num_words
    j = transcript_num_words

    ss_ind = lcs_memo_table[html_num_words - 1][transcript_num_words - 1]
    subsequence = []

    while i > 0 and j > 0:
        if string_equality(html_document.items[i - 1].content,
                           transcript.items[j - 1].content):
            new_lcs = AlignedItem()
            new_lcs.html_item = html_document.items[i - 1]
            new_lcs.trans_item = transcript.items[j - 1]
            new_lcs.html_item.best_transcript_match = new_lcs.trans_item
            subsequence.insert(0,new_lcs)
            i -= 1
            j -= 1
            ss_ind -= 1
        elif lcs_memo_table[i - 1][j] > lcs_memo_table[i][j - 1]:
            i -= 1
        else:
            j -= 1

    return subsequence

def backtrack_recursive(lcs_memo_table, html_document, transcript, i, j, string_equality):
    """
    Literally from Wikipedia.  Classic.
    https://en.wikipedia.org/wiki/Longest_common_subsequence_problem
    :param lcs_memo_table: Table generated by lcs_memo
    :param html_document: Data structure containing HTML doc sentences and items (words)
    :param transcript: Data structure containing transcript sentences and items
    :param html_num_words: # of words in the HTML
    :param transcript_num_words: # of words in the transcripts
    :param string_equality: A function that tells you whether 2 strings are equal (can be fuzzy)
    :return: A list of LCS objects which pair words between the transcript and HTML
    """
    if i == 0 or j == 0:
        return []
    if string_equality(html_document.items[i - 1].content,
                       transcript.items[j - 1].content):
        smaller = backtrack_recursive(lcs_memo_table, html_document, transcript, i - 1, j - 1,
                                      string_equality)
        new_lcs = AlignedItem()
        new_lcs.html_item = html_document.items[i - 1]
        new_lcs.trans_item = transcript.items[j - 1]
        new_lcs.html_item.best_transcript_match = new_lcs.trans_item
        smaller.append(new_lcs)
        return smaller
    if lcs_memo_table[i][j - 1] > lcs_memo_table[i - 1][
        j]:
        return backtrack_recursive(lcs_memo_table, html_document, transcript, i, j - 1,
                                   string_equality)
    return backtrack_recursive(lcs_memo_table, html_document, transcript, i - 1, j,
                               string_equality)


"""
Word comparison methods to use with longest common subsequence: string equality, Levenshtein distance, and soundex
"""

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

class AlignedItem:
    html_item: List[html.HtmlItem]
    trans_item: List[asr_json.Item]

    def __init__(self):
        self.trans_item = []
        self.html_item = []

    def __repr__(self):
        return self.content

    def __str__(self):
        return self.content
