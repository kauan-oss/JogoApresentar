"""Eleições Fighting Arena 3D — Ursina, dois jogadores no mesmo teclado.

Executar:
    python -m pip install -r requirements.txt
    python main.py
"""
from __future__ import annotations

import random
from ursina import Ursina, Entity, Vec3, camera, window, mouse, held_keys, time, color, destroy

from cenario import Arena
from personagem import ACESSORIOS, Lutador3D, gerar_candidatos_padrao, gerar_candidato_aleatorio
from colisao import verificar_ataque_e_colisao
from menu import Interface


class Partida:
    def __init__(self):
        self.arena = Arena()
        self.ui = Interface()
        self.candidatos = gerar_candidatos_padrao()
        self.id1, self.id2 = 0, 1
        self.a1, self.a2 = 0, 0
        self.v1 = self.v2 = 0
        self.p1 = self.p2 = None
        self.estado = "menu"
        self.intervalo = 0.0
        self.aviso = ""
        self.tempo_aviso = 0.0
        self.particulas = []
        self.exibir_menu()

    def criar_lutadores(self):
        if self.p1 is not None:
            self.p1.remover()
        if self.p2 is not None:
            self.p2.remover()
        self.p1 = Lutador3D(self.candidatos[self.id1], ACESSORIOS[self.a1], -3.75, -.15, lado=1)
        self.p2 = Lutador3D(self.candidatos[self.id2], ACESSORIOS[self.a2], 3.75, .15, lado=2)
        self.p1.olhar_para(self.p2)
        self.p2.olhar_para(self.p1)

    def exibir_menu(self):
        self.estado = "menu"
        self.v1 = self.v2 = 0
        self.ui.exibir("menu")
        self.ui.selecionar(self.candidatos[self.id1], self.candidatos[self.id2],
                           ACESSORIOS[self.a1], ACESSORIOS[self.a2])
        self.criar_lutadores()

    def escolher(self, tecla):
        mudou = True
        if tecla == "a":
            self.id1 = (self.id1 - 1) % len(self.candidatos)
        elif tecla == "d":
            self.id1 = (self.id1 + 1) % len(self.candidatos)
        elif tecla == "w":
            self.a1 = (self.a1 - 1) % len(ACESSORIOS)
        elif tecla == "s":
            self.a1 = (self.a1 + 1) % len(ACESSORIOS)
        elif tecla == "left arrow":
            self.id2 = (self.id2 - 1) % len(self.candidatos)
        elif tecla == "right arrow":
            self.id2 = (self.id2 + 1) % len(self.candidatos)
        elif tecla == "up arrow":
            self.a2 = (self.a2 - 1) % len(ACESSORIOS)
        elif tecla == "down arrow":
            self.a2 = (self.a2 + 1) % len(ACESSORIOS)
        elif tecla == "r":
            self.candidatos = [gerar_candidato_aleatorio(i) for i in range(6)]
            self.id1, self.id2 = 0, 1
            self.a1, self.a2 = 0, 0
        else:
            mudou = False
        if mudou:
            self.ui.selecionar(self.candidatos[self.id1], self.candidatos[self.id2],
                               ACESSORIOS[self.a1], ACESSORIOS[self.a2])
            self.criar_lutadores()

    def iniciar(self):
        self.v1 = self.v2 = 0
        self.nova_rodada()

    def nova_rodada(self):
        self.estado = "jogo"
        self.intervalo = 0.0
        self.aviso = "ROUND INICIADO!"
        self.tempo_aviso = 1.0
        self.ui.exibir("jogo")
        self.criar_lutadores()
        self.atualizar_hud()

    def atualizar_hud(self):
        self.ui.atualizar_placar(self.p1, self.p2, self.v1, self.v2, self.aviso)

    def impacto(self, alvo, texto, dano):
        self.aviso = f"{texto}  -{dano} HP"
        self.tempo_aviso = .70
        base = Vec3(alvo.x, 1.55, alvo.z)
        for _ in range(7):
            esfera = Entity(model="sphere", position=base + Vec3(
                random.uniform(-.38, .38),
                random.uniform(-.45, .45),
                random.uniform(-.32, .32)),
                scale=random.uniform(.08, .22),
                color=random.choice([color.rgb32(255, 207, 95),
                                     color.rgb32(241, 97, 112),
                                     color.rgb32(99, 226, 245)]))
            esfera.animate_scale(0, duration=.27)
            destroy(esfera, delay=.32)

    def fim_de_rodada(self):
        if self.p1.vida <= 0:
            self.v2 += 1
            nome = self.p2.nome
        elif self.p2.vida <= 0:
            self.v1 += 1
            nome = self.p1.nome
        else:
            return
        if self.v1 >= 2 or self.v2 >= 2:
            self.estado = "vitoria"
            self.ui.finalizar(nome)
        else:
            self.estado = "intervalo"
            self.intervalo = 1.85
            self.aviso = f"ROUND PARA {nome.upper()}!  PRÓXIMO EM INSTANTES"
            self.atualizar_hud()

    def atualizar(self):
        dt = min(time.dt, .05)
        if self.p1 is None or self.p2 is None:
            return
        if self.estado == "menu":
            self.p1.animar(dt)
            self.p2.animar(dt)
            return
        if self.estado == "vitoria":
            self.p1.animar(dt)
            self.p2.animar(dt)
            return
        if self.estado == "intervalo":
            self.p1.animar(dt)
            self.p2.animar(dt)
            self.intervalo -= dt
            if self.intervalo <= 0:
                self.nova_rodada()
            return

        eixo1_x = int(bool(held_keys["d"])) - int(bool(held_keys["a"]))
        eixo1_z = int(bool(held_keys["w"])) - int(bool(held_keys["s"]))
        eixo2_x = int(bool(held_keys["right arrow"])) - int(bool(held_keys["left arrow"]))
        eixo2_z = int(bool(held_keys["up arrow"])) - int(bool(held_keys["down arrow"]))

        self.p1.andar(eixo1_x, eixo1_z, dt)
        self.p2.andar(eixo2_x, eixo2_z, dt)
        self.p1.olhar_para(self.p2)
        self.p2.olhar_para(self.p1)
        self.p1.animar(dt)
        self.p2.animar(dt)

        for _atacante, alvo, dano, palavra in verificar_ataque_e_colisao(self.p1, self.p2):
            self.impacto(alvo, palavra, dano)

        if self.tempo_aviso > 0:
            self.tempo_aviso -= dt
            if self.tempo_aviso <= 0:
                self.aviso = ""
        self.atualizar_hud()
        if self.p1.vida <= 0 or self.p2.vida <= 0:
            self.fim_de_rodada()

    def tecla(self, key):
        if key == "f11":
            window.fullscreen = not window.fullscreen
            return
        if self.estado == "menu":
            if key == "enter":
                self.iniciar()
            elif key == "escape":
                from ursina import application
                application.quit()
            else:
                self.escolher(key)
            return
        if key == "escape":
            self.exibir_menu()
            return
        if self.estado == "vitoria":
            if key == "enter":
                self.exibir_menu()
            return
        if self.estado != "jogo":
            return
        if key == "f":
            self.p1.iniciar_ataque("soco")
        elif key == "g":
            self.p1.iniciar_ataque("chute")
        elif key in ("k", "j", "ç"):
            self.p2.iniciar_ataque("soco")
        elif key == "l":
            self.p2.iniciar_ataque("chute")


partida = None


def update():
    if partida is not None:
        partida.atualizar()


def input(key):
    if partida is not None:
        partida.tecla(key)


def iniciar():
    global partida
    app = Ursina(title="Eleições Fighting Arena 3D", borderless=False,
                 fullscreen=False, size=(1280, 720), vsync=True,
                 development_mode=False)
    window.color = color.rgb32(12, 23, 47)
    window.exit_button.visible = False
    window.fps_counter.enabled = False
    mouse.visible = True
    camera.position = Vec3(0, 7.8, -20.5)
    camera.look_at(Vec3(0, 1.35, .35))
    camera.fov = 48
    partida = Partida()
    app.run()


if __name__ == "__main__":
    iniciar()
