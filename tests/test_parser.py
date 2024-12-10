import pytest
from analisador_lexico_sintatico import lexer, parser  # Substitua pelo nome do arquivo onde o código está definido

@pytest.mark.parametrize("test_input,expected_tokens", [
    ('x = a + b * c;', ['ID', 'ASSIGN', 'ID', 'PLUS', 'ID', 'MUL', 'ID', 'SEMICOLON']),
    ('x = true;', ['ID', 'ASSIGN', 'BOOL', 'SEMICOLON']),
    ('a = (b + c) * (d - e);', ['ID', 'ASSIGN', 'LPAR', 'ID', 'PLUS', 'ID', 'RPAR', 'MUL', 'LPAR', 'ID', 'MINUS', 'ID', 'RPAR', 'SEMICOLON']),
    ('if (x > 5 && y < 10) {z = 1;} else {z = 0;};', [
        'IF', 'LPAR', 'ID', 'GT', 'INT', 'AND', 'ID', 'LT', 'INT', 'RPAR', 
        'LBRACE', 'ID', 'ASSIGN', 'INT', 'SEMICOLON', 'RBRACE', 
        'ELSE', 'LBRACE', 'ID', 'ASSIGN', 'INT', 'SEMICOLON', 'RBRACE', 'SEMICOLON'
    ]),
    ('x = 1;', ['ID', 'ASSIGN', 'INT', 'SEMICOLON']),
    ('x = a + b * c;', ['ID', 'ASSIGN', 'ID', 'PLUS', 'ID', 'MUL', 'ID', 'SEMICOLON']),
    ('a = (b + c) * (d - e);', ['ID', 'ASSIGN', 'LPAR', 'ID', 'PLUS', 'ID', 'RPAR', 'MUL', 'LPAR', 'ID', 'MINUS', 'ID', 'RPAR', 'SEMICOLON']),
    ('if (x > 5 && y < 10) {z = 1;} else {z = 0;};', [
        'IF', 'LPAR', 'ID', 'GT', 'INT', 'AND', 'ID', 'LT', 'INT', 'RPAR', 
        'LBRACE', 'ID', 'ASSIGN', 'INT', 'SEMICOLON', 'RBRACE', 
        'ELSE', 'LBRACE', 'ID', 'ASSIGN', 'INT', 'SEMICOLON', 'RBRACE', 'SEMICOLON'
    ]),
    ('while (x < 10) {x = x + 1;}', [
        'WHILE', 'LPAR', 'ID', 'LT', 'INT', 'RPAR', 
        'LBRACE', 'ID', 'ASSIGN', 'ID', 'PLUS', 'INT', 'SEMICOLON', 'RBRACE'
    ]),
    ('for (int i = 0; i < 10; i = i + 1) {sum = sum + i;}', [
        'FOR', 'LPAR', 'INT', 'ID', 'ASSIGN', 'INT', 'SEMICOLON', 
        'ID', 'LT', 'INT', 'SEMICOLON', 'ID', 'ASSIGN', 'ID', 'PLUS', 'INT', 'RPAR', 
        'LBRACE', 'ID', 'ASSIGN', 'ID', 'PLUS', 'ID', 'SEMICOLON', 'RBRACE'
    ]),
    ('return x + y;', ['RETURN', 'ID', 'PLUS', 'ID', 'SEMICOLON']),
    ('int a = 2; b = 3; c = 4;', [
        'INT', 'ID', 'ASSIGN', 'INT', 'SEMICOLON', 
        'ID', 'ASSIGN', 'INT', 'SEMICOLON', 
        'ID', 'ASSIGN', 'INT', 'SEMICOLON'
    ]),
    ('y = (a + b) / (c - d);', [
        'ID', 'ASSIGN', 'LPAR', 'ID', 'PLUS', 'ID', 'RPAR', 'DIV', 'LPAR', 'ID', 'MINUS', 'ID', 'RPAR', 'SEMICOLON'
    ]),
    ('int x = 10 + (y = 5);', [
        'INT', 'ID', 'ASSIGN', 'INT', 'PLUS', 'LPAR', 'ID', 'ASSIGN', 'INT', 'RPAR', 'SEMICOLON'
    ]),
    ('float x = 10.5, y = 20.3;', [
        'FLOAT', 'ID', 'ASSIGN', 'FLOAT', 'COMMA', 'ID', 'ASSIGN', 'FLOAT', 'SEMICOLON'
    ]),
    ('if (x == 5) {y = 2;} else {y = 3;}', [
        'IF', 'LPAR', 'ID', 'EQ', 'INT', 'RPAR', 
        'LBRACE', 'ID', 'ASSIGN', 'INT', 'SEMICOLON', 'RBRACE', 
        'ELSE', 'LBRACE', 'ID', 'ASSIGN', 'INT', 'SEMICOLON', 'RBRACE'
    ]),
    ('x = sin(x) * cos(x) + log(x);', [
        'ID', 'ASSIGN', 'ID', 'LPAR', 'ID', 'RPAR', 'MUL', 'ID', 'LPAR', 'ID', 'RPAR', 
        'PLUS', 'ID', 'LPAR', 'ID', 'RPAR', 'SEMICOLON'
    ]),
])

