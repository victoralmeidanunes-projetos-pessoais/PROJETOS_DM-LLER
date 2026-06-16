# db_config.py

import sqlite3
import os
from datetime import datetime

# =========================================
# BANCO
# =========================================

BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

BANCO = os.path.join(
    BASE_DIR,
    "usuarios.db"
)


def conectar():
    return sqlite3.connect(BANCO)


# =========================================
# TABELA USUÁRIOS
# =========================================

def criar_tabela():

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            login TEXT NOT NULL UNIQUE,
            senha TEXT NOT NULL,
            perfil TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


# =========================================
# TABELA HISTÓRICO
# =========================================

def criar_tabela_historico():

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS historico_acessos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario TEXT NOT NULL,
            data_hora TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


# =========================================
# USUÁRIOS
# =========================================

def criar_usuario(login, senha, perfil):

    conn = conectar()
    cursor = conn.cursor()

    try:

        cursor.execute(
            """
            INSERT INTO usuarios
            (
                login,
                senha,
                perfil
            )
            VALUES (?, ?, ?)
            """,
            (
                login.strip(),
                senha.strip(),
                perfil.strip()
            )
        )

        conn.commit()

    except sqlite3.IntegrityError:

        print(f"Usuário '{login}' já existe.")

    finally:

        conn.close()


# =========================================
# LOGIN
# =========================================

def validar_login(login, senha):

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            id,
            login,
            perfil
        FROM usuarios
        WHERE UPPER(TRIM(login)) = UPPER(?)
        AND TRIM(senha) = ?
        """,
        (
            login.strip(),
            senha.strip()
        )
    )

    usuario = cursor.fetchone()

    conn.close()

    return usuario


# =========================================
# HISTÓRICO
# =========================================

def registrar_acesso(usuario):

    conn = conectar()
    cursor = conn.cursor()

    data_hora = datetime.now().strftime(
        "%d/%m/%Y %H:%M:%S"
    )

    cursor.execute(
        """
        INSERT INTO historico_acessos
        (
            usuario,
            data_hora
        )
        VALUES (?, ?)
        """,
        (
            usuario,
            data_hora
        )
    )

    conn.commit()
    conn.close()


def listar_acessos():

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            usuario,
            data_hora
        FROM historico_acessos
        ORDER BY id DESC
    """)

    dados = cursor.fetchall()

    conn.close()

    return dados