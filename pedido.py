from enum import Enum
from prato import Prato
from bebida import Bebida
from mesa import Mesa

class Status(Enum):
    CRIADO = 'criado'
    NA_FILA = 'na fila'
    PREPARANDO = 'preparando'
    FINALIZADO = 'finalizado'
    ENTREGUE = 'entregue'

class Pedido:
    def __init__(self, prato: Prato, bebida: Bebida):
        self.prato = prato
        self.bebida = bebida
        self.valor = prato.preco + bebida.preco
        self.mesa = None
        self.status = Status.CRIADO


    def na_fila(self):
        self.status = Status.NA_FILA


    def preparando(self):
        self.status = Status.PREPARANDO


    def finalizado(self):
        self.status = Status.FINALIZADO


    def vincular(self, mesa: Mesa):
        self.mesa = mesa


    def entregar(self):
        """Marca o pedido como entregue e notifica a mesa."""
        self.status = Status.ENTREGUE
        self.mesa.receber_pedido()


    def verificar_status(self):
        print(f"Status do pedido: {self.status}")


    def esta_pronto(self):
        return self.status == Status.FINALIZADO