import random
from salao import Salao
from cardapio import Cardapio
from garcom import Garcom
from cliente import Cliente
from pedido import Pedido
from cozinha import Cozinha
from utils import validar_string, validar_inteiro

class Restaurante:

    TEMPO_POR_TURNO = 10

    def __init__(self, cardapio: Cardapio) -> None:
        self.cardapio = cardapio
        self.salao = Salao()
        self.cozinha = Cozinha()
        self.garcom = Garcom(self.salao, self.cozinha, self.cardapio)
        self.aberto = False
        self.turno = 1
        self.fila = []
        self.clientes: list[Cliente] = []
        self.pedidos: list[Pedido] = []
        self.avaliacoes = 0


    def verificar_status(self) -> None:
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

        print(f"\n===== TURNO {self.turno} =====")

        while self.aberto:
            self.talvez_chegue_cliente()
            self.acomodar_clientes()
            self.proximo_turno()
            if self.turno >= 10:
                self.encerrar()


    def talvez_chegue_cliente(self) -> None:
        """Define uma chance de 50% de um cliente chegar ao restaurante.
        Caso chegue, o recepciona. Caso contrário, exibe que não chegou."""
        if random.random() < 0.5:
            print("Um cliente chegou!")
            self.cadastrar_cliente()
        else:
            print("Nenhum cliente chegou neste turno.")


    def cadastrar_cliente(self) -> Cliente:
        """Cadastra um cliente e o armazena na lista de clientes, o retornando ao final."""
        nome = validar_string("> Cadastrar cliente: ")
        cliente = Cliente(nome)
        self.clientes.append(cliente)
        print(f"Cliente {nome} cadastrado com sucesso!")
        return cliente


    def acomodar_clientes(self) -> None:
        """Percorre a lista de clientes e verifica quais estão aguardando atendimento, 
        em seguida prossegue com a acomodação dos mesmos."""
        for cliente in self.clientes:
            if cliente.aguardando_atendimento():
                self.garcom.acomodar_cliente(cliente)


    def proximo_turno(self) -> None:
        """Processa o próximo turno de eventos, atualizando objetos."""
        self.turno += 1

        print(f"\n===== TURNO {self.turno} =====")

        for cliente in self.clientes:
            cliente.atualizar(self.TEMPO_POR_TURNO)

        self.garcom.atualizar()

        self.cozinha.atualizar(self.TEMPO_POR_TURNO)


    def encerrar(self) -> None:
        print("1. Aguardar próximo cliente \n2. Encerrar atendimentos")
        decisao = validar_inteiro("Qual a decisão? ")

        if decisao == 2:
            self.aberto = False