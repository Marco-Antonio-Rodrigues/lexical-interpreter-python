# PLY

O **[PLY (Python Lex-Yacc)](https://github.com/dabeaz/ply)** usa **expressões regulares** para definir os padrões que o **Lexer** deve reconhecer. As expressões regulares seguem o padrão da biblioteca `re` do Python.

---

## Elementos das Expressões Regulares

| **Elemento**         | **Descrição**                                                                                           | **Exemplo**                     |
|-----------------------|-------------------------------------------------------------------------------------------------------|----------------------------------|
| **Caractere Literal** | Reconhece um caractere literal específico.                                                            | `a` reconhece apenas `a`.       |
| **Conjuntos**         | Usa colchetes `[]` para corresponder a um conjunto de caracteres.                                      | `[a-z]` corresponde a letras minúsculas de `a` a `z`. |
| **Quantificadores**   | Define quantas vezes um padrão deve aparecer.                                                         | `a+` corresponde a `a`, `aa`, etc. |
| **Alternância**       | Usa `|` para corresponder a uma ou outra alternativa.                                                 | `a|b` corresponde a `a` ou `b`. |
| **Agrupamento**       | Usa parênteses para agrupar partes de uma expressão regular.                                           | `(ab)+` corresponde a `ab`, `abab`, etc. |
| **Meta-caracteres**   | Caracteres especiais que têm significados específicos em expressões regulares.                        | `\d` para dígitos, `\w` para caracteres alfanuméricos. |
| **Escapando**         | Usa `\` para tratar meta-caracteres como literais.                                                    | `\+` corresponde ao caractere `+`. |
| **Âncoras**           | Define posições na string, como início ou fim.                                                        | `^abc$` corresponde exatamente a `abc`. |

---

## Recursos Comuns do PLY

### Caractere Literal

```python
t_PLUS = r'\+'
```

- Corresponde apenas ao caractere `+`.

### Grupos

```python
t_IF_OR_ELSE = r'if|else'
```

- Corresponde à palavra `if` ou `else`.

### Quantificadores

| Símbolo  | Descrição                          |
|----------|------------------------------------|
| `*`      | Zero ou mais vezes.               |
| `+`      | Uma ou mais vezes.                |
| `?`      | Zero ou uma vez.                  |
| `{n}`    | Exatamente `n` vezes.             |
| `{n,m}`  | De `n` até `m` vezes.             |

**Exemplo:**

```python
t_NUMBER = r'\d+(\.\d+)?'
```

- Corresponde a números inteiros (`123`) ou decimais (`123.45`).

### Conjuntos de Caracteres

```python
t_LETTER = r'[a-zA-Z]'
```

- Corresponde a qualquer letra maiúscula ou minúscula.

```python
t_DIGIT = r'[0-9]'
```

- Corresponde a qualquer dígito.

### Escapando

```python
t_LPAREN = r'\('
t_RPAREN = r'\)'
```

- Corresponde a `(` e `)`.

### Âncoras

| Âncora | Descrição                       |
|--------|---------------------------------|
| `^`    | Início da string.              |
| `$`    | Fim da string.                 |

**Exemplo:**

```python
r'^[A-Za-z_][A-Za-z0-9_]*$'
```

- Corresponde a identificadores válidos que devem estar sozinhos na entrada.

### Meta-caracteres Comuns

| Meta-caractere | Descrição                          | Exemplo             |
|----------------|------------------------------------|---------------------|
| `.`            | Qualquer caractere, exceto nova linha. | `a.b` → `acb`, `axb`. |
| `\d`           | Dígitos (0-9).                    | `\d+` → `123`, `4567`. |
| `\w`           | Letras, números ou `_`.           | `\w+` → `abc123`, `x_y`. |
| `\s`           | Espaços em branco.               | `\s+` → ` `, `\t`. |
| `\b`           | Limite de palavra.                | `\bword\b`.         |

---

## Regras do PLY

### Definir Tokens como Funções ou Variáveis

- **Funções** são úteis para adicionar comportamento, como conversão de valores:

```python
def t_NUMBER(t):
    r'\d+(\.\d+)?'
    t.value = float(t.value)  # Converte o número para float
    return t
```

- **Variáveis** são suficientes para padrões simples:

```python
t_PLUS = r'\+'
```

### Ordem Importa

- O Lexer aplica as regras **na ordem em que elas são definidas**.
- Coloque regras mais específicas antes das gerais.

## example

```python

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

```