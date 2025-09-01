#!/usr/bin/env python3
import sys
import os
import argparse

def RC4(key, data):
    S = list(range(256))  # In Python 3, `range()` returns an iterator, so we use `list()`
    j = 0
    out = bytearray()

    # KSA Phase
    for i in range(256):
        j = (j + S[i] + ord(key[i % len(key)])) % 256
        S[i], S[j] = S[j], S[i]

    # PRGA Phase
    i = j = 0
    for char in data:
        i = (i + 1) % 256
        j = (j + S[i]) % 256
        S[i], S[j] = S[j], S[i]
        out.append(char ^ S[(S[i] + S[j]) % 256])
    return out

def get_raw_bytes(filename, offset=0):
    with open(filename, "rb") as fo:
        fo.seek(offset, 0)
        data = fo.read()
    return data

def save_raw_bytes(filename, data):
    with open(filename, "wb") as fo:
        fo.write(data)

def main():
    parser = argparse.ArgumentParser(description="RC4 Encoder/Decoder")
    parser.add_argument('--infile', dest="infile", default=None, help="Input file")
    parser.add_argument('--outfile', dest="outfile", default="out.tmp", help="Output file")
    parser.add_argument('--key', dest="key", default="test", help="Key")
    args = parser.parse_args()

    key = args.key
    raw = None

    if args.infile is None:
        # Read message from stdin
        print("Enter a message:")
        raw = input()  # `raw_input()` was replaced with `input()` in Python 3
    else:
        filename = args.infile
        raw = get_raw_bytes(filename)
    
    print("Data length:", len(raw))

    output = RC4(key, raw)

    save_raw_bytes(args.outfile, output)
    print("Output saved to:", args.outfile)

if __name__ == "__main__":
    main()
    