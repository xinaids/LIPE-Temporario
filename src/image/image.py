import pygame
import cv2
from typing import Tuple

def load_and_resize_png(image_path: str, size: Tuple[int, int] = (512, 512)) -> pygame.Surface:
    image = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)
    if image is None:
        raise FileNotFoundError(f"Erro: O arquivo de imagem não foi encontrado em '{image_path}'")

    image = cv2.resize(image, size)

    # carrega o PNG com o fundo transparente
    return pygame.image.frombuffer(image.tobytes(), size, "BGRA")