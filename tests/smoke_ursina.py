"""Smoke test do motor, executado no display virtual do CI."""
from ursina import Ursina, application
from main import Partida


def main():
    app = Ursina(title="Ursina smoke", size=(960, 540),
                 development_mode=False, vsync=False)
    p = Partida()
    assert p.estado == "menu"
    assert p.p1.root is not None and p.p2.root is not None
    p.escolher("d")
    p.escolher("up arrow")
    p.iniciar()
    assert p.estado == "jogo"
    assert p.p1.vida == 100 and p.p2.vida == 100
    assert p.p1.iniciar_ataque("soco")
    for _ in range(3):
        app.step()
    p.exibir_menu()
    assert p.estado == "menu"
    application.quit()
    print("SMOKE 3D OK")


if __name__ == "__main__":
    main()
