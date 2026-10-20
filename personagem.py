import pygame
import math
import random

ACESSORIOS = [
    {"nome": "Nenhum", "cor": None},
    {"nome": "Óculos Escuros", "cor": (15, 15, 15)},
    {"nome": "Faixa Presidencial", "cor": (255, 215, 0)},
    {"nome": "Gravata Borboleta", "cor": (220, 20, 20)},
    {"nome": "Chapéu Político", "cor": (40, 40, 50)},
]

TONS_PELE = [(240, 194, 142), (255, 220, 177), (198, 134, 66), (140, 85, 39)]
CORES_TERNO = [(25, 25, 30), (15, 40, 110), (240, 210, 30), (30, 45, 80), (20, 35, 90), (25, 35, 65)]
CORES_CABELO = [(30, 25, 20), (235, 235, 235), (200, 200, 200), (160, 160, 165)]

def checar_tecla(teclas, controle):
    """Verifica de forma segura se uma tecla individual ou lista de teclas está pressionada"""
    if controle is None:
        return False
    if isinstance(controle, (list, tuple, set)):
        for k in controle:
            try:
                if teclas[k]:
                    return True
            except (IndexError, KeyError, TypeError):
                pass
        return False
    try:
        return bool(teclas[controle])
    except (IndexError, KeyError, TypeError):
        return False

def gerar_candidato_aleatorio(id_num):
    nomes = ["Senador", "Ministro", "Governador", "Deputado", "Prefeito", "Embaixador"]
    sobrenomes = ["Silva", "Santos", "Oliveira", "Souza", "Pereira", "Lima", "Ferreira", "Costa"]
    nome_gerado = f"{random.choice(nomes)} {random.choice(sobrenomes)}"
    
    return {
        "nome": nome_gerado,
        "cor_terno": random.choice(CORES_TERNO),
        "cor_camiseta": random.choice([(10, 10, 10), (240, 240, 240)]),
        "cor_calca": random.choice([(110, 150, 200), (30, 30, 35), (15, 40, 110)]),
        "cor_pele": random.choice(TONS_PELE),
        "cor_cabelo": random.choice(CORES_CABELO),
        "estilo_cabelo": random.choice(["social", "grisalho", "topete", "calvo", "curto", "despojado"]),
        "velocidade": round(random.uniform(5.5, 8.5), 1),
        "forca": random.randint(8, 16),
        "imagem_path": None
    }

def gerar_candidatos_padrao():
    return [
        {
            "nome": "Renan Santos", 
            "cor_terno": (25, 25, 30),
            "cor_camiseta": (10, 10, 10),
            "cor_calca": (110, 150, 200),
            "cor_pele": TONS_PELE[0], 
            "cor_cabelo": (30, 25, 20), 
            "estilo_cabelo": "despojado", 
            "velocidade": 8.0, 
            "forca": 14,
            # "imagem_path": "assets/candidato_renan.png"
        },
        {
            "nome": "Lula", 
            "cor_terno": (15, 40, 110),
            "cor_camiseta": (240, 240, 240),
            "cor_calca": (15, 40, 110),
            "cor_pele": TONS_PELE[0], 
            "cor_cabelo": (235, 235, 235),
            "estilo_cabelo": "grisalho", 
            "velocidade": 6.8, 
            "forca": 13,
            # "imagem_path": "assets/candidato_lula.png"
        },
        {
            "nome": "Flávio", 
            "cor_terno": (240, 210, 30),
            "cor_camiseta": (240, 210, 30), 
            "cor_calca": (110, 150, 200),
            "cor_pele": TONS_PELE[0], 
            "cor_cabelo": (35, 25, 20), 
            "estilo_cabelo": "social", 
            "velocidade": 7.6, 
            "forca": 12,
            # "imagem_path": "assets/candidato_flavio.png"
        },
        {
            "nome": "Augusto Cury", 
            "cor_terno": (30, 45, 80),
            "cor_camiseta": (180, 210, 240),
            "cor_calca": (50, 50, 55),
            "cor_pele": TONS_PELE[0], 
            "cor_cabelo": (40, 35, 30), 
            "estilo_cabelo": "social", 
            "velocidade": 6.2, 
            "forca": 11,
            # "imagem_path": "assets/candidato_cury.png"
        },
        {
            "nome": "Caiado", 
            "cor_terno": (20, 35, 90),
            "cor_camiseta": (240, 240, 240),
            "cor_calca": (20, 35, 90),
            "cor_pele": TONS_PELE[0], 
            "cor_cabelo": (210, 210, 210),
            "estilo_cabelo": "grisalho", 
            "velocidade": 7.0, 
            "forca": 14,
            # "imagem_path": "assets/candidato_caiado.png"
        },
        {
            "nome": "Zema", 
            "cor_terno": (25, 35, 65),
            "cor_camiseta": (25, 35, 65), 
            "cor_calca": (40, 40, 50),
            "cor_pele": TONS_PELE[0], 
            "cor_cabelo": (170, 170, 175),
            "estilo_cabelo": "curto", 
            "velocidade": 7.8, 
            "forca": 10,
            # "imagem_path": "assets/candidato_zema.png"
        },
    ]

