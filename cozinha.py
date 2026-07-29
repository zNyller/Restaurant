from time import sleep
from pedido import Pedido

class Cozinha:
    def __init__(self):
        pass


    def preparar_prato(self, pedido: Pedido):
        """Prepara o prato de acordo com suas características."""
        pedido.preparando()
        print(f"Preparando {pedido.prato.nome}...")
        sleep(1)
        print("Misturando ingredientes...")
        tempo_preparo = pedido.prato.tempo / 10
        sleep(tempo_preparo)
        pedido.finalizar()
        print("Pedido finalizado!")