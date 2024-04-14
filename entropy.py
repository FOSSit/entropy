import argparse
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

    return LUT.__getitem__  # fastest way to count bits in a byte

bitcount = _cl_co()

def main(argv=sys.argv):
    parser = argparse.ArgumentParser(description='Calculate entropy of a file.')
    parser.add_argument('file', type=str, help='Path to the file')
    parser.add_argument('-b', '--bit', action='store_true', help='Calculate bit-level entropy')

    args = parser.parse_args(argv[1:])

    f = pt.Path(args.file)

    tot = 0
    counts = np.zeros(256, dtype=np.uint32)
    with f.open("rb") as fp:
        while (b := fp.read(256)):
            for i in range(0, len(b), 8):
                if args.bit:
                    for j in range(i, i + 8):
                        counts[b[j]] += 1
                        tot += 1
                else:
                    for j in range(i, i + 8):
                        counts[b[j]] += 1
                    tot += 64

    probs = counts / tot
    ent = -1 * (probs * np.log2(np.where(probs == 0, np.ones(1), probs))).sum()
    if ent == 0: ent = -1 * ent
    print(probs)
    print(counts)
    print("Entropy per byte: ", ent, "bits or", ent / 8, "bytes")
    print("Entropy of file: ", ent * tot, "bits or", ent * tot / 8, "bytes")
    print("Size of file: ", tot, "bytes")
    print("Delta: ", tot - ent * tot / 8, "bytes compressible theoretically")
    print("Best Theoretical Coding ratio: ", 8 / ent)

if __name__ == "__main__":
    main()
