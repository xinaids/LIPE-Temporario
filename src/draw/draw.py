#!/usr/bin/env python
# coding: utf-8

import cv2
import numpy as np
from PIL import Image, ImageFont, ImageDraw
import src.constants.colors as colors
from cv2.typing import MatLike
import cvzone
import src.constants.movements as mov
from src.constants.fonts import PRIMARY_FONT, SECONDARY_FONT, FONT_ARIAL_PATH
import os
from src.datatypes.confetti import Confetti
from typing import List


# TODO: Revisar todas os textos mostrados em tela para utilizar o PIL
def draw_rectangle(img: MatLike, text: str, text_size, position):
    cv2.rectangle(
        img,
        (position[0] - 50, position[1] - 50),
        (position[0] + text_size[0] + 50, position[1] + text_size[1] + 10),
        colors.ORANGE,
        -1,
    )
    cv2.putText(img, text, (position[0], position[1]), PRIMARY_FONT, 1, colors.WHITE, 2)


def write_center_screen(img: MatLike, text: str):
    img_height = img.shape[0]
    img_width = img.shape[1]

    text_size = cv2.getTextSize(text, PRIMARY_FONT, 1, 2)[0]
    textX = int((img_width - text_size[0]) / 2)
    textY = int((img_height + text_size[1]) / 2)
    draw_rectangle(img, text, text_size, (textX, textY))


def initial_message(img: MatLike):
    img_height = img.shape[0]
    img_width = img.shape[1]

    # escreve titulo
    title = "IDENTIFICADOR DE MAOS"
    title_size = cv2.getTextSize(title, PRIMARY_FONT, 1, 2)[0]
    titleX = int((img_width - title_size[0]) / 2)
    titleY = int((img_height + title_size[1]) / 2)
    draw_rectangle(img, title, title_size, (titleX, titleY))

    # Escreve orientações
    text = "Aperte 'esc' para sair"
    text_size = cv2.getTextSize(text, SECONDARY_FONT, 1, 1)[0]
    textX = int((img_width - text_size[0]) / 2)
    textY = int((img_height - text_size[1] - 20))
    cv2.putText(img, text, (textX, textY), SECONDARY_FONT, 1, colors.WHITE, 1)


def draw_message(img: MatLike, message: str):
    cv2.rectangle(img, (1, 0), (260, 30), colors.ORANGE, -1)

    pil_image = Image.fromarray(img)

    font = ImageFont.truetype(FONT_ARIAL_PATH, size=15)
    draw = ImageDraw.Draw(pil_image)

    draw.text((15, 5), message, font=font, stroke_width=1, stroke_fill=colors.BLACK)
    return np.asarray(pil_image)

def draw_message_position(img: MatLike, message: str, position: tuple[int, int], size: tuple[int, int]) -> MatLike:
    x, y = position
    width, height = size
    
    img_copy = np.copy(img)

    cv2.rectangle(img_copy, (x, y), (x + width, y + height), colors.ORANGE, -1)

    pil_image = Image.fromarray(img_copy)

    font = ImageFont.truetype(FONT_ARIAL_PATH, size=18)
    draw = ImageDraw.Draw(pil_image)
    
    _, _, text_width, text_height = font.getbbox(text=message, stroke_width=1)
    text_x = x + (width - text_width) // 2
    text_y = y + (height - text_height) // 2


    draw.text((text_x, text_y), message, font=font, stroke_width=1, stroke_fill=colors.BLACK)
    return np.asarray(pil_image)


def draw_points(img: MatLike, points):
    # um laço de repetição para percorrer todos os pontos e desenhar um círculo e o número do ponto
    for id, lm in enumerate(points.landmark):
        # print(f'ponto: {id}') #imprime os dados do ponto no terminal
        # print(lm);
        # calcula os pontos considerando as dimensões da tela
        cx, cy = int(lm.x * img.shape[1]), int(lm.y * img.shape[0])
        cv2.putText(
            img,
            str(int(id)),
            (cx + 5, cy - 5),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.3,
            colors.RED,
            1,
        )  # escreve o número do ponto
        cv2.circle(img, (cx, cy), 3, colors.RED, cv2.FILLED)  # desenha um círculo


