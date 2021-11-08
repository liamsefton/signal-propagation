import math
#function extractor for OpenROAD project liberty files, follows algebraic evaluation but that is probably wrong
function = "(!A * !B) + (CI * A)"

input_probabilities = {"A" : .6, "B" : .8, "CI" : .5}

def get_output(func, inputs):
    func = func.split(" + ")
    output = 0
    invert = False
    summation_list = []
    for group in func:
        product_list = []
        variables = group.split(" * ")
        for var in variables:
            var = var.strip("()")
            if var[0] == "!":
                product_list.append(1-inputs[var[1:]])
            else:
                product_list.append(inputs[var])
        product = 1
        for num in product_list:
            product = product * num
        summation_list.append(product)
    if sum(summation_list) > 1:
        return 1
    return sum(summation_list)

print(get_output(function, input_probabilities))



