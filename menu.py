"""Interface 2D sobreposta a cena 3D (menu, HUD e tela de vitoria)."""
from ursina import Entity, Text, camera, color


def painel(pai, pos, escala, opacidade=194):
    return Entity(parent=pai, model="quad", position=pos, scale=escala,
                  color=color.rgba(10, 18, 37, opacidade))


class Interface:
    def __init__(self):
        self.menu = Entity(parent=camera.ui)
        self.jogo = Entity(parent=camera.ui, enabled=False)
        self.vitoria = Entity(parent=camera.ui, enabled=False)

        painel(self.menu, (0, .425, .1), (1.78, .20), 210)
        Text(parent=self.menu, text="ELEIÇÕES  |  FIGHTING ARENA 3D",
             position=(0, .44), origin=(0, 0), scale=1.8,
             color=color.rgb(250, 213, 117))
        Text(parent=self.menu, text="ESCOLHA SEU CANDIDATO",
             position=(0, .335), origin=(0, 0), scale=.85,
             color=color.rgb(179, 214, 231))
        painel(self.menu, (-.50, -.015, .05), (.73, .19), 183)
        painel(self.menu, (.50, -.015, .05), (.73, .19), 183)
        self.nome1 = Text(parent=self.menu, text="", position=(-.78, .035),
                          scale=1.05, color=color.rgb(112, 205, 255))
        self.acess1 = Text(parent=self.menu, text="", position=(-.78, -.027),
                           scale=.80, color=color.rgb(213, 233, 249))
        self.nome2 = Text(parent=self.menu, text="", position=(.22, .035),
                          scale=1.05, color=color.rgb(255, 136, 139))
        self.acess2 = Text(parent=self.menu, text="", position=(.22, -.027),
                           scale=.80, color=color.rgb(247, 216, 216))
        painel(self.menu, (0, -.405, .12), (1.7, .22), 212)
        Text(parent=self.menu, text="P1: A/D candidato  W/S acessório     |     P2: SETAS candidato/acessório",
             position=(0, -.35), origin=(0, 0), scale=.78,
             color=color.rgb(231, 232, 242))
        Text(parent=self.menu, text="ENTER iniciar  •  R sortear elenco  •  F11 tela cheia  •  ESC sair",
             position=(0, -.415), origin=(0, 0), scale=.79,
             color=color.rgb(255, 215, 132))

        painel(self.jogo, (0, .426, .1), (1.8, .16), 206)
        self.n1 = Text(parent=self.jogo, position=(-.85, .459), scale=.88,
                       color=color.rgb(178, 224, 255))
        self.n2 = Text(parent=self.jogo, position=(.22, .459), scale=.88,
                       color=color.rgb(255, 186, 189))
        self.barra_fundo1 = painel(self.jogo, (-.85, .414, 0), (.67, .030), 255)
        self.barra_fundo1.origin = (-.5, 0)
        self.barra_fundo2 = painel(self.jogo, (.22, .414, 0), (.67, .030), 255)
        self.barra_fundo2.origin = (-.5, 0)
        self.barra1 = Entity(parent=self.jogo, model="quad", position=(-.85, .414, -.01),
                             origin=(-.5, 0), scale=(.67, .029),
                             color=color.rgb(51, 220, 137))
        self.barra2 = Entity(parent=self.jogo, model="quad", position=(.22, .414, -.01),
                             origin=(-.5, 0), scale=(.67, .029),
                             color=color.rgb(241, 94, 111))
        self.placar = Text(parent=self.jogo, position=(0, .405), origin=(0, 0),
                           scale=1, color=color.rgb(251, 220, 131))
        self.aviso = Text(parent=self.jogo, position=(0, .195), origin=(0, 0),
                          scale=1.6, color=color.rgb(252, 221, 113))
        painel(self.jogo, (0, -.478, .1), (1.55, .065), 177)
        Text(parent=self.jogo,
             text="P1: WASD + F soco / G chute       P2: SETAS + K soco / L chute       ESC menu",
             position=(0, -.486), origin=(0, 0), scale=.66,
             color=color.rgb(235, 239, 250))

        painel(self.vitoria, (0, 0, .15), (1.25, .58), 237)
        self.titulo_final = Text(parent=self.vitoria, text="ELEIÇÕES ENCERRADAS!",
                                position=(0, .135), origin=(0, 0), scale=1.65,
                                color=color.rgb(251, 215, 107))
        self.vencedor = Text(parent=self.vitoria, position=(0, .01), origin=(0, 0),
                             scale=1.28, color=color.rgb(98, 228, 151))
        Text(parent=self.vitoria, text="ENTER: selecionar novamente   |   ESC: menu",
             position=(0, -.145), origin=(0, 0), scale=.90,
             color=color.rgb(227, 234, 243))

    def selecionar(self, dados1, dados2, acess1, acess2):
        self.nome1.text = "P1  " + dados1["nome"]
        self.acess1.text = "Acessório: " + acess1
        self.nome2.text = "P2  " + dados2["nome"]
        self.acess2.text = "Acessório: " + acess2

    def atualizar_placar(self, p1, p2, v1, v2, aviso=""):
        self.n1.text = f"{p1.nome}  |  {p1.vida} HP"
        self.n2.text = f"{p2.nome}  |  {p2.vida} HP"
        self.barra1.scale_x = .67 * max(0, p1.vida / 100)
        self.barra2.scale_x = .67 * max(0, p2.vida / 100)
        self.placar.text = f"{v1} : {v2}"
        self.aviso.text = aviso

    def exibir(self, qual):
        self.menu.enabled = qual == "menu"
        self.jogo.enabled = qual == "jogo"
        self.vitoria.enabled = qual == "vitoria"

    def finalizar(self, nome):
        self.vencedor.text = nome.upper() + " VENCEU!"
        self.exibir("vitoria")
