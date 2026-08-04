from cardapio import Cardapio
from restaurante import Restaurante
from menu import menu_principal
from constants import BOAS_VINDAS

""" TO-DO NEXT:

- Refinar comunicação entre objetos (eventos, notificações, etc.).
- Adicionar filas de execução para os objetos (pedidos, estados, etc.)

"""

def main() -> None:
    cardapio = Cardapio()
    restaurante = Restaurante(cardapio)

    print(BOAS_VINDAS)

    running = True
    while running:
        running = menu_principal(restaurante, cardapio)


if __name__ == "__main__":
    main()