#!/usr/bin/env python3

import getopt
import sys
import tag_utils
from typing import List


def show_help():
    """ 显示帮助信息 """
    print("显示输入的一组文件使用到的tag")
    print()
    program = sys.argv[0]
    print(program + " <files>")
    def print_arg(name, info): print("  %-28s\t%s" % (name, info))
    print_arg("-h, --help", "显示帮助信息")
    print()
    print_arg("<files>", "待判断的文件名（一个或多个，支持使用通配符）")
    print()
    print(program + " *")
    print(program + " 张学友*")


def list_tag(files: List[str]):
    """显示输入的一组文件使用到的tag

    Args:
        files (List[str]): 文件名
    """
    dir_tags = tag_utils.get_files_tags(files)
    for tag in dir_tags:
        print(tag)


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
        list_tag(args)


if __name__ == '__main__':
    main()
