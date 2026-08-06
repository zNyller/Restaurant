from __future__ import annotations
from collections import deque
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from cozinha import Cozinha
    from event_bus import EventBus
    from cliente import Cliente
    from pedido import Pedido

class Garcom:
    def __init__(self, cozinha: Cozinha, event_bus: EventBus) -> None:
        self.cozinha = cozinha
        self.event_bus = event_bus
        self.fila_pedidos: deque[Cliente] = deque()
        self.pedidos_em_andamento: list[Pedido] = []


    def notificar_pedido(self, cliente: Cliente) -> None:
        """Registra na fila que este cliente está pronto para ter o pedido coletado."""
        self.fila_pedidos.append(cliente)


    def coletar_pedidos(self) -> None:
        while self.fila_pedidos:
            cliente = self.fila_pedidos.popleft()
            pedido = cliente.confirmar_pedido()

            self.event_bus.publicar(
                "Garçom", 
                f"📝 Pedido de {cliente.nome}"
                f"\n  - Prato: {pedido.prato.nome} "
                f"\n  - Bebida: {pedido.bebida.nome} "
                f"\n  - Total: R${pedido.valor:.2f}"
            )

            self.pedidos_em_andamento.append(pedido)
            self._enviar_para_cozinha(pedido)


    def entregar_pedidos(self) -> None:
        """Verifica os pedidos em andamento e entrega o que estiver pronto."""
        restantes = []

        for pedido in self.pedidos_em_andamento: 
            if pedido.esta_pronto():
                pedido.entregar()
                self.event_bus.publicar(
                    "Garçom",
                    f"🍽️  Pedido entregue na mesa {pedido.mesa.numero}."
                )
            else:
                restantes.append(pedido)

        self.pedidos_em_andamento = restantes


    def _enviar_para_cozinha(self, pedido: Pedido) -> None:
        self.cozinha.receber_pedido(pedido)
        self.event_bus.publicar("Garçom", "➡️  Pedido enviado à cozinha.")