from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from salao import Salao
    from cozinha import Cozinha
    from cliente import Cliente
    from pedido import Pedido

class Garcom:
    def __init__(self, cozinha: Cozinha) -> None:
        self.cozinha = cozinha
        self.fila_pedidos: list[Cliente] = []
        self.pedidos_em_andamento: list[Pedido] = []


    def notificar_pedido(self, cliente: Cliente) -> None:
        """Registra na fila que este cliente está pronto para ter o pedido coletado."""
        self.fila_pedidos.append(cliente)


    def coletar_pedidos(self) -> None:
        while self.fila_pedidos:
            cliente = self.fila_pedidos.pop(0)
            pedido = cliente.comunicar_pedido()

            print(f"Anotando o pedido...")
            print(
                f"O cliente pediu {pedido.prato.nome} e {pedido.bebida.nome}, "
                f"no valor total de R${pedido.valor:.2f} "
                f"\nTempo estimado: {pedido.prato.tempo}min"
            )

            self.pedidos_em_andamento.append(pedido)
            self._enviar_para_cozinha(pedido)


    def _enviar_para_cozinha(self, pedido: Pedido) -> None:
        self.cozinha.receber_pedido(pedido)
        print("Enviando o pedido à cozinha...")


    def entregar_pedidos(self) -> None:
        # O [:] cria uma cópia para iteração. # Evita que algum pedido seja pulado após remoção ao final.
        for pedido in self.pedidos_em_andamento[:]: 
            if pedido.esta_pronto():
                pedido.entregar()
                self.pedidos_em_andamento.remove(pedido)