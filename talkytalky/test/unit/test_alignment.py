from texttable import Texttable

from talkytalky.alignment.word_comparison import words_equal, acceptable_levenshtein, soundex
from talkytalky.alignment.alignment import CHAR_LENGTH, WORD_LENGTH, align_trans_to_html_files
from talkytalky.alignment.lcs import lcs_memo, backtrack
from talkytalky import asr_json
from talkytalky.util import html
from talkytalky.util.util import get_project_root, make_dir, get_test_root


def test_align_trans_to_html_sentences_wild_excerpt():
    align_and_show_table("the_call_of_the_wild_excerpt.json",
                         "call_of_the_wild_excerpt/EPUB/The_Call_of_the_Wild-2.xhtml",
                         "call_of_the_wild_excerpt_with_sentence_ids.html")


def test_align_trans_to_html_sentences_wild_ch1():
    align_and_show_table("call_of_the_wild_chapter_1.json",
                         "call_of_the_wild/OEBPS/@public@vhost@g@gutenberg@html@files@215@215-h@215-h-1.htm.html",
                         "call_of_the_wild_ch1_with_sentence_ids.html")


def test_align_trans_to_html_sentences_wild_dumb_phrases():
    align_and_show_table("call_of_the_wild_chapter_1.json",
                         "call_of_the_wild/OEBPS/@public@vhost@g@gutenberg@html@files@215@215-h@215-h-1.htm.html",
                         "call_of_the_wild_ch1_with_sentence_ids.html", dumb_phrases=True)


def test_align_trans_to_html_sentences_wild_char_length():
    align_and_show_table("call_of_the_wild_chapter_1.json",
                         "call_of_the_wild/OEBPS/@public@vhost@g@gutenberg@html@files@215@215-h@215-h-1.htm.html",
                         "call_of_the_wild_ch1_with_sentence_ids.html", match_criteria=CHAR_LENGTH)


def test_align_trans_to_html_sentences_wild_phrases_and_char():
    align_and_show_table("call_of_the_wild_chapter_1.json",
                         "call_of_the_wild/OEBPS/@public@vhost@g@gutenberg@html@files@215@215-h@215-h-1.htm.html",
                         "call_of_the_wild_ch1_with_sentence_ids.html", dumb_phrases=True, match_criteria=CHAR_LENGTH)


def test_align_trans_to_html_sentences_rabbit():
    align_and_show_table("peter_rabbit.json",
                         "peter_rabbit/OEBPS/@public@vhost@g@gutenberg@html@files@14838@14838-h@14838-h-0.htm.html",
                         "peter_rabbit_with_sentence_ids.html")

def test_align_trans_to_html_sentences_rabbit_excerpt():
    align_and_show_table("peter_rabbit_excerpt.json",
                         "peter_rabbit_excerpt/OEBPS/@public@vhost@g@gutenberg@html@files@14838@14838-h@14838-h-0.htm.html",
                         "peter_rabbit_excerpt_with_sentence_ids.html")


def test_align_trans_to_html_sentences_jack():
    align_and_show_table("the_house_that_jack_built.json",
                         "the_house_that_jack_built_no_images/OEBPS/@public@vhost@g@gutenberg@html@files@12109@12109-h@12109-h-0.htm.html",
                         "house_that_jack_built_with_sentence_ids.html")




def align_and_show_table(trans_file, html_file, out_file, dumb_phrases=False, match_criteria=WORD_LENGTH):
    test_root = get_test_root()
    out_dir =  test_root + "/temp/util/alignment/"
    make_dir(out_dir)

    trans_file = test_root + "/transcriptions/" + trans_file
    html_file = test_root + "/exploded_epubs/" + html_file
    out_file = out_dir + out_file

    '''
    transcript = asr_json.loadf(trans_file)
    html_sentences = html.assign_sentence_ids(html_file, out_file)
    for i in range(0, max(len(transcript.sentences), len(html_sentences))):
        print('| ', end='')
        if i < len(html_sentences):
            print(html_sentences[i].text, end='')

        print(' | ', end='')
        if i < len(transcript.sentences):
            print(transcript.sentences[i].text, end='')
        print(' |')
    '''
    sentence_pairs = align_trans_to_html_files(trans_file, html_file, out_file,
                                               match_criteria=match_criteria)
    table = get_two_column_table_head()
    table.header(["HTML", "Transcription"])

    for sentence_pair in sentence_pairs:
        table.add_row([sentence_pair[0].text, sentence_pair[1].text])

    print(table.draw())

def get_two_column_table_head():
    table = Texttable()
    table.set_cols_align(["l", "l"])
    table.set_cols_valign(["t", "t"])
    table.set_deco(Texttable.HEADER | Texttable.VLINES | Texttable.BORDER)
    table.set_max_width(0)
    return table


def show_lcs_result(lcs_list) :
    table = get_two_column_table_head()

    table.header(["HTML", "Transcription"])

    for lcs_item in lcs_list:
        table.add_row([lcs_item.html_item.content, lcs_item.trans_item.content])

    print(table.draw())


def show_lcs_table(memo_table):
    table = Texttable()
    table.set_cols_align(["c","c"])
    table.set_cols_valign(["t","t"])
    table.set_deco(Texttable.VLINES | Texttable.BORDER)
    table.set_max_width(0)
    for memo_line in memo_table:
        table.add_row(memo_line)
    print(table.draw())


def test_align_word_equals():
    align_lcs_sentences_rabbit(words_equal)


def test_align_leven():
    align_lcs_sentences_rabbit(acceptable_levenshtein)


def test_align_soundex():
    align_lcs_sentences_rabbit(soundex)


def align_lcs_sentences_rabbit(similarity_measure):

    trans_file = "peter_rabbit_excerpt.json"
    html_file = "peter_rabbit_excerpt/OEBPS/@public@vhost@g@gutenberg@html@files@14838@14838-h@14838-h-0.htm.html"
    out_file =  "peter_rabbit_excerpt_with_sentence_ids_lcs_out.html"

    test_root = get_test_root()
    out_dir =  test_root + "/temp/alignment/"
    make_dir(out_dir)

    trans_file = test_root + "/transcriptions/" + trans_file
    html_file = test_root + "/exploded_epubs/" + html_file
    out_file = out_dir + out_file

    transcript = asr_json.loadf(trans_file)
    html_document = html.assign_sentence_ids(html_file, out_file)

    memo_table = lcs_memo(html_document, transcript, similarity_measure)
    #show_lcs_table(memo_table)
    aligned_word_list = backtrack(memo_table, html_document, transcript, len(html_document.items),
                                            len(transcript.items), similarity_measure)

    show_lcs_result(aligned_word_list)