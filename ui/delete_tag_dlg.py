#!/usr/bin/env python3
# 删除一个或多个文件对应的Tag的对话框

from tkinter import *
from tkinter import ttk

from utils import tag_utils

class DeleteTagDialog(Toplevel):
    def __init__(self, files):
        super().__init__()
        self.title('删除Tag')
        self.wm_attributes("-toolwindow", True)
        self.resizable(False, False)

        self.deleted_tags = None
        frame = ttk.Frame(self)

        list = self.create_tag_list(frame, files)
        list.grid(column=0, row=0, sticky=NSEW)

        ttk.Label(frame, text='从上面的 Tag 列表中选择要删除的 Tag，然后点击 "删除" 按钮').grid(column=0, row=1, padx=5)

        buttons = self.craete_buttons(frame)
        buttons.grid(column=0, row=2, pady=5)

        frame.grid(column=0, row=0)


    def create_tag_list(self, parent, files):
        frame = ttk.Frame(parent)

        tag_list = ttk.Treeview(parent, columns=['Tag'], show='headings')
        tag_list.column('Tag', width=200, minwidth=50, anchor='w')
        tag_list.heading('Tag', text='Tag')

        scroll = ttk.Scrollbar(parent, orient=VERTICAL, command=tag_list.yview)
        tag_list['yscrollcommand'] = scroll.set

        # tags = ['abc', 'def', 'hij', "hell", "world", "name",'jack','rose', 'penny', 'tom', 'felix', 'def', 'hij', "hell", "world", "name",'jack','rose', 'penny', 'tom', 'felix']
        tags = tag_utils.get_files_tags(files)
        for tag in tags:
            tag_list.insert('', 'end', values = [tag])

        self.tag_list = tag_list

        tag_list.grid(column=0, row=0, sticky=NSEW)
        scroll.grid(column=1, row=0, sticky=NS)

        return frame


    def craete_buttons(self, parent):
        frame = ttk.Frame(parent)
        ttk.Button(frame, text="删除", command=self.on_ok).grid(column=0, row=0, padx=5)
        ttk.Button(frame, text="取消", command=self.on_cancel).grid(column=1, row=0, padx=5)
        return frame


    def on_ok(self):
        items = self.tag_list.selection()
        self.delete_tags(items)
        self.destroy()


    def on_cancel(self):
        self.destroy()


    def delete_tags(self, items):
        if items == []:
            return

        tags = []
        for item in items:
            values = self.tag_list.item(item, 'values')
            tags.append(str(values[0]))

        self.deleted_tags = tags

