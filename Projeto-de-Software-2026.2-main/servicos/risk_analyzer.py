from modelos.criptoativo import Criptoativo


def modelo_conservador(carteira, servico_cotacao) -> str:
    posicoes = carteira.obter_posicoes()

    if not posicoes:
        return "BAIXO"

    for posicao in posicoes:
        if isinstance(posicao.instrumento, Criptoativo):
            return "MODERADO"

    return "BAIXO"


def modelo_agressivo(carteira, servico_cotacao) -> str:
    posicoes = carteira.obter_posicoes()

    if not posicoes:
        return "BAIXO"

    valores = []

    for posicao in posicoes:
        valor = posicao.valor_em_reais(servico_cotacao)
        valores.append(valor)

    valor_total = sum(valores)

    if valor_total == 0:
        return "BAIXO"

    maior_concentracao = max(valores) / valor_total

    if maior_concentracao > 0.60:
        return "ALTO"

    return "BAIXO"


def avaliar_carteira(
    carteira,
    servico_cotacao,
    estrategia=modelo_conservador
) -> str:

    return estrategia(
        carteira,
        servico_cotacao
    )
