"""Loop principal do Eleições Fighting Game em 3D com Ursina."""
from ursina import *
import random

from personagem import CANDIDATOS, ACESSORIOS, Lutador3D
from colisao import resolver_ataque
from menu import limpar_ui, texto, botao, desenhar_painel_controles

app = Ursina(title="Eleições Fighting Game 3D", borderless=False)
window.size = (1280, 720)
window.color = color.rgb(22, 27, 43)
window.exit_button.visible = False
camera.position = (0, 8, -16)
camera.rotation_x = 22
camera.fov = 70

P1_KEYS = {"left":"a", "right":"d", "forward":"w", "back":"s"}
P2_KEYS = {"left":"left arrow", "right":"right arrow", "forward":"up arrow", "back":"down arrow"}

estado = "menu"
idx1, idx2, ac1, ac2 = 0, 1, 0, 0
vitorias1 = vitorias2 = 0
lutadores = []
ui = []
last_hud_state = None

# Arena 3D
Entity(model="plane", scale=(24,1,18), position=(0,0,0),
       color=color.rgb(70,75,85), texture="white_cube", texture_scale=(12,9),
       collider="box")
for x in range(-11,12,2):
    Entity(model="cube", position=(x,.015,0), scale=(.025,.02,18),
           color=color.rgb(100,105,120))
for z in range(-8,10,2):
    Entity(model="cube", position=(0,.02,z), scale=(24,.02,.025),
           color=color.rgb(100,105,120))
Entity(model="cube", position=(0,.08,8.8), scale=(24,.15,.12), color=color.gold)
Entity(model="sphere", position=(0,9,7), scale=2, color=color.rgb(255,220,100), unlit=True)
Sky(color=color.rgb(95,145,205))
DirectionalLight(y=10, z=-5, rotation=(45,-35,0), shadows=True)
AmbientLight(color=color.rgba(150,150,150,0.55))

def adicionar_texto(conteudo, pos, escala=1, cor=color.white, **kwargs):
    return texto(conteudo, pos, escala, cor, elementos=ui, **kwargs)

def adicionar_botao(conteudo, pos, acao, escala=(.28,.065), cor=color.rgb(45,55,78)):
    return botao(conteudo, pos, acao, elementos=ui, escala=escala, cor=cor)

def limpar_interface():
    limpar_ui(ui)

def criar_menu():
    global estado
    estado = "menu"
    for lutador in lutadores:
        destroy(lutador)
    lutadores.clear()
    limpar_interface()
    camera.position = (0,8,-16)
    camera.rotation_x = 22
    adicionar_texto("ELEIÇÕES FIGHTING GAME", (-.36,.39), 1.6, color.gold)
    adicionar_texto("LUTA 3D • MELHOR DE TRÊS", (-.25,.29), .9)
    adicionar_texto(f'P1: {CANDIDATOS[idx1]["nome"]} | Acessório: {ACESSORIOS[ac1]}',
                    (-.75,.17), .8, color.azure)
    adicionar_texto(f'P2: {CANDIDATOS[idx2]["nome"]} | Acessório: {ACESSORIOS[ac2]}',
                    (.12,.17), .8, color.red)
    adicionar_texto("P1: A/D candidato, W/S acessório", (-.7,.04), .7)
    adicionar_texto("P2: ←/→ candidato, ↑/↓ acessório", (.12,.04), .7)
    adicionar_texto("F11: tela cheia | R: sortear | ENTER: iniciar",
                    (-.47,-.06), .7, color.gold)
    adicionar_botao("P1: candidato anterior",(-.55,-.19),lambda:selecionar(-1,0,0))
    adicionar_botao("P1: próximo candidato",(-.25,-.19),lambda:selecionar(1,0,0))
    adicionar_botao("P2: candidato anterior",(.25,-.19),lambda:selecionar(0,-1,0))
    adicionar_botao("P2: próximo candidato",(.55,-.19),lambda:selecionar(0,1,0))
    adicionar_botao("P1: acessório anterior",(-.55,-.29),lambda:selecionar(0,0,-1))
    adicionar_botao("P1: próximo acessório",(-.25,-.29),lambda:selecionar(0,0,1))
    adicionar_botao("P2: acessório anterior",(.25,-.29),lambda:selecionar(0,0,-2))
    adicionar_botao("P2: próximo acessório",(.55,-.29),lambda:selecionar(0,0,2))
    adicionar_botao("INICIAR COMBATE",(0,-.40),iniciar_luta,(.34,.075),color.rgb(30,115,65))

