#!/usr/bin/env python3

import getopt
import sys
import utils.tag_utils as tag_utils
from typing import List


def show_help():
    """ 显示帮助信息 """
    print("给一个或多个文件删除tag")
    print()
    program = sys.argv[0]
    print(program + " [-h] [-print0] <tag> <files>")
    def print_arg(name, info): print("  %-28s\t%s" % (name, info))
    print_arg("-h, --help", "显示帮助信息")
    print_arg("-print0", "输出文件名使用 '\\0' 进行分隔（用于配合 xargs -0 使用）")
    print()
    print_arg("<tag>", "要删除的标签(tag)")
    print_arg("<files>", "需要删除标签的文件名（一个或多个，支持使用通配符）")
    print()
    print(program + " 中文 '张学友 - 烦恼歌.mp3'")
    print(program + " 日文 酒井法子*")


def delete_tag(tag: str, files: List[str], end: str=None):
    """给指定的文件删除标签

    Args:
        tag (str): 标签
        files (List[str]): 文件名数组
        end (str): 输出时的结尾符号。为 None 时表示不输出
    """
    for file in files:
        tag_file = tag_utils.get_tag_file(file)
        content = tag_utils.load_tag_content(tag_file)
        fil_tags = content.get('tags', [])
        if tag in fil_tags:
            fil_tags.remove(tag)
        content['tags'] = fil_tags
        tag_utils.write_tag_content(tag_file, content)
        if not (end is None):
            print(file, end=end)


def main():
    """ 分析调用参数，进行相应的处理 """
    long_args = ["help"]
    opts, args = getopt.getopt(sys.argv[1:], "h-print0", long_args)

    end = '\n'
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            show_help()
            return
        if opt in ("-print0"):
            end = '\0'
            continue

    if len(args) < 2:
        show_help()
    else:
        delete_tag(args[0], args[1:], end)


if __name__ == '__main__':
    main()
