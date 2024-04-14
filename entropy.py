import sys
import argparse
from pathlib import Path
from collections import Counter
from math import log2


def bitcount(i):
    return bin(i).count('1')


def main(argv=sys.argv):
    parser = argparse.ArgumentParser(
        description='Calculate the entropy of a file')
    parser.add_argument('file', type=str, help='Path to the input file')
    parser.add_argument('choice', type=str,
                        help='Calculation method: "byte" or "bit"')
    args = parser.parse_args(argv[1:])

    file_path = Path(args.file)

    if not file_path.exists():
        print("File not found")
        return

    total_bytes = 0
    byte_counts = Counter()
    total_bits_set = 0

    with file_path.open("rb") as file:
        for chunk in iter(lambda: file.read(256), b''):
            for byte in chunk:
                byte_counts[byte] += 1
                total_bits_set += bitcount(byte)
                total_bytes += 1

    if args.choice == "byte":
        probs = [count / total_bytes for count in byte_counts.values()]
        entropy = -sum(p * log2(p) for p in probs if p != 0)
        print(f"Entropy per byte: {entropy} bits or {entropy / 8} bytes")
        print(
            f"Entropy of file: {entropy * total_bytes} bits or {entropy * total_bytes / 8} bytes")

    elif args.choice == "bit":
        p1 = total_bits_set / (total_bytes * 8)
        p0 = 1 - p1
        entropy = p1 * (log2(total_bytes * 8) - log2(total_bits_set)) + p0 * \
            (log2(total_bytes * 8) - log2((total_bytes * 8) - total_bits_set))
        print(f"Informational entropy per bit: {entropy} bits")
        print(f"Entropy per byte: {entropy * 8} bits")
        print(f"Entropy of entire file: {entropy * total_bytes * 8} bits")


if _name_ == "_main_":
    main()
