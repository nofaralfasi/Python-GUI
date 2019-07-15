from tkinter import Tk, Message, Frame, Label, Button, Entry, LEFT, END, ttk
import re
import unittest


class Menu:
    def __init__(self, master):
        self.master = master
        master.title("Menu")
        self.notebook = ttk.Notebook(self.master)
        self.tabs = []
        self.labels = []
        self.entries = []
        self.label_desc = []

        self.instructions = ["Keep spaces between items. Do not delete brackets.\n"
                             "k can be 1 or 0 only.\n",
                             "String must be encrypted: each letter is the k'th letter before.\n",
                             "k is a number between 1 to 25.\n"
                             "The 2 sequences must be sorted and can be compared by <=.\n",
                             "Name file must end with '.txt'.\n"
                             "Ranking system must be one of: 'total'/'weighted'/'gold'.\n"]

        self.description = ["Deletes matrix's right top half if k=1, or left bottom half if k=0.",
                            "Decrypt a string according to a key value of the encryption.",
                            "Generator function - Merges 2 Iterable sequences.",
                            "Display countries from file according to ranking system."]

        self.default_input = [[[1,   2,  3,  4, 5], [6,   7,  8,  9, "spam"], [11, 12, 13, 14, 15], [16, "stam", 18, 19, 20]], 1,
                              "vrorqjdqgwkdqnviruwkhilvk", 3,
                              "1 3 7 10 16 24 30", "4 6 8 11 15 20 29",
                              "win.txt", 'total']

        self.inputs = ["Matrix:", "Key:", "String:", "Key:", "Iterable1:", "Iterable2:", "Name file:", "How to rank:"]

        for i in range(len(self.instructions)):
            self.tabs.append(Frame(self.notebook))
            self.notebook.add(self.tabs[i], text="Question #" + str(i+1))

        for i in range(len(self.tabs)):
            self.labels.append(Label(self.tabs[i], text=self.inputs[i*2], font="Ariel 11"))
            self.labels.append(Label(self.tabs[i], text=self.inputs[(i*2)+1], font="Ariel 11"))
            self.entries.append(Entry(self.tabs[i], width=60))
            self.entries.append(Entry(self.tabs[i], width=60))
            self.label_desc.append(Label(self.tabs[i], text=self.description[i], font="Ariel 11").grid(column=1, row=0))

        for i in range(len(self.entries)):
            self.labels[i].grid(row=i+1, column=0)
            self.entries[i].grid(row=i+1, column=1)

        self.instructions_button = Button(master, text="Instructions", width=20, command=self.instruction)
        self.default_button = Button(master, text="Default", width=15, command=self.default)
        self.submit_button = Button(master, text="Submit", width=15, command=self.submit)
        self.quit_button = Button(master, text="Quit", width=15, command=master.destroy)

        self.notebook.pack()
        self.instructions_button.pack(side=LEFT)
        self.default_button.pack(side=LEFT)
        self.submit_button.pack(side=LEFT)
        self.quit_button.pack(side=LEFT)

    def instruction(self):
        window = Tk()
        window.title("Instructions")
        for i in self.instructions:
            Label(window, text="Question #" + str(self.instructions.index(i) + 1), font="times 16 bold").pack()
            msg = Message(window, text=i, width=700)
            msg.config(font=('times', 14))
            msg.pack()
        window.mainloop()

    def submit(self):
        n = self.notebook.select()
        if (n[-1:]) == '2':
            print("\nQ2:")
            print(decrypt(self.entries[2].get(), int(self.entries[3].get())))
        elif (n[-1:]) == '3':
            print("\nQ3:")
            a = merge([int(x) for x in self.entries[4].get().split()], [int(x) for x in self.entries[5].get().split()])
            for i in a:
                print(i, end=' ')
            print()
        elif (n[-1:]) == '4':
            print("\nQ4 (Sorted by " + self.entries[7].get() + "):")
            a = rank(self.entries[6].get(), self.entries[7].get())
            for i in a:
                print(i)
        else:
            print("\nQ1:")
            m = []
            n = re.split('{|}', self.entries[0].get())
            for i in range(1, len(n), 2):
                m.append(n[i].split())
            print(half(m, int(self.entries[1].get())))

    def default(self):
        for i in range(len(self.entries)):
            self.entries[i].delete(0, END)
            self.entries[i].insert(0, self.default_input[i])

    # ---------------------------------------------------------------------------------


def half(matrix, k=1):
    return [(matrix[i])[-len(matrix[i]) + i * (1 - k):len(matrix[i]) - k*len(matrix[i]) + i + k] for i in range(len(matrix))]


