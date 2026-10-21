class Dinheiro:

    def __init__(self, valor, moeda):
        self.__valor = valor
        self.__moeda = moeda.upper()

    @property
    def valor(self):
        return self.__valor

    @property
    def moeda(self):
        return self.__moeda

    def __add__(self, outro):

        if not isinstance(outro, Dinheiro):
            raise TypeError("Operação permitida apenas entre objetos Dinheiro.")

        if self.__moeda != outro.__moeda:
            raise ValueError("Não é permitido somar moedas diferentes.")

        return Dinheiro(
            self.__valor + outro.__valor,
            self.__moeda
        )

    def __str__(self):
        return f"{self.__valor:.2f} {self.__moeda}"
