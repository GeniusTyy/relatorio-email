import pytest

from funcionario import Funcionario

@pytest.fixture
def func():
    return Funcionario("NoName", 1412.00, 30, True)


def test_create_class(func):
    
    assert func.nome == "NoName"
    assert func.salario_base == 1412.00
    assert func.dias_trabalhados == 30
    assert func.vale_transporte == True


def test_calc_salario_bruto(func):
    func.dias_trabalhados = 20
    salarioBruto = func.calcula_salario_bruto()
    assert round(salarioBruto, 2) == 941.33


    try:
        func.dias_trabalhados = 0
        func.calcula_salario_bruto()


    except ValueError as err:
        assert str(err) == "Salário base ou dias trabalhados inválidos."


def test_calc_inss_faixa_1(func):
    func.calcula_inss()
    
    assert round(func._inss, 2) == 105.90
    assert func._deducao_inss == 0.0


def test_calc_inss_faixa_2(func):
    func.salario_base = 1678.60
    func.calcula_inss()

    assert round(func._inss, 2) == 129.89
    assert func._deducao_inss == 21.18
    

def test_calc_inss_faixa_3(func):
    func.salario_base = 3500
    func.calcula_inss()

    assert round(func._inss, 2) == 318.82
    assert func._deducao_inss == 101.18


def test_calc_inss_faixa_4(func):
    func.salario_base = 5600
    func.calcula_inss()

    assert round(func._inss, 2) == 602.82
    assert func._deducao_inss == 181.18


def test_calc_inss_faixa_5(func):
    func.salario_base = 10000
    func.calcula_inss()

    assert round(func._inss, 2) != 1400

    assert round(func._inss, 2) == 908.85
    assert func._deducao_inss == 0


def test_calc_irpf_insento(func):
    func.salario_base = 1412
    func.calcula_irpf()

    assert round(func._irpf, 2) == 0
    assert func._deducao_irpf == 0


def test_calc_irpf_faixa_1(func):
    func.salario_base = 2680.79
    pass 
    
