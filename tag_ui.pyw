#!/usr/bin/env python3
# 界面

import json
import os
import time
from pathlib import Path
from typing import List

from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter import simpledialog
from tkinter import scrolledtext

from ui.delete_tag_dlg import DeleteTagDialog
from utils import gui_utils
from utils import str_utils
from utils import tag_utils

import tag_add
import tag_delete


class TagUI():
    def widget(self):
        return self.panewin

    def __init__(self, root, init_dir):
        self.curr_dir = init_dir

        self.create_menu(root)
        self.panewin = ttk.Panedwindow(root, orient=HORIZONTAL)

        self.frm_left = self.create_tag_tree(self.panewin)
        self.frm_left.grid(column=0, row=0, sticky=(N, S, E, W))
        self.panewin.add(self.frm_left, weight=1)

        self.pan_right = ttk.Panedwindow(self.panewin, orient=VERTICAL)
        self.pan_right.grid(column=0, row=0, sticky=(N, S, E, W))
        self.panewin.add(self.pan_right, weight=10)

        self.frm_list = self.create_file_list(self.pan_right)
        self.frm_list.grid(column=0, row=0, sticky=(N, S, E, W))
        self.pan_right.add(self.frm_list, weight=10)

        self.log = self.create_log(self.pan_right)
        self.log.grid(row = 0, column = 0, sticky = NSEW)
        self.pan_right.add(self.log, weight=1)


    def create_menu(self, parent):
        mbar = Menu(parent)
        fmenu = Menu(mbar, tearoff=False)
        mbar.add_cascade(label=' 文件 ',menu=fmenu)
        fmenu.add_command(label="打开文件夹", command=self.on_open_dir)
        fmenu.add_separator()
        fmenu.add_command(label="退出", command=parent.quit)

        parent.config(menu=mbar)


    def create_file_list(self, parent):
        """ 创建 文件列表 """
        frame = ttk.Frame(parent, relief=RIDGE)

        # 显示当前目录的文本框
        self.label_path_var = StringVar()
        self.label_path = ttk.Label(frame, textvariable=self.label_path_var)

        # 搜索框
        self.reverseFlag = False
        self.searchstr = StringVar()
        self.search = ttk.Entry(frame, textvariable=self.searchstr)
        self.searchstr.trace_add("write", self.on_search_files)

        # 文件列表（及滚动条）
        menubar = Menu(frame, tearoff=False)
        menubar.add_command(label='添加Tag', command=self.on_add_tag)
        menubar.add_command(label='删除Tag', command=self.on_delete_tag)
        self.file_list_menu = menubar

        columns = ('name', 'suffix', 'size', 'date')
        sort_types = ('zh', 'en', 'int', 'en')
        widths = (500, 60, 80, 200)
        texts = ("Name", "Ext", "Size", "Date")
        anchors = ("w", "w", "e", "c")
        self.file_list = ttk.Treeview(frame, columns=columns, show='headings')
        for i in range(len(columns)):
            self.file_list.column(columns[i], width=widths[i], minwidth=50, anchor=anchors[i])
            self.file_list.heading(columns[i], text=texts[i],
                command=lambda c=columns[i], t=sort_types[i]: gui_utils.sort_treeview_column(self.file_list, c, t, True))

        self.file_list.bind("<Double-1>", self.on_open_file)
        self.file_list.bind("<Button-3>", self.on_file_list_popup)
        self.file_list.bind("<<TreeviewSelect>>", self.on_select_files)
        scroll = ttk.Scrollbar(frame, orient=VERTICAL, command=self.file_list.yview)
        self.file_list['yscrollcommand'] = scroll.set
        self.fill_file_list()

        ttk.Label(frame, text="当前目录：").grid(column = 0, row = 0, sticky = W, padx=5, pady=5)
        self.label_path.grid(column = 1, row = 0, sticky = W)
        self.search.grid(column = 0, row = 1, sticky = EW, padx=5, pady=(0, 5), columnspan=2)
        self.file_list.grid(column = 0, row = 2, sticky = (N, S, E, W), columnspan=2)
        scroll.grid(column=3, row=2, padx=(0,5), sticky=(N, S))

        frame.rowconfigure(2, weight=10)
        frame.columnconfigure(1, weight=1)

        return frame


    def create_tag_tree(self, parent):
        """ 创建 Tag 树 """
        tree = ttk.Treeview(parent, selectmode='browse',show='tree')
        tree.bind("<Double-1>", self.on_tag_double_click)

        tag_file = Path("default.json")
        content = json.loads(tag_file.read_text(encoding='utf-8'))
        groups = content['groups']
        for group in groups:
            title = group['title']
            gid = tree.insert('', 'end', text=title)
            tags = group['tags']
            for tag in tags:
                tree.insert(gid, 'end', 'tag_' + gid + '_' + tag, text=tag)
        return tree


    def create_log(self, parent):
        """ 创建 日志控件 """
        text = scrolledtext.ScrolledText(parent, height=3)
        text.insert(END, "本区域为日志区，显示当前的操作信息。\n\n")
        text.insert(END, "上方是文件列表，显示当前目录下所有文件。\n\n")
        text.insert(END, "左侧为Tag区，双击叶节点可以将该Tag添加至文件列表中选中的文件。\n\n")
        text['state'] = 'disabled'
        return text


    def on_tag_double_click(self, event: Event):
        """ 双击 Tag 树中的 Tag 时，将相应的 Tag 添加到文件列表中当前选择的文件中 """
        e = event.widget
        iid = e.identify("item", event.x, event.y)
        if not iid.startswith('tag_'):
            self.show_log("")
            return

        tag = e.item(iid, "text")
        items = self.file_list.selection()
        if len(items) == 0:
            self.show_log("没有选中的文件，无法增加Tag")
            return

        files = [self.get_full_filename(item) for item in items]
        self.add_tag_to_files(tag, files)


    def add_tag_to_files(self, tag: str, files: List[Path]):
        """ 将 Tag 添加到文件列表中当前选择的文件中 """
        loginfo = f"Add tag [{tag}] to files:\n"
        for file in files:
            str = f"\t{file.name}\n"
            loginfo += str
        try:
            tag_add.add_tag(tag, files)
        except Exception as e:
            loginfo += f"{e}"
        self.show_log(loginfo)


    def on_search_files(self, *args):
        """ 搜索框内容发生变化时，在文件列表中显示满足条件的文件 """
        str = self.searchstr.get().lower()
        if str == "":
            self.show_file_list(self.all_file_data)
        else:
            visible_file_data = []
            for data in self.all_file_data:
                if str in data[0].lower():
                    visible_file_data.append(data)
            self.show_file_list(visible_file_data)


    def show_file_list(self, visible_file_data):
        """ 刷新文件列表中的内容 """
        items = self.file_list.get_children()
        [self.file_list.delete(item) for item in items]
        for data in visible_file_data:
            self.file_list.insert('', 'end', values = data)


    def on_open_file(self, event):
        """ 双击文件列表中的文件时，使用操作系统默认程序打开对应的文件 """
        items = self.file_list.selection()
        fullname = self.get_full_filename(items[0])
        self.show_log("open file: " + str(fullname))
        os.startfile(fullname)


    def on_select_files(self, event):
        """ 选择文件列表中的文件时，在日志中显示相应文件的信息 """
        items = self.file_list.selection()
        total_str = ""
        for item in items:
            file = self.get_full_filename(item)
            tags = tag_utils.get_file_tags(file)
            str = f"{file.name}\n\t{tags}\n"
            total_str += str
        self.show_log(total_str)


    def show_log(self, info: str):
        """在日志控件是显示日志信息

        Args:
            info (str): 要显示的日志信息
        """
        self.log['state'] = 'normal'
        self.log.delete("1.0", END)
        self.log.insert("end", info)
        self.log['state'] = 'disabled'


    def get_full_filename(self, tree_item) -> Path:
        """获取文件列表中一个文件的绝对路径

        Args:
            tree_item (_type_): 文件列表中的一项

        Returns:
            Path: 文件对应的绝对路径
        """
        values = self.file_list.item(tree_item, 'values')
        path = Path(self.curr_dir)
        filename = values[0] + values[1]
        fullname = path / filename
        return fullname


    def on_open_dir(self):
        """ 打开选择目录的界面，选择新目录后，刷新文件列表 """
        path = filedialog.askdirectory()
        if path == "":
            return
        self.curr_dir = path
        self.fill_file_list()


    def fill_file_list(self):
        """ 根据 curr_dir, 填充文件列表 """
        self.label_path_var.set(self.curr_dir)
        path = Path(self.curr_dir)
        self.all_file_data = []
        for entry in path.iterdir():
            if entry.name == ".tag" and entry.is_dir():
                continue
            data = [entry.stem,
                    entry.suffix,
                    entry.stat().st_size,
                    time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(entry.stat().st_mtime))]
            self.all_file_data.append(data)
        self.all_file_data.sort(key=lambda file: str_utils.to_pinyin(file[0]))
        self.show_file_list(self.all_file_data)


    def on_file_list_popup(self, event):
        self.file_list_menu.post(event.x_root, event.y_root)


    def on_add_tag(self):
        items = self.file_list.selection()
        if len(items) == 0:
            self.show_log("没有选中的文件，无法添加Tag")
            return
        tag = simpledialog.askstring("添加Tag", "输入要添加的Tag\n（会给文件列表中选中的文件同时增加此Tag）")
        if tag == '' or tag is None:
            return
        files = [self.get_full_filename(item) for item in items]
        self.add_tag_to_files(tag, files)


    def on_delete_tag(self):
        items = self.file_list.selection()
        if len(items) == 0:
            self.show_log("没有选中的文件，无法删除Tag")
            return
        files = [self.get_full_filename(item) for item in items]
        dlg = DeleteTagDialog(files)
        dlg.grab_set()
        self.panewin.wait_window(dlg)
        tags = dlg.deleted_tags
        loginfo = f"Delete tag(s) {tags} from file(s):\n"
        for file in files:
            loginfo += f"\t{file.name}\n"
        try:
            for tag in tags:
                tag_delete.delete_tag(tag, files)
        except Exception as e:
            total_str += f"{e}"
        self.show_log(loginfo)


def main():
    root = Tk()
    root.state("zoomed")
    root.title("Tag-Files")

    app = TagUI(root, Path.home() / 'Music')

    app.widget().grid(column=0, row=0, sticky=(N, S, E, W))
    root.rowconfigure(0, weight=1)
    root.columnconfigure(0, weight=1)

    root.mainloop()


if(__name__=='__main__'):
    main()

