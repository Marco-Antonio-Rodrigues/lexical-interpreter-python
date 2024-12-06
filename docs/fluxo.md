# Compilador/Interpretador

Um **compilador** ou **interpretador** transforma o código-fonte em uma forma executável ou compreensível pelo computador. Este processo é dividido em várias etapas bem definidas.

---

## 1. Entrada do Código-Fonte

O compilador ou interpretador recebe o código-fonte como uma string, geralmente escrito em uma linguagem de alto nível, como Python, C ou Java.

---

## 2. Análise Léxica (Lexical Analysis)

**Objetivo**: Quebrar o código-fonte em unidades menores chamadas **tokens**.

**Funcionamento**:
- O código é processado caractere por caractere.
- Tokens como palavras-chave (`if`, `while`), operadores (`+`, `-`, `=`), delimitadores (`(`, `)`), e identificadores (nomes de variáveis) são reconhecidos.

**Saída**: Uma lista de tokens.

**Exemplo**:
Para o código:
```python
x = 3 + 5
```
Tokens gerados:
```text
[IDENTIFIER(x), ASSIGN(=), NUMBER(3), PLUS(+), NUMBER(5)]
```

---

## 3. Análise Sintática (Syntax Analysis)

**Objetivo**: Garantir que a sequência de tokens segue as regras da gramática da linguagem.

**Funcionamento**:
- Os tokens são organizados em uma estrutura hierárquica chamada **árvore de sintaxe** ou **parse tree**.
- Erros sintáticos (ex.: esquecer um ponto e vírgula ou fechar um parêntese) são detectados.

**Saída**: Uma **árvore de sintaxe (Parse Tree)**.

**Exemplo**:
Para os tokens:
```text
[IDENTIFIER(x), ASSIGN(=), NUMBER(3), PLUS(+), NUMBER(5)]
```
Parse Tree:
```
     Assign
     /   \
  Name     +
   |      / \
   x     3   5
```

---

## 4. Análise Semântica (Semantic Analysis)

**Objetivo**: Verificar se o código faz sentido dentro do contexto da linguagem.

**Funcionamento**:
- Certifica-se de que as operações são válidas (ex.: não é permitido somar um número com uma string).
- Verifica o uso correto de variáveis, tipos e funções.

**Saída**: Uma árvore de sintaxe anotada com informações semânticas.

**Exemplo**:
```python
x = "hello" + 3  # Erro semântico: não pode somar string com número.
```

---

## 5. Geração da Árvore de Sintaxe Abstrata (AST)

**Objetivo**: Transformar a **Parse Tree** em uma **Abstract Syntax Tree (AST)**, que é uma forma mais simplificada e estruturada.

**Funcionamento**:
- Remove detalhes sintáticos redundantes da Parse Tree.
- Organiza os elementos essenciais em uma hierarquia.

**Saída**: Uma **AST**.

**Exemplo**:
Para o código `x = 3 + 5`, a AST seria:
```
    Assign
   /      \
 Name      +
  |      /   \
  x     3     5
```

---

## 6. Otimização (Opcional)

**Objetivo**: Melhorar o desempenho do código sem alterar seu comportamento.

**Funcionamento**:
- Remove código desnecessário (ex.: `x = 0; x = x + 1;` → `x = 1`).
- Simplifica expressões matemáticas (ex.: `2 * 3` → `6`).

**Saída**: Uma versão otimizada da AST ou código intermediário.

---

## 7. Geração de Código Intermediário

**Objetivo**: Traduzir a AST para uma representação intermediária (IR - Intermediate Representation), independente da linguagem ou da arquitetura.

**Saída**: Código intermediário.

**Exemplo**:
```text
LOAD 3
LOAD 5
ADD
STORE x
```

---

## 8. Geração de Código de Máquina

**Objetivo**: Traduzir o código intermediário ou a AST diretamente em **código de máquina** executável.

**Funcionamento**:
- A saída depende do tipo de compilador:
  - Um **compilador** gera diretamente o código de máquina.
  - Um **interpretador** pode executar a AST ou o código intermediário diretamente.

**Saída**: Código executável.

**Exemplo (em Assembly)**:
```asm
MOV R1, 3
MOV R2, 5
ADD R1, R2
MOV x, R1
```

---

## 9. Execução

- Um **compilador** gera um programa executável (ex.: `.exe`) que pode ser executado posteriormente.
- Um **interpretador** executa o código imediatamente, linha por linha ou diretamente da AST.

---

## Diferença entre Compilador e Interpretador

| Etapa                      | Compilador                             | Interpretador                     |
|----------------------------|----------------------------------------|-----------------------------------|
| **Saída Final**            | Código executável (ex.: `.exe`).       | Resultado imediato da execução.  |
| **Execução do Código**     | Após a compilação completa.            | Durante a análise do código.     |
| **Velocidade da Execução** | Geralmente mais rápida.                | Geralmente mais lenta.           |
| **Exemplo**                | GCC para C, javac para Java.           | Python, Ruby, PHP.               |