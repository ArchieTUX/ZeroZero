import sys

# Token types
LET = 'LET'
FUN = 'FUN'
GIVE = 'GIVE'
SAY = 'SAY'
IF = 'IF'
ELSE = 'ELSE'
WHILE = 'WHILE'
IDENT = 'IDENT'
NUMBER = 'NUMBER'
STRING = 'STRING'
OP = 'OP'
NEWLINE = 'NEWLINE'
EOF = 'EOF'
INDENT = 'INDENT'
DEDENT = 'DEDENT'
COLON = 'COLON'
LPAREN = 'LPAREN'
RPAREN = 'RPAREN'

class Token:
    def __init__(self, type_, value=None):
        self.type = type_
        self.value = value

    def __repr__(self):
        return f'Token({self.type}, {repr(self.value)})'

# Simple Lexer
def tokenize(code):
    import re
    token_specification = [
        ('NUMBER',   r'\d+(\.\d*)?'),  
        ('STRING',   r'"[^"]*"'),  
        ('LET',      r'let\b'),
        ('FUN',      r'fun\b'),
        ('GIVE',     r'give\b'),
        ('SAY',      r'say\b'),
        ('IF',       r'if\b'),
        ('ELSE',     r'else\b'),
        ('WHILE',    r'while\b'),
        ('OP',       r'==|!=|>=|<=|>|<|\+|\-|\*|\/|%'),
        ('IDENT',    r'[A-Za-z_][A-Za-z0-9_]*'),
        ('COLON',    r':'),
        ('LPAREN',   r'\('),
        ('RPAREN',   r'\)'),
        ('NEWLINE',  r'\n'),
        ('SKIP',     r'[ \t]+'),
        ('MISMATCH', r'.'),
    ]
    tok_regex = '|'.join(f'(?P<{name}>{regex})' for name, regex in token_specification)
    get_token = re.compile(tok_regex).match
    pos = 0
    mo = get_token(code, pos)
    while mo:
        kind = mo.lastgroup
        value = mo.group()
        if kind == 'NUMBER':
            yield Token(NUMBER, float(value) if '.' in value else int(value))
        elif kind == 'STRING':
            yield Token(STRING, value[1:-1])
        elif kind in {'LET','FUN','GIVE','SAY','IF','ELSE','WHILE','COLON','LPAREN','RPAREN','OP'}:
            yield Token(kind, value)
        elif kind == 'IDENT':
            yield Token(IDENT, value)
        elif kind == 'NEWLINE':
            yield Token(NEWLINE)
        elif kind == 'SKIP':
            pass
        else:
            raise SyntaxError(f'Unexpected character {value}')
        pos = mo.end()
        mo = get_token(code, pos)
    yield Token(EOF)

# Basic AST Nodes
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

class FunDef:
    def __init__(self, name, params, body):
        self.name = name
        self.params = params
        self.body = body

class FunCall:
    def __init__(self, name, args):
        self.name = name
        self.args = args

class If:
    def __init__(self, cond, then_body, else_body=None):
        self.cond = cond
        self.then_body = then_body
        self.else_body = else_body

class While:
    def __init__(self, cond, body):
        self.cond = cond
        self.body = body

class Give:
    def __init__(self, expr):
        self.expr = expr

# Parser and Interpreter would be big, so this is a stub example:

def run_code():
    with open(sys.argv[1], 'r') as f:
        code = f.read()

    tokens = list(tokenize(code))
    # For now, just print tokens — extend parser & interpreter next
    for t in tokens:
        print(t)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python interpreter.py <file.zer0>")
        sys.exit(1)
    run_code()
