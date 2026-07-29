from cardapio import Cardapio
from restaurante import Restaurante
from menu import menu_principal
from constants import BOAS_VINDAS

# TO-DO NEXT: APRIMORAR AS CLASSES EXISTENTES E SEUS ESTADOS | Ex: Classe PEDIDO

def main() -> None:
    cardapio = Cardapio()
    restaurante = Restaurante(cardapio)

    print(BOAS_VINDAS)

    running = True
    while running:
        running = menu_principal(restaurante, cardapio)


if __name__ == "__main__":
    main()