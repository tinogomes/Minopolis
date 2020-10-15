import random

from partida import *
from jogador import *

def test_gerar_preco():
    random.seed(0)
    assert gerar_preco() == 400
    assert gerar_preco() == 400
    assert gerar_preco() == 100
    assert gerar_preco() == 300
    random.seed()

def test_gerar_aluguel():
    random.seed(0)
    assert gerar_aluguel() == 90
    assert gerar_aluguel() == 90
    assert gerar_aluguel() == 30
    assert gerar_aluguel() == 70
    random.seed()

def test_partida():
    jogadores=[
        Jogador(impulsivo), 
        Jogador(cauteloso),
    ]
    random.seed(0)
    partida = Partida(jogadores=jogadores, num_propriedades=2)

    assert partida.rodadas == 0
    assert partida.ordem_jogadores == [jogadores[1], jogadores[0]]

    assert len(partida.tabuleiro.propriedades) == 3

    partida.turno(passos=1)

    assert partida.rodadas == 1

    assert partida.tabuleiro.jogadores == {
        jogadores[0]: 0,
        jogadores[1]: 1,
    }

    partida.turno(passos=1)

    assert partida.rodadas == 2
    assert partida.tabuleiro.jogadores == {
        jogadores[0]: 1,
        jogadores[1]: 1,
    }

    partida.turno(passos=1)

    assert partida.rodadas == 3
    assert partida.tabuleiro.jogadores == {
        jogadores[0]: 1,
        jogadores[1]: 2,
    }

    partida.rodadas = 999
    assert not partida.acabou()

    partida.turno(passos=1)
    assert partida.acabou()
    assert partida.vencedor() == jogadores[1]

    partida.rodadas = 999
    assert not partida.acabou()

    jogadores[1].saldo = -1
    assert partida.acabou()
    assert partida.vencedor() == jogadores[0]

    random.seed()
