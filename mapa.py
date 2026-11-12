import pygame
import random
from config import LARGURA, ALTURA, PRETO, BRANCO, AMARELO, VERMELHO, VERDE_ALIEN
from inimigo import Inimigo, Chefao

class Mapa:
    def __init__(self):
        self.estrelas = [
            [random.randint(0, LARGURA), random.randint(0, ALTURA), random.choice([1, 2])]
            for _ in range(60)
        ]
        self.fonte = pygame.font.SysFont("Courier", 20, bold=True)
        self.fonte_grande = pygame.font.SysFont("Courier", 36, bold=True)

    def atualizar_fundo(self):
        for estrela in self.estrelas:
            estrela[1] += estrela[2]
            if estrela[1] > ALTURA:
                estrela[1] = 0
                estrela[0] = random.randint(0, LARGURA)

    def desenhar_fundo(self, tela):
        tela.fill(PRETO)
        for sx, sy, tam in self.estrelas:
            pygame.draw.circle(tela, BRANCO, (sx, sy), tam)

    def carregar_fase(self, num_fase, grupo_inimigos, grupo_boss):
        grupo_inimigos.empty()
        grupo_boss.empty()
        if num_fase < 3:
            linhas = 2 + num_fase
            colunas = 7
            vel = 1.5 + (num_fase * 0.5)
            for l in range(linhas):
                for c in range(colunas):
                    grupo_inimigos.add(Inimigo(80 + c * 65, 50 + l * 45, vel))
        else:
            grupo_boss.add(Chefao())

    def desenhar_hud(self, tela, pontos, vidas, fase, boss):
        if boss:
            pygame.draw.rect(tela, VERMELHO, (170, 15, 300, 12))
            largura_hp = int(300 * (boss.hp / boss.max_hp))
            pygame.draw.rect(tela, VERDE_ALIEN, (170, 15, largura_hp, 12))

        txt_hud = self.fonte.render(f"PONTOS: {pontos}   VIDAS: {vidas}   FASE: {fase}", True, AMARELO)
        tela.blit(txt_hud, (15, ALTURA - 30))

    def desenhar_tela_final(self, tela, estado, pontos):
        overlay = pygame.Surface((LARGURA, ALTURA), pygame.SRCALPHA)
        overlay.fill((15, 15, 30, 200))
        tela.blit(overlay, (0, 0))

        if estado == "GAME_OVER":
            txt = self.fonte_grande.render("FIM DE JOGO!", True, VERMELHO)
            sub = self.fonte.render("Pressione R para jogar novamente", True, BRANCO)
        else:
            txt = self.fonte_grande.render("MISSAO CUMPRIDA!", True, VERDE_ALIEN)
            sub = self.fonte.render(f"Pontuacao Final: {pontos} (Pressione R)", True, BRANCO)

        tela.blit(txt, txt.get_rect(center=(LARGURA // 2, ALTURA // 2 - 20)))
        tela.blit(sub, sub.get_rect(center=(LARGURA // 2, ALTURA // 2 + 25)))