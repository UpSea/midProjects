# -*- coding: utf-8 -*-
import re
import os,sys
import subprocess
import platform;
import logging

def printSysInfo():
    logger = logging.getLogger('mid sysinfo')
    
    #logger.info = logger.warning
    
    logger.info("platform.machine()=%s", platform.machine());
    logger.info("platform.node()=%s", platform.node());
    logger.info("platform.platform()=%s", platform.platform());
    logger.info("platform.processor()=%s", platform.processor());
    logger.info("platform.python_build()=%s", platform.python_build());
    logger.info("platform.python_compiler()=%s", platform.python_compiler());
    logger.info("platform.python_branch()=%s", platform.python_branch());
    logger.info("platform.python_implementation()=%s", platform.python_implementation());
    logger.info("platform.python_revision()=%s", platform.python_revision());
    logger.info("platform.python_version()=%s", platform.python_version());
    logger.info("platform.python_version_tuple()=%s", platform.python_version_tuple());
    logger.info("platform.release()=%s", platform.release());
    logger.info("platform.system()=%s", platform.system());
    #logging.info("platform.system_alias()=%s", platform.system_alias());
    logger.info("platform.version()=%s", platform.version());
    logger.info("platform.uname()=%s", platform.uname());

#mid commit的-m参数后面的字符串必须要使用"",所以，外侧使用""" """
comments =  """ "mids upsea reconstructured." """

if __name__ == '__main__':
    sysstr = platform.system()
    if(sysstr =="Windows"):
        '''mid
        windows下需要将git路径手动添加到环境路径中，linux下不用
        windows下原来想使用下面的方法将git的路径加入到path中，以使os.system可以直接执行git命令
        多次尝试不行，所以只能手动通过windows的系统属性追加以下路径，之后在重启wingIde才能直接执行git而不用全路径
        '''
        gitpath = 'D:\\Program Files\\Git\\bin'
        os.system('path ')
        os.system('path %path% ;' + gitpath)
        os.system('path')
        #sys.path.append(gitpath) #mid 这个是添加到python路径中，不是系统路径，windows系统路径需要使用os.system
    elif(sysstr == "Linux"):
        print "Call Linux tasks"
    else:
        print "Other System tasks" 
    
    
    project_dir = os.path.abspath(os.path.dirname(__file__))
    try:
        os.chdir(project_dir)
        print 'pwd changed to '+project_dir        
    except Exception, e:
        raise e    
    
    try:
        os.system('git add --all')
        print 'git add --all'
    except Exception, error:
        print error    
    
    try:
        
        commit = 'git commit -m ' + comments
        print 'git commit -m'
        os.system(commit)
    except Exception, error:
        print error    
    
    try:
        os.system('git push git@github.com:upsea/midProjects master')        
        print 'push oked.'
    except Exception, error:
        print error
        
        
