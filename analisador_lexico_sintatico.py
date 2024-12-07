import ply.lex as lex
import ply.yacc as yacc

#--------------------------------------------------------- LEXER ---------------------------------------------------------#

tokens = (
    'PLUS', 'MINUS', 'MUL', 'DIV', 'EXP',
    'LPAR', 'RPAR', 'LBRACK', 'RBRACK', 'LBRACE', 'RBRACE',
    'ASSIGN', 'SEMICOLON', 'COMMA',
    'LT', 'GT', 'LEQ', 'GEQ', 'EQ', 'NEQ',
    'IF', 'ELSE',
    'NUMBER', 'FLOAT', 'ID',
    'FUNC'
)

#------------------------------------------------ Regras simples de regex ------------------------------------------------#

t_PLUS = r'\+'
t_MINUS = r'-'
t_MUL = r'\*'
t_DIV = r'/'
t_EXP = r'\^'
t_LPAR = r'\('
t_RPAR = r'\)'
t_LBRACK = r'\['
t_RBRACK = r'\]'
t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_ASSIGN = r'='
t_SEMICOLON = r';'
t_COMMA = r','
t_LT = r'<'
t_GT = r'>'
t_LEQ = r'>='
t_GEQ = r'<='
t_EQ = r'=='
t_NEQ = r'!='

#-------------------------------------------------- Palavras reservadas --------------------------------------------------#

reserved = {
    'if': 'IF',
    'else': 'ELSE',
    'sin': 'FUNC',
    'cos': 'FUNC',
    'tan': 'FUNC',
    'sqrt': 'FUNC',
    'log': 'FUNC',
    'exp': 'FUNC'
}

#------------------------------------------ Regex para números e identificadores -----------------------------------------#

def t_FLOAT(t):
    r'\d+\.\d+'
    t.value = float(t.value)
    return t

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = reserved.get(t.value, 'ID') 
    return t

#-------------------------------------------------------------------------------------------------------------------------#

# Ignorar espaços e tabs
t_ignore = ' \t'

# Rastrear erros léxicos
def t_error(t):
    print(f'Caractere inválido: {t.value[0]}')
    t.lexer.skip(1)

#--------------------------------------------------- Construir o lexer ---------------------------------------------------#

lexer = lex.lex()

#-------------------------------------------------------- PARSER ---------------------------------------------------------#

#----------------------------------------------- Precedência dos operadores ----------------------------------------------#

precedence = (
    ('left', 'PLUS', 'MINUS'),
    ('left', 'MUL', 'DIV'),
    ('right', 'EXP'),
)

#-------------------------------------------------- Regras da gramática --------------------------------------------------#

def p_stmt_assign(p):
    '''Stmt : ID ASSIGN Exp SEMICOLON'''
    # Atribuição de valor a uma variável: 'ID = Exp;'
    p[0] = ('assign', ('id', p[1]), p[3])

def p_stmt_if_else(p):
    '''Stmt : IF LPAR RelExp RPAR LBRACE StmtList RBRACE ELSE LBRACE StmtList RBRACE SEMICOLON
            | IF LPAR RelExp RPAR LBRACE StmtList RBRACE SEMICOLON'''
    # Condição if-else ou if simples
    if len(p) == 13:
        p[0] = ('if-else', p[3], p[6], p[10])  # 'if-else' com bloco 'else'
    else:
        p[0] = ('if', p[3], p[6])  # Apenas 'if'

def p_stmt_list(p):
    '''StmtList : Stmt
                | Stmt StmtList'''
    # Lista de instruções (sequência de instruções)
    if len(p) == 2:
        p[0] = [p[1]]  # Se houver apenas uma instrução
    else:
        p[0] = [p[1]] + p[2]  # Sequência de instruções

def p_exp_binop(p):
    '''Exp : Exp PLUS Exp
           | Exp MINUS Exp
           | Exp MUL Exp
           | Exp DIV Exp
           | Exp EXP Exp'''  # Para exponenciação
    # Regras para operações binárias (soma, subtração, multiplicação, divisão e exponenciação)
    if p[2] == '+':
        p[0] = ('+', p[1], p[3])
    elif p[2] == '-':
        p[0] = ('-', p[1], p[3])
    elif p[2] == '*':
        p[0] = ('*', p[1], p[3])
    elif p[2] == '/':
        p[0] = ('/', p[1], p[3])
    elif p[2] == '^':
        p[0] = ('^', p[1], p[3])  

def p_exp_term(p):
    'Exp : Term'
    # Uma expressão pode ser um termo (parte da expressão)
    p[0] = p[1]

def p_term_binop(p):
    '''Term : Term MUL Factor
            | Term DIV Factor'''
    # Regras para multiplicação e divisão de termos
    if p[2] == '*':
        p[0] = ('*', p[1], p[3])
    elif p[2] == '/':
        p[0] = ('/', p[1], p[3])

