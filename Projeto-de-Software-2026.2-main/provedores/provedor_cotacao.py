from abc import ABC, abstractmethod


class ProvedorCotacao(ABC):

    @abstractmethod
    def obter_cotacao(
        self,
        instrumento,
        moeda_referencia
    ):
        pass
