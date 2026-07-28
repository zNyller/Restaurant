from cardapio import Cardapio
from pedido import Pedido

class Cliente:
    def __init__(self, nome):
        self.nome = nome


    def fazer_pedido(self, cardapio: Cardapio) -> Pedido:
        """
        Recebe o cardápio como parâmetro para acessar os pratos e bebidas
        e monta um pedido aleatório, que ao final é retornado.
        """
        prato = cardapio.prato_aleatorio()
        bebida = cardapio.bebida_aleatoria()
        return Pedido(prato, bebida)