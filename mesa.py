from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from cliente import Cliente
    from pedido import Pedido

class Mesa:
    def __init__(self, numero: int):
        self.numero = numero
        self.ocupada = False
        self.cliente = None
        self.pedido = None
        self.pedido_recebido = False


    def esta_livre(self) -> bool:
        return not self.ocupada


    def ocupar(self, cliente: "Cliente") -> None:
        """Configura a mesa como ocupada e registra o cliente que está nela."""
        self.ocupada = True
        self.cliente = cliente
        self.cliente.sentar()


    def registrar_pedido(self, pedido: "Pedido") -> None:
        """Registra e vincula o pedido feito à mesa atual."""
        self.pedido = pedido


    def receber_pedido(self):
        self.pedido_recebido = True


    def recebeu_pedido(self) -> bool:
        return self.pedido_recebido


    def liberar(self) -> None:
        """Configura a mesa como liberada, remove o cliente e o pedido que estava nela."""
        self.ocupada = False
        self.cliente = None
        self.pedido = None