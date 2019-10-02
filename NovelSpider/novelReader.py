#-*- coding:utf-8 -*-

####简单的演示小说读取

import os
import msvcrt

with open("D:\\novel.txt", 'rb') as file:#代码结束后会自动file.close
    s = file.read(100)
    s = str(s, encoding='gbk')
    print(s, end = '')#使print 输出不换行

    while True :#util EOF
        t = msvcrt.getch()
        te = str(t, encoding = 'utf-8')
        if te == 'a':
            file.seek(-200, 1)#从当前位置偏移-100 若不使用b打开则会报错
            s = file.read(100)
        else:
            s = file.read(100)
        s = str(s, encoding='gbk')
        print(s, end = '')



