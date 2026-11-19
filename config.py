import pygame
import math
import struct
import random

# Configurações da Tela
LARGURA, ALTURA = 640, 480
FPS = 60
TITULO = "Desafio CCM Elias Abrahão - Batalha Espacial"

# Cores Retrô
PRETO = (15, 15, 30)
BRANCO = (255, 255, 255)
AMARELO = (255, 220, 50)
AZUL_NAVE = (50, 180, 255)
VERMELHO = (255, 60, 80)
VERDE_ALIEN = (60, 230, 100)
ROXO_BOSS = (180, 50, 230)

# Gerador de Sons 8-bit (100% nativo, sem precisar de numpy)
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

SOM_TIRO = criar_som(600, 0.1, "quadrada")
SOM_EXPLOSAO = criar_som(120, 0.25, "ruido")
SOM_DANO = criar_som(150, 0.3, "quadrada")

# Gerador de Pixel Art por Matriz
def criar_sprite(matriz, cores, escala=3):
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

MATRIZ_NAVE = [
    "     1     ",
    "    111    ",
    "    121    ",
    "  1 111 1  ",
    "  1111111  ",
    " 113111311 ",
    "11111111111",
    "1 11   11 1"
]

MATRIZ_ALIEN = [
    "  1     1  ",
    "   1   1   ",
    "  1111111  ",
    " 112111211 ",
    "11111111111",
    "1 1111111 1",
    "1 1     1 1",
    "   11 11   "
]

MATRIZ_BOSS = [
    "    11111111    ",
    "  111111111111  ",
    " 11221111112211 ",
    "1112211111122111",
    "1111111331111111",
    " 11111111111111 ",
    "  11 11  11 11  ",
    " 11  11  11  11 "
]

SPRITE_NAVE = criar_sprite(MATRIZ_NAVE, {"1": AZUL_NAVE, "2": BRANCO, "3": VERMELHO}, 4)
SPRITE_ALIEN = criar_sprite(MATRIZ_ALIEN, {"1": VERDE_ALIEN, "2": PRETO}, 3)
SPRITE_BOSS = criar_sprite(MATRIZ_BOSS, {"1": ROXO_BOSS, "2": AMARELO, "3": VERMELHO}, 5)

# Classe de Projétil
class Tiro(pygame.sprite.Sprite):
    def __init__(self, x, y, vel_y, cor):
        super().__init__()
        self.image = pygame.Surface((4, 12))
        self.image.fill(cor)
        self.rect = self.image.get_rect(center=(x, y))
        self.vel_y = vel_y

    def update(self):
        self.rect.y += self.vel_y
        if self.rect.bottom < 0 or self.rect.top > ALTURA:
            self.kill()