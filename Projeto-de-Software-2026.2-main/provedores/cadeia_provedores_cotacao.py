from modelos.exceptions import ProvedorNaoAtendeError
from provedores.provedor_cotacao import ProvedorCotacao


class ProvedorCotacaoEmCadeia(ProvedorCotacao):
    """
    Elo da Chain of Responsibility.

    Pede ao seu provedor que atenda a solicitação. Se o
    provedor responder que o instrumento não é com ele
    (ProvedorNaoAtendeError), repassa ao próximo elo.

    Qualquer outro erro (falha de rede, HTTP, ativo
    inexistente) para a cadeia e sobe com a mensagem
    original, para não ser confundido com "não é comigo".
    """

    def __init__(self, provedor, proximo=None):
        self._provedor = provedor
        self._proximo = proximo

    def obter_cotacao(self, instrumento, moeda_referencia):
        try:
            return self._provedor.obter_cotacao(
                instrumento,
                moeda_referencia
            )
        except ProvedorNaoAtendeError:
            if self._proximo is not None:
                return self._proximo.obter_cotacao(
                    instrumento,
                    moeda_referencia
                )

            raise ProvedorNaoAtendeError(
                f"Nenhum provedor atende cotação "
                f"para {instrumento.codigo}."
            ) from None

    def obter_historico(self, instrumento):
        try:
            return self._provedor.obter_historico(
                instrumento
            )
        except ProvedorNaoAtendeError:
            if self._proximo is not None:
                return self._proximo.obter_historico(
                    instrumento
                )

            raise ProvedorNaoAtendeError(
                f"Nenhum provedor atende histórico "
                f"para {instrumento.codigo}."
            ) from None
