#!/usr/bin/env python

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
    def __init__( self, key ):
        self.key = key

    def encrypt( self, raw ):
        raw = pad(raw)
        iv = Random.new().read( AES.block_size )
        cipher = AES.new( self.key, AES.MODE_CBC, iv )
        return base64.b64encode( iv + cipher.encrypt( raw ) ) 

    def decrypt( self, enc ):
        enc = base64.b64decode(enc)
        iv = enc[:BS]
        cipher = AES.new(self.key, AES.MODE_CBC, iv )
        return unpad(cipher.decrypt( enc[BS:] ))
###

def scramble(key):
    md_str = hashlib.sha512(key).hexdigest()
    salt = hashlib.sha512(key[::-1]).hexdigest()

    key2 = str_to_bytesstr(md_str)
    key3 = str_to_bytesstr(key)
    extended_key = key2 + key3

    m = hashlib.pbkdf2_hmac('sha512', bytearray(extended_key), salt, 100000)
    start = 2
    key_len = 32
    result = m[start : (start + key_len)]
    return result

def str_to_bytesstr(string):
    bytes = list()
    for c in string:
        bytes.append(ord(c))
    return "".join("%02x" % b for b in bytes)

###

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

def make_outfile_name(filename, isDecode, sufix):
    prefix = "enc_"
    if isDecode:
        prefix = "dec_"
    try:
        dot_indx = filename.index('.')
    except:
        dot_indx = len(filename)
    return prefix + filename[:dot_indx] + "."+ sufix

def main():
    parser = argparse.ArgumentParser(description="AES Encoder/Decoder")
    parser.add_argument('--infile', dest="infile", default=None, help="Input file")
    parser.add_argument('--oext', dest="out_ext", default=None, help="Output extension")
    parser.add_argument('--decode', dest="decode", default=False, action='store_true', help="Decode or encode the given input?")
    args = parser.parse_args()

    key = getpass.getpass()
    key = scramble(key)

    if args.infile is None:
        #read message from stdin:
        outfile = None
        print "Enter a message:"
        raw = raw_input()
    else:
        filename = args.infile
        #prepare output name:
        if args.decode:
            if args.out_ext is None:
                print "Output extension is required!"
                return
            outfile = make_outfile_name(filename, args.decode, args.out_ext)
        else:
            outfile = make_outfile_name(filename, args.decode, "txt")
        raw = get_raw_bytes(filename)
    
    aes = AESCipher(key)
    if args.decode:
        output = aes.decrypt(raw)
    else:
        output = aes.encrypt(raw)
    if outfile:
        save_raw_bytes(outfile, output)
        print "[OK] Output: " + outfile
    else:
        print "---"
        print output
        print "---"

if __name__ == "__main__":
    main()

