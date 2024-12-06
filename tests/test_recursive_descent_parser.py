import pytest
from app.consts import Consts
from app.recursive_descent_parser import RecursiveDescentParser
from app.token import Token


@pytest.fixture
def parser_factory():
    def _parser(tokens):
        return RecursiveDescentParser(tokens)
    return _parser


def test_parse_valid_single_integer(parser_factory):
    tokens = [
        Token(Consts.INT, 1),
        Token(Consts.EOF, None)
    ]
    parser = parser_factory(tokens)
    result, error = parser.parse()
    assert error is None, f"Erro inesperado: {error}"
    assert result == "iε", f"Resultado esperado 'iε', mas obteve '{result}'"


def test_parse_valid_expression_with_plus(parser_factory):
    tokens = [
        Token(Consts.INT, 1),
        Token(Consts.PLUS, '+'),
        Token(Consts.INT, 2),
        Token(Consts.EOF, None)
    ]
    parser = parser_factory(tokens)
    result, error = parser.parse()
    assert error is None, f"Erro inesperado: {error}"
    assert result == "i+iε", f"Resultado esperado 'i+iε', mas obteve '{result}'"


def test_parse_valid_expression_multiple_plus(parser_factory):
    tokens = [
        Token(Consts.INT, 1),
        Token(Consts.PLUS, '+'),
        Token(Consts.INT, 2),
        Token(Consts.PLUS, '+'),
        Token(Consts.INT, 3),
        Token(Consts.EOF, None)
    ]
    parser = parser_factory(tokens)
    result, error = parser.parse()
    assert error is None, f"Erro inesperado: {error}"
    assert result == "i+i+iε", f"Resultado esperado 'i+i+iε', mas obteve '{result}'"


def test_parse_missing_eof(parser_factory):
    tokens = [
        Token(Consts.INT, 1),
        Token(Consts.PLUS, '+'),
        Token(Consts.INT, 2)
    ]
    parser = parser_factory(tokens)
    result, error = parser.parse()
    assert result is None, "Resultado esperado 'None' em caso de erro de EOF"
    assert isinstance(error,str)


def test_parse_missing_integer_after_plus(parser_factory):
    tokens = [
        Token(Consts.INT, 1),
        Token(Consts.PLUS, '+'),
        Token(Consts.EOF, None)
    ]
    parser = parser_factory(tokens)
    result, error = parser.parse()
    assert result is None, "Resultado esperado 'None' em caso de erro de sintaxe"
    assert isinstance(error,str), \
        f"Erro esperado 'parse_K() falhou, '+' não foi seguido por um inteiro', mas obteve '{error}'"


def test_parse_invalid_start_token(parser_factory):
    tokens = [
        Token(Consts.PLUS, '+'),
        Token(Consts.INT, 1),
        Token(Consts.EOF, None)
    ]
    parser = parser_factory(tokens)
    result, error = parser.parse()
    assert result is None, "Resultado esperado 'None' em caso de erro de início inválido"
    assert isinstance(error,str), \
        f"Erro esperado 'parse_E() falhou, entrada não inicia com um inteiro', mas obteve '{error}'"


def test_parse_empty_input(parser_factory):
    tokens = [
        Token(Consts.EOF, None)
    ]
    parser = parser_factory(tokens)
    result, error = parser.parse()
    assert result is None, "Resultado esperado 'None' para entrada vazia"
    assert isinstance(error,str), \
        f"Erro esperado 'parse_E() falhou, entrada não inicia com um inteiro', mas obteve '{error}'"
