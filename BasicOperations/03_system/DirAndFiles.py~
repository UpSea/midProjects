import os
import sys
info=os.getcwd()
#info = './'
#listfile=os.listdir(os.getcwd())
#info=raw_input("请输入要列举文件的目录：(如D:\\temp)")

listfile=os.listdir(info)
file = info+'/'+'file.py'
filename=open(file,'w')
for line in listfile:  #把目录下的文件都赋值给line这个参数
    if line[-3:] == '.py' or line[-4:] != '.txt':
            print (line)
            out=open(line,'r')    #定义读取line里面的内容，也就是读取每个文件的内容
            for com in out:       #把每个文件的内容（也就是目录下的文件）赋值给com
                filename.write(line+":  "  +com)
                print(com)
 
    else:
        print(line+'  '+"该文件是目录形式")
filename.close() 