def decrypt(string, key=1):
    str1 = ""
    for i in range(len(string)):
        new_char = ord(string[i]) - key
        if new_char < ord('a'):
            new_char += 26
        str1 += chr(new_char)
    return str1


def div_by(n, limit):
    k = 0
    while k < limit:
        yield k
        k += n


def merge(l, r):
    iter1, iter2 = iter(l), iter(r)
    n1, n2 = next(iter1), next(iter2)
    while n1 is not None and n2 is not None:
        if n1 < n2:
            yield n1
            n1 = next(iter1, None)
        else:
            yield n2
            n2 = next(iter2, None)

    if n1 is None:
        n1, iter1 = n2, iter2
    while n1 is not None:
        yield n1
        n1 = next(iter1, None)


def rank(file_name, how_to_rank='total'):
    f = open(file_name, "r")
    words, counts = [], []
    data = f.readlines()
    for line in data:
        words += line.split()
    f.close()

    for i in range(0, len(words), 4):
        g, s, p = int(words[i + 1]), int(words[i + 2]), int(words[i + 3])
        if how_to_rank == 'total':
            counts.append((words[i], g + s + p, 0))
        elif how_to_rank == 'weighted':
            counts.append((words[i], g * 3 + s * 2 + p, 0))
        elif how_to_rank == 'gold':
            counts.append((words[i], g + s + p, g))

    counts.sort(key=lambda tup: (tup[2], tup[1]), reverse=True)
    for i in range(len(counts)):
        yield counts[i][0] + " : " + str(counts[i][1])


class TestProgram(unittest.TestCase):
    test_matrix = [[[1, 2, 3, 4, 5], [6, 7, 8, 9, "spam"], [11, 12, 13, 14, 15], [16, "stam", 18, 19, 20]], [[10, 20, 30, 40, 50], [60, 70, "spam"], [90, 100, 110, 120], [130, "stam"]]]
    test_decrypt = [('tqbn', 1), ('VrOrqjDqgWkdqnvIruWkhIlvk', 3), ('jgnnq', 2)]
    test_merge = [[1, 12, 23, 34, 45], [16, 37, 48, 69], [4, 17, 20, 44, 50], [2, 3, 7, 10, 11], [0, 2, 3, 4, 7, 8, 10, 11, 12, 16, 20]]
    test_rank = [('win.txt', 'total'), ('win.txt', 'gold'), ('win.txt', 'weighted')]

    def test_half_function(self):
        a = half(TestProgram.test_matrix[0], 0)
        b = half(TestProgram.test_matrix[0], 1)
        c = half(TestProgram.test_matrix[1], 0)
        d = half(TestProgram.test_matrix[1], 1)
        self.assertIsNotNone(a)
        self.assertIsNotNone(b)
        self.assertNotEqual(a,b)
        self.assertNotEqual(c, d)

    def test_decrypt_function(self):
        a = decrypt(TestProgram.test_decrypt[0][0], TestProgram.test_decrypt[0][1])
        b = decrypt(TestProgram.test_decrypt[1][0], TestProgram.test_decrypt[1][1])
        c = decrypt(TestProgram.test_decrypt[2][0], TestProgram.test_decrypt[2][1])
        self.assertIsNotNone(a)
        self.assertIsNotNone(b)
        self.assertNotEqual(a,b)
        self.assertNotEqual(c, b)

    def test_merge_function(self):
        test = div_by(4, 21)
        m = merge(test, TestProgram.test_merge[3])
        self.assertEqual(list(m),TestProgram.test_merge[4])
        a = merge(TestProgram.test_merge[0], TestProgram.test_merge[1])
        b = merge(TestProgram.test_merge[1], TestProgram.test_merge[2])
        c = merge(TestProgram.test_merge[2], TestProgram.test_merge[0])
        self.assertEqual(list(a),[1, 12, 16, 23, 34, 37, 45, 48, 69])
        self.assertIsNotNone(a)
        self.assertIsNotNone(b)
        self.assertNotEqual(a, b)
        self.assertNotEqual(c, b)

    def test_rank_function(self):
        a = rank(TestProgram.test_rank[0][0], TestProgram.test_rank[0][1])
        b = rank(TestProgram.test_rank[1][0], TestProgram.test_rank[1][1])
        c = rank(TestProgram.test_rank[2][0], TestProgram.test_rank[2][1])
        self.assertIsNotNone(a)
        self.assertIsNotNone(b)
        self.assertNotEqual(a,b)
        self.assertNotEqual(c, b)


root = Tk()
my_gui = Menu(root)
root.mainloop()

if __name__ == "__main__":
    unittest.main()