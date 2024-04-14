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

    # Check if bit-level entropy calculation is requested
    calculate_bit_level_entropy = False
    if len(argv) > 2 and argv[2] == "--bit-level":
        calculate_bit_level_entropy = True

    f = pt.Path(argv[1])

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
                counts[b[i]] += 1
                tot += 1

    probs = counts / tot

    if calculate_bit_level_entropy:
        bit_entropy = -1 * (probs * np.log2(np.where(probs == 0, np.ones(1), probs)))
        total_bit_entropy = bit_entropy.sum()
        print("Bit-level entropy: ", total_bit_entropy, "bits")

    byte_entropy = -1 * (probs * np.log2(np.where(probs == 0, np.ones(1), probs))).sum()
    if byte_entropy == 0: byte_entropy = -1 * byte_entropy
    print(probs)
    print(counts)
    print("Entropy per byte: ", byte_entropy, "bits or", byte_entropy / 8, "bytes")
    print("Entropy of file: ", byte_entropy * tot, "bits or", byte_entropy * tot / 8, "bytes")
    print("Size of file: ", tot, "bytes")
    print("Delta: ", tot - byte_entropy * tot / 8, "bytes compressible theoretically")
    print("Best Theoretical Coding ratio: ", 8 / byte_entropy)

if __name__ == "__main__":
    main()
