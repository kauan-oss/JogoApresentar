"""Arena parlamentar estilizada, com arquitetura e piso realmente tridimensionais."""
from __future__ import annotations

import math
from ursina import Entity, Mesh, Sky, AmbientLight, DirectionalLight, Vec3, color


def arco_horizontal(raio_x, raio_z, y, largura=.065, segmentos=80, cor=None, pai=None):
    """Malha anelar horizontal, sem depender de arquivos .obj externos."""
    vertices = []
    triangulos = []
    for i in range(segmentos + 1):
        a = 2 * math.pi * i / segmentos
        c, s = math.cos(a), math.sin(a)
        vertices.extend([
            (c * (raio_x - largura), y, s * (raio_z - largura)),
            (c * (raio_x + largura), y, s * (raio_z + largura)),
        ])
    for i in range(segmentos):
        j = i * 2
        triangulos.extend([(j, j + 2, j + 1), (j + 1, j + 2, j + 3)])
    return Entity(parent=pai, model=Mesh(vertices=vertices, triangles=triangulos),
                  color=cor or color.white, double_sided=True)


class Arena:
    def __init__(self):
        self.root = Entity()
        Sky(color=color.rgb(12, 23, 47))
        AmbientLight(color=color.rgb(100, 111, 142))
        sol = DirectionalLight()
        sol.look_at(Vec3(1, -3, -2))

        self.bloco((0, -1.38, 0), (65, 1.8, 55), (12, 22, 42))
        # Base eliptica em camadas. A superficie final coincide com y=0.
        self.cilindro((0, -.68, 0), (23.2, .78, 12.8), (22, 38, 65))
        self.cilindro((0, -.36, 0), (22.2, .52, 11.9), (46, 63, 86))
        self.cilindro((0, -.17, 0), (21.2, .34, 11.2), (63, 78, 96))
        self.cilindro((0, -.09, 0), (20.4, .19, 10.7), (35, 48, 73))

        arco_horizontal(9.9, 5.1, .045, .065, cor=color.rgb(255, 197, 75), pai=self.root)
        arco_horizontal(9.45, 4.65, .047, .025, cor=color.rgb(56, 199, 208), pai=self.root)
        arco_horizontal(7.7, 3.58, .05, .018, cor=color.rgb(85, 132, 172), pai=self.root)
        for i in range(13):
            x = (i - 6) * 1.22
            self.bloco((x, .045, 0), (.025, .013, 7.1), (45, 68, 100))
        for z in (-2.5, -1.25, 0, 1.25, 2.5):
            self.bloco((0, .047, z), (15.3, .013, .025), (43, 70, 103))

        # Arquibancadas, colunas e passarela externa.
        for i in range(13):
            a = math.pi * .15 + math.pi * .70 * i / 12
            x = math.cos(a) * 12.5
            z = math.sin(a) * 7.5 + 2.0
            self.bloco((x, -.28, z), (2.0, .50, 1.8), (34, 49, 80),
                       rotation_y=math.degrees(a) - 90)
            self.bloco((x, .17, z), (2.0, .28, 1.6), (50, 68, 94),
                       rotation_y=math.degrees(a) - 90)
        for x in (-11.5, -8.8, 8.8, 11.5):
            self.cilindro((x, 1.90, 6.7), (.72, 3.5, .72), (101, 118, 145))
            self.cilindro((x, 3.68, 6.7), (1.05, .27, 1.05), (196, 171, 107))
            self.cilindro((x, .21, 6.7), (1.12, .30, 1.12), (90, 104, 129))
        self.bloco((0, 4.0, 7.0), (28, .48, .55), (89, 105, 135))
        self.bloco((0, 5.4, 8.1), (32, 2.1, .50), (25, 43, 74))
        self.bloco((0, 4.93, 7.76), (21.0, .10, .13), (228, 181, 76))
        self.bloco((0, 5.85, 7.76), (17.0, .08, .13), (42, 168, 187))

        # Bandeiras e globos metalicos decorativos nas extremidades.
        for sx in (-1, 1):
            x = sx * 9.85
            self.cilindro((x, 1.8, 4.7), (.10, 3.6, .10), (181, 190, 199))
            Entity(parent=self.root, model="sphere", position=(x, 3.70, 4.7),
                   scale=.22, color=color.rgb(249, 210, 75))
            self.bloco((x + sx * .55, 2.90, 4.7), (1.02, .64, .07), (29, 139, 71))
            self.bloco((x + sx * .55, 2.90, 4.61), (.58, .34, .06), (231, 198, 64))
            self.cilindro((x, .78, -4.3), (.55, 1.55, .55), (40, 62, 99))
            Entity(parent=self.root, model="sphere", position=(x, 1.7, -4.3),
                   scale=.70, color=color.rgb(97, 205, 217))

        for x in (-6.8, 6.8):
            # Focos de luz sobre as entradas da arena.
            self.cilindro((x, .63, 5.0), (.61, 1.26, .61), (30, 52, 85))
            Entity(parent=self.root, model="sphere", position=(x, 1.36, 5.0),
                   scale=(.63, .20, .63), color=color.rgb(246, 194, 89))

    def bloco(self, pos, escala, rgb, **kwargs):
        return Entity(parent=self.root, model="cube", position=pos,
                      scale=escala, color=color.rgb(*rgb), **kwargs)

    def cilindro(self, pos, escala, rgb):
        return Entity(parent=self.root, model="cylinder", position=pos,
                      scale=escala, color=color.rgb(*rgb))
