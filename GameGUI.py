#!/usr/bin/python
from tkinter import *
import tkinter as tk
from tkinter import filedialog,ttk
import time
import numpy as np
import string as st
from functools import partial

window = tk.Tk()
window.attributes('-fullscreen',True)
window.configure(background='#D8D8EB')

def exit():
    window.destroy()

wordList = 'a,b,c,d,e,f,g,h,i,j,k,l,m,n,o,p,q,r,s,t,u,v,w,x,y,z'
numList = '0,1,2,3,4,5,6,7,8,9'
funList = '←,○,㊣'
keyBoardFrame = tk.Frame(window)
def keyBoard():
    nameButtom.config(state = 'disable')

    keyStr = numList+','+wordList+','+'_,-,[,]'+','+funList
    keyList = keyStr.split(',')
    col = 0
    row = 0
    keyLable = []
    lestLab = 0
    keyBoardFrame.pack(side = tk.BOTTOM)
    keyFrame = tk.Frame(keyBoardFrame)
    keyFrame.grid(column=0, row=0)
    for i in range(len(keyList)):

        if(keyList[i] == '←'):
            DEF = nameDel
            KEY = 0
        elif(keyList[i] == '○'):
            DEF = UpperKey
            KEY = keyLable
        elif(keyList[i] == '㊣'):
            DEF = keyBoardClose
            KEY = keyBoardFrame
        else:
            DEF = nameAdd
            KEY = keyList[i]
        #keyLable.append(tk.Label(keyBoardFrame,text=wordList[i],bg='yellow',borderwidth=2,relief='raised', width = 4, height = 2))
        keyLable.append(tk.Button(keyBoardFrame,text=keyList[i],bg='yellow', width = 4, height = 2,command=partial(DEF,KEY)))
        if(i%10 != 0):
            col += 1
        else:
            col = 0
            row +=1
        keyLable[i].grid(column=col, row=row, padx=3, pady=3)
        lestLab = i
def nameAdd(key):
    nameInsert['text'] += key

def nameDel(key):
    if(nameInsert['text']!=''):
        nameInsert['text'] = nameInsert['text'][:-1]

upperBool = False
def UpperKey(key):
    global upperBool,wordList
    if(upperBool):
        upperBool = False
        word = wordList
    else:
        word = wordList.upper()
        upperBool = True
    keyStr = numList+','+word+','+'_,-,[,]'+','+funList
    keyList = keyStr.split(',')
    for i in range(len(keyList)):
        if(keyList[i] == '←'):
            DEF = nameDel
            KEY = 0
        elif(keyList[i] == '○'):
            DEF = UpperKey
            KEY = key
        elif(keyList[i] == '㊣'):
            DEF = keyBoardClose
            KEY = keyBoardFrame
        else:
            DEF = nameAdd
            KEY = keyList[i]
        key[i].config(text = keyList[i],command = partial(DEF,KEY))
    

def keyBoardClose(key):
    key.pack_forget()
    nameButtom.config(state = 'active')

loginFrame = tk.Frame(window)
loginFrame.place(relx=0.5,rely=0.5,anchor=tk.CENTER)
loginTittle = tk.Label(loginFrame,text='註冊',width=15,height=2)
loginTittle.pack(side=tk.TOP)

inputFrame = tk.Frame(loginFrame)
inputFrame.pack(side = tk.TOP)
nameTittle = tk.Label(inputFrame,text='註冊姓名 : ',width=10,height=2)
nameTittle.grid(column=0, row=0, padx=5, pady=5)
nameInsert = tk.Label(inputFrame,text ='',width=20,bg='yellow',borderwidth=2,relief='raised')
nameInsert.grid(column=1, row=0, padx=5, pady=5)
nameButtom = tk.Button(inputFrame, text = "開啟鍵盤(測試)", width = 4, height = 1, command = keyBoard)
nameButtom.grid(column=2, row=0, padx=5, pady=5)

nameImgTittle = tk.Label(inputFrame,text='玩家照片 : ',width=10,height=2)
nameImgTittle.grid(column=0, row=1, padx=5, pady=5)
nameImgInsert = tk.Label(inputFrame,text='拍照',width=20,bg='yellow',borderwidth=2,relief='raised')
nameImgInsert .grid(column=1, row=1, padx=5, pady=5)

insertFrame = tk.Frame(loginFrame)
insertFrame.pack(side = tk.TOP)
insertConfn = tk.Label(insertFrame,text='確認註冊',width=12,height=1,bg='yellow',borderwidth=2,relief='raised')
insertConfn.pack(anchor=tk.CENTER)


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