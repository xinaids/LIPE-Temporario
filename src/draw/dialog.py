import pygame
from cv2.typing import MatLike
from src.constants.fonts import FONT_ARIAL_PATH
from src.datatypes.dialog import Dialog

def wrap_text(text: str, font: pygame.font.Font, max_width: int) -> list[str]:
    """
    Divide o texto em múltiplas linhas para caber no retângulo.

    :param text: Texto a ser renderizado.
    :param font: Fonte usada para renderizar o texto.
    :param max_width: Largura máxima permitida.
    :return: Lista de linhas do texto ajustadas ao tamanho.
    """
    words = text.split()
    lines = []
    current_line = []

    for word in words:
        # Testa se a linha atual mais a nova palavra cabem na largura máxima
        test_line = " ".join(current_line + [word])
        if font.size(test_line)[0] <= max_width:
            current_line.append(word)
        else:
            lines.append(" ".join(current_line))
            current_line = [word]

    if current_line:
        lines.append(" ".join(current_line))

    return lines


def character_speak(screen: pygame.Surface, character_dialog: Dialog, text_rect_height=150):

    font = pygame.font.Font(FONT_ARIAL_PATH, 30)
    font.set_italic(character_dialog.Italic)
    font.set_bold(character_dialog.Bold)

    text_rect = pygame.Rect(
        0,
        screen.get_height() - text_rect_height,
        screen.get_width(),
        text_rect_height,
    )

    # Dividir o texto em múltiplas linhas
    max_width = text_rect.width - 20  # Margem para o texto
    lines = wrap_text(character_dialog.Text, font, max_width)

    # Garantir que o texto caiba na altura do retângulo
    line_height = font.get_linesize()
    max_lines = text_rect.height // line_height
    lines = lines[:max_lines]  # Truncar linhas se necessário

    pygame.draw.rect(screen, (255, 255, 255), text_rect)  # Retângulo branco
    pygame.draw.rect(screen, (0, 0, 0), text_rect, 2)  # Borda preta no retângulo

    # Renderizar o texto linha por linha
    for i, line in enumerate(lines):
        rendered_text = font.render(line, True, (0, 0, 0))  # Texto preto
        screen.blit(rendered_text, (text_rect.x + 10, text_rect.y + 10 + i * line_height))
        
    click_to_continue(screen)

def click_to_continue(screen: pygame.Surface):
    # Clique para continuar
    fontSecondary = pygame.font.Font(FONT_ARIAL_PATH, 24)
    fontSecondary.set_italic(True)
    
    text = "Clique para continuar"
    
    rendered_text = fontSecondary.render(text, True, (0, 0, 0))  # Texto preto
    
    x_pos = screen.get_width() - rendered_text.get_width() - 10
    y_pos = screen.get_height() - rendered_text.get_height() - 10
    
    screen.blit(rendered_text, (x_pos, y_pos))
