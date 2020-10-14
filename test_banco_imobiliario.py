from _pytest.config.argparsing import ArgumentError
import pytest, random

from banco_imobiliario import *

def test_dado():
    random.seed(2)
    assert dado() == 1
    random.seed(1)
    assert dado() == 2
    random.seed(7)
    assert dado() == 3
    random.seed(0)
    assert dado() == 4
    random.seed(5)
    assert dado() == 5
    random.seed(19)
    assert dado() == 6

    random.seed()

def test_atributos_propriedade():
    assert Propriedade().preco == 300
    assert Propriedade().aluguel == 60

    propriedade = Propriedade(preco=300, aluguel=30)
    assert propriedade.preco == 300
    assert propriedade.aluguel == 30
    assert not propriedade.proprietario

    jogador = Jogador()
    propriedade.proprietario = jogador
    assert propriedade.proprietario == jogador

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

def test_tabuleiro():
    with pytest.raises(TypeError) as error:
            Tabuleiro()

    assert "__init__() missing 2 required positional arguments: 'jogadores' and 'propriedades'" in str(error.value)

    with pytest.raises(ValueError) as error:
            Tabuleiro(propriedades=[], jogadores=[])

    assert "o tabuleiro precisa de pelo menos 2 jogadores" in str(error.value)

    with pytest.raises(ValueError) as error:
            Tabuleiro(propriedades=[], jogadores=[Jogador(), Jogador()])

    assert "o tabuleiro precisa de pelo menos 1 propriedade" in str(error.value)

    for valor_invalido in [None, "Não é um número", {}, (), [], -1]:
        with pytest.raises(ValueError) as error:
                Tabuleiro(propriedades=[Propriedade()], jogadores=[Jogador(), Jogador()], reembolso=valor_invalido)

        assert f"o valor do reembolso deve ser um número maior ou igual a 0: {valor_invalido}" in str(error.value)

def test_jogadores_no_tabuleiro():
    propriedade = Propriedade()
    jogador_impulsivo = Jogador(estrategia=impulsivo)
    jogador_cauteloso = Jogador(estrategia=cauteloso)
    tabuleiro = Tabuleiro(jogadores=[jogador_impulsivo, jogador_cauteloso], propriedades=[propriedade]*20)

    assert tabuleiro.reembolso == 100
    assert Tabuleiro(jogadores=[jogador_impulsivo, jogador_cauteloso], propriedades=[propriedade], reembolso=200).reembolso == 200

    assert tabuleiro.jogadores == {
        jogador_impulsivo: 0,
        jogador_cauteloso: 0
    }
    assert len(tabuleiro.propriedades) == 21

    tabuleiro.andar(jogador_impulsivo, 6)
    assert tabuleiro.jogadores[jogador_impulsivo] == 6
    assert jogador_impulsivo.saldo == 0
    assert propriedade.proprietario == jogador_impulsivo

    tabuleiro.andar(jogador_impulsivo, 6)
    assert tabuleiro.jogadores[jogador_impulsivo] == 12
    assert jogador_impulsivo.saldo == 0
    assert propriedade.proprietario == jogador_impulsivo

    tabuleiro.andar(jogador_impulsivo, 6)
    assert tabuleiro.jogadores[jogador_impulsivo] == 18

    tabuleiro.andar(jogador_impulsivo, 6)
    assert tabuleiro.jogadores[jogador_impulsivo] == 4
    assert jogador_impulsivo.saldo == 100

def test_simula_jogadores_no_tabuleiro():
    propriedade_200 = Propriedade(preco=200, aluguel=60)
    propriedade_250 = Propriedade(preco=250, aluguel=60)
    jogador_impulsivo = Jogador(estrategia=impulsivo)
    jogador_cauteloso = Jogador(estrategia=cauteloso)
    tabuleiro = Tabuleiro(jogadores=[jogador_impulsivo, jogador_cauteloso], propriedades=[propriedade_200, propriedade_250])

    for (jogador, passos, posicao, saldo_jogador, propriedade, proprietario, saldo_proprietario) in [
        (jogador_impulsivo, 1, 1, 100, propriedade_200, jogador_impulsivo, 100),
        (jogador_cauteloso, 1, 1, 240, propriedade_200, jogador_impulsivo, 160),
        (jogador_impulsivo, 1, 2, 160, propriedade_250, None, None),
        (jogador_cauteloso, 2, 1, 280, propriedade_200, jogador_impulsivo, 220),
        (jogador_impulsivo, 2, 2, 70, propriedade_250, jogador_impulsivo, 70),
        (jogador_cauteloso, 1, 2, 220, propriedade_250, jogador_impulsivo, 130),
        (jogador_impulsivo, 1, 1, 230, propriedade_200, jogador_impulsivo, 230),
        (jogador_cauteloso, 1, 1, 260, propriedade_200, jogador_impulsivo, 290),
        (jogador_impulsivo, 1, 2, 290, propriedade_250, jogador_impulsivo, 290),
        (jogador_cauteloso, 1, 2, 200, propriedade_250, jogador_impulsivo, 350),
        (jogador_impulsivo, 1, 1, 450, propriedade_200, jogador_impulsivo, 450),
        (jogador_cauteloso, 1, 1, 240, propriedade_200, jogador_impulsivo, 510),
        (jogador_impulsivo, 1, 2, 510, propriedade_250, jogador_impulsivo, 510),
        (jogador_cauteloso, 1, 2, 180, propriedade_250, jogador_impulsivo, 570),
    ]:
        tabuleiro.andar(jogador, passos)
        assert jogador.saldo == saldo_jogador
        assert tabuleiro.jogadores[jogador] == posicao
        assert tabuleiro.propriedades[posicao] == propriedade
        if proprietario:
            assert propriedade.proprietario == proprietario
            assert proprietario.saldo == saldo_proprietario

def test_partida():
    jogadores=[
        Jogador(impulsivo), 
        Jogador(cauteloso),
        Jogador(aleatorio),
        Jogador(exigente),
    ]
    random.seed(0)
    partida = Partida(jogadores=jogadores)

    assert partida.tabuleiro.jogadores == {
        jogadores[2]: 0,
        jogadores[1]: 0,
        jogadores[3]: 0,
        jogadores[0]: 0,
    }
    random.seed()