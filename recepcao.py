from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from salao import Salao
    from cardapio import Cardapio
    from garcom import Garcom
    from mesa import Mesa

from cliente import Cliente
from utils import validar_string

class Recepcao:
    def __init__(self, salao: Salao, cardapio: Cardapio, garcom: Garcom):
        self.salao = salao
        self.cardapio = cardapio
        self.garcom = garcom
        self.fila: list[Cliente] = []


    def cadastrar_cliente(self) -> Cliente:
        """Cadastra um cliente e o armazena na lista de clientes, acomodando-o ao final."""
        nome = validar_string("> Cadastrar cliente: ")
        cliente = Cliente(nome)
        self.fila.append(cliente)
        print(f"Cliente {nome} entrou na fila.")

        self._acomodar_clientes()

        return cliente


    def atualizar(self) -> None:
        self._acomodar_clientes()


    def _acomodar_clientes(self) -> None:
        if self.fila and not self.salao.tem_mesa_disponivel():
            print(
                f"Nenhuma mesa disponível no momento. "
                f"{len(self.fila)} cliente(s) aguardando na fila."
            )
            
        while self.fila and self.salao.tem_mesa_disponivel():
            cliente = self.fila.pop(0)
            self._acomodar_cliente(cliente)


    def _acomodar_cliente(self, cliente: Cliente) -> None:
        mesa = self._localizar_mesa()
        mesa.receber(cliente, self.cardapio, self.garcom)

        print(f"{cliente.nome} acomodado à mesa n° {mesa.numero}")


    def _localizar_mesa(self) -> Mesa:
        for mesa in self.salao.mesas:
            if mesa.esta_livre():
                return mesa


    def _inserir_cliente_na_fila(self, cliente: Cliente) -> None:
        self.fila.append(cliente)
        print("Cliente inserido na fila de espera.")