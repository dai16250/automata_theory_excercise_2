import sys, getopt
from numpy import *

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


class Node:
    def __init__(self,data):
        self.data = data
        self.next = None


class TreeNode:

    def __init__(self, data):
        self.parent = None
        self.children = []
        self.data = data
        self.list = []


    def get_level(self):

        level = 0
        p = self.parent
        while p:
            level += 1
            p = p.parent

        return level

    def get_parent_node(self):
        print( str ( self.data.parent))
        return self.parent

    def add_child(self, child):
        child.parent = self
        self.children.append(child)

    def print_tree(self):
        spaces = ' '*self.get_level()*3
        prefix = spaces + "|__" if self.parent else ""
        print(prefix + self.data)
        if self.children:
            for child in self.children:
                child.print_tree()

    def create_tree(self, g, depth):


        if self.children and self.get_level() < depth:
            print("asd")
            for child in self.children:
                for x in range(0, len(g.matrix)):
                    #print(str(child.data) + " " + str(g.matrix[x][0] + " " + str(g.matrix[x][1])))
                    if str(child.data) is str(g.matrix[x][0]):
                        self.add_child(TreeNode(g.matrix[x][1]))
                        child.list.append(g.matrix[x][0])
                        child.create_tree(g, depth)
        elif self.children is None and self.get_level() < depth:
            self.add_child(TreeNode(str(self.data)))
            print(self.children)

            self.children[0].create_tree(g, depth)


        print("-----")
        self.print_tree()


class Grammar:
    def __init__(self, file):
        self.total_conditions = []
        self.non_ending_conditions = []
        self.beginning_conditions = []
        self.ending_conditions = []
        self.automate_stack = []
        self.alphabet = []
        self.file = file
        self.matrix = 0

    def initialize_grammar(self):
        tmp = self.file.read().split()

        K = int(tmp[0])

        for X in range(0 , K):
            if tmp[1][X] not in self.total_conditions:
                self.non_ending_conditions.append(tmp[1][X])
                self.total_conditions.append(tmp[1][X])
            else:
                print("There are at least 2 identical non-ending-conditions and the system cannot process this... "
                      "the program will terminate")
                sys.exit(1)
        L = int(tmp[2])

        for x in range(0,L):
            if tmp[3][x] not in self.total_conditions:
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

        for x in range(6,6+N*2):
            for y in range(0, len(tmp[x])):
                if tmp[x][y] not in self.alphabet:
                    self.alphabet.append(tmp[x][y])

        self.matrix = [[0 for x in range(col)] for y in range(rows)]

        for j in range(0, rows):
            for i in range(0, col):
                self.matrix[j][i] = tmp[(j*2 + i + 6)]


    def print_grammar(self):
        print("M = (K ,Σ ,Γ , Δ , s , F)")
        print("  - K =" + str(self.total_conditions))
        print("  - Σ =" + str(self.alphabet))
        print("  - Γ =")
        print("  - s =" + str(self.beginning_conditions))
        print("  - F =" + str(self.ending_conditions))
        print("  - D = ")
        print(*self.matrix, sep='\n')




def initialize_grammar():

    try:
        print("The file is scanned... ")
        inputfile = open(sys.argv[1], 'r')
        g = Grammar(inputfile)
        g.initialize_grammar()
        g.print_grammar()
        root = TreeNode(str(g.beginning_conditions[0]))


    except:
        print("file is not correct and did not open.... please put a correct root")
        sys.exit(1)
    else:
        print('The grammar has been created correctly...')
        while True:
            print("Give me the word you want to see if it exists in the language: ")
            word = input()
            depth = len(word)
            root.create_tree(g, depth)

            break






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
