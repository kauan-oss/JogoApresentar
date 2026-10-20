"""Renderiza o jogo num display virtual e valida cores de cena e lutadores."""
from panda3d.core import Filename
from ursina import Ursina, Vec3, camera, application, color
from main import Partida


def checar_rgba(nome, cor):
    assert all(0.0 <= canal <= 1.0 for canal in cor), (nome, tuple(cor))
    assert cor[3] > .1, (nome, tuple(cor))


def main():
    app = Ursina(title="Ursina smoke", size=(960, 540),
                 development_mode=False, vsync=False)
    camera.position = Vec3(0, 7.8, -20.5)
    camera.look_at(Vec3(0, 1.35, .35))
    camera.fov = 48
    p = Partida()
    assert p.estado == "menu"
    assert p.p1.root is not None and p.p2.root is not None

    # "color.rgb(255, 0, 0)" era um bug: Ursina espera 0-1 em rgb,
    # portanto tudo era convertido para branco. Em rgb32, 8-bit e correto.
    palco = [filho.color for filho in p.arena.root.children if hasattr(filho, "model") and filho.model]
    assert len(palco) > 25, len(palco)
    checar_rgba("terno P1", p.p1.cor_roupa)
    checar_rgba("terno P2", p.p2.cor_roupa)
    checar_rgba("pele", p.p1.cor_pele)
    for i, tinta in enumerate(palco):
        checar_rgba(f"arena {i}", tinta)

    assert p.p1.cor_roupa == color.rgb32(32, 35, 44)
    assert p.p2.cor_roupa == color.rgb32(24, 65, 133)
    assert sum(c[0] < .5 and c[1] < .6 for c in palco) > 20

    p.escolher("d")
    p.escolher("up arrow")
    p.iniciar()
    assert p.estado == "jogo"
    assert p.p1.vida == 100 and p.p2.vida == 100
    assert p.p1.iniciar_ataque("soco")
    for _ in range(6):
        app.step()

    # Validacao da imagem real, em vez de apenas checar imports.
    screenshot = app.win.getScreenshot()
    assert screenshot is not None
    largura, altura = screenshot.getXSize(), screenshot.getYSize()
    pontos = [screenshot.getXel(x, y)
              for y in range(25, altura - 25, 32)
              for x in range(25, largura - 25, 32)]
    claros = sum(1 for c in pontos if min(c[0], c[1], c[2]) > .91)
    assert claros / len(pontos) < .45, f"Imagem esbranquiçada: {claros}/{len(pontos)}"
    screenshot.write(Filename("preview-ursina.png"))

    p.exibir_menu()
    assert p.estado == "menu"
    application.quit()
    print(f"CORES 3D OK: {len(palco)} entidades, {claros}/{len(pontos)} pixels quase brancos")
    print("SMOKE 3D OK")


if __name__ == "__main__":
    main()
