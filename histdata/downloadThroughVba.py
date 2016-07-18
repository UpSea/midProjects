# -*- coding: utf-8 -*-

import os
import win32com.client

def genStrFunc(bookName,modeName,functionName,**kwargs):
    '''mid
    原计划通过此函数生成调用参数传递给vba执行
    得知执行此过程时也必须要打开被调用过程所在excel以打开choice终端后，直接在excel中做输入输出更加方便
    '''
    strFunc = bookName + '!' + modeName + '.' + functionName + '('
    
    for key in kwargs:  
        print "another keyword arg: %s: %s" % (key, kwargs[key])      

    strFunc = strFunc + ')'
    return strFunc

if __name__ == '__main__':
    '''mid
    调用前需要先打开对应的excel文件和加载choice addin 到excel，否则报错。
    '''
    xlapp = win32com.client.Dispatch('excel.application')
    filename = os.path.abspath(os.path.join(os.path.dirname(__file__),'vba','mid_hist.xlsm'))        
    
    xlbook = xlapp.workbooks.open(filename)
    strpara = xlbook.name + '!mid_hist.downloadHistAndToCsv()'
    status = xlapp.executeexcel4macro(strpara)
    
    print status
