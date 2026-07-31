from mesa import Mesa
from cardapio import Cardapio
from pedido import Pedido

class Cliente:
    def __init__(self, nome) -> None:
        self.nome = nome
        self.status = 'chegou'
        self.mesa = None
        self.pedido = None
        self.tempo_comendo: int = 30
        self.tempo_pagando: int = 20
        #self.comanda = 0


    def atualizar(self, minutos: int) -> None:
        """Avança um turno de clientes."""
        if self.status == 'aguardando pedido' and self.mesa.recebeu_pedido():
            self.consumir(self.pedido)

        if self.status == 'comendo':
            self.tempo_comendo -= minutos
            if self.tempo_comendo <= 0:
                self.pagar(self.pedido)
            else:
                turnos_restantes = self.tempo_comendo / minutos
                print(
                    f"{self.nome} está comendo... "
                    f"({turnos_restantes:.0f} turnos restantes)"
                )
                
        if self.status == 'pagando':
            self.tempo_pagando -= minutos
            if self.tempo_pagando <= 0:
                self.avaliar()
            else:
                turnos_restantes = self.tempo_pagando / minutos
                print(
                    f"{self.nome} está pagando... "
                    f"({turnos_restantes:.0f} turnos restantes)"
                )


    def chegou(self) -> bool:
        return self.status == 'chegou'


    def sentar(self) -> None:
        self.status = 'sentou'


    def esta_sentado(self) -> bool:
        return self.status == 'sentou'


    def ocupar(self, mesa: Mesa) -> None:
        self.mesa = mesa


    def aguardar_pedido(self) -> None:
        self.status = 'aguardando pedido'


    def esta_aguardando_pedido(self) -> bool:
        return self.status == 'aguardando pedido'


    def fazer_pedido(self, cardapio: Cardapio) -> Pedido:
        """
        Recebe o cardápio como parâmetro para acessar os pratos e bebidas
        e monta um pedido aleatório, que ao final é retornado.
        """
        prato = cardapio.prato_aleatorio()
        bebida = cardapio.bebida_aleatoria()
        self.pedido = Pedido(prato, bebida)
        return self.pedido


    def consumir(self, pedido: Pedido) -> None:
        self.status = 'comendo'
        print(f"{self.nome} está comendo o {pedido.prato.nome}...")


    def esta_consumindo(self) -> bool:
        return self.status == 'comendo'


    def pagar(self, pedido: Pedido):
        self.status = 'pagando'


    def esta_pagando(self) -> bool:
        return self.status == 'pagando'


    def avaliar(self) -> None:
        self.status = 'avaliando'
        print(f"{self.nome} avaliou o restaurante.")


    def sair(self) -> None:
        self.status = 'saiu'
        print(f"{self.nome} deixou o restaurante.")