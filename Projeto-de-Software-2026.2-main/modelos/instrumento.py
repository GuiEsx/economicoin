from abc import ABC, abstractmethod


class Instrumento(ABC):

    def __init__(self, codigo):
        self._codigo = codigo.upper()

    @property
    def codigo(self):
        return self._codigo

    @abstractmethod
    def calcular_volatilidade(self, cotacoes):
        """
        Calcula a volatilidade usando as cotações
        adequadas ao tipo de instrumento.
        """
        pass

    @abstractmethod
    def formatar_valor(self, valor):
        pass
