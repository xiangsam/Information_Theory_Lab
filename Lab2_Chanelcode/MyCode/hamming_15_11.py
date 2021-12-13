import numpy as np
from random import randint

class Ham_15_11:
    """
    The class is used for hamming code [15,11,3]
    """

    def __init__(self,sourceCode=None):
        self._H = np.matrix([[1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
                             [0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1],
                             [0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1],
                             [0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1]])
        self._G = np.matrix([[1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                             [1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                             [1, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
                             [1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0],
                             [0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0],
                             [1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0],
                             [0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0],
                             [1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0],
                             [0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0],
                             [1, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1]])
        self._sourceCode = sourceCode
        self._codeRes = None
    
    def updateSourceCode(self,sourceCode):
        if not isinstance(sourceCode, str):
            raise TypeError("sourceCode: expected string, but got %r" % type(sourceCode).__name__)
        assert len(sourceCode) == 11
        sourceCode = np.matrix([int(e) for e in list(sourceCode)])
        self._sourceCode = sourceCode

    def updateCodeRes(self, codeRes):
        if not isinstance(codeRes, str):
            raise TypeError("codeRes: expected string, but got %r" % type(codeRes).__name__)
        assert len(codeRes) == 15
        codeRes = np.matrix([int(e) for e in list(codeRes)])
        self._codeRes = codeRes
    
    def encode(self):
        codeRes = self._sourceCode * self._G % 2
        self._codeRes = codeRes
        codeRes = codeRes.tolist()[0]
        codeRes = ''.join([str(e) for e in codeRes])
        return codeRes

    def decode(self):
        z = self._H * self._codeRes.T % 2
        mul = np.matrix([1,2,4,8])
        error = (mul * z).sum()
        codeRes = self._codeRes.tolist()[0]
        if not error == 0:
            codeRes[error-1] = (codeRes[error-1]+1) % 2
        codeRes = codeRes[2:3]+codeRes[4:7] + codeRes[8:]
        return ''.join([str(e) for e in codeRes])

if __name__ == '__main__':
    ham = Ham_15_11()
    with open('hamming_15_11.txt','w') as f:
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
    
    #this part used to check decode
    with open('hamming_15_11.txt', 'r') as f:
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

    #this part used to simulate error and check decode
    with open('hamming_15_11.txt', 'r') as f:
        checkpoint = 0
        for line in f:
            codeRes = line.split(' ')[1].replace('\n','')
            codeRes = [int(e) for e in codeRes]
            errorP = randint(0, 14)
            codeRes[errorP] = (codeRes[errorP]+1) % 2
            codeRes = ''.join(str(e) for e in codeRes)
            ham.updateCodeRes(codeRes)
            expectedAns = line.split(',')[0]
            ans = ham.decode()
            if not ans == expectedAns:
                print('check failed in {} -> {},{} expected'.format(codeRes,ans,expectedAns))
                exit(-1)
            checkpoint += 1
        print('%d points checked, decode( with one error) test pass!!!' % checkpoint)


