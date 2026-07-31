from enum import Enum
from mesa import Mesa
from cardapio import Cardapio
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
        if self.status == Status.AGUARDANDO_PEDIDO and self.mesa.recebeu_pedido():
            self.consumir(self.pedido)

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
        self.mesa = mesa


    def aguardar_pedido(self) -> None:
        self.status = Status.AGUARDANDO_PEDIDO


    def esta_aguardando_pedido(self) -> bool:
        return self.status == Status.AGUARDANDO_PEDIDO


    def realizar_pedido(self, cardapio: Cardapio) -> Pedido:
        """
        Recebe o cardápio como parâmetro para acessar os pratos e bebidas
        e monta um pedido aleatório, que ao final é retornado.
        """
        prato = cardapio.prato_aleatorio()
        bebida = cardapio.bebida_aleatoria()
        self.pedido = Pedido(prato, bebida)
        return self.pedido


    def consumir(self, pedido: Pedido) -> None:
        self.status = Status.COMENDO
        print(f"{self.nome} está comendo o {pedido.prato.nome}...")


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