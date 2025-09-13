from typing import Protocol
import pygame

class Animatable(Protocol):
    def increment_frame(self) -> None:
        """Incrementa o quadro da animação"""
        pass

    def animate(self, screen: pygame.Surface,) -> None:
        """Executa a animação"""
        pass