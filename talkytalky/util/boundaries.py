from nltk import word_tokenize, HunposTagger
from nltk.chunk.regexp import ChunkRule, RegexpChunkParser

from talkytalky.util.util import get_project_root

"""
Rules for making phrases from tokens already labelled with parts of speech
"""
# Grammar source: https://github.com/ICTRC/Parsivar/blob/master/parsivar/chunker.py
PARSIVAR_CHUNK_RULES = [
    ChunkRule('<ADJ_SIM><V_PRS>', 'VP'),
    ChunkRule('<ADJ_INO><V.*>', 'VP'),
    ChunkRule('<V_PRS><N_SING><V_SUB>', 'VP'),
    ChunkRule('<N_SING><ADJ.*><N_SING>', 'NP'),
    ChunkRule('<N.*><PRO>', 'NP'),
    ChunkRule('<N_SING><V_.*>', 'VP'),
    ChunkRule('<V.*>+', 'VP'),
    ChunkRule('<ADJ.*>?<N.*>+ <ADJ.*>?', 'NP'),
    ChunkRule('<DET><NP>', 'DNP'),
    ChunkRule('<ADJ_CMPR><P>', 'PP'),
    ChunkRule('<ADJ_SIM><P>', 'PP'),
    ChunkRule('<P><N_SING>', 'PP'),
    ChunkRule('<P>*', 'PP'),
    ChunkRule('<NP><DNP>', 'DDNP'),
    ChunkRule('<PP><NP>+', 'NPP')
]

# Grammar source: https://github.com/nicolashernandez/PyRATA/blob/master/do_benchmark.py
# Doesn't appear to work for clauses.
PYRATA_CHUNK_RULES = [
    ChunkRule('<DT|JJ|NN.*>+', 'NP'),
    ChunkRule('<IN><NP>', 'PP'),
    ChunkRule('<VB.*><NP|PP|CLAUSE>+$', 'VP'),
    ChunkRule('<NP><VP>', 'CLAUSE')
]


def chunk_tagged_sentence(tagged_words, chunk_rules):
    """
    Given a list of words tagged with parts of speech, create the chunks using the chunk_rules grammar
    :param tagged_words: List of words in a sentence tagged with parts of speech
    :param chunk_rules: A list of rules for breaking down the sentence
    :return:
    """
    chunk_parser = RegexpChunkParser(chunk_rules, chunk_label='Phrase')
    chunk_tree = chunk_parser.parse(tagged_words)
    print(str(chunk_tree))
    print(repr(chunk_tree))
    return chunk_tree


def chunk_a_dunk(sentence, tag_method, chunk_rules):
    """
    Given a sentence, chunk and return a chunk tree
    :param sentence: Sentence to be turned into chunks
    :param tag_method: The tag method uses some algorithm to take a list of words and label them with parts of speech
    :param chunk_rules: A list of rules for breaking down the sentence
    :return:
    """
    words = word_tokenize(sentence)
    tagged_words = tag_method(words)
    #print("sentence: " + sentence)
    #print("words: " + str(words))
    print("tagged words: " + str(tagged_words))
    return chunk_tagged_sentence(tagged_words, chunk_rules)


def hunpos_tag(words):
    """
    The "hunpos" algorithm for tagging words with parts of speech
    https://stackoverflow.com/questions/17408543/how-to-correctly-set-hunpos-tagger-in-nltk-for-pos-tagging-in-english/17425786
    :param words:
    :return:
    """
    root = get_project_root()
    model_path = root + '/models/tagging/hunpos/'
    ht = HunposTagger(model_path + 'english.model', model_path + 'hunpos-tag', encoding='utf-8')
    tagged_words =  ht.tag(words)
    fixed_tagged_words = list(map(lambda t: (t[0], t[1].decode('utf-8')), tagged_words))
    return fixed_tagged_words


