import random

from tabuleiro import *
from propriedade import *

def gerar_preco():
    return random.choice(range(100, 500, 50))

def gerar_aluguel():
    return random.choice(range(30, 150, 10))

class Partida:
    def __init__(self, jogadores, num_propriedades=20):
        self.rodadas = 0
        self.ordem_jogadores = random.sample(jogadores, len(jogadores))
        self.tabuleiro = Tabuleiro(
            jogadores=jogadores, 
            propriedades=self.criar_propriedades(num_propriedades)
        )
        self.proximo_jogador = 0

    def __repr__(self):
        return f'Partida(jogadores=[...], num_propriedades={len(self.tabuleiro.propriedades)-1})'
    
    def __str__(self):
        return str(self.tabuleiro)

    def criar_propriedades(self, num_propriedades):
        return [Propriedade(preco=gerar_preco(), aluguel=gerar_aluguel()) for _ in range(num_propriedades)]

    def turno(self, passos):
        self.rodadas += 1
        jogador = self.ordem_jogadores[self.proximo_jogador]
        self.tabuleiro.andar(jogador, passos)
        if jogador:
            self.proximo_jogador += 1
        else:
            self.ordem_jogadores.remove(jogador)
        if self.proximo_jogador >= len(self.ordem_jogadores):
            self.proximo_jogador = 0
        
        return jogador
    
    def acabou(self):
        return self.rodadas >= 1000 or \
            len([jogador for jogador in self.ordem_jogadores if jogador]) == 1
    
    def vencedor(self):
        return max(self.ordem_jogadores)