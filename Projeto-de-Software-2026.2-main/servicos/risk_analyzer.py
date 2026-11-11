from abc import ABC, abstractmethod
from decimal import Decimal

from modelos.criptoativo import Criptoativo


class EstrategiaRisco(ABC):
    @abstractmethod
    def avaliar(self, carteira, servico_cotacao) -> str:
        pass


class EstrategiaRiscoConservadora(EstrategiaRisco):
    def avaliar(self, carteira, servico_cotacao) -> str:
        posicoes = carteira.obter_posicoes()

        if not posicoes:
            return "BAIXO"

        for posicao in posicoes:
            if isinstance(posicao.instrumento, Criptoativo):
                return "MODERADO"

        return "BAIXO"


class EstrategiaRiscoAgressiva(EstrategiaRisco):
    def avaliar(self, carteira, servico_cotacao) -> str:
        posicoes = carteira.obter_posicoes()

        if not posicoes:
            return "BAIXO"

        valores = [
            posicao.valor_em_reais(servico_cotacao)
            for posicao in posicoes
        ]
        valor_total = sum(valores, Decimal("0"))

        if valor_total == 0:
            return "BAIXO"

        maior_concentracao = max(valores) / valor_total

        if maior_concentracao > Decimal("0.60"):
            return "ALTO"

        return "BAIXO"


def avaliar_carteira(
    carteira,
    servico_cotacao,
    estrategia=None
) -> str:
    """
    Contexto do Strategy: executa a estratégia de risco
    recebida, sem saber qual é. Sem estratégia
    informada, usa a conservadora.
    """

    if estrategia is None:
        estrategia = EstrategiaRiscoConservadora()

    return estrategia.avaliar(
        carteira,
        servico_cotacao
    )
