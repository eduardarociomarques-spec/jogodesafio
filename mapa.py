import pygame
from config import (
    LARGURA, ALTURA, AREIA, TERRA_ESCURA,
    VERMELHO, VERDE, AMARELO, BRANCO, PRETO
)

class Mapa:
    def __init__(self):
        self.linha_chegada = LARGURA - 110
        self.fonte = pygame.font.SysFont("Courier", 18, bold=True)
        self.fonte_grande = pygame.font.SysFont("Courier", 34, bold=True)

    def desenhar_pista(self, tela):
        tela.fill(AREIA)
        pygame.draw.rect(tela, TERRA_ESCURA, (0, 60, LARGURA, ALTURA - 95))
        pygame.draw.line(tela, BRANCO, (85, 60), (85, ALTURA - 35), 4)
        pygame.draw.line(tela, VERMELHO, (self.linha_chegada, 60), (self.linha_chegada, ALTURA - 35), 6)

    def desenhar_hud(self, tela, estado_boneca, tempo_restante, pontos, vidas, fase):
        # Semáforo no topo
        if estado_boneca == "VERDE":
            cor = VERDE
            texto = "PODE CORRER!"
        elif estado_boneca == "ALERTA":
            cor = AMARELO
            texto = "ATENCAO..."
        else:
            cor = VERMELHO
            texto = "PARE AGORA!"

        pygame.draw.rect(tela, PRETO, (0, 0, LARGURA, 55))
        pygame.draw.circle(tela, cor, (35, 27), 16)
        txt_status = self.fonte.render(texto, True, cor)
        tela.blit(txt_status, (65, 17))

        txt_tempo = self.fonte.render(f"TEMPO: {tempo_restante:.1f}s", True, BRANCO)
        tela.blit(txt_tempo, (LARGURA - 170, 17))

        # Rodapé
        pygame.draw.rect(tela, PRETO, (0, ALTURA - 35, LARGURA, 35))
        txt_hud = self.fonte.render(f"PONTOS: {pontos}   VIDAS: {vidas}   FASE: {fase}/3", True, AMARELO)
        tela.blit(txt_hud, (15, ALTURA - 27))

    def desenhar_tela_final(self, tela, estado_jogo, pontos):
        overlay = pygame.Surface((LARGURA, ALTURA), pygame.SRCALPHA)
        overlay.fill((15, 15, 30, 210))
        tela.blit(overlay, (0, 0))

        if estado_jogo == "GAME_OVER":
            titulo = self.fonte_grande.render("VOCE FOI PEGO!", True, VERMELHO)
        else:
            titulo = self.fonte_grande.render("VENCEU O DESAFIO!", True, VERDE)

        sub = self.fonte.render(f"Pontuacao Final: {pontos} - Pressione R", True, BRANCO)
        tela.blit(titulo, titulo.get_rect(center=(LARGURA // 2, ALTURA // 2 - 20)))
        tela.blit(sub, sub.get_rect(center=(LARGURA // 2, ALTURA // 2 + 25)))