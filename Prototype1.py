import networkx as nx

class Cell:
    def __init__(self, liberty_function, inputs, name):
        self.lib_func = liberty_function
        self.inputs = inputs
        self.name = name
        self.output = -1
    
    def __str__(self):
        return self.name

    def getOutput(self):
        return self.output

    def updateInputs(self):
        for key in self.inputs.keys():
            if(type(self.inputs[key]) == Cell):
                self.inputs[key] = self.inputs[key].getOutput()


    def addOneBinary(self, b_list):
        carry = False
        for i in range(len(b_list)):
            if carry:
                if b_list[len(b_list) - 1 - i] == 0:
                    b_list[len(b_list) - 1 - i] = 1
                    carry = False
                    break
                else:
                    b_list[len(b_list) - 1 - i] = 0
            else:
                if b_list[len(b_list) - 1 - i] == 1:
                    carry = True
                    b_list[len(b_list) - 1 - i] = 0
                else:
                    b_list[len(b_list) - 1 - i] = 1
                    break

    def getBinaryOutput(self, binary, binary_index_dict):
        products = self.lib_func.split(" + ")
        sums = []
        i = 0
        for product in products:
            numbers = product.split(" * ")
            mult = 1
            for num in numbers:
                num = num.strip("()")
                if num[0] == "!":
                    mult = mult * (1 - binary[binary_index_dict[num[1]]])
                else:
                    mult = mult * binary[binary_index_dict[num[0]]]
                i += 1
            sums.append(mult)

        finalSum = sum(sums)
        if finalSum >= 1:
            return 1

        return 0

    def calculateOutput(self):
        numInputs = len(list(self.inputs.keys()))
        binary = []
        for i in range(numInputs):
            binary.append(0)

        binary_index_dict = {}
        reverse_index_dict = {}
        i = 0

        for key in self.inputs.keys():
            binary_index_dict[key] = i
            reverse_index_dict[i] = key
            i += 1

        i = 0
        binary_vectors = []
        for i in range(2**len(binary)):
            if self.getBinaryOutput(binary, binary_index_dict) == 1:
                binary_vectors.append(binary[:])
            self.addOneBinary(binary)

        prods = []
        for binary_vector in binary_vectors:
            mult = 1
            for i in range(len(binary_vector)):
                if binary_vector[i] == 0:
                    mult = mult * (1 - self.inputs[reverse_index_dict[i]])
                else:
                    mult = mult * self.inputs[reverse_index_dict[i]]
            prods.append(mult)
        self.output = sum(prods)

    def getLeakageWeightedAverage(self, when_funcs):
        input_probabilities = self.inputs
        weighted_average = 0
        for outer_loop in range(len(when_funcs)):
            func_key = str(list(when_funcs[outer_loop].keys())[0])
            func_split = func_key.split(" * ")
            i = 0
            prod = 1
            for input_pin in func_split:
                input_pin = input_pin.strip("()")
                if input_pin[0] == "!":
                    prod *= (1-input_probabilities[input_pin[1:]])
                else:
                    prod *= input_probabilities[input_pin]
                i += 1
            weighted_average += prod * when_funcs[outer_loop][func_key]
        return weighted_average  



#******DUMMY CIRCUIT DESIGN******
XOR1_lib_func = "(A * !B) + (!A * B)"

input_probabilities = {"A" : .5, "B" : .5}
XOR1_1 = Cell(XOR1_lib_func, input_probabilities, "XOR1_1")
XOR1_2 = Cell(XOR1_lib_func, input_probabilities, "XOR1_2")
XOR1_3 = Cell(XOR1_lib_func, {"A" : XOR1_1, "B" : XOR1_2}, "XOR1_3")
XOR1_4 = Cell(XOR1_lib_func, {"A" : XOR1_1, "B" : XOR1_2}, "XOR1_4")
XOR1_5 = Cell(XOR1_lib_func, {"A" : XOR1_2, "B" : XOR1_4}, "XOR1_5")
XOR1_6 = Cell(XOR1_lib_func, {"A" : XOR1_3, "B" : XOR1_5}, "XOR1_6")
XOR1_7 = Cell(XOR1_lib_func, {"A" : XOR1_3, "B" : XOR1_5}, "XOR1_7")
XOR1_8 = Cell(XOR1_lib_func, {"A" : XOR1_6, "B" : XOR1_7}, "XOR1_8")

connections_list = [(XOR1_1, XOR1_3), (XOR1_1, XOR1_4), (XOR1_2, XOR1_3), (XOR1_2, XOR1_4), (XOR1_2, XOR1_5),
                    (XOR1_3, XOR1_6), (XOR1_3, XOR1_7), (XOR1_4, XOR1_5), (XOR1_5, XOR1_6), (XOR1_5, XOR1_7),
                    (XOR1_6, XOR1_8), (XOR1_7, XOR1_8)]

when_func1 = {"(A * B)" : 10}
when_func2 = {"(A * !B)" : 5}
when_func3 = {"(!A * B)" : 15}
when_func4 = {"(!A * !B)" : 20}

when_functions = [when_func1, when_func2, when_func3, when_func4]
#******END OF DUMMY CIRCUIT DESIGN*******

module_dag = nx.DiGraph(connections_list)

result_list = list(nx.topological_sort(module_dag))

input_probabilities = {"A" : .5, "B" : .5}

total_leakage = 0

for cell in result_list:
    cell.updateInputs() #updates the inputs dictionary for any cells that have other cells as their inputs
    cell.calculateOutput() #calculates the output of the current cell for future cells to use
    total_leakage += cell.getLeakageWeightedAverage(when_functions) #gets the leakage for 1 cell

print(total_leakage)

