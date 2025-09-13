#!/usr/bin/env python
# coding: utf-8

import speech_recognition as sr
from speech_recognition import AudioData
import json
from src.speaker.text_reader import SpeakText
import whisper
import os

class SpeakerMic:
    def __init__(self) -> None:
        self.rec = sr.Recognizer()

    def SpeakRecongnize(self, order: str, file_name:int) -> str:
        try:
            if order:
                SpeakText(order)
            with sr.Microphone() as mic:
                self.rec.adjust_for_ambient_noise(mic, 0.2)
                audio = self.rec.listen(mic, phrase_time_limit=8)
                return self.RecongnizeWhisperSave(audio=audio, file_name=file_name)

        except sr.RequestError:
            return "Não Identificado"

        except sr.UnknownValueError:
            return "Valor não reconhecido"

    def RecognizeWhisper(self, audio: AudioData) -> str:
        try:
            recognized_text = self.rec.recognize_whisper(
                audio, language="pt", model="tiny"
            )
            recognized_text = recognized_text.lower()
            return recognized_text

        except sr.RequestError:
            return "Não Identificado"

        except sr.UnknownValueError:
            return "Valor não reconhecido"

    # para reconhecimentos numéricos do vosk, é necessário gravar o aúdio
    def RecongnizeVosk(self, audio: AudioData) -> str:
        try:
            recognized_text = json.loads(self.rec.recognize_vosk(audio))
            recognized_text = recognized_text["text"].lower()
            return recognized_text

        except sr.RequestError:
            return "Não Identificado"

        except sr.UnknownValueError:
            return "Valor não reconhecido"

    def RecongnizeWhisperSave(self, audio: AudioData, file_name:str) -> str:
        try:
            with open(file_name, "wb") as file:
                file.write(audio.get_wav_data())

            audio_loaded = whisper.load_audio(file_name)
            audio_loaded = whisper.pad_or_trim(audio_loaded)

            model = whisper.load_model("tiny")
            result = model.transcribe(
                audio_loaded,
                fp16=False,
                language="pt",
                verbose=True,
                patience=2,
                beam_size=5,
            )

            return result["text"]

        except:
            return "Texto não reconhecido"
