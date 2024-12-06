class Error(Exception):
    RUN_TIME_ERROR = "RunTime Error"
    PARSER_ERROR = "Parser Error"
    LEXER_ERROR = "Lexer Error"

    def __init__(self, error_type, message, details=None):
        super().__init__(message)
        self.error_type = error_type
        self.message = message
        self.details = details

    def __repr__(self):
        base_message = f"[{self.error_type}] {self.message}"
        if self.details:
            base_message += f"\nDetalhes: {self.details}"
        return base_message

    def __str__(self):
        return self.__repr__()

    @classmethod
    def runtime_error(cls, message, details=None):
        return cls(cls.RUN_TIME_ERROR, message, details)

    @classmethod
    def parser_error(cls, message, details=None):
        return cls(cls.PARSER_ERROR, message, details)

    @classmethod
    def lexer_error(cls, message, details=None):
        return cls(cls.LEXER_ERROR, message, details)

    @staticmethod
    def get_class_name(obj):
        return type(obj).__name__

    @staticmethod
    def singleton_message(obj):
        class_name = Error.get_class_name(obj)
        return (
            f"Singleton em {class_name}\n"
            f"Para corrigir:\n - Onde codificou '{class_name}()', use '{class_name}' para acessar a instância única."
        )
