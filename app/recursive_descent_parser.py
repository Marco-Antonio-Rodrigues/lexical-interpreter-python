from app.consts import Consts

class RecursiveDescentParser:
    """ i é int | f é float | E -> iK | E -> fK | K -> +iK | K -> +fK | K -> """
    
    def __init__(self, tokens: list):
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

        if error:
            return None, error

        if self.get_current_token() is not None and self.get_current_token().type == Consts.EOF:
            return result, None
        return None, "não encontrou EOF no final"

    def parse_E(self):
        if self.get_current_token() and self.get_current_token().type in {Consts.INT, Consts.FLOAT}:
            self.result += 'i' if self.get_current_token().type == Consts.INT else 'f'
            self.next_token()
            return self.parse_K()
        return None, "parse_E() falhou, entrada não inicia com um número válido"

    def parse_K(self):
        if self.get_current_token() and self.get_current_token().type == Consts.PLUS:
            self.next_token()
            if self.get_current_token() and self.get_current_token().type in {Consts.INT, Consts.FLOAT}:
                self.result += '+i' if self.get_current_token().type == Consts.INT else '+f'
                self.next_token()
                return self.parse_K()
            return None, "parse_K() falhou, '+' não foi seguido por um número válido"
        self.result += 'ε'
        return self.result, None
