# -*- coding: utf-8 -*-
import re
import os,sys
import subprocess
import platform;
import logbook  
logbook.StderrHandler().push_application()
logger = logbook.Logger('pull info ----')


def pullGit(projectDir = '',gitCommand = ''):
    logger.info('start ----')
    try:
        os.chdir(projectDir)
    except:
        logger.info(e)
        raise e           
    try:
        os.system(gitCommand)        
        logger.info('%s Oked.' % (gitCommand))
    except:
        logger.info(e)    
        raise e
    logger.info('end #####')


if __name__ == '__main__':
    projectDir = os.path.abspath(os.path.dirname(__file__))
    gitCommand = 'git pull git@github.com:upsea/midProjects'
    
    pullGit(projectDir=projectDir,gitCommand = gitCommand)

        
        
