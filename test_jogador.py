from jogador import *
from propriedade import *

def test_atributos_jogador():
    assert Jogador().saldo == 300
    assert Jogador(saldo=0).saldo == 0

def test_estrategia_impulsivo():
    propriedade = Propriedade()
    jogador = Jogador()

    assert impulsivo(jogador, propriedade)
    assert not impulsivo(Jogador(saldo=0), propriedade)
    propriedade.proprietario = Jogador()
    assert not impulsivo(jogador, propriedade)

def test_estrategia_exigente():
    propriedade = Propriedade()
    jogador = Jogador()

    assert exigente(jogador, propriedade)
    assert not exigente(jogador, Propriedade(aluguel=50))
    assert not exigente(Jogador(saldo=0), propriedade)

    propriedade.proprietario = Jogador()
    assert not exigente(jogador, propriedade)

def test_estrategia_cauteloso():
    propriedade = Propriedade(preco=220)
    jogador = Jogador()

    assert cauteloso(jogador, propriedade)
    assert not cauteloso(jogador, Propriedade(preco=221))
    assert not cauteloso(Jogador(saldo=0), propriedade)

    propriedade.proprietario = Jogador()
    assert not exigente(jogador, propriedade)

def test_estrategia_aleatorio():
    propriedade = Propriedade()
    jogador = Jogador()

    random.seed(1)
    assert aleatorio(jogador, propriedade)
    random.seed(0)
    assert not aleatorio(jogador, propriedade)
    random.seed(1)
    assert not aleatorio(Jogador(saldo=0), propriedade)
    propriedade.proprietario = Jogador()
    random.seed(1)
    assert not aleatorio(jogador, propriedade)
    
    random.seed()

def test_jogador():
    jogador = Jogador()
    assert jogador
    assert jogador.saldo == 300
    assert jogador.estrategia == None
    assert jogador.__repr__() == 'Jogador(saldo=300)'

    jogador = Jogador(impulsivo, saldo=250)
    assert jogador
    assert jogador.saldo == 250
    assert jogador.estrategia == impulsivo
    assert jogador.__repr__() == 'Jogador(impulsivo, saldo=250)'

    jogador.saldo = 0
    assert jogador

    jogador.saldo = -1
    assert not jogador


def test_comprar_ou_aluguar():
    proprietario = Jogador(estrategia=impulsivo)
    propriedade = Propriedade(preco=100)

    proprietario.comprar_ou_aluguar(propriedade)

    assert proprietario.saldo == 200
    assert propriedade.proprietario == proprietario

    jogador = Jogador()
    jogador.comprar_ou_aluguar(propriedade)

    assert jogador.saldo == 240
    assert proprietario.saldo == 260

    falido = Jogador(saldo=0)
    falido.comprar_ou_aluguar(propriedade)

    assert falido.saldo == -60
    assert proprietario.saldo == 260