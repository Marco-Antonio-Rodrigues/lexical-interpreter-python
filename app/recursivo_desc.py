from app.Consts import Consts
from app.Error import Error

""" i é int
 E-> iK
 K -> +iK
 K -> 
"""
class RecDescendente:
    def __init__(self, toks):
        self.tokens = toks
        self.id = -1
        self.current = None
        self.txt = ''
        
    def nextToken(self):
        self.id += 1
        if self.id < len(self.tokens):
            self.current = self.tokens[self.id]
        return self.current
    
    def currentTok(self):
        return self.current
        
    def start(self): 
        self.nextToken()
        a, e = self.E()
        if self.currentTok().type != Consts.EOF:
            return None, (e+":Error nao $ no final")
        return a, e
    
    def K(self):
        if self.currentTok().type == Consts.PLUS:
            self.nextToken()
            if self.currentTok().type == Consts.INT:
                self.nextToken()
                self.txt += "+i"
                a, e = self.K()
                return self.txt, e
            else:
                return self.txt, "erro não é inteiro (final?)"
        self.txt += "e"
        return self.txt, None
    
    def E(self):
        if self.currentTok().type == Consts.INT:
            self.txt += "i"
            self.nextToken()
            a, e = self.K()
            return a, e
        return None, "Falha E(), precisa iniciar com inteiro"
