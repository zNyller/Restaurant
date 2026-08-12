from __future__ import annotations
from collections import deque
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from financeiro import Financeiro
    from salao import Salao
    from cardapio import Cardapio
    from garcom import Garcom
    from event_bus import EventBus
    from mesa import Mesa

from comanda import Comanda
from cliente import Cliente
from utils import validar_string

class Recepcao:
    def __init__(
            self,
            financeiro: Financeiro, 
            salao: Salao, 
            cardapio: Cardapio, 
            garcom: Garcom, 
            event_bus: EventBus
        ) -> None:
        self.financeiro = financeiro
        self.salao = salao
        self.cardapio = cardapio
        self.garcom = garcom
        self.event_bus = event_bus
        self.comandas: int = 1
        self.clientes_registrados: list[Cliente] = []
        self.fila: deque[Cliente] = deque()

    def cadastrar_cliente(self) -> Cliente:
        """Cadastra um cliente com sua comanda e o recepciona, retornando-o ao final."""
        nome = validar_string("> Cadastrar cliente: ")
        comanda = Comanda(self.comandas)
        cliente = Cliente(nome, comanda, self.event_bus)
        self.clientes_registrados.append(cliente)

        self._recepcionar_cliente(cliente)

        self.comandas += 1

        return cliente

    def atualizar(self) -> None:
        self._gerenciar_fila()

    def fechar_a_conta(self, cliente: Cliente) -> None:
        valor_total = cliente.comanda.valor
        self.event_bus.registrar(
            "Recepção", 
            f"Fechando a conta de {cliente.nome}... Valor total: R${valor_total:.2f}"
        )
        cliente.pagar(valor_total)

    def receber_pagamento(self, cliente: Cliente) -> None:
        valor = cliente.comanda.valor
        self.financeiro.registrar_valor(valor)
        self.event_bus.registrar(
            "Recepção", 
            f"💳  {cliente.nome} efetuou o pagamento | Valor: R${valor:.2f}"
        )

    def _recepcionar_cliente(self, cliente: Cliente) -> None:
        self.fila.append(cliente)

        self.event_bus.registrar(
            "Recepção", f"🎟️  {cliente.nome} recepcionado."
        )

        self._gerenciar_fila()

    def _gerenciar_fila(self) -> None:
        if self.fila and not self.salao.tem_mesa_disponivel():
            self.event_bus.registrar(
                "Recepção", f"{len(self.fila)} cliente(s) aguardando na fila."
            )
            
        while self.fila and self.salao.tem_mesa_disponivel():
            cliente = self.fila.popleft()
            self._acomodar_cliente(cliente)

    def _acomodar_cliente(self, cliente: Cliente) -> None:
        mesa = self._localizar_mesa()
        mesa.receber(cliente, self.cardapio, self.garcom)

        self.event_bus.registrar(
            "Recepção", f"🪑 {cliente.nome} acomodado à mesa n° {mesa.numero}"
        )

    def _localizar_mesa(self) -> Mesa:
        for mesa in self.salao.mesas:
            if mesa.esta_livre:
                return mesa