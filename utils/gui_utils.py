#!/usr/bin/env python3
# GUI(tkinter)相关的工具类

from tkinter import *
from tkinter import ttk
from dataclasses import dataclass

if (__name__=='__main__'):
    import str_utils
else:
    from utils import str_utils


@dataclass
class Column:
     name: str      # 列的名字（ID）
     text: str      # 列显示的文字
     anchor: str    # 文字的显示位置。如：tk.N (可选值 N、NE、E、SE、S、SW、W、NW 或 CENTER)
     width: int     # 列的宽度
     sort_type: str # 排序方式. 可选值 'zh'，'en' 和 'int'。Defaults to 'en'.
                    #   'zh': 按中文的拼音排序
                    #   'en': 按英文的字母排序
                    #   'int': 按整数排序


class SortableTreeView(ttk.Treeview):
    def __init__(self, master=None, column_infos=None, **kw):
        self.img_arrow_up = PhotoImage(file='res/arrow_up.png')
        self.img_arrow_down = PhotoImage(file='res/arrow_down.png')
        self.img_empty = PhotoImage(file='res/empty.png')

        self.column_infos = column_infos
        self.last_sort_column = None
        self.last_sort_reverse = True

        names = [column.name for column in self.column_infos]
        kw.update({'columns': names})
        kw.update({'show': 'headings'})
        ttk.Treeview.__init__(self, master, **kw)
        for column in self.column_infos:
            self.column(column.name, width=column.width, minwidth=50, anchor=column.anchor)
            self.heading(column.name, text=column.text, image=self.img_empty,
                command=lambda c=column : self._on_click_column(c, True))


    def sort(self):
        if self.last_sort_column != None:
            self._sort(self.last_sort_column, self.last_sort_reverse)


    def select_first_row(self):
        self.focus_set()
        children = self.get_children()
        if children:
            self.focus(children[0])
            self.selection_set(children[0])


    def _on_click_column(self, column: Column, reverse: bool=True):
        self._sort(column, reverse)

        if self.last_sort_column != None:
            self.heading(self.last_sort_column.name, image=self.img_empty)

        img = self.img_arrow_down if reverse else self.img_arrow_up
        self.heading(column.name, image=img, command=lambda c=column : self._on_click_column(c, not reverse))

        self.last_sort_column = column
        self.last_sort_reverse = reverse


    def _sort(self, column, reverse):
        """（内部方法）对 TreeView 的列进行排序

        Args:
            column (Column): 待排序的列
            reverse (bool, optional): 排序方式。True为升序，False为降序. Defaults to True.
        """
        lst = [(self.set(k, column.name), k) for k in self.get_children('')]
        type = column.sort_type
        if type == 'zh':
            lst.sort(reverse=reverse, key=str_utils.to_pinyin)
        elif type == 'int':
            lst.sort(reverse=reverse, key=lambda item: (int(item[0])))
        else:
            lst.sort(reverse=reverse)

        for index, (val, k) in enumerate(lst):
            self.move(k, "", index)


class Demo:
    def __init__(self, root) -> None:
        frame = ttk.Frame(root)
        column_infos = [
            Column('name', 'Name', 'w', 500, 'zh'),
            Column('ext', 'Ext', 'w', 60, 'en'),
            Column('size', 'Size', 'e', 80, 'int')
        ]
        tv = SortableTreeView(frame, column_infos)
        tv.grid(column=0, row=0, sticky=(N, S, E, W))

        scrollbar = ttk.Scrollbar(frame, orient=VERTICAL, command=tv.yview)
        tv['yscrollcommand'] = scrollbar.set

        fill_tv(tv)
        tv.select_first_row()

        tv.grid(column=0, row=0)
        scrollbar.grid(column=1, row=0, sticky=NS)
        frame.columnconfigure(0, weight=1)
        frame.rowconfigure(0, weight=1)

        frame.grid(column=0, row=0)


def fill_tv(tv):
    datas = [
        ['张学友 - 每天爱你多一些', '.mp3', 11363324],
        ['张学友 - 情书', '.mp3', 9834557],
        ['张学友 - 烦恼歌', '.mp3', 10218383],
        ['酒井法子 (さかい のりこ) - 夢冒険', '.mp3', 3025271],
        ['酒井法子 (さかい のりこ) - 碧いうさぎ (碧绿色的兔子)', '.mp3', 9128258],
        ['酒井法子 (さかい のりこ) - あなたに天使が見える時 (当你看见天使的时候)', '.mp3', 12150253],
        ['周慧敏 - 痴心换情深', '.mp3', 10334335],
        ['周慧敏 - 最爱', '.mp3', 10728918],
        ['周慧敏 - 自作多情', '.mp3', 12783606],
        ['刘若英 - 为爱痴狂', '.mp3', 12234497],
        ['李宗盛 - 凡人歌', '.mp3', 9322146],
        ['李宗盛 _ 林忆莲 - 当爱已成往事', '.mp3', 11286699],
        ['李克勤 - 护花使者', '.mp3', 7885570],
        ['李克勤 - 月半小夜曲', '.mp3', 11679156],
        ['李克勤 - 红日 (粤语)', '.mp3', 11582657],
        ['陈雪凝 - 你的酒馆对我打了烊', '.mp3', 10122241],
        ['陈奕迅 - 孤勇者', '.mp3', 10291946],
        ['陈奕迅 _ 王菲 - 因为爱情', '.mp3', 8745129],
        ['王菲 - 如愿', '.mp3', 10724878],
        ['周华健 - 忙与盲', '.mp3', 11412263],
        ['井上杏美 (井上あずみ) - いつも何度でも (永远同在)', '.mp3', 11499254],
        ['中岛美嘉 (なかしま みか) - 僕が死のうと思ったのは (曾经我也想过一了百了)', '.mp3', 15324379],
        ['DJ OKAWARI - Flower Dance', '.mp3', 10639575],
        ['柳青瑶 - 听！秦王破阵乐！_hires', '.flac', 109822969],
        ['Diana Boncheva - Purple Passion', '.flac', 30308104],
        ['久石让 (ひさいし じょう) - The Sun Also Rises', '.mp3', 9021211],
        ['Anne-Sophie Mutter - 流浪者之歌', '.flac', 46479291],
        ['file1', '.txt', 1234]
    ]
    for data in datas:
        tv.insert('', END, values = data)


def main():
    root = Tk()
    root.title("SortableTreeView")

    app = Demo(root)

    root.rowconfigure(0, weight=1)
    root.columnconfigure(0, weight=1)

    root.mainloop()


if(__name__=='__main__'):
    main()


