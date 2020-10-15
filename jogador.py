from propriedade import Propriedade
import random

def impulsivo(jogador, propriedade):
    return jogador.saldo >= propriedade.preco and not propriedade.proprietario

def exigente(jogador, propriedade):
    return impulsivo(jogador, propriedade) and propriedade.aluguel > 50 

def cauteloso(jogador, propriedade):
    return impulsivo(jogador, propriedade) and jogador.saldo - propriedade.preco >= 80

def aleatorio(jogador, propriedade):
    return impulsivo(jogador, propriedade) and random.choice([True, False])

def manual(jogador, propriedade):
    if not impulsivo(jogador, propriedade):
        return False

    resposta = input(f"Você tem {jogador.saldo} de saldo. Você quer comprar {propriedade}? [y]/n").lower()

    return resposta in ['', 'y']

class Jogador():
    def __init__(self, estrategia=None, saldo=300):
        self.saldo = saldo
        self.estrategia = estrategia
    
    def __bool__(self):
        return self.saldo >= 0
    
    def __gt__(self, other):
        return self.saldo > other.saldo
    
    def __repr__(self):
        atributos = []
        if self.estrategia:
            atributos.append(self.estrategia.__name__)
        atributos.append(f'saldo={self.saldo}')
        return f"Jogador({', '.join(atributos)})"
    
    def comprar_ou_aluguar(self, propriedade):
        if propriedade.proprietario and propriedade.proprietario != self:
            self.saldo -= propriedade.aluguel
            if self.saldo > 0:
                propriedade.proprietario.saldo += propriedade.aluguel
        elif self.estrategia(self, propriedade):
            self.saldo -= propriedade.preco
            propriedade.proprietario = self
