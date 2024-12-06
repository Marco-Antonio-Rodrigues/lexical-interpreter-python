# Lexical Interpreter

Este é um projeto de interpretação lexical para uma linguagem específica, desenvolvido em Python. Ele é composto por módulos que realizam diferentes etapas de análise, como tokenização, análise de erros e execução interativa.

## 📁 Estrutura do Projeto

```bash
LEXICAL-INTERPRETER/
├── app/                    # Código principal do interpretador
│   ├── __init__.py         # Arquivo de inicialização do módulo
│   ├── Consts.py           # Constantes usadas no projeto
│   ├── Error.py            # Classe de tratamento de erros
│   ├── Lexer.py            # Lexer: módulo de análise lexical
│   ├── Repl.py             # REPL: Loop interativo de execução
│   └── Token.py            # Definição e manipulação de tokens
├── tests/                  # Diretório de testes
├── .gitignore              # Arquivos e pastas ignorados pelo Git
├── Gramatica.txt           # Arquivo de definição da gramática da linguagem
├── main.py                 # Ponto de entrada do programa
├── poetry.lock             # Arquivo de bloqueio do Poetry
└── pyproject.toml          # Arquivo de configuração do Poetry
```

## 🛠️ Funcionalidades

- **Análise Lexical (Lexer):**
  - Identifica e separa tokens do código-fonte com base na gramática especificada.
  
- **Tratamento de Erros (Error):**
  - Gera mensagens claras e detalhadas para erros encontrados durante a análise lexical.
  
- **Loop Interativo (REPL):**
  - Permite que o usuário interaja diretamente com o interpretador em um ambiente de linha de comando.

- **Definição de Tokens (Token):**
  - Representa os diferentes tipos de tokens usados na linguagem.

## 🚀 Como Executar

### Pré-requisitos
- Python 3.8 ou superior
- Poetry (para gerenciamento de dependências)

### Instalação

1. Clone o repositório:

   ```bash
   git clone <url_do_repositorio>
   cd lexical-interpreter
   ```

2. Instale as dependências usando o Poetry:

   ```bash
   poetry install
   ```

3. Ative o ambiente virtual:

   ```bash
   poetry shell
   ```

4. Execute o programa principal:

   ```bash
   python main.py
   ```

## 🧪 Testes

Para rodar os testes:

1. Certifique-se de que as dependências estão instaladas.
2. Execute os testes com:

   ```bash
   poetry run pytest
   ```

## 📜 Gramática

A gramática da linguagem utilizada está definida no arquivo `Gramatica.txt`. Consulte este arquivo para entender as regras e estruturas reconhecidas pelo interpretador.