import pyttsx3
import os
from pygame import mixer
import time

def SpeakText(data:str):
    engine = pyttsx3.init()  # Inicializa o mecanismo de síntese de fala

    # Configurações opcionais para melhorar a voz
    engine.setProperty('rate', 150)     # Ajusta a velocidade da fala
    engine.setProperty('volume', 0.9)   # Ajusta o volume (0.0 a 1.0)

    # Fala o texto
    engine.say(data)
    engine.runAndWait()

# def SpeakText(data:str):
#     try:
#         voice = 'pt-BR-AntonioNeural'
#         output_file = "data.mp3"
#         command = f'edge-tts --voice "{voice}" --text "{data}" --write-media "{output_file}"'
#         os.system(command)
        
#         mixer.init()
#         mixer.music.load(output_file)
#         mixer.music.play()
#         while mixer.music.get_busy():  # wait for music to finish playing
#             time.sleep(1)
#         mixer.music.stop()
#         mixer.quit()
#     except:
#         print("Ocorreu um erro durante a leitura")
