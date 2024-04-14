import sys
import pathlib as pt
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

def calculate_byte_entropy(counts, total):
    probs = counts / total
    entropy = -1 * (probs * np.log2(np.where(probs == 0, np.ones(1), probs))).sum()
    return entropy

def calculate_bit_entropy(counts, total):
    probs = counts / (total * 8)  # Total bits = total bytes * 8
    entropy = -1 * (probs * np.log2(np.where(probs == 0, np.ones(1), probs))).sum()
    return entropy

def main(argv=sys.argv):
    if len(argv) == 1:
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

    byte_entropy = calculate_byte_entropy(counts, tot)
    bit_entropy = calculate_bit_entropy(counts, tot)

    print("Entropy per byte: ", byte_entropy, "bits or", byte_entropy / 8, "bytes")
    print("Entropy per bit: ", bit_entropy, "bits")
    print("Entropy of file: ", byte_entropy * tot, "bits or", byte_entropy * tot / 8, "bytes")
    print("Size of file: ", tot, "bytes")

if __name__ == "__main__":
    main()
