from datetime import datetime, timedelta


class ServicoCotacao:

    def __init__(self, provedores, validade_cache_segundos=60):
        self.__provedores = tuple(provedores)
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

        for provedor in self.__provedores:

            try:

                cotacao = provedor.obter_cotacao(
                    instrumento,
                    moeda_referencia
                )

                self.__cache[chave] = (
                    cotacao,
                    agora
                )

                return cotacao

            except ValueError:
                continue

        raise ValueError(
            f"Nenhum provedor encontrou cotação "
            f"para {instrumento.codigo}."
        )

    def calcular_volatilidade(self, instrumento):
        """
        Obtém o histórico adequado ao instrumento
        através dos provedores e solicita ao próprio
        instrumento o cálculo da volatilidade.
        """

        for provedor in self.__provedores:

            try:

                historico = provedor.obter_historico(
                    instrumento
                )

                return instrumento.calcular_volatilidade(
                    historico
                )

            except ValueError:
                continue

        raise ValueError(
            f"Nenhum provedor encontrou histórico "
            f"para {instrumento.codigo}."
        )
