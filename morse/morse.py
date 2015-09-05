#!/usr/bin/python
"Morse encoder/decoder with option of custom charset, CC-BY: hasherezade"

class Morse:
#private:
    morse_map = { '01':'a', '1000':'b', '1010':'c', '100':'d', '0':'e', '0010':'f', '110':'g', '0000':'h',
                '00':'i','0111':'j','101':'k','0100':'l','11':'m','10':'n', '111':'o', '0110':'p',
                '1101':'q', '010':'r', '000':'s', '1':'t', '001':'u', '0001':'v', '011':'w','1001':'x',
                '1011':'y','1100':'z',
                '01111':'1', '00111':'2', '00011':'3', '00001':'4', '00000':'5', '10000':'6',  '11000':'7', '11100':'8', '11110':'9', '11111':'0', }

    BREAK_INDEX = 2

    def _makeReverseMap(self, inmap):
        outmap = {}
        for key in inmap.keys():
            val = inmap[key]
            outmap[val] = key
        return outmap

    def _mapInput(self, chunks, inmap):
        output = list()
        for chunk in chunks:
            if chunk in inmap.keys():
                output.append(inmap[chunk])
        return output

    def _splitchunk(self, string):
        splited = string.split(self.breakchar)
        return splited
    
    def _rawToCharset(self, chunk):
        if self.charset == None:
            return chunk
        outchunk = ""
        for c in chunk:
            num = ord(c) - ord('0')
            outchunk += self.charset[num]
        return outchunk

    def _charsetToRaw(self, chunk):
        if self.charset == None:
            return chunk
        outchunk = ""
        for c in chunk:
            index = self.charset.index(c)
            val = chr(index + ord('0'))
            outchunk += val
        return outchunk
    
    def _setCharset(self, chunks):
        out2 = list()
        for chunk in chunks:
            out2.append(self._rawToCharset(chunk))
        return out2

    def _unsetCharset(self, chunks):
        out2 = list()
        for chunk in chunks:
            out2.append(self._charsetToRaw(chunk))
        return out2

#public:
    def __init__( self, charset):
        self.rev_map = self._makeReverseMap(self.morse_map)
        self.charset = '.- '
        if charset:
            self.charset = charset
        self.breakchar = self.charset[self.BREAK_INDEX]

    def morse_dec(self, string):
        chunks = self._splitchunk(string)
        chunks = self._unsetCharset(chunks)
        output = self._mapInput(chunks, self.morse_map)
        return "".join(output)

    def morse_enc(self, string):
        string = string.lower()
        output = self._mapInput(string, self.rev_map)
        out2 = self._setCharset(output)
        return  self.breakchar.join(out2)


