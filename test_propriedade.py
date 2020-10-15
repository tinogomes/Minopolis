from propriedade import *
from jogador import *

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
