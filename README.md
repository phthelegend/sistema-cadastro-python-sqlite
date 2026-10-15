# Sistema de Cadastro de Pessoas — Python e SQLite

Sistema CRUD desenvolvido em Python, com armazenamento persistente utilizando SQLite e testes automatizados.

[![Testes Automatizados Python](https://github.com/phthelegend/sistema-cadastro-python-sqlite/actions/workflows/python-tests.yml/badge.svg)](https://github.com/phthelegend/sistema-cadastro-python-sqlite/actions/workflows/python-tests.yml)

## Funcionalidades

- Cadastro de pessoas com nome e idade.
- Listagem de registros.
- Pesquisa por nome.
- Atualização de cadastros.
- Exclusão de registros com confirmação.
- Validação de entradas e tratamento de erros.

## Tecnologias

- Python 3
- SQLite
- Biblioteca `sqlite3`
- Testes automatizados com `unittest`
- Git e GitHub

## Como executar

No terminal, dentro da pasta do projeto:

```bash
python principal.py
```

O banco de dados será criado automaticamente, caso não exista.

## Testes automatizados

Para executar os testes:

```bash
python -m unittest discover -s tests -v
```

Os testes utilizam bancos de dados temporários para não modificar os cadastros reais.

## Objetivo

Projeto desenvolvido para consolidar conhecimentos de lógica de programação, modularização, persistência de dados, operações SQL, tratamento de exceções e testes automatizados.

## Melhorias futuras

- Ampliação da cobertura de testes.
- Separação da lógica de negócio e da interface.
- Desenvolvimento de uma API REST.
- Criação de uma interface gráfica ou web.
