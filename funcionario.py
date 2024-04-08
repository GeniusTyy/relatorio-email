from decimal import Decimal
from openpyxl import Workbook
from datetime import datetime
from tabulate import tabulate

import os

class Funcionario:
    """
    Classe responsável por representar um funcionário.
    """

    def __init__(
        self,
        nome: str,
        salario_base: Decimal,
        dias_trabalhados: int,
        vale_transporte: bool = False,
    ):
        """
        Inicializa um novo funcionário.

        Args:
            nome (str): O nome do funcionário.
            salario_base (Decimal): O salário base do funcionário.
            dias_trabalhados (int): O número de dias trabalhados pelo funcionário no mês.
            vale_transporte (bool, opcional): Indica se o funcionário recebe vale transporte. O padrão é False.
        """
        self.nome = nome
        self.salario_base = salario_base
        self.dias_trabalhados = dias_trabalhados
        self.vale_transporte = vale_transporte

        self._salario_bruto = Decimal(0)
        self._salario_liquido = Decimal(0)

        self._inss = Decimal(0)
        self._deducao_inss = Decimal(0)

        self._irpf = Decimal(0)
        self._deducao_irpf = Decimal(0)

    def calcula_salario_bruto(self) -> Decimal:
        """
        Calcula o salário bruto do funcionário.

        Returns:
            Decimal: O salário bruto calculado.
        Raises:
            ValueError: Se o salário base for menor ou igual a zero, ou se o número de dias trabalhados for menor ou igual a zero ou maior que 30.
        """
        if (
            self.salario_base <= Decimal(0)
            or self.dias_trabalhados <= 0
            or self.dias_trabalhados > 30
        ):
            raise ValueError("Salário base ou dias trabalhados inválidos.")

        self._salario_bruto = (self.salario_base / Decimal(30)) * Decimal(
            self.dias_trabalhados
        )
        return self._salario_bruto

    def calcula_inss(self) -> Decimal:
        """
        Calcula a contribuição de INSS do funcionário.

        Returns:
            Decimal: O valor da contribuição de INSS calculado.
        """
        if not self._salario_bruto:
            self.calcula_salario_bruto()

        faixas_inss = [
            (Decimal(0), Decimal(1412), Decimal(0.075), Decimal(0)),
            (Decimal(1412.01), Decimal(2666.67), Decimal(0.09), Decimal(21.18)),
            (Decimal(2666.68), Decimal(4000.02), Decimal(0.12), Decimal(101.18)),
            (Decimal(4000.03), Decimal(7786.01), Decimal(0.14), Decimal(181.18)),
        ]

        for faixa in faixas_inss:
            if faixa[0] <= self._salario_bruto <= faixa[1]:
                self._inss = min(
                    (self._salario_bruto * faixa[2]) - faixa[3], Decimal(908.85)
                )
                self._aliquota_inss = faixa[2]
                self._deducao_inss = faixa[3]
                return self._inss

        self._inss = min(self._salario_bruto * Decimal(0.14), Decimal(908.85))
        self._deducao_inss = Decimal(0)
        return self._inss

    def calcula_vale_transporte(self) -> Decimal:
        """
        Calcula o desconto do Vale transporte.
        """
        self._aliquota_vale_transporte = Decimal(0.06)
        if self.vale_transporte:
            self._vale_transporte = self.salario_base * self._aliquota_vale_transporte
            return self._vale_transporte

        self._vale_transporte = 0
        return self._vale_transporte
        
        
    

    def calcula_irpf(self) -> Decimal:
        """
        Calcula o desconto do Imposto de Renda (IR) para Pessoa Física (PF) do funcionário.

        Returns:
            Decimal: Valor do desconto do IRPF calculado.
        """
        if not self._salario_bruto:
            self.calcula_salario_bruto()

        tabela_irpf = [
            (Decimal(0), Decimal(2259.20), Decimal(0), Decimal(0)),
            (Decimal(2259.20), Decimal(2826.65), Decimal(0.075), Decimal(158.40)),
            (Decimal(2826.66), Decimal(3751.05), Decimal(0.15), Decimal(370.40)),
            (Decimal(3751.06), Decimal(4664.68), Decimal(0.225), Decimal(651.73)),
            (Decimal(4664.69), Decimal("Infinity"), Decimal(0.275), Decimal(884.96)),
        ]

        for faixa in tabela_irpf:
            if faixa[0] <= self._salario_bruto <= faixa[1]:
                self._irpf = (self._salario_bruto * faixa[2]) - faixa[3]
                self._deducao_irpf = faixa[3]
                self._aliquota_irpf = faixa[2]
                return self._irpf

        return Decimal(0)  # Retorna 0 se o salário não se enquadrar em nenhuma faixa.

    def calcula_salario_liquido(self) -> Decimal:
        """
        Calcula o salário líquido do funcionário.

        Returns:
            Decimal: O salário líquido calculado.
        """
        inss = self.calcula_inss()
        irpf = self.calcula_irpf()

        if self.vale_transporte:
            vt = self.calcula_vale_transporte()
            self._salario_liquido = self._salario_bruto - (inss + irpf + vt)
            return self._salario_liquido
            
        self._salario_liquido = self._salario_bruto - (inss + irpf)  
        
        return self._salario_liquido


    def exportar_excel(self) -> None:
        # Cria um novo Workbook
        wb = Workbook()
        
        # Ativa a primeira planilha (por padrão)
        ws = wb.active
        
        # Define os cabeçalhos
        ws.append(["Nome", "Salario Base", "Dias Trabalhados"])
        
        # Adiciona os dados
        ws.append([self.nome, self.salario_base, self.dias_trabalhados])
        
        # Salva o arquivo Excel
        wb.save('relatorio.xlsx')


    def relatorio(self):
        os.system('cls || clear')
        print("=="*25)
        print(f"{'RELATORIO':^50}")
        print("=="*25)

        print(f"Data: {datetime.now().strftime('%d-%m-%Y')} \nHora: {datetime.now().strftime('%H:%M:%S')}")
        print("--"*25)

        print(f"Nome: {'':<18}|{self.nome.capitalize()}")
        print(f"Salário Base: {'':<10}|R$ {self.salario_base:.2f}")
        print(f"Dias Trabalhados:{'':<7}|{self.dias_trabalhados:02d}")
        
        print("--"*25)
        salario_bruto = self.calcula_salario_bruto()
        print(f"Salário Bruto:{'':<10}|R$ {salario_bruto:.2f}")
        print("--"*25)
        
        print('\n')
        
        print("--"*25)
        print(f"{'DESCONTOS':^50}")
        print("--"*25)

        # Calculando o desconto do vale transporte para exibir na tela
        vale_transporte = self.calcula_vale_transporte()
        if self.vale_transporte:
            vale_transporte = self.calcula_vale_transporte()
            print(f"Aliquota:{'':<15}|{(self._aliquota_vale_transporte*100):.1f}%")
        print(f"Vale Transporte:{'':<8}|R$ {vale_transporte:.2f}")
        print("--"*25)
        

        inss = self.calcula_inss()
        print(f"Aliquota:{'':<15}|{self._aliquota_inss*100:.1f}%")
        print(f"Dedução:{'':<16}|R$ {self._deducao_inss:.2f}")
        print(f"INSS:{'':<19}|R$ {inss:.2f}")
        print("--"*25)
        
        irpf = self.calcula_irpf()
        print(f"Aliquota:{'':<15}|{self._aliquota_irpf*100:.1f}%")
        print(f"Dedução:{'':<16}|R$ {self._deducao_irpf:.2f}")
        print(f"IRPF:{'':<19}|R$ {irpf:.2f}")
        print("--"*25)
        
        salario_liquido = self.calcula_salario_liquido()
        print(f"Salário Liquido:{'':<8}|R$ {salario_liquido:.2f}")
        print("--"*25)


        


if __name__ == '__main__':
    
    func1 = Funcionario("Tais", 3000, 30)

    func1.relatorio()
