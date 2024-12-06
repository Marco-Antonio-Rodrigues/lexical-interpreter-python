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