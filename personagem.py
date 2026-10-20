"""Elenco e modelos 3D procedurais. Nenhum sprite ou Pygame e necessario."""
from __future__ import annotations

import math
import random
from ursina import Entity, Vec3, Cylinder, color, destroy
from ursina.shaders import basic_lighting_shader

ACESSORIOS = ["Nenhum", "Óculos Escuros", "Faixa Presidencial", "Gravata Borboleta", "Chapéu Político"]

TONS_PELE = [(240, 194, 142), (255, 220, 177), (198, 134, 66), (140, 85, 39)]
CORES_TERNO = [(25, 25, 30), (15, 40, 110), (240, 210, 30), (30, 45, 80), (20, 35, 90), (25, 35, 65)]
CORES_CABELO = [(30, 25, 20), (235, 235, 235), (200, 200, 200), (160, 160, 165)]


def gerar_candidatos_padrao():
    return [
        dict(nome="Renan Santos", cor_terno=(32, 35, 44), cor_camiseta=(24, 29, 36),
             cor_calca=(78, 112, 157), cor_pele=TONS_PELE[0], cor_cabelo=(33, 25, 21),
             estilo_cabelo="despojado", velocidade=7.7, forca=14, barba=True, oculos=True),
        dict(nome="Lula", cor_terno=(24, 65, 133), cor_camiseta=(238, 240, 237),
             cor_calca=(24, 56, 112), cor_pele=TONS_PELE[0], cor_cabelo=(226, 225, 220),
             estilo_cabelo="grisalho", velocidade=6.8, forca=13, barba=True),
        dict(nome="Flávio", cor_terno=(214, 186, 51), cor_camiseta=(250, 232, 144),
             cor_calca=(80, 117, 172), cor_pele=TONS_PELE[0], cor_cabelo=(54, 40, 32),
             estilo_cabelo="social", velocidade=7.3, forca=12),
        dict(nome="Augusto Cury", cor_terno=(39, 56, 92), cor_camiseta=(190, 215, 236),
             cor_calca=(55, 62, 73), cor_pele=TONS_PELE[0], cor_cabelo=(65, 55, 49),
             estilo_cabelo="social", velocidade=6.4, forca=11, oculos=True),
        dict(nome="Caiado", cor_terno=(28, 49, 108), cor_camiseta=(239, 242, 242),
             cor_calca=(30, 49, 97), cor_pele=TONS_PELE[0], cor_cabelo=(215, 214, 205),
             estilo_cabelo="grisalho", velocidade=7.0, forca=14),
        dict(nome="Zema", cor_terno=(36, 48, 77), cor_camiseta=(71, 91, 119),
             cor_calca=(43, 51, 67), cor_pele=TONS_PELE[0], cor_cabelo=(164, 160, 156),
             estilo_cabelo="curto", velocidade=7.7, forca=10, oculos=True),
    ]


def gerar_candidato_aleatorio(indice=0):
    primeiros = ["Senador", "Ministro", "Governador", "Deputado", "Prefeito", "Embaixador"]
    ultimos = ["Silva", "Santos", "Oliveira", "Souza", "Pereira", "Lima"]
    return dict(
        nome=f"{primeiros[indice % len(primeiros)]} {random.choice(ultimos)}",
        cor_terno=random.choice(CORES_TERNO), cor_camiseta=(237, 238, 242),
        cor_calca=random.choice(CORES_TERNO), cor_pele=random.choice(TONS_PELE),
        cor_cabelo=random.choice(CORES_CABELO),
        estilo_cabelo=random.choice(["social", "grisalho", "topete", "calvo", "curto", "despojado"]),
        velocidade=round(random.uniform(6.3, 8.1), 1), forca=random.randint(10, 15),
        barba=random.choice([True, False]), oculos=False,
    )


def rgb(valor):
    return color.rgb32(*valor)


def esfera(pai, pos, escala, cor, **kwargs):
    """Volumes elipsoidais com silhuetas suaves, em vez de blocos."""
    return Entity(parent=pai, model="sphere", position=pos, scale=escala,
                  color=cor, shader=basic_lighting_shader, **kwargs)


