#!/usr/bin/env python3

import getopt
import sys
import tag_utils
from pathlib import Path
from typing import List


def show_help():
    """ 显示帮助信息 """
    print("显示输入的一组文件中所有未指定tag的文件")
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


def list_no_tag_file(files: List[str]):
    """显示输入的一组文件中所有未指定tag的文件

    Args:
        files (List[str]): 文件名
    """
    for entry in files:
        file = Path(entry)
        if file.is_dir():
            continue
        file_tags = tag_utils.get_file_tags(file)
        if file_tags == []:
            print(f"'{file}'")


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
        list_no_tag_file(args)


if __name__ == '__main__':
    main()
