import tkinter as tk
from tkinter import filedialog
from functools import partial
import sys
import pathlib as pt
from math import log2
import numpy as np

def _cl_co():
    def co(i):
        o = 0
        for _ in range(8):
            o += i & 1
            i >>= 1
        return o

    LUT = [co(i) for i in range(256)]

    return LUT.__getitem__ 

bitcount = _cl_co()

def calculate_byte_entropy(file_path):
    f = pt.Path(file_path)

    tot = 0
    counts = np.zeros(256, dtype=np.uint32)

    with f.open("rb") as fp:
        while (b := fp.read(256)):
            i = -1
            for i in range(7, len(b), 8):
                tot += 8
                counts[b[i]] += 1
                counts[b[i - 1]] += 1
                counts[b[i - 2]] += 1
                counts[b[i - 3]] += 1
                counts[b[i - 4]] += 1
                counts[b[i - 5]] += 1
                counts[b[i - 6]] += 1
                counts[b[i - 7]] += 1

            for i in range(i + 1, len(b)):
                tot += 1
                counts[b[i]] += 1

    probs = counts / tot
    ent = -1 * (probs * np.log2(np.where(probs == 0, np.ones(1), probs))).sum()
    if ent == 0: ent = -1 * ent

    return ent, tot

def calculate_bit_entropy(file_path):
    f = pt.Path(file_path)

    tot = 0
    h = 0

    with f.open("rb") as fp:
        while (b := fp.read(1)):
            tot += 8
            h += bitcount(b[0])

    p1 = h / tot
    p0 = (tot - h) / tot

    ent = p1 * (log2(tot) - log2(h)) + p0 * (log2(tot) - log2(tot - h))
    return ent, tot

def calculate_entropy_wrapper(file_path, option):
    if option == "byte":
        return calculate_byte_entropy(file_path)
    elif option == "bit":
        return calculate_bit_entropy(file_path)

class EntropyCalculatorApp:
    def __init__(self, master):
        self.master = master
        master.title("Entropy Calculator")

        self.file_paths = []
        self.option_var = tk.StringVar(master)
        self.option_var.set("byte")

        self.select_button = tk.Button(master, text="Select File", command=self.select_file)
        self.select_button.pack()

        self.option_menu = tk.OptionMenu(master, self.option_var, "byte", "bit")
        self.option_menu.pack()

        self.calculate_button = tk.Button(master, text="Calculate Entropy", command=self.calculate_entropy, state=tk.DISABLED)
        self.calculate_button.pack()

        self.result_label = tk.Label(master, text="")
        self.result_label.pack()

    def select_file(self):
        file_paths = filedialog.askopenfilenames()
        if file_paths:
            self.file_paths = file_paths
            self.calculate_button.config(state=tk.NORMAL)

    def calculate_entropy(self):
        option = self.option_var.get()

        results = ""
        for file_path in self.file_paths:
            ent, file_size = calculate_entropy_wrapper(file_path, option)
            results += f"\nFile: {file_path}\n"
            results += f"Entropy per {option}: {ent} bits or {ent / 8} bytes\n"
            results += f"Entropy of file: {ent * file_size} bits or {ent * file_size / 8} bytes\n"
            results += f"Size of file: {file_size} bytes\n"
            results += f"Delta: {file_size - ent * file_size / 8} bytes compressible theoretically\n"
            results += f"Best Theoretical Coding ratio: {8 / ent}\n"

        self.result_label.config(text=results)

def main():
    root = tk.Tk()
    root.geometry("600x400")  # Set initial window size
    app = EntropyCalculatorApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()