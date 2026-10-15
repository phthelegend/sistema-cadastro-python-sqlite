
import sqlite3
from pathlib import Path
from contextlib import closing

# Caminho do banco de dados
BANCO = Path(__file__).resolve().parent / "cadastro.db"


# Função para criar o banco e a tabela
def criar_banco():
    with closing(sqlite3.connect(BANCO)) as conexao:
        with conexao:
            conexao.execute("""
                CREATE TABLE IF NOT EXISTS pessoas (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome TEXT NOT NULL,
                    idade INTEGER NOT NULL
                        CHECK (idade BETWEEN 0 AND 130)
                )
            """)

    print("Banco de dados preparado com sucesso!")


# Função para cadastrar uma pessoa
def cadastrar_pessoa(nome, idade):
    with closing(sqlite3.connect(BANCO)) as conexao:
        with conexao:
            cursor = conexao.execute("""
                INSERT INTO pessoas (nome, idade)
                VALUES (?, ?)
            """, (nome, idade))

            codigo = cursor.lastrowid

    print(f"Cadastro realizado! Código: {codigo}")
    return codigo


# Função para listar as pessoas
def listar_pessoas():
    with closing(sqlite3.connect(BANCO)) as conexao:
        conexao.row_factory = sqlite3.Row

        cursor = conexao.execute("""
            SELECT id, nome, idade
            FROM pessoas
            ORDER BY id
        """)

        pessoas = [dict(pessoa) for pessoa in cursor.fetchall()]

    return pessoas

# Função para editar um cadastro
def editar_pessoa(codigo, nome, idade):
    with closing(sqlite3.connect(BANCO)) as conexao:
        with conexao:
            cursor = conexao.execute("""
                UPDATE pessoas
                SET nome = ?, idade = ?
                WHERE id = ?
            """, (nome, idade, codigo))

            return cursor.rowcount > 0


# Função para excluir um cadastro
def excluir_pessoa(codigo):
    with closing(sqlite3.connect(BANCO)) as conexao:
        with conexao:
            cursor = conexao.execute("""
                DELETE FROM pessoas
                WHERE id = ?
            """, (codigo,))

            return cursor.rowcount > 0
