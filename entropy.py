import sys
import pathlib as pt
import numpy as np

def calculate_byte_entropy(file_path):
    tot = 0
    counts = np.zeros(256, dtype=np.uint32)
    with open(file_path, "rb") as fp:
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
    ent = -1 * (probs * np.log2(np.where(probs == 0, np.ones(1), probs))).sum()
    if ent == 0: ent = -1 * ent
    return ent, tot

def calculate_bit_entropy(file_path):
    tot = 0
    counts = np.zeros(2, dtype=np.uint32)  # 0 and 1 counts
    with open(file_path, "rb") as fp:
        while (b := fp.read(1)):
            byte_val = int.from_bytes(b, byteorder="big")
            for i in range(8):
                bit_val = (byte_val >> i) & 1
                counts[bit_val] += 1
                tot += 1

    probs = counts / tot
    ent = -1 * (probs * np.log2(np.where(probs == 0, np.ones(1), probs))).sum()
    if ent == 0: ent = -1 * ent
    return ent, tot

def main(argv=sys.argv):
    if len(argv) < 3:
        print("Provide 'byte' or 'bit' and file paths as arguments")
        return

    mode = argv[1]
    if mode not in ['byte', 'bit']:
        print("Invalid mode. Choose 'byte' or 'bit'")
        return

    for file_path in argv[2:]:
        file_path = pt.Path(file_path)
        if mode == 'byte':
            ent, tot = calculate_byte_entropy(file_path)
            print("Byte-level entropy for", file_path.name, ":", ent, "bits or", ent / 8, "bytes")
            print("Byte-level entropy of", file_path.name, ":", ent * tot, "bits or", ent * tot / 8, "bytes")
            print("Size of", file_path.name, ":", tot, "bytes")
            print("Delta for", file_path.name, ":", tot - ent * tot / 8, "bytes compressible theoretically")
            print("Best Theoretical Coding ratio for", file_path.name, ":", 8 / ent)
            print()
        else:
            ent, tot = calculate_bit_entropy(file_path)
            print("Bit-level entropy for", file_path.name, ":", ent, "bits")
            print("Bit-level entropy of", file_path.name, ":", ent * tot, "bits")
            print("Size of", file_path.name, ":", tot, "bits")
            print("Delta for", file_path.name, ":", tot - ent * tot, "bits compressible theoretically")
            print("Best Theoretical Coding ratio for", file_path.name, ":", 1 / ent)
            print()

if __name__ == "__main__":
    main()
