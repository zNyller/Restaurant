import random
from terminal import Terminal
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
        self.salao = Salao()
        self.cozinha = Cozinha()
        self.garcom = Garcom(self.cozinha)
        self.recepcao = Recepcao(self.salao, self.cardapio, self.garcom)
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
        """Define uma chance de 50% de um cliente chegar ao restaurante.
        Caso chegue, o recepciona. Caso contrário, informa que não chegou."""
        if random.random() < 0.5:
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

        self._exibir_eventos()


    def _remover_clientes_finalizados(self):
        clientes_ativos = []

        for cliente in self.clientes:
            if not cliente.saiu():
                clientes_ativos.append(cliente)

        self.clientes = clientes_ativos


    def _exibir_eventos(self):
        eventos = []

        eventos.extend(self.recepcao.coletar_eventos())

        for cliente in self.clientes:
            eventos.extend(cliente.coletar_eventos())

        eventos.extend(self.garcom.coletar_eventos())
        eventos.extend(self.cozinha.coletar_eventos())

        Terminal.exibir(eventos)


    def _encerrar(self) -> None:
        print("1. Aguardar próximo cliente \n2. Encerrar atendimentos")
        decisao = validar_inteiro("Qual a decisão? ")

        if decisao == 2:
            self.aberto = False