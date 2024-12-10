import string

class Consts:
    DIGITOS = '0123456789' 
    LETRAS = string.ascii_letters 
    LETRAS_DIGITOS = DIGITOS + LETRAS
    UNDER = '_'
    
    # TERMINAIS
    PLUS      = '+' 
    MINUS     = '-' 
    MUL       = '*' 
    DIV       = '/' 
    POW       = '^' 
    ASSIGN    = '=' 
    LT        = '<' 
    GT        = '>' 
    GEQ       = '<=' 
    LEQ       = '>=' 
    EQ        = '==' 
    NEQ       = '!=' 
    AND       = '&&'
    OR        = '||'
    NOT       = '!'
    
    COMMA     = "," 
    SEMICOLON = ";" 
    LPAR      = '(' 
    RPAR      = ')' 
    LBRACE    = "{" 
    RBRACE    = "}" 
    LSQUARE   = "[" 
    RSQUARE   = "]" 
    
    EOF       = '$EOF'
    KEY       = "KEY"
    ID	      = 'ID' 
    
    # TIPOS
    VOID      = 'VOID'
    INT       = 'INT'
    STRING    = 'STRING'
    FLOAT     = 'FLOAT'
    BOOL      = 'BOOL'

    # Palavras reservadas
    IF          = 'if' 
    ELIF        = 'elif' 
    ELSE        = 'else' 
    WHILE       = 'while' 
    FOR         = 'for' 
    FUNC        = 'func' 
    RETURN      = 'return'
    TRUE        = 'true'
    FALSE       = 'false'
    
    BOOLS = [TRUE,FALSE]
        
    KEYS = [
        IF,
        ELIF,
        ELSE,
        WHILE,
        FOR,
        FUNC,
        RETURN
    ]
