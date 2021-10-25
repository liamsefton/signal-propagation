"""
Made by: Liam Sefton
Fucking sick ass algorithm that propagates a signal recursively
"""
import concurrent.futures
import time

ldata = {"OR" : [.13, .15, .11, .16], "AND" : [.09, .1, .12, .125],
         "NAND" : [.1, .15, .14, .2], "XOR" : [.13, .12, .11, .10],
         "NOR" : [.07, .08, .1, .11], "XNOR" : [.15, .13, .09, .16]}

class Node:
    def __init__(self, inputs, input_layer, type):
        self.inputs = inputs #list of nodes
        self.input_layer = input_layer #boolean true if part of input layer
        self.type = type

    def getLeakage(self, x1, x2):
        return (((1-x1) * (1-x2)) * ldata[self.type][0]) + (((1-x1) * x2) * ldata[self.type][1]) + ((x1 * (1-x2)) * ldata[self.type][2]) + ((x1 * x2) * ldata[self.type][3])

class AND(Node):
    def __init__(self, inputs, input_layer):
        super().__init__(inputs, input_layer, "AND")

    def getOutput(self, x1, x2):
        return x1 * x2

class OR(Node):
    def __init__(self, inputs, input_layer):
        super().__init__(inputs, input_layer, "OR")

    def getOutput(self, x1, x2):
        return x1 * x2 + (1-x1) * x2 + x1 * (1-x2)

class XOR(Node):
    def __init__(self, inputs, input_layer):
        super().__init__(inputs, input_layer, "XOR")

    def getOutput(self, x1, x2):
        return (1-x1) * x2 + x1 * (1-x2)

"""
xor_1 = XOR([.6, .6], True)
xor_2 = XOR([.8, .6], True)
or_1 = OR([xor_1, xor_2], False)
and_1 = AND([xor_1, or_1], False)
and_2 = AND([or_1, xor_2], False)
xor_3 = XOR([and_1, and_2], False)
"""
"""
and_1 = AND([.5, .5], True)
and_2 = AND([.5, .5], True)
and_3 = AND([and_1, and_2], False)
"""
"""
and_1 = AND([.5, .5], True)
xor_1 = XOR([.5, .5], True)
and_2 = AND([.5, .5], True)
or_1 = OR([.5, .5], True)
and_3 = AND([.5, .5], True)
or_2 = OR([and_1, xor_1], False)
and_4 = AND([xor_1, and_2], False)
xor_2 = XOR([and_2, or_1], False)
and_5 = AND([or_1, and_3], False)
or_3 = OR([or_2, and_4], False)
and_6 = AND([and_4, xor_2], False)
xor_3 = XOR([xor_2, and_5], False)
and_7 = AND([or_3, and_6], False)
or_4 = OR([and_6, xor_3], False)
and_8 = AND([and_7, or_4], False)
"""

total_leakage = 0
visited = {}

def propagate(node):  #returns the output probability of the given node and stores total leakage in the total_leakage global variable
    global total_leakage
    global visited
    if node.input_layer:
        if node not in visited.keys():
            total_leakage += node.getLeakage(node.inputs[0], node.inputs[1])
            visited[node] = node.getOutput(node.inputs[0], node.inputs[1])
        return visited[node]
    else:
        #x1 = concurrent.futures.ThreadPoolExecutor().submit(propagate, node.inputs[0]).result() concurrency slows it down for small circuits
        x1 = propagate(node.inputs[0])
        #x2 = concurrent.futures.ThreadPoolExecutor().submit(propagate, node.inputs[1]).result()
        x2 = propagate(node.inputs[1])
        if node not in visited.keys():
            total_leakage += node.getLeakage(x1, x2)
            visited[node] = node.getOutput(x1, x2)
        return visited[node]

pre_time = time.time_ns()
for i in range(100):
    propagate() #put tail node inside parantheses after decommenting that circuit above
post_time = time.time_ns()
print(total_leakage)
delta_t = post_time - pre_time
print("Nanoseconds: " + str(delta_t))



