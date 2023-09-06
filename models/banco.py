from typing import List
from time import sleep
from datetime import datetime
from models.cliente import Cliente
from models.conta import Conta
from utils.helper import formatar_cpf
import re

contas: List[Conta] = []


def main() -> None:
    try:
        menu()
    except Exception as e:
        print(f'Ocorreu um erro inesperado: {str(e)}')
        sleep(2)
        menu()


def mensagem_inicial() -> None:
    print('\nBem vindo(a)!!')
    print('\nProjeto de um banco simples que tem as funções de criar uma conta,\nefetuar saque, depósito, '
          'transferência, listar contas ou sair. Faça bom uso!!\n')
    print('=====================================')
    print('============== ATM ==================')
    print('=========== Banco Brasil 🏦💸 =======')
    print('=====================================')


def menu() -> None:
    mensagem_inicial()

    opcoes_menu = {
        1: criar_conta,
        2: efetuar_saque,
        3: efetuar_deposito,
        4: efetuar_transferencia,
        6: listar_contas,
        7: sair_do_sistema,
    }

    while True:

        print('Selecione uma opção no menu: ')
        print('1 - Criar conta')
        print('2 - Efetuar saque')
        print('3 - Efetuar depósito')
        print('4 - Efetuar transferência')
        print('6 - Listar contas')
        print('7 - Sair do sistema')

        try:
            opcao: int = int(input('Digite o número da opção escolhida: '))
        except ValueError:
            print('Opção inválida. Por favor, insira uma opção válida.')
            continue

        funcao_menu = opcoes_menu.get(opcao)
        if funcao_menu:
            funcao_menu()
        else:
            print(f'Opção {opcao} é inválida. Por favor, insira uma opção válida.')


def sair_do_sistema():
    print('\nObrigado por usar nosso sistema!\n'
          'Tenha um ótimo dia e até logo!👋😊')
    sleep(2)
    exit(0)


def criar_conta() -> None:
    print('\nInforme os dados do cliente: ')

    nome: str = input('Nome do cliente: ')
    email: str = solicitar_email()
    cpf: str = solicitar_cpf()
    data_nascimento: str = solicitar_data_nascimento()
    senha = solicitar_senha()

    if cpf_existente(cpf):
        print('CPF já cadastrado. Por favor, insira um CPF válido.')
        return

    cpf_formatado = formatar_cpf(cpf)

    cliente: Cliente = Cliente(nome, email, cpf_formatado, data_nascimento, senha)
    conta: Conta = Conta(cliente)
    contas.append(conta)

    print('Conta criada com sucesso.')
    print('Dados da conta: ')
    print('-----------------')
    print(f'Nome do cliente: {cliente.nome}')
    print(f'Número da conta: {conta.numero}')
    print(f'CPF do cliente: {cliente.cpf}')
    print('-----------------')
    sleep(2)


def cpf_existente(cpf: str) -> bool:
    for conta in contas:
        if conta.cliente.cpf == formatar_cpf(cpf):
            return True
    return False


def solicitar_senha() -> str:
    while True:
        senha = input('Digite a senha (pelo menos 5 caracteres, sem espaços): ')
        if len(senha) >= 5 and ' ' not in senha:
            return senha
        else:
            print('A senha deve ter pelo menos 5 caracteres e não pode conter espaços.')


def solicitar_email() -> str:
    while True:
        email: str = input('E-mail do cliente: ')
        if validar_email(email):
            return email
        else:
            print('E-mail inválido. Certifique-se de inserir um e-mail válido.')


def solicitar_cpf() -> str:
    while True:
        cpf: str = input('CPF do cliente: ')
        if validar_cpf(cpf):
            return cpf
        else:
            print('CPF inválido. Certifique-se de inserir um CPF válido.')


def solicitar_data_nascimento() -> str:
    while True:
        data_nascimento: str = input('Data de nascimento do cliente (DD/MM/AAAA): ')
        if validar_data_nascimento(data_nascimento):
            return data_nascimento
        else:
            print('Data de nascimento inválida. Certifique-se de seguir o formato DD/MM/AAAA.')


def validar_data_nascimento(data_texto):
    try:
        data_nascimento = datetime.strptime(data_texto, '%d/%m/%Y')
        data_atual = datetime.now()
        return data_nascimento < data_atual
    except ValueError:
        return False


def validar_email(email):
    padrao = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(padrao, email) is not None


def validar_cpf(cpf):
    if len(cpf) == 11 and cpf.isdigit():
        return True
    else:
        return False

def efetuar_saque() -> None:
    if len(contas) > 0:
        numero: int = int(input('Informe o número da sua conta: '))

        conta: Conta = buscar_conta_por_numero(numero)

        if conta:
            valor: float = float(input('Informe o valor do saque: '))

            conta.sacar(valor)
        else:
            print(f'Não foi encontrada a conta com número {numero}')
    else:
        print('Ainda não existem contas cadastradas.')
    sleep(2)
    menu()


def efetuar_deposito() -> None:
    if len(contas) > 0:
        numero: int = int(input('Informe o número da sua conta: '))

        conta: Conta = buscar_conta_por_numero(numero)

        if conta:
            valor: float = float(input('Informe o valor do depósito: '))

            conta.depositar(valor)
        else:
            print(f'Não foi encontrada uma conta com número {numero}')

    else:
        print('Ainda não existem contas cadastradas.')
    sleep(2)
    menu()


def efetuar_transferencia() -> None:
    if len(contas) > 0:
        numero_o: int = int(input('Informe o número da sua conta: '))

        conta_o: Conta = buscar_conta_por_numero(numero_o)

        if conta_o:
            numero_d: int = int(input('Informe o número da conta destino: '))

            conta_d: Conta = buscar_conta_por_numero(numero_d)

            if conta_d:
                valor: float = float(input('Informe o valor da transferência: '))

                conta_o.transferir(conta_d, valor)
            else:
                print(f'A conta destino com número {numero_d} não foi encontrada.')
        else:
            print(f'A sua conta com número {numero_o} não foi encontrada.')
    else:
        print('Ainda não existem contas cadastradas.')
    sleep(2)
    menu()


def listar_contas() -> None:
    if len(contas) > 0:
        print('Listagem de contas')

        for conta in contas:
            print('--------------------')
            print(conta)
            print('--------------------')
            sleep(1)
    else:
        print('Não existem contas cadastradas.')
    sleep(2)
    menu()


def buscar_conta_por_numero(numero: int) -> Conta:
    c: Conta = None

    if len(contas) > 0:
        for conta in contas:
            if conta.numero == numero:
                c = conta
    return c
