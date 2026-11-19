import pygame
import random
from config import (
    LARGURA, ALTURA, VERMELHO,
    SPRITE_BONECA_COSTAS, SPRITE_BONECA_FRENTE,
    SOM_ALERTA, tocar_som
)

class Boneca(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = SPRITE_BONECA_COSTAS
        self.rect = self.image.get_rect(center=(LARGURA - 55, ALTURA // 2))
        self.estado = "VERDE"  # VERDE, ALERTA, VERMELHO
        self.timer = 120

    def resetar(self):
        self.estado = "VERDE"
        self.timer = 100
        self.image = SPRITE_BONECA_COSTAS

    def update(self, fase):
        self.timer -= 1
        if self.timer <= 0:
            if self.estado == "VERDE":
                self.estado = "ALERTA"
                self.timer = max(25, 45 - fase * 5)
                tocar_som(SOM_ALERTA)
            elif self.estado == "ALERTA":
                self.estado = "VERMELHO"
                self.timer = random.randint(70, 130)
                self.image = SPRITE_BONECA_FRENTE
            elif self.estado == "VERMELHO":
                self.estado = "VERDE"
                self.timer = max(60, random.randint(90, 160) - fase * 15)
                self.image = SPRITE_BONECA_COSTAS

    def desenhar_radar(self, tela):
        if self.estado == "VERMELHO":
            pygame.draw.polygon(
                tela,
                VERMELHO,
                [(self.rect.left, self.rect.centery), (85, 60), (85, ALTURA - 35)],
                2
            )