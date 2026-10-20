"""Rotinas de alcance, dano e recuo para o combate 3D."""
def resolver_ataque(atacante, defensor, tipo):
    """Aplica um golpe se o adversário estiver à frente e dentro do alcance."""
    alcance = 1.65 if tipo == "soco" else 2.0
    frente = (defensor.x - atacante.x) * atacante.direcao > 0
    perto = abs(defensor.x-atacante.x) < alcance and abs(defensor.z-atacante.z) < 1.15
    if not (frente and perto):
        return False

    dano = atacante.forca if tipo == "soco" else int(atacante.forca * 1.35)
    defensor.vida = max(0, defensor.vida-dano)
    defensor.tempo_hit = 0.18
    defensor.x += 0.35 * atacante.direcao
    return True

def verificar_ataque_e_colisao(p1, p2):
    """Compatibilidade com o nome da função usada no jogo anterior."""
    return False
