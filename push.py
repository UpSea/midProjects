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

comments = " 'mid batch files added'"

if __name__ == '__main__':
    sysstr = platform.system()
    if(sysstr =="Windows"):
        '''mid
        windows下原来想使用下面的方法将git的路径加入到path中，以使os.system可以直接执行git命令
        多次尝试不行，所以只能手动通过windows的系统属性追加以下路径，之后在重启wingIde才能直接执行git而不用全路径
        '''
        gitpath = 'D:\\Program Files\\Git\\bin'
        os.system('path ')
        os.system('path %path% ;' + gitpath)
        os.system('path')
        #sys.path.append(gitpath)
    elif(sysstr == "Linux"):
        print "Call Linux tasks"
    else:
        print "Other System tasks" 
    
    
    project_dir = os.path.abspath(os.path.dirname(__file__))
    try:
        os.chdir(project_dir)
    except Exception, e:
        raise e    
    
    try:
        os.system('git add --all')
    except Exception, error:
        print error    
    
    try:
        commit = 'git commit -m ' + comments
        commit = """ git commit -m "mids batch files added" """

        os.system(commit)
    except Exception, error:
        print error    
    
    try:
        os.system('git push git@github.com:upsea/midProjects master')        
    except Exception, error:
        print error
        
        
