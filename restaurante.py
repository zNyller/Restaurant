from time import sleep
from cardapio import Cardapio
from cliente import Cliente
from cozinha import Cozinha
from utils import validar_string

class Restaurante:
    def __init__(self, cardapio: Cardapio) -> None:
        self.cardapio = cardapio
        self.cozinha = Cozinha()
        self.aberto = False
        self.clientes = []
        self.pedidos = []


    def abrir_restaurante(self) -> None:
        print("Abrindo restaurante...")
        self.aberto = True
        sleep(1)
        print("Um cliente chegou!")
        self.atender_cliente()


    def atender_cliente(self) -> None:
        cliente = self.cadastrar_cliente()
        print("Direcionando o cliente à mesa...")
        sleep(1)
        self.anotar_pedido(cliente)


    def cadastrar_cliente(self) -> Cliente:
        nome = validar_string("> Cadastrar cliente: ")
        cliente = Cliente(nome)
        self.clientes.append(cliente)
        print(f"Cliente {nome} cadastrado com sucesso!")
        return cliente


    def anotar_pedido(self, cliente: Cliente) -> None:
        pedido = cliente.fazer_pedido(self.cardapio)
        print(f"Anotando o pedido...")
        sleep(1)
        print(
            f"O cliente pediu {pedido.prato.nome} e {pedido.bebida.nome}, "
            f"no valor total de R${pedido.valor:.2f}"
        )
        print("Enviando o pedido à cozinha...")
        sleep(1)

        self.cozinha.preparar_prato(pedido.prato)