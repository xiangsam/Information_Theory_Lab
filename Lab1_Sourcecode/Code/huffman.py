# -*- coding: utf-8 -*-
#!/usr/bin/python2

import math
import os
import fileinput
import sys

def countFrequency(fname):
    """
    get the frequency of each byte
    """
    nodeDic = {}
    if isinstance(fname, list):#work for stdin/stdout part
        for e in fname:
            if e in nodeDic.keys():
                nodeDic[e] += 1
            else:
                nodeDic[e] = 1
        return sorted(nodeDic.items(), key = lambda x:x[1])
    with open(fname,'rb') as f:
        while True:
            byte = f.read(1)
            if not byte:
                break
            if byte in nodeDic.keys():
                nodeDic[byte] += 1
            else:
                nodeDic[byte] = 1
    return sorted(nodeDic.items(), key = lambda x:x[1])
    

class Node:
    """
    node of HuffmanTree
    """
    def __init__(self,name, value):
        self.name = name
        self.value = value
        self.left = None
        self.right = None
        self.code = ''


class HuffmanTree:
    def __init__(self, nodeDic):
        self.nodeList = [Node(e[0], e[1]) for e in nodeDic]
        self.nodeNum = len(nodeDic)
        self.codeTable = {}
        self.createTree()
        self.huffmanCode(self.nodeList[0])
    
    def push(self, node):
        if self.nodeNum == 0:
            self.nodeList = [node]
            self.nodeNum += 1
            return
        self.nodeNum += 1
        for i, e in enumerate(self.nodeList):
            if e.value > node.value:
                self.nodeList = self.nodeList[0:i] + [node] + self.nodeList[i:]
                return
        self.nodeList = self.nodeList+[node]
        return
    
    def pop(self):
        self.nodeNum -= 1
        return self.nodeList.pop(0)

    def createTree(self):
        while not self.nodeNum == 1:
            lnode = self.pop()
            rnode = self.pop()
            node = Node(None, lnode.value + rnode.value)
            node.left = lnode
            node.right = rnode
            self.push(node)
    
    def huffmanCode(self, node, code = ''):
        """
        Traverse huffman tree to encode the leaves
        """
        assert self.nodeNum == 1
        if node is None:
            return
        if node.left is None and node.right is None:
            node.code = code
            self.codeTable[node.name] = code
            return
        self.huffmanCode(node.left, code+'0')
        self.huffmanCode(node.right, code+'1')

    def printCodeTable(self):
        print(self.codeTable)

def encode(fname, foutname):
    """
    huffman encode: file to file
    """
    #build huffman tree and get codeTable
    nodeDic = countFrequency(fname)
    tree = HuffmanTree(nodeDic)
    codeTable = tree.codeTable
    headData = ''
    #write the nessesary information of huffman code dictionary for decode
    headData += chr(int(math.ceil(len(codeTable)/255.0))) #decide the number of bytes to store the length of codeTable
    temp = len(codeTable)
    for i in range(int(math.ceil(len(codeTable)/255.0))):
        headData += chr(temp & 0xff)
        temp = temp >> 8
    for key, value in codeTable.items():
        headData += key
        headData += chr(len(value)) #assert the length of huffman code <= 255
        for e in [value[8*i:8*i+8] for i in range(int(math.ceil(len(value)/8.0)))]:
            headData += chr(int(e,2))
    outlst = []
    with open(fname, 'rb') as f:
        fout = open(foutname, 'wb')
        data = f.read()
        fout.write(chr(0xff)) #magic number
        for e in data:
            outlst.append(codeTable[e])
        outData = ''.join(outlst)
        suffixZero = 8 - len(outData) % 8 #last byte also need to be 8 bits
        outData += '0'*suffixZero
        fout.write(chr(suffixZero))
        for e in headData:
            fout.write(e)
        outDataLen = len(outData)
        while outDataLen>0:
            fout.write(chr(int(outData[0:8], 2)))
            outData = outData[8:]
            outDataLen -= 8

def encode2():
    """
    huffman encode: stdin to stdout
    """
    inBuff = []
    outData = ''
    #f = fileinput.input(mode='rb')
    f = sys.stdin
    for line in f:
        for e in line:
            inBuff.append(e)
            if len(inBuff) == 1000:
                nodeDic = countFrequency(inBuff)
                tree = HuffmanTree(nodeDic)
                codeTable = tree.codeTable
                headData = ''
                headData += chr(int(math.ceil(len(codeTable)/255.0))) #decide the number of bytes to store the length of codeTable
                temp = len(codeTable)
                for i in range(int(math.ceil(len(codeTable)/255.0))):
                    headData += chr(temp & 0xff)
                    temp = temp >> 8
                for key, value in codeTable.items():
                    headData += key
                    headData += chr(len(value)) #assert the length of huffman code <= 255
                    for e in [value[8*i:8*i+8] for i in range(int(math.ceil(len(value)/8.0)))]:
                        headData += chr(int(e,2))
                outlst = []
                for ee in inBuff:
                    outlst.append(codeTable[ee])
                inBuff = []
                data = ''.join(outlst)
                suffixZero = 8 - len(data) % 8 #last byte also need to be 8 bits
                data += '0'*suffixZero
                outData = chr(suffixZero) + headData
                dataLen = len(data)
                while dataLen:
                    outData += chr(int(data[0:8], 2))
                    data = data[8:]
                    dataLen -= 8
                blockSize = len(outData) + 1 # one for magic number
                outData = chr((blockSize >> 8)&0xff) + chr(blockSize & 0xff)+chr(0xfe)+outData #use two bytes to store blockSize and one byte magic number
                sys.stdout.writelines(outData)
    if not len(inBuff) == 0: #the last inBuff if size < 1000
        nodeDic = countFrequency(inBuff)
        tree = HuffmanTree(nodeDic)
        codeTable = tree.codeTable
        headData = ''
        headData += chr(int(math.ceil(len(codeTable)/255.0)))
        temp = len(codeTable)
        for i in range(int(math.ceil(len(codeTable)/255.0))):
            headData += chr(temp & 0xff)
            temp = temp >> 8
        for key, value in codeTable.items():
            headData += key
            headData += chr(len(value)) #assert the length of huffman code <= 255
            for e in [value[8*i:8*i+8] for i in range(int(math.ceil(len(value)/8.0)))]:
                headData += chr(int(e,2))
        outlst = []
        for ee in inBuff:
            outlst.append(codeTable[ee])
        data = ''.join(outlst)
        suffixZero = 8 - len(data) % 8 #last byte also need to be 8 bits
        data += '0'*suffixZero
        outData = chr(suffixZero) + headData
        dataLen = len(data)
        while dataLen:
            outData += chr(int(data[0:8], 2))
            data = data[8:]
            dataLen -= 8
        blockSize = len(outData) + 1#one for magic number
        outData = chr((blockSize >> 8) & 0xff) + chr(blockSize & 0xff) +chr(0xfe) +outData
        sys.stdout.writelines(outData)
    return

