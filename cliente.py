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
    def __init__(self, nome: str) -> None:
        self.nome = nome
        self.status = Status.AGUARDANDO_ATENDIMENTO
        self.mesa: Mesa = None
        self.pedido: Pedido = None
        self.tempo_comendo: int = 30
        self.tempo_pagando: int = 20
        self.eventos: list[tuple[str, str]] = []
        #self.comanda = 0


    def atualizar(self, minutos: int) -> str | None:
        """Avança um turno de clientes."""

        if self.status == Status.SENTOU:
            self.realizar_pedido()

        elif self.status == Status.AGUARDANDO_PEDIDO:
            self.eventos.append(("Clientes", f"🕑 {self.nome} aguardando pedido..."))

        elif self.status == Status.COMENDO:
            self.tempo_comendo -= minutos
            if self.tempo_comendo <= 0:
                self.pagar(self.pedido)
            else:
                self.eventos.append(
                    ("Clientes", 
                     f"🍽️ {self.nome} está comendo... ({self.tempo_comendo:.0f}min)")
                )
                
        elif self.status == Status.PAGANDO:
            self.tempo_pagando -= minutos
            if self.tempo_pagando <= 0:
                self.avaliar()
                self.mesa.liberar()
            else:
                self.eventos.append(
                    ("Clientes", 
                     f"💳 {self.nome} está pagando... ({self.tempo_pagando:.0f}min)")
                )

        elif self.status == Status.AVALIANDO:
            self.sair()


    def aguardando_atendimento(self) -> bool:
        return self.status == Status.AGUARDANDO_ATENDIMENTO


    def sentar(self) -> None:
        self.status = Status.SENTOU


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


    def esta_aguardando_pedido(self) -> bool:
        return self.status == Status.AGUARDANDO_PEDIDO


    def consumir(self) -> None:
        self.status = Status.COMENDO


    def esta_consumindo(self) -> bool:
        return self.status == Status.COMENDO


    def pagar(self, pedido: Pedido):
        self.status = Status.PAGANDO


    def esta_pagando(self) -> bool:
        return self.status == Status.PAGANDO


    def avaliar(self) -> None:
        self.status = Status.AVALIANDO
        self.eventos.append(("Clientes", f"⭐ {self.nome} avaliou o restaurante."))


    def sair(self) -> None:
        self.status = Status.SAIU
        self.eventos.append(("Clientes", f"🚪 {self.nome} deixou o restaurante."))


    def saiu(self) -> bool:
        return self.status == Status.SAIU


    def coletar_eventos(self) -> list[tuple[str, str]]:
        eventos = self.eventos
        self.eventos = []
        return eventos