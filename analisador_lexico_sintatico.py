import ply.lex as lex
import ply.yacc as yacc

#--------------------------------------- Definição dos símbolos terminais (tokens) ---------------------------------------#

tokens = (
    'PLUS', 'MINUS', 'MUL', 'DIV', 'LPAR', 'RPAR', 'ASSIGN', 'LBRACK', 'RBRACK', 'COMMA',
    'SEMICOLON', 'LT', 'GT', 'LEQ', 'GEQ', 'EQ', 'NEQ', 'LBRACE', 'RBRACE',
    'IF', 'ELSE', 'ELIF', 'FOR', 'WHILE', 'INT', 'FLOAT', 'TRUE', 'FALSE', 'BOOL', 'VOID', 'RETURN',
    'ID', 'AND', 'OR', 'NOT'
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
    'true': 'TRUE',
    'false': 'FALSE',
    'bool': 'BOOL'
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
t_AND = r'\&\&'
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
    if t.type in ('TRUE', 'FALSE'):
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

#def p_program(p):
#    '''program : stmt_list'''
#    p[0] = ('Program', p[1])

def p_stmt_list(p):
    '''stmt_list : stmt stmt_list
                 | stmt'''
    if len(p) == 3: 
        p[0] = ('StmtList', p[1], p[2])  
    else:  
        p[0] = ('StmtList', p[1]) 

def p_stmt(p):
    '''stmt : if_stmt
            | var_stmt
            | func_declaration
            | return_stmt
            | exp_stmt
            | for_stmt
            | while_stmt'''
    p[0] = p[1]  

def p_if_stmt(p):
    '''if_stmt : IF LPAR rel_exp RPAR LBRACE stmt_list RBRACE elif_blocks else_block'''
    p[0] = ('IfStmt', p[3], p[6], p[8], p[9])

def p_elif_blocks(p):
    '''elif_blocks : elif_block elif_blocks
                   | '''  # Vazio
    if len(p) == 3:
        p[0] = (p[1],) + p[2]  
    else:
        p[0] = ()  

def p_elif_block(p):
    '''elif_block : ELIF LPAR rel_exp RPAR LBRACE stmt_list RBRACE'''
    p[0] = ('ElifBlock', p[3], p[6])

def p_else_block(p):
    '''else_block : ELSE LBRACE stmt_list RBRACE
                  | '''
    if len(p) == 5:
        p[0] = ('ElseBlock', p[3])
    else:
        p[0] = ()

def p_var_stmt(p):
    '''var_stmt : type ID var_assign_list SEMICOLON
                | ID ASSIGN exp SEMICOLON'''
    if len(p) == 5 and p[2] == '=':
        p[0] = ('VarStmt', None, p[1], p[2], p[3])  
    else:
        p[0] = ('VarStmt', p[1], p[2], p[3])
        
def p_var_assign_list(p):
    '''var_assign_list : ASSIGN exp
                       | COMMA ID var_assign_list
                       | '''  # Vazio
    if len(p) == 4:
        p[0] = (('ID', p[2]),) + p[3]
    elif len(p) == 3:
        p[0] = (('Assign', p[1], p[2]))
    else:
        p[0] = ()

def p_func_declaration(p):
    '''func_declaration : type ID LPAR arg_sequence_opt RPAR LBRACE stmt_list_opt return_stmt_opt RBRACE'''
    p[0] = ('FuncDeclaration', p[1], p[2], p[4], p[7])
    
def p_arg_sequence_opt(p):
    '''arg_sequence_opt : arg_sequence
                        | '''  # Vazio
    p[0] = p[1] if len(p) == 2 else ()
    
def p_arg_sequence(p):
    '''arg_sequence : type ID
                    | type ID COMMA arg_sequence'''
    if len(p) == 3:
        p[0] = ((p[1], p[2]))
    else:
        p[0] = ((p[1], p[2]),) + p[4]

def p_param_list_opt(p):
    '''param_list_opt : arg_sequence_opt
                      | '''  # Vazio
    p[0] = p[1] if len(p) == 2 else ()

def p_stmt_list_opt(p):
    '''stmt_list_opt : stmt_list
                     | '''  # Vazio
    p[0] = p[1] if len(p) == 2 else None

def p_return_stmt_opt(p):
    '''return_stmt_opt : return_stmt
                       | '''  # Vazio
    p[0] = p[1] if len(p) == 2 else None

def p_return_stmt(p):
    '''return_stmt : RETURN exp SEMICOLON
                   | RETURN SEMICOLON'''
    if len(p) == 4:  
        p[0] = ('ReturnStmt', p[2])
    else:  
        p[0] = ('ReturnStmt', None)

def p_exp_stmt(p):
    '''exp_stmt : exp SEMICOLON'''
    p[0] = ('ExpStmt', p[1])

def p_for_var_decl(p):
    '''for_var_decl : type ID ASSIGN exp
                    | type ID'''
    if len(p) == 5:  
        p[0] = ('ForVarDecl', p[1], p[2], p[4])
    else:  
        p[0] = ('ForVarDecl', p[1], p[2], None)

def p_for_stmt(p):
    '''for_stmt : FOR LPAR for_var_decl_opt SEMICOLON rel_exp_opt SEMICOLON exp_opt RPAR LBRACE stmt_list RBRACE'''
    p[0] = ('ForStmt', p[3], p[5], p[7], p[10])

def p_for_var_decl_opt(p):
    '''for_var_decl_opt : for_var_decl
                        | exp
                        | '''  # Vazio
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = None
    
def p_rel_exp_opt(p):
    '''rel_exp_opt : rel_exp
                   | '''  # Vazio
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = None

def p_exp_opt(p):
    '''exp_opt : exp
               | '''  # Vazio
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = None

def p_while_stmt(p):
    '''while_stmt : WHILE LPAR rel_exp RPAR LBRACE stmt_list RBRACE'''
    p[0] = ('WhileStmt', p[3], p[6])

def p_exp(p):
    '''exp : term
           | exp PLUS term
           | exp MINUS term
           | ID ASSIGN exp'''
    if len(p) == 4 and p[2] == '=':
        p[0] = ('Assign', p[1], p[3])
    elif len(p) == 2:
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
    p[0] = ('FuncCall', p[1], p[3] if len(p) == 5 else None)

def p_exp_sequence(p):
    '''exp_sequence : exp
                    | exp COMMA exp_sequence'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = [p[1]] + p[3]

def p_rel_exp(p):
    '''rel_exp : rel_exp OR rel_exp
               | rel_exp AND rel_exp
               | NOT rel_exp
               | exp rel_op exp
               | exp'''
    if len(p) == 4:
        p[0] = ('RelExp', p[1], p[2], p[3])
    elif len(p) == 3:
        p[0] = ('RelExp', p[1], p[2])
    else:
        p[0] = p[1]

def p_rel_op(p):
    '''rel_op : LT
              | LEQ
              | GT
              | GEQ
              | EQ
              | NEQ'''
    p[0] = p[1]

def p_type(p):
    '''type : INT
            | FLOAT
            | VOID'''
    p[0] = p[1]

def p_error(p):
    print("Erro de sintaxe em '%s'" % p.value if p else "Erro de sintaxe")

#--------------------------------------------------------- PARSER --------------------------------------------------------#

parser = yacc.yacc(start='stmt_list')

#--------------------------------------------------------- TESTE ---------------------------------------------------------#

def main():
    test_cases_valid = [
        'x = a + b * c;',                                                  # 1 - Operações com múltiplas variáveis
        'a = (b + c) * (d - e);',                                          # 2 - Operações com parênteses e múltiplos operadores
        'x = y == 10;',                                                    # 3 - Operação de comparação
        'if (x > 5 && y < 10) {z = 1;} else {z = 0;}',                     # 4 - Expressão com operador lógico
        'while (x < 10) {x = x + 1;}',                                     # 5 - Laço `while`
        'for (int i = 0; i < 10; i = i + 1) {sum = sum + i;}',             # 6 - Laço `for` com inicialização, condição e incremento
        'return x + y;',                                                   # 7 - Instrução `return` simples
        'int a = 2; b = 3; c = 4;',                                        # 8 - Declaração múltipla de variáveis
        'y = (a + b) / (c - d);',                                          # 9 - Expressões com divisão
        'int x = 10 + (y = 5);',                                           # 10 - Atribuição dentro de uma expressão
        'float x = 10.5; y = 20.3;',                                       # 11 - Declaração de variáveis flutuantes
        'while (x > 0) {x = x - 1;}',                                      # 12 - Laço `while`
        'if (x == 5) {y = 2;} else {y = 3;} ',                             # 13 - If-else com valores diferentes
        'int x = 0; y = 1; if (x == y) {a = 1;} else {a = 2;}',            # 14 - If-else simples
        'float z = sin(x) * cos(y);',                                      # 15 - Funções trigonométricas
        'int x = (a + b) * (c - d) / e;',                                  # 16 - Expressão com múltiplos operadores
        'for (int i = 0; i < 5; i = i + 1) {a = a + i;}',                  # 17 - Laço `for` com incremento simples
        'if (a != b) {a = 10;} else {b = 20;}',                            # 18 - Expressão de comparação e atribuição
        'y = sin(x) + cos(y);',                                            # 19 - Combinação de funções trigonométricas
        'z = log10(x) + sqrt(y);',                                         # 20 - Funções logarítmica e raiz
        'y = sqrt(x) + log(x);',                                           # 21 - Raiz quadrada e logaritmo em uma expressão
        'z = (x + y) * (sin(x) + cos(y));',                                # 22 - Expressão com funções trigonométricas
        'int a = 5; b = 6; if (a == b) {x = 7;} else {x = 8;}',            # 23 - If-else com comparação
        'x = 10 + (5 * 2);',                                               # 24 - Expressão com parênteses
        'y = [1 + 2, 3 + 4];',                                             # 25 - Lista com operações dentro
        'a = myFunc(x, y, 5, 10);',                                        # 26 - Chamada de função com múltiplos argumentos
        'z = [x, y, z];',                                                  # 27 - Declaração de lista
        'x = sin(x) * cos(x) + log(x);',                                   # 28 - Expressão matemática complexa
        'if (x != 0) {y = x + 1;} else {y = x - 1;}',                      # 29 - Condição com `!=`
        'y = x * 2 - (z + 3);',                                            # 30 - Operação com parênteses e subtração
        'x = (y + z) > 10;',                                               # 31 - Comparação com resultado de operação
        'int x = 10;',                                                     # 32 - Declaração de uma variável com atribuição
        'x = 100;',                                                        # 33 - Atribuição de valor a uma variável 
        'int x;',                                                          # 34 - Declaração de uma variável
        'x = true;',                                                       # 35 - Atribuição de valor boleano a variável
        'if (a != b) {a = 10;} elif (a > b) {b = 20;}',                    # 36 - Expressão de comparação e atribuição
        'if (a <= b) {a = 10;}',                                           # 37 - Expressão de comparação e atribuição
        'if (a >= b) {a = 10;} elif (a > b) {b = 20;} else {a = b - 1;}',  # 38 - Expressão de comparação e atribuição
        'if (a || b) {a = 10;} elif (a > b) {b = 20;}',                    # 39 - Expressão de comparação e atribuição
        'int soma(int a, int b) {return a + b;}',                          # 40 - Declaração de uma função 
        '\
        int fibonacci(int n) {\
            if (n <= 1) {\
                return n;\
            }\
            return fibonacci(n - 1) + fibonacci(n - 2);\
        }\
        \
        int main() {\
            int x = 10; y = 20; \
            float z;\
            z = 30.5;\
            int fibonacciNumber = 10;\
            int result = fibonacci(fibonacciNumber);\
            \
            if (x < y) {\
                z = z + x;\
            } elif (x == y) {\
                z = 0;\
            } else {\
                z = -1.0;\
            }\
            \
            for (int i = 0; i < 10; i = i + 1) {\
                z = z * 1.1;\
            }\
            \
            while (z > 50.0) {\
                z = z - 5.0;\
            }\
            \
            float calculaMedia(int a, int b) {\
                return (a + b) / 2.0;\
            }\
            \
            float media = calculaMedia(x, y);\
            \
            return 0;\
        }', # 41 - Bloco de código
        '\
        int main() {\
            int n = 5; \
            int fatorial_resultado = fatorial(n);\
            int soma_resultado = calculaSoma(n);\
            int fibonacci_resultado = fibonacci(n);\
            return 0;\
        }\
        \
        int fatorial(int n) {\
            int resultado = 1;\
            for (int i = 1; i <= n; i = i + 1) {\
                resultado = resultado * i;\
            }\
            return resultado;\
        }\
        \
        int calculaSoma(int n) {\
            int soma = 0;\
            for (int i = 1; i <= n; i = i + 1) {\
                soma = soma + i;\
            }\
            return soma;\
        }\
        \
        int fibonacci(int n) {\
            if (n <= 1) {\
                return n;\
            }\
            return fibonacci(n - 1) + fibonacci(n - 2);\
        }' # 42 - Bloco de código
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
        '[1, 2, 3,;',
        'else { x = 5; };'
    ]
    
#    print('+' + 54 * '-' + ' ANÁLISE LÉXICA '  + 54 * '-' + '+')
#    for _, case in enumerate(test_cases_valid):
#        print(f'Teste número {_ + 1}')
#        
#        lexer.input(case)
#
#        tokens_list = []
#
#        while True:
#            token = lexer.token() 
#            if not token:
#                break  
#            tokens_list.append(token.type)  
#
#        print(" ".join(tokens_list))
    
    print('+' + 53 * '-' + ' ANÁLISE SINTÁTICA '  + 52 * '-' + '+')
    print('+' + 124 * '-' + '+')
    print('+' + 54 * '-' + ' TESTES VÁLIDOS '  + 54 * '-' + '+')
    for idx, case in enumerate(test_cases_valid, start=1):
        print(f'Teste {idx}: {' '.join(case.split())}')
        try:
            result = parser.parse(case)
            print()
            print(f'Resultado do teste {idx}: {result}\n')
        except Exception as e:
            print(f'Erro ao processar: {e}\n')

#    print('+' + 53 * '-' + ' TESTES INVÁLIDOS '  + 53 * '-' + '+')
#    for idx, case in enumerate(test_cases_invalid, start=1):
#        print(f'Teste {idx}: {case}')
#        try:
#            result = parser.parse(case)
#            print(f'Resultado: {result}\n')
#        except Exception as e:
#            print(f'Erro: {e}\n')

#    print('+' + 53 * '-' + ' MODO INTERATIVO '  + 54 * '-' + '+')
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