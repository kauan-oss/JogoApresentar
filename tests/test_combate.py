"""Testes sem dependencias graficas para regras de combate."""
import unittest
from types import SimpleNamespace
from colisao import pode_acertar, verificar_ataque_e_colisao, separar_lutadores


class Simulador:
    def __init__(self, x, z, direcao, lado):
        self.root = SimpleNamespace(x=x, z=z)
        self.direcao = direcao
        self.lado = lado
        self.vida = 100
        self.forca = 12
        self.ataque = None
        self.ataque_tempo = 0.0
        self.ja_atingiu = False

    @property
    def x(self):
        return self.root.x

    @property
    def z(self):
        return self.root.z

    def receber_golpe(self, dano, direcao):
        self.vida -= dano


class TesteCombate(unittest.TestCase):
    def setUp(self):
        self.p1 = Simulador(0, 0, 1, 1)
        self.p2 = Simulador(1.2, 0, -1, 2)

    def test_soco_frontal_uma_unica_vez(self):
        self.p1.ataque = "soco"
        self.p1.ataque_tempo = .22
        self.assertTrue(pode_acertar(self.p1, self.p2))
        self.assertEqual(len(verificar_ataque_e_colisao(self.p1, self.p2)), 1)
        self.assertEqual(self.p2.vida, 88)
        self.assertEqual(verificar_ataque_e_colisao(self.p1, self.p2), [])

    def test_ataque_fora_da_janela_nao_acerta(self):
        self.p1.ataque = "soco"
        self.p1.ataque_tempo = .01
        self.assertFalse(pode_acertar(self.p1, self.p2))

    def test_oponente_atras_nao_acerta(self):
        self.p1.ataque = "soco"
        self.p1.ataque_tempo = .20
        self.p1.direcao = -1
        self.assertFalse(pode_acertar(self.p1, self.p2))

    def test_diferenca_lateral_impede_hit(self):
        self.p1.ataque = "chute"
        self.p1.ataque_tempo = .28
        self.p2.root.z = 1.2
        self.assertFalse(pode_acertar(self.p1, self.p2))

    def test_lutadores_nao_podem_ficar_sobrepostos(self):
        self.p1.root.x = self.p2.root.x = 0.0
        separar_lutadores(self.p1, self.p2)
        self.assertGreaterEqual(abs(self.p1.x - self.p2.x), .789)


if __name__ == "__main__":
    unittest.main()