def show_image_movements(img: MatLike, command: int = None, seq: int = None, color_background = colors.BLUE_LIGHT, show_image:bool = True):
    image = apply_filter(img, color_background)
    h_background, w_background, _ = image.shape

    if show_image and command:
        img_movement = cv2.imread(
            "images" + os.sep + mov.MOVEMENTS_IMAGES[command], cv2.IMREAD_UNCHANGED
        )
        img_movement = cv2.resize(img_movement, (0, 0), None, 0.5, 0.5)

        h_img_mov, w_img_mov, _ = img_movement.shape

        pos_x = (w_background - w_img_mov) // 2
        pos_y = (h_background - h_img_mov) // 2
        cvzone.overlayPNG(image, img_movement, [pos_x, pos_y])
    
    pil_image = Image.fromarray(image)

    if command and seq:
        order = f"{seq} - {mov.MOVEMENTS_ORDER[command]}"
    elif seq:
        order = f"{seq}"
    elif command:
        order = mov.MOVEMENTS_ORDER[command]
    else:
        order = ""
    
    font = ImageFont.truetype(FONT_ARIAL_PATH, size=25)
    draw = ImageDraw.Draw(pil_image)

    _, _, text_width, text_height = font.getbbox(text=order, stroke_width=1)

    if show_image and command:
        textX = int((w_background - text_width) / 2)
        textY = int(pos_y + h_img_mov)
    else:
        textX = int((w_background - text_width) / 2)
        textY = h_background - text_height - 50
        
    draw.text(
        (textX, textY), order, font=font, stroke_width=1, stroke_fill=colors.BLACK
    )
    image = np.asarray(pil_image)

    return image


def show_player_image(img: MatLike, seq_player: int = None, text_color: tuple[int, int, int] = colors.ORANGE, order:str = "") -> MatLike | None:
    dir_img_profile = f"PlayerImages{os.sep}{seq_player}{os.sep}profile.jpg"
    img_profile = cv2.imread(dir_img_profile, cv2.IMREAD_UNCHANGED)

    img_profile = cv2.resize(img_profile, (0, 0), fx=0.6, fy=0.6)

    h_background, w_background, _ = img.shape
    h_img_prof, w_img_prof, _ = img_profile.shape

    pos_y = (h_background - h_img_prof) // 2

    x_offset = (w_background - w_img_prof) // 2
    y_offset = (h_background - h_img_prof) // 2

    img[
        y_offset : y_offset + h_img_prof,
        x_offset : x_offset + w_img_prof,
    ] = img_profile

    pil_image = Image.fromarray(img)

    if len(order) > 0:
        font = ImageFont.truetype(FONT_ARIAL_PATH, size=35)
        draw = ImageDraw.Draw(pil_image)

        _, _, text_width, text_height = font.getbbox(text=order, stroke_width=1)

        textX = int((w_background - text_width) / 2)
        textY = int(pos_y + h_img_prof)
        draw.text(
            (textX, textY), order, font=font, stroke_width=1, stroke_fill=text_color
        )
        
    image = np.asarray(pil_image)

    return image

