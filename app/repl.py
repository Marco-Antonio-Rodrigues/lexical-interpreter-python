from app.lexer import Lexer
from cmd import Cmd
from app.recursivo_descent_parser import RecursiveDescentParser

class Repl(Cmd):
    prompt = 'UFC> '
    intro = "Bem-vindo!\nDigite:\n :h para ajuda\n :q para sair e imprimir o assembly\n :s para um exemplo!"

    def do_exit(self, _=None):
        """Encerra o REPL."""
        return True

    def help_exit(self):
        """Exibe as instruções para sair."""
        print("Digite:\n :q para sair\n :s para um exemplo!")
        return False

    def do_s(self, _=None):
        """Exibe exemplos para o usuário."""
        print("Exemplo de entrada:")
        print("    1+3*8*(1+2)")
        return False

    def default(self, inp):
        """Lida com entradas padrão."""
        if inp == ':q':
            return self.do_exit()
        elif inp == ':h':
            return self.help_exit()
        elif inp == ':s':
            return self.do_s()
        self.process_input(inp)
        return False

    do_EOF = do_exit
    help_EOF = help_exit

    def process_input(self, linha):
        """Executa o Lexer e o Parser na linha fornecida."""
        # Etapa 1: Análise Léxica
        tokens, lexer_error = Lexer(linha).makeTokens()
        if lexer_error:
            print(f"Erro no Lexer: {lexer_error}")
            return 
        print(f"Tokens gerados pelo Lexer: {tokens}")

        # Etapa 2: Análise Sintática
        parser = RecursiveDescentParser(tokens)
        semantic_node, parser_error = parser.parse()
        if parser_error:
            print(f"Erro no Parser: {parser_error}")
            return
        
        print(f"Resultado da análise sintática: {semantic_node}")
