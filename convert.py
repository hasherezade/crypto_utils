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

def get_chunks(buf, is_hex):
    pattern = DEC_BYTE
    base = 10
    if is_hex:
        pattern = HEX_BYTE
        base = 16
    t = re.findall (pattern, buf)
    byte_buf = []
    for chunk in t:
        x = chunk
        num = int (x, base)
        byte_buf.append(num)
    return byte_buf

def main():
    parser = argparse.ArgumentParser(description="Byte converter")
    parser.add_argument('--infile', dest="infile", default=None, help="Input file", required=True)
    parser.add_argument('--outfile', dest="outfile", default="out.tmp", help="Output file")
    parser.add_argument('--is_hex', dest="is_hex", default=False, help="Is byte represented by a hexadecimal numer? (If no: decimal)", action='store_true')
    args = parser.parse_args()

    in_fileName = args.infile
    out_fileName = args.outfile
    byte_buf = None
    with open(in_fileName, "r") as fileIn:
        buf = fileIn.read()
        byte_buf = get_chunks(buf, args.is_hex)
    
    if len(byte_buf) == 0:
        print "Parsing error"
        exit (-1)
    
    byte_arr = bytearray(byte_buf)
    with open(out_fileName, "wb") as fileOut:
        fileOut.write(byte_arr)
        print "Saved to a file: " + out_fileName

if __name__ == "__main__":
    sys.exit(main())

