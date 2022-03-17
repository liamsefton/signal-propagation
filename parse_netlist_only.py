#!/usr/bin/python

import sys
sys.path.append('../../../pythonmain/install')
import Verific

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


synlib_reader = Verific.synlib_file()
synlib_reader.Read("example.lib","work")
#synlib_reader.Read("liberty_counter.lib", "work")
#synlib_reader.Analyze("liberty_counter.lib")
#synlib_reader.Analyze("example.lib")

nl_reader = Verific.veri_nl_file()
nl_reader.Read("netlist_counter.v","work")
#nl_reader.Read("netlist_counter.v", "work")

top = Verific.Netlist_PresentDesign()
#top.SaveToFile("cool.txt")
#top = Verific.Netlist_PresentDesign()
print ("INFO: top level design is %s(%s)" % (top.Owner().Name(), top.Name()))

set = Verific.Set()
Accumulate(top,set)

set_iter = Verific.NetlistSetIter(set)
#lib_iter = Verific.SynlibLibraryMapIter(synlib_reader.GetLibraries())

#lib = lib_iter.First()
#while lib:
#    print("Liberty name: " + lib.GetLibrary().Name())

lib = synlib_reader.GetLibrary("XORdesign")
#lib = synlib_reader.GetLibrary("typical")
if not lib:
    print("gooooooooooooooooooooooooooood")
else:
    print("Class Type: " + str(type(lib.GetLibrary())))
#    atts_map = Verific.AttMapIter(lib.GetAtts())
#    att = atts_map.First()
#    while att:
#        print("LIBRARY ATT NAME: " + att.Key())



netlist = set_iter.First()
while netlist:
    print("Netlist name: " + netlist.Name() + " Is combinational: " + str(netlist.IsCombinational()))
    """
    print("INFO: netlist %s was instantiated %d times" % (netlist.Owner().Name(),netlist.NumOfRefs()))
    print("Ports: ")
    ports_map = Verific.PortMapIter(netlist.GetPorts())
    port = ports_map.First()
    print("********" + netlist.Owner().Name())
    cells_map = Verific.PortMapIter(netlist.Owner().Owner().GetCells())
    cell = cells_map.First()
    while cell:
        print("CELL NAME: " + cell.Name() + " NUM OF ATTS: " + str(cell.NumOfAtts()))
        cell = cells_map.Next()
    print("LIBRARY NAME: " + netlist.Owner().Owner().Name() +  " CELL NUM OF ATTS: " + str(netlist.Owner().Owner().GetCell("NAND2X4").NumOfAtts()))
    print("CELL TEST NAME: " + netlist.Owner().Owner().GetCell("counter").Name())
    print("*************LIBRARY ATTRIBUTEs*************")
    atts_map = Verific.AttMapIter(netlist.Owner().Owner().GetAtts())
    att = atts_map.First()
    while att:
        print("Attribute name: " + att.Key() + " -------> " + att.Value())
        att = atts_map.Next()
    while port:
        print(port.Name())
        port = ports_map.Next()
    print("Nets: ")
    nets_map = Verific.NetMapIter(netlist.GetNets())
    net = nets_map.First()
    while net:
        print(net.Name())
        net = nets_map.Next()
    """
    print("Instances: ")
    instances_map = Verific.InstanceMapIter(netlist.GetInsts())
    instance = instances_map.First()
    while instance:
        print("INSTANCE NAME: " + instance.Name() + " IS COMBINATIONAL: " + str(instance.IsCombinational()))
        print("    Port References:")
        port_refs_map = Verific.PortRefMapIter(instance.GetPortrefs())
        port_ref = port_refs_map.First()
        while port_ref:
            print("    " + port_ref.GetPort().Name() + " : " + port_ref.GetNet().Name())
            port_ref = port_refs_map.Next()

        atts_map = Verific.AttMapIter(instance.GetAtts())
        att = atts_map.First()
        while att:
            print("ATTRIBUTE NAME: " + att.Key() + " -------> " + att.Value())
            att = atts_map.Next()
        instance = instances_map.Next()

    netlist = set_iter.Next()
    

sys.exit(0)
