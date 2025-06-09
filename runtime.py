class RuntimeError(Exception):
    pass

class Environment:
    def __init__(self):
        self.vars = {}

    def set_var(self, name, value):
        self.vars[name] = value

    def get_var(self, name):
        if name in self.vars:
            return self.vars[name]
        raise RuntimeError(f"Variable '{name}' not defined")

class Interpreter:
    def __init__(self, ast):
        self.ast = ast
        self.env = Environment()

    def eval(self):
        for node in self.ast:
            self.execute(node)

    def execute(self, node):
        cls = node.__class__.__name__

        if cls == 'Assign':
            val = self.eval_expr(node.expr)
            self.env.set_var(node.name, val)

        elif cls == 'Say':
            val = self.eval_expr(node.expr)
            print(val)

        else:
            raise RuntimeError(f'Unknown AST node: {cls}')

    def eval_expr(self, expr):
        cls = expr.__class__.__name__

        if cls == 'Number':
            return expr.value

        elif cls == 'String':
            return expr.value

        elif cls == 'Var':
            return self.env.get_var(expr.name)

        else:
            raise RuntimeError(f'Unknown expression: {cls}')
