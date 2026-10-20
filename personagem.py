"""Dados dos candidatos e personagem 3D do jogo (motor Ursina)."""
from ursina import *
import math

ACESSORIOS = [
    "Nenhum", "Óculos Escuros", "Faixa Presidencial",
    "Gravata Borboleta", "Chapéu Político",
]

CANDIDATOS = [
    dict(nome="Renan Santos", terno=color.rgb(25,25,30), camisa=color.rgb(10,10,10), calca=color.rgb(110,150,200), pele=color.rgb(240,194,142), cabelo=color.rgb(30,25,20), estilo="despojado", velocidade=8.0, forca=14),
    dict(nome="Lula", terno=color.rgb(15,40,110), camisa=color.rgb(240,240,240), calca=color.rgb(15,40,110), pele=color.rgb(240,194,142), cabelo=color.rgb(235,235,235), estilo="grisalho", velocidade=6.8, forca=13),
    dict(nome="Flávio", terno=color.rgb(240,210,30), camisa=color.rgb(240,210,30), calca=color.rgb(110,150,200), pele=color.rgb(240,194,142), cabelo=color.rgb(35,25,20), estilo="social", velocidade=7.6, forca=12),
    dict(nome="Augusto Cury", terno=color.rgb(30,45,80), camisa=color.rgb(180,210,240), calca=color.rgb(50,50,55), pele=color.rgb(240,194,142), cabelo=color.rgb(40,35,30), estilo="social", velocidade=6.2, forca=11),
    dict(nome="Caiado", terno=color.rgb(20,35,90), camisa=color.rgb(240,240,240), calca=color.rgb(20,35,90), pele=color.rgb(240,194,142), cabelo=color.rgb(210,210,210), estilo="grisalho", velocidade=7.0, forca=14),
    dict(nome="Zema", terno=color.rgb(25,35,65), camisa=color.rgb(25,35,65), calca=color.rgb(40,40,50), pele=color.rgb(240,194,142), cabelo=color.rgb(170,170,175), estilo="curto", velocidade=7.8, forca=10),
]
PERSONAGENS_BASE = CANDIDATOS

class Lutador3D(Entity):
    """Lutador construído com primitivas 3D do Ursina."""
    def __init__(self, dados, acessorio, x, controles, cor_nome, lado):
        super().__init__(position=(x, 0, 0))
        self.dados, self.acessorio, self.controles = dados, acessorio, controles
        self.cor_nome, self.lado = cor_nome, lado
        self.vida = 100
        self.cooldown = 0.0
        self.atacando = False
        self.tempo_ataque = 0.0
        self.velocidade = dados["velocidade"] * 0.65
        self.forca = dados["forca"]
        self.direcao = 1 if lado == 1 else -1
        self.tempo_hit = 0.0
        self.partes = []

        def parte(modelo, pos, escala, cor, **kw):
            entidade = Entity(model=modelo, parent=self, position=pos, scale=escala, color=cor, **kw)
            self.partes.append(entidade)
            return entidade

        # Pernas, sapatos, tronco, cabeça, cabelo e braços.
        parte("cube", (-.19,.48,0), (.22,.9,.28), dados["calca"])
        parte("cube", (.19,.48,0), (.22,.9,.28), dados["calca"])
        parte("cube", (-.19,.06,-.06), (.32,.12,.48), color.rgb(20,20,25))
        parte("cube", (.19,.06,-.06), (.32,.12,.48), color.rgb(20,20,25))
        parte("cube", (0,1.25,0), (.82,.92,.42), dados["terno"])
        parte("cube", (0,1.27,-.225), (.22,.72,.035), dados["camisa"])
        self.cabeca = parte("sphere", (0,2.05,0), (.48,.5,.44), dados["pele"])
        parte("sphere", (0,2.28,0), (.49,.22,.45), dados["cabelo"])
        self.braco1 = parte("cube", (-.55,1.42,-.02), (.22,.78,.25), dados["terno"])
        self.braco2 = parte("cube", (.55,1.42,-.02), (.22,.78,.25), dados["terno"])

        if dados["nome"] in ("Lula", "Caiado"):
            parte("cube", (0,1.27,-.25), (.12,.95,.045), color.rgb(20,160,40), rotation_z=-24)
            parte("cube", (0,1.27,-.28), (.08,.95,.045), color.rgb(255,215,0), rotation_z=-24)
        if dados["nome"] == "Zema":
            parte("cube", (0,1.68,-.25), (.48,.08,.04), color.orange)

        if acessorio == "Óculos Escuros":
            parte("cube", (0,2.08,-.39), (.46,.12,.05), color.black)
        elif acessorio == "Faixa Presidencial":
            parte("cube", (0,1.3,-.30), (.15,1,.06), color.rgb(255,215,0), rotation_z=-24)
        elif acessorio == "Gravata Borboleta":
            parte("cube", (0,1.68,-.28), (.3,.12,.07), color.red)
        elif acessorio == "Chapéu Político":
            parte("cube", (0,2.42,0), (.72,.1,.62), color.rgb(40,40,50))
            parte("cube", (0,2.53,0), (.42,.2,.4), color.rgb(40,40,50))

        self.collider = BoxCollider(self, center=(0,1.15,0), size=(1.1,2.3,.8))

    def mover(self):
        from ursina import held_keys, time, clamp, Vec3
        if self.cooldown > 0:
            self.cooldown = max(0, self.cooldown-time.dt)
        dx = held_keys[self.controles["right"]] - held_keys[self.controles["left"]]
        dz = held_keys[self.controles["back"]] - held_keys[self.controles["forward"]]
        direcao = Vec3(dx,0,dz)
        if direcao.length() > 1:
            direcao = direcao.normalized()
        self.x += direcao.x*self.velocidade*time.dt
        self.z += direcao.z*self.velocidade*time.dt
        self.x = clamp(self.x,-10,10)
        self.z = clamp(self.z,-6,6)
        if dx:
            self.direcao = 1 if dx > 0 else -1
        if self.tempo_hit > 0:
            self.tempo_hit = max(0,self.tempo_hit-time.dt)
        if self.atacando:
            self.tempo_ataque -= time.dt
            if self.tempo_ataque <= 0:
                self.atacando = False
                self.braco1.rotation_z = 0
