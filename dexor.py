#!/usr/bin/python

import argparse

def decode(data, key, offset):
    maxlen = len(data)
    keylen = len(key)
    j = 0 #key index
    decoded = bytearray()
    for i in range(offset, maxlen):
        dec = data[i] ^ key[j % keylen]
        j += 1
        decoded.append(dec) 
    return decoded

def main():
    parser = argparse.ArgumentParser(description="Data XOR")
    parser.add_argument('--file', dest="file", default=None, help="Input file", required=True)
    parser.add_argument('--key', dest="key", default=None, help="Value with which to XOR", required=True)
    parser.add_argument('--offset',dest="offset", default=0,type=int, help="Offset in file from which XOR should start")
    args = parser.parse_args()

    data = bytearray(open(args.file, 'rb').read())
    key = bytearray(args.key)
    offset = args.offset
    
    print decode(data, key, offset)


if __name__ == "__main__":
    main()
