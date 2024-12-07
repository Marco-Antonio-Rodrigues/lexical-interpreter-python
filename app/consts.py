import string

class Consts:
    DIGITOS = '0123456789' #ok
    LETRAS = string.ascii_letters 
    LETRAS_DIGITOS = DIGITOS + LETRAS
    UNDER = '_'
    PLUS      = '+' #ok
    MINUS     = '-' #ok
    INT       = 'INT'
    FLOAT     = 'FLOAT'
    MUL       = '*' # ok
    DIV       = '/' # ok
    LPAR      = '(' # ok
    RPAR      = ')' # ok
    LT        = '<'
    GT        = '>' 
    LEQ       = '>='
    GEQ       = '<=' 
    EQ        = '=='
    NEQ       = '!='
    EOF       = '$EOF'
    EQ        = '='
    POW       = '^'
    ID	      = 'ID'
    NULL      = 'NULL'
    STRING    = "STRING"
    LSQUARE   = "[" # Left  Box brackets [
    RSQUARE   = "]" # Right Box brackets ]
    COMMA     = ","
    SEMICOLON = ";"
    KEY       = "KEY"

    # Exemplos de Palavras reservadas
    IF          = 'if'
    WHILE       = 'while'
    FOR         = 'for'
    KEYS = [
        IF,
        WHILE,
        FOR
    ]
