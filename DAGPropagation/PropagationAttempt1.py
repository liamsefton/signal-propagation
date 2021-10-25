"""
This program is designed to propagate a signal through a circuit by treating the gate-level netlist as a directed acyclic graph. 
Parallelization will be used to improve this process on large scale designs.
Author: Liam Sefton
Created for: Qualcomm senior project
Date: 10/24/2021
"""

#Dummy data structures defined here

#Liberty data
ldata = {"OR" : [.13, .15, .11, .16], "AND" : [.09, .1, .12, .125],
         "NAND" : [.1, .15, .14, .2], "XOR" : [.13, .12, .11, .10],
         "NOR" : [.07, .08, .1, .11], "XNOR" : [.15, .13, .09, .16]}

#DAG from verilog parser data below

#Logic cells
circuit_vertices = ["OR_1", "AND_1", "NAND_1", "AND_2", "OR_2", "AND_3", "AND_4", "XOR_1"]

#Inputs to the circuit
circuit_inputs = {"x1" : "OR_2", "x2" : "OR_1", "x3" : "OR_1",
                 "x4" : "AND_1", "x5" : "AND_1", "x6" : "AND_2",
                 "x7" : "AND_3"}

#Connections between cells, maps cell to list of its outputs
circuit_edges = {"OR_1" : ["NAND_1"], "AND_1" : ["NAND_1"],
                 "NAND_1" : ["OR_2", "AND_2"], "OR_2" : ["AND_4"],
                 "AND_2" : ["AND_4", "AND_3"], "AND_4" : ["XOR_1"],
                 "AND_3" : ["XOR_1"]}

#Outputs on the circuit
circuit_outputs = {"XOR_1" : "y1"}


