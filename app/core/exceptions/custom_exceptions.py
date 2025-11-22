class SwarvedBaseException(Exception):
    
    def __init__(self, message: str, details: dict | None = None):
        self.message = message
        self.details = details or {}
        super().__init__(self.message)


class LLMException(SwarvedBaseException):
    pass


class EmbeddingException(SwarvedBaseException):
    pass


class VectorDBException(SwarvedBaseException):
    pass


class DocumentException(SwarvedBaseException):
    pass


class IngestionException(SwarvedBaseException):
    pass