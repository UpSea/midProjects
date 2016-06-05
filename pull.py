# -*- coding: utf-8 -*-
import re
import os,sys
import subprocess
import platform;
import logging

if __name__ == '__main__':
    try:
        os.system('git pull git@github.com:upsea/midProjects')        
        print 'pull oked.'
    except Exception, error:
        print error
        
        
