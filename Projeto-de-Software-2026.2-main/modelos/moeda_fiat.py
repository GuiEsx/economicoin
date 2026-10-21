from decimal import Decimal

from modelos.instrumento import Instrumento


class MoedaFiat(Instrumento):

    def calcular_volatilidade(self, cotacoes):
        """
        Calcula a volatilidade da moeda fiduciária.

        A volatilidade é calculada como o desvio-padrão
        dos retornos percentuais entre cotações diárias.
        """

        if not cotacoes:
            raise ValueError(
                "É necessário informar as cotações "
                "para calcular a volatilidade."
            )

        if len(cotacoes) < 2:
            raise ValueError(
                "São necessárias pelo menos duas cotações "
                "para calcular a volatilidade."
            )

        retornos = []

        for anterior, atual in zip(
            cotacoes,
            cotacoes[1:]
        ):
            anterior = Decimal(str(anterior))
            atual = Decimal(str(atual))

            if anterior <= Decimal("0"):
                raise ValueError(
                    "As cotações devem ser maiores que zero."
                )

            retorno = (
                (atual / anterior) - Decimal("1")
            )

            retornos.append(retorno)

        media = (
            sum(retornos, Decimal("0"))
            / Decimal(str(len(retornos)))
        )

        soma_quadrados = Decimal("0")

        for retorno in retornos:
            diferenca = retorno - media
            soma_quadrados += diferenca ** 2

        variancia = (
            soma_quadrados
            / Decimal(str(len(retornos) - 1))
        )

        desvio_padrao = variancia.sqrt()

        return desvio_padrao * Decimal("100")

    def formatar_valor(self, valor):
        valor = Decimal(str(valor))

        return f"R$ {valor:.2f}".replace(".", ",")

    def __str__(self):
        return (
            f"{self.codigo} - Moeda fiduciária"
        )
