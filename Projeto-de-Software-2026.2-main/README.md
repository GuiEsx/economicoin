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
* **provedores:** comunicação com as APIs externas de cotação.
* **servicos:** gerenciamento das consultas, cache e análise de risco.

O diagrama de classes UML está disponível na pasta [`diagrama/`](diagrama/).

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
