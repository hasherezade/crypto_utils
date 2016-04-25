#!/usr/bin/env python
"""file2png.py: Visualise raw bytes of any given file and saves as a PNG"""

__author__ = 'hasherezade'
__license__ = "GPL"

import sys
import os
import math
import argparse
from PIL import Image

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

class ImageBuffer:
#private
    def _calcDimensions(self, size):
        #calculate pixel dimensiong for a square image
        unit = 3 #RGB
        pixelsCount = len(self.encbytes)/unit
        if self.w is None:
            self.w = int(math.ceil(math.sqrt(pixelsCount)))
            self.h = self.w #sqare
        else:
            self.h = pixelsCount / self.w
        self.padding  = int(((self.w * self.h) * unit) - size)

    def _appendPadding(self, stuffing):
        stuffingSize = len(stuffing)
        stuffingUnits = self.padding / stuffingSize
        stuffingRem = self.padding % stuffingSize
        print "Dif = %d, stuffing size = %d * %d + %d" % (self.padding, stuffingSize, stuffingUnits, stuffingRem)
        if self.padding == 0:
            return
        i = 0
        stuffing = stuffing * stuffingUnits
        self.encbytes += stuffing
        if stuffingRem == 0:
           return
        stuffing = stuffing[:stuffingRem]
        self.encbytes += stuffing

#public

    def __init__(self, rawbytes, width=None):
        self.encbytes = rawbytes
        self.w = width
        self._calcDimensions(len(rawbytes))
        self.printInfo()
        self._appendPadding('\0')

    def printInfo(self):
        print "width: " + str(self.w)
        print "height: " + str(self.h)
        print "Padding: " + str(self.padding)
        print "Finalsize: " + str(len(self.encbytes))

###

def encode(rawbytes):
    return rawbytes

def decode(encbytes):
    return encbytes

###

def save_image(imgBuffer, filename):
    imc = Image.frombuffer("RGB", (imgBuffer.w, imgBuffer.h), imgBuffer.encbytes,"raw","RGB",0,1)
    imc.save(filename)

def get_encoded_data(imgname):
    imo = Image.open(imgname)
    rawdata = list(imo.getdata())
    print "Len = %d\n" % len(rawdata)
    tsdata = ""
    for x in rawdata:
        for z in x:
            tsdata += chr(z)
    del rawdata
    return tsdata

def save_decoded(decdata, outfile):
    fr = open(outfile, "wb")
    for a in decdata:
        fr.write('%c' % a)
    fr.close()

def make_prefixed_name(name, prefix):
    index = name.rfind('/')
    if index == -1:
        index = name.rfind('\\')
    if index == -1:
        return prefix + name # simple append
    return name[:index+1]+prefix+name[index+1:]

def make_outfile_name(filename, suffix, prefix):
    filename = make_prefixed_name(filename, prefix)
    try:
        dot_indx = filename.index('.')
    except:
        dot_indx = len(filename)
    return filename[:dot_indx] + "."+ suffix

def main():
    parser = argparse.ArgumentParser(description="Bytes visualiser")
    parser.add_argument('--infile', dest="infile", default=None, help="Input file", required=True)
    parser.add_argument('--outfile', dest="outfile", default=None, help="Output file")
    parser.add_argument('--decode', dest="decode", default=False, help="Decode the given file?", action='store_true')
    parser.add_argument('--width', dest="width", default=None, help="Preffered width of the output image", type=int)
    args = parser.parse_args()

    filename = args.infile
    outfile = args.outfile
    prefix = "enc_"
    sufix = "png"
    if args.decode:
        prefix = "dec_"
        sufix = "out"

    if outfile is None:
        outfile = make_outfile_name(filename, sufix, prefix)

    print "Input: " + filename
    print "Output: " + outfile

    if args.decode == False:
        rawbytes = get_raw_bytes(filename)
        encodedbytes = encode(rawbytes)
        del rawbytes
        imagebuffer = ImageBuffer(encodedbytes, args.width)
        save_image(imagebuffer, outfile)
    else:
        tsdata = get_encoded_data(filename)
        decdata = decode(tsdata)
        print "decoded %d\n" % len(decdata)
        save_decoded(decdata, outfile)

if __name__ == "__main__":
    main()
