# BNF

O **Backus-Naur Form (BNF)** é um padrão usado para descrever a gramática de linguagens de programação e outras linguagens formais. Ele define a estrutura da linguagem de forma precisa e rigorosa, sendo amplamente utilizado em compiladores, interpretadores e documentação técnica.

---

## Estrutura Básica do BNF

O BNF utiliza **produções** para descrever regras. Cada produção é composta por:

1. **Não Terminais**:
   - Elementos abstratos da linguagem que precisam ser definidos por outras regras.
   - Representados entre `<>` (ex.: `<expression>`, `<term>`).

2. **Terminais**:
   - Elementos literais da linguagem, como palavras-chave, números e operadores.
   - Geralmente escritos como estão.

3. **Produções**:
   - Cada regra tem o formato:
     ```bnf
     <não-terminal> ::= <expressão>
     ```
   - Usa `|` para indicar alternativas.

4. **Recursão**:
   - Permite definir estruturas aninhadas.

---

## Exemplo de Gramática em BNF

Vamos criar a gramática de uma calculadora simples:

```bnf
<expression> ::= <term> "+" <term>
              | <term> "-" <term>
              | <term>

<term>       ::= <factor> "*" <factor>
              | <factor> "/" <factor>
              | <factor>

<factor>     ::= <number>
              | "(" <expression> ")"

<number>     ::= "0" | "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9"
```

---

## Elementos do BNF

| **Elemento**         | **Descrição**                                                                                           | **Exemplo**                     |
|-----------------------|-------------------------------------------------------------------------------------------------------|----------------------------------|
| **Não Terminais**     | Representam elementos abstratos definidos por outras regras.                                          | `<expression>`, `<term>`        |
| **Terminais**         | São os símbolos literais da linguagem.                                                               | `"+"`, `"("`, `"9"`             |
| **Produções**         | Relacionam não terminais a uma ou mais expressões.                                                    | `<expression> ::= <term> "+" <term>` |
| **Alternativas**      | Usadas para descrever várias opções para a mesma regra, separadas por `|`.                            | `<number> ::= "0" | "1"`        |
| **Recursão**          | Permite que uma regra referencie a si mesma, criando estruturas aninhadas.                            | `<expression> ::= <expression> "+" <term>` |

---

## Leitura de uma Gramática BNF

Para o exemplo:
```bnf
<expression> ::= <term> "+" <term>
              | <term>
<term>       ::= <factor> "*" <factor>
              | <factor>
<factor>     ::= <number>
<number>     ::= "0" | "1" | "2"
```

- `<expression>` pode ser:
  - Um `<term>` seguido de `+` e outro `<term>`.
  - Ou simplesmente um `<term>`.
- `<term>` pode ser:
  - Um `<factor>` multiplicado por outro `<factor>`.
  - Ou apenas um `<factor>`.
- `<factor>` é sempre um `<number>`.
- `<number>` pode ser `"0"`, `"1"` ou `"2"`.

**Exemplo válido**:  
```text
1 + 2 * 0
```

---

## Vantagens do BNF

1. **Clareza**:
   - Define a linguagem de forma rigorosa e legível.

2. **Simplicidade**:
   - Minimalista, sem muitos símbolos adicionais.

3. **Recursão**:
   - Facilita a definição de estruturas aninhadas, como expressões matemáticas e blocos de código.

---

## Limitações do BNF

1. **Expressividade Limitada**:
   - Difícil lidar com detalhes opcionais ou repetições sem tornar a gramática complexa.

2. **Falta de Recursos Avançados**:
   - Não suporta elementos como expressões regulares diretamente.

---

## Ferramentas para Trabalhar com BNF

1. **ANTLR**:
   - Aceita variações do BNF (como EBNF) e gera analisadores léxicos e sintáticos.
   - [https://www.antlr.org/](https://www.antlr.org/)

2. **Railroad Diagram Generators**:
   - Geram diagramas visuais a partir da gramática BNF.
   - [https://bottlecaps.de/rr/](https://bottlecaps.de/rr/)

3. **PLY (Python Lex-Yacc)**:
   - Permite implementar a gramática em Python.

---

Se precisar de mais informações ou exemplos, é só perguntar! 😊