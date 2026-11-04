from abc import ABC, abstractmethod

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
        valor_total = sum(valores)

        if valor_total == 0:
            return "BAIXO"

        maior_concentracao = max(valores) / valor_total

        if maior_concentracao > 0.60:
            return "ALTO"

        return "BAIXO"


def modelo_conservador(carteira, servico_cotacao) -> str:
    return EstrategiaRiscoConservadora().avaliar(
        carteira,
        servico_cotacao
    )


def modelo_agressivo(carteira, servico_cotacao) -> str:
    return EstrategiaRiscoAgressiva().avaliar(
        carteira,
        servico_cotacao
    )


def avaliar_carteira(
    carteira,
    servico_cotacao,
    estrategia=None
) -> str:
    if estrategia is None:
        estrategia = EstrategiaRiscoConservadora()

    if isinstance(estrategia, EstrategiaRisco):
        return estrategia.avaliar(
            carteira,
            servico_cotacao
        )

    return estrategia(
        carteira,
        servico_cotacao
    )
