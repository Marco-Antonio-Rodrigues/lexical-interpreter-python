from app.lexer import Lexer

def test_deve_aceitar_plus():
    input_string = '++'
    tokens, error = Lexer(input_string).makeTokens()
    
    assert error is None
    
def test_deve_aceitar_quebra_de_linha():
    input_string = '--'
    tokens, error = Lexer(input_string).makeTokens()
    
    assert error is None
    
def test_deve_aceitar_somas_de_numeros():
    input_string = '1+2+3'
    tokens, error = Lexer(input_string).makeTokens()
    
    assert error is None

def test_nu_sei_one():
    input_string = '12'
    tokens, error = Lexer(input_string).makeTokens()
    
    assert error is None
    
def test_nu_sei_two():
    input_string = '1.1'
    tokens, error = Lexer(input_string).makeTokens()
    
    assert error is None
    
def test_nu_sei_three():
    input_string = '(1+2)'
    tokens, error = Lexer(input_string).makeTokens()
    
    assert error is None

def test_nu_sei_four():
    input_string = '1+3*(1+4)'
    tokens, error = Lexer(input_string).makeTokens()
    
    assert error is None
    
def test_nu_sei_five():
    input_string = '4/2'
    tokens, error = Lexer(input_string).makeTokens()
    
    assert error is None
    
def test_lexer():
    input_string = '1+-/*()1.1'
    tokens, error = Lexer(input_string).makeTokens()
    
    assert error is None
def test_lexer_one():
    test_cases_valid = [
        'a = 10;',  # Atribuição simples
        'x = 5 + 3 * 2;', # Soma
        'if (x > 10) {y = 1;} else {y = 0;};', # Estrutura if-else
        'z = sin(x) + log(y);', # Atribuindo soma de funções a uma variável
        'w = [3 + 4, 5 * 2];', # Uso de lista
        'z = (sin(x), cos(y));', # Uso de tupla de funções
        'if (x <= 10) {a = 1 + 2 * 3;b = a * 2;} else {a = 5 + 7;b = a / 2;};', # Estrutura if-else
        'if (x > 0) {a = sin(x) + 5 * 3;b = sqrt(a) * cos(x);} else {a = log(10) * 2;b = a + 10;};', # Estrutura if-else
        'y = myFunc(x, 5);',
        'b = a + 5;',  # Soma
        'c = b * 2;',  # Multiplicação
        'd = a / 2;',  # Divisão
        'x = (3 + 2) * (4 - 1);',  # Uso de parênteses
        'if (x == 15) { y = x + 5; } else { y = x - 5; };',  # Estrutura if-else
        '5 + 5;',  # Soma simples
        'a = 5 ^ 2;',  # Exponenciação
        'if (x < 10) { x = x + 1; } else { x = x - 1; };',  # Condição com menor que
        'y = sqrt(25);',  # Função sqrt
        'z = log(100);',  # Função log
        'a = [1, 2, 3];',  # Uso de lista
        'f = sin(x);',  # Função trigonométrica
        'g = (a, b, c);'  # Uso de tupla
    ]
    
    for exp in test_cases_valid:
        tokens, error = Lexer(exp).makeTokens()
        assert error is None, f"Error em {exp}"