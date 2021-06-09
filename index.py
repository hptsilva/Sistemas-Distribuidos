
from xmlrpc.server import SimpleXMLRPCServer

clientes = [[1, 12345, 321, 800], [2, 54321, 123, 500]]


def proccess(src_account, dest_account, value):
    src_balance = check_balance(src_account)
    dest_balance = check_balance(dest_account)

    if src_balance >= value:
        opr = operation(src_account, dest_account, src_balance, dest_balance, value)

        if opr:
            print('Transação realizado com sucesso')

        else:
            print('Transação não realizada')

    else:
        print(f'O saldo de : {src_balance} insuficiente para efetuar a transação')


def operation(src_account, dest_account, src_balance, dest_balance, value):
    try:

        conn = connect()

        cur = conn.cursor()

        new_balance = src_balance - value

        cur.execute(f"""
                    UPDATE public.usuarios
                        SET saldo={new_balance}
                        WHERE conta = '{src_account}'
        """)

        new_balance = dest_balance + value

        cur.execute(f"""
                    UPDATE public.usuarios
                        SET saldo={new_balance}
                        WHERE conta = '{dest_account}'
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


def check_balance(account):
    try:

        conn = connect()

        cur = conn.cursor()

        cur.execute(f"""
                    SELECT
                    saldo::float 
                    FROM usuarios
                    WHERE conta = '{account}'
        """)

        balance = cur.fetchall()

        cur.close()



    except Exception as error:
        print(error)

    finally:
        if conn is not None:
            conn.close()
            return balance[0][0]


print("Servidor do banco...")

server = SimpleXMLRPCServer(("localhost", 8000))

# server.register_function()

server.serve_forever()