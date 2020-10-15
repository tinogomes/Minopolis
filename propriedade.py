class Propriedade():
    def __init__(self, preco=300, aluguel=60):
        self.preco = preco
        self.aluguel = aluguel
        self.proprietario = None

    def __repr__(self):
        return f'Propriedade(preco={self.preco}, aluguel={self.aluguel})'

    def __str__(self):
        return f'Propriedade(preco: {self.preco}, aluguel: {self.aluguel}, proprietario: {self.proprietario})'
