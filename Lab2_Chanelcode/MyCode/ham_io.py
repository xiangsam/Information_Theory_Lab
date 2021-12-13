# -*- coding: utf-8 -*-
#! /usr/bin/python3

import argparse
import sys
from hamming_15_11_v2 import Ham_15_11

if __name__ == '__main__':
    exampleText = '''Example:
    python3 ham_io -e
    python3 ham_io -d
    '''
    parser = argparse.ArgumentParser(prog = 'ham_io', usage='%(prog)s [OPTION]...',
                                     description='use hamming channel code to encode and decode the stdio binarray string\n'+exampleText,
                                     epilog='only support read standard input and write standard output.',
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    
    parser.add_argument('-e', '--encode', default= False, action='store_true', help='encode stdin')
    parser.add_argument('-d', '--decode', default=False, action='store_true', help='decode stdout')
    args = parser.parse_args()
    if args.encode:
        ham = Ham_15_11()
        buf = []
        f = sys.stdin
        for line in f:
            line = line.replace('\n','')
            for e in line:
                if not (e=='1' or e == '0'):
                    raise TypeError("wish only '1', '0', but %s get" % e)
                buf.append(e)
                if len(buf) == 11:
                    ham.updateSourceCode(''.join(str(e) for e in buf))
                    sys.stdout.write(ham.encode())
                    buf = []
        if len(buf) != 0:
            raise IndexError("Some input don't encode")

    if args.decode:
        ham = Ham_15_11()
        buf = []
        f = sys.stdin
        for line in f:
            line = line.replace('\n','')
            for e in line:
                if not (e=='1' or e == '0'):
                    raise TypeError("wish only '1', '0', but %s get" % e)
                buf.append(e)
                if len(buf) == 15:
                    ham.updateCodeRes(''.join(str(e) for e in buf))
                    sys.stdout.write(ham.decode())
                    buf = []
        if len(buf) != 0:
            raise IndexError("Some input don't decode")