def show_score(img: MatLike, scoreA: int, scoreB: int) -> MatLike:
    # Obtém as dimensões da imagem
    h_background, w_background, _ = img.shape

    # Converte para imagem PIL
    pil_image = Image.fromarray(img)

    # Fonte e estilo
    font = ImageFont.truetype(FONT_ARIAL_PATH, size=55)
    draw = ImageDraw.Draw(pil_image)

    # Texto para os scores
    text_scoreA = f"TIME VERMELHO: {scoreA}"
    text_scoreB = f"TIME AZUL: {scoreB}"

    # Calcula as posições do texto
    _, _, text_widthA, text_heightA = font.getbbox(text=text_scoreA, stroke_width=1)
    _, _, text_widthB, text_heightB = font.getbbox(text=text_scoreB, stroke_width=1)

    # Centraliza horizontalmente e posiciona verticalmente
    textX_A = int((w_background - text_widthA) / 2)
    textY_A = 250  # Offset para o score A

    textX_B = int((w_background - text_widthB) / 2)
    textY_B = textY_A + text_heightA + 100  # Espaçamento entre os textos

    # Desenha os textos
    draw.text(
        (textX_A, textY_A),
        text_scoreA,
        font=font,
        stroke_width=1,
        stroke_fill=colors.RED,
        fill="white",
    )
    draw.text(
        (textX_B, textY_B),
        text_scoreB,
        font=font,
        stroke_width=1,
        stroke_fill=colors.BLUE,
        fill="white",
    )

    # Converte de volta para o formato NumPy
    image = np.asarray(pil_image)

    return image


def show_correct_position(img: MatLike)->MatLike:
    image_filter = apply_filter(img, colors.GREEN)

    img_pos = cv2.imread(
        f"images{os.sep}silhueta.png", cv2.IMREAD_UNCHANGED
    )

    h_background, w_background, _ = image_filter.shape
    h_img_mov, w_img_mov, _ = img_pos.shape

    pos_x = (w_background - w_img_mov) // 2
    pos_y = (h_background - h_img_mov) // 2
    cvzone.overlayPNG(image_filter, img_pos, [pos_x, pos_y])

    pil_image = Image.fromarray(image_filter)

    order = "SE POSICIONE CORRETAMENTE"

    font = ImageFont.truetype(FONT_ARIAL_PATH, size=20)
    draw = ImageDraw.Draw(pil_image)

    _, _, text_width, text_height = font.getbbox(text=order, stroke_width=1)

    textX = int((w_background - text_width) / 2)
    textY = int(pos_y + h_img_mov)
    draw.text(
        (textX, textY), order, font=font, stroke_width=1, stroke_fill=colors.BLACK
    )
    image = np.asarray(pil_image)

    return image

def apply_filter(img: MatLike, color: tuple[3]) -> MatLike:
    blue_layer = np.full(img.shape, color, dtype=np.uint8)

    blended_img = cv2.addWeighted(img, 0.5, blue_layer, 0.5, 0)

    return blended_img


