import string

class Consts:
    DIGITOS = '0123456789' #ok
    LETRAS = string.ascii_letters 
    LETRAS_DIGITOS = DIGITOS + LETRAS
    UNDER = '_'
    PLUS      = '+' #ok
    MINUS     = '-' #ok
    MUL       = '*' # ok
    DIV       = '/' # ok
    LPAR      = '(' # ok
    RPAR      = ')' # ok
    LT        = '<' # ok
    GT        = '>' # ok
    LEQ       = '>=' # ok
    GEQ       = '<=' # ok
    EQ        = '==' # ok
    NEQ       = '!=' # ok
    EOF       = '$EOF'
    ASSIGN    = '=' # ok
    POW       = '^' # ok
    ID	      = 'ID' # ok
    LBRACE    = "{" # ok
    RBRACE    = "}" # ok
    LSQUARE   = "[" # ok
    RSQUARE   = "]" # ok
    COMMA     = "," #ok
    SEMICOLON = ";" #ok
    KEY       = "KEY" # ok
    
    # TIPOS
    NULL      = 'NULL'
    STRING    = "STRING"
    INT       = 'INT'
    FLOAT     = 'FLOAT'

    # Palavras reservadas
    IF          = 'if' # ok
    ELIF        = 'elif' # ok
    ELSE        = 'else' # ok
    WHILE       = 'while' # ok
    FOR         = 'for' # ok
    FUNC        = 'func' # ok
    KEYS = [
        IF,
        ELSE,
        WHILE,
        FOR,
        FUNC
    ]
