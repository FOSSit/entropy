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

    return LUT.__getitem__ # fastest way to count bits in a byte

bitcount = _cl_co()

def calculate_entropy(file_path):
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

def main(argv=sys.argv):
    if len(argv) == 1:
        print("Provide one or more file paths")
        return

    for file_path in argv[1:]:
        ent, file_size = calculate_entropy(file_path)
        print("\nFile:", file_path)
        print("Entropy per byte:", ent, "bits or", ent / 8, "bytes")
        print("Entropy of file:", ent * file_size, "bits or", ent * file_size / 8, "bytes")
        print("Size of file:", file_size, "bytes")
        print("Delta:", file_size - ent * file_size / 8, "bytes compressible theoretically")
        print("Best Theoretical Coding ratio:", 8 / ent)

if __name__ == "__main__":
    main()
