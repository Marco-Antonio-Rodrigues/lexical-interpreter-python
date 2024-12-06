import ply.lex as lex
import ply.yacc as yacc

# === LEXER =================================================
tokens = (
    'NUMBER',
    'PLUS',
    'MINUS',
    'TIMES',
    'DIVIDE',
    'LPAREN',
    'RPAREN',
)

# Regras de expressão regular para tokens simples
t_PLUS    = r'\+'
t_MINUS   = r'-'
t_TIMES   = r'\*'
t_DIVIDE  = r'/'
t_LPAREN  = r'\('
t_RPAREN  = r'\)'

# Ignorar espaços e tabulações
t_ignore = ' \t'

def t_NUMBER(t):
    r'\d+(\.\d+)?'
    t.value = float(t.value)
    return t

# Regra para rastrear erros léxicos
def t_error(t):
    print(f"Caractere inválido: {t.value[0]}")
    t.lexer.skip(1)

# Construção do lexer
lexer = lex.lex()


# === PARSER =================================================
# Precedência dos operadores
precedence = (
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE'),
)

# Regras da gramática
def p_expression_binop(p):
    '''expression : expression PLUS expression
                  | expression MINUS expression
                  | expression TIMES expression
                  | expression DIVIDE expression'''
    if p[2] == '+':
        p[0] = p[1] + p[3]
    elif p[2] == '-':
        p[0] = p[1] - p[3]
    elif p[2] == '*':
        p[0] = p[1] * p[3]
    elif p[2] == '/':
        p[0] = p[1] / p[3]

def p_expression_group(p):
    'expression : LPAREN expression RPAREN'
    p[0] = p[2]

def p_expression_number(p):
    'expression : NUMBER'
    p[0] = p[1]

def p_error(p):
    print("Erro de sintaxe!")

# Construção do parser
parser = yacc.yacc()

# === TESTE =================================================================
def main():
    while True:
        try:
            s = input("Digite a expressão: ")
        except EOFError:
            break
        if not s:
            continue
        result = parser.parse(s)
        print(f"Resultado: {result}")

if __name__ == '__main__':
    main()
