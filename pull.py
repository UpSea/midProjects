# -*- coding: utf-8 -*-
import re
import os,sys
import subprocess
import platform;
import logbook  
logbook.StderrHandler().push_application()
logger = logbook.Logger('pull info ----')

if __name__ == '__main__':
    project_dir = os.path.abspath(os.path.dirname(__file__))
    try:
        os.chdir(project_dir)
    except:
        raise e       
    
    try:
        os.system('git pull git@github.com:upsea/midProjects')        
        logger.info( 'pull oked.')
    except:
        logger.info( e )
        
        
