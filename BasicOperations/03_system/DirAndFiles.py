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

#mid 根据某个文件的相对位置打开确定的文件
import sys,os
#mid 获取当前文件父目录下孙文件夹的路径，不能使用‘/’，os.sep，算法中遇到‘/’时会清空之前的所有字符
path = os.path.abspath(os.path.join(os.path.dirname(__file__),os.pardir,'histdata','day'))
#mid 合成全文件名
filepath = path +os.sep + instrument + market + ".csv"
#mid 将文件夹添加入系统目录
sys.path.append(path) 
