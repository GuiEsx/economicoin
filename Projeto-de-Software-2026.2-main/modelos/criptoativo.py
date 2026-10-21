from decimal import Decimal

from modelos.instrumento import Instrumento


class Criptoativo(Instrumento):

    def calcular_volatilidade(self):
        return (
            "Critério: preços horários "
            "em uma janela de 24 horas."
        )

    def formatar_valor(self, valor):
        valor = Decimal(str(valor))

        return (
            f"{self.codigo} {valor:.8f}"
        )

    def __str__(self):
        return (
            f"{self.codigo} - Criptoativo"
        )
