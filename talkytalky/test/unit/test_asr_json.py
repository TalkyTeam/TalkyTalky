from talkytalky import asr_json
from talkytalky.util.util import get_project_root


def test_parse():
    project_root = get_project_root()
    print(project_root)
    infile = open(project_root + "/talkytalky/test/transcriptions/peter_rabbit.json")
    transcript = asr_json.load(infile)

    assert len(transcript.items) == 1099
    assert len(transcript.sentences) == 66

    word = transcript.items[0]
    assert word.content == "The"
    assert word.pronunciation is True
    assert word.punctuation is False
    assert word.start_time == 0.44
    assert word.end_time == 0.65

    period = transcript.items[8]
    assert period.content == "."
    assert period.pronunciation is False
    assert period.punctuation is True
    assert period.start_time == 0
    assert period.end_time == 0

    s = transcript.sentences[0]
    assert s.text == "The Tale of Peter Rabbit by Beatrix Potter."
    assert s.start_time == 0.44
    assert s.end_time == 3.56
    assert s.word_count == 8

    # Check that start time of first sentence and end time of last sentence line up with corresponding items
    assert transcript.sentences[0].start_time == transcript.items[0].start_time
    assert transcript.sentences[-1].end_time == \
           next(map(lambda x: x.end_time, filter(lambda x: x.pronunciation, reversed(transcript.items))))
