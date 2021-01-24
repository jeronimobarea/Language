from enum import IntEnum
from typing import Optional, List, Callable, Dict

from .ast import (
    Expression,
    ExpressionStatement,
    Identifier,
    Infix,
    Integer,
    Prefix,
    Program,
    ReturnStatement,
    Statement,
    VarStatement,
)
from ..lexer.lexer import Lexer
from ..lexer.token import Token, TokenType

PrefixParseFn = Callable[[], Optional[Expression]]
InfixParseFn = Callable[[Expression], Optional[Expression]]
PrefixParseFns = Dict[TokenType, PrefixParseFn]
InfixParseFns = Dict[TokenType, InfixParseFn]


class Precedence(IntEnum):
    LOWEST = 1
    EQUALS = 2
    LESS_GREATER = 3
    SUM = 4
    PRODUCT = 5
    PREFIX = 6
    CALL = 7


PRECEDENCES: Dict[TokenType, Precedence] = {
    TokenType.EQ: Precedence.EQUALS,
    TokenType.NOT_EQ: Precedence.EQUALS,
    TokenType.LT: Precedence.LESS_GREATER,
    TokenType.GT: Precedence.LESS_GREATER,
    TokenType.PLUS: Precedence.SUM,
    TokenType.MINUS: Precedence.SUM,
    TokenType.DIVISION: Precedence.PRODUCT,
    TokenType.MULTIPLICATION: Precedence.PRODUCT,
}


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

    def _current_precedence(self) -> Precedence:
        assert self._current_token
        try:
            return PRECEDENCES[self._current_token.token_type]
        except KeyError:
            return Precedence.LOWEST

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

    def _parse_expression(self, precedence: Precedence) -> Optional[Expression]:
        assert self._current_token
        try:
            prefix_parse_fn = self._prefix_parse_fns[self._current_token.token_type]
        except KeyError:
            self.errors.append(f'Could not find any function for parsing {self._current_token.literal}')
            return None

        left_expression = prefix_parse_fn()

        assert self._peek_token
        while (
                self._peek_token.token_type is not TokenType.SEMICOLON
                and precedence < self._peek_precedence()
        ):
            try:
                infix_parse_fn = self._infix_parse_fns[self._peek_token.token_type]
                self._advance_tokens()

                assert left_expression
                left_expression = infix_parse_fn(left_expression)
            except KeyError:
                return left_expression

        return left_expression

    def _parse_expression_statement(self) -> Optional[ExpressionStatement]:
        assert self._current_token
        expression_statement = ExpressionStatement(token=self._current_token)

        expression_statement.expression = self._parse_expression(Precedence.LOWEST)

        assert self._peek_token
        if self._peek_token.token_type == TokenType.SEMICOLON:
            self._advance_tokens()
        return expression_statement

    def _parse_identifier(self) -> Identifier:
        assert self._current_token
        return Identifier(token=self._current_token, value=self._current_token.literal)

    def _parse_infix_expression(self, left: Expression) -> Infix:
        assert self._current_token
        infix = Infix(token=self._current_token,
                      operator=self._current_token.literal,
                      left=left)
        precedence = self._current_precedence()

        self._advance_tokens()

        infix.right = self._parse_expression(precedence)
        return infix

    def _parse_integer(self) -> Optional[Integer]:
        assert self._current_token
        integer = Integer(token=self._current_token)

        try:
            integer.value = int(self._current_token.literal)
        except ValueError:
            self._errors.append(f'Error parsing {self._current_token} as integer')
            return None
        return integer

    def _parse_var_statement(self) -> Optional[VarStatement]:
        assert self._current_token
        var_statement: VarStatement = VarStatement(token=self._current_token)

        if not self._expected_token(TokenType.IDENT):
            return None
        var_statement.name = self._parse_identifier()

        if not self._expected_token(TokenType.ASSIGN):
            return None

        # TODO finish when learned how to parse expressions
        while self._current_token.token_type != TokenType.SEMICOLON:
            self._advance_tokens()

        return var_statement

    def _parse_prefix_expression(self) -> Expression:
        assert self._current_token
        prefix_expression = Prefix(token=self._current_token,
                                   operator=self._current_token.literal)
        self._advance_tokens()
        prefix_expression.right = self._parse_expression(Precedence.PREFIX)
        return prefix_expression

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
        return self._parse_expression_statement()

    def _peek_precedence(self) -> Precedence:
        assert self._peek_token
        try:
            return PRECEDENCES[self._peek_token.token_type]
        except KeyError:
            return Precedence.LOWEST

    def _register_infix_fns(self) -> InfixParseFns:
        return {
            TokenType.PLUS: self._parse_infix_expression,
            TokenType.MINUS: self._parse_infix_expression,
            TokenType.DIVISION: self._parse_infix_expression,
            TokenType.MULTIPLICATION: self._parse_infix_expression,
            TokenType.EQ: self._parse_infix_expression,
            TokenType.NOT_EQ: self._parse_infix_expression,
            TokenType.LT: self._parse_infix_expression,
            TokenType.GT: self._parse_infix_expression,
        }

    def _register_prefix_fns(self) -> PrefixParseFns:
        return {
            TokenType.IDENT: self._parse_identifier,
            TokenType.INT: self._parse_integer,
            TokenType.MINUS: self._parse_prefix_expression,
            TokenType.NEGATION: self._parse_prefix_expression,
        }
