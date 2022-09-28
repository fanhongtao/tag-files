#!/usr/bin/env python3
# 字符串相关的工具类

from itertools import chain
from pypinyin import pinyin, Style

def to_pinyin(s:str) -> str:
    """将输入的字符串转换成带声调拼音

    Args:
        s (str): 待转换的字符串

    Returns:
        str: 对应的拼音
    """
    return ''.join(chain.from_iterable(pinyin(s, style=Style.TONE3)))

