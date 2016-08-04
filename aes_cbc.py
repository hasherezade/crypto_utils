#!/usr/bin/env python2.7

import sys
import os
import argparse
import base64
import hashlib
import getpass
from Crypto.Cipher import AES
from Crypto import Random

BS = 16
pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS) 
unpad = lambda s : s[:-ord(s[len(s)-1:])]

class AESCipher:
    def __init__( self, key, iv):
        self.key = key
        self.iv = iv

    def encrypt( self, raw ):
        raw = pad(raw)
        cipher = AES.new( self.key, AES.MODE_CBC, self.iv )
        return cipher.encrypt(raw)

    def decrypt( self, enc ):
        cipher = AES.new(self.key, AES.MODE_CBC, self.iv )
        return unpad(cipher.decrypt(enc))
###
def expand_key(key):
    while len(key) < BS:
        key = key + key
    return key[:BS]

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
    parser = argparse.ArgumentParser(description="AES ECB Encoder/Decoder")
    parser.add_argument('--infile', dest="infile", default=None, help="Input file")
    parser.add_argument('--outfile', dest="outfile", default="out.tmp", help="Output file")
    parser.add_argument('--key', dest="key", default="test", help="Key")
    parser.add_argument('--iv', dest="iv", default="test", help="Initialization vector")
    parser.add_argument('--decode', dest="decode", default=False, action='store_true', help="Decode or encode the given input?")
    args = parser.parse_args()
    
    key = expand_key(args.key)
    iv = expand_key(args.iv)
    print key

    if args.infile is None:
        #read message from stdin:
        outfile = None
        print "Enter a message:"
        raw = raw_input()
    else:
        filename = args.infile
        raw = get_raw_bytes(filename)
    print len(raw)

    aes = AESCipher(key, iv)
    if args.decode:
        output = aes.decrypt(raw)
    else:
        output = aes.encrypt(raw)
    
    outfile = args.outfile
    if outfile:
        save_raw_bytes(outfile, output)
        print "[OK] Output: " + outfile
    else:
        print "---"
        print output
        print "---"

if __name__ == "__main__":
    main()

