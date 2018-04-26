#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    Copyright (c) 2016-2018 - Linkio SAS. All Rights Reserved.

    All information contained herein is, and remains the property of
    Linkio SAS.
    The intellectual and technical concepts contained herein are
    proprietary to Linkio SAS.
    Dissemination of this information or reproduction of this material
    is strictly forbidden unless prior written permission is obtained
    from Linkio SAS.

"""

__author__      = "Bruno DEGUET"
__email__       = "bruno@linkio.net"
__copyright__   = "Copyright 2018, Linkio SAS"
__version__     = "1.0.0"
__status__      = "Development"

#import tkinter as tk
try:
    # python 2.x
    #import Tkinter as tk
    from Tkinter import *
except ImportError:
    # python 3.x
    #import tkinter as tk
    from tkinter import *

class ItemFrame():
    def __init__(self, root, row, uid, on_open):
        self.row = row
        self.uid = uid
        self.text = StringVar()
        self.on_open = on_open
        self.window_opened = False
        self.window = None
        #Label(root, text="%s" % row, width=3, borderwidth="1",relief="solid").grid(row=row, column=0)
        #Label(root, text="%s" % row, width=3).grid(row=row, column=0)
        Label(root, text=uid).grid(row=row, column=1)
        self.entry = Entry(root, textvariable=self.text,width = 40).grid(row=row, column=2)
        Button(root, text = "Edit", width=6, command = self.open).grid(row=row, column=3)

    def open(self):
        #fDevice = Toplevel()
        print("open item %d"%(self.row))
        if self.on_open :
            self.on_open(self)

class ItemsList():
    def __init__(self, root):

        #self.f = Frame(root)
        #self.f.pack(side="top", fill="both", expand=True)
        self.canvas = Canvas(root, borderwidth=0,width=550)
        self.frame = Frame(self.canvas )
        self.vsb = Scrollbar(root, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.vsb.set)

        self.vsb.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)
        self.canvas.create_window((0,0), window=self.frame, anchor="nw",
                                  tags="self.frame")

        self.frame.bind("<Configure>", self.onFrameConfigure)

        #self.populate()
        self.ui_items = []
        self.widget = root

    def get(self,uid,on_open):
        for ui_item in self.ui_items :
            if ui_item.uid == uid:
                return ui_item
        # no item, create it
        next_row = len(self.ui_items)
        ui_item = ItemFrame(self.frame, next_row, uid,on_open)
        self.ui_items.append(ui_item)
        return ui_item

    def onFrameConfigure(self, event):
        '''Reset the scroll region to encompass the inner frame'''
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

if __name__ == "__main__":
    root=Tk()
    fRemote = LabelFrame(root,text="Remote modules",borderwidth=2,relief=GROOVE)
    fRemote.pack(fill="both", expand=False,side=RIGHT,padx=2,pady=2)

    mylist = ItemsList(fRemote)
    for row in range(10):
        item = mylist.get("ui%d"%(row))
        item.text.set("this text %d"%(row))
    root.mainloop()
