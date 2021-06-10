from xmlrpc.server import SimpleXMLRPCServer
import psycopg2
from config import config

print("Servidor do banco...")

server = SimpleXMLRPCServer(("localhost", 8000))


def verificacao(banco, conta, agencia, pin):

    data = get_data(banco, conta, agencia, pin)
    
    if len(data) == 0:
        return "Conta errada - Digite novamente...\n-------------------------------"

    else:
        return "Bem-vindo Senhor(a) " + str(data[0]['nome']) + "\nMensagem: " + str(data[0]['mensagem'])


def transacao(op, banco_destino, conta_destino, agencia_destino, banco, conta, agencia, valor):

    if op == 1:

        texto = "O valor a ser recebido do banco " + str(banco_destino) + " de conta " + str(conta_destino) + " e de número de agência " + str(agencia_destino) +" é de: " + str(valor)

        client = get_client(banco_destino, conta_destino, agencia_destino)

        if len(client) == 0:

            return "Conta não encontrada"

        else:
            retorno = insert_msg(banco_destino, conta_destino, agencia_destino, texto)

            if retorno:
                return 'Mensagem enviada'

            else:
                return 'Falha na operação'



    elif op == 2:

        client = get_client(banco_destino, conta_destino, agencia_destino)

        if len(client) == 0:

            return "Conta não encontrada"

        else:
            
            saldo_destino = check_balance(banco_destino, conta_destino, agencia_destino)

            saldo = check_balance(banco, conta, agencia)     

            novo_saldo = saldo - valor

            if  novo_saldo < 0:

                return 'Você não tem dinheiro suficiente na conta'

            else:
                retorno = operation(banco_destino, conta_destino, agencia_destino, banco, conta, agencia, valor, novo_saldo, saldo_destino)
                if retorno:
                    return "Transferência realizada"

                else:
                    return "Falha na transação"    


def insert_msg(banco_destino, conta_destino, agencia_destino, texto):

    try:

        conn = connect()

        cur = conn.cursor()

        cur.execute(f"""
                    UPDATE public.usuarios 
                    SET mensagem='{texto}'
                    WHERE banco = '{banco_destino}' AND conta = '{conta_destino}' AND agencia = '{agencia_destino}'
        """)


        conn.commit()

        cur.close()

    except Exception as error:
        print(error)

    finally:
        if conn is not None:
            conn.close()
            return True




def get_data(banco, conta, agencia, pin):

    try:

        conn = connect()

        cur = conn.cursor()

        data = []

        cur.execute(f"""
                    SELECT 
                    nome,
                    mensagem
                    FROM public.usuarios
                    WHERE banco = '{banco}' AND conta = '{conta}' AND agencia = '{agencia}' AND pin = '{pin}'
        """)

        desc = cur.description

        data = [ dict( zip( [col[0] for col in desc ], row)) for row in cur.fetchall()]

        cur.close()

    except Exception as error:
        print(error)

    finally:
        if conn is not None:
            conn.close()
            return data

def get_client(banco, conta, agencia):

    try:

        conn = connect()

        cur = conn.cursor()

        data = []

        cur.execute(f"""
                    SELECT 
                    nome,
                    mensagem
                    FROM public.usuarios
                    WHERE banco = '{banco}' AND conta = '{conta}' AND agencia = '{agencia}'
        """)

        desc = cur.description

        data = [ dict( zip( [col[0] for col in desc ], row)) for row in cur.fetchall()]

        cur.close()



    except Exception as error:
        print(error)

    finally:
        if conn is not None:
            conn.close()

    return data



def operation(banco_destino, conta_destino, agencia_destino, banco, conta, agencia, valor, novo_saldo, saldo_destino):

    try:

        conn = connect()

        cur = conn.cursor()

        cur.execute(f"""
                    UPDATE public.usuarios
                        SET saldo={novo_saldo}
                        WHERE conta = '{conta}' AND banco = '{banco}' AND agencia = '{agencia}' 
        """)

        saldo_destino +=  valor

        cur.execute(f"""
                    UPDATE public.usuarios
                        SET saldo={saldo_destino}
                        WHERE conta = '{conta_destino}' AND banco = '{banco_destino}' AND agencia = '{agencia_destino}' 
        """)

        updated_rows = cur.rowcount

        conn.commit()

        cur.close()



    except Exception as error:
        print(error)

    finally:
        if conn is not None:
            conn.close()

    return updated_rows


def check_balance(banco, conta, agencia):
    
    try:

        conn = connect()

        cur = conn.cursor()

        cur.execute(f"""
                    SELECT
                    saldo::float 
                    FROM usuarios
                    WHERE conta = '{conta}' AND banco = '{banco}' AND agencia = '{agencia}'
        """)

        balance = cur.fetchall()

        cur.close()



    except Exception as error:
        print(error)

    finally:
        if conn is not None:
            conn.close()
            return balance[0][0]

def connect():
    
    conn = None
    try:

        params = config()

        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)
		
    except Exception as error:
        print(error)

    finally:
        if conn is not None:
            return conn



server.register_function(verificacao)
server.register_function(transacao)

server.serve_forever()