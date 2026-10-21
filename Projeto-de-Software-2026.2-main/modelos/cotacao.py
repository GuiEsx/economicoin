from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class Cotacao:
    moeda_origem: str
    moeda_destino: str
    valor: object
    horario: datetime

    def __str__(self):
        return (
            f"{self.moeda_origem} -> {self.moeda_destino}: "
            f"{self.valor} ({self.horario})"
        )
