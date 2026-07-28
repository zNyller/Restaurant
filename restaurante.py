from time import sleep
from cardapio import Cardapio
from utils import validar_string

class Restaurante:
    def __init__(self, cardapio: Cardapio) -> None:
        self.cardapio = cardapio
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
        self.cadastrar_cliente()
        sleep(1)
        self.anotar_pedido()


    def cadastrar_cliente(self) -> None:
        cliente = validar_string("> Cadastrar cliente: ")
        print(f"Cliente {cliente} cadastrado com sucesso!")
        print("Direcionando o cliente à mesa...")


    def anotar_pedido(self) -> None:
        print("Anotando o pedido...")
        sleep(1)
        prato = self.cardapio.prato_aleatorio()
        print(f"O cliente pediu um {prato['nome']}, no valor de R$ {prato['preco']:.2f}")