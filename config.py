import pygame
import math
import struct
import random

# Configurações da Tela
LARGURA, ALTURA = 640, 480
FPS = 60
TITULO = "Batatinha Frita 1, 2, 3 - Desafio CCM"

# Cores Retrô
AREIA = (230, 200, 140)
TERRA_ESCURA = (190, 155, 100)
VERMELHO = (235, 50, 70)
VERDE = (50, 210, 90)
AMARELO = (255, 220, 50)
BRANCO = (255, 255, 255)
PRETO = (20, 20, 30)
LARANJA = (255, 130, 40)

# Gerador de Sons 8-bit
def criar_som(frequencia, duracao, tipo="quadrada"):
    try:
        if not pygame.mixer.get_init():
            pygame.mixer.init(frequency=22050, size=-16, channels=1)
        sample_rate = 22050
        n_samples = int(sample_rate * duracao)
        buffer = bytearray()

        for i in range(n_samples):
            t = i / sample_rate
            if tipo == "quadrada":
                valor = 1.0 if math.sin(2 * math.pi * frequencia * t) >= 0 else -1.0
            else:
                valor = random.uniform(-1.0, 1.0)

            envelope = 1.0 - (i / n_samples)
            amostra = int(valor * envelope * 32767 * 0.2)
            buffer.extend(struct.pack("<h", amostra))

        return pygame.mixer.Sound(buffer=bytes(buffer))
    except Exception:
        return None

def tocar_som(som):
    if som:
        try:
            som.play()
        except Exception:
            pass

SOM_PASSO = criar_som(300, 0.05, "quadrada")
SOM_ALERTA = criar_som(750, 0.25, "quadrada")
SOM_FALHA = criar_som(140, 0.35, "ruido")
SOM_VITORIA = criar_som(520, 0.4, "quadrada")

# Gerador de Pixel Art
def criar_sprite(matriz, cores, escala=4):
    altura = len(matriz) * escala
    largura = len(matriz[0]) * escala
    superficie = pygame.Surface((largura, altura), pygame.SRCALPHA)
    for y, linha in enumerate(matriz):
        for x, pixel in enumerate(linha):
            if pixel in cores:
                pygame.draw.rect(
                    superficie,
                    cores[pixel],
                    (x * escala, y * escala, escala, escala)
                )
    return superficie

MATRIZ_JOGADOR = [
    "  1111  ",
    "  1221  ",
    "  1111  ",
    " 333333 ",
    "3 3333 3",
    "  3333  ",
    "  4  4  ",
    "  4  4  "
]

MATRIZ_BONECA_COSTAS = [
    "  111111  ",
    " 11111111 ",
    " 11111111 ",
    "  111111  ",
    " 22222222 ",
    "2222222222",
    " 33333333 ",
    " 33333333 ",
    "  44  44  "
]

MATRIZ_BONECA_FRENTE = [
    "  111111  ",
    " 12222221 ",
    " 12522521 ",
    "  226622  ",
    " 22222222 ",
    "2233333322",
    " 33333333 ",
    " 33333333 ",
    "  44  44  "
]

CORES_JOGADOR = {"1": (130, 80, 40), "2": (255, 210, 170), "3": VERDE, "4": BRANCO}
CORES_BONECA = {
    "1": (40, 30, 30),
    "2": (255, 215, 180),
    "3": LARANJA,
    "4": BRANCO,
    "5": VERMELHO,
    "6": VERMELHO
}

SPRITE_JOGADOR = criar_sprite(MATRIZ_JOGADOR, CORES_JOGADOR, 4)
SPRITE_BONECA_COSTAS = criar_sprite(MATRIZ_BONECA_COSTAS, CORES_BONECA, 5)
SPRITE_BONECA_FRENTE = criar_sprite(MATRIZ_BONECA_FRENTE, CORES_BONECA, 5)
