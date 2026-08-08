from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from event_bus import EventBus
    from mesa import Mesa

from enum import Enum
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
        self._status = Status.AGUARDANDO_ATENDIMENTO
        self._mesa: Mesa = None
        self._pedido: Pedido = None
        self._tempo_comendo: int = 30
        self._tempo_pagando: int = 10
        self._avaliou_restaurante: bool = False
        #self.comanda = 0

    # Propriedades públicas
    @property
    def status(self) -> Status:
        return self._status

    @property
    def esta_aguardando_atendimento(self) -> bool:
        return self._status == Status.AGUARDANDO_ATENDIMENTO

    @property
    def esta_sentado(self) -> bool:
        return self._status == Status.SENTOU

    @property
    def esta_aguardando_pedido(self) -> bool:
        return self._status == Status.AGUARDANDO_PEDIDO

    @property
    def esta_consumindo(self) -> bool:
        return self._status == Status.COMENDO

    @property
    def esta_pagando(self) -> bool:
        return self._status == Status.PAGANDO

    @property
    def esta_avaliando(self) -> bool:
        return self._status == Status.AVALIANDO

    @property
    def avaliou(self) -> bool:
        return self._avaliou_restaurante

    @property
    def saiu(self) -> bool:
        return self._status == Status.SAIU

    # Métodos públicos
    def atualizar(self, minutos: int) -> str | None:
        """Avança um turno de clientes."""

        if self.esta_sentado:
            self._realizar_pedido()

        elif self.esta_aguardando_pedido:
            self.event_bus.registrar("Clientes", f"🕑 {self.nome} aguardando pedido...")

        elif self.esta_consumindo:
            self._tempo_comendo -= minutos
            if self._tempo_comendo <= 0:
                self._pagar(self._pedido)
            else:
                self.event_bus.registrar(
                    "Clientes", 
                    f"🍽️  {self.nome} está comendo... ({self._tempo_comendo:.0f}min)"
                )
                
        elif self.esta_pagando:
            self._tempo_pagando -= minutos
            if self._tempo_pagando <= 0:
                self._avaliar()
                self._mesa.liberar()

        elif self.esta_avaliando:
            self._avaliou_restaurante = True
            self._sair()

    def sentar(self) -> None:
        self._status = Status.SENTOU

    def ocupar(self, mesa: Mesa) -> None:
        """Vincula a mesa ao cliente."""
        self._mesa = mesa

    def confirmar_pedido(self) -> Pedido:
        """Vincula o pedido à mesa e o retorna."""
        self._mesa.registrar_pedido(self._pedido)
        return self._pedido

    def aguardar_pedido(self) -> None:
        self._status = Status.AGUARDANDO_PEDIDO

    def consumir(self) -> None:
        self._status = Status.COMENDO

    # Métodos privados
    def _realizar_pedido(self) -> None:
        """Monta um pedido aleatório utilizando o cardapio à mesa e notifica o garçom."""
        prato = self._mesa.cardapio.prato_aleatorio()
        bebida = self._mesa.cardapio.bebida_aleatoria()
        self._pedido = Pedido(prato, bebida)
        self._mesa.chamar_garcom()

    def _pagar(self, pedido: Pedido) -> None:
        self._status = Status.PAGANDO
        self.event_bus.registrar(
            "Clientes", f"💳  {self.nome} está pagando... (R${pedido.valor:.2f})"
        )

    def _avaliar(self) -> None:
        self._status = Status.AVALIANDO
        self.event_bus.registrar("Clientes", f"⭐ {self.nome} avaliou o restaurante.")

    def _sair(self) -> None:
        self._status = Status.SAIU
        self.event_bus.registrar("Clientes", f"🚪 {self.nome} deixou o restaurante.")