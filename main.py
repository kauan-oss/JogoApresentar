import pygame
import sys
import math
from personagem import PERSONAGENS_BASE, ACESSORIOS, Lutador, gerar_candidato_aleatorio
from colisao import verificar_ataque_e_colisao
from menu import desenhar_painel_controles

pygame.init()

LARGURA, ALTURA = 1000, 600
tela = pygame.display.set_mode((LARGURA, ALTURA), pygame.RESIZABLE)
pygame.display.set_caption("Eleições Fighting Game 3D")
relogio = pygame.time.Clock()

e_tela_cheia = False

def alternar_tela_cheia():
    global tela, e_tela_cheia
    e_tela_cheia = not e_tela_cheia
    if e_tela_cheia:
        tela = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    else:
        tela = pygame.display.set_mode((LARGURA, ALTURA), pygame.RESIZABLE)

CONTROLES_P1 = {
    'esquerda': pygame.K_a,
    'direita': pygame.K_d,
    'cima': pygame.K_w,
    'baixo': pygame.K_s,
    'soco': pygame.K_f,
    'chute': pygame.K_g
}

CONTROLES_P2 = {
    'esquerda': pygame.K_LEFT,
    'direita': pygame.K_RIGHT,
    'cima': pygame.K_UP,
    'baixo': pygame.K_DOWN,
    'soco': [pygame.K_k, pygame.K_j, pygame.K_SEMICOLON, pygame.K_c, pygame.K_KP1, pygame.K_u, pygame.K_i],
    'chute': [pygame.K_l, pygame.K_o, pygame.K_KP2]
}

vitorias_p1 = 0
vitorias_p2 = 0

def desenhar_cenario_dinamico(tela, larg_atual, alt_atual, y_min):
    for y in range(y_min):
        fator = y / y_min
        r = int(30 + (220 - 30) * fator)
        g = int(50 + (120 - 50) * fator)
        b = int(120 + (50 - 120) * fator)
        pygame.draw.line(tela, (r, g, b), (0, y), (larg_atual, y))

    sol_x, sol_y = larg_atual // 2, y_min - 15
    pygame.draw.circle(tela, (255, 220, 100), (sol_x, sol_y), 65)
    pygame.draw.circle(tela, (255, 240, 180), (sol_x, sol_y), 45)

    pygame.draw.rect(tela, (70, 75, 85), (0, y_min, larg_atual, alt_atual - y_min))

    num_linhas_p = 12
    cx_foco = larg_atual // 2
    for i in range(num_linhas_p + 1):
        x_base = (larg_atual / num_linhas_p) * i
        pygame.draw.line(tela, (90, 95, 105), (cx_foco, y_min), (x_base, alt_atual), 2)

    num_linhas_h = 8
    for i in range(1, num_linhas_h + 1):
        fator_h = (i / num_linhas_h) ** 2
        hy = int(y_min + (alt_atual - y_min) * fator_h)
        pygame.draw.line(tela, (110, 115, 130), (0, hy), (larg_atual, hy), 2)

    pygame.draw.line(tela, (255, 215, 0), (0, y_min), (larg_atual, y_min), 4)

