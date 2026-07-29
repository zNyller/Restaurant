from time import sleep
from cardapio import Cardapio
from cliente import Cliente
from mesa import Mesa
from pedido import Pedido
from cozinha import Cozinha
from utils import validar_string

class Restaurante:
    def __init__(self, cardapio: Cardapio) -> None:
        self.cardapio = cardapio
        self.cozinha = Cozinha()
        self.aberto = False
        self.mesas = []
        self.clientes = []
        self.pedidos = []
        self.avaliacoes = 0

        self.criar_mesas()


    def criar_mesas(self) -> None:
        """Cria as mesas do restaurante e as adiciona à lista de mesas."""
        for num in range (1, 7):
            self.mesas.append(Mesa(num))


    def verificar_status(self) -> None:
        """Exibe o status atual do restaurante (avaliações, mesas, clientes, etc...)"""
        print(
            f"Status atual do restaurante:"
            f"\nAvaliações: {self.avaliacoes}"
            f"\nNúmero de mesas: {len(self.mesas)}"
            f"\nNúmero de clientes: {len(self.clientes)}"
            f"\nNúmero de pedidos feitos: {len(self.pedidos)}"
        )


    def abrir_restaurante(self) -> None:
        """Abre o restaurante e inicia o fluxo de atendimento."""
        print("Abrindo restaurante...")
        self.aberto = True
        sleep(1)
        print("Um cliente chegou!")
        self.atender_cliente()


    def atender_cliente(self) -> None:
        """Realiza o atendimento do cliente, da acomodação até a entrega do pedido."""
        cliente = self.cadastrar_cliente()
        if self.mesas_disponiveis():
            mesa = self.acomodar_cliente(cliente)
            sleep(1)
            pedido = self.anotar_pedido(cliente, mesa)
            self.enviar_para_cozinha(pedido)
            self.entregar_pedido(pedido, mesa)


    def cadastrar_cliente(self) -> Cliente:
        """Cadastra um cliente e o armazena na lista de clientes, o retornando ao final."""
        nome = validar_string("> Cadastrar cliente: ")
        cliente = Cliente(nome)
        self.clientes.append(cliente)
        print(f"Cliente {nome} cadastrado com sucesso!")
        return cliente


    def mesas_disponiveis(self) -> bool:
        """
        Verifica mesas disponíveis para acomodar o cliente, 
        retorna se foi (True) ou não (False) possível.
        """
        for mesa in self.mesas:
            if mesa.esta_livre():
                return True

        print("Não há mesas disponíveis!")
        return False


    def acomodar_cliente(self, cliente: Cliente) -> Mesa:
        """
        Acomoda o cliente e retorna a mesa que foi ocupada.
        """
        for mesa in self.mesas:
            if not mesa.ocupada:
                mesa.ocupar(cliente)
                print(f"Cliente acomodado à mesa n° {mesa.numero}.")
                return mesa


    def anotar_pedido(self, cliente: Cliente, mesa: Mesa) -> Pedido:
        """Anota o pedido feito pelo cliente, registra na lista de pedidos e o retorna."""
        pedido = cliente.fazer_pedido(self.cardapio)
        self.pedidos.append(pedido)
        mesa.registrar_pedido(pedido)

        print(f"Anotando o pedido (Mesa n° {mesa.numero})...")
        sleep(1)
        print(
            f"O cliente pediu {pedido.prato.nome} e {pedido.bebida.nome}, "
            f"no valor total de R${pedido.valor:.2f}"
        )

        return pedido


    def enviar_para_cozinha(self, pedido: Pedido) -> None:
        """Envia o pedido à cozinha para ser preparado."""
        print("Enviando o pedido à cozinha...")
        sleep(1)
        self.cozinha.preparar_prato(pedido)


    def entregar_pedido(self, pedido: Pedido, mesa: Mesa) -> None:
        """Realiza a entrega do pedido."""
        pedido.entregar(mesa)