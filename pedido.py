from prato import Prato
from bebida import Bebida
from mesa import Mesa

class Pedido:
    def __init__(self, prato: Prato, bebida: Bebida):
        self.prato = prato
        self.bebida = bebida
        self.valor = prato.preco + bebida.preco
        self.mesa = None
        self.status = "criado"


    def na_fila(self):
        self.status = "na fila"


    def preparando(self):
        self.status = "preparando"


    def finalizado(self):
        self.status = "finalizado"


    def entregue(self, mesa: Mesa):
        self.status = "entregue"
        print(f"Pedido entregue na mesa n° {mesa.numero}.")


    def verificar_status(self):
        print(f"Status do pedido: {self.status}")


    def esta_pronto(self):
        if self.status == "finalizado":
            return True
        return False