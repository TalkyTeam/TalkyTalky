import json
import wave
from pydub import AudioSegment
from vosk import Model, KaldiRecognizer

from talkytalky.stt.Item import Item
from talkytalky.stt.Transcript import Transcript
from talkytalky.util.util import get_project_root, exists

"""Transcribe an mp3 with vosk and create list of items.  No sentence data."""

MODEL_DIR = get_project_root() + "/talkytalky/models/vosk/vosk-model-en-us-daanzu-20200905"


def get_mp3_transcript(mp3_filename):
    """
    Generate Transcript object from mp3
    """
    wav_filename = get_wav_from_mp3(mp3_filename)
    return get_transcript(wav_filename)


def get_wav_from_mp3(mp3_filename):
    """
    Convert mp3 to WAV
    """
    wav_filename = mp3_filename.replace(".mp3", ".wav")
    audio_segment = AudioSegment.from_mp3(mp3_filename)
    audio_segment = audio_segment.set_frame_rate(16000)
    audio_segment = audio_segment.set_channels(1)
    audio_segment.export(wav_filename, format='wav')
    return wav_filename


def get_transcript(wav_filename):
    """
    From a WAV filename, use vosk to generate a Transcript object
    See example code https://github.com/alphacep/vosk-api/blob/master/python/example/test_simple.py
    """
    transcript_text = []
    transcript = Transcript()
    wav_file = wave.open(wav_filename, "rb")
    if wav_file.getnchannels() != 1 or wav_file.getsampwidth() != 2 or wav_file.getcomptype() != "NONE":
        print("Audio file must be WAV format mono PCM.")
        raise Exception("Audio file must be WAV format mono PCM.")
    model = Model(MODEL_DIR)
    rec = KaldiRecognizer(model, wav_file.getframerate())
    rec.SetWords(True)
    while True:
        data = wav_file.readframes(4000)
        if len(data) == 0:
            break
        if rec.AcceptWaveform(data):
            result = rec.Result();
            json_result = json.loads(result)
            if (exists(json_result, 'result')):
                for word in json_result['result']:
                    item = Item()
                    item.start_time = word['start']
                    item.end_time = word['end']
                    item.confidence = word['conf']
                    item.content = word['word']
                    transcript.items.append(item)
            if (exists(json_result, 'text')):
                transcript_text.append(json_result['text'])
    transcript.text = ' '.join(transcript_text)
    return transcript

