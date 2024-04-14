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

def main(argv=sys.argv):
    if len(argv) == 1:
        print("Provide a file")
        return

    bit_level = False
    for i, arg in enumerate(argv):
        if arg == "-b" or arg == "--bit":
            bit_level = True
            argv.pop(i)
            break

    f = pt.Path(argv[1])

    tot = 0
    counts = np.zeros(256, dtype=np.uint32)
    # h = 0
    with f.open("rb") as fp:
        while (b := fp.read(256)):
            if bit_level:
                for i in range(len(b)):
                    for j in range(8):
                        tot += 1
                        counts[b[i] & (1 << j)] += 1
            else:
                for i in range(len(b)):
                    tot += 1
                    counts[b[i]] += 1

    probs = counts / tot
    ent = -1 * (probs * np.log2(np.where(probs == 0, np.ones(1), probs))).sum()
    if ent == 0: ent = -1 * ent
    print(probs)
    print(counts)
    print("Entropy per byte: ", ent, "bits or", ent / 8, "bytes")
    print("Entropy of file: ", ent * tot, "bits or", ent * tot / 8, "bytes")
    print("Size of file: ", tot, "bytes")
    print("Delta: ", tot - ent * tot / 8, "bytes compressable theoritically")
    print("Best Theoritical Coding ratio: ", 8 / ent)

if __name__ == "__main__":
    main()