from prato import Prato
from bebida import Bebida

class Pedido:
    def __init__(self, prato: Prato, bebida: Bebida):
        self.prato = prato
        self.bebida = bebida
        self.valor = prato.preco + bebida.preco
