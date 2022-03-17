#!/usr/bin/python

import sys
sys.path.append('../../../pythonmain/install')
import Verific
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
    def __init__(self, lib_func, inputs, name):
        self.lib_func = lib_func
        self.inputs = inputs
        self.name = name
   
    def __str__(self):
        return "{" + self.lib_func + ", " + str(self.inputs) + ", " + self.name + "}"

library = parse_liberty(open("example.lib").read())
cell_groups = library.get_groups('cell')
function_dict = {}


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

cell_list = []
netlist = set_iter.First()

while netlist:
    if netlist.Owner().Name() == "top":
        instances_map = Verific.InstanceMapIter(netlist.GetInsts())
        instance = instances_map.First()
        while instance:
            print(" INSTANCE NAME: " + instance.Name() + " Cell Type: " + instance.View().Name())
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
                    except:
                        port_dict[port_ref.GetPort().Name()] = .5

                    print("        Input port: " + port_ref.GetPort().Name())
                else:
                    print("        Output Port: " + port_ref.GetPort().Name())

                port_ref = port_refs_map.Next()
            print(port_dict)
            cell_list.append(Cell("PLACEHOLDER", port_dict, instance.Name()))

            instance = instances_map.Next()


    netlist = set_iter.Next()

for cell in cell_list:
    print(cell)

sys.exit(0)
