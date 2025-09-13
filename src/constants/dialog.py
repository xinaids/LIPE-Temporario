from src.datatypes.dialog import Animation, Dialog
from src.animation.explosion import ExplosionAnimation
import os

CHARACTER_DIALOG = "images" + os.sep + "robot" + os.sep + "lipe.png"
CHARACTER_DIALOG2 = "images" + os.sep + "robot" + os.sep + "lipe2.png"

DIALOG_START_GAME = [
    Dialog(
        Text="Olá, eu sou o Lipe, o robô do Laboratório Inteligente voltado para Educação",
        Character_Dir=CHARACTER_DIALOG,
    ),
    Dialog(
        Text="O Lipe, como todos os outros robôs, não sabe o que fazer sozinho.",
        Character_Dir=CHARACTER_DIALOG,
        Italic=True,
    ),
    Dialog(
        Text="Para que ele consiga realizar tarefas, os programadores precisam ensiná-lo usando algo chamado algoritmo.",
        Character_Dir=CHARACTER_DIALOG,
        Italic=True,
    ),
    Dialog(
        Text="Um algoritmo é escrito através de uma linguagem especial que o computador do robô consegue entender.",
        Character_Dir=CHARACTER_DIALOG2,
        Italic=True,
    ),
    Dialog(
        Text="Essa linguagem é chamada de código.",
        Character_Dir=CHARACTER_DIALOG,
        Italic=True,
    ),
    Dialog(
        Text="O computador lê o código e segue os passos do algoritmo.",
        Character_Dir=CHARACTER_DIALOG,
        Italic=True,
    ),
    Dialog(
        Text="Mas temos um problema, o Lipe bateu a cabeça, o que prejudicou sua memória.",
        Character_Dir=CHARACTER_DIALOG,
        Italic=True,
        Animations=[Animation(AnimateObj=ExplosionAnimation(), Position=(300, -100), Scale = 0.5)],
    ),
    Dialog(
        Text="Ele não lembra como seguir os passos de um algoritmo.",
        Character_Dir=CHARACTER_DIALOG,
        Italic=True,
        Animations=[Animation(AnimateObj=ExplosionAnimation(), Position=(300, -100), Scale = 0.5)],
    ),
    Dialog(
        Text="Para ajudá-lo vocês deverão executar os passos de alguns algoritmos.",
        Character_Dir=CHARACTER_DIALOG,
        Italic=True,
    ),
    Dialog(
        Text="Vamos lá?",
        Character_Dir=CHARACTER_DIALOG,
        Italic=True,
        Bold=True,
    ),
]

DIALOG_SEQUENCE = [
    Dialog(
        Text="Sequência é tipo uma receita!",
        Character_Dir=CHARACTER_DIALOG,
    ),
    Dialog(
        Text="Primeiro faz isso, depois aquilo... sempre na ordem certinha!",
        Character_Dir=CHARACTER_DIALOG,
    ),
    Dialog(
        Text="Imagine que você tem uma missão: ajudar o robô a descer o escorregador!",
        Character_Dir=CHARACTER_DIALOG,
    ),
    Dialog(
        Text="Você seguirá a seguinte ordem:",
        Character_Dir=CHARACTER_DIALOG,
    ),
    Dialog(
        Text="1 - Ande até o escorregador.",
        Character_Dir=CHARACTER_DIALOG,
    ),
    Dialog(
        Text="2 - Suba as escadinhas.",
        Character_Dir=CHARACTER_DIALOG,
    ),
    Dialog(
        Text="3 - Sente no topo.",
        Character_Dir=CHARACTER_DIALOG,
    ),
    Dialog(
        Text="4 - ESCORREGA!!!",
        Character_Dir=CHARACTER_DIALOG,
    ),
    Dialog(
        Text="Se você fizer fora da ordem, dá erro",
        Character_Dir=CHARACTER_DIALOG,
    ),
    Dialog(
        Text="Pronto pra praticar?",
        Character_Dir=CHARACTER_DIALOG,
    ),
    Dialog(
        Text="Primeiro serão mostrados em tela os movimentos a serem realizados",
        Character_Dir=CHARACTER_DIALOG,
    ),
    Dialog(
        Text="Memorize os movimentos e depois repitá-os na ordem que eles apareceram.",
        Character_Dir=CHARACTER_DIALOG,
    ),
    Dialog(
        Text="Vamos lá!",
        Character_Dir=CHARACTER_DIALOG,
    ),
]

DIALOG_CONDITION = [
    Dialog(
        Text=f"Imagine que você está brincando e alguém te pergunta: 'Está chovendo lá fora?'.",
        Character_Dir=CHARACTER_DIALOG,
    ),
    Dialog(
        Text=f"Se estiver chovendo, você responde 'Sim', e fica em casa.",
        Character_Dir=CHARACTER_DIALOG,
    ),
    Dialog(
        Text=f"Se não estiver chovendo, você diz 'Não' e sai para brincar.",
        Character_Dir=CHARACTER_DIALOG,
    ),
    Dialog(
        Text=f"Isso é uma condição! É como uma pergunta que ajuda a escolher o que fazer.",
        Character_Dir=CHARACTER_DIALOG,
    ),
    Dialog(
        Text=f"Agora, imagine que o computador também precisa tomar decisões.",
        Character_Dir=CHARACTER_DIALOG,
    ),
    Dialog(
        Text=f"Ele faz perguntas como: 'O botão foi pressionado?' ou 'O número é maior que 10?'.",
        Character_Dir=CHARACTER_DIALOG,
    ),
    Dialog(
        Text=f"Dependendo da resposta, ele faz uma coisa ou outra.",
        Character_Dir=CHARACTER_DIALOG,
    ),
    Dialog(
        Text="Pronto pra praticar?",
        Character_Dir=CHARACTER_DIALOG,
    ),
    Dialog(
        Text="Nesse jogo os movimentos são representados por cores.",
        Character_Dir=CHARACTER_DIALOG,
    ),
    Dialog(
        Text="Primeiro, será mostrado qual movimento cada cor representa.",
        Character_Dir=CHARACTER_DIALOG,
    ),
    Dialog(
        Text="Depois será mostrado em tela a sequencia de cores.",
        Character_Dir=CHARACTER_DIALOG,
    ),
    Dialog(
        Text="Memorize as cores e depois realize os movimentos que elas representam na ordem correta.",
        Character_Dir=CHARACTER_DIALOG,
    ),
    Dialog(
        Text="Vamos lá!",
        Character_Dir=CHARACTER_DIALOG,
    ),
]

DIALOG_ITERATION = [
    Dialog(
        Text="AQUI VAI O TEXTO DA ITERAÇÃO",
        Character_Dir=CHARACTER_DIALOG,
    ),
]
