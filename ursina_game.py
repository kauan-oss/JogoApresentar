"""Versão 3D do Eleições Fighting Game usando Ursina.
Mantém os candidatos, acessórios, seleção, controles e combate melhor de três.
Instalação: pip install -r requirements.txt
Execução: python main.py
"""
from ursina import *
import random
import math

app = Ursina(title="Eleições Fighting Game 3D", borderless=False)
window.size = (1280, 720)
window.color = color.rgb(22, 27, 43)
window.exit_button.visible = False
camera.position = (0, 8, -16)
camera.rotation_x = 22

CANDIDATOS = [
    dict(nome="Renan Santos", terno=color.rgb(25,25,30), camisa=color.rgb(10,10,10), calca=color.rgb(110,150,200), pele=color.rgb(240,194,142), cabelo=color.rgb(30,25,20), estilo="despojado", velocidade=8.0, forca=14),
    dict(nome="Lula", terno=color.rgb(15,40,110), camisa=color.rgb(240,240,240), calca=color.rgb(15,40,110), pele=color.rgb(240,194,142), cabelo=color.rgb(235,235,235), estilo="grisalho", velocidade=6.8, forca=13),
    dict(nome="Flávio", terno=color.rgb(240,210,30), camisa=color.rgb(240,210,30), calca=color.rgb(110,150,200), pele=color.rgb(240,194,142), cabelo=color.rgb(35,25,20), estilo="social", velocidade=7.6, forca=12),
    dict(nome="Augusto Cury", terno=color.rgb(30,45,80), camisa=color.rgb(180,210,240), calca=color.rgb(50,50,55), pele=color.rgb(240,194,142), cabelo=color.rgb(40,35,30), estilo="social", velocidade=6.2, forca=11),
    dict(nome="Caiado", terno=color.rgb(20,35,90), camisa=color.rgb(240,240,240), calca=color.rgb(20,35,90), pele=color.rgb(240,194,142), cabelo=color.rgb(210,210,210), estilo="grisalho", velocidade=7.0, forca=14),
    dict(nome="Zema", terno=color.rgb(25,35,65), camisa=color.rgb(25,35,65), calca=color.rgb(40,40,50), pele=color.rgb(240,194,142), cabelo=color.rgb(170,170,175), estilo="curto", velocidade=7.8, forca=10),
]
ACESSORIOS = ["Nenhum", "Óculos Escuros", "Faixa Presidencial", "Gravata Borboleta", "Chapéu Político"]
P1_KEYS = {'left':'a','right':'d','forward':'w','back':'s','punch':'f','kick':'g'}
P2_KEYS = {'left':'left arrow','right':'right arrow','forward':'up arrow','back':'down arrow','punch':'k','kick':'l'}
estado = 'menu'
idx1, idx2, ac1, ac2 = 0, 1, 0, 0
vitorias1 = vitorias2 = 0
lutadores = []
ui = []
mensagem = None
tempo_mensagem = 0
last_hud_state = None

# Arena tridimensional: piso, linhas de perspectiva e iluminação.
Entity(model='plane', scale=(24,1,18), position=(0,0,0), color=color.rgb(70,75,85), texture='white_cube', texture_scale=(12,9), collider='box')
for x in range(-11,12,2):
    Entity(model='cube', position=(x,0.015,0), scale=(.025,.02,18), color=color.rgb(100,105,120))
for z in range(-8,10,2):
    Entity(model='cube', position=(0,.02,z), scale=(24,.02,.025), color=color.rgb(100,105,120))
Entity(model='cube', position=(0,.08,8.8), scale=(24,.15,.12), color=color.gold)
Entity(model='sphere', position=(0,9,7), scale=2, color=color.rgb(255,220,100), unlit=True)
Sky(color=color.rgb(95,145,205))
DirectionalLight(y=10, z=-5, rotation=(45,-35,0), shadows=True)
AmbientLight(color=color.rgba(150,150,150,0.55))

def limpar_ui():
    global ui
    for elemento in ui:
        destroy(elemento)
    ui = []

def texto(conteudo, pos, escala=1, cor=color.white, **kwargs):
    t = Text(conteudo, position=pos, scale=escala, color=cor, **kwargs)
    ui.append(t)
    return t

def botao(conteudo, pos, acao, escala=(.28,.065), cor=color.rgb(45,55,78)):
    b = Button(text=conteudo, position=pos, scale=escala, color=cor, highlight_color=color.azure, pressed_color=color.gold, on_click=acao)
    ui.append(b)
    return b

