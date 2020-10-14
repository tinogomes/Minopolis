import random
from typing import OrderedDict

from _pytest.config.argparsing import ArgumentError

def dado(lados=6):
    return random.randint(1, lados)

def impulsivo(jogador, propriedade):
    return jogador.saldo >= propriedade.preco and not propriedade.proprietario

def exigente(jogador, propriedade):
    return propriedade.aluguel > 50 and impulsivo(jogador, propriedade)

def cauteloso(jogador, propriedade):
    return jogador.saldo - propriedade.preco >= 80 and impulsivo(jogador, propriedade)

def aleatorio(jogador, propriedade):
    return random.choice([True, False]) and impulsivo(jogador, propriedade)

class Jogador():
    def __init__(self, estrategia=None, saldo=300):
        self.saldo = saldo
        self.estrategia = estrategia
    
    def comprar_ou_aluguar(self, propriedade):
        if propriedade.proprietario and propriedade.proprietario != self:
            self.saldo -= propriedade.aluguel
            if self.saldo > 0:
                propriedade.proprietario.saldo += propriedade.aluguel
        elif self.estrategia(self, propriedade):
            self.saldo -= propriedade.preco
            propriedade.proprietario = self

class Propriedade():
    def __init__(self, preco=300, aluguel=60):
        self.preco = preco
        self.aluguel = aluguel
        self.proprietario = None

class Tabuleiro():
    def __init__(self, jogadores, propriedades, reembolso=100):
        self._valida_argumentos(jogadores, propriedades, reembolso)
        self.propriedades = [None] + propriedades
        self.jogadores = {}
        self.reembolso = reembolso

        for jogador in jogadores:
            self.jogadores[jogador] = 0

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
        self.jogadores[jogador] = nova_posicao

class Partida:
    def __init__(self, jogadores, num_propriedades=20):
        jogadores = jogadores.copy()
        random.shuffle(jogadores)

        propriedades = [Propriedade() for _ in range(num_propriedades)]
        self.tabuleiro = Tabuleiro(jogadores=jogadores, propriedades=propriedades)