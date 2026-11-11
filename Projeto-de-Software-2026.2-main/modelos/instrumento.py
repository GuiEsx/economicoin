from abc import ABC, abstractmethod
from decimal import Decimal


class Instrumento(ABC):

    def __init__(self, codigo):
        self._codigo = codigo.upper()

    @property
    def codigo(self):
        return self._codigo

    @abstractmethod
    def calcular_volatilidade(self, cotacoes):
        """
        Calcula a volatilidade usando as cotações
        adequadas ao tipo de instrumento.
        """
        pass

    @abstractmethod
    def formatar_valor(self, valor):
        pass

    @staticmethod
    def _desvio_padrao_dos_retornos(cotacoes):
        """
        Desvio-padrão amostral dos retornos percentuais
        entre cotações consecutivas, em %.

        O cálculo é comum às famílias; o que muda entre
        elas é o critério das cotações recebidas
        (diárias para fiat, horárias para cripto).
        """

        if not cotacoes:
            raise ValueError(
                "É necessário informar as cotações "
                "para calcular a volatilidade."
            )

        if len(cotacoes) < 3:
            raise ValueError(
                "São necessárias pelo menos três cotações "
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

            retornos.append(
                (atual / anterior) - Decimal("1")
            )

        media = (
            sum(retornos, Decimal("0"))
            / Decimal(len(retornos))
        )

        soma_quadrados = Decimal("0")

        for retorno in retornos:
            diferenca = retorno - media
            soma_quadrados += diferenca ** 2

        variancia = (
            soma_quadrados
            / Decimal(len(retornos) - 1)
        )

        return variancia.sqrt() * Decimal("100")
