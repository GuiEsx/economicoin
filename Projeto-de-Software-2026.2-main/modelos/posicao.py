from decimal import Decimal

from modelos.exceptions import QuantidadeInvalidaError


class Posicao:
    def __init__(self, instrumento, quantidade):
        quantidade = Decimal(str(quantidade))

        if quantidade <= Decimal("0"):
            raise QuantidadeInvalidaError(
                "A quantidade deve ser maior que zero."
            )

        self.__instrumento = instrumento
        self.__quantidade = quantidade

    @property
    def instrumento(self):
        return self.__instrumento

    @property
    def quantidade(self):
        return self.__quantidade

    def valor_em_reais(self, servico):
        cotacao = servico.obter_cotacao(
            self.instrumento,
            "BRL"
        )

        return self.quantidade * cotacao.valor
