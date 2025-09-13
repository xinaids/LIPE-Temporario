#!/usr/bin/env python
# coding: utf-8

import src.constants.movements as mov
import src.poses.poses as poses
import random
import cv2
from cv2.typing import MatLike
import time
import os
from src.constants.constants import DIRECTORY_LOGS_IMAGE
import logging
from pathlib import Path

logging.basicConfig(
    level=logging.INFO,
    filename="execucoes.log",
    format="%(asctime)s - %(levelname)s - %(message)s",
)


# classe que identifica os movimentos do usuário
class Identifier(poses.Poses):
    def __init__(self, list_valid_movements:list[int]):
        
        #TODO: Liberar apenas os metodos liberados para o tipo de jogo
        self.MOVEMENTS_METHODS = [
            self.hand_left,
            self.hand_right,
            self.jump_identifier,
            self.crouch_identifier,
        ]

        super().__init__()

    def __str__(self):
        pass

    def process_image(self, img: MatLike):
        # manda o mediapipe processar a imagem
        self.copy_image = img.copy()
        result_processing = self.pose.process(self.copy_image)
        # pego os pontos detectados na imagem
        self.points = result_processing.pose_landmarks

        if self.points:  # se foi identificado algum ponto...
            self.mpDraw.draw_landmarks(
                self.copy_image, self.points, self.mpPose.POSE_CONNECTIONS
            )

            # capturo os dados das posições desejadas para este contexto
            self.handRX = float(
                self.points.landmark[self.mpPose.PoseLandmark.RIGHT_INDEX].x
            )
            self.handRY = float(
                self.points.landmark[self.mpPose.PoseLandmark.RIGHT_INDEX].y
            )
            self.handLX = float(
                self.points.landmark[self.mpPose.PoseLandmark.LEFT_INDEX].x
            )
            self.handLY = float(
                self.points.landmark[self.mpPose.PoseLandmark.LEFT_INDEX].y
            )
            self.noseX = float(self.points.landmark[self.mpPose.PoseLandmark.NOSE].x)
            self.noseY = float(self.points.landmark[self.mpPose.PoseLandmark.NOSE].y)
            self.shoulderRY = float(
                self.points.landmark[self.mpPose.PoseLandmark.RIGHT_SHOULDER].y
            )
            self.shoulderLY = float(
                self.points.landmark[self.mpPose.PoseLandmark.LEFT_SHOULDER].y
            )

    def hand_left(self) -> bool:
        # distancia levando em consideração apenas a altura
        distMaos = abs(self.handRY - self.handLY)

        # se a distância das mãos e dos pés bater nas medidas, ele incrementa as contagens
        if distMaos > 0.5:
            if self.noseY >= self.handRY:
                return False
            if self.noseY >= self.handLY:
                return True

        return False

    def hand_right(self) -> bool:
        # distancia levando em consideração apenas a altura
        distMaos = abs(self.handRY - self.handLY)

        # se a distância das mãos e dos pés bater nas medidas, ele incrementa as contagens
        if distMaos > 0.5:
            if self.noseY >= self.handLY:
                return False
            if self.noseY >= self.handRY:
                return True

        return False

    def jump_identifier(self) -> bool:
        actual_mid_y = (self.shoulderRY + self.shoulderLY) / 2

        # aceita variações de menos de 30%
        lower_bound = self.standing_mid_y - (self.standing_mid_y * 0.3)

        if actual_mid_y < lower_bound:
            return True

        return False

    def crouch_identifier(self) -> bool:
        actual_mid_y = (self.shoulderRY + self.shoulderLY) / 2

        # aceita variações de mais de 30%
        upper_bound = self.standing_mid_y + (self.standing_mid_y * 0.3)

        if actual_mid_y > upper_bound:
            return True

        return False

    def is_correct_positioned(self) -> bool:
        if self.shoulderRY == 0 or self.shoulderLY == 0:
            return False

        mid_shoulders = (self.shoulderRY + self.shoulderLY) / 2
        # verifica se a altura dos ombros está aceitavel
        if (mid_shoulders > 0.8) or (mid_shoulders < 0.2):
            return False

        self.standing_mid_y = mid_shoulders

        return True
        
    def sort_movements(self, list_movements:list[int], qtd: int = 1):
        self.list_commands = []
        for _ in range(qtd):
            self.list_commands.append(random.choice(list_movements))

        self.reset_seq_command()

    def identify(self) -> bool:
        match self.command:
            case mov.LEFT_HAND:
                return self.hand_left()

            case mov.RIGHT_HAND:
                return self.hand_right()

            case mov.JUMP:
                return self.jump_identifier()

            case mov.CROUCH:
                return self.crouch_identifier()

    def identify_list_movements(self, serial_id: int) -> bool | None:
        self.identified_movement = None

        if self.MOVEMENTS_METHODS[self.command - 1]():
            self.identified_movement = self.command
            self.save_log(
                mov.MOVEMENTS_ORDER[self.command], mov.MOVEMENTS_ORDER[self.command], serial_id
            )
            return True

        for i, fn in enumerate(self.MOVEMENTS_METHODS):
            if fn():
                self.identified_movement = i + 1
                self.save_log(
                    mov.MOVEMENTS_ORDER[self.command],
                    mov.MOVEMENTS_ORDER[i + 1],
                    serial_id,
                )
                return False

        return None

    def save_log(self, mov_command: str, move_identified: str, serial_id: int):
        timestamp = time.time()

        logging.info(
            f"{serial_id} - {str(timestamp)}, Movimento Esperado: {mov_command}, Retornado: {move_identified}, handRX: {self.handRX}, handRY: {self.handRY}, handLX: {self.handLX}, handLY: {self.handLY}, noseX: {self.noseX}, noseY: {self.noseY}, shoulderRY: {self.shoulderRY}, shoulderLY: {self.shoulderLY}, standing_mid_y: {self.standing_mid_y}"
        )

        Path(DIRECTORY_LOGS_IMAGE).mkdir(exist_ok=True)

        cv2.imwrite(
            DIRECTORY_LOGS_IMAGE
            + os.sep
            + "#"
            + str(serial_id)
            + "_"
            + str(timestamp)
            + ".jpg",
            self.copy_image,
        )

    def has_next_movement(self) -> bool:
        return self.seq_command < self.qtd_movements() - 1

    def qtd_movements(self) -> int:
        return len(self.list_commands)

    def seq_command(self) -> int:
        return self.seq_command

    def reset_seq_command(self):
        self.seq_command = 0
        self.command = self.list_commands[self.seq_command]

    def command_at(self, pos: int) -> int:
        return self.list_commands[pos]

    def points(self):
        return self.points

    def next_movement(self):
        self.seq_command += 1
        self.command = self.list_commands[self.seq_command]
        
    def list_commands(self, new_list_commands:list):
        self.list_commands = new_list_commands
        
    def list_commands(self)->list:
        return self.list_commands