def test_lexer_valid(test_input, expected_tokens):
    lexer.input(test_input)
    tokens = [token.type for token in lexer]
    assert tokens == expected_tokens
  

  
@pytest.mark.parametrize("test_input,expected_tokens", [
    # Erros de sintaxe
    ('10 = a;', None),              # Tentativa de atribuir um valor para um número
    ('1var = 5;', None),            # Identificador inválido que começa com um número
    ('a + * b;', None),             # Operadores consecutivos inválidos
    ('a = (5 + 3;', None),          # Parêntese não fechado
    ('a & b;', None),               # Operador lógico inválido (& não é suportado)
    ('sin(10 + 5;', None),          # Parêntese não fechado em chamada de função

    # Palavras reservadas ou símbolos mal posicionados
    ('if (x > 10) { x = 5; else { x = 10; };', None),  # Bloco else sem fechamento do bloco anterior
    ('a = 5 @ 3;', None),           # Operador inválido (@ não é suportado)
    ('[1, 2, 3,;', None),           # Lista com vírgula final inválida
    ('else { x = 5; };', None),     # "else" sem um bloco "if" correspondente

    # Tipos de dados ou expressões malformadas
    ('truee', None),                # Identificador semelhante a palavra reservada
    ('123abc', None),               # Identificador começando com número seguido de letras
    ('float = 2..5;', None),        # Formato de número de ponto flutuante inválido
    ('while (x > 0 x = x - 1;', None),  # Falta de operador lógico ou de separador entre expressões
])

def test_lexer_invalid(test_input, expected_tokens):
    lexer.input(test_input)
    tokens = [token.type for token in lexer]
    assert tokens == expected_tokens


@pytest.mark.parametrize("test_input", [
    '10 = a;',
    '1var = 5;',
    'a + * b;',
    'a = (5 + 3;',
    'a & b;',
    'sin(10 + 5;',
    'if (x > 10) { x = 5; else { x = 10; };',
    'a = 5 @ 3;',
    'int a = 5;',
    '[1, 2, 3,;',
    'else { x = 5; };',
])
def test_lexer_invalid(test_input):
    lexer.input(test_input)
    with pytest.raises(Exception):
        for token in lexer:
            pass  # Apenas itera para verificar se há exceções


@pytest.mark.parametrize("test_input,expected_parse", [
    ('x = a + b * c;', ('StmtList', ('VarStmt', 'ID', 'ASSIGN', 'Exp', ('ID', 'PLUS', ('Term', ('ID', 'MUL', 'ID')))))),
    ('if (x > 5) {y = 2;} else {y = 3;};', 
     ('StmtList', ('IfStmt', ('RelExp', ('ID', 'GT', 'INT')), ('StmtList', ('VarStmt', 'ID', 'ASSIGN', 'Exp', ('INT',)), None)))),
])
def test_parser_valid(test_input, expected_parse):
    result = parser.parse(test_input)
    assert result == expected_parse


@pytest.mark.parametrize("test_input", [
    'a + * b;',
    'if (x > 10) { x = 5; else { x = 10; };',
    '[1, 2, 3,;',
])
def test_parser_invalid(test_input):
    with pytest.raises(Exception):
        parser.parse(test_input)
