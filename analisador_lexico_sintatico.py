import ply.lex as lex
import ply.yacc as yacc

#--------------------------------------- Definição dos símbolos terminais (tokens) ---------------------------------------#

tokens = (
    'PLUS', 'MINUS', 'MUL', 'DIV', 'LPAR', 
    'RPAR', 'ASSIGN', 'LBRACK', 'RBRACK', 'COMMA',
    'SEMICOLON', 'LT', 'GT', 'LEQ', 'GEQ', 'EQ', 'NEQ', 
    'LBRACE', 'RBRACE', 'IF', 'ELSE', 'ELIF', 'FOR', 
    'WHILE', 'INT', 'FLOAT','BOOL','VOID', 'RETURN',
    'ID', 'AND', 'OR', 'NOT', 'TRUE','FALSE'
)

#-------------------------------------------------- Palavras reservadas --------------------------------------------------#

reserved = {
    'if': 'IF',
    'else': 'ELSE',
    'elif': 'ELIF',
    'for': 'FOR',
    'while': 'WHILE',
    'return': 'RETURN',
    'int': 'INT',
    'float': 'FLOAT',
    'void': 'VOID',
    'bool': 'BOOL',
    'false': 'FALSE',
    'true': 'TRUE',
}

#------------------------------------ Definindo as expressões regulares para os tokens -----------------------------------#

t_PLUS = r'\+'
t_MINUS = r'-'
t_MUL = r'\*'
t_DIV = r'/'
t_LPAR = r'\('
t_RPAR = r'\)'
t_ASSIGN = r'='
t_LBRACK = r'\['
t_RBRACK = r'\]'
t_COMMA = r','
t_SEMICOLON = r';'
t_LT = r'<'
t_GT = r'>'
t_LEQ = r'<='
t_GEQ = r'>='
t_EQ = r'=='
t_NEQ = r'!='
t_AND = r'&&'
t_OR = r'\|\|' 
t_NOT = r'!'
t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_IF = r'if'
t_ELIF = r'elif'
t_ELSE = r'else'
t_FOR = r'for'
t_WHILE = r'while'
t_RETURN = r'return'

t_ignore = ' \t\n'


def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = reserved.get(t.value, 'ID') 
    if t.type == 'TRUE' or t.type == 'FALSE':
        t.type = 'BOOL' 
    return t

def t_FLOAT(t):
    r'\d+\.\d+'
    t.value = float(t.value)
    return t

