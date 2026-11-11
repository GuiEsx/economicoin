from decimal import Decimal

from modelos.instrumento import Instrumento


class Criptoativo(Instrumento):

    def calcular_volatilidade(self, cotacoes):
        """
        Calcula a volatilidade do criptoativo.

        Critério: desvio-padrão dos retornos percentuais
        entre preços horários (janela de 24 horas).
        """

        return self._desvio_padrao_dos_retornos(cotacoes)

    def formatar_valor(self, valor):
        valor = Decimal(str(valor))

        return (
            f"{self.codigo} {valor:.8f}"
        )

    def __str__(self):
        return (
            f"{self.codigo} - Criptoativo"
        )
