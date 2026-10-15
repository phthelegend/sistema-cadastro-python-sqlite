# Módulo interface.py

def linha(tamanho=42):
    return "-" * tamanho

def cabecalho(texto):
    print(linha())
    print(texto.center(42))
    print(linha())

def leiaInt(mensagem):
    while True:
        try:
            numero = int(input(mensagem))
            return numero

        except ValueError:
            print("ERRO! Digite um número inteiro válido.")

        except (KeyboardInterrupt, EOFError):
            print("\nEntrada interrompida pelo usuário.")
            return None

def menu(opcoes):
    cabecalho("MENU PRINCIPAL")

    for indice, opcao in enumerate(opcoes, start=1):
        print(f"{indice} - {opcao}")

    print(linha())

    return leiaInt("Sua opção: ")
