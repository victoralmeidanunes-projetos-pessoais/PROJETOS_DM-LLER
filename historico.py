import sqlite3

BANCO = "historico.db"


def conectar():
    return sqlite3.connect(BANCO)


def criar_tabela():

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS historico_atualizacoes (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            arquivo TEXT NOT NULL,

            data_hora DATETIME DEFAULT CURRENT_TIMESTAMP

        )
    """)

    conn.commit()
    conn.close()


def registrar_atualizacao(arquivo):

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO historico_atualizacoes
        (
            arquivo
        )
        VALUES (?)
    """, (
        arquivo,
    ))

    conn.commit()
    conn.close()


# Cria a tabela automaticamente
criar_tabela()

