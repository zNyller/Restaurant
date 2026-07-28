class Prato:
    def __init__(self, nome: str, preco: float, tempo: int):
        self.nome = nome
        self.preco = preco
        self.tempo = tempo


    def descricao(self) -> str:
        """Retorna a descrição do prato."""
        return f"\n{self.nome} | Preço: R${self.preco:.2f} | Tempo de preparo: {self.tempo}min"