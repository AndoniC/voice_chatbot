import shutil
from typing import List
import zipfile
import sys
from fastapi import FastAPI, UploadFile, File, HTTPException, status
import time
import os
from whispering import whisper_text
from sendquery import *
from speakingOutLoud import speakOutLoud

#to accept body parameters in the POST request
# https://stackoverflow.com/questions/59929028/python-fastapi-error-422-with-post-request-when-sending-json-data
from pydantic import BaseModel

#import rollbar

def check_extension(filename):
    if filename.endswith('zip'):
        return True
    return False

def decompress(file_path):
    zip = zipfile.ZipFile(file_path, "r")
    try:
        zip.extractall(path = "/hostcode/fastAPI/files/")
        return True
    except:
        return False

app = FastAPI(
    title="Elleanor Assistant",
)

@app.get("/")
def read_root():
    time.sleep(1)
    return {"Hello": "World"}


class Data(BaseModel):
    val: str
# with Body parameters
@app.post("/test", tags = ["testing POST in server"])
def test(name:Data,surname: Data):
    time.sleep(1)
    return {"Hello": name.val + "  "+ surname.val}

#with path parameters   
@app.post("/test1", tags = ["testing POST in server"])
def test1(name:str,surname: str):
    time.sleep(1)
    return {"Hello": name + "  "+ surname}
	
@app.post("/email_analyzer", tags = ["Email"])
async def root(files: List[UploadFile] = File(...)):
    for file_num in files:
        file_path = "/hostmedia/fastAPI/" + file_num.filename
        with open(f'{file_num.filename}', "wb") as buffer:
            shutil.copyfileobj(file_num.file, buffer)
            if check_extension(file_path):
                if not decompress(file_path):
                    raise HTTPException(status_code=status.HTTP_405_FORBIDDEN, detail='No se ha podido descomprimir ' + str(file_num.filename) + '.')
            else:
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='El archivo introducido ' + str(file_num.filename) + ' no es un zip.')
    
@app.post("/reply/", tags = ["Reply to sentence"])
async def reply_sentence(file: str):
        file_path = "/hostmedia/assistant/" + file
        file_base_name , fext=  os.path.splitext(os.path.basename(file))
        print(file_path)
        res = {"answer": ''}
        if os.path.isfile(file_path):
            ext = os.path.splitext(file_path)[-1].lower()
            if ext=='.wav' or ext=='.mp3':
                text= whisper_text(file)
                try:
                    answer = querychatSonic(text)
                    #answer = text
                    output_file = "/hostmedia/assistant/" + file_base_name + "_response"+fext
                    output_file_names = speakOutLoud(answer,output_file)

                    res = {"answer": answer,"wav_files":output_file_names}
                except Exception as e:
                    # monitor exception using Rollbar
                    
                    raise HTTPException(status_code=status.HTTP_405_FORBIDDEN, detail='Error asking ChatGPT ' + e + '.')
                
                return res
            else:
                raise HTTPException(status_code=status.HTTP_405_FORBIDDEN, detail='Extensión de archivo de audio incorrecta ' + ext + '.')

        else:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='El archivo introducido ' + file + ' no existe.')
    
                


