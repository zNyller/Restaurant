from time import sleep
from cardapio import Cardapio
from cliente import Cliente
from mesa import Mesa
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
        for num in range (1, 7):
            self.mesas.append(Mesa(num))


    def verificar_status(self):
        print(
            f"Status atual do restaurante:"
            f"\nAvaliações: {self.avaliacoes}"
            f"\nNúmero de mesas: {len(self.mesas)}"
            f"\nNúmero de clientes: {len(self.clientes)}"
            f"\nNúmero de pedidos feitos: {len(self.pedidos)}"
        )


    def abrir_restaurante(self) -> None:
        print("Abrindo restaurante...")
        self.aberto = True
        sleep(1)
        print("Um cliente chegou!")
        self.atender_cliente()


    def atender_cliente(self) -> None:
        cliente = self.cadastrar_cliente()
        if self.acomodar_cliente(cliente):
            sleep(1)
            self.anotar_pedido(cliente)


    def cadastrar_cliente(self) -> Cliente:
        nome = validar_string("> Cadastrar cliente: ")
        cliente = Cliente(nome)
        self.clientes.append(cliente)
        print(f"Cliente {nome} cadastrado com sucesso!")
        return cliente


    def acomodar_cliente(self, cliente: Cliente):
        for mesa in self.mesas:
            if not mesa.ocupada:
                mesa.ocupar(cliente)
                print(f"Cliente {cliente.nome} acomodado à mesa n° {mesa.numero}.")
                return True

        print("Não há mesas disponíveis!")
        return False


    def anotar_pedido(self, cliente: Cliente) -> None:
        pedido = cliente.fazer_pedido(self.cardapio)
        self.pedidos.append(pedido)
        print(f"Anotando o pedido...")
        sleep(1)
        print(
            f"O cliente pediu {pedido.prato.nome} e {pedido.bebida.nome}, "
            f"no valor total de R${pedido.valor:.2f}"
        )
        print("Enviando o pedido à cozinha...")
        sleep(1)

        self.cozinha.preparar_prato(pedido.prato)