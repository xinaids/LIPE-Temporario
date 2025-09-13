#!/usr/bin/env python
# coding: utf-8

from src.constants.game_modes import SEQUENCE
from src.constants.movements import *
from src.constants.colors import RED, BLUE, GREEN, YELLOW
from src.screens.game.game import Game
from src.interfaces.game_mode import IGameMode
from src.draw.draw import (
    show_image_movements,
    draw_message_center_screen
)
import time
from src.constants.constants import *
from src.constants.timers import *


class SequenceGame(IGameMode, Game):
    def __init__(self):
        Game.__init__(self)

        self._mode = SEQUENCE
        self._list_movements = [LEFT_HAND, RIGHT_HAND, JUMP, CROUCH]

    def show_movement(self):
        if self.is_showing_repeat_msg:
            self.show_repeat_msg()
            return
        
        self.img = show_image_movements(
            img=self.img,
            command=self.my_identifier.command_at(self.mov_showing_seq),
            seq=self.mov_showing_seq + 1,
        )


        delta = time.perf_counter() - self.timer_is_showing_movements

        if delta > TIME_NEXT_MOVE:
            if self.mov_showing_seq < self.my_identifier.qtd_movements() - 1:
                self.timer_is_showing_movements = time.perf_counter()
                self.mov_showing_seq += 1
            else:
                self.is_showing_repeat_msg = True
                self.timer_repeat_msg = time.perf_counter()
                
    def show_repeat_msg(self):
        delta = time.perf_counter() - self.timer_repeat_msg

        if delta < TIME_SHOW_REPEAT_MESSAGE:
            self.img = draw_message_center_screen(self.img, "Repita os movimentos")
        else:
            # para de mostrar o movimento na tela
            self.is_showing_movements = False
            self.is_draw_circles = True

    def reset_variables_mode(self):
        self.timer_is_showing_movements = time.perf_counter()
        self.is_showing_repeat_msg = False
        pass

    def start(self, width: int, height: int):
        self.Show(width, height, self)

    @property
    def mode(self) -> int:
        return self._mode
    
    @property
    def list_movements(self) -> list[int]:
        return self._list_movements
