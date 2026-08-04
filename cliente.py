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
    def __init__(self, nome) -> None:
        self.nome = nome
        self.status = Status.AGUARDANDO_ATENDIMENTO
        self.mesa = None
        self.pedido = None
        self.tempo_comendo: int = 30
        self.tempo_pagando: int = 20
        #self.comanda = 0


    def atualizar(self, minutos: int) -> None:
        """Avança um turno de clientes."""

        if self.status == Status.SENTOU:
            self.realizar_pedido()

        if self.status == Status.COMENDO:
            self.tempo_comendo -= minutos
            if self.tempo_comendo <= 0:
                self.pagar(self.pedido)
            else:
                turnos_restantes = self.tempo_comendo / minutos
                print(
                    f"{self.nome} está comendo... "
                    f"({turnos_restantes:.0f} turnos restantes)"
                )
                
        if self.status == Status.PAGANDO:
            self.tempo_pagando -= minutos
            if self.tempo_pagando <= 0:
                self.avaliar()
                self.mesa.liberar()
            else:
                turnos_restantes = self.tempo_pagando / minutos
                print(
                    f"{self.nome} está pagando... "
                    f"({turnos_restantes:.0f} turnos restantes)"
                )


    def aguardando_atendimento(self) -> bool:
        return self.status == Status.AGUARDANDO_ATENDIMENTO


    def sentar(self) -> None:
        self.status = Status.SENTOU


    def esta_sentado(self) -> bool:
        return self.status == Status.SENTOU


    def ocupar(self, mesa: Mesa) -> None:
        """Vincula a mesa ao cliente."""
        self.mesa = mesa


    def aguardar_pedido(self) -> None:
        self.status = Status.AGUARDANDO_PEDIDO


    def esta_aguardando_pedido(self) -> bool:
        return self.status == Status.AGUARDANDO_PEDIDO


    def realizar_pedido(self) -> None:
        """Monta um pedido aleatório utilizando o cardapio à mesa e notifica o garçom."""
        prato = self.mesa.cardapio.prato_aleatorio()
        bebida = self.mesa.cardapio.bebida_aleatoria()
        self.pedido = Pedido(prato, bebida)
        self.status = Status.REALIZANDO_PEDIDO
        self.mesa.garcom.notificar_pedido(self)


    def comunicar_pedido(self) -> Pedido:
        """Vincula o pedido à mesa e o retorna."""
        self.mesa.registrar_pedido(self.pedido)
        return self.pedido


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
        print(f"{self.nome} avaliou o restaurante.")


    def sair(self) -> None:
        self.status = Status.SAIU
        print(f"{self.nome} deixou o restaurante.")