import random
from time import sleep

from partida import *
from jogador import *

def dado(lados=6):
    return random.randint(1, lados)

if __name__ == "__main__":
    print('Iniciando a partida...')

    jogadores = [
        Jogador(impulsivo),
        Jogador(cauteloso),
        Jogador(exigente),
        Jogador(aleatorio),
        # Jogador(manual),
    ]

    partida = Partida(jogadores=jogadores, num_propriedades=20)
    print(f'  Tabuleiro de início '.center(50, '*'))
    print(partida)

    while not partida.acabou():
        passos = dado()
        jogador = partida.turno(passos)

        print(f' Rodada: {partida.rodadas}, passos: {passos} - {jogador}'.center(80, '*'))
        print(partida)
        if not jogador:
            print(f'{jogador} saiu do jogo')
        # sleep(1)
    
    print("E o vencedor foi:", partida.vencedor())
