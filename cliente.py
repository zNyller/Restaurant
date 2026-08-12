from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from comanda import Comanda
    from event_bus import EventBus
    from mesa import Mesa

from enum import Enum
from pedido import Pedido

class Status(Enum):
    AGUARDANDO_ATENDIMENTO = 'aguardando atendimento'
    SENTOU = 'sentou'
    AGUARDANDO_PEDIDO = 'aguardando pedido'
    COMENDO = 'comendo'
    PEDINDO_A_CONTA = 'pedindo a conta'
    PAGANDO = 'pagando'
    PAGOU = 'pagou'
    AVALIANDO = 'avaliando'
    SAIU = 'saiu'

class Cliente:
    def __init__(self, nome: str, comanda: Comanda, event_bus: EventBus) -> None:
        self.nome = nome
        self._comanda = comanda
        self._event_bus = event_bus
        self._status = Status.AGUARDANDO_ATENDIMENTO
        self._mesa: Mesa = None
        self._tempo_comendo: int = 30
        self._tempo_pagando: int = 10
        self._avaliou_restaurante: bool = False

    # Propriedades públicas
    @property
    def status(self) -> Status:
        return self._status

    @property
    def comanda(self) -> Comanda:
        return self._comanda

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
    def esta_pedindo_a_conta(self) -> bool:
        return self._status == Status.PEDINDO_A_CONTA

    @property
    def esta_pagando(self) -> bool:
        return self._status == Status.PAGANDO

    @property
    def pagou(self) -> bool:
        return self._status == Status.PAGOU

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
    def atualizar(self, minutos: int) -> None:
        """Avança um turno de clientes."""

        if self.esta_sentado:
            self._realizar_pedido()

        elif self.esta_aguardando_pedido:
            self._event_bus.registrar("Clientes", f"🕑 {self.nome} aguardando pedido...")

        elif self.esta_consumindo:
            self._tempo_comendo -= minutos
            if self._tempo_comendo <= 0:
                self._pedir_a_conta()
                self._mesa.liberar()
            else:
                self._event_bus.registrar(
                    "Clientes", 
                    f"🍽️  {self.nome} está comendo... ({self._tempo_comendo:.0f}min)"
                )
                
        elif self.esta_pagando:
            self._tempo_pagando -= minutos
            if self._tempo_pagando <= 0:
                self._status = Status.PAGOU

        elif self._status == Status.PAGOU:
            self._avaliar()

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
        self._mesa.registrar_pedido(self._comanda.pedido)
        return self._comanda.pedido

    def aguardar_pedido(self) -> None:
        self._status = Status.AGUARDANDO_PEDIDO

    def consumir(self) -> None:
        self._status = Status.COMENDO

    def pagar(self, valor: float) -> None:
        self._status = Status.PAGANDO
        self._event_bus.registrar(
            "Clientes", f"💳  {self.nome} está pagando... (R${valor:.2f})"
        )

    # Métodos privados
    def _realizar_pedido(self) -> None:
        """Monta um pedido aleatório utilizando o cardapio à mesa e notifica o garçom."""
        prato = self._mesa.cardapio.prato_aleatorio()
        bebida = self._mesa.cardapio.bebida_aleatoria()
        pedido = Pedido(prato, bebida)

        self._comanda.registrar(pedido)
        self._mesa.chamar_garcom()

    def _pedir_a_conta(self) -> None:
        self._event_bus.registrar("Clientes", f"🧾 {self.nome} pediu a conta.")
        self._status = Status.PEDINDO_A_CONTA

    def _avaliar(self) -> None:
        self._status = Status.AVALIANDO
        self._event_bus.registrar("Clientes", f"⭐ {self.nome} avaliou o restaurante.")

    def _sair(self) -> None:
        self._status = Status.SAIU
        self._event_bus.registrar("Clientes", f"🚪 {self.nome} deixou o restaurante.")