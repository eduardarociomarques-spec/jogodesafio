import pygame
from config import LARGURA, ALTURA, SPRITE_JOGADOR, SOM_PASSO, tocar_som

class Jogador(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = SPRITE_JOGADOR
        self.x = 50.0
        self.y = float(ALTURA // 2)
        self.rect = self.image.get_rect(center=(int(self.x), int(self.y)))
        self.vidas = 3
        self.movendo = False
        self.passo_som = 0

    def voltar_inicio(self):
        self.x = 50.0
        self.y = float(ALTURA // 2)
        self.rect.center = (int(self.x), int(self.y))

    def update(self, fase):
        teclas = pygame.key.get_pressed()
        self.movendo = False
        velocidade = 2.6 + (fase * 0.2)

        if teclas[pygame.K_RIGHT] or teclas[pygame.K_d]:
            self.x += velocidade
            self.movendo = True
        if teclas[pygame.K_LEFT] or teclas[pygame.K_a]:
            self.x = max(20.0, self.x - velocidade)
            self.movendo = True
        if teclas[pygame.K_UP] or teclas[pygame.K_w]:
            self.y = max(70.0, self.y - velocidade)
            self.movendo = True
        if teclas[pygame.K_DOWN] or teclas[pygame.K_s]:
            self.y = min(float(ALTURA - 50), self.y + velocidade)
            self.movendo = True

        self.rect.center = (int(self.x), int(self.y))

        if self.movendo:
            self.passo_som += 1
            if self.passo_som % 12 == 0:
                tocar_som(SOM_PASSO)