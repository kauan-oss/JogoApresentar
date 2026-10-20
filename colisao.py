import pygame
import random

PALAVRAS_GOLPE = ["DEBATE!", "FAKE NEWS!", "PROPOSTA!", "VOTO!", "IMPEACHMENT!", "CENSURA!"]

def verificar_ataque_e_colisao(p1, p2):
    """Verifica colisão de socos e chutes entre os lutadores e dispara textos temáticos de impacto"""
    
    for atacante, defensor in [(p1, p2), (p2, p1)]:
        if atacante.atacando and not atacante.ja_causou_dano and atacante.cooldown_ataque > 4:
            is_soco = atacante.tipo_ataque == "soco"
            alcance = int((70 if is_soco else 88) * atacante.escala)
            dano_base = atacante.forca if is_soco else int(atacante.forca * 1.35)

            cx = atacante.rect.centerx
            top_y = atacante.rect.y + int(15 * atacante.escala)
            altura_hitbox = int(65 * atacante.escala)

            if atacante.virado_direita:
                hitbox = pygame.Rect(cx, top_y, alcance, altura_hitbox)
            else:
                hitbox = pygame.Rect(cx - alcance, top_y, alcance, altura_hitbox)

            if hitbox.colliderect(defensor.rect) and abs(atacante.y - defensor.y) < 55:
                defensor.vida = max(0, defensor.vida - dano_base)
                defensor.tempo_hit = 14
                defensor.vx += 13.0 if atacante.virado_direita else -13.0
                atacante.ja_causou_dano = True

                # Dispara palavra temática de impacto no defensor
                defensor.texto_impacto = random.choice(PALAVRAS_GOLPE)
                defensor.tempo_texto_impacto = 25