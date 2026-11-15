# Painel de Moedas e Economia

Projeto acadêmico em Python para consultar e gerenciar moedas fiduciárias e criptoativos, acompanhar cotações e posições em carteira, registrar compras e analisar riscos.

O código-fonte está na pasta [`Projeto-de-Software-2026.2-main/`](Projeto-de-Software-2026.2-main/). Os exemplos abaixo mostram trechos das implementações existentes nesse projeto.

## Funcionalidades

* **RF1** – Consultar cotação
* **RF2** – Trabalhar com dinheiro sem misturar moedas implicitamente
* **RF3** – Criar instrumentos fiduciários e criptoativos
* **RF4** – Exibir valores e calcular volatilidade
* **RF5** – Adicionar posição
* **RF6** – Consultar cotação multifonte
* **RF7** – Comprar ativo
* **RF8** – Tratar erros
* **RF9** – Analisar risco da carteira
* **RF10** – Armazenar cotações em cache

## Tecnologias e serviços externos

* Python e Programação Orientada a Objetos
* `Decimal` para valores numéricos financeiros
* [Frankfurter](https://www.frankfurter.dev/) para cotações e históricos de moedas fiduciárias
* [CoinGecko](https://www.coingecko.com/) para cotações e históricos de criptoativos
* PlantUML para o diagrama de classes

## Executar

Na pasta do código-fonte, execute:

```bash
cd Projeto-de-Software-2026.2-main
python main.py
```

## Padrões criacionais

### Factory Method

**Implementação:** [`fabricas/criador_instrumento.py`](Projeto-de-Software-2026.2-main/fabricas/criador_instrumento.py). A classe abstrata `CriadorInstrumento` declara `criar()`. `CriadorMoedaFiat` e `CriadorCriptoativo` sobrescrevem esse método para produzir, respectivamente, `MoedaFiat` e `Criptoativo`. O menu e a demonstração RF3 usam os criadores em [`main.py`](Projeto-de-Software-2026.2-main/main.py).

**Motivo:** separar a criação de cada tipo de instrumento em um criador específico. Para adicionar um novo tipo, pode-se implementar um novo criador sem colocar sua instanciação dentro da regra de negócio que usa o instrumento. No menu, a escolha do criador concreto continua explícita, pois é a interface que pergunta ao usuário qual instrumento quer criar.

**Trecho da implementação:**

```python
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
```

**Uso no programa:**

```python
fiat = CriadorMoedaFiat().criar(codigo_fiat)
crypto = CriadorCriptoativo().criar(codigo_crypto)
```

### Abstract Factory

**Implementação:** [`fabricas/fabrica_provedores_cotacao.py`](Projeto-de-Software-2026.2-main/fabricas/fabrica_provedores_cotacao.py). `FabricaProvedoresCotacao` declara métodos para criar os dois produtos da família de provedores: o de moeda fiduciária e o de criptoativos. `FabricaProvedoresApi` implementa os métodos e retorna os provedores com logging decorado. A fábrica é usada na inicialização do [`ServicoCotacao`](Projeto-de-Software-2026.2-main/main.py).

**Motivo:** manter a criação dos provedores relacionados em um único objeto e evitar que o código de inicialização precise conhecer os detalhes de construção de cada um. Outra implementação da fábrica poderia fornecer uma família alternativa, como provedores simulados para testes. No estado atual há uma fábrica concreta; essa substituição é uma possibilidade de extensão, não uma implementação já presente.

**Trecho da implementação:**

```python
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
```

Os produtos são os **objetos provedores**, que consultam as APIs externas; a fábrica não cria as próprias APIs.

## Padrões estruturais

### Adapter

**Implementação:** [`adaptadores/adaptador_coingecko.py`](Projeto-de-Software-2026.2-main/adaptadores/adaptador_coingecko.py), utilizado por [`provedores/provedor_crypto.py`](Projeto-de-Software-2026.2-main/provedores/provedor_crypto.py).

**Motivo:** a resposta da CoinGecko tem um formato próprio. O adaptador transforma esse formato em objetos `Cotacao` e listas de `Decimal`, que são as formas usadas pelo restante do sistema. Assim, os detalhes do payload externo ficam concentrados na integração com a CoinGecko.

**Trechos da implementação e uso:**

```python
class AdaptadorCoinGecko:
    @staticmethod
    def adaptar_cotacao(dados, codigo, moeda_referencia):
        # Valida e converte a resposta externa.
        ...
        return Cotacao(
            codigo,
            moeda_referencia,
            valor,
            datetime.now()
        )
```

```python
return AdaptadorCoinGecko.adaptar_cotacao(
    dados,
    codigo,
    moeda_referencia
)
```

### Decorator

**Implementação:** [`provedores/provedor_cotacao_decorador.py`](Projeto-de-Software-2026.2-main/provedores/provedor_cotacao_decorador.py). `ProvedorCotacaoComLog` envolve um provedor concreto e é aplicado pela fábrica de provedores.

**Motivo:** acrescentar diagnóstico de consultas sem alterar as classes que acessam as APIs e sem mudar a interface esperada pelo serviço. Os registros são feitos no nível `DEBUG`.

**Trecho da implementação:**

```python
class ProvedorCotacaoComLog(ProvedorCotacaoDecorador):
    def obter_cotacao(self, instrumento, moeda_referencia):
        self._logger.debug(
            "Consultando %s em %s",
            instrumento.codigo,
            moeda_referencia
        )
        cotacao = super().obter_cotacao(
            instrumento,
            moeda_referencia
        )
        self._logger.debug(
            "Cotação recebida para %s: %s",
            instrumento.codigo,
            cotacao.valor
        )
        return cotacao
```

## Padrões comportamentais

### Strategy

**Implementação:** [`servicos/risk_analyzer.py`](Projeto-de-Software-2026.2-main/servicos/risk_analyzer.py). `EstrategiaRisco` define o contrato implementado por `EstrategiaRiscoConservadora` e `EstrategiaRiscoAgressiva`. A demonstração RF9 em [`main.py`](Projeto-de-Software-2026.2-main/main.py) escolhe a estratégia e a entrega a `avaliar_carteira`.

**Motivo:** oferecer algoritmos diferentes de análise de risco e permitir selecionar qual executar sem misturar suas regras à função que coordena a avaliação.

**Trechos da implementação e uso:**

```python
class EstrategiaRisco(ABC):
    @abstractmethod
    def avaliar(self, carteira, servico_cotacao) -> str:
        pass


class EstrategiaRiscoConservadora(EstrategiaRisco):
    def avaliar(self, carteira, servico_cotacao) -> str:
        ...


class EstrategiaRiscoAgressiva(EstrategiaRisco):
    def avaliar(self, carteira, servico_cotacao) -> str:
        ...
```

```python
return estrategia.avaliar(
    carteira,
    servico_cotacao
)
```

### Chain of Responsibility

**Implementação:** [`provedores/cadeia_provedores_cotacao.py`](Projeto-de-Software-2026.2-main/provedores/cadeia_provedores_cotacao.py), montada pelo [`ServicoCotacao`](Projeto-de-Software-2026.2-main/servicos/servicos_cotacao.py).

**Motivo:** os provedores atendem tipos diferentes de instrumento. A cadeia permite que a solicitação passe ao próximo provedor quando o atual sinaliza especificamente que não atende àquele tipo. Isso evita que o serviço precise conhecer a regra de cada provedor.

**Trecho da implementação:**

```python
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
```

Somente `ProvedorNaoAtendeError` avança a cadeia. Erros reais, como falha de rede ou resposta inválida, não são tratados como se o provedor simplesmente não atendesse à solicitação.

## Estrutura do projeto

```text
Projeto-de-Software-2026.2-main/
├── adaptadores/
├── fabricas/
├── modelos/
├── provedores/
├── servicos/
├── diagrama/
└── main.py
```

O diagrama de classes está na pasta [`diagrama/`](Projeto-de-Software-2026.2-main/diagrama/).