def p_term_factor(p):
    'Term : Factor'
    # Um termo é um fator (parte do termo)
    p[0] = p[1]

def p_factor_exp(p):
    '''Factor : PLUS Factor
              | MINUS Factor'''
    # Um fator pode ser positivo ou negativo
    if p[1] == '+':
        p[0] = ('pos', p[2])
    elif p[1] == '-':
        p[0] = ('neg', p[2])

def p_factor_atom(p):
    'Factor : Atom'
    # Um fator é um átomo (pode ser um número, variável ou expressão entre parênteses)
    p[0] = p[1]

def p_atom_number(p):
    '''Atom : NUMBER
            | FLOAT'''
    # Um átomo pode ser um número inteiro ou decimal
    p[0] = ('number', p[1])

def p_atom_id(p):
    'Atom : ID'
    # Um átomo pode ser um identificador (variável)
    p[0] = ('id', p[1])

def p_atom_group(p):
    'Atom : LPAR Exp RPAR'
    # Um átomo pode ser uma expressão entre parênteses
    p[0] = p[2]

def p_atom_func(p):
    '''Atom : FUNC LPAR ExpSequence RPAR'''
    # Um átomo pode ser uma função pré-definida
    p[0] = ('func', p[1], p[3])

def p_atom_custom_func(p):
    'Atom : ID LPAR ExpSequence RPAR'
    # Um átomo pode ser uma função personalizada
    p[0] = ('func', p[1], p[3])

def p_atom_list(p):
    'Atom : LBRACK ExpSequence RBRACK'
    # Um átomo pode ser uma lista de expressões
    p[0] = ('list', p[2])

def p_atom_tuple(p):
    'Atom : LPAR ExpSequence RPAR'
    # Um átomo pode ser uma tupla de expressões
    p[0] = ('tuple', p[2])

def p_rel_exp(p):
    '''RelExp : Exp LT Exp
              | Exp GT Exp
              | Exp LEQ Exp
              | Exp GEQ Exp
              | Exp EQ Exp
              | Exp NEQ Exp'''
    # Regras para expressões relacionais (comparações)
    p[0] = (p[2], p[1], p[3])

def p_exp_sequence(p):
    '''ExpSequence : Exp
                   | Exp COMMA ExpSequence'''
    # Sequência de expressões separadas por vírgula
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = [p[1]] + p[3]

def p_stmt_end(p):
    'Stmt : Exp SEMICOLON'
    # Instrução que termina com ponto e vírgula
    p[0] = p[1]

def p_error(p):
    # Tratamento de erro de sintaxe
    print('Erro de sintaxe!')

#--------------------------------------------------- Construir o parse ---------------------------------------------------#

parser = yacc.yacc()

#--------------------------------------------------------- TESTE ---------------------------------------------------------#

def main():
    
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
            
    test_cases_invalid = [
        '10 = a;',  # Atribuição inválida
        '1var = 5;',  # Identificador inválido
        'a + * b;',  # Erro de operação inválida
        'a = (5 + 3;',  # Parênteses não fechados
        'a & b;',  # Operador inválido
        'sin(10 + 5;',  # Parênteses de função não fechados
        'if (x > 10) { x = 5; else { x = 10; };',  # Sintaxe inválida em if-else
        'a = 5 @ 3;',  # Operador inválido
        'int a = 5;',  # Tipo inválido
        '[1, 2, 3,;',  # Lista mal formada
        'else { x = 5; };'  # else sem if correspondente
    ]
    
    print('+' + 52 * '-' + ' TESTES VÁLIDOS '  + 52 * '-' + '+')
    for idx, case in enumerate(test_cases_valid, start=1):
        print(f'Teste {idx}: {case}')
        try:
            result = parser.parse(case)
            print(f'Resultado: {result}\n')
        except Exception as e:
            print(f'Erro ao processar: {e}\n')

    print('+' + 51 * '-' + ' TESTES INVÁLIDOS '  + 51 * '-' + '+')
    for idx, case in enumerate(test_cases_invalid, start=1):
        print(f'Teste {idx}: {case}')
        try:
            result = parser.parse(case)
            print(f'Resultado: {result}\n')
        except Exception as e:
            print(f'Erro: {e}\n')

    print('+' + 51 * '-' + ' MODO INTERATIVO '  + 52 * '-' + '+')
    while True:
        try:
            s = input('Digite a expressão (ou "sair" para encerrar): ')
            if s.lower() == 'sair':
                break
        except EOFError:
            break
        if not s:
            continue
        try:
            result = parser.parse(s)
            print(f'Resultado: {result}')
        except Exception as e:
            print(f'Erro: {e}')

if __name__ == '__main__':
    main()