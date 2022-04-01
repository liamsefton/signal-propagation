"""
Basic calculator
================
A simple example of a REPL calculator
This example shows how to write a basic calculator with variables.
"""
from lark import Lark, Transformer, v_args


try:
    input = raw_input   # For Python2 compatibility
except NameError:
    pass


calc_grammar = """
    ?start: operator

    ?operator: pin
        | operator "|" pin   -> prob_or
        | operator "^" pin   -> prob_xor
        | operator "&" pin   -> prob_and
    ?pin: LETTER   
         | "!" pin         -> prob_not
         | "(" operator ")"
    %import common.CNAME -> NAME
    %import common.LETTER
    %import common.WS_INLINE
    %ignore WS_INLINE
"""


@v_args(inline=True)    # Affects the signatures of the methods
class CalculateTree(Transformer):
    from operator import add, sub, mul, truediv as div, neg
    #from numpy import np.logical_xor, np.logical_or, np.logical_and
    number = float

    def __init__(self, pin_dict):
        self.pin_dict = pin_dict
        self.vars = {}

    def assign_var(self, name):
        self.vars[name] = self.pin_dict[name]
        return self.pin_dict[name]

    def prob_xor(self, a, b):
        if type(a) != float:
            a = self.pin_dict[a]
        if type(b) != float:
            b = self.pin_dict[b]
        return a - 2*a*b + b

    def prob_and(self, a, b):
        if type(a) != float:
            a = self.pin_dict[a]
        if type(b) != float:
            b = self.pin_dict[b]
        return a * b

    def prob_or(self, a, b):
        if type(a) != float:
            a = self.pin_dict[a]
        if type(b) != float:
            b = self.pin_dict[b]
        return a + b - a*b

    def prob_not(self, a):
        if type(a) != float:
            a = self.pin_dict[a]
        return 1 - a

    def var(self, a):
        try:
            return self.pin_dict[a]
        except KeyError:
            raise Exception("Variable not found: %s" % a)

pd = {'A' : .5, 'B' : .5, 'C' : .5, 'D': .5, 'E' : .5}
calc_parser = Lark(calc_grammar, parser='lalr', transformer=CalculateTree(pd))
calc = calc_parser.parse


def main():
    while True:
        try:
            s = input('> ')
        except EOFError:
            break
        print(calc(s))


def test():
    print(calc("!(A&B|C^!(D&!E))"))


if __name__ == '__main__':
    test()
    