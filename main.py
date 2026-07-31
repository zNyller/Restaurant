from cardapio import Cardapio
from restaurante import Restaurante
from menu import menu_principal
from constants import BOAS_VINDAS

""" TO-DO NEXT: RESTAURANTE coordenar os acontecimentos do turno.

Ex:
while self.aberto:
    self.talvez_chegue_cliente()  FEITO ✅

    self.proximo_turno()  FEITO ✅

    self.acomodar_clientes()  FEITO ✅

    self.coletar_pedidos()  FEITO ✅

    self.entregar_pedidos()  FEITO ✅

    self.finalizar_atendimentos()

    self.encerrar()
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