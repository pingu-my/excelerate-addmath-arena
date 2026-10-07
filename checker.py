"""Bounded arithmetic parser: no eval, imports, attributes or symbolic code."""
import ast
import math
import operator

OPS = {ast.Add: operator.add, ast.Sub: operator.sub, ast.Mult: operator.mul, ast.Div: operator.truediv}
FUNCS = {'sqrt': math.sqrt, 'sin': math.sin, 'cos': math.cos, 'tan': math.tan, 'ln': math.log, 'log': math.log10, 'exp': math.exp, 'abs': abs}
CONSTANTS = {'pi': math.pi, 'e': math.e}


def numeric(text):
    text = str(text).strip().replace('^', '**').replace('π', 'pi').replace('×', '*').replace('÷', '/')
    if not text or len(text) > 160:
        raise ValueError('Enter a short numeric answer.')
    try:
        root = ast.parse(text, mode='eval')
    except SyntaxError as exc:
        raise ValueError('Invalid numeric expression.') from exc
    if len(list(ast.walk(root))) > 70:
        raise ValueError('Expression is too long.')
    def visit(node):
        if isinstance(node, ast.Constant) and type(node.value) in (int, float):
            if abs(node.value) > 1e15:
                raise ValueError('Number is too large.')
            return float(node.value)
        if isinstance(node, ast.Name) and node.id in CONSTANTS:
            return CONSTANTS[node.id]
        if isinstance(node, ast.UnaryOp) and isinstance(node.op, (ast.USub, ast.UAdd)):
            value = visit(node.operand)
            return -value if isinstance(node.op, ast.USub) else value
        if isinstance(node, ast.BinOp):
            left, right = visit(node.left), visit(node.right)
            if isinstance(node.op, ast.Pow):
                if abs(right) > 20 or abs(left) > 1e8:
                    raise ValueError('Power is too large.')
                value = left ** right
            elif type(node.op) in OPS:
                value = OPS[type(node.op)](left, right)
            else:
                raise ValueError('Unsupported operation.')
            if not isinstance(value, (int, float)) or not math.isfinite(value) or abs(value) > 1e15:
                raise ValueError('Answer must be finite and real.')
            return value
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id in FUNCS and len(node.args) == 1 and not node.keywords:
            value = FUNCS[node.func.id](visit(node.args[0]))
            if not math.isfinite(value) or abs(value) > 1e15:
                raise ValueError('Answer is out of range.')
            return value
        raise ValueError('Use numbers, arithmetic, pi, e, or sqrt(...).')
    try:
        value = visit(root.body)
        if not math.isfinite(value):
            raise ValueError('Answer must be finite.')
        return value
    except (ArithmeticError, TypeError, OverflowError) as exc:
        raise ValueError('Check the arithmetic and denominator.') from exc


def check(responses, question):
    expected = question['answers']
    if len(responses) != len(expected):
        raise ValueError('Complete every answer field.')
    values = [numeric(v) for v in responses]
    if question.get('unordered'):
        values, expected = sorted(values), sorted(expected)
    tolerance = question.get('tolerance', 1e-7)
    return all(abs(a-b) <= tolerance for a,b in zip(values, expected))
