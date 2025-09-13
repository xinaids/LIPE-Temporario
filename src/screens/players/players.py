#!/usr/bin/env python
# coding: utf-8

import cv2
from src.video_config.video_config import VideoConfig
from pathlib import Path
from src.constants.constants import DIRECTORY_IMAGE_PLAYER, DIRECTORY_AUDIO_PLAYER
from src.constants.timers import TIME_SHOW_PLAYER
from threading import Thread, Event, Lock
import schedule
from src.face_recognition.face_detect import (
    face_detection_model,
)
from random import *
from src.draw.draw import write_message, draw_text_top_right, draw_message_position
from src.speaker import speaker
from src.utils.utils import string_from_numbers, number_in_words_2_numeric
import time
import os
import uuid
from pathlib import Path
from src.speaker.text_reader import SpeakText
from src.speaker.speaker import SpeakerMic
from database.students.students import select_max_id, add_student
from src.utils.dir import delete_files_in_directory
from src.datatypes.player import Player
from src.utils.like_detector import detect_hand_like
from src.globals import variables

screen_name = "Identificador de Movimentos"


class PlayerScreen:
    def __init__(self) -> None:
        self.btn_position = (0, 0)
        self.btn_size = (120, 50)
        
        self.player: Player
        self.lock = Lock()
        self.my_event = Event()
        self.GetLastUserId()

        self.get_serial_number()
        self.reset_variables()

    def reset_variables(self):
        self.msg_in_screen = ""
        self.awaiting_new_player = True

        self.qtd_img_playes = 0
        self.is_saving_images = False
        self.all_images_recorded = False

        self.is_requesting_name = False
        self.is_requesting_age = False

        self.request_name_complete = False
        self.request_age_complete = False

        self.is_saving_images_profile = False
        self.next_player = False

        self.is_enabled_save_user = False
        
        self.button_clicked = False

    def add_number_id(self):
        self.serial_id += 1
        with open("serial_id.txt", "w") as f:
            f.write(str(self.serial_id))

    def get_serial_number(self):
        try:
            with open("serial_id.txt", "r") as f:
                self.serial_id = int(f.read())
        except FileNotFoundError:
            self.serial_id = 1

    def request_name(self):
        with self.lock:
            self.is_requesting_name = True

        speaker_mic = SpeakerMic()

        dir_audio_name = self.directory_save_audio + os.sep + "nome.wav"
        dir_txt_age = self.directory_save_audio + os.sep + "nome.txt"

        name_returned = speaker_mic.SpeakRecongnize("Qual seu nome?", dir_audio_name)
        
        #para não pegar caracteres especiais
        self.name = str(name_returned.encode("utf-8").decode("utf-8"))
        
        with open(dir_txt_age, "w") as f:
            f.write(self.name)

        speaker.SpeakText("Seja bem-vindo!")

        with self.lock:
            self.request_name_complete = True
            self.is_requesting_name = False

    def request_age(self):
        with self.lock:
            self.is_requesting_age = True

        speaker_mic = SpeakerMic()

        order = "Qual sua idade?"

        dir_audio_age = self.directory_save_audio + os.sep + "idade.wav"
        dir_txt_age = self.directory_save_audio + os.sep + "idade.txt"

        age_returned = speaker_mic.SpeakRecongnize(order, dir_audio_age)
        
        #para não pegar caracteres especiais
        text_age = str(age_returned.encode("utf-8").decode("utf-8")) 
        with open(dir_txt_age, "w") as f:
            f.write(text_age)

        age_list = string_from_numbers(text_age)
        converted_age = number_in_words_2_numeric(text_age)

        self.age = 0
        if age_list:
            self.age = age_list[0]
        elif converted_age:
            self.age = converted_age

        if self.age > 0:
            speaker.SpeakText(self.age)

        with self.lock:
            self.is_requesting_age = False
            self.request_age_complete = True

    def GetLastUserId(self):
        last_id = select_max_id()
        self.player_id = last_id + 1

    def SavePlayer(self):
        variables.Is_Traninig_Realized = False
        add_student(self.player)

    def create_directory(self):
        self.directory_save = DIRECTORY_IMAGE_PLAYER + os.sep + str(self.player_id)
        Path(self.directory_save).mkdir(exist_ok=True)
        delete_files_in_directory(self.directory_save)

        self.directory_save_audio = (
            DIRECTORY_AUDIO_PLAYER + os.sep + str(self.player_id)
        )
        Path(self.directory_save_audio).mkdir(exist_ok=True)
        delete_files_in_directory(self.directory_save_audio)

    def SaveProfilePicture(self) -> True:
        faces = face_detection_model(self.real_image)

        for x, y, w, h in faces:
            pY = int(y // 1.8)
            pX = int(x // 1.5)

            height = int(h * 1.8)
            width = int(w * 1.5)

            cv2.imwrite(
                self.directory_save + os.sep + "profile.jpg",
                self.real_image[pY : y + height, pX : x + width],
            )

            schedule.cancel_job(self.schIsaveImgProfile)
            break

    def SavePlayerImages(self):
        faces = face_detection_model(self.real_image)

        for x, y, w, h in faces:
            cv2.imwrite(
                self.directory_save + os.sep + str(uuid.uuid1()) + ".jpg",
                self.real_image,
            )

            self.qtd_img_playes += 1

        if self.qtd_img_playes >= 20:
            with self.lock:
                self.all_images_recorded = True
                self.is_saving_images = False

            schedule.cancel_job(self.schSaveImg)
            
    def mouse_callback(self, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            if self.btn_position[0] <= x <= self.btn_size[0] and self.btn_position[1] <= y <= self.btn_size[1]:
                self.button_clicked = True

    def Show(self, width: int, height: int):
        video_conf = VideoConfig(screen_name, width=width, height=height)
        video_conf.start()

        thread_req_name = None
        thread_req_age = None
        
        self.reset_variables()
        
        cv2.setMouseCallback(screen_name, self.mouse_callback)

        while True:
            if video_conf.stopped is True:
                break

            self.img = video_conf.read()
            self.real_image = video_conf.read()

            schedule.run_pending()
            
            with self.lock:
                if len(self.msg_in_screen) > 0:
                    self.img = write_message(self.img, self.msg_in_screen)

                if self.awaiting_new_player:
                    self.img = draw_message_position(self.img, "CONCLUIR", self.btn_position, self.btn_size)

                    self.msg_in_screen = "DÊ UM LIKE QUANDO ESTIVER PRONTO"
                    if detect_hand_like(self.real_image):
                        self.new_request_name = True
                        self.awaiting_new_player = False
                    
                elif self.new_request_name:
                    self.msg_in_screen = "SOLICITANDO NOME"

                    self.create_directory()

                    self.schIsaveImgProfile = schedule.every(1).seconds.do(
                        self.SaveProfilePicture
                    )
                    self.schSaveImg = schedule.every(1).seconds.do(
                        self.SavePlayerImages
                    )

                    thread_req_name = Thread(target=self.request_name)
                    thread_req_name.start()
                    self.new_request_name = False

                elif self.is_requesting_name:
                    self.msg_in_screen = "IDENTIFICANDO NOME..."

                elif self.request_name_complete:
                    self.request_name_complete = False
                    self.new_request_age = True

                elif self.new_request_age:
                    self.msg_in_screen = "SOLICITANDO IDADE"

                    thread_req_age = Thread(target=self.request_age)
                    thread_req_age.start()
                    self.new_request_age = False

                elif self.is_requesting_age:
                    self.msg_in_screen = "IDENTIFICANDO IDADE..."

                elif self.request_age_complete:
                    self.request_age_complete = False

                    if not self.all_images_recorded:
                        self.is_saving_images = True

                    self.is_enabled_save_user = True

                elif self.is_saving_images:
                    self.msg_in_screen = "SALVANDO IMAGENS..."

                elif self.all_images_recorded and self.is_enabled_save_user:
                    self.player = Player(self.player_id, self.name, self.age, "", [], True)
                    self.SavePlayer()
                    self.player = None

                    self.next_player = True
                    self.timer_is_showing_next_player = time.perf_counter()
                    self.all_images_recorded = False

                elif self.next_player:
                    # if not self.msg_in_screen == "PRÓXIMO JOGADOR":
                    #     self.msg_in_screen = "PRÓXIMO JOGADOR"
                    #     speaker.SpeakText(self.msg_in_screen)
                    delta = time.perf_counter() - self.timer_is_showing_next_player

                    if delta > TIME_SHOW_PLAYER:
                        self.add_number_id()
                        self.GetLastUserId()
                        self.reset_variables()

            cv2.imshow(screen_name, self.img)  # exibe a imagem com os pontos na tela

            tecla = cv2.waitKey(33)  # espera em milisegundos da execução das imagens
            if tecla == 27 or self.button_clicked:
                self.my_event.set()
                break

        if thread_req_name:
            thread_req_name.join()
        if thread_req_age:
            thread_req_age.join()
        video_conf.stop()
        cv2.destroyAllWindows()
