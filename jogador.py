import pygame
from config import LARGURA, ALTURA, AMARELO, SPRITE_NAVE, SOM_TIRO, tocar_som, Tiro

class Jogador(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = SPRITE_NAVE
        self.rect = self.image.get_rect(midbottom=(LARGURA // 2, ALTURA - 20))
        self.velocidade = 5
        self.vidas = 3
        self.cooldown = 0
        self.invencivel = 0

    def update(self):
        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_LEFT] or teclas[pygame.K_a]:
            self.rect.x -= self.velocidade
        if teclas[pygame.K_RIGHT] or teclas[pygame.K_d]:
            self.rect.x += self.velocidade

        self.rect.clamp_ip(pygame.Rect(0, 0, LARGURA, ALTURA))

        if self.cooldown > 0:
            self.cooldown -= 1
        if self.invencivel > 0:
            self.invencivel -= 1

    def atirar(self):
        if self.cooldown == 0:
            tocar_som(SOM_TIRO)
            self.cooldown = 18
            return Tiro(self.rect.centerx, self.rect.top, -8, AMARELO)
        return None