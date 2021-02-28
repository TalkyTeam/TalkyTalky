import os
import re

from talkytalky.util.util import contains_interesting_text, normalize_space
from bs4 import BeautifulSoup
from nltk.tokenize import sent_tokenize, word_tokenize

GUTENBERG_HEADER_PATTERN = re.compile(r'\*\*\* START OF THIS PROJECT[ A-Z]+\*\*\*')
GUTENBERG_FOOTER_PATTERN = re.compile(r'\*\*\* END OF THIS PROJECT[ A-Z]+\*\*\*')


def extract_paragraphs(infilepath):
    """
    Extract text existing within paragraph elements
    :param infilepath:
    :return:
    """
    if os.path.exists(infilepath):
        with open(infilepath, 'r') as input_file:
            xhtml = input_file.read()
    if xhtml:
        soup = BeautifulSoup(xhtml, 'html.parser')
        paragraphs = []
        for para in soup.find_all(["p","h1","h2","h3"]):
            if para and para.strings and contains_interesting_text(' '.join(para.strings)):
                paragraphs.append(' '.join(para.strings))
        return paragraphs


def contains_pattern(search_pattern, paragraphs):
    """
    True if any in a list of strings contains the pattern
    :param search_pattern:
    :param paragraphs:
    :return:
    """
    for paragraph in paragraphs:
        head = search_pattern.search(paragraph)
        if head is not None:
            return True
    return False


def remove_gutenberg_from_paragraph_list(paragraphs):
    """
    Remove the boilerplate Gutenberg text (because it won't match the Librivox recording.)
    :param in_text: Array of paragraph Text, not HTML containing Gutenberg header/footer
    :return: text without the Gutenberg header/footer
    """
    if contains_pattern(GUTENBERG_HEADER_PATTERN, paragraphs):
        while GUTENBERG_HEADER_PATTERN.search(paragraphs[0]) is None:
            paragraphs.pop(0)
            head = GUTENBERG_HEADER_PATTERN.search(paragraphs[0])
            headless = paragraphs[0][head.end():]
            if contains_interesting_text(headless):
                paragraphs[0] = headless
            else:
                paragraphs.pop(0)
    para_count = 0
    if contains_pattern(GUTENBERG_FOOTER_PATTERN, paragraphs):
        while GUTENBERG_FOOTER_PATTERN.search(paragraphs[para_count]) is None:
            para_count = para_count + 1

        foot = GUTENBERG_FOOTER_PATTERN.search(paragraphs[para_count])
        footless = paragraphs[para_count][:foot.start]
        if contains_interesting_text(footless):
            paragraphs[para_count] = footless
        else:
            paragraphs.pop(para_count)
            para_count = para_count - 1
        paragraphs = paragraphs[:para_count+1]

    return paragraphs


def paragraphs_to_sentences(paragraphs):
    """
    Turn each a list of paragraphs into a list of sentences
    :param paragraphs:
    :return:
    """
    sentence_list = []
    for paragraph in paragraphs:
        sentences = sent_tokenize(paragraph, language='english')
        for sentence in sentences:
            sentence_list.append(sentence)
    return sentence_list


def sentences_to_dumb_phrases(sentences):
    """
    Using a dumb split on semicolons and commas, turn sentences into phrases
    :param sentences:
    :return:
    """
    phrase_list = []
    for sentence in sentences:
        # TODO: This could be a single regex with re.split
        sentence = sentence.replace(', and','; and')
        sentence = sentence.replace(', or','; or')
        sentence = sentence.replace(', but','; or')
        phrases = sentence.split(';')
        for phrase in phrases:
            if contains_interesting_text(phrase):
                phrase_list.append(phrase)
    return phrase_list

def get_sentence_regex(sentence):
    """
    Generate a regex we'll use to search in the HTML for a sentence
    :param sentence:
    :return:
    """
    # If sentence is short, look for exact match
    if len(sentence) <= 60:
        return re.escape(sentence)
    # If sentence is longer, match at beginning and end
    else:
        re_sentence = re.escape(sentence)
        return re_sentence[:30] + '.+?' + re_sentence[-30:]

def assign_sentence_ids(infilepath, outfilepath):
    """
    Attempt sentence tokenization and assign IDs to sentence spans
    :param infilepath:
    :param outfilepath:
    :return: A list of HtmlSentence objects, linking the new IDs to sentence data
    """
    html_document = HtmlDocument()
    counter = 1
    paragraphs = extract_paragraphs(infilepath)
    if os.path.exists(infilepath):
        with open(infilepath, 'r') as input_file:
            xhtml = input_file.read()
    if xhtml and paragraphs:
        paragraphs = remove_gutenberg_from_paragraph_list(paragraphs)
        print(paragraphs)
        file_pos = 0
        match = GUTENBERG_HEADER_PATTERN.search(xhtml)
        if match is not None:
            file_pos = match.end()
        sentences = paragraphs_to_sentences(paragraphs)
        for sentence in sentences:
            print(str(counter) + ': ' + sentence)
            new_id = 'smil_sent' + str(counter)
            sent_object = HtmlSentence()
            sent_object.element_id = new_id
            sent_object.text = sentence
            words = word_tokenize(sentence, language='english')
            if words and len(words) > 0:
                for word in words:
                    word_object = HtmlItem()
                    word_object.content = word
                    word_object.sentence = sent_object
                    html_document.items.append(word_object)
                    sent_object.items.append(word_object)

                sent_object.word_count = len(words)
                sent_object.character_count = len(normalize_space(sentence))
                html_document.sentences.append(sent_object)
                pattern = re.compile(get_sentence_regex(sentence))
                match = pattern.search(xhtml, file_pos)
                if match is not None:
                    # print("Match start and end: " + str(match.start())+ "," + str(match.end()))
                    new_span = '<span id="' + str(new_id) + '">' + match.group(0) + '</span>'
                    xhtml = xhtml[:match.start()] + new_span + xhtml[match.end():]
                    file_pos = match.start() + len(new_span)
                counter = counter + 1

        with open(outfilepath, 'w') as output_file:
            output_file.write(xhtml)
        return html_document


class HtmlDocument:
    def __init__(self):
        self.text = ""
        self.items = []
        self.sentences = []

    def __repr__(self):
        return "Html Document %d items, %d sentences: %s" % (len(self.items), len(self.sentences), self.text)

    def __str__(self):
        return self.text


class HtmlSentence:

    def __init__(self):
        self.text = ""
        self.word_count = 0
        self.character_count = 0
        self.element_id = ""
        self.start_time = 0.0
        self.end_time = 0.0
        self.items = []
        self.previous = None
        self.next = None

    def __repr__(self):
        return "HTML Sentence (%s): %s" % (self.element_id, self.text)

    def __str__(self):
        return self.text

    def audio_start(self):
        for item in self.items:
            if item.best_transcript_match and item.best_transcript_match.start_time > 0.0:
                return item.best_transcript_match.start_time
        return 0.0

    def audio_end(self):
        for item in reversed(self.items):
            if item.best_transcript_match and item.best_transcript_match.end_time > 0.0:
                return item.best_transcript_match.end_time
        return 0.0

class HtmlItem:
    def __init__(self):
        self.content = ""
        self.sentence = None
        self.best_transcript_match = None

    def __repr__(self):
        return self.content

    def __str__(self):
        return self.content
