from typing import List
from unittest import TestCase

from src.lexer.token import Token, TokenType
from src.lexer.lexer import Lexer


class LexerTest(TestCase):

    def test_illegal(self) -> None:
        source: str = '¡¿@'
        lexer: Lexer = Lexer(source)

        tokens: List[Token] = []
        for i in range(len(source)):
            tokens.append(lexer.next_token())

        expected_tokens: List[Token] = [
            Token(TokenType.ILLEGAL, '¡'),
            Token(TokenType.ILLEGAL, '¿'),
            Token(TokenType.ILLEGAL, '@'),
        ]

        self.assertEqual(tokens, expected_tokens)

    def test_one_character_operators(self) -> None:
        source: str = '=+-/*<>!'
        lexer: Lexer = Lexer(source)

        tokens: List[Token] = []

        for i in range(len(source)):
            tokens.append(lexer.next_token())

        expected_tokens: List[Token] = [
            Token(TokenType.ASSIGN, '='),
            Token(TokenType.PLUS, '+'),
            Token(TokenType.MINUS, "-"),
            Token(TokenType.DIVISION, "/"),
            Token(TokenType.MULTIPLICATION, "*"),
            Token(TokenType.LT, "<"),
            Token(TokenType.GT, ">"),
            Token(TokenType.NEGATION, "!"),
        ]

        self.assertEqual(tokens, expected_tokens)

    def test_eof(self) -> None:
        source: str = '+'
        lexer: Lexer = Lexer(source)

        tokens: List[Token] = []
        for i in range(len(source) + 1):
            tokens.append(lexer.next_token())

        expected_tokens: List[Token] = [
            Token(TokenType.PLUS, '+'),
            Token(TokenType.EOF, ''),
        ]

        self.assertEqual(tokens, expected_tokens)

    def test_delimiters(self) -> None:
        source: str = '(){},;'
        lexer: Lexer = Lexer(source)

        tokens: List[Token] = []
        for i in range(len(source)):
            tokens.append(lexer.next_token())

        expected_tokens: List[Token] = [
            Token(TokenType.LPAREN, '('),
            Token(TokenType.RPAREN, ')'),
            Token(TokenType.LBRACE, '{'),
            Token(TokenType.RBRACE, '}'),
            Token(TokenType.COMMA, ','),
            Token(TokenType.SEMICOLON, ';'),
        ]

        self.assertEqual(tokens, expected_tokens)

    def test_assignment(self) -> None:
        source: str = 'var num = 5;'
        lexer: Lexer = Lexer(source)

        tokens: List[Token] = []
        for i in range(5):
            tokens.append(lexer.next_token())

        expected_tokens: List[Token] = [
            Token(TokenType.VAR, 'var'),
            Token(TokenType.IDENT, 'num'),
            Token(TokenType.ASSIGN, '='),
            Token(TokenType.INT, '5'),
            Token(TokenType.SEMICOLON, ';'),
        ]

        self.assertEqual(tokens, expected_tokens)

    def test_function_declaration(self) -> None:
        source: str = '''
        var res = func(x, y) {
            x + y;
        };
        '''
        lexer: Lexer = Lexer(source)

        tokens: List[Token] = []
        for i in range(16):
            tokens.append(lexer.next_token())

        expected_tokens: List[Token] = [
            Token(TokenType.VAR, 'var'),
            Token(TokenType.IDENT, 'res'),
            Token(TokenType.ASSIGN, '='),
            Token(TokenType.FUNCTION, 'func'),
            Token(TokenType.LPAREN, '('),
            Token(TokenType.IDENT, 'x'),
            Token(TokenType.COMMA, ','),
            Token(TokenType.IDENT, 'y'),
            Token(TokenType.RPAREN, ')'),
            Token(TokenType.LBRACE, '{'),
            Token(TokenType.IDENT, 'x'),
            Token(TokenType.PLUS, '+'),
            Token(TokenType.IDENT, 'y'),
            Token(TokenType.SEMICOLON, ';'),
            Token(TokenType.RBRACE, '}'),
            Token(TokenType.SEMICOLON, ';'),
        ]

        self.assertEqual(tokens, expected_tokens)

    def test_function_call(self) -> None:
        source: str = 'var res = sum(x, y);'
        lexer: Lexer = Lexer(source)

        tokens: List[Token] = []
        for i in range(10):
            tokens.append(lexer.next_token())

        expected_tokens: List[Token] = [
            Token(TokenType.VAR, 'var'),
            Token(TokenType.IDENT, 'res'),
            Token(TokenType.ASSIGN, '='),
            Token(TokenType.IDENT, 'sum'),
            Token(TokenType.LPAREN, '('),
            Token(TokenType.IDENT, 'x'),
            Token(TokenType.COMMA, ','),
            Token(TokenType.IDENT, 'y'),
            Token(TokenType.RPAREN, ')'),
            Token(TokenType.SEMICOLON, ';'),
        ]

        self.assertEqual(tokens, expected_tokens)

    def test_control_statement(self) -> None:
        source: str = '''
        if (5 < 10) {
            return true;
        } else {
            return false;
        }
        '''
        lexer: Lexer = Lexer(source)

        tokens: List[Token] = []
        for i in range(17):
            tokens.append(lexer.next_token())

        expected_tokens: List[Token] = [
            Token(TokenType.IF, 'if'),
            Token(TokenType.LPAREN, '('),
            Token(TokenType.INT, '5'),
            Token(TokenType.LT, '<'),
            Token(TokenType.INT, '10'),
            Token(TokenType.RPAREN, ')'),
            Token(TokenType.LBRACE, '{'),
            Token(TokenType.RETURN, 'return'),
            Token(TokenType.TRUE, 'true'),
            Token(TokenType.SEMICOLON, ';'),
            Token(TokenType.RBRACE, '}'),
            Token(TokenType.ELSE, 'else'),
            Token(TokenType.LBRACE, '{'),
            Token(TokenType.RETURN, 'return'),
            Token(TokenType.FALSE, 'false'),
            Token(TokenType.SEMICOLON, ';'),
            Token(TokenType.RBRACE, '}'),
        ]
        self.assertEqual(tokens, expected_tokens)

    def test_two_character_operations(self) -> None:
        source: str = '''
        10 == 10;
        10 != 9;
        '''
        lexer: Lexer = Lexer(source)

        tokens: List[Token] = []
        for i in range(8):
            tokens.append(lexer.next_token())

        expected_tokens: List[Token] = [
            Token(TokenType.INT, '10'),
            Token(TokenType.EQ, '=='),
            Token(TokenType.INT, '10'),
            Token(TokenType.SEMICOLON, ';'),
            Token(TokenType.INT, '10'),
            Token(TokenType.NOT_EQ, '!='),
            Token(TokenType.INT, '9'),
            Token(TokenType.SEMICOLON, ';'),
        ]

        self.assertEqual(tokens, expected_tokens)

    def test_complex_var_name(self) -> None:
        source: str = 'var num_1 = 10;'
        lexer: Lexer = Lexer(source)

        tokens: List[Token] = []
        for i in range(5):
            tokens.append(lexer.next_token())

        expected_tokens: List[Token] = [
            Token(TokenType.VAR, 'var'),
            Token(TokenType.IDENT, 'num_1'),
            Token(TokenType.ASSIGN, '='),
            Token(TokenType.INT, '10'),
            Token(TokenType.SEMICOLON, ';'),
        ]

        self.assertEqual(tokens, expected_tokens)
