from collections import defaultdict

class Terminal:

    @staticmethod
    def exibir(eventos: list[tuple[str, str]]) -> None:
        grupos = defaultdict(list)

        for categoria, mensagem in eventos:
            grupos[categoria].append(mensagem)

        for categoria, mensagens in grupos.items():
            print(f"\n[{categoria}]")
            print("-" * (len(categoria) + 2))

            for mensagem in mensagens:
                print(mensagem)