"""

Author: Konstantinos Razgelis
ID:     dai16250
Date:   January 2021

"""

import getopt
import sys

"""
Assigment of global variables and lists.
"""
empty_symbol = '@'
show_information = 0
found = False
route = []
depth = 0
word = ''
letter_counter = []


def union(list1, list2):
    """
    The union function unites 2 lists into one

    :param list1:               The first list to be united
    :param list2:               The second list to be united
    :return:                    The united list
    """

    final_list = list1 + list2
    return final_list


def split_list(a_list, position):
    """
    The split_list function splits a lists into 2 parts  of each self the right and left side of the list.
    The place where the split takes place is the position of the letter which is exchanged.

    :param a_list:                          Is the list that we want to split
    :param position:                        Is the position of the index of the list that we want to split
    :return:                                the left and the right side of the list
    """
    return a_list[:position + 1], a_list[position + 1:]



def listToString(s):
    """
    The listToString function creates a string word for the letters of a list

    :param s:                          s is the list
    :return:                           The string
    """
    # initialize an empty string
    str1 = ""

    # traverse in the string
    for ele in s:
        str1 += ele

    # return string
    return str1


def count_digits(g, word_):
    """
    The count_digits function takes the word given by the user and counts how many copies of each letter it has.
    This function return that amount in a 2D-list representing a good idea on which leaf the program is going to cut
    in order the tree will no have any child that is proven it will no longer have a possible correct result.

    :param g:                           g is the grammar
    :param word_:                       word is the word given by the user
    :return:                            the list with all the letters counted
    """
    letters = []

    for x in g.alphabet:
        if x != empty_symbol:
            letters.append(x)


    list = [[0 for x in range(2)] for y in range(len(letters))]

    for index in range(0, len(letters)):
        list[index][0] = letters[index]


    for letter in word_:
        for index in range(0, len(letters)):
            if letter == letters[index]:
                list[index][1] += 1
                break

    if show_information:
        for rows in list:
            print(rows)

    return list


def puming(array, g):

    """
    The puming function cuts the leaf of the tree that is proven they wont lead to a result.

    :param array:                   array is the matrix which has all the possible moves
    :param g:                       g is the grammar
    :return:                        the puming_matrix which only has items from the g.matrix showing the next step
    """

    flag = []
    count = 0
    puming_matrix = []

    check = count_digits(g, listToString(array))

    for index in range(0, len(check)):
        if check[index][1] == letter_counter[index][1]:
            flag.append(check[index][0])
            count += 1



    for rows in g.matrix:
        good = True
        for letter in rows[1]:
            for flagger in range(0, len(flag)):
                if str(letter) == str(flag[flagger]):
                    good = False
                    break
        if good:
            puming_matrix.append(rows)

    if show_information:
        print("---------")
        for rows in puming_matrix:
            print(rows)
        print("---------")

    return puming_matrix


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

    def __repr__(self):
        return f'{self.data}'

    def get_level(self):
        """
        The get_level function take a child and returns how deep is in the tree.

        :return:                The depth of the specific child.
        """
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
        """
        The add_child function adds a child in the Node.

        :param child:               It adds a child
        :param letter:              The letter which the action was taken place.

        """
        child.parent = self
        child.key = letter
        self.children.append(child)

    def print_tree(self):
        """
        The print_tree function prints all the children of a Tree.

        :return:                The Tree.

        """
        if not self.parent:
            print("-------------The Tree is being displayed bellow-------------------")

        spaces = ' ' * self.get_level() * 3
        prefix = spaces + "|__" if self.parent else ""
        print(prefix + self.__repr__())
        if self.children:
            for child in self.children:
                child.print_tree()

    def renew_list(self, parent, next_step, key):
        """
        The renew_list function takes a the list of a child and changes the information.

        :param parent:                      Is the parent of the child.
        :param next_step:                   The possible next moves.
        :param key:                         Is the key letter where the change has occurred.
        :return:                            The new combined list.
        """
        if show_information:
            print("The parent is: " + str(parent))
            print("The next is: " + str(next_step))
            print("The key is: " + str(key))

        self.list = parent

        for x in self.list:
            if str(x) == str(key):
                list_1, list_2 = split_list(self.list, self.list.index(x))
                if show_information:
                    print("The list_1 :" + str(list_1))
                    print("The list_2 :" + str(list_2))
                list_1.pop(list_1.index(x))

                for elem in next_step:
                    if elem is not empty_symbol:
                        list_1.append(elem)

                self.list = list_1 + list_2
                break

    def add_tree(self, g):
        """

        The add_tree function it creates the tree with all the possible steps of a given language. The tree's depth is
        based on the length of a given word (e.g. word: abba --> TreeDepth = 4, word: aab --> TreeDepth = 3).

        :param g:                   g is the Grammar of the language.
        :param depth:               depth is the depth of the tree.
        :param key:                 key is the key letter in every singe condition.
        :return:                    A complete N-depth tree with all the possible roots of a language.

        """


        if self.parent:
            self.renew_list(self.parent.list, self.data, self.key)
        else:
            for elem in self.data:
                self.list.append(elem)

        if self.get_level() < depth:
            for letter in self.data:

                checker = puming(self.list, g)
                for index in range(0, len(checker)):
                    if letter == checker[index][0]:
                        self.add_child(TreeNode(checker[index][1]), letter)

        for child in self.children:
            child.add_tree(g)

    def print_route(self):
        global route
        route.append(self)


        if self.parent:
            self.parent.print_route()
        else:
            print("--------------The route of the algorithm to find the word---------")

    def traverse_tree(self):
        """

        The traverse_tree function is a breadth-first search algorithm. Is searches a Tree to find if the 'word' belongs
        to the language.

        :param word:                The word is the word that the user is looking to find if it belongs in the language.
        :return:                    True if it belongs/False if it does not belong.

        """
        global found, route

        if self.children and not found:
            for child in self.children:
                if str(word) == listToString(child.list):
                    found = True
                    child.print_route()
                    for x in range(len(route) - 1, -1, -1):
                        if x == 0:
                            print(listToString(route[x].list))
                        else:
                            print(listToString(route[x].list), end=' ----> ')
                    break
                else:
                    child.traverse_tree()

        return found

    def reset_tree(self):
        """
        The reset_tree function resets the tree when the user is willing to search if another word belongs to the Language.

        :return:                   The reset tree node.
        """
        if self.children:
            for child in self.children:
                child.reset_tree()
        else:
            self.data = 0
            self.list.clear()
            self.key = None
            self.parent = None

    def print_lists(self):
        """
        The print_lists function returns the value of the list from all the Nodes in the root

        :return:
        """
        if not self.parent:
            print('--------All the possible words that are being created ------------')

        print(listToString(self.list) , end= ', ')
        for child in self.children:
            child.print_lists()