def draw_face_positioning(img: MatLike) -> MatLike:
    height, width, _ = img.shape
    center_coordinates = (width // 2, height // 2)
    axesLength = (width // 3 - 100, height // 3)
    angle = 90
    startAngle = 0
    endAngle = 360
    thickness = -1

    mask = np.zeros(img.shape[:2], dtype="uint8")
    cv2.ellipse(
        mask, center_coordinates, axesLength, angle, startAngle, endAngle, 255, -1
    )
    return cv2.bitwise_and(img, img, mask=mask)


def draw_message_center_screen(img: MatLike, text: str, color:tuple[3] = colors.BLACK) -> MatLike:
    img_height, img_width, _ = img.shape

    pil_image = Image.fromarray(img)

    font = ImageFont.truetype(FONT_ARIAL_PATH, size=70)
    draw = ImageDraw.Draw(pil_image)

    _, _, text_width, text_height = font.getbbox(text=text, stroke_width=1)
    textX = int((img_width - text_width) / 2)
    textY = int((img_height - text_height - 50))
    draw.text((textX, textY), text, font=font, stroke_width=1, stroke_fill=color)

    image = np.asarray(pil_image)
    return image


def write_message(img: MatLike, message: str) -> MatLike:
    img_height, img_width, _ = img.shape

    pil_image = Image.fromarray(img)

    # Draw non-ascii text onto image
    font = ImageFont.truetype(FONT_ARIAL_PATH, size=40)
    draw = ImageDraw.Draw(pil_image)

    _, _, text_width, text_height = font.getbbox(text=message, stroke_width=1)
    textX = int((img_width - text_width) / 2)
    textY = int((img_height - text_height - 50))
    draw.text((textX, textY), message, font=font, stroke_width=1, stroke_fill=colors.BLACK)

    image = np.asarray(pil_image)
    return image


def draw_circles(
    img: MatLike, num_circles: int, last_correct: int, wrong_move: bool = False, bounce_frame: int = 0
):
    height, width, _ = img.shape
    overlay = img.copy()

    radius = 30  # Raio fixo para os círculos
    margin = 10  # Margem entre os círculos

    # Definir o número de círculos por linha (no máximo 3 por linha)
    if num_circles <= 3:
        circles_in_first_line = num_circles
        draw_second_line = False
    else:
        circles_in_first_line = num_circles // 2
        draw_second_line = True

    font_scale = 1.5
    font_thickness = 3
    thickness_border = 10
    opacity = 0.5

    # Função para desenhar uma linha de círculos
    def draw_circle_line(start_count: int, num_circles_in_line: int, y_center: int):
        # Calcular o espaçamento horizontal para centralizar os círculos
        total_width = (num_circles_in_line + start_count) * (2 * radius + margin) - margin
        start_x = (width - total_width) // 2 + radius

        for i in range(start_count, num_circles_in_line):
            if last_correct > i:
                color_circle = colors.GREEN
                text = "V"
            elif last_correct == i and wrong_move:
                color_circle = colors.RED
                text = "X"
            else:
                color_circle = colors.GRAY
                text = "-"

            bounce_effect = 0
            if i == last_correct and bounce_frame > 0:
                bounce_values = [0, 4, 7, 4, 0]  # Pode ajustar esse vetor pra suavidade
                bounce_effect = bounce_values[bounce_frame % len(bounce_values)]

            adjusted_radius = radius + bounce_effect
            center_x = start_x + i * (2 * radius + margin)
            
            cv2.circle(img, (center_x, y_center), adjusted_radius, color_circle, thickness=-1)
            cv2.circle(img, (center_x, y_center), adjusted_radius, thickness_border)

            (text_width, text_height), _ = cv2.getTextSize(
                text, PRIMARY_FONT, font_scale, font_thickness
            )
            text_x = center_x - text_width // 2
            text_y = y_center + text_height // 2

            cv2.putText(
                img,
                text,
                (text_x, text_y),
                PRIMARY_FONT,
                font_scale,
                colors.WHITE,
                font_thickness,
            )

    if circles_in_first_line > 0:
        y_first_line = height - 2 * radius - 50
        draw_circle_line(0, circles_in_first_line, y_first_line)

    if draw_second_line:
        y_second_line = height - radius - 20
        draw_circle_line(circles_in_first_line, num_circles, y_second_line)

    cv2.addWeighted(overlay, opacity, img, 1 - opacity, 0, img)

    return img

def draw_confetti(img, confetti_particles: List[Confetti]):
    for particle in confetti_particles:
        cv2.circle(img, (particle.PosX, particle.PosY), 5, particle.Color, -1)
        particle.PosY += particle.Speed
    
    return img

def draw_text_top_right(img: MatLike, order: str) ->MatLike:
    pil_image = Image.fromarray(img)

    img_height, img_width, _ = img.shape

    font = ImageFont.truetype(FONT_ARIAL_PATH, size=20)

    _, _, text_width, text_height = font.getbbox(text=order, stroke_width=1)

    textX = int((img_width - text_width)) - 20
    textY = 0
    
    draw = ImageDraw.Draw(pil_image)

    draw.text((textX, textY), order, font=font, stroke_width=1, stroke_fill=colors.BLACK)
    return np.asarray(pil_image)