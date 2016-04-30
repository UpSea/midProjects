'''
open a python program file and execute it.
'''
#----------------------------------------------------------------------      
def exec_filePath(self,filepath):
    global_namespace = {"__file__": filepath,"__name__": "__main__","__fig__":self.strategyFig}
    with open(filepath, 'rb') as file:
        exec(compile(file.read(), filepath, 'exec'), global_namespace)
#----------------------------------------------------------------------
def slotSaveAndRun(self):
    """        
    execute the file
    """
    self.strategyFig = plt.figure()
    strategyFile = os.getcwd()+'/test.py'
    self.exec_filePath(strategyFile)  