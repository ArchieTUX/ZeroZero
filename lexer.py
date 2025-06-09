import re
from collections import namedtuple

Token = namedtuple('Token', ['type', 'value'])

class Lexer:
    def __init__(self, code):
        self.code = code
        self.pos = 0
        self.tokens = []
        self.token_specification = [
            ('NUMBER',   r'\d+(\.\d+)?'),
            ('STRING',   r'"[^"]*"'),
            ('LET',      r'\blet\b'),
            ('FUN',      r'\bfun\b'),
            ('GIVE',     r'\bgive\b'),
            ('SAY',      r'\bsay\b'),
            ('IF',       r'\bif\b'),
            ('ELSE',     r'\belse\b'),
            ('WHILE',    r'\bwhile\b'),
            ('IDENT',    r'[A-Za-z_][A-Za-z0-9_]*'),
            ('OP',       r'==|!=|>=|<=|>|<|\+|\-|\*|\/|%'),
            ('COLON',    r':'),
            ('LPAREN',   r'\('),
            ('RPAREN',   r'\)'),
            ('NEWLINE',  r'\n'),
            ('SKIP',     r'[ \t]+'),
            ('MISMATCH', r'.'),
        ]
        self.token_regex = re.compile('|'.join(f'(?P<{name}>{pattern})' for name, pattern in self.token_specification))

    def tokenize(self):
        for mo in self.token_regex.finditer(self.code):
            kind = mo.lastgroup
            value = mo.group()
            if kind == 'NUMBER':
                if '.' in value:
                    value = float(value)
                else:
                    value = int(value)
                yield Token(kind, value)
            elif kind == 'STRING':
                yield Token(kind, value[1:-1])  # strip quotes
            elif kind == 'SKIP' or kind == 'NEWLINE':
                continue
            elif kind == 'MISMATCH':
                raise SyntaxError(f'Unexpected character: {value}')
            else:
                yield Token(kind, value)
