from Node import Node

def main():
    # file_input = input("Enter file name: ")
    file_name = "test4.txt"

    # File preparation stuff, gets data from file and then parses it to usable variables
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

        # Main Driver for application
        debruijin_pairs = make_pairs(file_pairs_splitpairs)
        start_node = glue_pairs(debruijin_pairs)
        answer = eulerian_path(start_node)
        dimensional_answer = interpret_answer(answer, d)
        flat_answer = flatten_answer(dimensional_answer)
        print(flat_answer)

def make_pairs(pairs):
    """
        Parses the data into the usable pairs of k-1 length

        Parameters:

            pairs (list[list]): a list of k-mer pairs
                Example: [["GAGA", "TTGA"], ["TCGT", "GATG"]]

        Returns:

            debruijn_pairs (list[Node])
    """
    debruijn_pairs = []
    for pair in pairs:
        # Make first prefix and suffix using pair[0]
        prefix_1 = pair[0][:-1]
        suffix_1 = pair[0][1:]

        # Make second prefix and suffix using pair[1]
        prefix_2 = pair[1][:-1]
        suffix_2 = pair[1][1:]

        # Append the prefix's and suffix's to their lists and make them into a Node object,
        # and append to list of Nodes
        prefix = [prefix_1, prefix_2]
        suffix = [suffix_1, suffix_2]
        node = Node(prefix, suffix, pair)
        debruijn_pairs.append(node)

    return debruijn_pairs

def glue_pairs(pairs):
    """
        Takes a list of debruijn pairs and ties them together using Node getNext and getPrev methods
        After tieing them together, checks for similar nodes, and ties them together

        Parameters:

            pairs (list[Node]): A list of debrujin pair nodes to be tied together

        Returns:

            start_node (Node): The first Node in the path
    """
    # Ties nodes together in one contig strand
    for node in pairs:
        for other_node in pairs:
            if (other_node != node):
                if (node.getSuffix() == other_node.getPrefix() and not node.getNext() and not other_node.getPrev()):
                    # Then are a match!
                    node.addNext(other_node)
                    other_node.addPrev(node)
                    node.addPair(other_node, node.getPair())
                    # Found match, don't need to continue
                    break

    node_list = []

    # Finds the start node (the node that has no previous Node)
    start_node = None
    for node in pairs:
        if (not node.getPrev()):
            start_node = node

    # Fill up our node_list so we can parse it for similar Nodes, without worrying about breaking next and prev continuity
    current_node = start_node
    while (current_node):
        node_list.append(current_node)
        try:
            current_node = current_node.getNext()[0]
        except:
            break

    # Iterate through the node list, take the current node and check all occurances after it in the list for matching prefixes
    end = len(node_list)
    for i in range(len(node_list)):
        j = i + 1
        while (j < end):
            # If we have a match
            if(node_list[i].getPrefix() == node_list[j].getPrefix()):
                # Take all the Nodes the matching node points to, and append them to the current Node
                node_list[i].appendNext(node_list[j].getNext())
                # Take the PairMap from the matching Node and append it to the current node
                node_list[i].addPairMap(node_list[j].getPairMap())
                # Remove pointers to the matching Node
                node_list[j].getPrev()[0].wipeNext()
                # Take the pointers that pointer to the matching Node, and point them to the current Node
                node_list[j].getPrev()[0].addNext(node_list[i])
                # Remove the matching node from the list
                node_list.pop(j)
                end -= 1
            j += 1

    return start_node

def eulerian_path(start_node):
    """
        Calculates Eulerian path of Nodes from the start_node

        Parameters:

            start_node (Node): The beginning Node in the De Bruijn Graph

        Returns:

            answer: (list[Node]): The ordered list of Nodes to be interpreted
    """
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

def interpret_answer(answer, d):
    """
        Interprets the ordered list of Nodes and parses it to a 2D matrix

        Parameters:

            answer (list[Node]): The list of Nodes in order to interpret
            d (int): Distance between read-pairs

        Returns:

            dimensional (list[list[char]]): a 2D representation of the read pairs
    """
    dimensional = []
    offset = 0
    extra_spaces = len(answer) - 1

    for i in reversed(range(len(answer))):
        # Get current Node's pairmap
        map = answer[i].getPairMap()
        # Get the next Node's prefix
        next_pref = answer[i - 1].getPrefix()
        pair = None
        # If the map is populated (not the last object in the de Bruijn graph)
        if (map):
            # Search the map for the edge's pair
            for next in map:
                if (next.getPrefix() == next_pref):
                    pair = map.get(next)
                    break
        else:
            # Else we're on the last node, get the last edge
            pair = answer[i].getPair()

        # Build a dimension of the array
        chararray = []
        # Pad beginning with spaces length of offset
        for i in range(offset):
            chararray.append(" ")

        # Turn top pair into list of chars
        chararray.extend(list(pair[0]))

        # Pad distance between read pairs with spaces
        for i in range(d):
            chararray.append(" ")

        # Turn bottom pair into list of chars
        chararray.extend(list(pair[1]))

        # Pad with spaces the length of the longest pair
        for i in range(extra_spaces - offset):
            chararray.append(" ")

        offset += 1

        # Append it to the 2D array
        dimensional.append(chararray)

    return dimensional

def flatten_answer(dimensional):
    """
        Take the 2D array, and check every column to make sure it is the same character, if they are, return the flattened array

        Parameters:

            dimensional (list[list[char]]): 2D representation of the read-pairs

        Returns:

            answer (string): A string representing our re-assembed composition
    
    """
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

    return answer
        

if __name__ == "__main__":
    main()
