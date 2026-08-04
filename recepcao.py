from typing import TYPE_CHECKING
from salao import Salao
from garcom import Garcom
from cliente import Cliente
from cardapio import Cardapio
from utils import validar_string

if TYPE_CHECKING:
    from mesa import Mesa

class Recepcao:
    def __init__(self, salao: Salao, cardapio: Cardapio, garcom: Garcom):
        self.salao = salao
        self.cardapio = cardapio
        self.garcom = garcom
        self.clientes: list[Cliente] = []
        self.fila: list[Cliente] = []


    def cadastrar_cliente(self) -> Cliente:
        """Cadastra um cliente e o armazena na lista de clientes, acomodando-o ao final."""
        nome = validar_string("> Cadastrar cliente: ")
        cliente = Cliente(nome)
        self.clientes.append(cliente)
        print(f"Cliente {nome} cadastrado com sucesso!")
        self.acomodar_clientes()


    def acomodar_clientes(self) -> None:
        for cliente in self.clientes:
            if cliente.aguardando_atendimento():
                self._acomodar_cliente(cliente)
                return


    def _acomodar_cliente(self, cliente: Cliente) -> None:
        mesa = self._localizar_mesa()

        if mesa is None:
            print("Nenhuma mesa disponível no momento. Cliente inserido na fila...")
            self._inserir_cliente_na_fila(cliente)
            return

        mesa.receber(cliente, self.cardapio, self.garcom)

        print(f"{cliente.nome} acomodado à mesa n° {mesa.numero}")


    def _localizar_mesa(self) -> "Mesa" | None:
        for mesa in self.salao.mesas:
            if mesa.esta_livre():
                return mesa

        return None


    def _inserir_cliente_na_fila(self, cliente: Cliente) -> None:
        self.fila.append(cliente)
        print("Cliente inserido na fila de espera.")