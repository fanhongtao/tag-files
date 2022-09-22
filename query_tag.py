#!/usr/bin/env python3

import getopt
import sys
import tag_utils
from pathlib import Path
from typing import List


def show_help():
    """ 显示帮助信息 """
    print("在指定目录下查询含有指定tag的文件")
    print()
    program = sys.argv[0]
    print(program + " [-h] [-print0] [-d <dir>] <tags>")
    def print_arg(name, info): print("  %-28s\t%s" % (name, info))
    print_arg("-h, --help", "显示帮助信息")
    print_arg("-print0", "输出文件名使用 '\\0' 进行分隔（用于配合 xargs -0 使用）")
    print_arg("-d, --dir", "待查询的目录，默认为当前目录")
    print()
    print_arg("<tags>", "待查询的标签(tag)。")
    print_arg("", "当指定多个标签时，文件必须同时包含所有指定的标签才会显示。")
    print()
    print(program + " 中文")
    print(program + " -d /home/music 日文")
    print(program + " --dir=/home/music 日文")


def query_tag(dir: str, tags: List[str]):
    """在指定目录下查询含有指定tag的文件，找到满足条件的文件时，打印文件名。

    Args:
        dir (str): 待查询的目录
        tags (List[str]): 标签
    """
    path = Path(dir)
    for file in path.iterdir():
        if file.is_dir():
            continue
        file_tags = tag_utils.get_file_tags(file)
        for tag in tags:
            if tag not in file_tags:
                break
        else:
            print(file, end=g_end)


def main():
    """ 分析调用参数，进行相应的处理 """
    dir = "."
    long_args = ["help", "dir="]
    opts, args = getopt.getopt(sys.argv[1:], "hd:-print0", long_args)

    global g_end
    g_end = '\n'
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            show_help()
            return
        if opt in("-d", "--dir"):
            dir = arg
            continue
        if opt in ("-print0"):
            g_end = '\0'
            continue

    if len(args) < 1:
        show_help()
    else:
        query_tag(dir, args)


if __name__ == '__main__':
    main()
