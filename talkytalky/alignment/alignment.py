

from nltk.translate.gale_church import align_blocks

from talkytalky.alignment.lcs import lcs
from talkytalky import asr_json
from talkytalky.util import html

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