class Lutador3D(Entity):
    def __init__(self, dados, acessorio, x, controles, cor_nome, lado):
        super().__init__(position=(x,0,0))
        self.dados, self.acessorio, self.controles = dados, acessorio, controles
        self.cor_nome, self.lado = cor_nome, lado
        self.vida, self.cooldown, self.atacando, self.tempo_ataque = 100, 0, False, 0
        self.velocidade = dados['velocidade'] * .65
        self.forca = dados['forca']
        self.direcao = 1 if lado == 1 else -1
        self.partes = []
        def parte(modelo, parent, pos, escala, cor, **kw):
            e = Entity(model=modelo, parent=parent, position=pos, scale=escala, color=cor, **kw)
            self.partes.append(e)
            return e
        # Pernas, tronco, cabeça e braços são peças 3D independentes.
        parte('cube', self, (-.19,.48,0), (.22,.9,.28), dados['calca'])
        parte('cube', self, (.19,.48,0), (.22,.9,.28), dados['calca'])
        parte('cube', self, (0,1.25,0), (.82,.92,.42), dados['terno'])
        parte('cube', self, (0,1.27,-.225), (.22,.72,.035), dados['camisa'])
        self.cabeca = parte('sphere', self, (0,2.05,0), (.48,.5,.44), dados['pele'])
        parte('sphere', self, (0,2.28,0), (.49,.22,.45), dados['cabelo'])
        self.braco1 = parte('cube', self, (-.55,1.42,0), (.22,.78,.25), dados['terno'])
        self.braco2 = parte('cube', self, (.55,1.42,0), (.22,.78,.25), dados['terno'])
        parte('cube', self, (0,.06,0), (.85,.12,.48), color.rgb(25,25,30))
        if dados['nome'] in ('Lula','Caiado'):
            parte('cube', self, (0,1.27,-.25), (.12,.95,.045), color.rgb(255,215,0), rotation_z=-24)
        if dados['nome'] == 'Zema':
            parte('cube', self, (0,1.68,-.25), (.48,.08,.04), color.orange)
        if acessorio == 'Óculos Escuros':
            parte('cube', self, (0,2.08,-.39), (.46,.12,.05), color.black)
        elif acessorio == 'Faixa Presidencial':
            parte('cube', self, (0,1.3,-.27), (.15,1,.06), color.rgb(255,215,0), rotation_z=-24)
        elif acessorio == 'Gravata Borboleta':
            parte('cube', self, (0,1.68,-.28), (.3,.12,.07), color.red)
        elif acessorio == 'Chapéu Político':
            parte('cube', self, (0,2.42,0), (.72,.1,.62), color.rgb(40,40,50))
            parte('cube', self, (0,2.53,0), (.42,.2,.4), color.rgb(40,40,50))
        self.collider = BoxCollider(self, center=(0,1.15,0), size=(1.1,2.3,.8))

    def mover(self):
        if self.cooldown > 0: self.cooldown -= time.dt
        dx = (held_keys[self.controles['right']] - held_keys[self.controles['left']])
        dz = (held_keys[self.controles['back']] - held_keys[self.controles['forward']])
        direcao = Vec3(dx,0,dz)
        if direcao.length() > 1: direcao = direcao.normalized()
        self.x += direcao.x * self.velocidade * time.dt
        self.z += direcao.z * self.velocidade * time.dt
        self.x = clamp(self.x,-10,10)
        self.z = clamp(self.z,-6,6)
        if dx: self.direcao = 1 if dx > 0 else -1
        if self.atacando:
            self.tempo_ataque -= time.dt
            self.braco1.rotation_z = -70 * self.direcao
            if self.tempo_ataque <= 0:
                self.atacando = False
                self.braco1.rotation_z = 0

    def atacar(self, tipo, inimigo):
        if self.cooldown > 0: return
        self.cooldown = .48 if tipo == 'soco' else .68
        self.atacando, self.tempo_ataque = True, .22
        self.braco1.rotation_z = -70 * self.direcao
        alcance = 1.65 if tipo == 'soco' else 2.0
        frente = (inimigo.x-self.x) * self.direcao > 0
        perto = abs(inimigo.x-self.x) < alcance and abs(inimigo.z-self.z) < 1.15
        if frente and perto:
            dano = self.forca if tipo == 'soco' else int(self.forca*1.35)
            inimigo.vida = max(0, inimigo.vida-dano)
            inimigo.x += .35*self.direcao

def iniciar_luta():
    global estado, lutadores, vitorias1, vitorias2
    limpar_ui()
    estado='luta'
    vitorias1=vitorias2=0
    criar_round()

def criar_round():
    global lutadores
    for l in lutadores: destroy(l)
    lutadores = [
        Lutador3D(CANDIDATOS[idx1], ACESSORIOS[ac1], -4, P1_KEYS, color.azure, 1),
        Lutador3D(CANDIDATOS[idx2], ACESSORIOS[ac2], 4, P2_KEYS, color.red, -1)
    ]
    atualizar_hud()

def atualizar_hud():
    global last_hud_state
    limpar_ui()
    texto(f'{CANDIDATOS[idx1]["nome"]}  |  HP: {lutadores[0].vida}  |  ROUNDS: {vitorias1}', (-.86,.45), .9, color.azure)
    texto(f'{CANDIDATOS[idx2]["nome"]}  |  HP: {lutadores[1].vida}  |  ROUNDS: {vitorias2}', (.25,.45), .9, color.red)
    texto('P1: WASD + F soco + G chute     P2: Setas + K soco + L chute', (-.48,-.46), .8)
    texto('F11: tela cheia  |  ESC: menu', (-.18,-.49), .65, color.gold)
    last_hud_state = (lutadores[0].vida, lutadores[1].vida, vitorias1, vitorias2)

