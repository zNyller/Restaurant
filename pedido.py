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
    def __init__(self, prato: Prato, bebida: Bebida) -> None:
        self.prato = prato
        self.bebida = bebida
        self.valor = prato.preco + bebida.preco
        self.mesa = None
        self._status = Status.CRIADO


    # Propriedas públicas
    @property
    def status(self) -> Status:
        return self._status


    @property
    def esta_pronto(self) -> bool:
        return self.status == Status.FINALIZADO


    # Comportamentos públicos
    def inserir_na_fila(self) -> None:
        self._status = Status.NA_FILA


    def iniciar_preparo(self) -> None:
        self._status = Status.PREPARANDO


    def finalizar(self) -> None:
        self._status = Status.FINALIZADO


    def vincular(self, mesa: Mesa) -> None:
        self.mesa = mesa


    def entregar(self) -> None:
        """Marca o pedido como entregue e notifica a mesa."""
        self._status = Status.ENTREGUE
        self.mesa.receber_pedido()