def tela_vitoria(nome_vencedor):
    fonte_g = pygame.font.SysFont('Arial', 36, bold=True)
    fonte_m = pygame.font.SysFont('Arial', 22, bold=True)
    
    rodando = True
    while rodando:
        relogio.tick(60)
        larg_atual, alt_atual = tela.get_size()
        tela.fill((15, 20, 35))

        txt_tit = fonte_g.render("ELEIÇÕES ENCERRADAS!", True, (255, 215, 0))
        txt_venc = fonte_g.render(f"NOVO PRESIDENTE: {nome_vencedor.upper()}!", True, (50, 220, 100))
        txt_sub = fonte_m.render("Pressione ENTER para Voltar ao Menu Principal", True, (200, 200, 200))

        tela.blit(txt_tit, (larg_atual // 2 - txt_tit.get_width() // 2, alt_atual // 3 - 30))
        tela.blit(txt_venc, (larg_atual // 2 - txt_venc.get_width() // 2, alt_atual // 3 + 40))
        tela.blit(txt_sub, (larg_atual // 2 - txt_sub.get_width() // 2, alt_atual // 3 + 130))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_RETURN, pygame.K_SPACE, pygame.K_ESCAPE]:
                    rodando = False
                elif event.key == pygame.K_F11:
                    alternar_tela_cheia()

        pygame.display.flip()

def menu_selecao():
    global vitorias_p1, vitorias_p2, PERSONAGENS_BASE
    
    idx_p1, idx_p2 = 0, 1
    acess_p1, acess_p2 = 0, 0
    tempo_idle_menu = 0.0
    
    fonte = pygame.font.SysFont('Arial', 24, bold=True)
    fonte_p = pygame.font.SysFont('Arial', 16, bold=True)
    
    rodando = True
    while rodando:
        relogio.tick(60)
        tempo_idle_menu += 0.05
        larg_atual, alt_atual = tela.get_size()
        tela.fill((25, 30, 45))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F11:
                    alternar_tela_cheia()
                elif event.key == pygame.K_r:
                    PERSONAGENS_BASE = [gerar_candidato_aleatorio(i) for i in range(6)]
                    vitorias_p1, vitorias_p2 = 0, 0
                    idx_p1, idx_p2 = 0, 1
                elif event.key == pygame.K_a:
                    idx_p1 = (idx_p1 - 1) % len(PERSONAGENS_BASE)
                elif event.key == pygame.K_d:
                    idx_p1 = (idx_p1 + 1) % len(PERSONAGENS_BASE)
                elif event.key == pygame.K_w:
                    acess_p1 = (acess_p1 - 1) % len(ACESSORIOS)
                elif event.key == pygame.K_s:
                    acess_p1 = (acess_p1 + 1) % len(ACESSORIOS)
                elif event.key == pygame.K_LEFT:
                    idx_p2 = (idx_p2 - 1) % len(PERSONAGENS_BASE)
                elif event.key == pygame.K_RIGHT:
                    idx_p2 = (idx_p2 + 1) % len(PERSONAGENS_BASE)
                elif event.key == pygame.K_UP:
                    acess_p2 = (acess_p2 - 1) % len(ACESSORIOS)
                elif event.key == pygame.K_DOWN:
                    acess_p2 = (acess_p2 + 1) % len(ACESSORIOS)
                elif event.key == pygame.K_RETURN:
                    rodando = False

        txt_titulo = fonte.render("SELEÇÃO DE CANDIDATOS (MD3)", True, (255, 215, 0))
        tela.blit(txt_titulo, (larg_atual // 2 - txt_titulo.get_width() // 2, 20))

        txt_p1 = fonte.render(f"P1: {PERSONAGENS_BASE[idx_p1]['nome']} (Pontos: {vitorias_p1})", True, (100, 200, 255))
        txt_acess_p1 = fonte_p.render(f"Acessório: {ACESSORIOS[acess_p1]['nome']}", True, (200, 220, 255))
        tela.blit(txt_p1, (80, 70))
        tela.blit(txt_acess_p1, (80, 100))

        txt_p2 = fonte.render(f"P2: {PERSONAGENS_BASE[idx_p2]['nome']} (Pontos: {vitorias_p2})", True, (255, 100, 100))
        txt_acess_p2 = fonte_p.render(f"Acessório: {ACESSORIOS[acess_p2]['nome']}", True, (255, 200, 200))
        tela.blit(txt_p2, (larg_atual - 380, 70))
        tela.blit(txt_acess_p2, (larg_atual - 380, 100))

        pos_y_preview = int(alt_atual * 0.40)
        p1_preview = Lutador(int(larg_atual * 0.22), pos_y_preview, {}, PERSONAGENS_BASE[idx_p1], ACESSORIOS[acess_p1], virado_direita=True)
        p2_preview = Lutador(int(larg_atual * 0.70), pos_y_preview, {}, PERSONAGENS_BASE[idx_p2], ACESSORIOS[acess_p2], virado_direita=False)

        p1_preview.tempo_idle = tempo_idle_menu
        p2_preview.tempo_idle = tempo_idle_menu

        p1_preview.escala = 1.6
        p2_preview.escala = 1.6
        p1_preview.rect.width = int(p1_preview.largura_base * 1.6)
        p1_preview.rect.height = int(p1_preview.altura_base * 1.6)
        p2_preview.rect.width = int(p2_preview.largura_base * 1.6)
        p2_preview.rect.height = int(p2_preview.altura_base * 1.6)

        p1_preview.desenhar(tela)
        p2_preview.desenhar(tela)

        desenhar_painel_controles(tela, larg_atual, alt_atual, fonte_p)
        pygame.display.flip()

    return idx_p1, idx_p2, acess_p1, acess_p2

def loop_jogo(idx_p1, idx_p2, acess_p1, acess_p2):
    global vitorias_p1, vitorias_p2
    vitorias_p1 = 0
    vitorias_p2 = 0
    
    fonte = pygame.font.SysFont('Arial', 22, bold=True)
    fonte_round = pygame.font.SysFont('Arial', 30, bold=True)
    
    # Loop principal da MD3: Permanece no combate até que alguém alcance 2 vitórias
    while vitorias_p1 < 2 and vitorias_p2 < 2:
        p1 = Lutador(200, 380, CONTROLES_P1, PERSONAGENS_BASE[idx_p1], ACESSORIOS[acess_p1], virado_direita=True)
        p2 = Lutador(700, 380, CONTROLES_P2, PERSONAGENS_BASE[idx_p2], ACESSORIOS[acess_p2], virado_direita=False)
        
        round_ativo = True
        while round_ativo:
            relogio.tick(60)
            larg_atual, alt_atual = tela.get_size()
            y_min, y_max = int(alt_atual * 0.52), int(alt_atual * 0.88)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_F11:
                        alternar_tela_cheia()

            p1.mover(y_min, y_max)
            p2.mover(y_min, y_max)
            verificar_ataque_e_colisao(p1, p2)

            if p1.vida <= 0:
                vitorias_p2 += 1
                round_ativo = False
            elif p2.vida <= 0:
                vitorias_p1 += 1
                round_ativo = False

            desenhar_cenario_dinamico(tela, larg_atual, alt_atual, y_min)
            
            lutadores = sorted([p1, p2], key=lambda lutador: lutador.y)
            for l in lutadores:
                l.desenhar(tela)

            # Barra de Vida HUD
            pygame.draw.rect(tela, (200, 30, 30), (30, 20, 300, 22))
            pygame.draw.rect(tela, (30, 200, 30), (30, 20, max(0, int(300 * (p1.vida / 100))), 22))
            
            pygame.draw.rect(tela, (200, 30, 30), (larg_atual - 330, 20, 300, 22))
            pygame.draw.rect(tela, (30, 200, 30), (larg_atual - 330, 20, max(0, int(300 * (p2.vida / 100))), 22))

            txt_p1 = fonte.render(f"{p1.nome} ({p1.vida} HP) | VITORIAS: {vitorias_p1}", True, (255, 255, 255))
            txt_p2 = fonte.render(f"{p2.nome} ({p2.vida} HP) | VITORIAS: {vitorias_p2}", True, (255, 255, 255))
            tela.blit(txt_p1, (30, 48))
            tela.blit(txt_p2, (larg_atual - 330, 48))

            pygame.display.flip()

        # Transição visual entre rounds sem ir para o menu
        if vitorias_p1 < 2 and vitorias_p2 < 2:
            tempo_espera = 90  # 1.5 segundos a 60 FPS
            while tempo_espera > 0:
                relogio.tick(60)
                larg_atual, alt_atual = tela.get_size()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()

                desenhar_cenario_dinamico(tela, larg_atual, alt_atual, int(alt_atual * 0.52))
                txt_round = fonte_round.render("FIM DO ROUND! PREPARE-SE...", True, (255, 215, 0))
                tela.blit(txt_round, (larg_atual // 2 - txt_round.get_width() // 2, alt_atual // 2 - 20))
                pygame.display.flip()
                tempo_espera -= 1

    # Encerramento do confronto MD3 (2 Pontos Alcançados)
    if vitorias_p1 >= 2:
        tela_vitoria(PERSONAGENS_BASE[idx_p1]['nome'])
    elif vitorias_p2 >= 2:
        tela_vitoria(PERSONAGENS_BASE[idx_p2]['nome'])

    vitorias_p1, vitorias_p2 = 0, 0

def main():
    while True:
        p1_idx, p2_idx, a1, a2 = menu_selecao()
        loop_jogo(p1_idx, p2_idx, a1, a2)

if __name__ == "__main__":
    main()
