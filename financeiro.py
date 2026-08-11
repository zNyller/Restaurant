class Financeiro:
    def __init__(self) -> None:
        self.saldo_atual: int = 0


    def registrar_valor(self, valor: float) -> None:
        self.saldo_atual += valor


    def registrar_despesa(self, valor: float) -> None:
        self.saldo_atual -= valor