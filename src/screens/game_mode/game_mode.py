#!/usr/bin/env python
# coding: utf-8

import pygame
import pygame_gui
from src.screens.players import players
from src.screens.loading import loading
from src.screens.game.condition_game import ConditionGame
from src.screens.game.sequence_game import SequenceGame
from src.constants.constants import DEVELOP_MODE
from src.screens.dialog.dialog import DialogScreen
from src.constants.dialog import *
from src.globals import variables

class GameMode:
    def __init__(self):
        self.window_surface = pygame.display.set_mode((1920, 1080), pygame.FULLSCREEN)
        
        self.background = pygame.image.load("images/background.jpg")
        self.window_surface.blit(self.background, (0, 0))
        self.manager = pygame_gui.UIManager(
            (self.window_surface.get_width(), self.window_surface.get_height()),
            "src/styles/style.json",
        )

        self.player_screen = players.PlayerScreen()
        self.dialog_screen = DialogScreen()

    def Show(self):
        btn_back = pygame_gui.elements.UIButton(
            pygame.Rect(5, 5, 200, 50),
            "VOLTAR",
            self.manager,
            anchors={"left": "left", "top": "top"},
        )
        
        btn_sequence = pygame_gui.elements.UIButton(
            pygame.Rect(0, -120, 500, 100),
            "SEQUÊNCIA",
            self.manager,
            anchors={"centerx": "centerx", "centery": "centery"},
        )

        btn_condition = pygame_gui.elements.UIButton(
            pygame.Rect(0, 0, 500, 100),
            "CONDIÇÃO",
            self.manager,
            anchors={"centerx": "centerx", "centery": "centery"},
        )

        btn_iteration = pygame_gui.elements.UIButton(
            pygame.Rect(0, 120, 500, 100),
            "REPETIÇÃO",
            self.manager,
            anchors={"centerx": "centerx", "centery": "centery"},
        )
        btn_iteration.disable()

        clock = pygame.time.Clock()
        is_running = True

        while is_running:
            time_delta = clock.tick(10) / 1000.0
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    is_running = False

                elif event.type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == btn_back:
                        is_running = False
                        
                    elif event.ui_element == btn_sequence:
                        self.game = SequenceGame()
                        
                        if not DEVELOP_MODE and not variables.Is_Traninig_Realized:
                            self.loading = loading.Loading(self.window_surface, self.background)
                            self.loading.Show()
                            
                        self.dialog_screen.Show(*pygame.display.get_window_size(), DIALOG_SEQUENCE)
                        self.game.start(*pygame.display.get_window_size())

                    elif event.ui_element == btn_condition:
                        self.game = ConditionGame()
                            
                        if not DEVELOP_MODE and not variables.Is_Traninig_Realized:
                            self.loading = loading.Loading(self.window_surface, self.background)
                            self.loading.Show()
                            
                        self.dialog_screen.Show(*pygame.display.get_window_size(), DIALOG_CONDITION)
                        self.game.start(*pygame.display.get_window_size())
                        
                    elif event.ui_element == btn_iteration:
                        # self.game = IterationGame()
                        
                        # if not DEVELOP_MODE and not variables.Is_Traninig_Realized:
                        #     self.loading = loading.Loading(self.window_surface, self.background)
                        #     self.loading.Show(self.game)

                        # self.dialog_screen.Show(*pygame.display.get_window_size(), DIALOG_ITERATION)
                        # self.game.start(*pygame.display.get_window_size())
                        pass
                    
                    pygame.event.clear()
                    
                self.manager.process_events(event)

            self.manager.set_window_resolution(
                (self.window_surface.get_width(), self.window_surface.get_height())
            )
            self.manager.update(time_delta)

            self.window_surface.blit(self.background, (0, 0))
            self.manager.draw_ui(self.window_surface)

            pygame.display.update()

        pygame.event.clear()