# tests/test_funcao_ola.py

from app.main import funcao_ola


def test_funcao_ola():
    assert funcao_ola() == "Olá, mundo!"
