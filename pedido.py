from prato import Prato
from bebida import Bebida
from mesa import Mesa

class Pedido:
    def __init__(self, prato: Prato, bebida: Bebida):
        self.prato = prato
        self.bebida = bebida
        self.valor = prato.preco + bebida.preco
        self.mesa = None
        self.status = None


    def preparando(self):
        self.status = "preparando"


    def finalizar(self):
        self.status = "finalizado"


    def entregar(self, mesa: Mesa):
        self.status = "entregue"
        print(f"Pedido entregue na mesa n° {mesa.numero}.")


    def verificar_status(self):
        print(f"Status do pedido: {self.status}")