from tracemalloc import start
from Node import Node
import numpy as num

def main():
    # file_input = input("Enter file name: ")
    file_name = "test1.txt"

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
    for node in pairs:
        for other_node in pairs:
            if (other_node != node):
                if (node.getSuffix() == other_node.getPrefix() and not node.getNext() and not other_node.getPrev()):
                    #Then They are paired!
                    node.addNext(other_node)
                    other_node.addPrev(node)
                    node.addPair(other_node, node.getPair())
                    break

    node_list = []

    start_node = None
    for node in pairs:
        if (not node.getPrev()):
            start_node = node

    current_node = start_node
    while (current_node):
        node_list.append(current_node)
        try:
            current_node = current_node.getNext()[0]
        except:
            break

    end = len(node_list)
    for i in range(len(node_list)):
        j = i + 1

        # TODO: ALMOST DONE WITH THIS, LITTLE MORE TWEAKING, NEED TO FIX 
        while (j < end):
            if(node_list[i].getPrefix() == node_list[j].getPrefix()):
                node_list[i].appendNext(node_list[j].getNext())
                node_list[i].addPairMap(node_list[j].getPairMap())
                node_list[j].getPrev()[0].wipeNext()
                node_list[j].getPrev()[0].addNext(node_list[i])
                node_list.pop(j)
                end -= 1
            j += 1

    return start_node

# Remember to break to other method if a cycle appears
def eulerian_path(start_node):
    answer = []

    stack = []
    stack.append(start_node)
    while (len(stack) > 0):
        v = stack[-1]
        if (not v.getNext()):
            answer.append(v)
            stack.pop()
        else:
            w = v.getNext()[0]
            stack.append(w)
            v.removeNext(w)

    return answer

def interpret_answer(answer, k, d):
    dimensional = []
    offset = 0
    extra_spaces = len(answer) - 1

    for i in reversed(range(len(answer))):
        initial = answer[i].getPrefix()
        map = answer[i].getPairMap()
        next_pref = answer[i - 1].getPrefix()
        pair = None
        if (map):
            for next in map:
                if (next.getPrefix() == next_pref):
                    pair = map.get(next)
                    break
        else:
            pair = answer[i].getPair()

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
            print(dimensional[j][i], end=" ")
            if (current_char == None):
                if (dimensional[j][i] != " "):
                    current_char = dimensional[j][i]
            else:
                if (dimensional[j][i] != " " and dimensional[j][i] != current_char):
                    print("An error occured with the alignment in pairs, something went wrong!")
                    print("Exiting...")
                    exit()

        print()
        answer += current_char

    print(answer)
        

if __name__ == "__main__":
    main()
