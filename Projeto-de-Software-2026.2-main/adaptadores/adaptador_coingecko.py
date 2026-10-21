from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation

from modelos.cotacao import Cotacao
from modelos.exceptions import AtivoDesconhecidoError


class AdaptadorCoinGecko:
    """Converte respostas da CoinGecko para o formato do domínio."""

    @staticmethod
    def adaptar_cotacao(dados, codigo, moeda_referencia):
        if not dados:
            raise AtivoDesconhecidoError(codigo)

        moeda = dados[0]

        if "current_price" not in moeda:
            raise ValueError(
                "A CoinGecko não retornou "
                "uma cotação válida."
            )

        try:
            valor = Decimal(str(moeda["current_price"]))
        except (InvalidOperation, TypeError, ValueError) as erro:
            raise ValueError(
                "A cotação retornada pela "
                "CoinGecko é inválida."
            ) from erro

        return Cotacao(
            codigo,
            moeda_referencia,
            valor,
            datetime.now()
        )

    @staticmethod
    def adaptar_historico(dados, horas):
        precos = dados.get("prices", [])

        if not precos:
            raise ValueError(
                "A CoinGecko não retornou preços "
                "históricos."
            )

        precos_horarios = {}

        for timestamp, preco in precos:
            instante = datetime.fromtimestamp(
                timestamp / 1000,
                tz=timezone.utc
            )
            hora = instante.replace(
                minute=0,
                second=0,
                microsecond=0
            )
            precos_horarios[hora] = Decimal(str(preco))

        historico = sorted(
            precos_horarios.items(),
            key=lambda item: item[0]
        )[-horas:]

        valores = [preco for _, preco in historico]

        if len(valores) < 2:
            raise ValueError(
                "Não há dados horários suficientes "
                "para calcular a volatilidade."
            )

        return valores
