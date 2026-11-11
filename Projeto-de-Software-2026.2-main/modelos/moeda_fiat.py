from decimal import Decimal

from modelos.instrumento import Instrumento


class MoedaFiat(Instrumento):

    def calcular_volatilidade(self, cotacoes):
        """
        Calcula a volatilidade da moeda fiduciária.

        Critério: desvio-padrão dos retornos percentuais
        entre cotações diárias (janela de 30 dias).
        """

        return self._desvio_padrao_dos_retornos(cotacoes)

    def formatar_valor(self, valor):
        valor = Decimal(str(valor))

        return f"R$ {valor:.2f}".replace(".", ",")

    def __str__(self):
        return (
            f"{self.codigo} - Moeda fiduciária"
        )
