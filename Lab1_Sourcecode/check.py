#!/usr/bin/python3
import re


def check(s: str) -> bool:
    return re.fullmatch(r'2021信息论与编码-实验1-(\d|\w)+-[^-]+\.(rar|7z|tar\.gz|tar\.lzma)', s) is not None


if __name__ == "__main__":
    name = input("Your file name with extension: ")
    if check(name):
        print("Good name, you can submit your homework now!")
    else:
        print("Please double check your file name.")
