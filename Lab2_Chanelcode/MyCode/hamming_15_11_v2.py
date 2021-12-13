# -*- coding: utf-8 -*-
#! /usr/bin/python3

from random import randint

class Ham_15_11:
    def __init__(self):
        self._sourceCode = None
        self._codeRes = None
    
    def updateSourceCode(self,sourceCode):
        if not isinstance(sourceCode, str):
            raise TypeError("sourceCode: expected string, but got %r" % type(sourceCode).__name__)
        assert len(sourceCode) == 11
        sourceCode = [int(e) for e in list(sourceCode)]
        self._sourceCode = sourceCode

    def updateCodeRes(self, codeRes):
        if not isinstance(codeRes, str):
            raise TypeError("codeRes: expected string, but got %r" % type(codeRes).__name__)
        assert len(codeRes) == 15
        codeRes = [int(e) for e in list(codeRes)]
        self._codeRes = codeRes

    def encode(self):
        assert isinstance(self._sourceCode, list)
        sourceCode = self._sourceCode
        codeRes = [0,0,sourceCode[0], 0, sourceCode[1],sourceCode[2],sourceCode[3],0]
        codeRes += sourceCode[4:]
        b = 0
        for i, e in enumerate(codeRes):
            pos = i+1
            if not e == 0:
                b ^= pos
        codeRes[0] = b & 0b1
        codeRes[1] = (b >> 1) & 0b1
        codeRes[3] = (b >> 2) & 0b1
        codeRes[7] = (b >> 3) & 0b1
        return ''.join(str(e) for e in codeRes)

    def decode(self):
        assert isinstance(self._codeRes, list)
        codeRes = self._codeRes
        b = 0
        for i, e in enumerate(codeRes):
            pos = i + 1
            if not e == 0:
                b ^= pos
        if not b == 0:
            codeRes[b-1] = (codeRes[b-1]+1) % 2
        sourceCode = codeRes[2:3]+codeRes[4:7]+codeRes[8:]
        return ''.join(str(e) for e in sourceCode)

if __name__ == '__main__':
    ham = Ham_15_11()
    with open('hamming_15_11_v2.txt','w') as f:
        for i in range(2**11):
            sourceCode = bin(i).replace('0b','').rjust(11,'0')
            sourceCode = sourceCode[::-1]
            ham.updateSourceCode(sourceCode)
            codeRes = ham.encode()
            line = ''.join([sourceCode,', ',codeRes,'\n'])
            if i == 2**11-1:
                line=line[:-1]
            f.write(line)
        f.close()

    #this part is uesd to check decode
    with open('hamming_15_11_v2.txt', 'r') as f:
        checkpoint = 0
        for line in f:
            codeRes = line.split(' ')[1].replace('\n','')
            ham.updateCodeRes(codeRes)
            expectedAns = line.split(',')[0]
            ans = ham.decode()
            if not ans == expectedAns:
                print('check failed in {} -> {},{} expected'.format(codeRes,ans,expectedAns))
                exit(-1)
            checkpoint += 1
        print('%d points checked, decode test pass!!!' % checkpoint)
        f.close()

    #this part is used to simulate error and check decode
    with open('hamming_15_11_v2.txt', 'r') as f:
        checkpoint = 0
        for line in f:
            codeRes = line.split(' ')[1].replace('\n','')
            codeRes = [int(e) for e in codeRes]
            errorP = randint(0, 14)
            codeRes[errorP] = (codeRes[errorP] + 1) % 2
            codeRes = ''.join(str(e) for e in codeRes)
            ham.updateCodeRes(codeRes)
            expectedAns = line.split(',')[0]
            ans = ham.decode()
            if not ans == expectedAns:
                print('check failed in {} -> {},{} expected'.format(codeRes,ans,expectedAns))
                exit(-1)
            checkpoint += 1
        print('%d points checked, decode(with one error) test pass!!!' % checkpoint)

