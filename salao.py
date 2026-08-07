from mesa import Mesa

class Salao:
    def __init__(self):
        self.mesas: list[Mesa] = []

        self.criar_mesas()


    def criar_mesas(self):
        for num in range(1, 7):
            self.mesas.append(Mesa(num))


    def tem_mesa_disponivel(self) -> bool:
        for mesa in self.mesas:
            if mesa.esta_livre:
                return True
            
        return False