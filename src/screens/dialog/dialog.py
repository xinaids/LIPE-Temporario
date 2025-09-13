#!/usr/bin/env python
# coding: utf-8

import pygame
import sys
from src.constants.timers import *
from src.constants.constants import *
from src.constants.game_modes import *
from src.datatypes.dialog import Dialog
from src.constants.colors import *
from src.draw.dialog import *
from src.image.image import load_and_resize_png
import cv2

screen_name = "Identificador de Movimentos"

class DialogScreen:
    def __init__(self):       
        self.seq_dialog = 0

    def reset_variables(self):
        self.seq_dialog = 0
            
    def Show(self, width: int, height, dialogs:list[Dialog]):
        background_image = cv2.imread("images/park_background.jpg")
        background_image = cv2.blur(background_image, (15, 15))
        background_image = cv2.cvtColor(background_image, cv2.COLOR_BGR2RGB)
        
        self.background = pygame.image.frombuffer(
            background_image.tobytes(),
            (background_image.shape[1], background_image.shape[0]),
            "RGB"
        )
        
        is_running = True
        screen = pygame.display.set_mode((width, height), pygame.FULLSCREEN)
        clock = pygame.time.Clock()
        
        self.reset_variables()
        
        while is_running:
            character_image_path = dialogs[self.seq_dialog].Character_Dir
            if not os.path.exists(character_image_path):
                print(f"Erro: O arquivo de imagem não foi encontrado em '{character_image_path}'")
                pygame.quit()
                sys.exit()
            
            character_image = load_and_resize_png(character_image_path, (850, 850))
            character_dialog = dialogs[self.seq_dialog]
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    is_running = False
                    
                if event.type == pygame.MOUSEBUTTONUP:
                    self.seq_dialog += 1
                    if len(dialogs) <= self.seq_dialog:
                        return

            screen.blit(self.background, (0, 0))
            screen.blit(character_image, (0, 0))
            character_speak(screen, character_dialog)
            
            if not character_dialog.Animations is None:
                for animation in character_dialog.Animations:
                    animation.AnimateObj.animate(screen, animation.Position, animation.Scale)
                    animation.AnimateObj.increment_frame()


            pygame.display.update()

            clock.tick(5)