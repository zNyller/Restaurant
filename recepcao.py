from __future__ import annotations
from collections import deque
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from salao import Salao
    from cardapio import Cardapio
    from garcom import Garcom
    from event_bus import EventBus
    from mesa import Mesa

from cliente import Cliente
from utils import validar_string

class Recepcao:
    def __init__(
            self, 
            salao: Salao, 
            cardapio: Cardapio, 
            garcom: Garcom, 
            event_bus: EventBus
        ) -> None:
        self.salao = salao
        self.cardapio = cardapio
        self.garcom = garcom
        self.event_bus = event_bus
        self.fila: deque[Cliente] = deque()


    def cadastrar_cliente(self) -> Cliente:
        """Cadastra um cliente e o armazena na lista de clientes, acomodando-o ao final."""
        nome = validar_string("> Cadastrar cliente: ")
        cliente = Cliente(nome, self.event_bus)
        self.fila.append(cliente)
        self.event_bus.publicar(
            "Recepção", f"🎟️  {nome} recepcionado."
        )

        self._acomodar_clientes()
        return cliente


    def atualizar(self) -> None:
        self._acomodar_clientes()


    def _acomodar_clientes(self) -> None:
        if self.fila and not self.salao.tem_mesa_disponivel():
            self.event_bus.publicar(
                "Recepção", f"{len(self.fila)} cliente(s) aguardando na fila."
            )
            
        while self.fila and self.salao.tem_mesa_disponivel():
            cliente = self.fila.popleft()
            self._acomodar_cliente(cliente)


    def _acomodar_cliente(self, cliente: Cliente) -> None:
        mesa = self._localizar_mesa()
        mesa.receber(cliente, self.cardapio, self.garcom)

        self.event_bus.publicar(
            "Recepção", f"🪑 {cliente.nome} acomodado à mesa n° {mesa.numero}"
        )


    def _localizar_mesa(self) -> Mesa:
        for mesa in self.salao.mesas:
            if mesa.esta_livre():
                return mesa