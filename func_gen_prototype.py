
   
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
    ?start: or
    ?or: and
        | or "|" and -> str_or2
    ?and: xor
        | and "&" xor -> str_and2
    ?xor: pin
        | xor "^" pin -> str_xor2
    ?pin: NAME -> var
         | "!" pin         -> str_not
         | "(" or ")"
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

    def str_xor2(self, a, b):
        return "prob_xor(" + a + ", " + b + ")"

    def str_and2(self, a, b):
        return "prob_and(" + a + ", " + b + ")"

    def str_or2(self, a, b):
        return "prob_or(" + a + ", " + b + ")"

    def str_not(self, a):
        return "(1 - " + a + ")"

    def var(self, a):
        return "pin_dict[\"" + a + "\"]"

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
    cell_dict = {"cell_one" : "A|!B|C|!(D|E)"}
    import time
    t = time.time() * 1000
    cell_dict = {"cell_one" : "A&!B^!(C|!D)&!E^F^G|!H", "cell_two" : "A&B&C&D&E&F&G&H", "cell_three" : "!A^!B^!C^!D^!E^!F^!G^!H"}
    f = open("output_func.py", "w")
    f.write("func_dict = {}\n")

    f.write("def prob_or(a, b):\n")
    f.write("    return a + b - a * b\n\n")

    f.write("def prob_and(a, b):\n")
    f.write("    return a * b\n\n")

    f.write("def prob_xor(a, b):\n")
    f.write("    return a - 2 * a * b + b \n\n")

    for key in cell_dict.keys():
        f.write("def output_" + key + "(pin_dict):\n")
        f.write("    return " + calc(cell_dict[key]) + "\n\n")
        f.write("func_dict[\"" + key + "\"] = " + "output_" + key + "\n\n")
    f.close()
    from output_func import func_dict
    for key in cell_dict.keys():
        print(func_dict[key]({'A' : .5, 'B' : .5, 'C' : .5, 'D': .5, 'E' : .5, 'F' : .5, 'G' : .5, 'H' : .5}))

    print("RUNTIME: " + str((time.time() * 1000) - t))


if __name__ == '__main__':
    test()
    A = .5
    B = .5
    C = .5
    D = .5
    E = .5
