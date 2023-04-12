#From https://github.com/coqui-ai/TTS
from TTS.api import TTS
import os

# List available 🐸TTS models and choose the first one
model_name = TTS.list_models()[1]
print(TTS.list_models())
print ("Loading model : " + model_name)
# Init TTS
tts = TTS(model_name)
 
def speakOutLoud(textin,outputwav):


    # split the text by periods
    sentence_list = textin.split('.')
    file_name, file_extension = os.path.splitext(outputwav)
    file_base = os.path.basename(outputwav)
    file_list = []

    for i, sentence in enumerate(sentence_list):

        # Running a multi-speaker and multi-lingual model
    
        # Run TTS
        # ❗ Since this model is multi-speaker and multi-lingual, we must set the target speaker and the language
        # Text to speech with a numpy output
        #wav = tts.tts("This is a test! This is also a test!!", speaker=tts.speakers[0], language=tts.languages[0])
        # Text to speech to a file
        output_file_name = file_name+str(i)+file_extension
        if sentence_list[i]:
            tts.tts_to_file(text=sentence_list[i], speaker=tts.speakers[0], language=tts.languages[0], file_path=output_file_name)

        # Running a single speaker model

        # Init TTS with the target model name
        #tts = TTS(model_name="tts_models/de/thorsten/tacotron2-DDC", progress_bar=False, gpu=False)
        # Run TTS
        #tts.tts_to_file(text="Ich bin eine Testnachricht.", file_path=OUTPUT_PATH)

        # Example voice cloning with YourTTS in English, French and Portuguese:
        #tts = TTS(model_name="tts_models/multilingual/multi-dataset/your_tts", progress_bar=False, gpu=True)
        #tts.tts_to_file("This is voice cloning.", speaker_wav="my/cloning/audio.wav", language="en", file_path="output.wav")
        #tts.tts_to_file("C'est le clonage de la voix.", speaker_wav="my/cloning/audio.wav", language="fr", file_path="output.wav")
        #tts.tts_to_file("Isso é clonagem de voz.", speaker_wav="my/cloning/audio.wav", language="pt", file_path="output.wav")
        file_list.append(output_file_name)

    #return the list of files generated
    return file_list