#!/usr/bin/env python
# coding: utf-8

from src.constants.game_modes import CONDITION
from src.constants.movements import *
from src.constants.colors import RED, BLUE, BLUE_LIGHT, GREEN, YELLOW
from src.screens.game.game import Game
import random
from src.interfaces.game_mode import IGameMode
from src.draw.draw import (
    show_image_movements,
    apply_filter,
    write_message,
    draw_message_center_screen,
)
import time
from src.constants.constants import *
from src.constants.timers import *
import src.constants.colors as colors


class ConditionGame(IGameMode, Game):
    def __init__(self):
        Game.__init__(self)

        self._mode = CONDITION
        self._list_movements = [LEFT_HAND, RIGHT_HAND]

    def show_movement(self):
        if not self.is_showing_representation:
            self.is_showing_representation = True
            self.color_move_representation()
        
        if not self.is_showed_representation:
            self.show_representation_movement()
            return
        
        if self.is_showing_repeat_msg:
            self.show_repeat_msg()
            return

        self.img = show_image_movements(
            img=self.img,
            seq=self.mov_showing_seq + 1,
            color_background=self.move_in_colors.get(self.my_identifier.list_commands[self.mov_showing_seq]),
            show_image=False
        )

        delta = time.perf_counter() - self.timer_is_showing_movements

        if delta > TIME_NEXT_MOVE:
            if self.mov_showing_seq < self.my_identifier.qtd_movements() - 1:
                self.timer_is_showing_movements = time.perf_counter()
                self.mov_showing_seq += 1
            else:
                self.is_showing_repeat_msg = True
                self.timer_repeat_msg = time.perf_counter()

    def show_representation_movement(self):
        self.img = show_image_movements(
            img=self.img,
            command=self.move_representation_seq,
            color_background=list(self.move_in_colors.values())[self.move_representation_seq - 1],
        )

        self.img = write_message(
            self.img,
            colors.COLOR_NAME.get(
                self.move_in_colors.get(self.move_representation_seq)
            ),
        )

        delta = time.perf_counter() - self.timer_is_showing_movements

        if delta > TIME_SHOW_MOVEMENT_REPRESENTATION:
            if self.move_representation_seq < len(self.move_in_colors):
                self.timer_is_showing_movements = time.perf_counter()
                self.move_representation_seq += 1
            else:
                self.timer_is_showing_movements = time.perf_counter()
                self.is_showed_representation = True
    
    def show_repeat_msg(self):
        delta = time.perf_counter() - self.timer_repeat_msg

        if delta < TIME_SHOW_REPEAT_MESSAGE:
            self.img = draw_message_center_screen(self.img, "Repita os movimentos")
        else:
            # para de mostrar o movimento na tela
            self.is_showing_movements = False
            self.is_draw_circles = True
            
    def color_move_representation(self):
        colors = [RED, BLUE, GREEN, YELLOW]

        #sorteando todas as vezes o jogo ficou muito dificil
        #então manter as cores fixas para cada movimento e utilizar apenas 3
        self.move_in_colors = {
            LEFT_HAND: RED,
            RIGHT_HAND: BLUE,
            # JUMP: GREEN,
            # CROUCH: YELLOW,
        }

        # for mov in MOVEMENTS:
        #     rand_color = random.choice(colors)
        #     self.move_in_colors[mov] = rand_color
        #     colors.remove(rand_color)

    def reset_variables_mode(self):
        self.is_showing_representation = False
        self.move_representation_seq = 1
        self.is_showed_representation = False
        self.is_showing_repeat_msg = False
        self.timer_repeat_msg = 0

    def start(self, width: int, height: int):
        self.Show(width, height, self)

    @property
    def mode(self) -> int:
        return self._mode

    @property
    def list_movements(self) -> list[int]:
        return self._list_movements
