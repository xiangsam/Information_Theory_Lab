import argparse
import os
import sys
sys.path.append('..')
from Code import huffman
from Code.lz77 import LZ77

if __name__ == '__main__':
    exampleText ='''Example:
  cat file | python2 myzip.py
  cat file.mz | python2 myzip.py -d
  python2 myzip.py file1 file2
  python2 myzip.py -d file1.mz file2.mz
    '''
    parser = argparse.ArgumentParser(prog = 'myzip', usage='%(prog)s [OPTION]... [FILE]...',
                                     description='Compress or uncompress files using huffman  and LZ77\nthe compress file will end with .mz, and the uncompress file will end with .uz\n'+exampleText,
                                     epilog='With no FILE, or when FILE is -, read standard input.',
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('-f','--file', type=str, nargs='*', default=['-'],help='target file')
    parser.add_argument('-d', '--decompress', default=False, action='store_true',help='uncompress the file')
    args = parser.parse_args()
    filenames = args.file
    if filenames == []:
        filenames.append('-')
    if args.decompress: #uncompress
        for filename in filenames:
            if filename == '-': #pipe
                r,w = os.pipe()
                pid = os.fork()
                if pid: # parent process
                    os.wait()
                    os.close(w)
                    saved_stdin = sys.stdin
                    sys.stdin = os.fdopen(r, 'rb') #redirect the stdin to pipe in for parent
                    LZ77().decode2()
                    sys.stdin.close()
                    sys.stdin = saved_stdin
                else: #child process
                    os.close(r)
                    saved_stdout = sys.stdout
                    sys.stdout = os.fdopen(w,'wb') #redirect the stdout to pipe out for child
                    huffman.decode2()
                    sys.stdout.close()
                    sys.stdout = saved_stdout
                    sys.exit(0)
                break
            assert filename.endswith('.mz')#make sure the target file is compress with myzip
            huffman.decode(filename, filename[:-3]+'.tmp')
            LZ77().decode(filename[:-3]+'.tmp', filename[:-3]+'.uz')
            os.remove(filename[:-3]+'.tmp')
    else:
        for filename in filenames:
            if filename == '-':
                r,w = os.pipe()
                pid = os.fork()
                if pid: #parent process
                    os.wait()
                    os.close(w)
                    saved_stdin = sys.stdin
                    sys.stdin = os.fdopen(r, 'rb') #redirect the stdin to pipe in for parent
                    huffman.encode2()
                    sys.stdin.close()
                    sys.stdin = saved_stdin
                else: #child process
                    os.close(r)
                    saved_stdout = sys.stdout
                    sys.stdout = os.fdopen(w,'wb') #redirect the stdout to pipe out for child
                    LZ77().encode2()
                    sys.stdout.close()
                    sys.stdout = saved_stdout
                    sys.exit(0)               
                break
            LZ77().encode(filename, filename+'.tmp')
            huffman.encode(filename+'.tmp', filename+'.mz')
            os.remove(filename+'.tmp')
