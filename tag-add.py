#!/usr/bin/env python3

import getopt
import sys
import utils.tag_utils as tag_utils
from typing import List


def show_help():
    """ 显示帮助信息 """
    print("给一个或多个文件添加tag")
    print()
    program = sys.argv[0]
    print(program + " [-h] [-print0] <tag> <files>")
    def print_arg(name, info): print("  %-28s\t%s" % (name, info))
    print_arg("-h, --help", "显示帮助信息")
    print_arg("-print0", "输出文件名使用 '\\0' 进行分隔（用于配合 xargs -0 使用）")
    print()
    print_arg("<tag>", "要添加的标签(tag)")
    print_arg("<files>", "需要添加标签的文件名（一个或多个，支持使用通配符）")
    print()
    print(program + " 中文 '张学友 - 烦恼歌.mp3'")
    print(program + " 日文 酒井法子*")


def add_tag(tag: str, files: List[str]):
    """给指定的文件添加标签

    Args:
        tag (str): 标签
        files (List[str]): 文件名数组
    """
    for file in files:
        tag_file = tag_utils.get_tag_file(file)
        content = tag_utils.load_tag_content(tag_file)
        fil_tags = content.get('tags', [])
        if tag not in fil_tags:
            fil_tags.append(tag)
        content['tags'] = fil_tags
        tag_utils.write_tag_content(tag_file, content)
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

    if len(args) < 2:
        show_help()
    else:
        add_tag(args[0], args[1:])


if __name__ == '__main__':
    main()
