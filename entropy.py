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

    return LUT.__getitem__ # fastest way to count bits in a byte

bitcount = _cl_co()

def main(argv=sys.argv):
    if len(argv) < 2:
        print("Usage: python script.py <file> <entropy_type>")
        print("<entropy_type>: 'byte' or 'bit'")
        return

    entropy_type = argv[2].lower() if len(argv) >= 3 else 'byte'

    if entropy_type not in ['byte', 'bit']:
        print("Invalid entropy type. Please choose 'byte' or 'bit'.")
        return

    f = pt.Path(argv[1])

    tot = 0
    counts = np.zeros(256, dtype=np.uint32)
    with f.open("rb") as fp:
        while (b := fp.read(256)):
            for i in range(len(b)):
                counts[b[i]] += 1
                tot += 1

    if entropy_type == 'byte':
        probs = counts / tot
        ent = -1 * (probs * np.log2(np.where(probs == 0, np.ones(1), probs))).sum()
    else:  # Calculate bit-level entropy
        h = 0
        for i in range(len(b)):
            h += bitcount(b[i])
        p1 = h / (tot * 8)
        p0 = (tot * 8 - h) / (tot * 8)
        ent = p1 * np.log2(1 / p1) + p0 * np.log2(1 / p0)

    if ent == 0: ent = -1 * ent
    print("Entropy: ", ent, "bits" if entropy_type == 'bit' else "bytes")
    print("Size of file: ", tot, "bytes")

if __name__ == "__main__":
    main()
