from liberty.parser import parse_liberty

library = parse_liberty(open("libertytest.lib").read())

#for cell_group in library.get_groups('cell'):
    #name = cell_group.args[0]
    #print(name)

#print(str(library.get_groups('pin')))
#for pins in library.get_groups('pin'):
#    print(pins)
#    break

cell_groups = library.get_groups('cell')
print(len(cell_groups))
leakage_groups = cell_groups[0].get_groups('leakage_power')
for group in leakage_groups:
    print(group.get('value'))
    print(group.get('when'))
pin_groups = cell_groups[0].get_groups('pin')
print(len(pin_groups))
#print(pin_groups[0].get('function'))
for thing in pin_groups:
    print(thing.get('function'))
    


#for thing in pin_groups:
#    print(thing)