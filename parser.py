from lexer import Lexer, Token

class ParseError(Exception):
    pass

# AST Nodes
class Number:
    def __init__(self, value):
        self.value = value

class String:
    def __init__(self, value):
        self.value = value

class Var:
    def __init__(self, name):
        self.name = name

class BinOp:
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

class Assign:
    def __init__(self, name, expr):
        self.name = name
        self.expr = expr

class Say:
    def __init__(self, expr):
        self.expr = expr

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def current(self):
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return Token('EOF', None)

    def eat(self, type_):
        token = self.current()
        if token.type == type_:
            self.pos += 1
            return token
        raise ParseError(f'Expected {type_} but got {token.type}')

    def parse(self):
        statements = []
        while self.current().type != 'EOF':
            stmt = self.statement()
            statements.append(stmt)
        return statements

    def statement(self):
        token = self.current()
        if token.type == 'LET':
            return self.assignment()
        elif token.type == 'SAY':
            return self.say_statement()
        else:
            raise ParseError(f'Unknown statement starting with {token.type}')

    def assignment(self):
        self.eat('LET')
        var_name = self.eat('IDENT').value
        self.eat('OP')  # Expect '=' operator
        expr = self.expression()
        return Assign(var_name, expr)

    def say_statement(self):
        self.eat('SAY')
        expr = self.expression()
        return Say(expr)

    def expression(self):
        # Only simple for now: number, string, or var
        token = self.current()
        if token.type == 'NUMBER':
            self.eat('NUMBER')
            return Number(token.value)
        elif token.type == 'STRING':
            self.eat('STRING')
            return String(token.value)
        elif token.type == 'IDENT':
            self.eat('IDENT')
            return Var(token.value)
        else:
            raise ParseError(f'Unexpected token in expression: {token.type}')
