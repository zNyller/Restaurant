from cliente import Cliente

class Mesa:
    def __init__(self, numero: int):
        self.numero = numero
        self.ocupada = False
        self.cliente = None


    def ocupar(self, cliente: Cliente) -> None:
        self.ocupada = True
        self.cliente = cliente


    def liberar (self) -> None:
        self.cliente = None
        self.ocupada = False