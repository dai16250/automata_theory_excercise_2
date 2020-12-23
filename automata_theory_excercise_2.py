import sys, getopt
from numpy import *

class TreeNode:
    def __init__(self, data):
        self.parent = None
        self.children = []
        self.data = data

    def get_parent_node(self):
        print( str ( self.data.parent))
        return self.parent

    def add_child(self, child):
        child.parent = self
        self.children.append(child)

    def print_tree(self):
        print(self.data)
        if self.children:
            for child in self.children:
                child.print_tree()



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

        self.matrix = [[0 for x in range(col)] for y in range(rows + len(self.alphabet))]

        for j in range(0, rows):
            for i in range(0, col):
                self.matrix[j][i] = tmp[(j*2 + i + 6)]

        j = len(self.matrix) - len(self.alphabet)
        for letter in self.alphabet:
            if str(letter) != 'S':
                self.matrix[j][0] = str(letter)
                self.matrix[j][1] = str(letter)
                j += 1

    def print_grammar(self):
        print("M = (K ,Σ ,Γ , Δ , s , F)")
        print("  - K =" + str(self.total_conditions))
        print("  - Σ =" + str(self.alphabet))
        print("  - Γ =")
        print("  - s =" + str(self.beginning_conditions))
        print("  - F =" + str(self.ending_conditions))
        print("  - D = ")
        print(*self.matrix, sep='\n')

def create_tree(g , r):

    r.print_tree()



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

        root = TreeNode(str(g.beginning_conditions[0]))
        create_tree(g, root)



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
