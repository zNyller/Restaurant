from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from cozinha import Cozinha
    from cliente import Cliente
    from pedido import Pedido

class Garcom:
    def __init__(self, cozinha: Cozinha) -> None:
        self.cozinha = cozinha
        self.fila_pedidos: list[Cliente] = []
        self.pedidos_em_andamento: list[Pedido] = []
        self.eventos: list[tuple[str, str]] = []


    def notificar_pedido(self, cliente: Cliente) -> None:
        """Registra na fila que este cliente está pronto para ter o pedido coletado."""
        self.fila_pedidos.append(cliente)


    def coletar_pedidos(self) -> None:
        while self.fila_pedidos:
            cliente = self.fila_pedidos.pop(0)
            pedido = cliente.confirmar_pedido()

            self.eventos.append(
                ("Garçom", 
                f"📝 Pedido de {cliente.nome}"
                f"\n  - Prato: {pedido.prato.nome} "
                f"\n  - Bebida: {pedido.bebida.nome} "
                f"\n  - Total: R${pedido.valor:.2f}")
            )

            self.pedidos_em_andamento.append(pedido)
            self._enviar_para_cozinha(pedido)


    def entregar_pedidos(self) -> None:
        # O [:] cria uma cópia para iteração. # Evita que algum pedido seja pulado após remoção ao final.
        for pedido in self.pedidos_em_andamento[:]: 
            if pedido.esta_pronto():
                pedido.entregar()
                self.eventos.append((
                    "Garçom",
                    f"🍽️ Pedido entregue na mesa {pedido.mesa.numero}."
                ))
                self.pedidos_em_andamento.remove(pedido)


    def coletar_eventos(self) -> list[tuple[str, str]]:
        eventos = self.eventos
        self.eventos = []
        return eventos


    def _enviar_para_cozinha(self, pedido: Pedido) -> None:
        self.cozinha.receber_pedido(pedido)
        self.eventos.append(("Garçom", "➡️  Pedido enviado à cozinha."))