def menu():
    global estado
    estado='menu'
    for l in lutadores: destroy(l)
    limpar_ui()
    camera.position=(0,8,-16); camera.rotation_x=22
    texto('ELEIÇÕES FIGHTING GAME', (-.36,.39), 1.6, color.gold)
    texto('SELEÇÃO DE CANDIDATOS (MD3)', (-.28,.29), .9)
    texto(f'P1: {CANDIDATOS[idx1]["nome"]}  |  Acessório: {ACESSORIOS[ac1]}',(-.75,.17),.8,color.azure)
    texto(f'P2: {CANDIDATOS[idx2]["nome"]}  |  Acessório: {ACESSORIOS[ac2]}',(.12,.17),.8,color.red)
    texto('P1: A/D candidato, W/S acessório',(-.7,.04),.7)
    texto('P2: ←/→ candidato, ↑/↓ acessório',(.12,.04),.7)
    texto('F11: tela cheia  |  R: sortear candidatos  |  ENTER: iniciar',(-.47,-.06),.7,color.gold)
    botao('P1: candidato anterior',(-.55,-.19),lambda:selecionar(-1,0,0))
    botao('P1: próximo candidato',(-.25,-.19),lambda:selecionar(1,0,0))
    botao('P2: candidato anterior',(.25,-.19),lambda:selecionar(0,-1,0))
    botao('P2: próximo candidato',(.55,-.19),lambda:selecionar(0,1,0))
    botao('P1: acessório anterior',(-.55,-.29),lambda:selecionar(0,0,-1))
    botao('P1: próximo acessório',(-.25,-.29),lambda:selecionar(0,0,1))
    botao('P2: acessório anterior',(.25,-.29),lambda:selecionar(0,0,-2))
    botao('P2: próximo acessório',(.55,-.29),lambda:selecionar(0,0,2))
    botao('INICIAR COMBATE', (0,-.40), iniciar_luta, (.34,.075), color.rgb(30,115,65))

def selecionar(d1=0,d2=0,da=0):
    global idx1,idx2,ac1,ac2
    if d1: idx1=(idx1+d1)%len(CANDIDATOS)
    if d2: idx2=(idx2+d2)%len(CANDIDATOS)
    if da == -1: ac1=(ac1-1)%len(ACESSORIOS)
    elif da == 1: ac1=(ac1+1)%len(ACESSORIOS)
    elif da == -2: ac2=(ac2-1)%len(ACESSORIOS)
    elif da == 2: ac2=(ac2+1)%len(ACESSORIOS)
    menu()

def atualizar():
    global estado, vitorias1, vitorias2, last_hud_state
    if estado != 'luta' or len(lutadores)!=2: return
    p1,p2=lutadores
    p1.mover(); p2.mover()
    if p1.vida<=0 or p2.vida<=0:
        if p1.vida<=0: vitorias2+=1
        else: vitorias1+=1
        if vitorias1>=2 or vitorias2>=2:
            vencedor=CANDIDATOS[idx1 if vitorias1>=2 else idx2]['nome']
            estado='fim'
            limpar_ui()
            texto('ELEIÇÕES ENCERRADAS!',(-.3,.15),1.5,color.gold)
            texto(f'NOVO PRESIDENTE: {vencedor.upper()}!',(-.42,.03),1.1,color.lime)
            botao('VOLTAR AO MENU', (0,-.15), menu, (.3,.07))
        else:
            criar_round()
    else:
        hud_state = (p1.vida, p2.vida, vitorias1, vitorias2)
        if hud_state != last_hud_state:
            atualizar_hud()

def input(tecla):
    global idx1,idx2,ac1,ac2
    if tecla=='f11': window.fullscreen=not window.fullscreen
    if estado=='menu':
        if tecla=='enter': iniciar_luta()
        elif tecla=='r':
            random.shuffle(CANDIDATOS); idx1,idx2=0,1
            menu()
        elif tecla=='a': selecionar(-1,0,0)
        elif tecla=='d': selecionar(1,0,0)
        elif tecla=='w': selecionar(0,0,-1)
        elif tecla=='s': selecionar(0,0,1)
        elif tecla=='left arrow': selecionar(0,-1,0)
        elif tecla=='right arrow': selecionar(0,1,0)
        elif tecla=='up arrow': selecionar(0,0,-2)
        elif tecla=='down arrow': selecionar(0,0,2)
    elif estado=='luta' and tecla in ('f','g','k','l') and len(lutadores)==2:
        atacante = lutadores[0] if tecla in ('f','g') else lutadores[1]
        defensor = lutadores[1] if atacante is lutadores[0] else lutadores[0]
        atacante.atacar('soco' if tecla in ('f','k') else 'chute', defensor)
    elif tecla=='escape' and estado in ('luta','fim'):
        menu()

menu()
