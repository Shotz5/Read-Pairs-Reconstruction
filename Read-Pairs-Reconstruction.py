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

        print(str(k) + " " + str(d))
        print(file_pairs_splitpairs)
        make_pairs(file_pairs_splitpairs)

def make_pairs(pairs):
    debruijn_pairs = []
    for pair in pairs:
        prefix_1 = pair[0][:-1]
        suffix_1 = pair[0][1:]

        prefix_2 = pair[1][:-1]
        suffix_2 = pair[1][1:]

        debruijn_pairs.append([prefix_1, prefix_2])
        debruijn_pairs.append([suffix_1, suffix_2])

        print(debruijn_pairs)

if __name__ == "__main__":
    main()

