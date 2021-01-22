from enum import (
    auto,
    Enum,
    unique
)
from typing import NamedTuple, Dict


@unique
class TokenType(Enum):
    """
    Token definitions of the language.
    """
    ASSIGN = auto()
    COMMA = auto()
    DIVISION = auto()
    ELSE = auto()
    EQ = auto()
    EOF = auto()
    FALSE = auto()
    FUNCTION = auto()
    GT = auto()
    IDENT = auto()
    IF = auto()
    ILLEGAL = auto()
    INT = auto()
    LBRACE = auto()
    LPAREN = auto()
    LT = auto()
    MINUS = auto()
    MULTIPLICATION = auto()
    NEGATION = auto()
    NOT_EQ = auto()
    PLUS = auto()
    RBRACE = auto()
    RETURN = auto()
    RPAREN = auto()
    SEMICOLON = auto()
    TRUE = auto()
    VAR = auto()


class Token(NamedTuple):
    token_type: TokenType
    literal: str

    def __str__(self) -> str:
        return f'Type: {self.token_type}, Literal: {self.literal}'


def lookup_token_type(literal: str) -> TokenType:
    keywords: Dict[str, TokenType] = {
        'else': TokenType.ELSE,
        'false': TokenType.FALSE,
        'func': TokenType.FUNCTION,
        'if': TokenType.IF,
        'return': TokenType.RETURN,
        'true': TokenType.TRUE,
        'var': TokenType.VAR,
    }
    return keywords.get(literal, TokenType.IDENT)
