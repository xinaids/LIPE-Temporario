#!/usr/bin/env python
# coding: utf-8

import cv2
import time
import random
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from typing import List


from src.video_config.video_config import VideoConfig
import src.identifier.identifier as identifier
import src.constants.movements as mov
import src.constants.colors as colors
from src.constants.timers import *
from src.constants.constants import *
from src.datatypes.confetti import Confetti
from src.constants.game_modes import *
from src.datatypes.player import Player
from src.draw.draw import (
    draw_message,
    draw_circles,
    draw_message_center_screen,
    apply_filter,
    write_message,
    draw_confetti,
    show_score,
    show_error_feedback,
)
from database.students.students import select_students
from database.scores.scores import add_score
from src.interfaces.game_mode import IGameMode

screen_name = "Jogo de Movimentos"

class Game:
    def __init__(self):       
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

        # cronometros da exibicao de times/jogadores: inicializados aqui para
        # existirem antes da primeira leitura (evita AttributeError no inicio da partida).
        self.timer_show_msg_teams = time.perf_counter()
        self.timer_show_players_teams = time.perf_counter()

        # estados de fluxo lidos no loop principal antes de serem definidos no meio da logica.
        self.is_time_to_start = False
        self.is_showing_next_player = False
        
        self.is_showing_start_messages = False
        self.is_showing_movements = False
        self.is_movement_wrong = False
        self.is_movement_identified = False
        self.is_draw_circles = False
        self.bounce_frame = 0
        self.movement_correct = False

        self.mov_showing_seq = 0
        self.num_circles = 0
        
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
            
    def player_is_positioned(self):
        self.my_identifier.process_image(self.real_image)

        if self.my_identifier.is_correct_positioned():
            self.sort_movement = False
            self.is_showing_start_messages = True
            self.timer_message_start = time.perf_counter()
        else:
            self.img = draw_message_center_screen(self.img, "Posicione-se corretamente!", colors.RED)
            
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
        
        team_filter = [player for player in self.list_players if player.Team == self.show_team_id]
        
        delta = time.perf_counter() - self.timer_show_players_teams
        if delta < TIME_SHOW_PLAYER and self.count_player_Show < len(team_filter):
            nome = team_filter[self.count_player_Show].Name
            self.img = draw_message_center_screen(self.img, nome, color)
        else:
            if self.count_player_Show < len(team_filter) - 1:
                self.count_player_Show += 1
            elif self.show_team_id == "A":
                 # terminou time A, troca para B
                 self.count_player_Show = 0
                 self.show_team_id = "B"
                 self.timer_show_msg_teams = time.perf_counter()
                 return
            elif self.show_team_id == "B":
             # terminou time B, encerra a exibição
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
       
        self.set_player(self.expected_player.Name, remove_player)

     
        if self.expected_player.Movements:
            self.my_identifier.list_commands = list(self.expected_player.Movements)
        else:
            self.my_identifier.sort_movements(self.game_mode.list_movements,
                                              self.number_movements)
            self.expected_player.Movements = list(self.my_identifier.list_commands)

    
        self.my_identifier.reset_seq_command()

      
        self.reset_variables()
        self.game_mode.reset_variables_mode()
        self.my_identifier.arm_detection()

        self.sort_movement = True
        self.is_showing_start_messages = True
        self.number_start_message = 0

      self.is_showing_next_player = True
      self.timer_show_player = time.perf_counter()

    
    def get_next_player(self, current_name:str)-> Player | None:
        next_player = None
        current_player_found = False
        
        for p in self.list_players:
            if current_player_found:
                next_player = p
                break
                
            if p.Name == current_name:
                current_player_found = True
                
        return next_player
    
    def set_player(self, previous_name:str, remove_previous_player:bool):
        next_player = self.get_next_player(previous_name)
        
        if remove_previous_player: 
            self.list_players = [p for p in self.list_players if p.Name != previous_name]
                
        if not next_player:
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

        self.my_identifier.reset_seq_command()
            
        self.expected_player = next_player
            
    def is_last_round(self)->bool:
        team_a_found = any(p.Team == "A" for p in self.list_players)
        team_b_found = any(p.Team == "B" for p in self.list_players)
        return not (team_a_found and team_b_found)
        
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
        color = colors.RED if self.expected_player.Team == "A" else colors.BLUE
        nome = self.expected_player.Name
        self.img = draw_message_center_screen(self.img, f"PRÓXIMO: {nome}", color)

        delta = time.perf_counter() - self.timer_show_player
        if delta > TIME_SHOW_PLAYER:
            self.is_showing_next_player = False
            self.player_found = True  # já está definido
        
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
        
        video_conf = VideoConfig(screen_name, width=width, height=height)
        video_conf.start()

        self.my_identifier = identifier.Identifier(self.game_mode.list_movements)
        self.my_identifier.sort_movements(self.game_mode.list_movements, self.number_movements)
        db_players = select_students()
        self.list_players = []
        team = "A"
        for p in db_players:
          p.Team = team
             
          p.Movements = list(getattr(p, "Movements", []))
          self.list_players.append(p)
          team = "B" if team == "A" else "A"

        if not self.list_players:
          print("Nenhum jogador encontrado no banco de dados. Encerrando jogo.")
          video_conf.stop()
          cv2.destroyAllWindows()
        

        self.expected_player = self.list_players[0]

        self.expected_player.Movements = list(self.my_identifier.list_commands)
        
        self.is_end_game = False
        self.showed_players_teams = False
        self.is_running = True

        with ThreadPoolExecutor(max_workers=4) as self.executor:
            while self.is_running:
                if video_conf.stopped: break
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

                    if self.my_identifier.points:
                        if self.sort_movement:
                            self.player_is_positioned()
                                
                        elif self.is_showing_start_messages:
                            self.show_start_message()

                        elif self.is_showing_movements:
                            self.game_mode.show_movement()

                        elif not self.is_movement_identified and not self.is_movement_wrong:
                            self.movement_correct = self.my_identifier.identify_list_movements(self.serial_id, self.expected_player.Name)

                            if self.movement_correct is None:
                                pass
                            elif self.movement_correct:
                                self.score_player += 1
                                self.is_movement_wrong = False
                                self.is_movement_identified = True
                                self.timer_next_mov = time.perf_counter()
                            else:
                                self.timer_is_movement_wrong = time.perf_counter()
                                self.is_movement_wrong = True

                        elif self.is_movement_wrong:
                            add_score((self.number_movements, self.expected_player.Name))
                            delta = time.perf_counter() - self.timer_is_movement_wrong
                            if delta < 4:
                                self.img = apply_filter(self.img, colors.RED)
                                if self.my_identifier.identified_movement is not None:
                                    self.img = show_error_feedback(
                                        self.img,
                                        self.my_identifier.identified_movement,
                                        self.my_identifier.command,
                                    )
                            else:
                                self.call_next_player(True)
                        elif self.is_movement_identified:
                            self.movement_correct = self.my_identifier.identify_list_movements(self.serial_id, self.expected_player.Name)
                            self.show_identified_movement()

                
                cv2.imshow(screen_name, self.img)

                tecla = cv2.waitKey(33)
                if tecla == 27:  # esc
                    break

        video_conf.stop()
        cv2.destroyAllWindows()