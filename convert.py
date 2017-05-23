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
BIN_BYTE = r'[0-1]{8}\s'

def chunks(s, n):
    for start in range(0, len(s), n):
        yield s[start:start+n]

def fetch_chunks(buf, base, is_cont):
    pattern = HEX_BYTE
    chunk_len = 2
    if base == 10:
        pattern = DEC_BYTE
        chunk_len = 3
    elif base == 2:
        pattern = BIN_BYTE
        chunk_len = 8

    if is_cont == False:
        return re.findall (pattern, buf)
    t = []
    for chunk in chunks(buf, chunk_len):
       t.append(chunk)
    return t


def convert_chunks(buf, base_id, is_cont):
    base = 16
    if base_id == 'd':
        base = 10
    elif base_id == 'b':
        base = 2
    buf = buf.strip()
    t = fetch_chunks(buf, base, is_cont)
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
    parser.add_argument('--base', dest="base_id", default='h', help="Number base. Supported: b - binary, d - decimal, h -hexadecimal.", required=True)
    args = parser.parse_args()

    in_fileName = args.infile
    out_fileName = args.outfile
    byte_buf = None
    with open(in_fileName, "r") as fileIn:
        buf = fileIn.read()
        byte_buf = convert_chunks(buf, args.base_id, args.is_cont)
    
    if len(byte_buf) == 0:
        print "Parsing error"
        exit (-1)
    
    byte_arr = bytearray(byte_buf)
    with open(out_fileName, "wb") as fileOut:
        fileOut.write(byte_arr)
        print "Saved to a file: " + out_fileName

if __name__ == "__main__":
    sys.exit(main())

