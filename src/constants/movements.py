#!/usr/bin/env python
# coding: utf-8

# Constantes que definem os movimentos
LEFT_HAND = 1
RIGHT_HAND = 2
JUMP = 3
CROUCH = 4

MOVEMENTS = (LEFT_HAND, RIGHT_HAND, JUMP, CROUCH)

MOVEMENTS_ORDER = {
    LEFT_HAND: "Mão Esquerda",
    RIGHT_HAND: "Mão Direita",
    JUMP: "Pule",
    CROUCH: "Agache",
}

MOVEMENTS_MESSAGE = {
    LEFT_HAND: "Mão Esquerda",
    RIGHT_HAND: "Mão Direita",
    JUMP: "Pulando",
    CROUCH: "Agachado",
}

MOVEMENTS_IMAGES = {
    LEFT_HAND: "left_hand.png",  # https://br.freepik.com/icone/levantar-silhueta-mao_62253#fromView=resource_detail&position=65
    RIGHT_HAND: "right_hand.png",  # https://br.freepik.com/icone/malhando-silhueta-braco-cima_62143#fromView=search&page=2&position=41&uuid=495787f1-ef1d-4a19-aea6-62d3eccaf9d9
    JUMP: "jump.png",  # https://br.freepik.com/icone/pessoa_11432220#fromView=search&page=1&position=0&uuid=d8cb86c4-b284-4747-8829-38b7bfc6c8fa
    CROUCH: "crouch.png",  # https://br.freepik.com/icone/filho_10060661#fromView=search&page=1&position=10&uuid=724adb7b-f148-49bf-b92d-026284b7fa98
}