gerar_candidato_padrao = gerar_candidatos_padrao
PERSONAGENS_BASE = gerar_candidatos_padrao()

class Lutador:
    def __init__(self, x, y, controles, dados, acessorio, virado_direita):
        self.x = float(x)
        self.y = float(y)
        self.vx = 0.0
        self.vy = 0.0
        
        self.largura_base = 70
        self.altura_base = 140
        self.rect = pygame.Rect(self.x, self.y, self.largura_base, self.altura_base)
        
        self.nome = dados.get("nome", "Candidato")
        self.cor_terno = dados.get("cor_terno", (30, 30, 30))
        self.cor_camiseta = dados.get("cor_camiseta", (240, 240, 240))
        self.cor_calca = dados.get("cor_calca", (20, 20, 25))
        self.cor_pele = dados.get("cor_pele", TONS_PELE[0])
        self.cor_cabelo = dados.get("cor_cabelo", (30, 30, 30))
        self.estilo_cabelo = dados.get("estilo_cabelo", "social")
        self.velocidade_max = dados.get("velocidade", 7.0)
        self.forca = dados.get("forca", 10)
        self.acessorio = acessorio
        
        self.atacando = False
        self.tipo_ataque = None
        self.ja_causou_dano = False
        self.vida = 100
        self.controles = controles
        self.virado_direita = virado_direita
        self.cooldown_ataque = 0
        self.escala = 1.0
        
        # Variáveis do texto flutuante de impacto
        self.texto_impacto = ""
        self.tempo_texto_impacto = 0
        
        self.imagem_sprite = None
        if dados.get("imagem_path"):
            try:
                img = pygame.image.load(dados["imagem_path"]).convert_alpha()
                self.imagem_sprite = img
            except:
                self.imagem_sprite = None

        self.tempo_andando = 0.0
        self.tempo_idle = 0.0
        self.tempo_hit = 0
        self.progresso_ataque = 0.0

    def atualizar_escala(self, y_min, y_max):
        fator = (self.y - y_min) / max(1, (y_max - y_min))
        self.escala = 0.65 + (fator * 0.45)
        
        self.rect.width = int(self.largura_base * self.escala)
        self.rect.height = int(self.altura_base * self.escala)
        self.rect.x = int(self.x)
        self.rect.y = int(self.y)

    def mover(self, y_min, y_max):
        ACELERACAO = 1.3
        FRICCAO = 0.80
        
        ax, ay = 0.0, 0.0
        teclas = pygame.key.get_pressed()

        if checar_tecla(teclas, self.controles.get('esquerda')):
            ax -= ACELERACAO
            self.virado_direita = False
        if checar_tecla(teclas, self.controles.get('direita')):
            ax += ACELERACAO
            self.virado_direita = True
        if checar_tecla(teclas, self.controles.get('cima')):
            ay -= ACELERACAO * 0.6
        if checar_tecla(teclas, self.controles.get('baixo')):
            ay += ACELERACAO * 0.6

        self.vx = (self.vx + ax) * FRICCAO
        self.vy = (self.vy + ay) * FRICCAO

        v_total = math.hypot(self.vx, self.vy)
        if v_total > self.velocidade_max:
            fator = self.velocidade_max / v_total
            self.vx *= fator
            self.vy *= fator

        self.x += self.vx
        self.y += self.vy

        self.y = max(y_min, min(y_max - self.rect.height, self.y))

        soco_pressionado = checar_tecla(teclas, self.controles.get('soco'))
        chute_pressionado = checar_tecla(teclas, self.controles.get('chute'))

        if soco_pressionado and self.cooldown_ataque == 0:
            self.atacando = True
            self.tipo_ataque = "soco"
            self.cooldown_ataque = 24
            self.ja_causou_dano = False
            self.progresso_ataque = 1.0

        elif chute_pressionado and self.cooldown_ataque == 0:
            self.atacando = True
            self.tipo_ataque = "chute"
            self.cooldown_ataque = 30
            self.ja_causou_dano = False
            self.progresso_ataque = 1.0

        if self.cooldown_ataque > 0:
            self.cooldown_ataque -= 1
            self.progresso_ataque = self.cooldown_ataque / (24.0 if self.tipo_ataque == "soco" else 30.0)
        else:
            self.atacando = False
            self.tipo_ataque = None

        if self.tempo_hit > 0:
            self.tempo_hit -= 1

        if abs(self.vx) > 0.3 or abs(self.vy) > 0.3:
            self.tempo_andando += 0.2
        else:
            self.tempo_andando = 0.0
            
        self.tempo_idle += 0.05
        self.atualizar_escala(y_min, y_max)

    def desenhar(self, tela):
        e = self.escala
        cx = self.rect.centerx
        cy = int(self.y + self.altura_base * e)
        top_y = self.rect.y
        dir_frente = 1 if self.virado_direita else -1
        
        # 1. Sombra 3D
        sombra_w = int(self.rect.width * 0.9)
        sombra_h = int(14 * e)
        sombra_surf = pygame.Surface((sombra_w, sombra_h), pygame.SRCALPHA)
        pygame.draw.ellipse(sombra_surf, (0, 0, 0, 110), (0, 0, sombra_w, sombra_h))
        tela.blit(sombra_surf, (cx - sombra_w // 2, cy - sombra_h // 2))

        if self.imagem_sprite:
            img_scaled = pygame.transform.scale(self.imagem_sprite, (self.rect.width, self.rect.height))
            if not self.virado_direita:
                img_scaled = pygame.transform.flip(img_scaled, True, False)
            tela.blit(img_scaled, (self.rect.x, top_y))
        else:
            cor_terno = (255, 80, 80) if self.tempo_hit > 0 and self.tempo_hit % 4 < 2 else self.cor_terno
            bobbing = math.sin(self.tempo_idle) * 3 * e

            # 2. Pernas
            y_quadril = top_y + int(85 * e + bobbing)
            larg_perna = int(12 * e)
            alt_perna = int(45 * e)

            if self.atacando and self.tipo_ataque == "chute":
                extensao = math.sin((1.0 - self.progresso_ataque) * math.pi)
                pygame.draw.line(tela, self.cor_calca, (cx - dir_frente * int(10 * e), y_quadril), (cx - dir_frente * int(10 * e), y_quadril + alt_perna), larg_perna)
                pygame.draw.circle(tela, (15, 15, 20), (cx - dir_frente * int(10 * e), y_quadril + alt_perna), int(7 * e))

                chute_x = cx + dir_frente * int((20 + extensao * 50) * e)
                chute_y = y_quadril + int(10 * e) - int(extensao * 15 * e)
                pygame.draw.line(tela, self.cor_calca, (cx, y_quadril), (chute_x, chute_y), int(14 * e))
                pygame.draw.circle(tela, (15, 15, 20), (int(chute_x), int(chute_y)), int(9 * e))
            else:
                angulo_perna = math.sin(self.tempo_andando) * 25
                for i, mult in enumerate([-1, 1]):
                    ang = math.radians(angulo_perna * mult if abs(self.vx) > 0.3 or abs(self.vy) > 0.3 else 0)
                    px_fim = cx + mult * int(12 * e) + math.sin(ang) * alt_perna
                    py_fim = y_quadril + math.cos(ang) * alt_perna
                    pygame.draw.line(tela, self.cor_calca, (cx + mult * int(10 * e), y_quadril), (px_fim, py_fim), larg_perna)
                    pygame.draw.circle(tela, (15, 15, 20), (int(px_fim), int(py_fim)), int(7 * e))

            # 3. Tronco
            tronco_rect = pygame.Rect(cx - int(22 * e), top_y + int(40 * e + bobbing), int(44 * e), int(50 * e))
            pygame.draw.rect(tela, cor_terno, tronco_rect, border_radius=int(6 * e))
            pygame.draw.rect(tela, self.cor_camiseta, (cx - int(10 * e), top_y + int(42 * e + bobbing), int(20 * e), int(46 * e)))

            if self.nome == "Zema":
                pygame.draw.rect(tela, (240, 110, 20), (cx - int(12 * e), top_y + int(40 * e + bobbing), int(24 * e), int(5 * e)))
            elif self.nome in ["Lula", "Caiado"]:
                pt1 = (cx - int(18 * e), top_y + int(42 * e + bobbing))
                pt2 = (cx + int(18 * e), top_y + int(85 * e + bobbing))
                pygame.draw.line(tela, (20, 160, 40), pt1, pt2, max(4, int(9 * e)))
                pygame.draw.line(tela, (255, 215, 0), pt1, pt2, max(2, int(4 * e)))

            # Broches e Números
            numeros = {"Renan Santos": "R14", "Lula": "13", "Flávio": "22", "Augusto Cury": "70", "Caiado": "55", "Zema": "30"}
            if self.nome in numeros:
                texto_numero = numeros[self.nome]
                pos_badge_x = cx - int(14 * e) if self.virado_direita else cx + int(6 * e)
                pos_badge_y = top_y + int(54 * e + bobbing)

                cor_fundo_badge = (255, 215, 0)
                cor_texto = (0, 0, 0)
                if self.nome == "Lula":
                    cor_fundo_badge = (210, 30, 30)
                    cor_texto = (255, 255, 255)
                elif self.nome == "Flávio":
                    cor_fundo_badge = (20, 20, 25)
                    cor_texto = (255, 215, 0)

                pygame.draw.circle(tela, cor_fundo_badge, (pos_badge_x, pos_badge_y), int(8 * e))
                fonte_badge = pygame.font.SysFont('Arial', max(7, int(9 * e)), bold=True)
                txt_num = fonte_badge.render(texto_numero, True, cor_texto)
                tela.blit(txt_num, (pos_badge_x - txt_num.get_width() // 2, pos_badge_y - txt_num.get_height() // 2))

            # 4. Cabeça
            raio_cabeca = int(18 * e)
            centro_cabeca = (cx, top_y + int(24 * e + bobbing))
            pygame.draw.circle(tela, self.cor_pele, centro_cabeca, raio_cabeca)

            if self.nome == "Lula":
                pygame.draw.arc(tela, self.cor_cabelo, (cx - raio_cabeca, centro_cabeca[1] - int(4*e), raio_cabeca * 2, raio_cabeca * 2), math.pi, 2 * math.pi, int(10 * e))

            if self.estilo_cabelo != "calvo":
                pygame.draw.arc(tela, self.cor_cabelo, (cx - raio_cabeca - 2, centro_cabeca[1] - raio_cabeca - int(3*e), raio_cabeca * 2 + 4, raio_cabeca * 2), 0, math.pi + 0.5, int(11 * e))

            if self.nome in ["Augusto Cury", "Zema", "Renan Santos"]:
                ox = cx + int(dir_frente * 3 * e)
                oy = centro_cabeca[1] - int(2 * e)
                cor_oculos = (15, 15, 15) if self.nome == "Renan Santos" else (50, 50, 60)
                pygame.draw.rect(tela, cor_oculos, (ox - int(12 * e), oy - int(4 * e), int(22 * e), int(9 * e)), border_radius=2)
            else:
                dir_x = 4 * e if self.virado_direita else -4 * e
                pygame.draw.circle(tela, (20, 20, 20), (int(cx + dir_x), int(centro_cabeca[1] - 2 * e)), max(1, int(3 * e)))

            # 5. Braços
            y_ombro = top_y + int(48 * e + bobbing)

            if self.atacando and self.tipo_ataque == "soco":
                extensao = math.sin((1.0 - self.progresso_ataque) * math.pi)
                mao_x = cx + dir_frente * int((20 + extensao * 55) * e)
                mao_y = y_ombro + int(5 * e)

                pygame.draw.line(tela, cor_terno, (cx, y_ombro), (mao_x, mao_y), int(14 * e))
                pygame.draw.circle(tela, self.cor_pele, (int(mao_x), int(mao_y)), int(11 * e))
                pygame.draw.circle(tela, (255, 215, 0), (int(mao_x), int(mao_y)), int(6 * e), width=2)
            else:
                pygame.draw.line(tela, cor_terno, (cx - int(12 * e), y_ombro), (cx + dir_frente * int(15 * e), y_ombro + int(20 * e)), int(10 * e))

            # Acessórios
            if self.acessorio["nome"] == "Óculos Escuros":
                ox = cx + int(dir_frente * 3 * e)
                oy = centro_cabeca[1] - int(2 * e)
                pygame.draw.rect(tela, (15, 15, 15), (ox - int(12 * e), oy - int(4 * e), int(22 * e), int(9 * e)), border_radius=2)
            elif self.acessorio["nome"] == "Faixa Presidencial":
                pt1 = (cx - int(18 * e), top_y + int(42 * e + bobbing))
                pt2 = (cx + int(18 * e), top_y + int(85 * e + bobbing))
                pygame.draw.line(tela, (20, 160, 40), pt1, pt2, max(4, int(9 * e)))
                pygame.draw.line(tela, (255, 215, 0), pt1, pt2, max(2, int(4 * e)))
            elif self.acessorio["nome"] == "Gravata Borboleta":
                gy = top_y + int(44 * e + bobbing)
                pygame.draw.polygon(tela, (220, 20, 20), [(cx, gy), (cx - int(10 * e), gy - int(6 * e)), (cx - int(10 * e), gy + int(6 * e))])
                pygame.draw.polygon(tela, (220, 20, 20), [(cx, gy), (cx + int(10 * e), gy - int(6 * e)), (cx + int(10 * e), gy + int(6 * e))])
                pygame.draw.circle(tela, (180, 10, 10), (cx, gy), int(3 * e))
            elif self.acessorio["nome"] == "Chapéu Político":
                hy = centro_cabeca[1] - raio_cabeca - int(4 * e)
                pygame.draw.rect(tela, (40, 40, 50), (cx - int(22 * e), hy, int(44 * e), int(8 * e)))
                pygame.draw.rect(tela, (40, 40, 50), (cx - int(14 * e), hy - int(12 * e), int(28 * e), int(14 * e)))

        # Renderização do Texto Flutuante de Impacto acima do personagem
        if self.tempo_texto_impacto > 0:
            self.tempo_texto_impacto -= 1
            fonte_impacto = pygame.font.SysFont('Arial', max(14, int(22 * e)), bold=True)
            
            # Texto amarelo com borda preta para contraste
            txt_sombra = fonte_impacto.render(self.texto_impacto, True, (0, 0, 0))
            txt_surf = fonte_impacto.render(self.texto_impacto, True, (255, 230, 0))
            
            subida_y = (25 - self.tempo_texto_impacto) * 1.5
            pos_x = cx - txt_surf.get_width() // 2
            pos_y = top_y - int(30 * e) - int(subida_y)

            tela.blit(txt_sombra, (pos_x + 2, pos_y + 2))
            tela.blit(txt_surf, (pos_x, pos_y))