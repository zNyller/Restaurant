import random
from terminal import Terminal
from event_bus import EventBus
from recepcao import Recepcao
from salao import Salao
from cardapio import Cardapio
from garcom import Garcom
from cliente import Cliente
from pedido import Pedido
from cozinha import Cozinha
from utils import validar_inteiro

class Restaurante:

    TEMPO_POR_TURNO = 10

    def __init__(self, cardapio: Cardapio) -> None:
        self.cardapio = cardapio
        self.event_bus = EventBus()
        self.salao = Salao()
        self.cozinha = Cozinha(self.event_bus)
        self.garcom = Garcom(self.cozinha, self.event_bus)
        self.recepcao = Recepcao(self.salao, self.cardapio, self.garcom, self.event_bus)
        self.aberto: bool = False
        self.turno: int = 0
        self.clientes: list[Cliente] = []
        self.pedidos: list[Pedido] = []
        self.avaliacoes: int = 0


    def exibir_status(self) -> None:
        """Exibe o status atual do restaurante (avaliações, mesas, clientes, etc...)"""
        print(
            f"Status atual do restaurante:"
            f"\nAvaliações: {self.avaliacoes}"
            f"\nNúmero de mesas: {len(self.salao.mesas)}"
            f"\nNúmero de clientes: {len(self.clientes)}"
            f"\nNúmero de pedidos feitos: {len(self.pedidos)}"
        )


    def abrir_restaurante(self) -> None:
        """Abre o restaurante e inicia o fluxo de atendimento."""
        print("Abrindo restaurante...")
        self.aberto = True

        while self.aberto:
            self._proximo_turno()
            if self.turno >= 7:
                self._encerrar()


    def _talvez_chegue_cliente(self) -> None:
        """Define uma chance de 70% de um cliente chegar ao restaurante.
        Caso chegue, o recepciona. Caso contrário, informa que não chegou."""
        if random.random() < 0.7:
            print("Um cliente chegou!")
            cliente = self.recepcao.cadastrar_cliente()
            self.clientes.append(cliente)
        else:
            print("Nenhum cliente chegou neste turno.")


    def _proximo_turno(self) -> None:
        """Processa o próximo turno de eventos, atualizando objetos."""
        self.turno += 1
        print(f"\n===== TURNO {self.turno} =====")

        self._talvez_chegue_cliente()

        for cliente in self.clientes:
            cliente.atualizar(self.TEMPO_POR_TURNO)

        self.garcom.coletar_pedidos()

        self.cozinha.atualizar(self.TEMPO_POR_TURNO)

        self.garcom.entregar_pedidos()

        self.recepcao.atualizar()

        self._remover_clientes_finalizados()

        Terminal.exibir(self.event_bus.coletar())


    def _remover_clientes_finalizados(self):
        clientes_ativos = []

        for cliente in self.clientes:
            if not cliente.saiu():
                clientes_ativos.append(cliente)

        self.clientes = clientes_ativos


    def _encerrar(self) -> None:
        print("1. Aguardar próximo cliente \n2. Encerrar atendimentos")
        decisao = validar_inteiro("Qual a decisão? ")

        if decisao == 2:
            self.aberto = False