import pygame
import random
from config import LARGURA, ALTURA, FPS, TITULO, VERMELHO, SOM_EXPLOSAO, SOM_DANO, Tiro
from mapa import Mapa
from jogador import Jogador

def main():
    tela = pygame.display.set_mode((LARGURA, ALTURA))
    pygame.display.set_caption(TITULO)
    clock = pygame.time.Clock()
    mapa = Mapa()

    def iniciar_partida():
        jogador = Jogador()
        grupo_jogador = pygame.sprite.GroupSingle(jogador)
        inimigos = pygame.sprite.Group()
        tiros_jogador = pygame.sprite.Group()
        tiros_inimigos = pygame.sprite.Group()
        grupo_boss = pygame.sprite.GroupSingle()
        mapa.carregar_fase(1, inimigos, grupo_boss)
        return jogador, grupo_jogador, inimigos, tiros_jogador, tiros_inimigos, grupo_boss, 0, 1, "JOGANDO"

    jogador, grupo_jogador, inimigos, tiros_jogador, tiros_inimigos, grupo_boss, pontos, fase, estado = iniciar_partida()

    rodando = True
    while rodando:
        clock.tick(FPS)
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False
            if evento.type == pygame.KEYDOWN:
                if estado == "JOGANDO" and evento.key == pygame.K_SPACE:
                    tiro = jogador.atirar()
                    if tiro:
                        tiros_jogador.add(tiro)
                elif estado in ["GAME_OVER", "VITORIA"] and evento.key == pygame.K_r:
                    jogador, grupo_jogador, inimigos, tiros_jogador, tiros_inimigos, grupo_boss, pontos, fase, estado = iniciar_partida()

        mapa.atualizar_fundo()

        if estado == "JOGANDO":
            grupo_jogador.update()
            tiros_jogador.update()
            tiros_inimigos.update()
            inimigos.update()
            grupo_boss.update()

            # Movimento em bloco dos inimigos
            inverter = False
            for inimigo in inimigos:
                if inimigo.rect.right >= LARGURA - 10 or inimigo.rect.left <= 10:
                    inverter = True
                if inimigo.rect.bottom >= ALTURA - 35:
                    estado = "GAME_OVER"
                if random.random() < 0.002 * fase:
                    tiros_inimigos.add(Tiro(inimigo.rect.centerx, inimigo.rect.bottom, 5, VERMELHO))

            if inverter:
                for inimigo in inimigos:
                    inimigo.velocidade *= -1
                    inimigo.rect.y += 15

            # Ataque do Chefão
            if grupo_boss.sprite and random.random() < 0.04:
                boss = grupo_boss.sprite
                tiros_inimigos.add(Tiro(boss.rect.centerx - 20, boss.rect.bottom, 6, VERMELHO))
                tiros_inimigos.add(Tiro(boss.rect.centerx + 20, boss.rect.bottom, 6, VERMELHO))

            # Colisões: Tiros do jogador nos inimigos
            acertos = pygame.sprite.groupcollide(inimigos, tiros_jogador, True, True)
            if acertos:
                SOM_EXPLOSAO.play()
                pontos += len(acertos) * 100

            # Colisões: Tiros do jogador no Chefão
            if grupo_boss.sprite:
                hits_boss = pygame.sprite.spritecollide(grupo_boss.sprite, tiros_jogador, True)
                for _ in hits_boss:
                    SOM_EXPLOSAO.play()
                    grupo_boss.sprite.hp -= 1
                    pontos += 50
                    if grupo_boss.sprite.hp <= 0:
                        grupo_boss.empty()
                        pontos += 1000
                        estado = "VITORIA"

            # Dano no jogador
            if jogador.invencivel == 0:
                atingido_tiro = pygame.sprite.spritecollide(jogador, tiros_inimigos, True)
                atingido_nave = pygame.sprite.spritecollide(jogador, inimigos, True)
                if atingido_tiro or atingido_nave:
                    SOM_DANO.play()
                    jogador.vidas -= 1
                    jogador.invencivel = 60
                    if jogador.vidas <= 0:
                        estado = "GAME_OVER"

            # Avançar de fase
            if estado == "JOGANDO" and len(inimigos) == 0 and not grupo_boss.sprite and fase < 3:
                fase += 1
                tiros_inimigos.empty()
                mapa.carregar_fase(fase, inimigos, grupo_boss)

        # Renderização
        mapa.desenhar_fundo(tela)

        if jogador.invencivel == 0 or (jogador.invencivel // 5) % 2 == 0:
            grupo_jogador.draw(tela)

        inimigos.draw(tela)
        grupo_boss.draw(tela)
        tiros_jogador.draw(tela)
        tiros_inimigos.draw(tela)

        mapa.desenhar_hud(tela, pontos, jogador.vidas, fase, grupo_boss.sprite)

        if estado in ["GAME_OVER", "VITORIA"]:
            mapa.desenhar_tela_final(tela, estado, pontos)

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()