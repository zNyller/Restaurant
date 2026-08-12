from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pedido import Pedido

class Comanda:
    def __init__(self, numero: int) -> None:
        self.numero = numero
        self.pedido: Pedido | None = None

    @property
    def valor(self) -> float:
        return self.pedido.valor if self.pedido else 0.0

    def registrar(self, pedido: Pedido) -> None:
        self.pedido = pedido