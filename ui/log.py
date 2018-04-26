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

import argparse

from lmp.lmpserial import *

try:
    # python 2.x
    #import Tkinter as tk
    from Tkinter import *
except ImportError:
    # python 3.x
    #import tkinter as tk
    from tkinter import *

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class UILog():
    def __init__(self):
        wLog = Toplevel()
        wLog.title("Log")
        wLog.protocol("WM_DELETE_WINDOW", wLog.iconify)
        #fLog = LabelFrame(wLog,text="Log",borderwidth=2,relief=GROOVE)
        #fLog.pack(fill="both", expand=False,side=RIGHT,padx=2,pady=2)
        # make a scrollbar
        scrollbar = Scrollbar(wLog)
        scrollbar.pack(side=RIGHT, fill=Y)

        # make a text box to put the serial output
        self.log = Text( wLog, width=100, takefocus=0) #, width=40, height=30
        self.log.pack(fill="both", expand=True,side=LEFT)
        # attach text box to scrollbar
        self.log.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.log.yview)

    def debug( self,name,*args ):
        st = ''.join(args)
        date = timestamp_str(None)
        self.log.insert("end", "%s DEBUG  %8s: %s\n"%(date,name,st))
        self.log.see("end")
        print( "%s DEBUG  %8s: %s"%(date,name,st) + bcolors.ENDC )

    def info( self,name,*args ):
        st = ''.join(args)
        date = timestamp_str(None)
        self.log.insert("end", "%s INFO   %8s: %s\n"%(date,name,st))
        self.log.see("end")
        print(bcolors.OKGREEN + "%s INFO   %8s: %s"%(date,name,st) + bcolors.ENDC )

    def warning( self,name,*args ):
        st = ''.join(args)
        date = timestamp_str(None)
        self.log.insert("end", "%s WARNING%8s: %s\n"%(date,name,st))
        self.log.see("end")
        print(bcolors.WARNING + "%s WARNING%8s: %s"%(date,name,st) + bcolors.ENDC )

    def error( self,name,*args ):
        st = ''.join(args)
        date = timestamp_str(None)
        self.log.insert("end", "%s ERROR  %8s: %s\n"%(date,name,st))
        self.log.see("end")
        print(bcolors.FAIL + "%s ERROR  %8s: %s"%(date,name,st) + bcolors.ENDC )


if __name__ == "__main__":
    ui_log.debug("UI","test")
    ui_log.info("UI","test")
    ui_log.warning("UI","test")
    ui_log.error("UI","test")
