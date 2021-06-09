import xmlrpc.client as xmlrpclib

client = xmlrpclib.ServerProxy("http://localhost:8000")

verificador = 0

while verificador == 0:

    print("\n-------------------------------\n")
    print("Digite o banco: ")
    banco = str(input())
    print("Digite o número da conta: ")
    conta = int(input())
    print("Digite o número da agência: ")
    agencia = int(input())
    print("Digite o pin da conta: ")
    pin = int(input())

    autenticacao = (client.verificacao(banco, conta, agencia, pin))

    if autenticacao == 1:

        verificador = 1
        print("\n-------------------------------\nConta aceita\n-------------------------------\n")

    else:
        print("\n-------------------------------\nConta errada")


print("-------------------------------\n")
print(client.mensagem(banco, conta, agencia, pin))
print("\n-------------------------------\n")
print("Digite o tipo de transação a ser feita: \n1 - Adicionar receita\n2 - Reduzir receita")
op = int(input())


if op == 1:
    print("Digite o valor a ser recebido: ")
    valor = int(input())
    print("Digite o banco da conta de origem do valor: ")
    bancoDestino = str(input())
    print("Digite o número da conta de origem do valor: ")
    contaDestino = int(input())
    print("Digite o número da agência da conta de origem do valor: ")
    agenciaDestino = int(input())

elif op == 2:

    print("Digite o valor a ser retirado: ")
    valor = int(input())
    print("Digite o banco da conta alvo: ")
    bancoDestino = str(input())
    print("Digite a conta alvo destinada para o valor: ")
    contaDestino = int(input())
    print("Digite o número da agência da conta alvo: ")
    agenciaDestino = int(input())

print(client.transacao(op, bancoDestino, contaDestino, agenciaDestino, valor))

