from pydub import AudioSegment

import sys
# caution: path[0] is reserved for script path (or '' in REPL)
sys.path.insert(1, '/hostrepos/whisper')

import whisper
#import csv
import unicodecsv as csv
import os
import json
model = whisper.load_model("small")

def whisper_text(audio_file_name):
  
    result = model.transcribe('/hostmedia/assistant/'+audio_file_name)
    print(result["text"])
    return result["text"]