import pygame
from config import LARGURA, ALTURA, FPS, TITULO, SOM_FALHA, SOM_VITORIA, tocar_som
from mapa import Mapa
from jogador import Jogador
from inimigo import Boneca

def main():
    pygame.init()
    tela = pygame.display.set_mode((LARGURA, ALTURA))
    pygame.display.set_caption(TITULO)
    clock = pygame.time.Clock()
    mapa = Mapa()

    def iniciar_partida():
        jogador = Jogador()
        boneca = Boneca()
        sprites = pygame.sprite.Group(jogador, boneca)
        return jogador, boneca, sprites, 0, 1, 35.0, "JOGANDO"

    jogador, boneca, sprites, pontos, fase, tempo_restante, estado_jogo = iniciar_partida()

    rodando = True
    while rodando:
        dt = clock.tick(FPS) / 1000.0

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False
            if evento.type == pygame.KEYDOWN:
                if estado_jogo in ["GAME_OVER", "VITORIA"] and evento.key == pygame.K_r:
                    jogador, boneca, sprites, pontos, fase, tempo_restante, estado_jogo = iniciar_partida()

        if estado_jogo == "JOGANDO":
            tempo_restante -= dt
            if tempo_restante <= 0:
                tempo_restante = 0
                estado_jogo = "GAME_OVER"

            boneca.update(fase)
            jogador.update(fase)

            # Verifica se o jogador se mexeu no sinal vermelho
            if jogador.movendo and boneca.estado == "VERMELHO":
                tocar_som(SOM_FALHA)
                jogador.vidas -= 1
                jogador.voltar_inicio()
                if jogador.vidas <= 0:
                    estado_jogo = "GAME_OVER"

            # Verifica se cruzou a linha de chegada
            if jogador.x >= mapa.linha_chegada:
                tocar_som(SOM_VITORIA)
                pontos += int(tempo_restante * 20) + (fase * 200)
                if fase < 3:
                    fase += 1
                    jogador.voltar_inicio()
                    boneca.resetar()
                    tempo_restante = max(20.0, 35.0 - (fase * 5))
                else:
                    estado_jogo = "VITORIA"

        # Renderização
        mapa.desenhar_pista(tela)
        boneca.desenhar_radar(tela)
        sprites.draw(tela)
        mapa.desenhar_hud(tela, boneca.estado, tempo_restante, pontos, jogador.vidas, fase)

        if estado_jogo in ["GAME_OVER", "VITORIA"]:
            mapa.desenhar_tela_final(tela, estado_jogo, pontos)

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
