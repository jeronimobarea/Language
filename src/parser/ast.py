from abc import ABC, abstractmethod
from typing import List, Optional

from ..lexer.token import Token


class ASTNode(ABC):
    """
    This is the definition of the ASTNode.
    This abstract class will inherit all the logic needed for the Statement and Expressions.

    function: toke_literal -> The value of the token
    function: __str__ -> The representation of the class Instance
    """

    @abstractmethod
    def token_literal(self) -> str:
        pass

    @abstractmethod
    def __str__(self) -> str:
        pass


class Statement(ASTNode):
    """
    This class will be used for all the language Statements var, return...
    """

    def __init__(self, token: Token) -> None:
        self.token = token

    def token_literal(self) -> str:
        return self.token.literal

    def __str__(self) -> str:
        pass


class Expression(ASTNode):
    """
    This class will be used for all the language Expressions integer, bool...
    """

    def __init__(self, token: Token) -> None:
        self.token = token

    def token_literal(self) -> str:
        return self.token.literal

    def __str__(self) -> str:
        pass


class Program(ASTNode):
    """
    This class will be the representation of the source code.

    param: statements -> All the detected commands of the program.
    """

    def __init__(self, statements: List[Statement]) -> None:
        self.statements = statements

    def token_literal(self) -> str:
        """
        returns the firsts literal of the list
        """
        if self.statements:
            return self.statements[0].token_literal()
        return ''

    def __str__(self) -> str:
        """
        returns all the statements parsed as string
        """
        out: List[str] = []
        for statement in self.statements:
            out.append(str(statement))
        return ''.join(out)


class Identifier(Expression):
    """
    Expression for representing the Identifier 'your_var_name'
    """

    def __init__(self, token: Token, value: str) -> None:
        super().__init__(token)
        self.value = value

    def __str__(self) -> str:
        return self.value


class VarStatement(Statement):
    """
    Statement for representing the Var 'var'

    param: token -> The token of the Statement
    param: name -> the name of the Identifier
    param: value -> value of the identifier

    example: var x = 10;
    var -> token
    x -> name
    10 -> value
    """

    def __init__(self,
                 token: Token,
                 name: Optional[Identifier] = None,
                 value: Optional[Expression] = None) -> None:
        super().__init__(token)
        self.name = name
        self.value = value

    def __str__(self) -> str:
        return f'{self.token_literal()} {str(self.name)} = {str(self.value)};'


class ReturnStatement(Statement):
    """
    Statement for representing the 'return'

    param: token -> The token of the statement.
    param: return_value -> The value that we are returning

    example: func() { return 10; }
    return -> token
    10 -> return_value
    """

    def __init__(self,
                 token: Token,
                 return_value: Optional[Expression] = None) -> None:
        super().__init__(token)
        self.return_value = return_value

    def __str__(self) -> str:
        return f'{self.token_literal()} {str(self.return_value)};'


class ExpressionStatement(Statement):
    """
    Statement for representing the Expressions

    param: token -> Expression token
    param: expression -> The value of the expression

    exampleL: 5;
    5 -> ExpressionStatement.expression
    """

    def __init__(self,
                 token: Token,
                 expression: Optional[Expression] = None) -> None:
        super().__init__(token)
        self.expression = expression

    def __str__(self) -> str:
        return str(self.expression)


class Integer(Expression):
    """
    Expresion for representing the integer types.

    param: token -> the token of the integer type
    param: value -> the value of the token declaration

    example: var x = 5;
    5 -> Token.TokenType == INTEGER, value = 5
    """

    def __init__(self,
                 token: Token,
                 value: Optional[int] = None) -> None:
        super().__init__(token)
        self.value = value

    def __str__(self) -> str:
        return str(self.value)


class Prefix(Expression):

    def __init__(self,
                 token: Token,
                 operator: str,
                 right: Optional[Expression] = None) -> None:
        super().__init__(token)
        self.operator = operator
        self.right = right

    def __str__(self) -> str:
        return f'({self.operator}{str(self.right)})'


class Infix(Expression):

    def __init__(self,
                 token: Token,
                 left: Expression,
                 operator: str,
                 right: Optional[Expression] = None):
        super().__init__(token)
        self.left = left
        self.operator = operator
        self.right = right

    def __str__(self) -> str:
        return f'({str(self.left)} {self.operator} {str(self.right)})'
