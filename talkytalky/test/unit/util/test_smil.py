from talkytalky.util import smil

from talkytalky.util.alignment import align_trans_to_html_files, align_using_lcs_words, soundex
from talkytalky.util.util import make_dir, get_project_root


def test_generate_smil():
    project_root = get_project_root()

    out_dir = project_root + "/test/temp/util/smil/"
    make_dir(out_dir)
    out_file = out_dir + "call_of_the_wild_ch1_with_sentence_ids.html"

    html_file_name = "@public@vhost@g@gutenberg@html@files@215@215-h@215-h-1.htm.html"
    html_file = project_root + "/test/exploded_epubs/call_of_the_wild/OEBPS/" + html_file_name
    transcriptions_file = project_root + "/test/transcriptions/call_of_the_wild_chapter_1.json"

    sentence_pairs = align_trans_to_html_files(transcriptions_file, html_file, out_file)

    smil_file = open(out_dir + "smil.xml", 'wb')
    smil.generate_smil(sentence_pairs, html_file_name, 'call_of_the_wild_ch1.mp3', smil_file)
    smil_file.close()


def test_generate_lcs_smil():
    trans_file = "peter_rabbit_excerpt.json"
    html_file = "peter_rabbit_excerpt/OEBPS/@public@vhost@g@gutenberg@html@files@14838@14838-h@14838-h-0.htm.html"
    html_smil_filename = "@public@vhost@g@gutenberg@html@files@14838@14838-h@14838-h-0.htm.html"
    out_file = "peter_rabbit_excerpt_with_sentence_ids_lcs_out.html"
    similarity_measure=soundex
    mp3_filename = 'peter_rabbit_excerpt_lcs.mp3'
    smil_filename = 'peter_rabbit_excerpt_smil.xml'
    generate_lcs_smil(trans_file, html_file, html_smil_filename, out_file, mp3_filename, smil_filename, similarity_measure)


def test_lcs_smil_wild_ch1():
    generate_lcs_smil("call_of_the_wild_chapter_1.json",
                      "call_of_the_wild/OEBPS/@public@vhost@g@gutenberg@html@files@215@215-h@215-h-1.htm.html",
                      "@public@vhost@g@gutenberg@html@files@215@215-h@215-h-1.htm.html",
                      "call_of_the_wild_ch1_with_sentence_ids.html",
                      "call_of_the_wild.mp3",
                      "call_of_the_wild_smil.xml",
                      soundex)


def test_lcs_smil_wild_all_ch():
    for i in range(1,8):
        generate_lcs_smil("call_of_the_wild_ch_0" + str(i) + "_general.json",
                      "call_of_the_wild/OEBPS/@public@vhost@g@gutenberg@html@files@215@215-h@215-h-" + str(i) + ".htm.html",
                      "@public@vhost@g@gutenberg@html@files@215@215-h@215-h-" + str(i) + ".htm.html",
                      "call_of_the_wild_ch" + str(i) + "_with_sentence_ids.html",
                      "callofwild3_0" + str(i) + "_london.mp3",
                      "call_of_the_wild_ch0" + str(i) + ".smil",
                      soundex)


def test_lcs_smil_peter_rabbit():
    generate_lcs_smil("peter_rabbit.json",
                      "peter_rabbit/OEBPS/@public@vhost@g@gutenberg@html@files@14838@14838-h@14838-h-0.htm.html",
                      "@public@vhost@g@gutenberg@html@files@14838@14838-h@14838-h-0.htm.html",
                      "peter_rabbit_with_sentence_ids.html",
                      "storytime_11_peterrabbit_potter.mp3",
                      "peter_rabbit.smil",
                      soundex)


def generate_lcs_smil(trans_file, html_file, html_smil_filename, out_file, mp3_filename, smil_filename, similarity_measure):

    print([trans_file, html_file, html_smil_filename, out_file, mp3_filename, smil_filename, similarity_measure])
    project_root = get_project_root()
    out_dir = project_root + "/test/temp/util/smil/"
    make_dir(out_dir)
    smil_filename = out_dir + smil_filename

    trans_file = project_root + "/test/transcriptions/" + trans_file
    html_file = project_root + "/test/exploded_epubs/" + html_file
    out_file = out_dir + out_file

    html_document, aligned_word_list = align_using_lcs_words(trans_file, html_file, out_file, similarity_measure)
    smil_file = open(smil_filename, 'wb')
    smil.generate_lcs_based_smil(html_document, html_smil_filename, mp3_filename, smil_file)
    smil_file.close()
