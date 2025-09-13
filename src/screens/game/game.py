#!/usr/bin/env python
# coding: utf-8

import cv2
import time
from src.video_config.video_config import VideoConfig
import src.identifier.identifier as identifier
import src.constants.movements as mov
import src.constants.colors as colors
from src.constants.timers import *
from src.constants.constants import *
from src.datatypes.confetti import Confetti
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from src.constants.game_modes import *
from src.datatypes.player import Player

from src.face_recognition.face_recognizer import FaceRecognizer
from src.draw.draw import (
    initial_message,
    draw_message,
    draw_circles,
    draw_points,
    draw_message_center_screen,
    show_image_movements,
    show_player_image,
    apply_filter,
    write_message,
    write_center_screen,
    show_correct_position,
    draw_confetti,
    show_score
)
import random
from database.students.students import select_students
from database.scores.scores import add_score
from typing import List
from typing import Union
from src.interfaces.game_mode import IGameMode

DEFAULT_ENCODINGS_PATH = Path("output/encodings.pkl")

screen_name = "Identificador de Movimentos"

class Game:
    def __init__(self):       
        self.searching_player = False
        self.player_found = False
        self.is_showing_next_round = False

        self.number_movements = INITIAL_NUMBER_MOVEMENTS
        
        self.score_timeA = 0
        self.score_timeB = 0

        self.confetti_particles: List[Confetti] = []
        self.get_serial_number()
        self.reset_variables()

    def reset_variables(self):
        self.score_player = 0
        
        self.sort_movement = True
        self.number_start_message = 0
        
        self.count_player_Show = 0
        self.show_team_id = "A"
        
        self.is_showing_start_messages = False
        self.is_showing_movements = False
        self.is_movement_wrong = False
        self.is_movement_identified = False
        self.is_draw_circles = False
        self.bounce_frame = 0
        self.movement_correct = False

        self.mov_showing_seq = 0
        self.num_circles = 0
        
        self.num_attempts_find_player = 0
        
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
            
    def find_expected_player(self):

        if not self.searching_player:
            self.fut_player_search = self.executor.submit(
                self.my_face_recognizer.recognize_faces, self.real_image
            )
            self.searching_player = True
            self.timer_search_player = time.perf_counter()

        elif self.fut_player_search.done():
            searched_player = self.fut_player_search.result()
        
            if not searched_player is None: 
                print(f"Player Consultado {searched_player}")
                self.searching_player = False
                if int(searched_player) == self.expected_player.Id or self.num_attempts_find_player > NUMBERS_MAX_ATTEMPS_IDENTIFY_PLAYER:
                    print("Iniciando o Jogo")
                    self.player_found = True
                else:
                    self.num_attempts_find_player += 1
                    
    def player_is_positioned(self):
        self.my_identifier.process_image(self.real_image)

        if self.my_identifier.is_correct_positioned():
            self.sort_movement = False
            self.is_showing_start_messages = True
            self.timer_message_start = time.perf_counter()
        else:
            self.img = show_correct_position(self.img)
            
    def show_start_message(self):
        delta = time.perf_counter() - self.timer_message_start
        if delta > TIME_SHOW_START_MESSAGE:
            self.number_start_message += 1
            self.timer_message_start = time.perf_counter()
            
        if self.number_start_message < len(START_MESSAGES):
            message = START_MESSAGES[self.number_start_message]
            self.img = draw_message_center_screen(self.img, message)
        else:
            self.is_showing_start_messages = False
            self.is_showing_movements = True
            self.timer_is_showing_movements = time.perf_counter()
        
    def show_player_teams(self):
        
        if self.show_team_id == "A":
            color = colors.RED
            team_name = "TIME VERMELHO"
        else:
            color = colors.BLUE
            team_name = "TIME AZUL"
            
        delta = time.perf_counter() - self.timer_show_msg_teams
        if delta < TIME_SHOW_PLAYER:
            self.img = draw_message_center_screen(self.img, team_name, color)
            self.timer_show_players_teams = time.perf_counter()
            return
        
        team_filter = [player for player in  self.list_players if player.Team == self.show_team_id]
        
        delta = time.perf_counter() - self.timer_show_players_teams
        if delta < TIME_SHOW_PLAYER:
            player_id = team_filter[self.count_player_Show].Id
            self.img = show_player_image(self.img, player_id, color)
        else:
            if len(team_filter) < self.count_player_Show:
                self.count_player_Show += 1
            
            elif self.show_team_id == "A":
                self.count_player_Show = 0
                self.show_team_id = "B"
                self.timer_show_msg_teams = time.perf_counter()
                return

            self.showed_players_teams = True
            self.is_time_to_start = True
            self.timer_is_time_to_start = time.perf_counter()

    def time_to_start(self):

        delta = time.perf_counter() - self.timer_show_players_teams
        if delta < TIME_SHOW_PLAYER:
            self.img = draw_message_center_screen(self.img, "HORA DE COMEÇAR")
        
        else:
            self.is_time_to_start = False
            self.is_showing_next_player = True
            self.timer_show_player = time.perf_counter()

    def show_identified_movement(self):
        if self.movement_correct:
            message_mov = f"{self.my_identifier.seq_command + 1} - {mov.MOVEMENTS_MESSAGE[self.my_identifier.command]}"
            self.img = draw_message(self.img, message_mov)
            
        if self.num_circles == self.my_identifier.seq_command:
            self.num_circles += 1
        
        delta = time.perf_counter() - self.timer_next_mov
        
        if delta > MIN_TIME_SHOW_MOVEMENT:
            if (delta > TIME_SHOW_MOVEMENT or not self.movement_correct):
                if self.my_identifier.has_next_movement():
                    self.my_identifier.next_movement()
                    self.is_movement_identified = False
                    self.is_movement_wrong = False
                    self.timer_next_mov = time.perf_counter()
                else:
                    self.call_next_player(False)

    def call_next_player(self, remove_player: bool = True):
        
        if self.expected_player.Team == "A":
            self.score_timeA += self.score_player
        else:
            self.score_timeB += self.score_player

        if len(self.list_players) == 0:
            print("Não foram identificados jogadores.")
            self.expected_player = None
        else:
            self.reset_variables()
            self.game_mode.reset_variables_mode()
            self.my_identifier.reset_seq_command()
                
            self.set_player(self.expected_player.Id, remove_player)
        
        self.is_showing_next_player = True
        self.timer_show_player = time.perf_counter()
    
    def get_next_player(self, current_player_id:int)-> Player | None:
        next_player = None
        current_player_found = False
        
        for p in self.list_players:
            if current_player_found:
                next_player = p
                break
                
            if p.Id == current_player_id:
                current_player_found = True
                
        return next_player
    
    def set_player(self, previous_player_id:int, remove_previous_player:bool):
        next_player = self.get_next_player(previous_player_id)
        
        if remove_previous_player: 
            self.list_players = [p for p in self.list_players if p.Id != previous_player_id]
                
        if not next_player: # todos os jogadores já jogaram o round
            if self.is_last_round():
                self.is_end_game = True
                self.timer_show_score = time.perf_counter()
                return
            
            self.add_new_movement()
            next_player = self.list_players[0]
            
        if next_player.Movements is None:
            self.my_identifier.sort_movements(self.game_mode.list_movements, self.number_movements)
            next_player.Movements = self.my_identifier.list_commands
        else:
            self.my_identifier.list_commands = next_player.Movements
            
        self.expected_player = next_player
            
        
        
    def is_last_round(self)->bool:
        team_a_found = False
        team_b_found = False
        
        for u in self.list_players:
            if u.Team == "A":
                team_a_found = True
            elif u.Team == "B":
                team_b_found = True

        if not team_a_found or not team_b_found:
            return True
    
        return False
        
    def show_end_score(self):
        delta = time.perf_counter() - self.timer_show_score
        if delta < TIME_SHOW_SCORE:
            self.img[:, :] = colors.BLUE_LIGHT
            self.img = show_score(self.img, self.score_timeA * 5, self.score_timeB * 5)
        else:
            self.is_running = False
            print("Acabou")
        
    def add_new_movement(self):
        self.mov_showing_seq = 0
        self.num_circles = 0
        self.my_identifier.reset_seq_command()

        self.number_movements += 1
        
        print(self.list_players)
        for u in self.list_players:
            u.Movements.append(random.randint(1, len(self.game_mode.list_movements)))
            self.my_identifier.list_commands = u.Movements

        self.is_movement_wrong = False
        self.is_movement_identified = False
        self.sort_movement = True

        self.is_showing_movements = False
        self.is_draw_circles = False
        self.movement_correct = False
    
    def call_next_round(self):
        self.mov_showing_seq = 0
        self.num_circles = 0
        self.my_identifier.reset_seq_command()

        self.number_movements += 1
        self.my_identifier.list_commands.append(random.randint(1, len(mov.MOVEMENTS)))

        self.is_movement_wrong = False
        self.is_movement_identified = False
        self.sort_movement = True

        self.is_showing_movements = False
        self.is_draw_circles = False
        self.movement_correct = False

        self.is_showing_next_round = True
        self.sort_confetti()
        self.timer_show_player = time.perf_counter()

    def sort_confetti(self):
        self.confetti_particles.clear()
        
        for _ in range(NUMBER_CONFETTI_PARTICLES): 
            x = random.randint(0, self.img.shape[1])
            y = random.randint(-200, self.img.shape[0] // 2)
            color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
            speed = random.randint(10, 25)
            
            confetti = Confetti(PosX=x, PosY=y, Color=color, Speed=speed)

            self.confetti_particles.append(confetti)
            
    def show_next_player(self):
        if self.expected_player.Team == "A":
            color = colors.RED
        else:
            color = colors.BLUE
        
        img_player = show_player_image(self.img, self.expected_player.Id, color, "PRÓXIMO JOGADOR")

        if img_player is None:
            return

        self.img = img_player

        delta = time.perf_counter() - self.timer_show_player
        if delta > TIME_SHOW_PLAYER:
            self.is_showing_next_player = False
            self.player_found = False
            
    def show_message_new_round(self):
        self.img = write_message(self.img, "PASSOU DE FASE!")
        
        delta = time.perf_counter() - self.timer_show_player
        
        if delta > TIME_SHOW_PLAYER:
            self.is_showing_next_round = False
            self.player_found = False
        
    def Show(self, width: int, height: int, game_mode:IGameMode):
        self.game_mode = game_mode
        
        self.reset_variables()
        self.game_mode.reset_variables_mode()
        
        # abre o fluxo de leitura
        # video_conf = VideoConfig(screen_name, "./images/videomaos.mp4") #lê de um vídeo
        video_conf = VideoConfig(screen_name, width=width, height=height)
        video_conf.start()

        self.my_identifier = identifier.Identifier(self.game_mode.list_movements)
        self.my_identifier.sort_movements(self.game_mode.list_movements, self.number_movements)
        
        self.my_face_recognizer = FaceRecognizer(
            encodings_location=DEFAULT_ENCODINGS_PATH
        )

        self.list_players = select_students()
        self.timer_show_msg_teams = time.perf_counter()
        
        team = None
        for p in self.list_players:
            if team == "A":
                team = "B"
            else:
                team = "A"
            
            p.Team = team     
            p.Active = True   

        self.expected_player = self.list_players[0]
        self.expected_player.Movements = self.my_identifier.list_commands
        
        self.is_end_game = False
        self.showed_players_teams = False
        
        print("---> " + str(self.expected_player.Id))

        self.is_running = True

        with ThreadPoolExecutor(max_workers=4) as self.executor:

            while self.is_running:
                if video_conf.stopped is True:
                    break
                else:
                    self.img = video_conf.read()
                    self.real_image = video_conf.real_image()
                    
                    if self.is_draw_circles:
                        if self.bounce_frame >= 10:
                            self.bounce_frame = 0
                        else:
                            self.bounce_frame += 1
                            
                        draw_circles(self.img, self.number_movements, self.num_circles, self.is_movement_wrong, self.bounce_frame)
                    
                        
                    if len(self.confetti_particles) > 0:
                        self.img = draw_confetti(self.img, self.confetti_particles)
                        self.confetti_particles = [particle for particle in self.confetti_particles if particle.PosY < self.img.shape[0]]
                    
                    elif self.is_end_game:
                        self.show_end_score()
                    
                    elif not self.showed_players_teams:
                        self.show_player_teams()
                    
                    elif self.is_time_to_start:
                        self.time_to_start()
                        
                    elif self.is_showing_next_player:
                        self.show_next_player()
                        
                    elif self.is_showing_next_round:
                        self.show_message_new_round()

                    else:
                        self.my_identifier.process_image(self.real_image)
                        # draw_points(self.img, self.my_identifier.points)

                        if self.my_identifier.points:
                            if not self.player_found:
                                self.find_expected_player()
                                
                            elif self.sort_movement:
                                self.player_is_positioned()
                                
                            elif self.is_showing_start_messages:
                                self.show_start_message()

                            elif self.is_showing_movements:
                                self.game_mode.show_movement()

                            elif not self.is_movement_identified and not self.is_movement_wrong:
                                # Verifico se existe a necessidade de realizar um novo sorteio
                                self.movement_correct = (
                                    self.my_identifier.identify_list_movements(
                                        self.serial_id
                                    )
                                )

                                if self.movement_correct is None:
                                    pass
                                elif self.movement_correct:
                                    self.score_player += 1
                                    self.is_movement_wrong = False
                                    self.is_movement_identified = True
                                    self.timer_next_mov = time.perf_counter()
                                elif not self.movement_correct:
                                    self.timer_is_movement_wrong = time.perf_counter()
                                    self.is_movement_wrong = True
                                    print("MOVIMENTO ERRADO: ", self.list_players)

                            elif self.is_movement_wrong:
                                add_score((self.number_movements, self.expected_player.Id))
                                delta = (
                                    time.perf_counter() - self.timer_is_movement_wrong
                                )
                                if delta < 4:
                                    self.img = apply_filter(self.img, colors.RED)
                                else:
                                    self.call_next_player(True)
                            elif self.is_movement_identified:
                                self.movement_correct = (
                                    self.my_identifier.identify_list_movements(
                                        self.serial_id
                                    )
                                )
                                self.show_identified_movement()

                    video_conf.write(self.img)
                    
                    cv2.imshow(
                        screen_name, self.img
                    )  # exibe a imagem com os pontos na tela

                # verifica que teclas foram apertadas
                tecla = cv2.waitKey(
                    33
                )  # espera em milisegundos da execução das imagens
                if tecla == 27:  # verifica se foi a tecla esc
                    break

        video_conf.stop()
        cv2.destroyAllWindows()
