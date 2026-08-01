from mesa import Mesa

class Salao:
    def __init__(self):
        self.mesas = []

        self.criar_mesas()


    def criar_mesas(self):
        for num in range(1, 7):
            self.mesas.append(Mesa(num))