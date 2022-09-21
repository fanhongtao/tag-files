#!/usr/bin/env python3

import getopt
import sys
import tag_utils


def show_help():
    """ 显示帮助信息 """
    print("显示指定目录下所有文件使用到的tag")
    print()
    program = sys.argv[0]
    print(program + " <dir>")
    def print_arg(name, info): print("  %-28s\t%s" % (name, info))
    print_arg("-h, --help", "显示帮助信息")
    print()
    print_arg("<dir>", "指定的目录")
    print()
    print(program + " .")
    print(program + " /home/music")


def list_tag(dir: str):
    """显示指定目录下所有文件使用到的tag

    Args:
        dir (str): 指定的目录
    """
    dir_tags = tag_utils.get_dir_tags(dir)
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
        list_tag(args[0])


if __name__ == '__main__':
    main()
