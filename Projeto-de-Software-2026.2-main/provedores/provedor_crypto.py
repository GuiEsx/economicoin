import json
import os

from datetime import datetime, timedelta, timezone
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

from modelos.criptoativo import Criptoativo
from modelos.exceptions import (
    AtivoDesconhecidoError,
    ProvedorNaoAtendeError
)
from adaptadores.adaptador_coingecko import AdaptadorCoinGecko
from provedores.provedor_cotacao import ProvedorCotacao


class ProvedorCripto(ProvedorCotacao):

    URL_BASE = "https://api.coingecko.com/api/v3"

    def __init__(self, api_key=None):
        # A API pública da CoinGecko funciona sem chave.
        # Uma chave demo é opcional e vem de fora do código.
        self.api_key = api_key or os.environ.get(
            "COINGECKO_API_KEY"
        )

    def _cabecalhos(self):
        cabecalhos = {
            "User-Agent": "Painel-de-Moedas-e-Economia/1.0"
        }

        if self.api_key:
            cabecalhos["x-cg-demo-api-key"] = self.api_key

        return cabecalhos

    def obter_cotacao(
        self,
        instrumento,
        moeda_referencia
    ):

        if not isinstance(
            instrumento,
            Criptoativo
        ):
            raise ProvedorNaoAtendeError(
                "Este provedor atende apenas "
                "criptoativos."
            )

        moeda_referencia = moeda_referencia.upper()
        codigo = instrumento.codigo.upper()

        if moeda_referencia != "BRL":
            raise ValueError(
                "Nesta etapa a referência é BRL."
            )

        parametros = urlencode({
            "vs_currency": moeda_referencia.lower(),
            "symbols": codigo.lower(),
            "include_tokens": "top"
        })

        url = (
            f"{self.URL_BASE}/coins/markets?"
            f"{parametros}"
        )

        requisicao = Request(
            url,
            headers=self._cabecalhos()
        )

        try:

            with urlopen(
                requisicao,
                timeout=10
            ) as resposta:

                dados = json.loads(
                    resposta.read().decode("utf-8")
                )

        except HTTPError as erro:

            if erro.code in (401, 403):
                raise ValueError(
                    "A CoinGecko recusou o acesso "
                    "(chave inválida ou limite de uso)."
                )

            try:
                mensagem = erro.read().decode(
                    "utf-8"
                )
            except Exception:
                mensagem = ""

            raise ValueError(
                f"Erro ao consultar a CoinGecko: "
                f"HTTP {erro.code}. "
                f"{mensagem}"
            )

        except URLError as erro:

            raise ValueError(
                "Não foi possível conectar à CoinGecko."
            ) from erro

        except json.JSONDecodeError as erro:

            raise ValueError(
                "A CoinGecko retornou uma "
                "resposta inválida."
            ) from erro

        return AdaptadorCoinGecko.adaptar_cotacao(
            dados,
            codigo,
            moeda_referencia
        )

    def obter_historico(
        self,
        instrumento,
        moeda_referencia="BRL",
        horas=24
    ):
        """
        Obtém preços históricos horários de um criptoativo.

        Os dados são obtidos da CoinGecko e organizados
        em intervalos de uma hora.
        """

        if not isinstance(
            instrumento,
            Criptoativo
        ):
            raise ProvedorNaoAtendeError(
                "Este provedor atende apenas "
                "criptoativos."
            )

        moeda_referencia = moeda_referencia.upper()
        codigo = instrumento.codigo.upper()

        if moeda_referencia != "BRL":
            raise ValueError(
                "Nesta etapa a referência é BRL."
            )

        if horas <= 0:
            raise ValueError(
                "A quantidade de horas deve ser "
                "maior que zero."
            )

        # Primeiro descobrimos o ID interno
        # usado pela CoinGecko para o ativo.
        parametros = urlencode({
            "vs_currency": moeda_referencia.lower(),
            "symbols": codigo.lower(),
            "include_tokens": "top"
        })

        url_mercado = (
            f"{self.URL_BASE}/coins/markets?"
            f"{parametros}"
        )

        requisicao_mercado = Request(
            url_mercado,
            headers=self._cabecalhos()
        )

        try:

            with urlopen(
                requisicao_mercado,
                timeout=10
            ) as resposta:

                dados_mercado = json.loads(
                    resposta.read().decode("utf-8")
                )

        except HTTPError as erro:

            if erro.code in (401, 403):
                raise ValueError(
                    "A CoinGecko recusou o acesso "
                    "(chave inválida ou limite de uso)."
                )

            raise ValueError(
                f"Erro ao consultar a CoinGecko: "
                f"HTTP {erro.code}."
            )

        except URLError as erro:

            raise ValueError(
                "Não foi possível conectar à CoinGecko."
            ) from erro

        except json.JSONDecodeError as erro:

            raise ValueError(
                "A CoinGecko retornou uma "
                "resposta inválida."
            ) from erro

        if not dados_mercado:
            raise AtivoDesconhecidoError(codigo)

        coin_id = dados_mercado[0].get("id")

        if not coin_id:
            raise AtivoDesconhecidoError(codigo)

        # Consulta aproximadamente as últimas 24 horas.
        agora = datetime.now(timezone.utc)
        inicio = agora - timedelta(hours=horas)

        parametros_historico = urlencode({
            "vs_currency": moeda_referencia.lower(),
            "from": int(inicio.timestamp()),
            "to": int(agora.timestamp())
        })

        url_historico = (
            f"{self.URL_BASE}/coins/"
            f"{coin_id}/market_chart/range?"
            f"{parametros_historico}"
        )

        requisicao_historico = Request(
            url_historico,
            headers=self._cabecalhos()
        )

        try:

            with urlopen(
                requisicao_historico,
                timeout=10
            ) as resposta:

                dados_historico = json.loads(
                    resposta.read().decode("utf-8")
                )

        except HTTPError as erro:

            if erro.code in (401, 403):
                raise ValueError(
                    "A CoinGecko recusou o acesso "
                    "(chave inválida ou limite de uso)."
                )

            raise ValueError(
                f"Erro ao consultar o histórico "
                f"da CoinGecko: HTTP {erro.code}."
            )

        except URLError as erro:

            raise ValueError(
                "Não foi possível conectar à CoinGecko."
            ) from erro

        except json.JSONDecodeError as erro:

            raise ValueError(
                "A CoinGecko retornou um histórico "
                "inválido."
            ) from erro

        return AdaptadorCoinGecko.adaptar_historico(
            dados_historico,
            horas
        )
