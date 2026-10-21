class ErroFinanceiro(Exception):
    """Classe base para erros financeiros do sistema."""
    pass


class SaldoInsuficienteError(ErroFinanceiro):
    """Erro gerado quando o saldo não é suficiente para uma operação."""

    def __init__(self, saldo_atual, valor_tentado):
        super().__init__(
            f"Saldo insuficiente. Disponível: R$ {saldo_atual:.2f}, "
            f"Tentativa de compra: R$ {valor_tentado:.2f}"
        )


class QuantidadeInvalidaError(ErroFinanceiro):
    """Erro gerado quando uma quantidade ou valor é inválido."""

    def __init__(
        self,
        mensagem="A quantidade e o valor devem ser maiores que zero."
    ):
        super().__init__(mensagem)


class AtivoDesconhecidoError(ErroFinanceiro):
    """Erro gerado quando o ativo não é encontrado por nenhum provedor."""

    def __init__(self, codigo):
        super().__init__(
            f"Ativo {codigo} não encontrado."
        )
