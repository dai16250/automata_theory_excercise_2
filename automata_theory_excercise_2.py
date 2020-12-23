import sys, getopt
from numpy import *


class Grammar:
    def __init__(self, file):
        self.total_conditions = []
        self.non_ending_conditions = []
        self.ending_conditions = []
        self.automate_stack = []
        self.alphabet = []
        self.file = file
        self.matrix = 0

    def initialize_grammar(self):
        tmp = self.file.read().split()

        K = int(tmp[0])
        for x in range(1, 1 + K):
            self.non_ending_conditions.append(tmp[x])
            self.total_conditions.append(tmp[x])

        L = int(tmp[K + 1])
        for x in range(K + 1 + L, K + 2 + L):
            self.ending_conditions.append(tmp[x])
            self.total_conditions.append(tmp[x])

        N = int(tmp[K + L + 2])

        col = 2
        rows = N
        step = K + L + N

        for j in range(0, rows):
            for i in range(0, col):
                for x in range(len(tmp[step + 2 * j + i])):
                    if tmp[(step + 2 * j + i)][x] not in self.alphabet:
                        self.alphabet.append(str(tmp[(step + 2 * j + i)][x]))

        self.matrix = [[0 for x in range(col)] for y in range(rows + len(self.alphabet))]

        for j in range(0, rows):
            for i in range(0, col):
                self.matrix[j][i] = tmp[(step + 2 * j + i)]

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
        print("  - s =" + str(self.non_ending_conditions))
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
    except:
        print("file is not correct and did not open.... please put a correct root")
        sys.exit(1)
    else:
        print('The grammar has been created correctly...')


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
