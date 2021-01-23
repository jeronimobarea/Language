from unittest import TestCase

from src.lexer.token import Token, TokenType
from src.parser.ast import Program, VarStatement, Identifier, ReturnStatement


class ASTTest(TestCase):

    def test_var_statement(self) -> None:
        program: Program = Program(
            statements=[
                VarStatement(
                    token=Token(TokenType.VAR, literal='var'),
                    name=Identifier(
                        token=Token(TokenType.IDENT, literal='x'),
                        value='x',
                    ),
                    value=Identifier(
                        token=Token(TokenType.IDENT, literal='y'),
                        value='y',
                    ),
                ),
            ]
        )

        program_str = str(program)

        self.assertEqual(program_str, 'var x = y;')

    def test_return_statement(self) -> None:
        program: Program = Program(
            statements=[
                ReturnStatement(
                    token=Token(TokenType.RETURN, 'return'),
                    return_value=Identifier(
                        token=Token(TokenType.IDENT, 'x'),
                        value='x'
                    ),
                )
            ]
        )
        program_str = str(program)

        self.assertEqual(program_str, 'return x;')
