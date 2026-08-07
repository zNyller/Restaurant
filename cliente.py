from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from event_bus import EventBus

from enum import Enum
from mesa import Mesa
from pedido import Pedido

class Status(Enum):
    AGUARDANDO_ATENDIMENTO = 'aguardando atendimento'
    SENTOU = 'sentou'
    AGUARDANDO_PEDIDO = 'aguardando pedido'
    COMENDO = 'comendo'
    PAGANDO = 'pagando'
    AVALIANDO = 'avaliando'
    SAIU = 'saiu'

class Cliente:
    def __init__(self, nome: str, event_bus: EventBus) -> None:
        self.nome = nome
        self.event_bus = event_bus
        self.status = Status.AGUARDANDO_ATENDIMENTO
        self.mesa: Mesa = None
        self.pedido: Pedido = None
        self.tempo_comendo: int = 30
        self.tempo_pagando: int = 10
        self.avaliou_restaurante: bool = False
        #self.comanda = 0


    def atualizar(self, minutos: int) -> str | None:
        """Avança um turno de clientes."""

        if self.esta_sentado:
            self.realizar_pedido()

        elif self.esta_aguardando_pedido:
            self.event_bus.publicar("Clientes", f"🕑 {self.nome} aguardando pedido...")

        elif self.esta_consumindo:
            self.tempo_comendo -= minutos
            if self.tempo_comendo <= 0:
                self.pagar(self.pedido)
            else:
                self.event_bus.publicar(
                    "Clientes", 
                    f"🍽️  {self.nome} está comendo... ({self.tempo_comendo:.0f}min)"
                )
                
        elif self.esta_pagando:
            self.tempo_pagando -= minutos
            if self.tempo_pagando <= 0:
                self.avaliar()
                self.mesa.liberar()

        elif self.esta_avaliando:
            self.avaliou_restaurante = True
            self.sair()


    @property
    def aguardando_atendimento(self) -> bool:
        return self.status == Status.AGUARDANDO_ATENDIMENTO


    def sentar(self) -> None:
        self.status = Status.SENTOU


    @property
    def esta_sentado(self) -> bool:
        return self.status == Status.SENTOU


    def ocupar(self, mesa: Mesa) -> None:
        """Vincula a mesa ao cliente."""
        self.mesa = mesa


    def realizar_pedido(self) -> None:
        """Monta um pedido aleatório utilizando o cardapio à mesa e notifica o garçom."""
        prato = self.mesa.cardapio.prato_aleatorio()
        bebida = self.mesa.cardapio.bebida_aleatoria()
        self.pedido = Pedido(prato, bebida)
        self.mesa.chamar_garcom()


    def confirmar_pedido(self) -> Pedido:
        """Vincula o pedido à mesa e o retorna."""
        self.mesa.registrar_pedido(self.pedido)
        return self.pedido


    def aguardar_pedido(self) -> None:
        self.status = Status.AGUARDANDO_PEDIDO


    @property
    def esta_aguardando_pedido(self) -> bool:
        return self.status == Status.AGUARDANDO_PEDIDO


    def consumir(self) -> None:
        self.status = Status.COMENDO


    @property
    def esta_consumindo(self) -> bool:
        return self.status == Status.COMENDO


    def pagar(self, pedido: Pedido):
        self.status = Status.PAGANDO
        self.event_bus.publicar(
            "Clientes", f"💳  {self.nome} está pagando... (R${pedido.valor:.2f})"
        )


    @property
    def esta_pagando(self) -> bool:
        return self.status == Status.PAGANDO


    def avaliar(self) -> None:
        self.status = Status.AVALIANDO
        self.event_bus.publicar("Clientes", f"⭐ {self.nome} avaliou o restaurante.")


    @property
    def esta_avaliando(self) -> bool:
        return self.status == Status.AVALIANDO


    @property
    def avaliou(self) -> bool:
        return self.avaliou_restaurante


    def sair(self) -> None:
        self.status = Status.SAIU
        self.event_bus.publicar("Clientes", f"🚪 {self.nome} deixou o restaurante.")


    @property
    def saiu(self) -> bool:
        return self.status == Status.SAIU