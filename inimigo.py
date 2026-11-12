import pygame
from config import LARGURA, SPRITE_ALIEN, SPRITE_BOSS

class Inimigo(pygame.sprite.Sprite):
    def __init__(self, x, y, velocidade):
        super().__init__()
        self.image = SPRITE_ALIEN
        self.rect = self.image.get_rect(topleft=(x, y))
        self.velocidade = velocidade

    def update(self):
        self.rect.x += self.velocidade

class Chefao(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = SPRITE_BOSS
        self.rect = self.image.get_rect(midtop=(LARGURA // 2, 40))
        self.velocidade = 3
        self.hp = 30
        self.max_hp = 30

    def update(self):
        self.rect.x += self.velocidade
        if self.rect.right >= LARGURA - 20 or self.rect.left <= 20:
            self.velocidade *= -1