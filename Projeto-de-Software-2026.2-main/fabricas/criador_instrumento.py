from abc import ABC, abstractmethod

from modelos.criptoativo import Criptoativo
from modelos.moeda_fiat import MoedaFiat


class CriadorInstrumento(ABC):
    @abstractmethod
    def criar(self, codigo):
        pass


class CriadorMoedaFiat(CriadorInstrumento):
    def criar(self, codigo):
        return MoedaFiat(codigo)


class CriadorCriptoativo(CriadorInstrumento):
    def criar(self, codigo):
        return Criptoativo(codigo)
