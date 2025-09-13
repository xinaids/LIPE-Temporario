import pygame
from src.constants.animation import ANIMATION_EXPLOSION_PATH

class ExplosionAnimation:
    def __init__(self):
        self.current_frame = 0

    def increment_frame(self):
        self.current_frame += 1

    def animate(self, screen: pygame.Surface, position = (0, 0), scale = 1):
        spritesheet = pygame.image.load(ANIMATION_EXPLOSION_PATH).convert_alpha()

        SHEET_WIDTH, SHEET_HEIGHT = 2000, 1333  # Dimensão total da imagem
        SPRITE_WIDTH, SPRITE_HEIGHT = SHEET_WIDTH // 4, SHEET_HEIGHT // 2  # Dimensão de cada frame
        NUM_COLUMNS, NUM_ROWS = 4, 2  # Organização da spritesheet
        FRAME_COUNT = NUM_COLUMNS * NUM_ROWS  # Total de frames

        # Criar uma lista de frames recortados
        frames = []
        for row in range(NUM_ROWS):
            for col in range(NUM_COLUMNS):
                frame = spritesheet.subsurface(
                    pygame.Rect(col * SPRITE_WIDTH, row * SPRITE_HEIGHT, SPRITE_WIDTH, SPRITE_HEIGHT)
                )
                frames.append(frame)

        if FRAME_COUNT == self.current_frame:
            self.current_frame = 0
            
        new_size = (frames[self.current_frame].get_width() * scale, frames[self.current_frame].get_height() * scale)

        resized_frame = pygame.transform.scale(frames[self.current_frame], new_size)

        screen.blit(resized_frame, position)

        # for self.current_frame in range(FRAME_COUNT):
        #     screen.blit(background)  # Limpa a tela para evitar sobreposição
        #     screen.blit(frames[self.current_frame], (0, 0))
        #     pygame.display.flip()  # Atualiza a tela para mostrar o novo frame
        #     clock.tick(10)
        