class Grammar:

    def __init__(self, file):
        """
        The __init__ function creates an object of the grammar class.
        A 'Grammar Object' is defined by the following variables :

        total_conditions:       all the conditions that the grammar has.
        non_ending_conditions:  all the non-conditions that the grammar has.That means that the automate machine cannot stop there.
        ending_conditions:      all the ending-conditions that the grammar has. That means the the automate machine can stop there.
        alphabet:               is the total letters that the grammar has.
        file :                  is the file that the programs gathers information about the grammar.
        matrix:                 is a 2D-matrix that all the necessary information is being stored and the program can use.

        :param file:            is the file that has all the information about the language(It is given by the user).
        """
        self.total_conditions = []
        self.non_ending_conditions = []
        self.beginning_conditions = []
        self.ending_conditions = []
        self.alphabet = []
        self.file = file
        self.matrix = 0

    def initialize_grammar(self):
        """
        The initialize_grammar function is processing the file which has the information of the grammar given by the user.

        :return:                An Grammar Object that has all the information from the file given.
        """
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
                if tmp[x][y] not in self.alphabet and tmp[x][y] not in self.total_conditions:
                    self.alphabet.append(tmp[x][y])

        self.matrix = [[0 for x in range(col)] for y in range(rows)]

        for j in range(0, rows):
            for i in range(0, col):
                self.matrix[j][i] = tmp[(j * 2 + i + 6)]

    def print_grammar(self):
        """

        The print_grammar function takes a Grammar Object.

        :return:                It returns the information of the grammar in a visible way.

        """
        print("G = (V ,Σ ,R , S)")
        print("  - V =" + str(self.alphabet))
        print("  - Σ =" + str(self.ending_conditions))
        print("  - s =" + str(self.beginning_conditions))
        print("  - R = ")
        for x in range(0, len(self.matrix)):
            print("    " + (str(x + 1)) + ') ' + self.matrix[x][0] + " --> " + self.matrix[x][1])


def initialize_grammar():
    global found, depth, route, word
    global letter_counter

    """
    It open a file given by the user and if no problem occurred during the procedure then it continues to the main
    program.
    """
    try:
        print("The file is scanned... ")
        file = open(sys.argv[1], 'r')
        g = Grammar(file)
        g.initialize_grammar()
        g.print_grammar()
    except:
        print("\nfile is not correct and did not open.... please put a correct root")
        sys.exit(1)
    else:
        print('The grammar has been created correctly...\n'
              "--------------------------------------------------------------------")
        while True:
            flag = 0
            print("Give me the word you want to see if it exists in the language: ")
            word = input()

            for letter in word:
                if letter not in g.alphabet:
                    print("The word has letters that doesn't belong in the language's alphabet. "
                          "\nPlease choose another word...\n\n")
                    flag = 1
                    break

            if not flag:
                depth = len(word)
                letter_counter = count_digits(g, word)

                root = TreeNode(str(g.beginning_conditions[0]))
                root.add_tree(g)

                root.print_lists()
                print('\n')
                root.print_tree()

                if show_information:
                    root.print_lists()

                print('\n')
                if root.traverse_tree():
                    print("The word '" + word + "' belongs to our language!!!!")
                else:
                    print("The word '" + word + "' does not belong to our language!!!!")

            print("Do you want to find another word?? Press 'Y' if you want to continue")

            if str(input()) == 'Y':
                root.reset_tree()
                route.clear()
                found = False
                print("The program has been restarted\n"
                      "--------------------------------------------------------------------\n")
            else:

                print("--------------------------------------------------------------------\n"
                      "Thank you for using the program ... the system will terminate now.")
                sys.exit(0)


def main(argv):
    """
    The main function is the main program which asks from the user to add the file with the grammar.
    """
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
