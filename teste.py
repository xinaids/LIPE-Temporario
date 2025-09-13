import speech_recognition as sr
from threading import Event
import vosk
import pyaudio
import json
from src.speaker.text_reader import SpeakText

def SpeakRecongnize()->str:
    rec = sr.Recognizer()
    
    while(True):
        try:               
            with sr.Microphone() as mic:
                rec.adjust_for_ambient_noise(mic, 0.2)
                audio = rec.listen(mic, phrase_time_limit=8)
                
                recognized_text = json.loads(rec.recognize_vosk(audio))
                recognized_text = recognized_text['text'].lower()
                return recognized_text

        except sr.RequestError:
            return "Não Identificado"


# def SpeakRecongnizeVosk()->str:
#     rec = sr.Recognizer()
    
#     while(True):
#         try:               
#             with sr.Microphone() as mic:
#                 rec.adjust_for_ambient_noise(mic, 0.2)
#                 audio = rec.listen(mic, phrase_time_limit=8)
#                 recognized_text = json.loads(rec.recognize_vosk(audio))
#                 recognized_text = recognized_text['text'].lower()
#                 return recognized_text

#         except sr.RequestError:
#             return "Não Identificado"


print(SpeakRecongnize())