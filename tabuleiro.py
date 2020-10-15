from propriedade import Propriedade


class Tabuleiro():
    def __init__(self, jogadores, propriedades, reembolso=100):
        self._valida_argumentos(jogadores, propriedades, reembolso)
        self.propriedades = [None] + propriedades
        self.jogadores = {}
        self.reembolso = reembolso

        for jogador in jogadores:
            self.jogadores[jogador] = 0

    def __str__(self):
        resultado = []

        for indice, propriedade in enumerate(self.propriedades):
            jogadores = [jogador for (jogador, posicao) in self.jogadores.items() if posicao == indice ]
            if propriedade:
                resultado.append(f"[{str(propriedade)}, {jogadores}]")
            else:
                resultado.append(f"[Inicio, {jogadores}]")

        return '\n'.join(resultado)

    def _valida_argumentos(self, jogadores, propriedades, reembolso):
        if len(jogadores) < 2:
            raise ValueError("o tabuleiro precisa de pelo menos 2 jogadores")
        if len(propriedades) < 1:
            raise ValueError("o tabuleiro precisa de pelo menos 1 propriedade")
        if type(reembolso) != int or reembolso <= 0:
            raise ValueError(f"o valor do reembolso deve ser um número maior ou igual a 0: {reembolso}")

    def andar(self, jogador, passos):
        nova_posicao = self.jogadores[jogador] + passos

        if nova_posicao > len(self.propriedades)-1:
            jogador.saldo += 100
            nova_posicao -= len(self.propriedades)-1

        jogador.comprar_ou_aluguar(self.propriedades[nova_posicao])

        if jogador.saldo >= 0:
            self.jogadores[jogador] = nova_posicao
        else:
            for propriedade in self.propriedades:
                if propriedade and propriedade.proprietario == jogador:
                    propriedade.proprietario = None