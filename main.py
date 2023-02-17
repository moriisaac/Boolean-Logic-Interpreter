class BooleanInterpreter:
    def __init__(self):
        self.variables = {}

    def eval(self, expression):
        tokens = self.tokenize(expression)
        ast = self.parse(tokens)
        return self.evaluate(ast)

    def tokenize(self, expression):
        tokens = []
        i = 0
        while i < len(expression):
            if expression[i] in ['T', 'F']:
                tokens.append(('value', expression[i]))
                i += 1
            elif expression[i].isalpha():
                j = i
                while j < len(expression) and expression[j].isalpha():
                    j += 1
                variable = expression[i:j]
                tokens.append(('variable', variable))
                i = j
            elif expression[i] in ['^', 'v', '(', ')']:
                tokens.append(('operator', expression[i]))
                i += 1
            else:
                raise ValueError('Invalid character: {}'.format(expression[i]))
        return tokens

    def parse(self, tokens):
        i = 0
        ast = self.parse_expression(tokens, i)
        if i != len(tokens):
            raise ValueError('Invalid syntax')
        return ast

    def parse_expression(self, tokens, i):
        left = self.parse_term(tokens, i)
        while i < len(tokens) and tokens[i][1] in ['^', 'v']:
            operator = tokens[i][1]
            i += 1
            right = self.parse_term(tokens, i)
            left = ('binop', operator, left, right)
        return left

    def parse_term(self, tokens, i):
        if tokens[i][1] == '(':
            i += 1
            ast = self.parse_expression(tokens, i)
            if tokens[i][1] != ')':
                raise ValueError('Missing closing parenthesis')
            i += 1
        elif tokens[i][0] == 'value':
            ast = ('value', tokens[i][1])
            i += 1
        elif tokens[i][0] == 'variable':
            ast = ('variable', tokens[i][1])
            i += 1
        else:
            raise ValueError('Invalid term')
        return ast

    def evaluate(self, ast):
        if ast[0] == 'value':
            return ast[1] == 'T'
        elif ast[0] == 'variable':
            return self.variables.get(ast[1], False)
        elif ast[0] == 'binop':
            left = self.evaluate(ast[2])
            right = self.evaluate(ast[3])
            if ast[1] == '^':
                return left and right
            elif ast[1] == 'v':
                return left or right
            else:
                raise ValueError('Invalid operator')

    def let(self, variable, value):
        self.variables[variable] = value
