import textwrap
from datetime import datetime

# Decorator que registra a transação
def log_transacao(func):
    def regist_op(*args, **kwargs):
        print(f"\n=== LOG: Transação realizada em {datetime.now()} ===")
        return func(*args, **kwargs)
    return regist_op

def exibir_menu():
    menu_texto = """\n
    ================ MENU ================
    [d]\tDepositar
    [s]\tSacar
    [e]\tExtrato
    [nc]\tNova conta
    [lc]\tListar contas
    [nu]\tNovo usuário
    [q]\tSair
    => """
    return input(textwrap.dedent(menu_texto))

def buscar_cliente_por_cpf(cpf, clientes):
    return next((cliente for cliente in clientes if cliente["cpf"] == cpf), None)

def recuperar_conta(cliente):
    if not cliente["contas"]:
        print("\nXXX Cliente não possui conta! XXX")
        return None
    return cliente["contas"][0]

@log_transacao
def depositar(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = buscar_cliente_por_cpf(cpf, clientes)

    if not cliente:
        print("\nXXX Cliente não encontrado! XXX")
        return

    valor = float(input("Informe o valor do depósito: "))
    conta = recuperar_conta(cliente)
    if conta:
        conta["saldo"] += valor
        conta["historico"].append({"tipo": "Depósito", "valor": valor})
        print(f"Depósito de R$ {valor:.2f} realizado com sucesso.")

@log_transacao
def sacar(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = buscar_cliente_por_cpf(cpf, clientes)

    if not cliente:
        print("\nXXX Cliente não encontrado! XXX")
        return

    valor = float(input("Informe o valor do saque: "))
    conta = recuperar_conta(cliente)
    if conta:
        if valor > conta["saldo"]:
            print("\nXXX Saldo insuficiente! XXX")
        else:
            conta["saldo"] -= valor
            conta["historico"].append({"tipo": "Saque", "valor": valor})
            print(f"Saque de R$ {valor:.2f} realizado com sucesso.")

@log_transacao
def exibir_extrato(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = buscar_cliente_por_cpf(cpf, clientes)

    if not cliente:
        print("\nXXX Cliente não encontrado! XXX")
        return

    conta = recuperar_conta(cliente)
    if conta:
        print("\n================ EXTRATO ================")
        for transacao in conta["historico"]:
            print(f"{transacao['tipo']}:\tR$ {transacao['valor']:.2f}")
        print(f"\nSaldo:\n\tR$ {conta['saldo']:.2f}")
        print("==========================================")

@log_transacao
def criar_cliente(clientes):
    cpf = input("Informe o CPF (somente número): ")
    if buscar_cliente_por_cpf(cpf, clientes):
        print("\nXXX Já existe cliente com esse CPF! XXX")
        return

    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")

    novo_cliente = {
        "nome": nome,
        "cpf": cpf,
        "data_nascimento": data_nascimento,
        "endereco": endereco,
        "contas": []
    }

    clientes.append(novo_cliente)
    print("\n=== Cliente criado com sucesso! ===")

@log_transacao
def criar_conta(numero_conta, clientes, contas):
    cpf = input("Informe o CPF do cliente: ")
    cliente = buscar_cliente_por_cpf(cpf, clientes)

    if not cliente:
        print("\nXXX Cliente não encontrado, operação encerrada! XXX")
        return

    nova_conta = {
        "numero": numero_conta,
        "saldo": 0.0,
        "historico": []
    }

    contas.append(nova_conta)
    cliente["contas"].append(nova_conta)

    print("\n=== Conta criada com sucesso! ===")

def listar_contas(contas):
    for conta in contas:
        print("=" * 100)
        print(f"Conta {conta['numero']} - Saldo: R$ {conta['saldo']:.2f}")
        print("=" * 100)

def main():
    clientes = []
    contas = []

    opcoes_menu = {
        "d": depositar,
        "s": sacar,
        "e": exibir_extrato,
        "nc": criar_conta,
        "nu": criar_cliente,
        "lc": listar_contas,
        "q": exit
    }

    while True:
        opcao = exibir_menu()

        if opcao in opcoes_menu:
            if opcao == "nc":
                numero_conta = len(contas) + 1
                opcoes_menu[opcao](numero_conta, clientes, contas)
            else:
                opcoes_menu[opcao](clientes)
        else:
            print("\nXXX Operação inválida, por favor selecione novamente a operação desejada. XXX")

main()
