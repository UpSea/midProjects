#!/usr/bin/env python    
# -*- coding: utf-8 -*-   
import os  
import platform  
import subprocess  
import commands  
def subproc():  
    print "系统进程数："  
    subprocess.call("ps -ef|wc -l",shell=True)  
def os_popen():  
    print "IP地址："  
    os1 = platform.system()  
    if os1 == "Linux":  
        print os1  
        ip1 =os.popen("/sbin/ifconfig eth0|grep 'inet addr'").read().strip().split(":")[1].split()[0]  
        print "\033[1;32;40m%s\033[0m" % ip1  
def os_system():  
    os_command = 'free -m'   
    cls_node1 = "命令执行成功...."  
    cls_node2 = "命令执行失败...."  
    if os.system(os_command) == 0:  
        print "\n\033[1;32;40m%s\033[0m" % cls_node1  
    else:  
        print "\n\033[1;31;40m%s\033[0m" % cls_node2  
def os_commands():  
    (status, output) = commands.getstatusoutput('pwd')  
    print status, output  
def main():  
    subproc()  
    os_popen()  
    os_system()  
    os_commands()  
if __name__ == "__main__":  
        main()  