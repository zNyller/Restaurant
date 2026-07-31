from cardapio import Cardapio
from restaurante import Restaurante
from menu import menu_principal
from constants import BOAS_VINDAS

""" TO-DO NEXT:

- Cliente decidir suas próprias ações com base no seu estado.

- Mesa assume mais responsabilidades relacionadas à própria ocupação.

- Restaurante passa a apenas coordenar os sistemas.

- Remover chamadas duplicadas e estados intermediários desnecessários.

- Refinar comunicação entre objetos (eventos, notificações, etc.).

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