import sqlite3

from interface import menu, cabecalho, leiaInt

from banco import (
    criar_banco,
    cadastrar_pessoa,
    listar_pessoas,
    editar_pessoa,
    excluir_pessoa
)


# Exibir os cadastros em uma tabela
def mostrar_tabela(pessoas):
    if not pessoas:
        print("Nenhuma pessoa encontrada.")
        return

    print("-" * 45)
    print(f"{'ID':<6}{'NOME':<28}{'IDADE':>5}")
    print("-" * 45)

    for pessoa in pessoas:
        print(
            f"{pessoa['id']:<6}"
            f"{pessoa['nome']:<28.28}"
            f"{pessoa['idade']:>5}"
        )

    print("-" * 45)


# Validar o nome
def ler_nome(mensagem="Nome: "):
    while True:
        try:
            nome = input(mensagem).strip()

            if nome:
                return nome

            print("ERRO! O nome não pode ficar vazio.")

        except (KeyboardInterrupt, EOFError):
            print("\nOperação cancelada.")
            return None


# Validar a idade
def ler_idade():
    while True:
        idade = leiaInt("Idade: ")

        if idade is None:
            return None

        if 0 <= idade <= 130:
            return idade

        print("ERRO! Digite uma idade entre 0 e 130.")


# Selecionar um cadastro pelo ID
def selecionar_pessoa():
    pessoas = listar_pessoas()

    if not pessoas:
        print("Nenhuma pessoa cadastrada.")
        return None

    mostrar_tabela(pessoas)

    codigo = leiaInt("Digite o ID da pessoa: ")

    if codigo is None:
        return None

    for pessoa in pessoas:
        if pessoa["id"] == codigo:
            return pessoa

    print("ERRO! Cadastro não encontrado.")
    return None


# Programa principal
def principal():
    try:
        criar_banco()

    except sqlite3.Error as erro:
        print(f"Erro ao iniciar o banco: {erro}")
        return

    opcoes = [
        "Ver pessoas cadastradas",
        "Cadastrar nova pessoa",
        "Pesquisar pessoa",
        "Editar cadastro",
        "Excluir cadastro",
        "Sair do sistema"
    ]

    while True:
        try:
            escolha = menu(opcoes)

            # LISTAR
            if escolha == 1:
                cabecalho("PESSOAS CADASTRADAS")
                mostrar_tabela(listar_pessoas())

            # CADASTRAR
            elif escolha == 2:
                cabecalho("NOVO CADASTRO")

                nome = ler_nome()
                if nome is None:
                    continue

                idade = ler_idade()
                if idade is None:
                    continue

                cadastrar_pessoa(nome, idade)

            # PESQUISAR
            elif escolha == 3:
                cabecalho("PESQUISAR PESSOA")

                pesquisa = ler_nome("Pesquisar nome: ")
                if pesquisa is None:
                    continue

                pessoas = listar_pessoas()

                encontrados = [
                    pessoa for pessoa in pessoas
                    if pesquisa.casefold()
                    in pessoa["nome"].casefold()
                ]

                mostrar_tabela(encontrados)

            # EDITAR
            elif escolha == 4:
                cabecalho("EDITAR CADASTRO")

                pessoa = selecionar_pessoa()

                if pessoa is None:
                    continue

                print(f"Editando: {pessoa['nome']}")

                novo_nome = ler_nome("Novo nome: ")
                if novo_nome is None:
                    continue

                nova_idade = ler_idade()
                if nova_idade is None:
                    continue

                if editar_pessoa(
                    pessoa["id"], novo_nome, nova_idade
                ):
                    print("Cadastro atualizado com sucesso!")
                else:
                    print("Não foi possível atualizar.")

            # EXCLUIR
            elif escolha == 5:
                cabecalho("EXCLUIR CADASTRO")

                pessoa = selecionar_pessoa()

                if pessoa is None:
                    continue

                print(f"Pessoa: {pessoa['nome']}")

                confirmar = input(
                    "Confirmar exclusão? [S/N]: "
                ).strip().upper()

                if confirmar == "S":
                    if excluir_pessoa(pessoa["id"]):
                        print("Cadastro excluído com sucesso!")
                    else:
                        print("Não foi possível excluir.")
                else:
                    print("Exclusão cancelada.")

            # SAIR
            elif escolha == 6 or escolha is None:
                cabecalho("ENCERRANDO O SISTEMA")
                print("Até logo!")
                break

            else:
                print("ERRO! Escolha uma opção válida.")

        except sqlite3.Error as erro:
            print(f"Erro no banco de dados: {erro}")

        except (KeyboardInterrupt, EOFError):
            print("\nOperação cancelada.")


if __name__ == "__main__":
    principal()

