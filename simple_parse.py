#!/usr/bin/python

import sys
sys.path.append('../../../pythonmain/install')
import Verific
import networkx as nx
from liberty.parser import parse_liberty

#*******************************************************
#******** DATABASE EXAMPLE #1 ***************************
#*******************************************************
#
#               NOTE TO THE READER:
#
#  Here is an example on how to read a Synopsys Liberty file.
#
#*******************************************************/

def Accumulate(nl,done):
    if not nl:
        return
    if done.GetItem(nl):
        return
    inst_iter = Verific.InstanceMapIter(nl.GetInsts())
    inst = inst_iter.First()
    while inst:
        Accumulate(inst.View(),done)
        inst = inst_iter.Next()
    done.Insert(nl)

class Cell:
    def __init__(self, cell_type, inputs, name):
        self.cell_type = cell_type
        self.inputs = inputs
        self.name = name
        self.output = -1
    
    def update_inputs(self, cell_dict):
        for key in self.inputs.keys():
            if isinstance(self.inputs[key], float):
                pass
            else:
                self.inputs[key] = cell_dict[self.inputs[key]].output

    def calculate_output(self, lib_dict):
        func = lib_dict[self.cell_type][0]
        if "Q" in func:
            self.output = .5
        else:
            if func[1] == "&":
                self.output = self.inputs[func[0]] * self.inputs[func[2]]
            elif func[1] == "^":
                self.output = self.inputs[func[0]] - (2 * self.inputs[func[0]] * self.inputs[func[2]]) + self.inputs[func[2]]
            else:
                self.output = .5

    def get_leakage(self, lib_dict):
        ret = 0
        if "Q" in lib_dict[self.cell_type][0]:
            #count = 0
            #for key in lib_dict[self.cell_type][1].keys():
            #    ret += lib_dict[self.cell_type][1][key]
            #    count += 1
            #return ret / count
            return 20
        else:
            when_dict = lib_dict[self.cell_type][1]
            for when in when_dict:
                mult = 1
                when_split = when.strip("()").split("&")
                for chunk in when_split:
                    if chunk[0] == "!":
                        mult *= 1 - self.inputs[chunk[1]]
                    else:
                        mult *= self.inputs[chunk[0]]
                ret += mult * when_dict[when]
            return ret

    def __str__(self):
        return "{" + self.cell_type + ", " + str(self.inputs) + ", " + self.name + "}"


#CELL DICT: {CELL_NAME : (CELL_FUNCTION, {WHEN_VALUE : LEAKAGE VALUE})} 
library = parse_liberty(open("liberty_counter4.lib").read())
cell_groups = library.get_groups('cell')
lib_dict = {}
for cell_group in cell_groups:
    leakage_groups = cell_group.get_groups('leakage_power')
    leakage_dict = {}
    for leakage_group in leakage_groups:
        leakage_dict[str(leakage_group.get("when")).strip("\"")] = float(leakage_group.get("value"))
    pin_groups = cell_group.get_groups('pin')
    function = "ERROR: FUNCTION NOT FOUND"
    for pin_group in pin_groups:
        if pin_group.get('function') != None:
            function = str(pin_group.get('function')).strip("\"")
    lib_dict[str(cell_group.args[0])] = (function, leakage_dict)

print(lib_dict)


synlib_reader = Verific.synlib_file()
#synlib_reader.Read("example.lib","work")
#synlib_reader.Read("example_modified.lib", "work")
synlib_reader.Read("liberty_counter4.lib", "work")
#synlib_reader.Analyze("liberty_counter.lib")
#synlib_reader.Analyze("example.lib")

nl_reader = Verific.veri_nl_file()
nl_reader.Read("netlist_counter.v","work")
#nl_reader.Read("test.v", "work")
#nl_reader.Read("test_modified2.v", "work")

top = Verific.Netlist_PresentDesign()
#top.SaveToFile("cool.txt")
#top = Verific.Netlist_PresentDesign()
print ("INFO: top level design is %s(%s)" % (top.Owner().Name(), top.Name()))

set = Verific.Set()
Accumulate(top,set)

set_iter = Verific.NetlistSetIter(set)

cell_dict = {}
connections_list = []
netlist = set_iter.First()

while netlist:
    if netlist.Owner().Name() == "top":
        instances_map = Verific.InstanceMapIter(netlist.GetInsts())
        instance = instances_map.First()
        while instance:
            print(" INSTANCE NAME: " + instance.Name() + " Cell Type: " + instance.View().Owner().Name())
            atts_map = Verific.AttMapIter(instance.View().GetAtts())
            att = atts_map.First()
            while att:
                print("ATT KEY: " + str(att.Key()) + " ----> " + str(att.Value()))
                att = atts_map.Next()
            port_refs_map = Verific.PortRefMapIter(instance.GetPortrefs())
            port_ref = port_refs_map.First()
            port_dict = {}
            while port_ref:
                if port_ref.GetPort().IsInput():
                    try:
                        port_dict[port_ref.GetPort().Name()] = port_ref.GetNet().Driver().Name()
                        if "Q" in lib_dict[port_ref.GetNet().Driver().View().Owner().Name()][0]:
                            port_dict[port_ref.GetPort().Name()] = .5
                        if "Q" not in lib_dict[instance.View().Owner().Name()][0]:
                        	connections_list.append((port_ref.GetNet().Driver().Name(), instance.Name()))
                    except:
                        port_dict[port_ref.GetPort().Name()] = .5

                    print("        Input port: " + port_ref.GetPort().Name())
                else:
                    print("        Output Port: " + port_ref.GetPort().Name())

                port_ref = port_refs_map.Next()
            print(port_dict)
            cell_dict[instance.Name()] = Cell(str(instance.View().Owner().Name()), port_dict, instance.Name())

            instance = instances_map.Next()


    netlist = set_iter.Next()
print("********CONNECTIONS LIST***********")
print(connections_list)


print("********CELL DICT************")
for key in cell_dict.keys():
    print("KEY: " + key + " -> VALUE: " + str(cell_dict[key]) + " and has function " + lib_dict[cell_dict[key].cell_type][0])

design_dag = nx.DiGraph(connections_list)

result_list = list(nx.topological_sort(design_dag))

print("**********WHEN VALUES*********")
for cell in lib_dict.keys():
    print("CELL TYPE: " + cell)
    for when in lib_dict[cell][1].keys():
        print("    " + when)

print("**********TOPOLOGICALLY SORTED DAG************")
print(result_list)

print("**************PROPAGATION****************")
total_leakage = 0
for cell_name in result_list:
    cell = cell_dict[cell_name]
    cell.update_inputs(cell_dict)
    cell.calculate_output(lib_dict)
    print(cell_name + " HAS OUTPUT " + str(cell.output))
    cell_leakage = cell.get_leakage(lib_dict)
    print(cell_name + " HAS LEAKAGE " + str(cell_leakage))
    total_leakage += cell_leakage

print("TOTAL LEAKGE = " + str(total_leakage))

sys.exit(0)
