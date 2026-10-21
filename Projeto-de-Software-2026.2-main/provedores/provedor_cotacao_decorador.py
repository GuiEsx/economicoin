import logging

from provedores.provedor_cotacao import ProvedorCotacao


class ProvedorCotacaoDecorador(ProvedorCotacao):
    def __init__(self, provedor):
        self._provedor = provedor

    def obter_cotacao(self, instrumento, moeda_referencia):
        return self._provedor.obter_cotacao(
            instrumento,
            moeda_referencia
        )

    def obter_historico(self, instrumento):
        return self._provedor.obter_historico(instrumento)


class ProvedorCotacaoComLog(ProvedorCotacaoDecorador):
    def __init__(self, provedor):
        super().__init__(provedor)
        self._logger = logging.getLogger(
            f"{__name__}.{type(provedor).__name__}"
        )

    def obter_cotacao(self, instrumento, moeda_referencia):
        self._logger.debug(
            "Consultando %s em %s",
            instrumento.codigo,
            moeda_referencia
        )
        cotacao = super().obter_cotacao(
            instrumento,
            moeda_referencia
        )
        self._logger.debug(
            "Cotação recebida para %s: %s",
            instrumento.codigo,
            cotacao.valor
        )
        return cotacao

    def obter_historico(self, instrumento):
        self._logger.debug(
            "Consultando histórico de %s",
            instrumento.codigo
        )
        historico = super().obter_historico(instrumento)
        self._logger.debug(
            "Histórico de %s recebido com %d registros",
            instrumento.codigo,
            len(historico)
        )
        return historico
