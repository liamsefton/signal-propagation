from liberty.types import EscapedString
import networkx as nx
from liberty.parser import parse_liberty
import sys

#Cell class used for propagating the probabilities through a liberty function
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

    def updateInputs(self, cell_name_dict):
        for key in self.inputs.keys():
            if(type(self.inputs[key]) == str):
                self.inputs[key] = cell_name_dict[self.inputs[key]].getOutput()


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

#******Circuit Instantiation******
library = parse_liberty(open("liberty.lib").read())
cell_groups = library.get_groups('cell')
leakage_groups = cell_groups[0].get_groups('leakage_power')
when_functions = []
for group in leakage_groups:
    when_functions.append({str(group.get("when")).strip("\"") : float(group.get("value"))})

pin_groups = cell_groups[0].get_groups('pin')
XOR1_lib_func = ""
for thing in pin_groups:
    if str(thing.get('function')) != None:
        XOR1_lib_func  = str(thing.get('function')).strip("\"")

class Gate:
    def __init__(self, n, o, i1, i2):
        self.name = n
        self.output = o
        self.inputs = [i1, i2]
    def __str__(self):
        return self.name

def parseBlock(gate): # parse gate block
    gate = gate.split("\n")
    name = gate[0].split()[0][:-1]
    z = [name]
    for g in gate[1:]: #skip name
        if "Identifier:" in g:
            z.append(g.split()[1])
    return Gate(z[0], z[1], z[2], z[3])

def initialize(file): # create array of gate objects, dictionary of gate name to gate object
    inputs = []
    gates = []
    gates_dict = {}
    with open(file) as f:
        line = f.readline()
        while "Input:" not in line:
            line = f.readline()
        while "Input:" in line:
            inputs.append(line.split()[1][:-1])
            line = f.readline()
        while "Instance:" not in line:
            line = f.readline()
        blocks = line + f.read()
        blocks = blocks.split("Instance: ")[1:] # weird spacing in front
        for gate in blocks: 
            gates.append(parseBlock(gate))

            curr = gates[-1]
            input_probability = 0.5
            inDict = {}
            a = curr.inputs[0]
            b = curr.inputs[1]
            inDict["A"] = input_probability if a in inputs else getGate(a, gates)
            inDict["B"] = input_probability if b in inputs else getGate(b, gates)
            gates_dict[curr.name] = Cell(XOR1_lib_func, inDict, curr.name)

    return gates, gates_dict

def getGate(x, gates):
    for g in gates:
        if x == g.output:
            return g.name

def createConnections(gates): # function name
    total = []
    for g in gates:
        for ga in gates:
            i1 = g.inputs[0]
            i2 = g.inputs[1]
            o = ga.output
            if i1 == o or i2 == o:
                total.append((ga.name, g.name))
    return total

gates, cell_name_dict = initialize("netlistStruct.txt")
connections_list = createConnections(gates)
#******End of Circuit Instantiation*******



#Putting it all together
module_dag = nx.DiGraph(connections_list)

result_list = list(nx.topological_sort(module_dag))

total_leakage = 0

for cell in result_list:
    cell = cell_name_dict[cell]
    cell.updateInputs(cell_name_dict) #updates the inputs dictionary for any cells that have other cells as their inputs
    cell.calculateOutput() #calculates the output of the current cell for future cells to use
    total_leakage += cell.getLeakageWeightedAverage(when_functions) #gets the leakage for 1 cell



print(total_leakage)

