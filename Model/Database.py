import psycopg2 as pg
from psycopg2.extras import DictCursor

def conectar_BD():
    try:
        conn = pg.connect(
            dbname="ProjetoBD",
            user="postgres",
            password="senha123",
            host="localhost",
            port="5432"
        )
        return conn
    except (Exception, pg.Error) as error:
        print("Erro ao conectar ao banco de dados: ", error)
        return None

def executar_consulta(query, params=None):
    conn = conectar_BD()
    if conn:
        try:
            cursor = conn.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            conn.commit()
            return cursor
        except (Exception, pg.Error) as error:
            print("Erro ao realizar consulta: ", error)
            conn.rollback()
            return None
        finally:
            conn.close()
    else:
        return None


def selecionar_dados(query, params=None):
    conn = conectar_BD()
    if conn:
        try:
            cursor = conn.cursor(cursor_factory=DictCursor)
            if params:
                cursor.execute(query, params or ())
            else:
                cursor.execute(query)
            resultado = cursor.fetchall()
            cursor.close()
            return resultado
        except (Exception, pg.Error) as error:
            print("Erro ao realizar a consulta: ", error)
            conn.rollback()
            return []
        finally:
            conn.close()
    else:
        return []