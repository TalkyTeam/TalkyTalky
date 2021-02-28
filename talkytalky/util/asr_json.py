import json
import nltk

from talkytalky.util.util import normalize_space

"""Utility class for loading Amazon Automatic Speech Recognition data."""


def loadf(filename):
    """Loads an AWS ASR JSON file specified by the provided filename and produces a populated Transcript object.
    :param filename Full path to file to be opened
    :returns a Transcript populated from the specified JSON file
    """
    infile = open(filename, "r")
    return load(infile)


def load(infile):
    """Loads a file-like object containing AWS ASR JSON and produces a populated Transcript object.
    :param infile File-like object
    :returns a Transcript populated from the provided file-like object
    """
    j = json.load(infile)
    t = Transcript()

    t.text = j['results']['transcripts'][0]['transcript']
    tokenized_sentences = nltk.sent_tokenize(t.text)
    sentence_index = 0
    s = Sentence()

    for item in j['results']['items']:
        i = Item()
        i.content = item['alternatives'][0]['content']
        i.confidence = float(item['alternatives'][0]['confidence'])

        if item['type'] == 'pronunciation':
            i.pronunciation = True
            i.start_time = float(item['start_time'])
            i.end_time = float(item['end_time'])

            if len(s.text) == 0:
                s.text = i.content
            else:
                s.text += (" " + i.content)
            s.word_count += 1
        else:
            i.punctuation = True
            s.text += i.content

        t.items.append(i)
        s.items.append(i)

        # compare against current sentence
        if s.text == tokenized_sentences[sentence_index]:
            # Save sentence details
            s.character_count = len(normalize_space(s.text))
            s.start_time = next(map(lambda x: x.start_time, filter(lambda x: x.pronunciation, s.items)), 0.0)
            s.end_time = next(map(lambda x: x.end_time, filter(lambda x: x.pronunciation, reversed(s.items))), 0.0)
            t.sentences.append(s)

            # initialize for next sentence
            s = Sentence()
            sentence_index += 1

    # If the current sentence has any content, append it
    if s.word_count > 0:
        t.sentences.append(s)

    return t


class Transcript:
    def __init__(self):
        self.text = ""
        self.items = []
        self.sentences = []

    def __repr__(self):
        return "Transcript %d items, %d sentences: %s" % (len(self.items), len(self.sentences), self.text)

    def __str__(self):
        return self.text


class Sentence:
    """Aggregates items into suspected sentences."""
    def __init__(self):
        self.text = ""
        self.start_time = 0.0
        self.end_time = 0.0
        self.word_count = 0
        self.character_count = 0
        self.items = []

    def __repr__(self):
        return "Sentence (%.2f - %.2f): %s" % (self.start_time, self.end_time, self.text)

    def __str__(self):
        return self.text


class Item:
    """Encapsulates ASR Item data. Does not support multiple alternatives."""
    def __init__(self):
        self.content = ""
        self.confidence = 0.0
        self.punctuation = False
        self.pronunciation = False
        self.start_time = 0.0
        self.end_time = 0.0

    def __repr__(self):
        if self.pronunciation:
            return "Pronunciation (%.2f - %.2f): %s" % (self.start_time, self.end_time, self.content)
        else:
            return "Punctuation: %s" % self.content

    def __str__(self):
        return self.content
