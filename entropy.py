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
        print("Provide one or more files")
        return

    total_entropy = 0
    total_size = 0

    for file_path in argv[1:]:
        f = pt.Path(file_path)

        if not f.exists():
            print(f"File {file_path} does not exist")
            continue

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

        print(f"Entropy per byte for {file_path}: ", ent, "bits or", ent / 8, "bytes")
        print(f"Entropy of file {file_path}: ", ent * tot, "bits or", ent * tot / 8, "bytes")
        print(f"Size of file {file_path}: ", tot, "bytes")
        print(f"Delta: ", tot - ent * tot / 8, "bytes compressable theoritically")
        print(f"Best Theoritical Coding ratio: ", 8 / ent)

        total_entropy += ent * tot
        total_size += tot

    print(f"Total entropy for all files: {total_entropy} bits or {total_entropy / 8} bytes")
    print(f"Total size for all files: {total_size} bytes")
    print(f"Average entropy per byte for all files: {total_entropy / total_size} bits")

if __name__ == "__main__":
    main()
