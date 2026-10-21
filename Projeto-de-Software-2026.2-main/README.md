## Padrões estruturais

### Adapter

O `AdaptadorCoinGecko`, em `adaptadores/adaptador_coingecko.py`, converte os payloads específicos da CoinGecko para os tipos esperados internamente: cotações `Cotacao` e históricos como listas de `Decimal`. O `ProvedorCripto` usa esse adaptador depois de consultar a API. Assim, o formato externo da API não precisa se espalhar pelo domínio.

### Decorator

`ProvedorCotacaoComLog`, em `provedores/provedor_cotacao_decorador.py`, envolve um provedor e acrescenta registros de diagnóstico às consultas de cotação e histórico, mantendo a mesma interface. O `main.py` usa o decorador ao configurar os provedores. Os registros usam o nível `DEBUG`; podem ser habilitados configurando o logging da aplicação, sem alterar o provedor ou o serviço.

## Padrões criacionais

### Factory Method

Em `fabricas/criador_instrumento.py`, `CriadorInstrumento` define o método abstrato `criar`, e os criadores concretos `CriadorMoedaFiat` e `CriadorCriptoativo` instanciam, respectivamente, `MoedaFiat` e `Criptoativo`. O menu de seleção e a demonstração RF3 usam esses criadores em vez de instanciar diretamente as classes. Isso concentra a decisão de criação por tipo e permite acrescentar novos instrumentos com um criador específico.

### Abstract Factory

Em `fabricas/fabrica_provedores_cotacao.py`, `FabricaProvedoresCotacao` declara operações para criar os provedores de moedas fiduciárias e de criptoativos. `FabricaProvedoresApi` cria essa família de provedores concretos, já envolvidos pelo Decorator de logging. O `main.py` depende da fábrica para montar o `ServicoCotacao`, mantendo a configuração dos produtos fora do fluxo principal e facilitando substituir a família de provedores futuramente.

## APIs utilizadas

### Frankfurter

Utilizada para obtenção de cotações e históricos de moedas fiduciárias.

### CoinGecko

Utilizada para obtenção de cotações e históricos de criptoativos.

## Execução

É necessário ter o **Python 3** instalado.

Execute o projeto pela raiz do repositório:

```bash
python main.py
```

O sistema apresenta um menu interativo para acesso às funcionalidades implementadas.

## Programação Orientada a Objetos

O projeto utiliza conceitos de:

* Encapsulamento
* Herança
* Abstração
* Polimorfismo

# Painel de Moedas e Economia

Projeto desenvolvido para a disciplina de Projeto de Software, utilizando Programação Orientada a Objetos em Python.

## Sobre o projeto

O **Painel de Moedas e Economia** é um sistema para consulta e gerenciamento de moedas fiduciárias e criptoativos, permitindo trabalhar com cotações, posições em carteira, compras de ativos e análise de risco.

O projeto utiliza diferentes provedores de cotação e possui um mecanismo de cache para evitar consultas externas repetidas em curto intervalo.

## Funcionalidades

O projeto implementa os requisitos funcionais:

* **RF1** – Consultar cotação
* **RF2** – Trabalhar com dinheiro
* **RF3** – Instrumentos
* **RF4** – Exibição e volatilidade
* **RF5** – Adicionar posição
* **RF6** – Consultar cotação multifonte
* **RF7** – Comprar ativo
* **RF8** – Tratamento de erros
* **RF9** – Análise de risco
* **RF10** – Cache de cotações

## Tecnologias

* Python
* Programação Orientada a Objetos
* Decimal
* Frankfurter API
* CoinGecko API
* PlantUML

## Estrutura do projeto

```text
diagrama/
├── diagrama.puml
└── diagrama.png

adaptadores/
└── adaptador_coingecko.py

fabricas/
├── criador_instrumento.py
└── fabrica_provedores_cotacao.py

modelos/
├── carteira.py
├── cotacao.py
├── criptoativo.py
├── dinheiro.py
├── exceptions.py
├── instrumento.py
├── moeda_fiat.py
└── posicao.py

provedores/
├── provedor_cotacao.py
├── provedor_crypto.py
├── provedor_cotacao_decorador.py
└── provedor_fiat.py

servicos/
├── risk_analyzer.py
└── servicos_cotacao.py

.gitignore
README.md
main.py
```

## Arquitetura

O projeto está organizado em três camadas principais:

* **modelos:** entidades e regras do domínio, como moedas, criptoativos, dinheiro, posições e carteiras.
* **adaptadores:** conversão das respostas externas para os formatos usados pelo domínio.
* **provedores:** comunicação com as APIs externas de cotação.
* **servicos:** gerenciamento das consultas, cache e análise de risco.

O diagrama de classes UML está disponível na pasta [`diagrama/`](diagrama/).
