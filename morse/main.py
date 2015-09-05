#!/usr/bin/python
"Morse encoder/decoder with option of custom charset, CC-BY: hasherezade"

import argparse
from morse import *

def main():
    parser = argparse.ArgumentParser(description="Morse Encoder/Decoder")
    parser.add_argument('--charset', dest="charset", default='.- ', help="Charset in format: 'DitDashBreak', i.e '.- '")
    parser.add_argument('--decode', dest="decode", default=False, action='store_true', help="Decode or encode the given input?")
    args = parser.parse_args()
    
    m = Morse(args.charset)

    print "Enter a message:"
    raw = raw_input()

    if args.decode:
        print m.morse_dec(raw)
    else:
        print m.morse_enc(raw)

if __name__ == "__main__":
    main()
