from xmlrpc.server import SimpleXMLRPCServer

print("Servidor do banco...")

server = SimpleXMLRPCServer(("localhost", 8000))

# [id, Nome, Banco, Número da Conta Bancária, Número da Agência, Número do Cartão de Crédito, PIN, Valor da Conta, Mensagem de aviso]
clientes = [[1, "Humberto Pereira", "Bradesco", 12345, 100, 987654, 321, 1000, ""],
            [2, "Welerson Assis", "Itau", 54321, 200, 456789, 123, 1000, ""]]

verificador = False
dados = None
conta_Cliente = None
id = None


def verificacao(banco, conta, agencia, pin):
    global verificador, id
    for dados in clientes:

        if dados[2] == banco and dados[3] == conta and dados[4] == agencia and dados[6] == pin:
            print("Conta aceita")
            id = dados[0]
            return 1

    if verificador is False:
        return "Conta errada - Digite novamente...\n-------------------------------"


def mensagem(banco, conta, agencia, pin):

    for dados in clientes:
        if dados[2] == banco and dados[3] == conta and dados[4] == agencia and dados[6] == pin:

            return "Bem-vindo Senhor(a) " + str(dados[1]) + "\nMensagem: " + str(dados[8])


def transacao(op, banco_Destino, conta_Destino, agencia_Destino, valor):

    global id
    if op == 1:

        texto = "O valor a ser recebido do banco " + str(banco_Destino) + " de conta " + str(conta_Destino) + " e de número de agência " + str(agencia_Destino) +" é de: " + str(valor)
        for contas in clientes:

            if banco_Destino == contas[2] and conta_Destino == contas[3] and agencia_Destino == contas[4]:
                contas[8] = texto
                return texto

    elif op == 2:

        for contas in clientes:

            if id == contas[0]:
                contas[7] = contas[7] - valor
                if contas[7] < 0:

                    contas[7] = contas[7] + valor
                    return 'Você não tem dinheiro suficiente na conta'

            if banco_Destino == contas[2] and conta_Destino == contas[3] and agencia_Destino == contas[4]:
                contas[7] = contas[7] + valor

        return clientes


server.register_function(verificacao)
server.register_function(mensagem)
server.register_function(transacao)

server.serve_forever()
