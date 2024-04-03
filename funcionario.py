class Funcionario:
    """
    Classe responsável por representar um funcionário.
    """

    def __init__(self, nome: str, salario_base: float, dias_trabalhados: int, vale_transporte: bool = False):
        """
        Inicializa um novo funcionário.

        Args:
            nome (str): O nome do funcionário.
            salario_base (float): O salário base do funcionário.
            dias_trabalhados (int): O número de dias trabalhados pelo funcionário no mês.
            vale_transporte (bool, opcional): Indica se o funcionário recebe vale transporte. O padrão é False.
        """
        self.nome = nome
        self.salario_base = salario_base
        self.dias_trabalhados = dias_trabalhados
        self.vale_transporte = vale_transporte
        self._salario_bruto = 0
        self._inss = 0
        self._deducao_inss = 0

    def calcula_salario_bruto(self) -> float:
        """
        Calcula o salário bruto do funcionário.

        Returns:
            float: O salário bruto calculado.
        Raises:
            ValueError: Se o salário base for menor ou igual a zero, ou se o número de dias trabalhados for menor ou igual a zero ou maior que 30.
        """
        if self.salario_base <= 0 or self.dias_trabalhados <= 0 or self.dias_trabalhados > 30:
            raise ValueError("Salário base ou dias trabalhados inválidos.")

        self._salario_bruto = (self.salario_base / 30) * self.dias_trabalhados
        return self._salario_bruto

    def calcula_inss(self) -> float:
        """
        Calcula a contribuição de INSS do funcionário.

        Returns:
            float: O valor da contribuição de INSS calculado.
        """
        self.calcula_salario_bruto()
        faixas_inss = {
            (0, 1412): (0.075, 0),
            (1412.01, 2666.67): (0.09, 21.18),
            (2666.68, 4000.02): (0.12, 101.18),
            (4000.03, 7786.01): (0.14, 181.18)
        }

        for faixa, (aliquota, deducao) in faixas_inss.items():
            if faixa[0] <= self._salario_bruto <= faixa[1]:
                self._inss = min((self._salario_bruto * aliquota) - deducao, 908.85)
                self._deducao_inss = deducao
                return self._inss

        self._inss = min(self._salario_bruto * 0.14, 908.85)
        self._deducao_inss = 0
        return self._inss


    def calcula_irpf(self) -> float:
        """
        Calcula o desconto do Imposto de Renda (IR) para Pressoa Fisica (PF) do funcionário.

        Returns:
            float: Valor do desconto do IRPF calculado.
        """
        self.calcula_salario_bruto()
        tabela_irpf = {
            (0, 2112.00): (0, 0),
            (2112.01, 2826.65): (0.075, 158.40),
            (2826.66, 3751.05): (0.15, 370.40),
            (3751.06, 4664.68): (0.225, 651.73),
            (4664.69, float('inf')): (0.275, 884.96)
        }

        for faixa, (aliquota, deducao) in tabela_irpf.items():
            print("Faixa: ", faixa)
            print("Aliquota: ", aliquota)
            print("Deduçao: ", deducao)
            print("Salario bruto: ", self._salario_bruto)
            if faixa[0] <= self._salario_bruto <= faixa[1]:
                self._irpf = (self._salario_bruto * aliquota) - deducao
                self._deducao_irpf = deducao
                return self._irpf

            
