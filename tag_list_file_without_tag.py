#!/usr/bin/env python3

import getopt
import sys
import utils.tag_utils as tag_utils
from pathlib import Path
from typing import List


def show_help():
    """ 显示帮助信息 """
    print("显示输入的一组文件中所有未指定tag的文件")
    print()
    program = sys.argv[0]
    print(program + " [-h] [-print0] <files>")
    def print_arg(name, info): print("  %-28s\t%s" % (name, info))
    print_arg("-h, --help", "显示帮助信息")
    print_arg("-print0", "输出文件名使用 '\\0' 进行分隔（用于配合 xargs -0 使用）")
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
            print(file, end=g_end)


def main():
    """ 分析调用参数，进行相应的处理 """
    long_args = ["help"]
    opts, args = getopt.getopt(sys.argv[1:], "h-print0", long_args)

    global g_end
    g_end = '\n'
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            show_help()
            return
        if opt in ("-print0"):
            g_end = '\0'
            continue

    if len(args) < 1:
        show_help()
    else:
        list_no_tag_file(args)


if __name__ == '__main__':
    main()
