from typing import Optional

from .ast import Program, Statement, VarStatement, Identifier
from ..lexer.lexer import Lexer
from ..lexer.token import Token, TokenType


class Parser:

    def __init__(self, lexer: Lexer) -> None:
        self._lexer = lexer
        self._current_token: Optional[Token] = None
        self._peek_token: Optional[Token] = None

        self._advance_tokens()
        self._advance_tokens()

    def parse_program(self) -> Program:
        program: Program = Program(statements=[])

        assert self._current_token
        while self._current_token.token_type != TokenType.EOF:
            statement = self._parse_statement()
            if statement:
                program.statements.append(statement)
            self._advance_tokens()
        return program

    def _advance_tokens(self) -> None:
        self._current_token = self._peek_token
        self._peek_token = self._lexer.next_token()

    def _expected_token(self, token_type: TokenType) -> bool:
        assert self._peek_token
        if self._peek_token.token_type == token_type:
            self._advance_tokens()
            return True
        return False

    def _parse_var_statement(self) -> Optional[VarStatement]:
        assert self._current_token
        var_statement: VarStatement = VarStatement(token=self._current_token)

        if not self._expected_token(TokenType.IDENT):
            return None
        var_statement.name = Identifier(
            token=self._current_token,
            value=self._current_token.literal
        )

        if not self._expected_token(TokenType.ASSIGN):
            return None

        # TODO finish when learned how to parse expressions
        while self._current_token.token_type != TokenType.SEMICOLON:
            self._advance_tokens()

        return var_statement

    def _parse_statement(self) -> Optional[Statement]:
        assert self._current_token
        if self._current_token.token_type == TokenType.VAR:
            return self._parse_var_statement()
        return None
