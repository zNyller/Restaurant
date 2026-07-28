def validar_inteiro(msg: str) -> int:
    while True:
        try:
            retorno = int(input(msg))
            return retorno
        except ValueError:
            print("Entrada inválida! Por favor, insira um número inteiro.")


def validar_string(msg: str) -> str:
    while True:
        retorno = input(msg)
        if retorno.strip():
            return retorno
        print("Entrada inválida! Por favor, tente novamente.")
        