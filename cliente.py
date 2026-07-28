from cardapio import Cardapio

class Cliente:
    def __init__(self, nome):
        self.nome = nome


    def fazer_pedido(self, cardapio: Cardapio):
        pedido = cardapio.prato_aleatorio()
        return pedido