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
    if len(argv) < 2:
        print("Provide a file")
        return

    f = pt.Path(argv[1])

    tot = 0
    counts = np.zeros(256, dtype=np.uint32)

    with f.open("rb") as fp:
        while (b := fp.read(256)):
            for i in range(len(b)):
                counts[b[i]] += 1
                tot += 1

    probs = counts / tot
    ent = -1 * (probs * np.log2(np.where(probs == 0, np.ones(1), probs))).sum()
    if ent == 0: ent = -1 * ent

    print(f"Entropy per byte: {ent} bits or {ent / 8} bytes")
    print(f"Entropy of file: {ent * tot} bits or {ent * tot / 8} bytes")
    print(f"Size of file: {tot} bytes")

    if len(argv) > 2 and argv[2] == "--bit-level":
        bit_counts = np.zeros(8, dtype=np.uint32)
        for i in range(len(counts)):
            for j in range(8):
                bit_counts[j] += (i & (1 << j)) > 0

        bit_probs = bit_counts / tot
        bit_ent = -1 * (bit_probs * np.log2(np.where(bit_probs == 0, np.ones(1), bit_probs))).sum()
        if bit_ent == 0: bit_ent = -1 * bit_ent

        print(f"Bit-level entropy: {bit_ent} bits or {bit_ent} bits per byte")

if __name__ == "__main__":
    main()
