import pygame

def desenhar_painel_controles(tela, largura, altura, fonte_p):
    y_ctrl = altura - 110
    pygame.draw.rect(tela, (20, 25, 40, 200), (40, y_ctrl, largura - 80, 95), border_radius=10)
    pygame.draw.rect(tela, (255, 215, 0), (40, y_ctrl, largura - 80, 95), width=2, border_radius=10)
    
    t_p1 = fonte_p.render("P1: W,A,S,D (Mover 3D) | F (Soco) | G (Chute)", True, (255, 255, 255))
    t_p2 = fonte_p.render("P2: Setas (Mover 3D) | K ou Ç (Soco) | L (Chute)", True, (255, 255, 255))
    t_fs = fonte_p.render("F11: Tela Cheia | R: Sortear/Resetar Vitórias | ENTER: Iniciar", True, (255, 215, 0))
    
    tela.blit(t_p1, (largura // 2 - t_p1.get_width() // 2, y_ctrl + 12))
    tela.blit(t_p2, (largura // 2 - t_p2.get_width() // 2, y_ctrl + 38))
    tela.blit(t_fs, (largura // 2 - t_fs.get_width() // 2, y_ctrl + 64))