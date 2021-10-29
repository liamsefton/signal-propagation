original_inputs = [.5, .4, .6, .8]

processed_inputs = [[.5, .5], [.6, .4], [.4, .6], [.2, .8]] #[[x1', x1], [x2', x2], ..., [xn', xn]]

b_list = [0, 0, 0, 0]

def processInputs(o_inputs):
    p_list = []
    for i in range(len(o_inputs)):
        p_list.append([1 - o_inputs[i], o_inputs[i]])
    return p_list

def addOneBinary(b_list):
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

def getStateProbabilities(p_inputs, b_list):
    probabilities = []
    for i in range(2**len(b_list)):
        probability = 1
        for j in range(len(p_inputs)):
            probability = probability * p_inputs[j][b_list[j]]
        probabilities.append(probability)
        addOneBinary(b_list)
    return probabilities

print(getStateProbabilities(processInputs(original_inputs), b_list))




