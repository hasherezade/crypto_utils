#!/usr/bin/env python2.7
import sys
import os
import argparse

def RC4(key, data):
    S = range(256)
    j = 0
    out = bytearray()

    #KSA Phase
    for i in range(256):
        j = (j + S[i] + ord( key[i % len(key)] )) % 256
        S[i] , S[j] = S[j] , S[i]

    #PRGA Phase
    i = j = 0
    for char in data:
        i = ( i + 1 ) % 256
        j = ( j + S[i] ) % 256
        S[i] , S[j] = S[j] , S[i]
        out.append(chr(ord(char) ^ S[(S[i] + S[j]) % 256]))
    return out

def get_raw_bytes(filename, offset=0):
    fo = open(filename,"rb")
    fo.seek(offset, 0)
    data = fo.read()
    fo.close()
    return data

def save_raw_bytes(filename, data):
    fo = open(filename,"wb")
    fo.write(data)
    fo.close()

def main():
    parser = argparse.ArgumentParser(description="RC4 Encoder/Decoder")
    parser.add_argument('--infile', dest="infile", default=None, help="Input file")
    parser.add_argument('--outfile', dest="outfile", default="out.tmp", help="Output file")
    parser.add_argument('--key', dest="key", default="test", help="Key")
    args = parser.parse_args()

    key = args.key
    raw = None

    if args.infile is None:
        #read message from stdin:
        print "Enter a message:"
        raw = raw_input()
    else:
        filename = args.infile
        raw = get_raw_bytes(filename)
    print "Data length: ", len(raw)

    output = RC4(key, raw)

    save_raw_bytes(args.outfile, output)
    print "Output saved to: " + args.outfile

if __name__ == "__main__":
    main()

