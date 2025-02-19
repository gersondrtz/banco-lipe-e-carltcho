from abc import ABC, abstractmethod


class Conta(ABC):
    def __init__(self, numero: int, titular: str, saldo: float = 0.0):
        self._numero = numero  
        self._titular = titular
        self._saldo = saldo

    @abstractmethod
    def depositar(self, valor: float):
        pass

    @abstractmethod
    def sacar(self, valor: float):
        pass

    def get_saldo(self):
        return self._saldo

    def get_titular(self):
        return self._titular

    def __eq__(self, outra):
        return self._numero == outra._numero

    def __lt__(self, outra):
        return self._saldo < outra._saldo


class SaldoInsuficienteException(Exception):
    def __init__(self, mensagem="Saldo insuficiente para a operação."):
        super().__init__(mensagem)


class ContaCorrente(Conta):
    def __init__(self, numero, titular, saldo=0.0, limite=500.0):
        super().__init__(numero, titular, saldo)
        self._limite = limite  

    
    def sacar(self, valor: float):
        if valor > (self._saldo + self._limite):
            raise SaldoInsuficienteException()
        self._saldo -= valor

    def depositar(self, valor: float):
        self._saldo += valor


class ContaPoupanca(Conta):
    def __init__(self, numero, titular, saldo=0.0, rendimento=0.02):
        super().__init__(numero, titular, saldo)
        self._rendimento = rendimento

 
    def sacar(self, valor: float):
        if valor > self._saldo:
            raise SaldoInsuficienteException()
        self._saldo -= valor

    def depositar(self, valor: float):
        self._saldo += valor

    def render_juros(self):
        self._saldo += self._saldo * self._rendimento



conta1 = ContaCorrente(101, "luis lipe", 1000)
conta2 = ContaPoupanca(102, "Carlitcho Henriquito", 300)


def menu(conta):
    while True:
        print(f"\n--- Conta de {conta.get_titular()} ---")
        print("1. Depositar")
        print("2. Sacar")
        print("3. Ver Saldo")
        print("4. Sair")
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            valor = float(input("Digite o valor para depositar: "))
            conta.depositar(valor)
            print(f"Depósito de R$ {valor} realizado com sucesso.")
        elif opcao == "2":
            valor = float(input("Digite o valor para sacar: "))
            try:
                conta.sacar(valor)
                print(f"Saque de R$ {valor} realizado com sucesso.")
            except SaldoInsuficienteException as e:
                print(e)  
        elif opcao == "3":
            print(f"Saldo atual: R$ {conta.get_saldo()}")
        elif opcao == "4":
            break
        else:
            print("Opção inválida. Tente novamente.")



print("--- Conta Corrente ---")
menu(conta1)

print("\n--- Conta Poupança ---")
menu(conta2)
