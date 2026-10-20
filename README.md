# Eleições Fighting Game — 3D

Jogo de luta local para dois jogadores, desenvolvido em Python com o motor **Ursina**. Os personagens, a arena, a iluminação, os acessórios e a interface são renderizados em 3D.

## Requisitos
- Python 3.10 ou superior (recomendado).
- Dependências listadas em `requirements.txt`.

## Instalação
Abra o terminal na pasta do projeto e execute:

```bash
python -m pip install -r requirements.txt
python main.py
```

No Windows, se `python` não funcionar, tente `py -m pip install -r requirements.txt` e depois `py main.py`.

## Controles
- **Jogador 1:** W/A/S/D para mover; F para soco; G para chute.
- **Jogador 2:** setas para mover; K para soco; L para chute.
- **Menu:** A/D escolhem o candidato do jogador 1; W/S escolhem seu acessório; esquerda/direita escolhem o candidato do jogador 2; cima/baixo escolhem seu acessório.
- **Enter:** iniciar; **R:** embaralhar candidatos; **F11:** tela cheia; **Esc:** voltar ao menu durante a luta.

A partida é melhor de três rounds. Os módulos `personagem.py`, `colisao.py` e `menu.py` separam os personagens, a lógica de combate e os componentes da interface.
