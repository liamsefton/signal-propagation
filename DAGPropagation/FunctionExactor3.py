#Algoritm to calculate the probability for a logic function to output 1, given static probability inputs


#functionExample = "(A * B) + (C)"
#functionExample = "(A) + (B) + (C)"
#functionExample = "(!A * !B * C)"
#functionExample = "(A) + (B)"
functionExample = "(A * B * !C) + (A * !B * C) + (!A * B * C) + (!A * !B * !C)"

probabilitiesExample = {"A" : .9, "B" : .8, "C" : .7}
#probabilitiesExample = {"A" : .9, "B" : .8, "C" : .7}
#probabilitiesExample = {"A":.5, "B":.5}


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

def getBinaryOutput(function, binary, binary_index_dict):
    products = function.split(" + ")
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


def getOutput(function, probabilities):
    numInputs = len(list(probabilities.keys()))
    binary = []
    for i in range(numInputs):
        binary.append(0)

    binary_index_dict = {}
    reverse_index_dict = {}
    i = 0

    for key in probabilities.keys():
        binary_index_dict[key] = i
        reverse_index_dict[i] = key
        i += 1

    i = 0
    binary_vectors = []
    for i in range(2**len(binary)):
        if getBinaryOutput(function, binary, binary_index_dict) == 1:
            binary_vectors.append(binary[:])
        addOneBinary(binary)

    prods = []
    for binary_vector in binary_vectors:
        mult = 1
        for i in range(len(binary_vector)):
            if binary_vector[i] == 0:
                mult = mult * (1 - probabilities[reverse_index_dict[i]])
            else:
                mult = mult * probabilities[reverse_index_dict[i]]
        prods.append(mult)
    return sum(prods)
    

print(getOutput(functionExample, probabilitiesExample))