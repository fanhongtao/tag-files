#!/usr/bin/env python3
# GUI(tkinter)相关的工具类

from tkinter import *
from tkinter import ttk

from utils import str_utils

def sort_treeview_column(tv: ttk.Treeview, column: str, type: str='en', reverse: bool=True):
    """对 TreeView 的列进行排序

    Args:
        tv (ttk.Treeview): 待排序的 TreeView 控件
        col (str): 待排序的列
        type (str, optional): 排序方式. 可选值 'zh'，'en' 和 'int'。Defaults to 'en'.
                        'zh': 按中文的拼音排序
                        'en': 按英文的字母排序
                        'int': 按整数排序
        reverse (bool, optional): 排序方式。True为升序，False为降序. Defaults to True.
    """
    lst = [(tv.set(k, column), k) for k in tv.get_children('')]

    if type == 'zh':
        lst.sort(reverse=reverse, key=str_utils.to_pinyin)
    elif type == 'int':
        lst.sort(reverse=reverse, key=lambda item: (int(item[0])))
    else:
        lst.sort(reverse=reverse)

    for index, (val, k) in enumerate(lst):
        tv.move(k, "", index)

    tv.heading(column, command=lambda: sort_treeview_column(tv, column, type, not reverse))