class Lutador3D:
    DURACAO = {"soco": 0.42, "chute": 0.57}
    RECARGA = {"soco": 0.55, "chute": 0.74}

    def __init__(self, dados, acessorio, x, z=0, lado=1):
        self.dados = dados
        self.nome = dados["nome"]
        self.acessorio = acessorio
        self.lado = lado
        self.vida = 100
        self.forca = dados["forca"]
        self.velocidade = dados["velocidade"] * 0.56
        self.direcao = 1 if lado == 1 else -1
        self.root = Entity(position=(x, 0, z), rotation_y=90 * self.direcao)
        self.cor_roupa = rgb(dados["cor_terno"])
        self.cor_calca = rgb(dados["cor_calca"])
        self.cor_pele = rgb(dados["cor_pele"])
        self.cor_cabelo = rgb(dados["cor_cabelo"])

        self.esqueleto = Entity(parent=self.root)
        self.bracos = []
        self.pernas = []
        self.corpo = None
        self._montar_modelo()

        self.vx = 0.0
        self.vz = 0.0
        self.andando = False
        self.tempo = random.uniform(0, 6)
        self.ataque = None
        self.ataque_tempo = 0.0
        self.ataque_total = 0.0
        self.recarga = 0.0
        self.ja_atingiu = False
        self.hit_tempo = 0.0
        self.impacto_recuo = 0.0

    def _montar_modelo(self):
        p = self.esqueleto
        roupa = self.cor_roupa
        pele = self.cor_pele
        calca = self.cor_calca

        # Quadril, paleto e ombros: todos os contornos sao arredondados.
        esfera(p, (0, 1.03, 0), (.75, .43, .48), roupa)
        self.corpo = esfera(p, (0, 1.69, 0), (.91, 1.23, .58), roupa)
        esfera(p, (0, 1.68, .278), (.35, .86, .115), rgb(self.dados["cor_camiseta"]))
        esfera(p, (0, 2.23, 0), (.26, .26, .25), pele)
        # Gola, lapelas e gravata em volumes ovais/triangulares.
        for sx in (-1, 1):
            esfera(p, (.17 * sx, 1.93, .306), (.20, .52, .09),
                   rgb((204, 209, 215)) if sx == -1 else roupa,
                   rotation_z=22 * sx)
        esfera(p, (0, 1.83, .388), (.105, .38, .05), color.rgb32(170, 35, 54))
        esfera(p, (0, 2.02, .395), (.13, .13, .075), color.rgb32(192, 43, 59))

        for sx in (-1, 1):
            braco = Entity(parent=p, position=(.50 * sx, 2.03, 0))
            esfera(braco, (0, -.25, 0), (.35, .62, .36), roupa)
            esfera(braco, (0, -.55, 0), (.29, .32, .32), roupa)
            esfera(braco, (0, -.78, .04), (.26, .45, .28), roupa)
            esfera(braco, (0, -1.04, .10), (.26, .25, .28), pele)
            braco.rotation_z = 8 * sx
            self.bracos.append(braco)

            perna = Entity(parent=p, position=(.21 * sx, 1.00, 0))
            esfera(perna, (0, -.23, 0), (.34, .64, .37), calca)
            esfera(perna, (0, -.54, .0), (.31, .37, .34), calca)
            esfera(perna, (0, -.76, .015), (.28, .48, .31), calca)
            esfera(perna, (0, -.95, .15), (.34, .22, .53), color.rgb32(24, 25, 34))
            self.pernas.append(perna)

        # Rosto tridimensional com nariz, orelhas, olhos e cabelo individualizado.
        cabeca = Entity(parent=p, position=(0, 2.66, .015))
        esfera(cabeca, (0, 0, 0), (.71, .81, .65), pele)
        esfera(cabeca, (0, -.23, .125), (.56, .34, .47), pele)
        for sx in (-1, 1):
            esfera(cabeca, (.352 * sx, -.015, .0), (.20, .29, .19), pele)
            esfera(cabeca, (.151 * sx, .035, .291), (.17, .16, .07), color.rgb32(248, 247, 241))
            esfera(cabeca, (.145 * sx, .032, .352), (.075, .095, .038), color.rgb32(37, 45, 56))
            esfera(cabeca, (.151 * sx, .164, .304), (.22, .067, .08), self.cor_cabelo,
                   rotation_z=8 * sx)
        esfera(cabeca, (0, -.075, .372), (.19, .26, .21), pele)
        esfera(cabeca, (0, -.272, .316), (.28, .046, .045), color.rgb32(121, 66, 64))

        estilo = self.dados.get("estilo_cabelo", "social")
        if estilo != "calvo":
            esfera(cabeca, (0, .321, -.035), (.737, .31, .657), self.cor_cabelo)
            if estilo in ("topete", "despojado"):
                for i in range(5):
                    xx = (i - 2) * .125
                    yy = .40 + (.13 if estilo == "topete" else random.Random(i).uniform(.02, .14))
                    esfera(cabeca, (xx, yy, .17), (.27, .21, .28), self.cor_cabelo,
                           rotation_z=(i - 2) * -13)
            if estilo in ("curto", "grisalho"):
                esfera(cabeca, (0, .31, .17), (.64, .20, .37), self.cor_cabelo)
        if self.dados.get("barba", False):
            esfera(cabeca, (0, -.295, .207), (.51, .19, .35), self.cor_cabelo)
            for sx in (-1, 1):
                esfera(cabeca, (.17 * sx, -.15, .347), (.19, .11, .07), self.cor_cabelo)
        if self.dados.get("oculos", False) or self.acessorio == "Óculos Escuros":
            lente = color.rgb32(17, 23, 33) if self.acessorio == "Óculos Escuros" else color.rgb32(51, 67, 86)
            for sx in (-1, 1):
                esfera(cabeca, (.16 * sx, .053, .351), (.33, .23, .087), lente)
            esfera(cabeca, (0, .07, .37), (.12, .047, .068), color.rgb32(44, 44, 49))

        if self.acessorio == "Faixa Presidencial":
            esfera(p, (0, 1.70, .41), (.13, 1.10, .09), color.rgb32(24, 159, 72),
                   rotation_z=-33)
            esfera(p, (0, 1.70, .48), (.035, 1.05, .035), color.rgb32(245, 210, 59),
                   rotation_z=-33)
        elif self.acessorio == "Gravata Borboleta":
            for sx in (-1, 1):
                esfera(p, (.14 * sx, 2.056, .44), (.29, .22, .11), color.rgb32(207, 34, 48),
                       rotation_z=-22 * sx)
            esfera(p, (0, 2.056, .49), (.14, .15, .13), color.rgb32(137, 18, 34))
        elif self.acessorio == "Chapéu Político":
            Entity(parent=cabeca, model=Cylinder(resolution=24, start=-.5), position=(0, .48, 0),
                   scale=(.94, .095, .87), color=color.rgb32(34, 42, 61), shader=basic_lighting_shader)
            esfera(cabeca, (0, .65, 0), (.60, .38, .55), color.rgb32(41, 50, 69))
            esfera(cabeca, (0, .58, .30), (.57, .09, .10), color.rgb32(222, 188, 57))

    @property
    def x(self):
        return self.root.x

    @property
    def z(self):
        return self.root.z

    def olhar_para(self, outro):
        dx = outro.x - self.x
        if abs(dx) > .12:
            self.direcao = 1 if dx > 0 else -1
            self.root.rotation_y = 90 * self.direcao

    def andar(self, eixo_x, eixo_z, dt):
        mag = math.hypot(eixo_x, eixo_z)
        if mag > 1:
            eixo_x /= mag
            eixo_z /= mag
        fator = min(1, dt * 11)
        self.vx += (eixo_x * self.velocidade - self.vx) * fator
        self.vz += (eixo_z * self.velocidade * .76 - self.vz) * fator
        if self.hit_tempo > 0:
            self.vx *= .55
            self.vz *= .55
        self.root.x = max(-7.35, min(7.35, self.root.x + self.vx * dt))
        self.root.z = max(-3.25, min(3.25, self.root.z + self.vz * dt))
        self.andando = (abs(self.vx) + abs(self.vz)) > .26

    def iniciar_ataque(self, tipo):
        if self.vida <= 0 or self.recarga > 0 or self.hit_tempo > 0:
            return False
        if tipo not in self.DURACAO:
            return False
        self.ataque = tipo
        self.ataque_tempo = 0
        self.ataque_total = self.DURACAO[tipo]
        self.recarga = self.RECARGA[tipo]
        self.ja_atingiu = False
        return True

    def animar(self, dt):
        self.tempo += dt
        self.recarga = max(0, self.recarga - dt)
        self.hit_tempo = max(0, self.hit_tempo - dt)
        if self.ataque:
            self.ataque_tempo += dt
            if self.ataque_tempo >= self.ataque_total:
                self.ataque = None
        fase = math.sin(self.tempo * 11) if self.andando else 0
        bob = math.sin(self.tempo * 2.6) * .023 + abs(fase) * .045
        self.esqueleto.y = bob
        self.esqueleto.rotation_z = (math.sin(self.tempo * 2.2) * 1.2
                                    + (10 if self.hit_tempo > 0 else 0) * -self.direcao)
        for i, perna in enumerate(self.pernas):
            perna.rotation_x = (fase * (24 if i == 0 else -24))
            perna.rotation_z = (3 if i == 0 else -3)
        for i, braco in enumerate(self.bracos):
            braco.rotation_x = fase * (-16 if i == 0 else 16)
            braco.rotation_z = (-8 if i == 0 else 8)
        if self.ataque:
            t = min(1, self.ataque_tempo / self.ataque_total)
            gesto = max(0, math.sin(t * math.pi)) ** .65
            if self.ataque == "soco":
                self.bracos[1].rotation_x = -97 * gesto
                self.bracos[1].rotation_z = -16
                self.esqueleto.rotation_y = -10 * gesto
            else:
                self.pernas[1].rotation_x = -83 * gesto
                self.bracos[0].rotation_x = 25 * gesto
                self.esqueleto.rotation_y = 8 * gesto
        else:
            self.esqueleto.rotation_y = 0
        self.corpo.color = color.rgb32(224, 72, 79) if self.hit_tempo > 0 else self.cor_roupa

    def receber_golpe(self, dano, direcao):
        self.vida = max(0, self.vida - dano)
        self.hit_tempo = .28
        self.root.x = max(-7.35, min(7.35, self.root.x + .30 * direcao))
        self.vx = 0
        self.vz = 0

    def remover(self):
        destroy(self.root)
