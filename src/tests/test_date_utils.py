from src.common import date_utils

def test_get_month_number():
    mes = date_utils.get_month_number()
    assert mes.isdigit() and 1 <= int(mes) <= 12

def test_get_year():
    ano = date_utils.get_year()
    assert len(ano) == 4
    assert ano.isdigit()

def test_get_month_name():
    nome = date_utils.get_month_name()
    assert isinstance(nome, str)
    assert len(nome) > 0
