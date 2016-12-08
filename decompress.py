#!/usr/bin/env python2.7
"""decompress.py: Zlib compressor/decompresso"""

__author__ = 'hasherezade'
__license__ = "GPL"

import sys
import os, argparse
import zlib

def getfilebytes(filename,offset=0):
    """
        Get bytes from source file
    """
    fo = open(filename,"rb")
    fo.seek(offset,0) #seek from current file position
    data = fo.read()
    fo.close()
    return (len(data),data)

def get_raw_bytes(filename):
    filesize = os.path.getsize(filename)
    (bytesread,rawbytes) = getfilebytes(filename)
    return rawbytes

###

def save_decoded(decdata, outfile):
    fr = open(outfile, "wb")
    if fr is None:
        return False
    for a in decdata:
        fr.write('%c' % a)
    fr.close()
    return True

def main():
    parser = argparse.ArgumentParser(description="Zlib compressor/decompressor")
    parser.add_argument('--infile', dest="infile", default=None, help="Input file", required=True)
    parser.add_argument('--outfile', dest="outfile", default=None, help="Output file")
    parser.add_argument('--decode', dest="decode", default=False, help="Decode the given file?", action='store_true')
    args = parser.parse_args()

    filename = args.infile
    outfile = args.outfile

    if outfile is None:
        outfile = "out.bin"

    print "Input: " + filename
    print "Output: " + outfile
    rawbytes = get_raw_bytes(filename)

    if args.decode:
        print "[+] Decompressing..."
        outdata = zlib.decompress(rawbytes)
    else:
        print "[+] Compressing..."
        outdata = zlib.compress(rawbytes)

    if save_decoded(outdata, outfile):
        print "[+] Saved to: " + outfile
    else:
        print "[-] Error: cannot write to file: " + outfile

if __name__ == "__main__":
    main()
