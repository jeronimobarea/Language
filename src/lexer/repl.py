from .lexer import Lexer
from .token import (
    Token,
    TokenType,
)

EOF_TOKEN: Token = Token(TokenType.EOF, '')


def start_repl() -> None:
    """
    Little version of an interactive REPL.
    Right know it only processes the characters and shows the TokenType of the written syntax.
    """
    while (source := input('>> ')) != 'exit()':
        lexer: Lexer = Lexer(source)

        while (token := lexer.next_token()) != EOF_TOKEN:
            print(token)
