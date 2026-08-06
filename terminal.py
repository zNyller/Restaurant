from collections import defaultdict

class Terminal:

    @staticmethod
    def exibir(eventos: list[tuple[str, str]]) -> None:
        grupos = defaultdict(list)

        ultima_categoria = None

        for categoria, mensagem in eventos:
            if categoria != ultima_categoria:
                print(f"\n[{categoria}]")
                print("-" * (len(categoria) + 2))
                ultima_categoria = categoria

            print(mensagem)