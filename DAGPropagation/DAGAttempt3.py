"""
Made by: Liam Sefton
Fucking sick ass algorithm that propagates a signal recursively
"""
import concurrent.futures
import time
import sys
import os
#import resource ONLY WORKS ON LINUX

sys.setrecursionlimit(100000)
#resource.setrlimit(resource.RLIMIT_STACK, [0x10000000, resource.RLIM_INFINITY]) ONLY WORKS ON LINUX


ldata = {"OR" : [.13, .15, .11, .16], "AND" : [.09, .1, .12, .125],
         "NAND" : [.1, .15, .14, .2], "XOR" : [.13, .12, .11, .10],
         "NOR" : [.07, .08, .1, .11], "XNOR" : [.15, .13, .09, .16]}

class Node:
    def __init__(self, inputs, type):
        self.inputs = inputs #list of nodes
        self.type = type

    def getLeakage(self, x1, x2):
        return (((1-x1) * (1-x2)) * ldata[self.type][0]) + (((1-x1) * x2) * ldata[self.type][1]) + ((x1 * (1-x2)) * ldata[self.type][2]) + ((x1 * x2) * ldata[self.type][3])

class AND(Node):
    def __init__(self, inputs):
        super().__init__(inputs, "AND")

    def getOutput(self, x1, x2):
        return x1 * x2

class OR(Node):
    def __init__(self, inputs):
        super().__init__(inputs, "OR")

    def getOutput(self, x1, x2):
        return x1 * x2 + (1-x1) * x2 + x1 * (1-x2)

class XOR(Node):
    def __init__(self, inputs):
        super().__init__(inputs, "XOR")

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

and_1 = AND([.5, .5])
xor_1 = XOR([.5, .5])
and_2 = AND([.5, .5])
or_1 = OR([.5, .5])
and_3 = AND([.5, .5])
or_2 = OR([and_1, xor_1])
and_4 = AND([xor_1, and_2])
xor_2 = XOR([and_2, or_1])
and_5 = AND([or_1, and_3])
or_3 = OR([or_2, and_4])
and_6 = AND([and_4, xor_2])
xor_3 = XOR([xor_2, and_5])
and_7 = AND([or_3, and_6])
or_4 = OR([and_6, xor_3])
and_8 = AND([and_7, or_4])


#design = [XOR([.5, .5]), XOR([.5, .5]), XOR([.5, .5]), XOR([.5, .5]), XOR([.5, .5]), XOR([.5, .5]), XOR([.5, .5]), XOR([.5, .5]), XOR([.5, .5]), XOR([.5, .5])]
design = [XOR([.5, .5]), XOR([.5, .5])]

#for i in range(10, 39270, 10):
for i in range(2, 7854, 2):
    #design.append(XOR([design[i-20], design[i-19], design[i-18], design[i-17], design[i-16], design[i-15], design[i-14], design[i-13], design[i-12], design[i-11], design[i-10],
    #design[i-9], design[i-8], design[i-7], design[i-6], design[i-5], design[i-4], design[i-3], design[i-2], design[i-1]]))
    """
    design.append(XOR([design[i-10], design[i-9]]))
    design.append(XOR([design[i-9], design[i-8]]))
    design.append(XOR([design[i-8], design[i-7]]))
    design.append(XOR([design[i-7], design[i-6]]))
    design.append(XOR([design[i-6], design[i-5]]))
    design.append(XOR([design[i-5], design[i-4]]))
    design.append(XOR([design[i-4], design[i-3]]))
    design.append(XOR([design[i-3], design[i-2]]))
    design.append(XOR([design[i-2], design[i-1]]))
    design.append(XOR([design[i-2], design[i-1]]))
    """

    design.append(XOR([design[i-2], design[i-1]]))
    design.append(XOR([design[i-2], design[i-1]]))




total_leakage = 0

visited = {}

def propagate(node):  #returns the output probability of the given node and stores total leakage in the total_leakage global variable
    global total_leakage
    global visited
    if isinstance(node.inputs[0], float):
        x1 = node.inputs[0]
    elif visited.get(node.inputs[0]) == None:
        #x1 = concurrent.futures.ThreadPoolExecutor().submit(propagate, node.inputs[0]).result()
        x1 = propagate(node.inputs[0])
    else:
        x1 = visited[node.inputs[0]]

    if isinstance(node.inputs[1], float):
        x2 = node.inputs[1]
    elif visited.get(node.inputs[1]) == None:
        x2 = propagate(node.inputs[1])
        #x2 = concurrent.futures.ThreadPoolExecutor().submit(propagate, node.inputs[1]).result()
    else:
        x2 = visited[node.inputs[1]]

    if visited.get(node) == None:
        total_leakage += node.getLeakage(x1, x2)
        visited[node] = node.getOutput(x1, x2)

    return visited[node]

pre_time = time.time_ns()
for i in range(1):
    total_leakage = 0
    visited = {}
    for i in range(10):
        propagate(design[len(design) - 1 - i])
post_time = time.time_ns()
print(total_leakage)
delta_t = post_time - pre_time
print("Milliseconds: " + str(delta_t / 1000000))



