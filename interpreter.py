from lexer import Lexer
from parser import Parser
from runtime import Interpreter

def run(code: str):
    tokens = list(Lexer(code).tokenize())
    ast = Parser(tokens).parse()
    interpreter = Interpreter(ast)
    interpreter.eval()

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python interpreter.py <file>.zer0")
        sys.exit(1)

    filename = sys.argv[1]
    with open(filename, 'r') as f:
        source_code = f.read()

    try:
        run(source_code)
    except Exception as e:
        print(f"Runtime/Error: {e}")