def decode(fname, foutname):
    """
    huffman decode: file to file
    """
    fout = open(foutname, 'wb')
    with open(fname, 'rb') as f:
        #recover the huffman code dictionary
        data = list(f.read())
        assert ord(data.pop(0)) == 0xff #check magic number
        suffixZero = ord(data.pop(0))
        temp = ord(data.pop(0))
        codeTableLen = 0
        for i in range(temp):
            codeTableLen += ord(data.pop(0)) << (8*i) #get all bytes storing length information of codeTable
        codeTable = {}
        maxLength = -1
        for i in range(codeTableLen):
            key = data.pop(0)
            valueLen = ord(data.pop(0))
            maxLength = max(maxLength, valueLen)
            value = ''
            for j in range(int(math.ceil(valueLen/8.0))):
                byte = bin(ord(data.pop(0))).replace('0b','')
                if j == math.ceil(valueLen/8.0) - 1:
                    value += byte.zfill(8)[-(valueLen%8):]
                else:
                    value += byte.zfill(8)
            codeTable[key] = value
        invcodeTable = {value: key for key, value in codeTable.items()}
        codeData = ''
        for e in data:
            codeData += bin(ord(e)).replace('0b', '').zfill(8)
        if suffixZero != 0:
            codeData = codeData[:-suffixZero]
        codeDataLen = len(codeData)
        while codeDataLen:
            for i in range(1,min(codeDataLen+1,maxLength+1)):
                tmp = codeData[0:i]
                if tmp in invcodeTable.keys():
                    fout.write(invcodeTable[tmp])
                    codeData = codeData[i:]
                    codeDataLen -= i
                    break

def decode2():
    """
    huffman decode: stdin to stdout
    """
    inBuff = []
    blockSize = 0
    tempBlockSize = -2
    #f = fileinput.input(mode = 'rb')
    f = sys.stdin
    for line in f:
        for e in line:
            if tempBlockSize == -2:
                tempBlockSize += 1
                blockSize += ord(e)<<8
            elif tempBlockSize == -1:
                tempBlockSize += 1
                blockSize += ord(e)
            else:
                inBuff.append(e)
            if tempBlockSize == 0 and len(inBuff) == blockSize:
                data = inBuff
                inBuff = []
                blockSize = 0
                tempBlockSize = -2
                codeData = ''
                assert ord(data.pop(0)) == 0xfe
                suffixZero = ord(data.pop(0))
                temp = ord(data.pop(0))
                codeTableLen = 0
                for i in range(temp):
                    codeTableLen += ord(data.pop(0)) << (8*i)
                codeTable = {}
                maxLength = -1
                for i in range(codeTableLen):
                    key = data.pop(0)
                    valueLen = ord(data.pop(0))
                    maxLength = max(maxLength, valueLen)
                    value = ''
                    for j in range(int(math.ceil(valueLen/8.0))):
                        byte = bin(ord(data.pop(0))).replace('0b','')
                        if j == math.ceil(valueLen/8.0) - 1:
                            value += byte.zfill(8)[-(valueLen%8):]
                        else:
                            value += byte.zfill(8)
                    codeTable[key] = value
                invcodeTable = {value: key for key, value in codeTable.items()}
                for e in data:
                    codeData += bin(ord(e)).replace('0b', '').zfill(8)
                if suffixZero != 0:
                    codeData = codeData[:-suffixZero]
                codeDataLen = len(codeData)
                while codeDataLen:
                    for i in range(1,min(codeDataLen+1,maxLength+1)):
                        tmp = codeData[0:i]
                        if tmp in invcodeTable.keys():
                            sys.stdout.write(invcodeTable[tmp])
                            codeData = codeData[i:]
                            codeDataLen -= i
                            break
    return

if __name__ == '__main__':
    #encode('testfile1', 'testfile1.mz')
    #decode('testfile1.mz', 'testfile1.uz')
    #encode('temp', 'temp.mz')
    #decode('temp.mz', 'temp.uz')
    encode2()
    #decode2()
