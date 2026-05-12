import tkinter as tk
from tkinter import messagebox
from nltk import CFG
from nltk.parse import ChartParser
from nltk.tree import Tree
import nltk

nltk.download('punkt')


class CFGApp:

    def __init__(self, root):

        self.root = root
        self.root.title("CFG Parser")
        self.root.geometry("800x600")

        tk.Label(root, text="Grammar").pack()

        self.grammar_box = tk.Text(root, height=10, width=70)
        self.grammar_box.pack()

        self.grammar_box.insert(tk.END,
"""S -> NP VP
NP -> Det N
VP -> V NP
Det -> 'the'
N -> 'cat' | 'dog'
V -> 'chased'"""
        )

        tk.Label(root, text="Sentence").pack()

        self.sentence = tk.Entry(root, width=70)
        self.sentence.pack()
        self.sentence.insert(0, "the cat chased the dog")

        self.mode = tk.StringVar(value="Left")

        tk.Radiobutton(root, text="Left", variable=self.mode, value="Left").pack()
        tk.Radiobutton(root, text="Right", variable=self.mode, value="Right").pack()

        tk.Button(root, text="Generate", command=self.generate).pack(pady=10)

        self.output = tk.Text(root, height=15, width=90)
        self.output.pack()

    def derivation(self, tree, reverse=False):

        steps = []

        def walk(t):

            if isinstance(t, Tree):

                children = t[::-1] if reverse else t

                if reverse:
                    for c in children:
                        walk(c)

                steps.append(
                    f"{t.label()} -> {' '.join([c.label() if isinstance(c, Tree) else c for c in t])}"
                )

                if not reverse:
                    for c in children:
                        walk(c)

        walk(tree)

        return steps

    def ast(self, tree):

        important = ['S', 'NP', 'VP', 'V', 'N']

        if not isinstance(tree, Tree):
            return tree

        children = [self.ast(c) for c in tree]

        children = [c for c in children if c]

        if tree.label() not in important:

            if len(children) == 1:
                return children[0]

            return Tree("X", children)

        return Tree(tree.label(), children)

    def generate(self):

        try:

            grammar = CFG.fromstring(
                self.grammar_box.get("1.0", tk.END)
            )

            parser = ChartParser(grammar)

            trees = list(
                parser.parse(
                    self.sentence.get().split()
                )
            )

            if not trees:
                messagebox.showerror("Error", "Invalid sentence")
                return

            tree = trees[0]

            reverse = self.mode.get() == "Right"

            derivation = self.derivation(tree, reverse)

            self.output.delete("1.0", tk.END)

            self.output.insert(tk.END, "=== DERIVATION ===\n\n")

            for step in derivation:
                self.output.insert(tk.END, step + "\n")

            tree.draw()

            self.ast(tree).draw()

        except Exception as e:
            messagebox.showerror("Error", str(e))


root = tk.Tk()

app = CFGApp(root)

root.mainloop()