from pprint import pprint
from talkytalky.stt.vosk import get_mp3_transcript
from talkytalky.util.util import make_dir, get_test_root


def test_transcribe():
    test_root = get_test_root()

    audio_file = test_root + "/audio/peter_rabbit/storytime_11_peterrabbit_potter.mp3"
    out_dir = test_root + "/temp/transcribe/"
    make_dir(out_dir)
    print("Start transcribe test")

    transcript = get_mp3_transcript(audio_file)
    pprint(transcript)
    print("Transcribe test complete")
