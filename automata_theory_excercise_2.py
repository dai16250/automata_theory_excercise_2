import getopt
import sys

global empty_sylmbol
empty_symbol = '@'
global show_information
show_information = 0


def union(list1, list2):
    final_list = list1 + list2
    return final_list


class LinkedList:

    def __init__(self, nodes=None):
        self.head = None
        if nodes is not None:
            node = Node(data=nodes.pop(0))
            self.head = node
            for elem in nodes:
                node.next = Node(data=elem)
                node = node.next

    def __repr__(self):
        node = self.head
        nodes = []
        while node is not None:
            nodes.append(node.data)
            node = node.next
        nodes.append("None")
        return " -> ".join(nodes)

    def __iter__(self):
        node = self.head
        while node is not None:
            yield node
            node = node.next


def split_list(a_list, position):
    return a_list[:position+1], a_list[position+1:]


# Function to convert
def listToString(s):
    # initialize an empty string
    str1 = ""

    # traverse in the string
    for ele in s:
        str1 += ele

        # return string
    return str1

class Node:
    def __init__(self, data):
        self.data = data
        self.next = None


class TreeNode:

    def __init__(self, data):
        self.parent = None
        self.children = []
        self.data = data
        self.list = []
        self.key = None

    def get_level(self):

        level = 0
        p = self.parent
        while p:
            level += 1
            p = p.parent

        return level

    def get_parent_node(self):
        print(str(self.data.parent))
        return self.parent

    def add_child(self, child, letter):
        child.parent = self
        child.key = letter
        self.children.append(child)

    def __repr__(self):
        return f'{self.data}'

    def print_tree(self):
        spaces = ' ' * self.get_level() * 3
        prefix = spaces + "|__" if self.parent else ""
        print(prefix + self.__repr__())
        if self.children:
            for child in self.children:
                child.print_tree()

    def renew_list(self, parent, next, key):

        if show_information:
            print("The parent is: " + str(parent))
            print("The next is: " + str(next))
            print("The key is: " + str(key))

        for x in self.list:
            if x is key:
                list_1, list_2 = split_list(self.list, self.list.index(x))
                if show_information:
                    print("The list_1 :" + str(list_1))
                    print("The list_2 :" + str(list_2))
                list_1.pop(list_1.index(x))

                for elem in next:
                    if elem is not empty_symbol:
                        list_1.append(elem)
                self.list = list_1 + list_2
                break


    def add_tree(self, g, depth, key):



        if self.parent is None:
            for elem in self.data:
                self.list.append(elem)
        else:
            if show_information:
                print("-----------")
                self.renew_list(self.parent.data, self.data, key)
                print("The parent's list: " +str(self.parent.list))
                print("The child's list: " +str(self.list))
                print("-----------")
            else:
                self.renew_list(self.parent.data, self.data, key)


        if self.get_level() < depth:
            for letter in self.data:
                for x in range(0, len(g.matrix)):
                    if str(letter) is str(g.matrix[x][0]):
                        self.add_child(TreeNode(g.matrix[x][1]), str(letter))

            for y in range(0, len(self.children)):
                self.children[y].list = union(self.list, self.children[y].list)
                self.children[y].add_tree(g, depth, self.children[y].key)

    def traverse_tree(self, word):

        if self.children:
            for child in self.children:

                print(str(word) + ' ' + listToString(child.list) )

                print(str(word) is listToString(child.list))

                if str(word) is str(listToString(child.list)):
                    print("vrethike")
                    return True
                else:
                    child.traverse_tree(word)
        else:
            return False

    def reset_tree(self):

        if self.children:
            for child in self.children:
                child.reset_tree()
        else:
            self.data = 0
            self.list.clear()
            self.key = None
            self.parent = None

    def print_lists(self):
        print(self.list)
        for child in self.children:
            child.print_lists()


class Grammar:

    def __init__(self, file):
        self.total_conditions = []
        self.non_ending_conditions = []
        self.beginning_conditions = []
        self.ending_conditions = []
        self.alphabet = []
        self.file = file
        self.matrix = 0

    def initialize_grammar(self):
        tmp = self.file.read().split()

        K = int(tmp[0])

        for X in range(0, K):
            if tmp[1][X] not in self.non_ending_conditions:
                self.non_ending_conditions.append(tmp[1][X])
                self.total_conditions.append(tmp[1][X])
            else:
                print("There are at least 2 identical non-ending-conditions and the system cannot process this... "
                      "the program will terminate")
                sys.exit(1)
        L = int(tmp[2])

        for x in range(0, L):
            if tmp[3][x] not in self.ending_conditions:
                self.ending_conditions.append(tmp[3][x])
                self.total_conditions.append(tmp[3][x])
            else:
                print("There are at least 2 identical ending-conditions and the system cannot process this... the "
                      "program will terminate")
                sys.exit(1)

        self.beginning_conditions.append(str(tmp[4]))

        N = int(tmp[5])

        col = 2
        rows = N

        for x in range(6, 6 + N * 2):
            for y in range(0, len(tmp[x])):
                if tmp[x][y] not in self.alphabet:
                    self.alphabet.append(tmp[x][y])

        self.matrix = [[0 for x in range(col)] for y in range(rows)]

        for j in range(0, rows):
            for i in range(0, col):
                self.matrix[j][i] = tmp[(j * 2 + i + 6)]

    def print_grammar(self):
        print("M = (K ,Σ ,Γ , Δ , s , F)")
        print("  - K =" + str(self.total_conditions))
        print("  - Σ =" + str(self.alphabet))
        print("  - Γ =")
        print("  - s =" + str(self.beginning_conditions))
        print("  - F =" + str(self.ending_conditions))
        print("  - D = ")

        for rows in self.matrix:
            print("      Δ" + str(rows))


def initialize_grammar():
    try:
        print("The file is scanned... ")
        inputfile = open(sys.argv[1], 'r')
        g = Grammar(inputfile)
        g.initialize_grammar()
        g.print_grammar()

    except:
        print("file is not correct and did not open.... please put a correct root")
        sys.exit(1)
    else:
        print('The grammar has been created correctly...')
        while True:
            flag = 0
            print("Give me the word you want to see if it exists in the language: ")
            word = input()
            for letter in word:
                if letter not in g.alphabet:
                    print("The word has letters that doesn't belong in the language's alphabet. \nPlease choose another word...\n\n")
                    flag = 1
                    break

            if not flag:
                root = TreeNode(str(g.beginning_conditions[0]))
                depth = len(word)
                root.add_tree(g, depth, g.beginning_conditions[0])
                if show_information:
                    root.print_tree()
                    root.print_lists()

                if root.traverse_tree(word):
                    print("The word '" + word + "' belongs to our language!!!!")
                else:
                    print("The word '" + word + "' does not belong to our language!!!!")

            print("Do you want to find another word?? Press 'Y' if you want to continue")
            if input() is 'Y':
                root.reset_tree()
            else:
                print("Thank you for using the program ... the system will terminate now")
                sys.exit(0)


def main(argv):
    try:
        opts, args = getopt.getopt(argv, "hi:o", ["ifile=", "ofile="])
    except getopt.GetoptError:
        print('test.py -i <inputfile.txt> -o <outputfile.txt')
        sys.exit(2)

    if len(sys.argv) != 2:
        print("Not the correct format.... python test.py <file.txt>")
        sys.exit(1)

    initialize_grammar()


if __name__ == "__main__":
    main(sys.argv[1:])
