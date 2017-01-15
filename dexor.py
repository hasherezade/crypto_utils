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

def save_decoded(decdata, outfile):
    fr = open(outfile, "wb")
    if fr is None:
        return False
    for a in decdata:
        fr.write('%c' % a)
    fr.close()
    return True

def main():
    parser = argparse.ArgumentParser(description="Data XOR")
    parser.add_argument('--file', dest="file", default=None, help="Input file", required=True)
    parser.add_argument('--outfile', dest="outfile", default="out.bin", help="Output file")
    parser.add_argument('--key', dest="key", default=None, help="Value with which to XOR")
    parser.add_argument('--keyfile', dest="keyfile", default=None, help="File with which to XOR")
    parser.add_argument('--offset',dest="offset", default=0,type=int, help="Offset in file from which XOR should start")
    args = parser.parse_args()


    data = bytearray(open(args.file, 'rb').read())
    if (args.key == None and args.keyfile == None):
        print "Supply key or keyfile"
        exit (-1)
    if args.keyfile:
        key = bytearray(open(args.keyfile, 'rb').read())
    else:
        key = bytearray(args.key)
    offset = args.offset

    decdata = decode(data, key, offset)
    save_decoded(decdata, args.outfile)

    print "Saved to: "+ args.outfile


if __name__ == "__main__":
    main()