def selecionar(d1=0,d2=0,da=0):
    global idx1, idx2, ac1, ac2
    if estado != "menu":
        return
    if d1: idx1 = (idx1+d1) % len(CANDIDATOS)
    if d2: idx2 = (idx2+d2) % len(CANDIDATOS)
    if da == -1: ac1 = (ac1-1) % len(ACESSORIOS)
    elif da == 1: ac1 = (ac1+1) % len(ACESSORIOS)
    elif da == -2: ac2 = (ac2-1) % len(ACESSORIOS)
    elif da == 2: ac2 = (ac2+1) % len(ACESSORIOS)
    criar_menu()

def iniciar_luta():
    global estado, vitorias1, vitorias2
    estado = "luta"
    vitorias1 = vitorias2 = 0
    criar_round()

def criar_round():
    limpar_interface()
    for lutador in lutadores:
        destroy(lutador)
    lutadores.clear()
    lutadores.extend([
        Lutador3D(CANDIDATOS[idx1], ACESSORIOS[ac1], -4, P1_KEYS, color.azure, 1),
        Lutador3D(CANDIDATOS[idx2], ACESSORIOS[ac2], 4, P2_KEYS, color.red, -1)
    ])
    atualizar_hud()

def atualizar_hud():
    global last_hud_state
    limpar_interface()
    if len(lutadores) != 2:
        return
    adicionar_texto(f'{CANDIDATOS[idx1]["nome"]} | HP: {lutadores[0].vida} | ROUNDS: {vitorias1}',
                    (-.86,.45), .8, color.azure)
    adicionar_texto(f'{CANDIDATOS[idx2]["nome"]} | HP: {lutadores[1].vida} | ROUNDS: {vitorias2}',
                    (.25,.45), .8, color.red)
    desenhar_painel_controles(ui)
    adicionar_texto("F11: tela cheia | ESC: menu",(-.18,-.49),.65,color.gold)
    last_hud_state = (lutadores[0].vida,lutadores[1].vida,vitorias1,vitorias2)

def processar_ataque(tecla):
    if len(lutadores) != 2:
        return
    mapa = {"f":(0,"soco"), "g":(0,"chute"), "k":(1,"soco"), "l":(1,"chute")}
    if tecla not in mapa:
        return
    indice, tipo = mapa[tecla]
    atacante = lutadores[indice]
    defensor = lutadores[1-indice]
    if atacante.cooldown > 0:
        return
    atacante.cooldown = .48 if tipo == "soco" else .68
    atacante.atacando = True
    atacante.tempo_ataque = .22
    atacante.braco1.rotation_z = -70 * atacante.direcao
    resolver_ataque(atacante, defensor, tipo)

def finalizar_luta():
    global estado
    vencedor = CANDIDATOS[idx1 if vitorias1 >= 2 else idx2]["nome"]
    estado = "fim"
    limpar_interface()
    adicionar_texto("ELEIÇÕES ENCERRADAS!",(-.3,.15),1.5,color.gold)
    adicionar_texto(f"VENCEDOR: {vencedor.upper()}!",(-.32,.03),1.1,color.lime)
    adicionar_botao("VOLTAR AO MENU",(0,-.15),criar_menu,(.3,.07))

def atualizar():
    global vitorias1, vitorias2, estado, last_hud_state
    if estado != "luta" or len(lutadores) != 2:
        return
    p1,p2 = lutadores
    p1.mover()
    p2.mover()
    if p1.vida <= 0 or p2.vida <= 0:
        if p1.vida <= 0: vitorias2 += 1
        else: vitorias1 += 1
        if vitorias1 >= 2 or vitorias2 >= 2:
            finalizar_luta()
        else:
            criar_round()
        return
    hud_state = (p1.vida,p2.vida,vitorias1,vitorias2)
    if hud_state != last_hud_state:
        atualizar_hud()

def processar_input(tecla):
    if tecla == "f11":
        window.fullscreen = not window.fullscreen
    if estado == "menu":
        if tecla == "enter": iniciar_luta()
        elif tecla == "r":
            random.shuffle(CANDIDATOS)
            selecionar()
        elif tecla == "a": selecionar(-1,0,0)
        elif tecla == "d": selecionar(1,0,0)
        elif tecla == "w": selecionar(0,0,-1)
        elif tecla == "s": selecionar(0,0,1)
        elif tecla == "left arrow": selecionar(0,-1,0)
        elif tecla == "right arrow": selecionar(0,1,0)
        elif tecla == "up arrow": selecionar(0,0,-2)
        elif tecla == "down arrow": selecionar(0,0,2)
    elif estado in ("luta","fim"):
        if tecla == "escape":
            criar_menu()
        elif estado == "luta":
            processar_ataque(tecla)

class ControladorJogo(Entity):
    def update(self):
        atualizar()

    def input(self, key):
        # Ursina envia eventos de soltura como "tecla up"; só processamos key-down.
        if not key.endswith(" up"):
            processar_input(key)

controlador_jogo = ControladorJogo()
criar_menu()

def iniciar_aplicacao():
    app.run()
