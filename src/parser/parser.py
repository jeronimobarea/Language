from typing import Optional, List, Callable, Dict

from .ast import Program, Statement, VarStatement, Identifier, ReturnStatement, Expression
from ..lexer.lexer import Lexer
from ..lexer.token import Token, TokenType

PrefixParseFn = Callable[[], Optional[Expression]]
InfixParseFn = Callable[[Expression], Optional[Expression]]
PrefixParseFns = Dict[TokenType, PrefixParseFn]
InfixParseFns = Dict[TokenType, InfixParseFn]


class Parser:

    def __init__(self, lexer: Lexer) -> None:
        self._lexer = lexer
        self._current_token: Optional[Token] = None
        self._peek_token: Optional[Token] = None
        self._errors: List[str] = []

        self._prefix_parse_fns: PrefixParseFns = self._register_prefix_fns()
        self._infix_parse_fns: InfixParseFns = self._register_infix_fns()

        self._advance_tokens()
        self._advance_tokens()

    @property
    def errors(self) -> List[str]:
        return self._errors

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
        self._expected_token_error(token_type)
        return False

    def _expected_token_error(self, token_type: TokenType) -> None:
        assert self._peek_token
        error = f'The expected token was {token_type} ' + \
                f'but got {self._peek_token.token_type}'
        self._errors.append(error)

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

    def _parse_return_statement(self) -> Optional[ReturnStatement]:
        assert self._current_token
        return_statement = ReturnStatement(token=self._current_token)
        self._advance_tokens()

        # TODO finish when learned how to parse expressions
        while self._current_token.token_type != TokenType.SEMICOLON:
            self._advance_tokens()
        return return_statement

    def _parse_statement(self) -> Optional[Statement]:
        assert self._current_token
        if self._current_token.token_type == TokenType.VAR:
            return self._parse_var_statement()
        elif self._current_token.token_type == TokenType.RETURN:
            return self._parse_return_statement()
        return None

    def _register_infix_fns(self) -> InfixParseFns:
        return {}

    def _register_prefix_fns(self) -> PrefixParseFns:
        return {}
