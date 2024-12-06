from app.Consts import Consts

class RecursiveDescentParser:
    """ i é int | E-> iK | K -> +iK | K -> """
    
    def __init__(self, tokens):
        self.tokens = tokens
        self.current_index = -1
        self.current_token = None
        self.result = ''

    def next_token(self):
        self.current_index += 1
        self.current_token = self.tokens[self.current_index] if self.current_index < len(self.tokens) else None

    def get_current_token(self):
        return self.current_token

    def parse(self):
        self.next_token()
        result, error = self.parse_E()
        if self.get_current_token() is not None and self.get_current_token().type != Consts.EOF:
            return None, "não encontrou EOF no final"
        return result, error

    def parse_E(self):
        if self.get_current_token() and self.get_current_token().type == Consts.INT:
            self.result += 'i'
            self.next_token()
            return self.parse_K()
        return None, "parse_E() falhou, entrada não inicia com um inteiro"

    def parse_K(self):
        if self.get_current_token() and self.get_current_token().type == Consts.PLUS:
            self.next_token()
            if self.get_current_token() and self.get_current_token().type == Consts.INT:
                self.result += '+i'
                self.next_token()
                return self.parse_K()
            return None, "parse_K() falhou, '+' não foi seguido por um inteiro"
        self.result += 'ε'
        return self.result, None
