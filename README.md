# voice_chatbot
A chat-sonic based voice chatbot that I usually call Elleanor.


![imagen](https://user-images.githubusercontent.com/4378233/227831219-de66d6bc-b17f-410b-b0b2-ca4e3b50dc0a.png)

## Installation
Windows Host:

1. Install python 3.7 in the host
2. Install the following packages
  ```
  pip install requests  #synchronous for fastapi calls
  pip install grequests  #asynchronous requests
  pip install playsound==1.2.2 #to reproduce .wave files
  pip install pyaudio  # to save .wave files
  ```
3. Clone https://github.com/coqui-ai/TTS repository in a folder that will be shared between host and container
4. Clone https://github.com/openai/whisper repository in a folder that will be shared between host and container
5. Build provided dockerfile calling the build.bat script
```
C:\> build elleanor/chatbot:1.0
```
7. Run dockerfile with provided script run.sh, modifying the paths in a convenient way.
```
run_cpu [ip/adapter identifier:0.0] [media_dir]  [code_dir] [models_dir] [libs dir] [repos_dir] [build dir]
```
9. Once in the container go to the folder where main.py is
10. change key-api by one of your own in sendquery.py
11. launch this command to run fastapi server:
  ```
  uvicorn main:app --host=0.0.0.0 --port=8000 --reload
  ```
10. From host launch the assistant.py script


Linux Host:

Not tested but it should work in a similar way.

## Tasks List
- [ ] create c++ client for host
- [ ] add different tts engine models for generating wave
- [ ] take into account the input language when selecting TTS voice to generate the output audio file
- [ ] copy models in the docker image so that it is not neccesary to download them when launching fastapi server
- [ ] convert the chatbot into an assistant :-)
- [ ] test in linux


