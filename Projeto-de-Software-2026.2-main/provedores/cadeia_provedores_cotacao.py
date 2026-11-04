from provedores.provedor_cotacao import ProvedorCotacao


class ProvedorCotacaoEmCadeia(ProvedorCotacao):
    def __init__(self, provedor, proximo=None):
        self._provedor = provedor
        self._proximo = proximo

    def obter_cotacao(self, instrumento, moeda_referencia):
        try:
            return self._provedor.obter_cotacao(
                instrumento,
                moeda_referencia
            )
        except ValueError:
            if self._proximo is not None:
                return self._proximo.obter_cotacao(
                    instrumento,
                    moeda_referencia
                )

            raise ValueError(
                f"Nenhum provedor encontrou cotação "
                f"para {instrumento.codigo}."
            ) from None

    def obter_historico(self, instrumento):
        try:
            return self._provedor.obter_historico(
                instrumento
            )
        except ValueError:
            if self._proximo is not None:
                return self._proximo.obter_historico(
                    instrumento
                )

            raise ValueError(
                f"Nenhum provedor encontrou histórico "
                f"para {instrumento.codigo}."
            ) from None