def t_INT(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_error(t):
    if t.value[0] not in ['\n', ' ', '\t']:
        print(f"Caracter ilegal: {repr(t.value)}")
    t.lexer.skip(1)

#--------------------------------------------------------- LEXER ---------------------------------------------------------#

lexer = lex.lex()

#-------------------------------------------- Definição das regras do parser ---------------------------------------------#

precedence = (
    ('left', 'OR', 'AND'),
    ('left', 'EQ', 'NEQ'),
    ('left', 'LT', 'LEQ', 'GT', 'GEQ'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'MUL', 'DIV'),
    ('right', 'NOT'),
)

def p_program(p):
    '''program : stmt_list'''
    p[0] = ('Program', p[1])

def p_stmt_list(p):
    '''stmt_list : stmt stmt_list
                 | stmt'''
    if len(p) == 3:  # Caso tenha duas partes
        p[0] = ['StmtList'] + [p[1]] + p[2]
    else:  # Caso tenha apenas uma parte
        p[0] = ['StmtList', p[1]]

def p_stmt(p):
    '''stmt : if_stmt
            | var_stmt
            | func_declaration
            | return_stmt
            | exp_stmt
            | for_stmt
            | while_stmt'''
    p[0] = p[1]  # Retorna a primeira parte da produção


def p_if_stmt(p):
    '''if_stmt : IF LPAR rel_exp RPAR LBRACE stmt_list RBRACE elif_block else_block
               | IF LPAR rel_exp RPAR LBRACE stmt_list RBRACE'''
    if len(p) == 8:
        p[0] = ('IfStmt', p[3], p[6], p[7])
    else:
        p[0] = ('IfStmt', p[3], p[6], None)

def p_elif_block(p):
    '''elif_block : ELIF LPAR rel_exp RPAR LBRACE stmt_list RBRACE elif_block
                  | '''
    if len(p) == 7:
        p[0] = ('ElifBlock', p[3], p[6], p[7])
    else:
        p[0] = ('ElifBlock',)

def p_else_block(p):
    '''else_block : ELSE LBRACE stmt_list RBRACE
                  | '''
    if len(p) == 5:
        p[0] = ('ElseBlock', p[3])
    else:
        p[0] = ('ElseBlock',)

def p_var_stmt(p):
    '''var_stmt : type ID ASSIGN exp SEMICOLON
                | type ID SEMICOLON
                | ID ASSIGN exp SEMICOLON'''
    if len(p) == 6:
        p[0] = ('VarStmt', p[1], 'ID', p[2], p[3], p[4], p[5])
    elif len(p) == 5:
        p[0] = ('VarStmt', 'ID', p[1], p[2], p[3], p[4])
    else:
        p[0] = ('VarStmt', p[1], 'ID', p[2], p[3])

def p_func_declaration(p):
    '''func_declaration : type ID LPAR exp_sequence RPAR LBRACE stmt_list return_stmt RBRACE
                        | type ID LPAR exp_sequence RPAR LBRACE stmt_list RBRACE
                        | type ID LPAR RPAR LBRACE stmt_list return_stmt RBRACE
                        | type ID LPAR RPAR LBRACE stmt_list RBRACE'''
    p[0] = ('FuncDeclaration', p[1], p[2], p[4], p[6])

def p_return_stmt(p):
    '''return_stmt : RETURN exp SEMICOLON
                   | RETURN SEMICOLON'''
    if len(p) == 4:  # Caso tenha uma expressão
        p[0] = ('ReturnStmt', p[2])
    else:  # Caso não tenha expressão
        p[0] = ('ReturnStmt', None)

def p_exp_stmt(p):
    '''exp_stmt : exp SEMICOLON'''
    p[0] = ('ExpStmt', p[1])

def p_for_stmt(p):
    '''for_stmt : FOR LPAR var_stmt exp SEMICOLON rel_exp SEMICOLON exp RPAR LBRACE stmt_list RBRACE'''
    p[0] = ('ForStmt', p[3], p[4], p[6], p[8], p[10])

def p_while_stmt(p):
    '''while_stmt : WHILE LPAR rel_exp RPAR LBRACE stmt_list RBRACE'''
    p[0] = ('WhileStmt', p[3], p[6])

def p_exp(p):
    '''exp : term
           | exp PLUS term
           | exp MINUS term'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = ('Exp', p[1], p[2], p[3])

def p_term(p):
    '''term : factor
            | term MUL factor
            | term DIV factor'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = ('Term', p[1], p[2], p[3])

def p_factor(p):
    '''factor : PLUS atom
              | MINUS atom
              | atom'''
    if len(p) == 3:
        p[0] = ('Factor', p[1], p[2])
    else:
        p[0] = ('Factor', p[1])

def p_atom(p):
    '''atom : INT
            | FLOAT
            | BOOL
            | TRUE
            | FALSE
            | ID
            | LPAR exp RPAR
            | func_call
            | LBRACK exp_sequence RBRACK'''
    if len(p) == 2:
        p[0] = ('Atom', p[1])
    else:
        p[0] = ('Atom', p[2])

def p_func_call(p):
    '''func_call : ID LPAR exp_sequence RPAR
                 | ID LPAR RPAR'''
    p[0] = ('FuncCall', p[1], p[3] if len(p) == 4 else None)

def p_exp_sequence(p):
    '''exp_sequence : exp
                    | exp COMMA exp_sequence'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = [p[1]] + p[3]

def p_rel_exp(p):
    '''rel_exp : exp LT exp
               | exp GT exp
               | exp LEQ exp
               | exp GEQ exp
               | exp EQ exp
               | exp NEQ exp
               | exp AND exp
               | exp OR exp
               | NOT exp
               | exp'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = ('RelExp', p[1], p[2], p[3])

def p_type(p):
    '''type : INT
            | FLOAT
            | VOID'''
    p[0] = p[1]

def p_error(p):
    print("Erro de sintaxe em '%s'" % p.value if p else "Erro de sintaxe")

#--------------------------------------------------------- PARSER --------------------------------------------------------#

parser = yacc.yacc()

#--------------------------------------------------------- TESTE ---------------------------------------------------------#

def main():
    test_cases_valid = [
        'x = 1;',                                        # 1 - Operações com múltiplas variáveis
        'x = a + b * c;',                                        # 1 - Operações com múltiplas variáveis
        'a = (b + c) * (d - e);',                                # 2 - Operações com parênteses e múltiplos operadores
        #'x = y == 10;',                                          # 3 - Operação de comparação
        'if (x > 5 && y < 10) {z = 1;} else {z = 0;};',          # 4 - Expressão com operador lógico
        'while (x < 10) {x = x + 1;}',                           # 5 - Laço `while`
        'for (int i = 0; i < 10; i = i + 1) {sum = sum + i;}',   # 6 - Laço `for` com inicialização, condição e incremento
        'return x + y;',                                         # 7 - Instrução `return` simples
        'int a = 2; b = 3; c = 4;',                              # 8 - Declaração múltipla de variáveis
        'y = (a + b) / (c - d);',                                # 9 - Expressões com divisão
        'int x = 10 + (y = 5);',                                 # 10 - Atribuição dentro de uma expressão
        'float x = 10.5, y = 20.3;',                             # 11 - Declaração de variáveis flutuantes
        'while (x > 0) {x = x - 1;}',                            # 12 - Laço `while`
        'if (x == 5) {y = 2;} else {y = 3;} ',                   # 13 - If-else com valores diferentes
        'int x = 0, y = 1; if (x == y) {a = 1;} else {a = 2;}',  # 14 - If-else simples
        'float z = sin(x) * cos(y);',                            # 15 - Funções trigonométricas
        'int x = (a + b) * (c - d) / e;',                        # 16 - Expressão com múltiplos operadores
        'for (int i = 0; i < 5; i = i + 1) {a = a + i;}',        # 17 - Laço `for` com incremento simples
        'if (a != b) {a = 10;} else {b = 20;}',                 # 18 - Expressão de comparação e atribuição
        'y = sin(x) + cos(y);',                                  # 19 - Combinação de funções trigonométricas
        'z = log10(x) + sqrt(y);',                               # 20 - Funções logarítmica e raiz
        'y = sqrt(x) + log(x);',                                 # 21 - Raiz quadrada e logaritmo em uma expressão
        'z = (x + y) * (sin(x) + cos(y));',                      # 22 - Expressão com funções trigonométricas
        'int a = 5, b = 6; if (a == b) {x = 7;} else {x = 8;}',  # 23 - If-else com comparação
        'x = 10 + (5 * 2);',                                     # 24 - Expressão com parênteses
        'for (int i = 0; i < 5; i++) {a = a + i;}',              # 25 - Laço `for` com incremento simples
        'y = [1 + 2, 3 + 4];',                                   # 26 - Lista com operações dentro
        'a = myFunc(x, y, 5, 10);',                              # 27 - Chamada de função com múltiplos argumentos
        'z = [x, y, z];',                                        # 28 - Declaração de lista
        'x = sin(x) * cos(x) + log(x);',                         # 29 - Expressão matemática complexa
        'if (x != 0) {y = x + 1;} else {y = x - 1;}',           # 30 - Condição com `!=`
        'y = x * 2 - (z + 3);',                                  # 31 - Operação com parênteses e subtração
        'x = (y + z) > 10;',                                     # 32 - Comparação com resultado de operação
        'int x = 10;',                                           # 33 - Declaração de uma variável com atribuição
        'x = 100;',                                              # 33 - Atribuição de valor a uma variável 
        'int x;',                                                # 33 - Declaração de uma variável
        'x + y;'
    ]
            
    test_cases_invalid = [
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
        'else { x = 5; };'
    ]
    
    # print('+' + 52 * '-' + ' ANÁLISE LÉXICA '  + 52 * '-' + '+')
    # for _, case in enumerate(test_cases_valid):
    #     print(f'Teste número {_ + 1}')
        
    #     lexer.input(case)

    #     tokens_list = []

    #     while True:
    #         token = lexer.token() 
    #         if not token:
    #             break  
    #         tokens_list.append(token.type)  
        
    #     print(" ".join(tokens_list))
    
    print('+' + 51 * '-' + ' ANÁLISE SINTÁTICA '  + 54 * '-' + '+')
    print('+' + 52 * '-' + ' TESTES VÁLIDOS '  + 52 * '-' + '+')
    for idx, case in enumerate(test_cases_valid, start=1):
        print(f'Teste {idx}: {case}')
        try:
            result = parser.parse(case)
            print(f'Resultado: {result}\n')
        except Exception as e:
            print(f'Erro ao processar: {e}\n')

#    print('+' + 51 * '-' + ' TESTES INVÁLIDOS '  + 51 * '-' + '+')
#    for idx, case in enumerate(test_cases_invalid, start=1):
#        print(f'Teste {idx}: {case}')
#        try:
#            result = parser.parse(case)
#            print(f'Resultado: {result}\n')
#        except Exception as e:
#            print(f'Erro: {e}\n')
#
#    print('+' + 51 * '-' + ' MODO INTERATIVO '  + 52 * '-' + '+')
#    while True:
#        try:
#            s = input('Digite a expressão (ou "sair" para encerrar): ')
#            if s.lower() == 'sair':
#                break
#        except EOFError:
#            break
#        if not s:
#            continue
#        try:
#            result = parser.parse(s)
#            print(f'Resultado: {result}')
#        except Exception as e:
#            print(f'Erro: {e}')

if __name__ == '__main__':
    main()