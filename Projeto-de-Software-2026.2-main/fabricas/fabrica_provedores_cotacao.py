from abc import ABC, abstractmethod

from provedores.provedor_cotacao import ProvedorCotacao
from provedores.provedor_cotacao_decorador import (
    ProvedorCotacaoComLog
)
from provedores.provedor_crypto import ProvedorCripto
from provedores.provedor_fiat import ProvedorFiat


class FabricaProvedoresCotacao(ABC):
    @abstractmethod
    def criar_provedor_fiat(self) -> ProvedorCotacao:
        pass

    @abstractmethod
    def criar_provedor_crypto(self) -> ProvedorCotacao:
        pass


class FabricaProvedoresApi(FabricaProvedoresCotacao):
    def criar_provedor_fiat(self):
        return ProvedorCotacaoComLog(ProvedorFiat())

    def criar_provedor_crypto(self):
        return ProvedorCotacaoComLog(ProvedorCripto())
