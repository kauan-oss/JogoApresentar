"""Regras de combate 3D: alcance, orientacao, golpes e separacao fisica."""
from __future__ import annotations

import math
import random

PALAVRAS_GOLPE = ("DEBATE!", "PROPOSTA!", "VOTO!", "ARGUMENTO!", "DISCURSO!")


def separar_lutadores(p1, p2):
    dx, dz = p2.x - p1.x, p2.z - p1.z
    distancia = math.hypot(dx, dz)
    minimo = .79
    if distancia >= minimo:
        return
    if distancia < .001:
        dx, dz, distancia = .001 if p1.lado == 1 else -.001, 0.0, .001
    fator = (minimo - distancia) / (2 * distancia)
    p1.root.x = max(-7.35, min(7.35, p1.x - dx * fator))
    p1.root.z = max(-3.25, min(3.25, p1.z - dz * fator))
    p2.root.x = max(-7.35, min(7.35, p2.x + dx * fator))
    p2.root.z = max(-3.25, min(3.25, p2.z + dz * fator))


def pode_acertar(atacante, defensor):
    if not atacante.ataque or atacante.ja_atingiu or defensor.vida <= 0:
        return False
    t = atacante.ataque_tempo
    inicio, fim = ((.12, .35) if atacante.ataque == "soco" else (.17, .45))
    if not inicio <= t <= fim:
        return False
    dx, dz = defensor.x - atacante.x, defensor.z - atacante.z
    alcance = 1.55 if atacante.ataque == "soco" else 1.88
    return (math.hypot(dx, dz) <= alcance
            and dx * atacante.direcao > .02
            and abs(dz) <= 1.00)


def verificar_ataque_e_colisao(p1, p2):
    """Retorna (atacante, defensor, dano, palavra) somente para impactos reais."""
    separar_lutadores(p1, p2)
    eventos = []
    for atacante, defensor in ((p1, p2), (p2, p1)):
        if pode_acertar(atacante, defensor):
            dano = atacante.forca if atacante.ataque == "soco" else int(atacante.forca * 1.35)
            atacante.ja_atingiu = True
            defensor.receber_golpe(dano, atacante.direcao)
            eventos.append((atacante, defensor, dano, random.choice(PALAVRAS_GOLPE)))
    return eventos
