from app.consts import Consts
from app.token import Token
from app.error import Error

class Lexer:
    def __init__(self, source_code):
        self.code = source_code
        self.current = None
        self.indice, self.coluna, self.linha = -1, -1, 0
        self.__advance()
        
    def __advance(self):
        self.__advanceCalc(self.current)
        self.current = self.code[self.indice] if self.indice < len(self.code) else None
        

    def __advanceCalc(self, _char=None):
        self.indice += 1
        self.coluna += 1
        if _char == '\n':
                self.linha += 1
                self.coluna = 0
        return self
    
    def makeTokens(self):
        tokens = []
        while self.current != None:
            if self.current in ' \t':
                self.__advance()
            elif self.current in Consts.DIGITOS:
                tokens.append(self.__makeNumber())
            elif self.current == '"':
                tokens.append(self.__makestring())
            elif self.current in Consts.LETRAS:
                tokens.append(self.__make_id())
            elif self.current == Consts.PLUS:
                tokens.append(Token(Consts.PLUS))
                self.__advance()
            elif self.current == Consts.MINUS:
                tokens.append(Token(Consts.MINUS))
                self.__advance()
            elif self.current == Consts.MUL:
                tokens.append(Token(Consts.MUL))
                self.__advance()
            elif self.current == Consts.DIV:
                tokens.append(Token(Consts.DIV))
                self.__advance()
            elif self.current == Consts.LPAR:
                tokens.append(Token(Consts.LPAR))
                self.__advance()
            elif self.current == Consts.RPAR:
                tokens.append(Token(Consts.RPAR))
                self.__advance()
            elif self.current == Consts.ASSIGN:
                tokens.append(Token(Consts.ASSIGN))
                self.__advance()
            elif self.current == Consts.SEMICOLON:
                tokens.append(Token(Consts.SEMICOLON))
                self.__advance()
            elif self.current == Consts.COMMA:
                tokens.append(Token(Consts.COMMA))
                self.__advance()
            elif self.current == Consts.LSQUARE:
                tokens.append(Token(Consts.LSQUARE))
                self.__advance()
            elif self.current == Consts.RSQUARE:
                tokens.append(Token(Consts.RSQUARE))
                self.__advance()
            elif self.current == Consts.LBRACE:
                tokens.append(Token(Consts.LBRACE))
                self.__advance()
            elif self.current == Consts.RBRACE:
                tokens.append(Token(Consts.RBRACE))
                self.__advance()
            elif self.current == Consts.POW:
                tokens.append(Token(Consts.POW))
                self.__advance()
            elif self.current == Consts.NEQ:
                tokens.append(Token(Consts.NEQ))
                self.__advance()
            elif self.current == Consts.EQ:
                tokens.append(Token(Consts.EQ))
                self.__advance()
            elif self.current == Consts.GEQ:
                tokens.append(Token(Consts.GEQ))
                self.__advance()
            elif self.current == Consts.LEQ:
                tokens.append(Token(Consts.LEQ))
                self.__advance()
            elif self.current == Consts.GT:
                tokens.append(Token(Consts.GT))
                self.__advance()
            elif self.current == Consts.LT:
                tokens.append(Token(Consts.LT))
                self.__advance()
            else:
                self.__advance()
                return [], Error.lexer_error(message=f"lex-symbol '{self.current}' fail!",details=f"line: {self.linha}, column: {self.coluna}, indice: {self.indice}")

        tokens.append(Token(Consts.EOF))
        return tokens, None

    def __makeNumber(self):
        """return int or float"""
        strNumber = ''
        dotCount = 0
        while self.current != None and self.current in Consts.DIGITOS + '.':
            if self.current == '.':
                if dotCount == 1: break
                dotCount += 1
                strNumber += '.'
            else:
                strNumber += self.current
            self.__advance()
        if dotCount == 0:
            return Token(Consts.INT, int(strNumber))
        else:
            return Token(Consts.FLOAT, float(strNumber))
    
    def __makestring(self):
        stri = ""
        bypass = False
        self.__advance()
        specialChars = {'n':'\n', 't': '\t'}
        while (self.current != None and (self.current != '"' or bypass)):
            if (bypass):
                c = specialChars.get(self.current, self.current)
                stri += c
                bypass = False
            else:
                if (self.current == '\\'):
                    bypass = True
                else:
                    stri += self.current
            self.__advance()

        self.__advance()
        return Token(Consts.STRING, stri)
    
    def __make_id(self):
        """ variaveis, funções e palavras reservadas"""
        id = ""
        while self.current!= None and self.current in Consts.LETRAS_DIGITOS + Consts.UNDER:
            id += self.current
            self.__advance()
        if id in Consts.KEYS:
            return Token(Consts.KEY, id)
        return Token(Consts.ID, id)
    