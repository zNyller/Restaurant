class Financeiro:
    def __init__(self) -> None:
        self._saldo_atual: float = 0

    @property
    def saldo(self) -> float:
        return self._saldo_atual

    def registrar_valor(self, valor: float) -> None:
        self._saldo_atual += valor

    def registrar_despesa(self, valor: float) -> None:
        self._saldo_atual -= valor