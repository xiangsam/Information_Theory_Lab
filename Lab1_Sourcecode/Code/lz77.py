# -*- coding: utf-8 -*-
#! /usr/bin/python2

import fileinput
import sys

class LZ77:
    """
    if match string, then use(1, distance<12 bits>, length<4 bits>) to replace
    else, use (0, char<8 bits>) to replace
    """
    def __init__(self):
        self.windowSize = 4095 #the max number for 12 bits(index: 0 -> 4095)
        self.lookAheadBufferSize = 15  #the max number for 4 bits(len: 1 -> 15)
    
    def findMaxPrefix(self, data, cursor):
        windowBegin = 0
        windowEnd = 0
        if cursor == 0:
            return None
        if cursor <= self.windowSize:
            windowBegin = 0
            windowEnd = cursor-1
        else:
            windowBegin = cursor-self.windowSize-1
            windowEnd = cursor-1
        lookEnd = 0
        if len(data) - cursor < self.lookAheadBufferSize:
            lookEnd = len(data)-1
        else:
            lookEnd = cursor + self.lookAheadBufferSize -1
        prefix = [0,0,0]
        for i in range(cursor, lookEnd+1):
            tmp = data[cursor:i+1]
            if tmp in data[windowBegin:windowEnd+1]:
                index = data[windowBegin:windowEnd+1].index(tmp)
                prefix[0] = 1
                prefix[1] = windowEnd-(windowBegin+index)
                prefix[2] = i-cursor+1
                continue
            break
        if prefix[0] == 0: # not match
            return None
        return prefix
    
    def encode(self, fname, foutname):
        """
        lz77 encode: file to file
        """
        fout = open(foutname, 'wb')
        with open(fname, 'rb') as f:
            data = f.read()
            binarystr = ''
            i = 0
            while i < len(data):
                prefix = self.findMaxPrefix(data, i)
                if prefix is None: # only <0, code(8 bits)>
                    binarystr += '0'+bin(ord(data[i])).replace('0b','').zfill(8)
                    i += 1
                else: #need to store (1, distance<12 bits>, length<4 bits>)
                    binarystr += '1'+bin(prefix[1]).replace('0b','').zfill(12) + bin(prefix[2]).replace('0b', '').zfill(4)
                    i += prefix[2]
                while len(binarystr) >= 8:
                    fout.write(chr(int(binarystr[0:8],2)))
                    binarystr = binarystr[8:]
        while len(binarystr) > 0:
            binarystr = binarystr + '0'*(8-len(binarystr))
            fout.write(chr(int(binarystr[0:8],2)))
            binarystr = binarystr[8:]
    
    def encode2(self):
        """
        lz77 encode: stdin to stdout
        """
        #f = fileinput.input(mode='rb')
        f = sys.stdin
        inBuff = []
        data = ''
        outData = ''
        for line in f:
            for e in line:
                inBuff.append(e)
                if len(inBuff) == 1000:
                    data = ''.join(inBuff)
                    inBuff = []
                    binarystr = ''
                    outData = ''
                    i = 0
                    while i < len(data):
                        prefix = self.findMaxPrefix(data, i)
                        if prefix is None: # only <0, code(8 bits)>
                            binarystr += '0'+bin(ord(data[i])).replace('0b','').zfill(8)
                            i += 1
                        else: #need to store (1, distance<12 bits>, length<4 bits>)
                            binarystr += '1'+bin(prefix[1]).replace('0b','').zfill(12) + bin(prefix[2]).replace('0b', '').zfill(4)
                            i += prefix[2]
                        while len(binarystr) >= 8:
                            outData += chr(int(binarystr[0:8],2))
                            binarystr = binarystr[8:]
                    while len(binarystr) > 0:
                        binarystr = binarystr + '0'*(8-len(binarystr))
                        outData += chr(int(binarystr[0:8],2))
                        binarystr = binarystr[8:]
                    blockSize = len(outData)
                    outData = chr((blockSize >> 8) & 0xff) + chr(blockSize & 0xff) + outData
                    sys.stdout.write(outData)
        if len(inBuff) > 0: # the last block
            data = ''.join(inBuff)
            inBuff = []
            binarystr = ''
            outData = ''
            i = 0
            while i < len(data):
                prefix = self.findMaxPrefix(data, i)
                if prefix is None: # only <0, code(8 bits)>
                    binarystr += '0'+bin(ord(data[i])).replace('0b','').zfill(8)
                    i += 1
                else: #need to store (1, distance<12 bits>, length<4 bits>)
                    binarystr += '1'+bin(prefix[1]).replace('0b','').zfill(12) + bin(prefix[2]).replace('0b', '').zfill(4)
                    i += prefix[2]
                while len(binarystr) >= 8:
                    outData += chr(int(binarystr[0:8],2))
                    binarystr = binarystr[8:]
            while len(binarystr) > 0:
                binarystr = binarystr + '0'*(8-len(binarystr))
                outData += chr(int(binarystr[0:8],2))
                binarystr = binarystr[8:]
            blockSize = len(outData)
            outData = chr((blockSize >> 8) & 0xff) + chr(blockSize & 0xff) + outData
            sys.stdout.write(outData)

    def decode(self, fname, foutname):
        """
        lz77 decode: file to file
        """
        datalst = []
        with open(fname, 'rb') as f:
            while True:
                byte = f.read(1)
                if not byte:
                    break
                datalst.append(bin(ord(byte)).replace('0b','').zfill(8))
        data = ''.join(datalst)
        out = []
        dataLen = len(data)
        while dataLen >= 9:
            mode = int(data[0])
            data = data[1:]
            dataLen -= 1
            if mode == 0: #mode == 0: <0, code(8 bits)>
                byte = chr(int(data[0:8],2))
                out.append(byte)
                data = data[8:]
                dataLen -= 8
            else: # mode == 1: (1, distance<12 bits>, length<4 bits>)
                distance = int(data[0:12],2)
                length = int(data[12:16], 2)
                data = data[16:]
                dataLen -= 16
                for i in range(length):
                    out.append(out[-distance-1])
        out_data = ''.join(out)
        with open(foutname, 'wb') as f:
            f.write(out_data)

    def decode2(self):
        """
        lz77 decode: stdin to stdout
        """
        blockSize = 0
        tempBlockMark = -2
        inBuff = []
        #f = fileinput.input(mode = 'rb')
        f = sys.stdin
        for line in f:
            for e in line:
                if tempBlockMark == -2:
                    tempBlockMark += 1
                    blockSize = ord(e) << 8
                elif tempBlockMark == -1:
                    tempBlockMark += 1
                    blockSize += ord(e)
                else:
                    inBuff.append(e)
                    if tempBlockMark == 0 and len(inBuff) == blockSize:
                        for i, e in enumerate(inBuff):
                            inBuff[i] = bin(ord(e)).replace('0b','').zfill(8)
                        tempBlockMark = -2
                        blockSize = 0
                        data = ''.join(inBuff)
                        inBuff = []
                        out = []
                        dataLen = len(data)
                        while dataLen >= 9:
                            mode = int(data[0])
                            data = data[1:]
                            dataLen -= 1
                            if mode == 0:
                                byte = chr(int(data[0:8],2))
                                out.append(byte)
                                data = data[8:]
                                dataLen -= 8
                            else:
                                distance = int(data[0:12],2)
                                length = int(data[12:16], 2)
                                data = data[16:]
                                dataLen -= 16
                                for i in range(length):
                                    out.append(out[-distance-1])
                        out_data = ''.join(out)
                        sys.stdout.write(out_data)

if __name__ == '__main__':
    #LZ77().encode('temp', 'temp.mz')
    #LZ77().decode('temp.mz', 'temp.uz')
    LZ77().decode2()
