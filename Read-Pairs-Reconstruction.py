from Node import Node
import numpy as num

def main():
    # file_input = input("Enter file name: ")
    file_name = "test5.txt"

    with open(file_name, "r") as file:
        file_digits = file.readline()
        file_digits_split = file_digits.split(" ")

        file_pairs = file.read()
        file_pairs_splitline = file_pairs.split("\n")
        file_pairs_splitpairs = []

        for pair in file_pairs_splitline:
            file_pairs_splitpairs.append(pair.split("|"))
       
        try:
            k = int(file_digits_split[0])
            d = int(file_digits_split[1])
        except:
            print("Unable to parse k and d, please check these values and try again")
            exit()

        debruijin_pairs = make_pairs(file_pairs_splitpairs)
        start_node = glue_pairs(debruijin_pairs)
        answer = eulerian_path(start_node)
        dimensional_answer = interpret_answer(answer, k, d)
        flatten_answer(dimensional_answer)

def make_pairs(pairs):
    debruijn_pairs = []
    for pair in pairs:
        prefix_1 = pair[0][:-1]
        suffix_1 = pair[0][1:]

        prefix_2 = pair[1][:-1]
        suffix_2 = pair[1][1:]

        prefix = [prefix_1, prefix_2]
        suffix = [suffix_1, suffix_2]
        node = Node(prefix, suffix, pair)
        debruijn_pairs.append(node)
    
    return debruijn_pairs

def glue_pairs(pairs):
    num_verticies = 1
    for node in pairs:
        for other_node in pairs:
            if (other_node != node):
                if (node.getSuffix() == other_node.getPrefix() and not node.getNext() and not other_node.getPrev()):
                    #Then They are paired!
                    node.addNext(other_node)
                    other_node.addPrev(node)
                    num_verticies += 1
                    break

    node_list = []

    start_node = None
    for node in pairs:
        if (not node.getPrev()):
            start_node = node

    current_node = start_node
    while(current_node):
        node_list.append(current_node)
        try:
            current_node = current_node.getNext()[0]
        except:
            break

    end = len(node_list)
    for i in range(len(node_list)):
        j = i + 1

        while(j < end):
            #print(str(node_list[i].getPrefix()) + " Compared to " + str(node_list[j].getPrefix()))
            if(node_list[i].getPrefix() == node_list[j].getPrefix()):
                node_list[i].appendNext(node_list[j].getNext())
                node_list.pop(j)
                end -= 1
            j += 1

    # for node in node_list:
    #     print("Node: " + str(node))
    #     for other_node in node.getNext():
    #         print("Next: " + str(other_node))

    return start_node

# Remember to break to other method if a cycle appears
def eulerian_path(start_node):
    answer = []

    stack = []
    stack.append(start_node)
    while (len(stack) > 0):
        v = stack[-1]
        if (v.getNext() == []):
            answer.append(v)
            stack.pop()
        else:
            w = v.getNext()[0]
            v.removeNext(w)
            stack.append(w)

    return answer

def interpret_answer(answer, k, d):
    dimensional = []
    offset = 0
    extra_spaces = len(answer) - 1
    for node in answer[::-1]:
        pair = node.getPair()
        chararray = []
        for i in range(offset):
            chararray.append(" ")

        chararray.extend(list(pair[0]))

        for i in range(d):
            chararray.append(" ")

        chararray.extend(list(pair[1]))

        for i in range(extra_spaces - offset):
            chararray.append(" ")

        offset += 1

        dimensional.append(chararray)

    return dimensional

def flatten_answer(dimensional):
    answer = ""
    for i in range(len(dimensional[0])):
        current_char = None
        for j in range(len(dimensional)):
            if (dimensional[j][i] != " "):
                current_char = dimensional[j][i]

        answer += current_char

    print(answer)
        

if __name__ == "__main__":
    main()
