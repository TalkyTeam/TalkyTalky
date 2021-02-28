from nltk import pos_tag

from talkytalky.util.boundaries import chunk_a_dunk, PARSIVAR_CHUNK_RULES, hunpos_tag, PYRATA_CHUNK_RULES
from talkytalky.util.html import extract_paragraphs, paragraphs_to_sentences
from talkytalky.util.util import get_project_root

def test_chunk_a_dunk_pos_pyrata():
    sentences = get_wild_sentences()
    for sentence in sentences:
        print(sentence)
        chunk_a_dunk(sentence, pos_tag, PYRATA_CHUNK_RULES)


def test_chunk_a_dunk_pos_parsivar():
    sentences = get_wild_sentences()
    for sentence in sentences:
        print(sentence)
        chunk_a_dunk(sentence, pos_tag, PARSIVAR_CHUNK_RULES)


def test_chunk_a_dunk_hunpos():
    sentences = get_wild_sentences()
    for sentence in sentences:
        print(sentence)
        chunk_a_dunk(sentence, hunpos_tag, PYRATA_CHUNK_RULES)

def get_wild_sentences():
    project_root = get_project_root()
    print(project_root)
    in_file = project_root + "/test/exploded_epubs/call_of_the_wild_excerpt/EPUB/The_Call_of_the_Wild-2.xhtml"
    paragraphs = extract_paragraphs(in_file)
    return paragraphs_to_sentences(paragraphs)