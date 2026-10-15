import sqlite3
from pathlib import Path
from contextlib import closing

from banco import BANCO, criar_banco

# Localização do arquivo antigo
ARQUIVO_TXT = Path(__file__).resolve().parent / "pessoas.txt"


def migrar_dados():
    print("-" * 45)
    print("MIGRAÇÃO DE DADOS PARA SQLITE")
    print("-" * 45)

    # Verificando se o arquivo existe
    if not ARQUIVO_TXT.is_file():
        print("ERRO! Arquivo pessoas.txt não encontrado.")
        print(f"Caminho procurado: {ARQUIVO_TXT}")
        return

    registros = []
    ignorados = 0

    # Lendo os dados antigos
    with open(ARQUIVO_TXT, "r", encoding="utf-8") as arquivo:
        for linha in arquivo:
            dados = linha.strip().split(";")

            if len(dados) != 2:
                ignorados += 1
                continue

            nome = dados[0].strip()

            try:
                idade = int(dados[1])

                if not nome or not 0 <= idade <= 130:
                    ignorados += 1
                    continue

                registros.append((nome, idade))

            except ValueError:
                ignorados += 1

    if not registros:
        print("Nenhum registro válido encontrado.")
        return

    # Garantindo que a tabela existe
    criar_banco()

    # Inserindo no SQLite
    with closing(sqlite3.connect(BANCO)) as conexao:
        with conexao:

            # Controle para evitar importações repetidas
            conexao.execute("""
                CREATE TABLE IF NOT EXISTS migracoes (
                    origem TEXT PRIMARY KEY
                )
            """)

            ja_importado = conexao.execute("""
                SELECT 1 FROM migracoes
                WHERE origem = ?
            """, ("pessoas.txt",)).fetchone()

            if ja_importado:
                print("Este arquivo já foi importado!")
                return

            # Importando os cadastros
            conexao.executemany("""
                INSERT INTO pessoas (nome, idade)
                VALUES (?, ?)
            """, registros)

            # Registrando a migração
            conexao.execute("""
                INSERT INTO migracoes (origem)
                VALUES (?)
            """, ("pessoas.txt",))

    print(f"Registros importados: {len(registros)}")
    print(f"Linhas ignoradas: {ignorados}")
    print("Migração concluída com sucesso!")

# Programa principal
if __name__ == "__main__":
    try:
        migrar_dados()

    except (OSError, UnicodeError, sqlite3.Error) as erro:
        print(f"ERRO durante a migração: {erro}")
