"""Componentes de interface feitos com Ursina; não utiliza Pygame."""
from ursina import Button, Text, destroy, color

def limpar_ui(elementos):
    for elemento in elementos[:]:
        destroy(elemento)
    elementos.clear()

def texto(conteudo, pos, escala=1, cor=color.white, elementos=None, **kwargs):
    elemento = Text(conteudo, position=pos, scale=escala, color=cor, **kwargs)
    if elementos is not None:
        elementos.append(elemento)
    return elemento

def botao(conteudo, pos, acao, elementos=None, escala=(.28,.065), cor=color.rgb(45,55,78)):
    elemento = Button(text=conteudo, position=pos, scale=escala, color=cor,
                      highlight_color=color.azure, pressed_color=color.gold, on_click=acao)
    if elementos is not None:
        elementos.append(elemento)
    return elemento

def desenhar_painel_controles(elementos=None):
    """Adiciona instruções de controles à interface 3D."""
    return texto("P1: WASD + F soco + G chute   |   P2: Setas + K soco + L chute",
                 (-.48,-.46), .75, elementos=elementos)
