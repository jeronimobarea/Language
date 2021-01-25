from re import match

from .token import Token, TokenType, lookup_token_type


class Lexer:
    """
    The Lexer class reads all the Tokens of the program and fulfills all the
    Token instances with the required params (token_type, literal)

    param: _source -> The plain text of the program.
    param: _character -> The actual character we are processing.
    param: _read_position -> The next position of the text we are going to read.
    param: _position -> The actual position of the text we are processing.
    """

    def __init__(self, source: str) -> None:
        self._source: str = source
        self._character: str = ''
        self._read_position: int = 0
        self._position: int = 0

        self._read_character()

    def next_token(self) -> Token:
        """
        This function reads the token and with regex we make match with one of the defined
        TokenTypes, if we there is no valid token by default we send a TokenType.ILLEGAL
        """
        self._skip_whitespace()
        if match(r'^=$', self._character):
            """
            Here we check if the token contains the '=' symbol and the calculate if it corresponds
            to the assign (=) or the equals (==) symbol
            """
            if self._peek_character() == '=':
                token = self._make_two_character_token(TokenType.EQ)
            else:
                token = Token(TokenType.ASSIGN, self._character)
        elif match(r'^\+$', self._character):
            token = Token(TokenType.PLUS, self._character)
        elif match(r'^$', self._character):
            token = Token(TokenType.EOF, self._character)
        elif match(r'^\($', self._character):
            token = Token(TokenType.LPAREN, self._character)
        elif match(r'^\)$', self._character):
            token = Token(TokenType.RPAREN, self._character)
        elif match(r'^{$', self._character):
            token = Token(TokenType.LBRACE, self._character)
        elif match(r'^}$', self._character):
            token = Token(TokenType.RBRACE, self._character)
        elif match(r'^,$', self._character):
            token = Token(TokenType.COMMA, self._character)
        elif match(r'^;$', self._character):
            token = Token(TokenType.SEMICOLON, self._character)
        elif match(r'^<$', self._character):
            token = Token(TokenType.LT, self._character)
        elif match(r'^>$', self._character):
            token = Token(TokenType.GT, self._character)
        elif match(r'^-$', self._character):
            token = Token(TokenType.MINUS, self._character)
        elif match(r'^/$', self._character):
            token = Token(TokenType.DIVISION, self._character)
        elif match(r'^\*$', self._character):
            token = Token(TokenType.MULTIPLICATION, self._character)
        elif match(r'^!$', self._character):
            """
               Here we check if the token contains the '!' symbol and the calculate if it corresponds
               to the not (!) or the distinct (!=) symbol
               """
            if self._peek_character() == '=':
                token = self._make_two_character_token(TokenType.NOT_EQ)
            else:
                token = Token(TokenType.NEGATION, self._character)
        elif self._is_letter(self._character):
            literal = self._read_identifier()
            token_type = lookup_token_type(literal)
            return Token(token_type, literal)
        elif self._is_number(self._character):
            literal = self._read_number()
            return Token(TokenType.INT, literal)
        else:
            token = Token(TokenType.ILLEGAL, self._character)
        self._read_character()
        return token

    def _is_letter(self, character: str) -> bool:
        """
        Function for calculating if a character is a valid letter.
        """
        return bool(match(r'^[a-zA-Z_]$', character))

    def _is_number(self, character: str) -> bool:
        """
        Function for calculating if a character is a number
        """
        return bool(match(r'^\d$', character))

    def _make_two_character_token(self, token_type: TokenType) -> Token:
        """
        This function if used for calculating if we can make a two character Token with the actual one
        and the next character.
        """
        prefix = self._character
        self._read_character()
        suffix = self._character

        return Token(token_type, f'{prefix}{suffix}')

    def _peek_character(self) -> str:
        """
        TODO
        """
        if self._read_position >= len(self._source):
            return ''
        return self._source[self._read_position]

    def _read_character(self) -> None:
        """
        This function reads the next character when its called.
        """
        if self._read_position >= len(self._source):
            self._character = ''
        else:
            self._character = self._source[self._read_position]
        self._position = self._read_position
        self._read_position += 1

    def _read_identifier(self) -> str:
        """
        This function defines if the character is a TokenType.IDENT 'identifier'
        """
        initial_position = self._position
        while self._is_letter(self._character) or self._is_number(self._character):
            self._read_character()
        return self._source[initial_position:self._position]

    def _read_number(self) -> str:
        """
        This function reads all the numbers that belong to the same variable or function
        Example: var x = 555555555;
        In this example we will take the first 5 and then try to know if we need to continue
        reading the next chapters. 5, 55, 555, 555...5 until ';' and then it will stop.
        """
        initial_position = self._position
        while self._is_number(self._character):
            self._read_character()
        return self._source[initial_position:self._position]

    def _skip_whitespace(self) -> None:
        """
        This function is made for skipping all the whitespaces of the source program,
        because in the syntax is not relevant and we don't want to process empty characters.
        """
        while match(r'^\s$', self._character):
            self._read_character()
