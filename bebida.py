class Bebida:
    def __init__(self, nome, preco):
        self.nome = nome
        self.preco = preco


    def descricao(self) -> str:
        """Retorna a descrição da bebida."""
        return f"{self.nome} | Preço: R${self.preco:.2f}"