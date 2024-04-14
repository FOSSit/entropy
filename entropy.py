import sys
import pathlib as pt
from math import log2
import numpy as np

def calculate_entropy(filename):
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

    f = pt.Path(filename)

    tot = 0
    counts = np.zeros(256, dtype=np.uint32)

    with f.open("rb") as fp:
        while (b := fp.read(256)):
            i = -1
            for i in range(7, len(b), 8):
                tot += 8
                for j in range(8):
                    counts[b[i - j]] += 1

            for j in range(i + 1, len(b)):
                counts[b[j]] += 1
                tot += 1

    probs = counts / tot
    ent = -1 * (probs * np.log2(np.where(probs == 0, np.ones(1), probs))).sum()
    if ent == 0: ent = -1 * ent
    return ent, tot

def main(filename):
    ent, tot = calculate_entropy(filename)
    print("Entropy of file: ", ent * tot, "bits or", ent * tot / 8, "bytes")
    print("Size of file: ", tot, "bytes")
    print("Delta: ", tot - ent * tot / 8, "bytes compressible theoretically")
    print("Best Theoretical Coding ratio: ", 8 / ent)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python entropy.py <filename>")
        sys.exit(1)
    main(sys.argv[1])
