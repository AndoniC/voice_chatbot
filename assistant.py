import pyaudio
import wave
from speakingOut import play
import matplotlib.pyplot as plt
import requests
import numpy as np
import time
from tqdm import tqdm

api_url = "http://localhost:8000/"

# Set parameters for audio recording
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024
RECORD_SECONDS = 10
OUTPUT_PATH= "F:/MEDIA/assistant/"
WAVE_OUTPUT_FILENAME = "output.wav"

# Initialize PyAudio
audio = pyaudio.PyAudio()
print(audio.get_default_input_device_info())
# Open microphone stream
stream = audio.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

time.sleep(3)
print("Recording...")
# Start recording
frames = []
for i in tqdm(range(0, int(RATE / CHUNK * RECORD_SECONDS))):
    data = stream.read(CHUNK)
    frames.append(data)

frames_plot = b"".join(frames)

plt.figure(1)
plt.title("Signal Wave...")
amplitude = np.fromstring(frames_plot, np.int16)
plt.plot(amplitude)
plt.show()

print("Finished recording.")

# Stop recording and close stream
stream.stop_stream()
stream.close()
audio.terminate()

print("Saving "+WAVE_OUTPUT_FILENAME)
# Save audio to WAV file
wf = wave.open(OUTPUT_PATH + WAVE_OUTPUT_FILENAME, 'wb')
wf.setnchannels(CHANNELS)
wf.setsampwidth(audio.get_sample_size(FORMAT))
wf.setframerate(RATE)
wf.writeframes(b''.join(frames))
wf.close()

print("Send audio to fastapi")

#call get
#response = requests.get(api_url)
#call post
data = {"file": WAVE_OUTPUT_FILENAME}
response = requests.post(api_url+'reply', params=data)
print( response.json())
print (response.status_code)

output_wav_files = response.json()["wav_files"]
for wav_file in output_wav_files:
    new_string = wav_file.replace("/hostmedia", "F:/MEDIA" )
    play(new_string)

print("Play audio aloud")
