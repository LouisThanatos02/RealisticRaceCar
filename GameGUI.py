#!/usr/bin/python
from tkinter import *
import tkinter as tk
from tkinter import filedialog,ttk
import time
import numpy as np
import string as st

window = tk.Tk()
window.attributes('-fullscreen',True)
window.configure(background='#D8D8EB')

def exit():
    window.destroy()

loginFrame = tk.Frame(window)
loginFrame.place(relx=0.5,rely=0.5,anchor=tk.CENTER)
loginTittle = tk.Label(loginFrame,text='註冊',width=15,height=2)
loginTittle.pack(side=tk.TOP)

inputFrame = tk.Frame(loginFrame)
inputFrame.pack(side = tk.TOP)
nameTittle = tk.Label(inputFrame,text='註冊姓名 : ',width=10,height=2)
nameTittle.grid(column=0, row=0, ipadx=5, pady=5)
nameInsert = tk.Label(inputFrame,text ='輸入姓名',width=20,bg='yellow',borderwidth=2,relief='raised')
nameInsert .grid(column=1, row=0, ipadx=5, pady=5)

nameImgTittle = tk.Label(inputFrame,text='玩家照片 : ',width=10,height=2)
nameImgTittle.grid(column=0, row=1, ipadx=5, pady=5)
nameImgInsert = tk.Label(inputFrame,text='拍照',width=20,bg='yellow',borderwidth=2,relief='raised')
nameImgInsert .grid(column=1, row=1, ipadx=5, pady=5)

insertFrame = tk.Frame(loginFrame)
insertFrame.pack(side = tk.TOP)
insertConfn = tk.Label(insertFrame,text='確認註冊',width=12,height=1,bg='yellow',borderwidth=2,relief='raised')
insertConfn.pack(anchor=tk.CENTER)

wordInput = st.ascii_lowercase
numInput = '0123456789'
col = 0
row = 0
keyLable = wordInput
keyBoardFrame = tk.Frame(window)
keyBoardFrame.pack(anchor = tk.CENTER)
for i in range(len(wordInput)):
    keyLable[i] = tk.Label(keyBoardFrame,text=wordInput[i],bg='yellow',borderwidth=2,relief='raised')
    if(i%7 != 0):
        col += 1
    else:
        col = 0
        row +=1
    keyLable.grid(column=col, row=row, ipadx=5, pady=5)
    print(keyLable)



fnBarFrame = tk.Frame(window) #選項的frame
fnBarFrame.pack(anchor=tk.NW)
creat_count = 1
"""
for i in range(len(sel_EN)):
    sel_EN[i] = tk.Label(fnBarFrame, text = sel_CH[i],width=12,height=2,bg=sel_colr[i],borderwidth=2,relief=sel_list[i])
    sel_EN[i] .pack(side=tk.LEFT,padx = 10,pady = 10)
    if(i > 1):
        sel_EN[i].pack_forget()
    if(creat_count < len(sel_EN)):
        sel_list.append('flat')
        sel_colr.append('yellow')
    creat_count += 1
"""
def  exit():
    window.destroy()

testFrame = tk.Frame(window) #測試用的frame
testFrame.pack(anchor =tk.SE)
button_lev = tk.Button(testFrame, text = "離開", width = 12, height = 2, command = exit)
button_lev.pack(anchor =tk.SE)


if __name__ == "__main__":
    window.mainloop()