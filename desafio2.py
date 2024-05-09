import textwrap

def menu(): 
    menu ="""\n
    ==============================
    ========== Banco FB ==========
    ==============================\n
    Escolha abaixo a operação que deseja realizar!
    
    [ 1 ] Depositar
    [ 2 ] Sacar
    [ 3 ] Extrato
    [ 4 ] Cadastrar Usuário
    [ 5 ] Criar Conta Corrente
    [ 6 ] Listas Contas
    [ 0 ] Sair
    => """
    return input(textwrap.dedent(menu))

def depositar(saldo, valor, extrato, /):
    if valor > 0:
        saldo += valor
        extrato += f'Deposito:\t\033[0;34mR$ {valor:.2f} reais\033[m\n'
        print('\n=== Depósito realizado com sucesso.===')
    else:
        print('\n@@@ Operação falhou! O valor informado é invalido. @@@')
    return saldo, extrato

def sacar(*, saldo, valor, extrato, limite, numero_saques, limite_saques):
    excedeu_saldo = valor > saldo
    excedeu_limite = valor > limite
    excedeu_saques = numero_saques >= limite_saques

    if excedeu_saldo:
        print('\n@@@ Operação falhou! Você não tem saldo suficiente. @@@')

    elif excedeu_limite:
        print('\n@@@ Operação falhou! O valor do saque excede o limite. @@@')
        
    elif excedeu_saques:
        print('\n@@@ Operação falhou! Número máximo de saques diários excedido. @@@')

    elif valor > 0:
        saldo -= valor
        extrato += f'Saque:\t\t \033[0;31mR$ {valor:.2f}\033[m reais\n'
        numero_saques += 1
        print('\n===Saque realizado com sucesso! ===')

    else:
        print('\n @@@Operação falhou! O valor informado é inválido. @@@')
        
    return saldo, extrato

def exibir_extrato(saldo, /, *, extrato):
    print('='*20, 'Extrato', '='*20)
    print('Não foram realizada movimentações' if not extrato else extrato)
    print(f'\nSeu Saldo atual é de: \33[0;34mR$ {saldo:.2f}\033[m reais.')
    print('='*49)

def filtrar_usuario(cpf, usuarios):
    usuarios_filtrados = [usuario for usuario in usuarios if usuario['cpf'] == cpf]
    return usuarios_filtrados[0] if usuarios_filtrados else None

def criar_conta(agencia, numero_conta, usuarios):
    cpf = input('Informe o cpf do usuário: ')
    usuario = filtrar_usuario(cpf, usuarios)
    if usuario:
        print('\n=== Conta criada com sucesso ===')
        return {'agencia': agencia, 'numero_conta': numero_conta, 'usuario': usuario}
    print('\n@@@ Usuário não encontrado, fluxo de criação de conta encerada @@@')

def criar_usuario(usuarios):
    cpf = input("Informe o CPF (Somente números): ")
    usuario = filtrar_usuario(cpf, usuarios)
    
    if usuario:
        print("@@@ Ja existe usuário com esse CPF! @@@")
        return
    
    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input("Informe o endereço (Logradouro, nº - bairro - cidade/sigla do estado): ")

    usuarios.append({"nome": nome, "data_nascimento": data_nascimento, "cpf": cpf, "endereco": endereco})

    print("=== Usuário criado com sucesso! ===")

def listar_contas(contas):
    for conta in contas:
        linha  = f"""\
            Agência:\t{conta['agencia']}
            C/C:\t\t{conta['numero_conta']}
            Titular:\t{conta['usuario']['nome']}
        """
        print('=' * 100)
        print(textwrap.dedent(linha))

def main():
    LIMITE_SAQUE = 3
    AGENCIA = '0001'

    saldo = 0
    limite = 500
    extrato = ''
    numero_saques = 0
    usuarios = []
    contas = []
    while True:
        opcao = menu()

        if opcao == '1':
            print('Depositar')
            valor = float(input('Digite o valor do deposito: '))

            saldo, extrato = depositar(saldo, valor, extrato)
            
        elif opcao == '2':
            print('Sacar')
            valor = float(input('Qual o valor que você deseja sacar? '))

            saldo, extrato = sacar(
                saldo=saldo,
                valor=valor,
                extrato=extrato,
                limite=limite,
                numero_saques=numero_saques,
                limite_saques=LIMITE_SAQUE,
            )

        elif opcao == '3':
            exibir_extrato(saldo, extrato=extrato)

        elif opcao == '4':
            criar_usuario(usuarios)
        
        elif opcao == '5':
            numero_conta = len(contas) + 1
            conta = criar_conta(AGENCIA, numero_conta, usuarios)
            if conta:
                contas.append(conta)

        elif opcao == '6':
            listar_contas(contas)
                
        elif opcao == '0':
            break

        else:
            print('Operação inválida, selecione novamente a operação que deseja realizar')
    
main()