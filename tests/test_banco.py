
import sqlite3
import tempfile
import unittest

from pathlib import Path
from unittest.mock import patch

import banco


class TesteBancoSQLite(unittest.TestCase):

    def setUp(self):
        # Criando uma pasta temporária
        self.pasta = tempfile.TemporaryDirectory()
        self.addCleanup(self.pasta.cleanup)

        # Criando um banco exclusivo para cada teste
        caminho = Path(self.pasta.name) / "teste.db"

        self.patcher = patch.object(
            banco, "BANCO", caminho
        )

        self.patcher.start()
        self.addCleanup(self.patcher.stop)

        # Preparando a tabela
        banco.criar_banco()

    # TESTE 1 - Criar a tabela
    def test_criar_banco(self):
        pessoas = banco.listar_pessoas()

        self.assertEqual(pessoas, [])

    # TESTE 2 - Cadastrar e consultar
    def test_cadastrar_pessoa(self):
        codigo = banco.cadastrar_pessoa("Carlos", 25)

        pessoas = banco.listar_pessoas()

        self.assertEqual(len(pessoas), 1)
        self.assertEqual(pessoas[0]["id"], codigo)
        self.assertEqual(pessoas[0]["nome"], "Carlos")
        self.assertEqual(pessoas[0]["idade"], 25)

    # TESTE 3 - Editar um cadastro
    def test_editar_pessoa(self):
        codigo = banco.cadastrar_pessoa("Ana", 20)

        resultado = banco.editar_pessoa(
            codigo, "Ana Maria", 30
        )

        pessoa = banco.listar_pessoas()[0]

        self.assertTrue(resultado)
        self.assertEqual(pessoa["nome"], "Ana Maria")
        self.assertEqual(pessoa["idade"], 30)

    # TESTE 4 - Excluir um cadastro
    def test_excluir_pessoa(self):
        codigo = banco.cadastrar_pessoa("Pedro", 35)

        resultado = banco.excluir_pessoa(codigo)

        self.assertTrue(resultado)
        self.assertEqual(banco.listar_pessoas(), [])

    # TESTE 5 - Código inexistente
    def test_codigo_inexistente(self):
        edicao = banco.editar_pessoa(
            999, "Teste", 30
        )

        exclusao = banco.excluir_pessoa(999)

        self.assertFalse(edicao)
        self.assertFalse(exclusao)

    # TESTE 6 - Idade inválida
    def test_idade_invalida(self):
        with self.assertRaises(sqlite3.IntegrityError):
            banco.cadastrar_pessoa("Teste", -10)

        self.assertEqual(banco.listar_pessoas(), [])


if __name__ == "__main__":
    unittest.main()
