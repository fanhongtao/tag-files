#!/usr/bin/env python3

import getopt
import sys
import tag_utils
from typing import List


def show_help():
    """ 显示帮助信息 """
    print("显示一个或多个文件的tag")
    print()
    program = sys.argv[0]
    print(program + " <files>")
    def print_arg(name, info): print("  %-28s\t%s" % (name, info))
    print_arg("-h, --help", "显示帮助信息")
    print()
    print_arg("<files>", "文件名（一个或多个，支持使用通配符）")
    print()
    print(program + " '张学友 - 烦恼歌.mp3'")
    print(program + " 酒井法子*")


def show_tag(files: List[str]):
    """显示一个或多个文件的tag

    Args:
        files (List[str]): 文件名数组
    """
    for file in files:
        file_tags = tag_utils.get_file_tags(file)
        print(file)
        print('\t' + str(file_tags))


def main():
    """ 分析调用参数，进行相应的处理 """
    long_args = ["help"]
    opts, args = getopt.getopt(sys.argv[1:], "h", long_args)

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            show_help()
            return

    if len(args) < 1:
        show_help()
    else:
        show_tag(args)


if __name__ == '__main__':
    main()
