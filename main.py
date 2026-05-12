import tkinter as tk
from tkinter import messagebox
from nltk import CFG
from nltk.parse import ChartParser
from nltk.tree import Tree
import nltk

nltk.download('punkt')


class Gramatica:

    def __init__(self, root):

        self.root = root
        self.root.title("Analizador de Expresiones Matemáticas")
        self.root.geometry("800x600")

        tk.Label(root, text="Gramática").pack()

        self.grammar_box = tk.Text(root, height=15, width=70)
        self.grammar_box.pack()

        self.grammar_box.insert(
            tk.END,
"""E -> E '+' T
E -> E '-' T
E -> T

T -> T '*' F
T -> T '/' F
T -> F

F -> '(' E ')'
F -> '1'
F -> '2'
F -> '3'
F -> '4'
F -> '5'"""
        )

        tk.Label(root, text="Expresión Matemática").pack()

        self.sentence = tk.Entry(root, width=70)
        self.sentence.pack()
        self.sentence.insert(0, "1 + 2 * 3")

        self.mode = tk.StringVar(value="Izquierda")

        tk.Radiobutton(
            root,
            text="Derivación Izquierda",
            variable=self.mode,
            value="Izquierda"
        ).pack()

        tk.Radiobutton(
            root,
            text="Derivación Derecha",
            variable=self.mode,
            value="Derecha"
        ).pack()

        tk.Button(
            root,
            text="Generar",
            command=self.generate
        ).pack(pady=10)

        self.output = tk.Text(root, height=15, width=90)
        self.output.pack()

    def derivacion(self, tree, reverse=False):

        pasos = []

        def recorrer(t):

            if isinstance(t, Tree):

                children = t[::-1] if reverse else t

                if reverse:
                    for c in children:
                        recorrer(c)

                pasos.append(
                    f"{t.label()} -> {' '.join([c.label() if isinstance(c, Tree) else c for c in t])}"
                )

                if not reverse:
                    for c in children:
                        recorrer(c)

        recorrer(tree)

        return pasos

    def ast(self, tree):

        importantes = ['E', 'T', 'F']

        if not isinstance(tree, Tree):
            return tree

        children = [self.ast(c) for c in tree]

        children = [c for c in children if c]

        if tree.label() not in importantes:

            if len(children) == 1:
                return children[0]

            return Tree("AST", children)

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
                messagebox.showerror(
                    "Error",
                    "Expresión matemática inválida"
                )
                return

            tree = trees[0]

            reverse = self.mode.get() == "Derecha"

            derivacion = self.derivacion(tree, reverse)

            self.output.delete("1.0", tk.END)

            self.output.insert(
                tk.END,
                "=== DERIVACIÓN ===\n\n"
            )

            for paso in derivacion:
                self.output.insert(tk.END, paso + "\n")

            ast_tree = self.ast(tree)

            ast_tree.draw()

            tree.draw()

        except Exception as e:

            messagebox.showerror(
                "Error",
                str(e)
            )


root = tk.Tk()

app = Gramatica(root)

root.mainloop()