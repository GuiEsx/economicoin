from datetime import datetime, timedelta

from provedores.cadeia_provedores_cotacao import (
    ProvedorCotacaoEmCadeia
)


class ServicoCotacao:

    def __init__(self, provedores, validade_cache_segundos=60):
        self.__provedores = tuple(provedores)
        self.__cadeia_provedores = None

        for provedor in reversed(self.__provedores):
            self.__cadeia_provedores = ProvedorCotacaoEmCadeia(
                provedor,
                self.__cadeia_provedores
            )

        self.__cache = {}
        self.__validade_cache = timedelta(
            seconds=validade_cache_segundos
        )

    def obter_cotacao(
        self,
        instrumento,
        moeda_referencia
    ):

        chave = (
            instrumento.codigo,
            moeda_referencia.upper()
        )

        agora = datetime.now()

        if chave in self.__cache:

            cotacao, horario_cache = self.__cache[chave]

            if agora - horario_cache < self.__validade_cache:
                return cotacao

            del self.__cache[chave]

        if self.__cadeia_provedores is None:
            raise ValueError(
                f"Nenhum provedor encontrou cotação "
                f"para {instrumento.codigo}."
            )

        cotacao = self.__cadeia_provedores.obter_cotacao(
            instrumento,
            moeda_referencia
        )
        self.__cache[chave] = (
            cotacao,
            agora
        )
        return cotacao

    def calcular_volatilidade(self, instrumento):
        """
        Obtém o histórico adequado ao instrumento
        através dos provedores e solicita ao próprio
        instrumento o cálculo da volatilidade.
        """

        if self.__cadeia_provedores is None:
            raise ValueError(
                f"Nenhum provedor encontrou histórico "
                f"para {instrumento.codigo}."
            )

        historico = self.__cadeia_provedores.obter_historico(
            instrumento
        )
        return instrumento.calcular_volatilidade(
            historico
        )
