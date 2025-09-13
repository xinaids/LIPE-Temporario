#!/usr/bin/env python
# coding: utf-8

import cv2
from threading import Thread
import time
from cv2.typing import MatLike
from src.constants.constants import DIRECTORY_IMAGE_PLAYER, DIRECTORY_CAPTURES
import os


class VideoConfig:
    def __str__(self):
        return f"width {self.screen_width}, height {self.screen_height}"

    def __init__(
        self, screen_name: str, width: int, height: int, video_source: int = 0
    ):
        cv2.namedWindow(screen_name, cv2.WND_PROP_FULLSCREEN)
        cv2.setWindowProperty(
            screen_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN
        )
        cv2.setUseOptimized(True)

        # abre o fluxo de leitura
        self.video_cap = cv2.VideoCapture(video_source, cv2.CAP_DSHOW)
        if self.video_cap.isOpened() is False:
            print("[Exiting]: Erro ao acessar a WebCam.")
            exit(0)

        self.set_screen_size(width, height)
        self.video_cap.set(cv2.CAP_PROP_FPS, 30)

        self.grabbed, self.frame = self.video_cap.read()
        if self.grabbed is False:
            print("[Exiting] Não existem mais frames para leitura")
            exit(0)

        self.stopped = True

        self.t = Thread(target=self.update, args=())
        self.t.daemon = True  # daemon threads keep running in the background while the program is executing

        real_width = int(self.video_cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        real_height = int(self.video_cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        codec = cv2.VideoWriter_fourcc(*"mp4v")  # Codec para o formato AVI

        timestamp = time.time()
        self.out_cap = cv2.VideoWriter(
            f"{DIRECTORY_CAPTURES}{os.sep}{timestamp}-saida.mp4",
            codec,
            20.0,
            (real_width, real_height),
        )

    def start(self):
        self.stopped = False
        self.t.start()

    def update(self):
        while True:
            if self.stopped is True:
                break
            self.grabbed, self.frame = self.video_cap.read()
            if self.grabbed is False:
                print("[Exiting] Não existem mais frames para leitura")
                self.stopped = True
                break

        self.video_cap.release()
        self.out_cap.release()

    def set_screen_size(self, screen_width: int, screen_height: int):
        self.screen_width = int(screen_width)
        self.screen_height = int(screen_height)

        self.video_cap.set(cv2.CAP_PROP_FRAME_WIDTH, screen_width)
        self.video_cap.set(cv2.CAP_PROP_FRAME_HEIGHT, screen_height)

    def read(self) -> MatLike:
        return cv2.flip(self.frame, 1)

    # imagem real sem a inversão
    def real_image(self) -> MatLike:
        return self.frame

    def stop(self):
        self.stopped = True
        self.t.join()

    def video(self) -> cv2.VideoCapture:
        return self.video_cap

    def height(self) -> int:
        return self.screen_height

    def width(self) -> int:
        return self.screen_width

    def write(self, img: MatLike):
        self.out_cap.write(img)