import sys
import pathlib as pt
import argparse
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

parser = argparse.ArgumentParser()
parser.add_argument("FILE")
parser.add_argument("-b", "--bits",
                    help="Toggle calculation of bit level entropy",
                    action="store_true")

def main():
    args = parser.parse_args()

    f = pt.Path(args.FILE)

    tot = 0
    counts = np.zeros(256, dtype=np.uint32)
    h = 0
    with f.open("rb") as fp:
        while (b := fp.read(256)):
            i = -1
            for i in range(7, len(b), 8):
                if args.bits:
                    h += bitcount(b[i]) \
                        + bitcount(b[i - 1]) \
                        + bitcount(b[i - 2]) \
                        + bitcount(b[i - 3]) \
                        + bitcount(b[i - 4]) \
                        + bitcount(b[i - 5]) \
                        + bitcount(b[i - 6]) \
                        + bitcount(b[i - 7])
                    tot += 64
                else:
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
                if args.bits:
                    tot += 8
                    h += bitcount(b[i])
                else:
                    counts[b[i]] += 1
                    tot += 1

    probs = counts / tot
    ent = -1 * (probs * np.log2(np.where(probs == 0, np.ones(1), probs))).sum()
    if ent == 0: ent = -1 * ent

    print("Entropy per byte: ", ent, "bits or", ent / 8, "bytes")
    print("Entropy of file: ", ent * tot, "bits or", ent * tot / 8, "bytes")
    print("Size of file: ", tot, "bytes")
    print("Delta: ", tot - ent * tot / 8, "bytes compressable theoritically")
    if (not args.bits):
        print("Best Theoritical Coding ratio: ", 8 / ent)

    # Realised late, I could have calculated byte entropy and wouldn't need
    # bit counting
    # Realizing that I needed bit entropy after all :)
    if args.bits:
        p1 = h / tot
        p0 = (tot - h) / tot
        print("Probability to be high: ", p1, h, tot)

        ent = p1 * (log2(tot) - log2(h)) + p0 * (log2(tot) - log2(tot - h))
        print("Informational entropy per bit: ", ent, "bits")
        print("Entropy per byte: ", ent * 8, "bits")
        print("Entropy of entire file: ", ent * tot, "bits")

if __name__ == "__main__":
    main()
