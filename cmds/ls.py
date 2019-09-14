import glob 
import os 

class ls(object):
    def __init__(self):
        print(type(self).__name__)
        
    def match(self, name):
        return type(self).__name__ == name
        
    def execute(self, lstcmd, page):
        for elm in glob.glob(os.path.join(os.getcwd(),"*.*")):
            #print(elm)
            if page.isImage(elm):
                page.addImageConsole(elm)          
            else:
                page.addTextConsole(os.path.basename(elm))
 
        page.page.currentFrame().evaluateJavaScript("var lightbox = $('.gallery a').simpleLightbox();");