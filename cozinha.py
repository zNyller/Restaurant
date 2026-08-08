from __future__ import annotations
from collections import deque
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from event_bus import EventBus
    from pedido import Pedido

class Cozinha:
    def __init__(self, event_bus: EventBus) -> None:
        self.event_bus = event_bus
        self.fila: deque[Pedido] = deque()
        self.pedido_atual: Pedido = None
        self._tempo_restante: int = 0


    def receber_pedido(self, pedido: Pedido) -> None:
        """Recebe um novo pedido e o adiciona à fila."""
        pedido.inserir_na_fila()
        self.fila.append(pedido)


    def atualizar(self, minutos: int) -> None:
        """Avança um turno da cozinha, com base nos minutos recebidos como parâmetro."""

        # Se não há pedido sendo preparado, pega o próximo da fila.
        if self.pedido_atual is None and self.fila:
            self.pedido_atual = self.fila.popleft()
            self.pedido_atual.iniciar_preparo()
            self._tempo_restante = self.pedido_atual.prato.tempo

        if self.pedido_atual is not None:
            self._preparar(minutos)


    def _preparar(self, minutos) -> None:
        """Processa um turno do preparo do pedido atual."""
        
        if self._tempo_restante > 0:
            self.event_bus.registrar(
                "Cozinha", 
                f"🫕  Preparando {self.pedido_atual.prato.nome} ({self._tempo_restante}min)"
            )
            
            self._tempo_restante -= minutos
            return

        self._disponibilizar_prato()


    def _disponibilizar_prato(self) -> None:
        """Finaliza o pedido atual."""
        self.pedido_atual.finalizar()
        self.event_bus.registrar(
            "Cozinha", f"🍝  {self.pedido_atual.prato.nome} ficou pronto!"
        )

        self.pedido_atual = None
        self._tempo_restante = 0