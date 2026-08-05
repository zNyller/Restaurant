from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pedido import Pedido

class Cozinha:
    def __init__(self):
        self.fila = []
        self.pedido_atual: Pedido = None
        self.tempo_restante: int = 0
        self.eventos: list[tuple[str, str]] = []


    def receber_pedido(self, pedido: Pedido):
        """Recebe um novo pedido e o adiciona à fila."""
        pedido.na_fila()
        self.fila.append(pedido)


    def atualizar(self, minutos: int) -> None:
        """Avança um turno da cozinha."""

        # Se não há pedido sendo preparado, pega o próximo da fila.
        if self.pedido_atual is None and self.fila:
            self.pedido_atual = self.fila.pop(0)
            self.pedido_atual.preparando()
            self.tempo_restante = self.pedido_atual.prato.tempo

        if self.pedido_atual is not None:
            self.preparar(minutos)


    def preparar(self, minutos) -> None:
        """Processa um turno do preparo do pedido atual."""
        self.tempo_restante -= minutos

        if self.tempo_restante > 0:
            self.eventos.append(
                (
                    "Cozinha", 
                    f"🫕  Preparando {self.pedido_atual.prato.nome} ({self.tempo_restante}min)"
                )
            )
            return

        self.disponibilizar_prato()


    def disponibilizar_prato(self) -> None:
        """Finaliza o pedido atual."""
        self.pedido_atual.finalizado()
        self.eventos.append(("Cozinha", f"{self.pedido_atual.prato.nome} ficou pronto!"))

        self.pedido_atual = None
        self.tempo_restante = 0


    def coletar_eventos(self) -> list[tuple[str, str]]:
        eventos = self.eventos
        self.eventos = []
        return eventos