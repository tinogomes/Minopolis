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
