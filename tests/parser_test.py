from typing import List, cast
from unittest import TestCase

from src.lexer.lexer import Lexer
from src.parser.ast import Program, VarStatement
from src.parser.parser import Parser


class ParserTest(TestCase):

    def test_parse_program(self) -> None:
        source: str = 'var x = 5;'
        lexer: Lexer = Lexer(source)
        parser: Parser = Parser(lexer)

        program: Program = parser.parse_program()

        self.assertIsNotNone(program)
        self.assertIsInstance(program, Program)

    def test_var_statements(self) -> None:
        source: str = '''
        var x = 5;
        var y = 10;
        var foo = 20;
        '''
        lexer: Lexer = Lexer(source)
        parser: Parser = Parser(lexer)

        program: Program = parser.parse_program()

        self.assertEqual(len(program.statements), 3)

        for statement in program.statements:
            self.assertEqual(statement.token_literal(), 'var')
            self.assertIsInstance(statement, VarStatement)

    def test_names_in_let_statements(self) -> None:
        source: str = '''
        var x = 5;
        var y = 10;
        var foo = 20;
        '''
        lexer: Lexer = Lexer(source)
        parser: Parser = Parser(lexer)

        program: Program = parser.parse_program()

        names: List[str] = []
        for statement in program.statements:
            statement = cast(VarStatement, statement)
            assert statement.name
            names.append(statement.name.value)

        expected_names: List[str] = ['x', 'y', 'foo']

        self.assertEqual(names, expected_names)

    def test_parse_errors(self) -> None:
        source: str = 'var x 5;'
        lexer: Lexer = Lexer(source)
        parser: Parser = Parser(lexer)
