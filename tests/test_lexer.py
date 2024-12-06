from app.Lexer import Lexer

def test_deve_aceitar_plus():
    input_string = '++'
    lexer = Lexer(input_string)
    
    tokens, error = lexer.makeTokens()
    assert error is None
    assert len(tokens) == 3
    
def test_deve_aceitar_quebra_de_linha():
    input_string = '"oii \n"'
    lexer = Lexer(input_string)
    
    tokens, error = lexer.makeTokens()
    assert error is None
    assert len(tokens) == 2
    
def test_deve_aceitar_somas_de_numeros():
    input_string = '1+2+3'
    lexer = Lexer(input_string)
    
    tokens, error = lexer.makeTokens()
    assert error is None
    assert len(tokens) == 6
    