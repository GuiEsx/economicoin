from decimal import Decimal

from modelos.posicao import Posicao
from modelos.criptoativo import Criptoativo

from modelos.exceptions import (
    SaldoInsuficienteError,
    QuantidadeInvalidaError
)


class Carteira:

    def __init__(self):
        self.__posicoes = []

    def adicionar_posicao(self, instrumento, quantidade):
        posicao = Posicao(
            instrumento,
            quantidade
        )

        self.__posicoes.append(posicao)

    def obter_posicoes(self):
        return tuple(self.__posicoes)

    def valor_total_em_reais(self, servico):
        total = Decimal("0")

        for posicao in self.__posicoes:
            total += posicao.valor_em_reais(servico)

        return total

    def exibir(self, servico):
        print("\nPOSIÇÕES DA CARTEIRA")
        print("-" * 40)

        if not self.__posicoes:
            print("Nenhuma posição cadastrada.")
            return

        for posicao in self.__posicoes:

            valor = posicao.valor_em_reais(servico)

            if isinstance(
                posicao.instrumento,
                Criptoativo
            ):
                quantidade_formatada = (
                    f"{posicao.quantidade:.8f}"
                )
            else:
                quantidade_formatada = (
                    f"{posicao.quantidade:.2f}"
                )

            print(
                f"{posicao.instrumento.codigo}: "
                f"{quantidade_formatada} "
                f"-> "
                f"R$ {valor:.2f}".replace(".", ",")
            )

        print("-" * 40)

        total = self.valor_total_em_reais(servico)

        print(
            f"TOTAL DA CARTEIRA: "
            f"R$ {total:.2f}".replace(".", ",")
        )


class CarteiraProtegida:

    def __init__(self, saldo_inicial):
        saldo_inicial = Decimal(str(saldo_inicial))

        if saldo_inicial < Decimal("0"):
            raise QuantidadeInvalidaError(
                "O saldo inicial não pode ser negativo."
            )

        self.__saldo = saldo_inicial
        self.__posicoes = []

    @property
    def saldo(self):
        return self.__saldo

    def comprar(
        self,
        instrumento,
        quantidade,
        valor_total
    ):
        quantidade = Decimal(str(quantidade))
        valor_total = Decimal(str(valor_total))

        if quantidade <= Decimal("0"):
            raise QuantidadeInvalidaError(
                "A quantidade deve ser maior que zero."
            )

        if valor_total <= Decimal("0"):
            raise QuantidadeInvalidaError(
                "O valor da operação deve ser maior que zero."
            )

        if valor_total > self.__saldo:
            raise SaldoInsuficienteError(
                self.__saldo,
                valor_total
            )

        self.__saldo -= valor_total

        self.__posicoes.append(
            Posicao(
                instrumento,
                quantidade
            )
        )

    def listar_posicoes(self):
        if not self.__posicoes:
            print("\nNenhuma posição cadastrada.")
            return

        print("\nPOSIÇÕES PROTEGIDAS")

        for posicao in self.__posicoes:
            print(
                f"{posicao.instrumento.codigo} - "
                f"{posicao.quantidade}"
            )

    def obter_posicoes(self):
        return tuple(self.__posicoes)

    def valor_total_em_reais(self, servico):
        total = Decimal("0")

        for posicao in self.__posicoes:
            total += posicao.valor_em_reais(servico)

        return total

    def exibir(self, servico):
        print("\nPOSIÇÕES DA CARTEIRA")
        print("-" * 40)

        if not self.__posicoes:
            print("Nenhuma posição cadastrada.")
            return

        for posicao in self.__posicoes:

            valor = posicao.valor_em_reais(servico)

            if isinstance(
                posicao.instrumento,
                Criptoativo
            ):
                quantidade_formatada = (
                    f"{posicao.quantidade:.8f}"
                )
            else:
                quantidade_formatada = (
                    f"{posicao.quantidade:.2f}"
                )

            print(
                f"{posicao.instrumento.codigo}: "
                f"{quantidade_formatada} "
                f"-> "
                f"R$ {valor:.2f}".replace(".", ",")
            )

        print("-" * 40)

        total = self.valor_total_em_reais(servico)

        print(
            f"TOTAL DA CARTEIRA: "
            f"R$ {total:.2f}".replace(".", ",")
        )
