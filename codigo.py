from abc import ABC, abstractmethod
import re

class Conta(ABC):
    def __init__(self, numero: int, titular: str, cpf: str, saldo: float = 0.0):
        self._numero = numero  
        self._titular = titular
        self._cpf = cpf
        self._saldo = saldo

    @abstractmethod
    def sacar(self, valor: float):
        pass

    def depositar(self, valor: float):
        self._saldo += valor

    @property
    def saldo(self):
        return self._saldo

    @property
    def titular(self):
        return self._titular
    
    @property
    def cpf(self):
        return self._cpf


class SaldoInsuficienteException(Exception):
    def __init__(self, mensagem="Saldo insuficiente para a operação."):
        super().__init__(mensagem)


class ContaCorrente(Conta):
    def __init__(self, numero, titular, cpf, saldo=0.0, limite=500.0):
        super().__init__(numero, titular, cpf, saldo)
        self._limite = limite  

    def sacar(self, valor: float):
        if valor > (self._saldo + self._limite):
            raise SaldoInsuficienteException()
        self._saldo -= valor


class ContaPoupanca(Conta):
    def __init__(self, numero, titular, cpf, saldo=0.0, rendimento=0.02):
        super().__init__(numero, titular, cpf, saldo)
        self._rendimento = rendimento

    def sacar(self, valor: float):
        if valor > self._saldo:
            raise SaldoInsuficienteException()
        self._saldo -= valor

    def render_juros(self):
        self._saldo += self._saldo * self._rendimento


def validar_cpf(cpf):
    if not re.fullmatch(r"\d{11}", cpf):
        return False
    return True 


def criar_conta():
    while True:
        cpf = input("Digite seu CPF (apenas números, 11 dígitos): ")
        if not validar_cpf(cpf):
            print("CPF inválido. Tente novamente.")
            continue
        if cpf in banco:
            print("Esse CPF já está cadastrado.")
            continue
        break

    titular = input("Digite seu nome: ")
    numero = len(banco) + 101
    
    print("Escolha o tipo de conta:")
    print("1. Conta Corrente")
    print("2. Conta Poupança")
    tipo = input("Opção: ")
    
    if tipo == "1":
        banco[cpf] = ContaCorrente(numero, titular, cpf)
    elif tipo == "2":
        banco[cpf] = ContaPoupanca(numero, titular, cpf)
    else:
        print("Opção inválida. Conta não criada.")
        return

    print(f"Conta criada com sucesso! Número da conta: {numero}")


banco = {
    "12345678900": ContaCorrente(101, "Luis Lipe", "12345678900", 1000),
    "09876543211": ContaPoupanca(102, "Carlitcho Henriquito", "09876543211", 300)
}


def menu(conta):
    while True:
        print(f"\n--- Conta de {conta.titular} ---")
        print("1. Depositar")
        print("2. Sacar")
        print("3. Ver Saldo")
        print("4. Sair")
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            valor = float(input("Digite o valor para depositar: "))
            conta.depositar(valor)
            print(f"Depósito de R$ {valor:.2f} realizado com sucesso.")
        elif opcao == "2":
            valor = float(input("Digite o valor para sacar: "))
            try:
                conta.sacar(valor)
                print(f"Saque de R$ {valor:.2f} realizado com sucesso.")
            except SaldoInsuficienteException as e:
                print(e)  
        elif opcao == "3":
            print(f"Saldo atual: R$ {conta.saldo:.2f}")
        elif opcao == "4":
            print("Saindo...")
            break
        else:
            print("Opção inválida. Tente novamente.")


def login():
    while True:
        print("1. Fazer login")
        print("2. Criar conta")
        opcao = input("Escolha uma opção: ")
        
        if opcao == "1":
            cpf = input("Digite seu CPF: ")
            conta = banco.get(cpf)
            if conta:
                menu(conta)
            else:
                print("CPF não encontrado. Verifique os dados e tente novamente.")
        elif opcao == "2":
            criar_conta()
        else:
            print("Opção inválida. Tente novamente.")


print("--- Sistema Bancário ---")
login()
