import os 

class cd(object):
    #def __init__(self):
    #   print(type(self).__name__)
        
    def match(self, name):
        return type(self).__name__ == name
        
    def execute(self, lstcmd, page):
        os.chdir(lstcmd[1])
       