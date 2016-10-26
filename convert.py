#!/usr/bin/env python
"""convert.py: Fetches bytes represented as ASCII numbers - hex or dec and converts them to binary"""

__author__ = 'hasherezade'
__license__ = "GPL"

import os
import sys
import re
import argparse

HEX_BYTE = r'[0-9a-fA-F]{2}\s'
DEC_BYTE = r'[0-9]{1,3}\s'

def chunks(s, n):
    for start in range(0, len(s), n):
        yield s[start:start+n]

def fetch_chunks(buf, is_dec, is_cont):
    pattern = HEX_BYTE
    if is_dec:
        pattern = DEC_BYTE

    if is_cont == False:
        return re.findall (pattern, buf)
    t = []
    chunk_len = 2
    if is_dec:
       chunk_len = 3
    for chunk in chunks(buf, chunk_len):
       t.append(chunk)
    return t


def convert_chunks(buf, is_dec, is_cont):
    base = 16
    if is_dec:
        base = 10
    buf = buf.strip()
    t = fetch_chunks(buf, is_dec, is_cont)
    byte_buf = []
    for chunk in t:
        num = int (chunk, base)
        byte_buf.append(num)
    return byte_buf

def main():
    parser = argparse.ArgumentParser(description="Byte converter")
    parser.add_argument('--infile', dest="infile", default=None, help="Input file", required=True)
    parser.add_argument('--outfile', dest="outfile", default="out.tmp", help="Output file")
    parser.add_argument('--is_cont', dest="is_cont", default=False, help="Is it a continuous string? (if False: delimiter separated)", action='store_true')
    parser.add_argument('--is_dec', dest="is_dec", default=False, help="Is byte represented by a decimal numer? (If False: hexadecimal)", action='store_true')
    args = parser.parse_args()

    in_fileName = args.infile
    out_fileName = args.outfile
    byte_buf = None
    with open(in_fileName, "r") as fileIn:
        buf = fileIn.read()
        byte_buf = convert_chunks(buf, args.is_dec, args.is_cont)
    
    if len(byte_buf) == 0:
        print "Parsing error"
        exit (-1)
    
    byte_arr = bytearray(byte_buf)
    with open(out_fileName, "wb") as fileOut:
        fileOut.write(byte_arr)
        print "Saved to a file: " + out_fileName

if __name__ == "__main__":
    sys.exit(main())

