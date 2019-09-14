import sys
import os
import importlib

import PySide.QtGui as QtGui
from PySide.QtCore import QUrl
from PySide.QtWebKit import QWebView,QWebPage,QWebSettings
from PySide.QtCore import Signal

class pluginManager:
    def __init__(self, path):
        self._path = path
        self._modules = {}
        self._loadmodules()

    def _loadmodules(self):
        for filepy in os.listdir(self._path):
            if filepy == "__init__.py":
                continue

            if filepy[-2:] == "py":
                modulename = os.path.join(self._path,filepy[:-3]).replace(os.sep,".")
                self._modules[filepy[:-3]] = importlib.import_module(modulename)

    def reloadModules(self):
        for key in self._modules:
            reload(self._modules[key])

    @property
    def modules(self):
        return self._modules

    def classes(self):
        for key in self._modules:
            my_class = getattr(self._modules[key], key)
            yield my_class()

##############################################################################3

class _LoggedPage(QWebPage):
    obj = [] # synchronous
    commandRecieved = Signal(str) 
    def javaScriptConsoleMessage(self, msg, line, source):
        l = msg.split(",")
        
        self.obj = l
        if line == 770:
            self.commandRecieved.emit(msg)
        print ('JS: %s line %d: %s' % (source, line, msg))

class Example(QtGui.QFrame):

    def __init__(self):
        super(Example, self).__init__()
        self.initUI()
        self.cwd = os.getcwd()
        self._command = []
        self.registerCmd()
    
    def registerCommand(self, command, method):
        self._command[commamd] = method

    def initUI(self):

        hbox = QtGui.QVBoxLayout()
        #hbox.addStretch()
        plot_view = QWebView()
        self.page = _LoggedPage()
        #page.newData.connect(onNewData)
        self.page.commandRecieved.connect(self.commandRecieved)
        plot_view.setPage(self.page)
        #plot_path = 'test.html'
        dir_path = os.path.dirname(os.path.realpath(__file__))

        plot_view.load(QUrl('file:///%s/ptty.html' % dir_path))
        plot_view_settings = plot_view.settings()
        plot_view_settings.setAttribute(QWebSettings.WebGLEnabled, True)
        plot_view_settings.setAttribute(QWebSettings.DeveloperExtrasEnabled, True)

        hbox.addWidget(plot_view)        
        self.setLayout(hbox)

        self.setWindowTitle('WTerminal')
        self.show()
       
    #############################################################
    #  internal Usefull method
    #############################################################
    def chgPrompt(self, prompt):
        self.page.currentFrame().evaluateJavaScript("setPrompt('%s')" % prompt.replace("\\","/"));
    
    def addTextConsole(self, elm):
        self.page.currentFrame().evaluateJavaScript("addtext('%s')" % elm.replace("\\","/"))

    def addImageConsole(self, elm):
        #self.page.currentFrame().evaluateJavaScript("addtext('%s : <img src=\"%s\" width=\"100px\"/>')" % (os.path.basename(elm), elm.replace("\\","/")))
        self.page.currentFrame().evaluateJavaScript("addtext('<div class=\"gallery\"><a href=\"%s\"><img src=\"%s\" alt=\"%s\" width=100px />%s</a></div>')" % (elm.replace("\\","/"), elm.replace("\\","/"),os.path.basename(elm),os.path.basename(elm)))


    def isImage(self, filename):
       return  os.path.splitext(filename)[1].lower() in [".jpg",".png",".gif",".jpeg"]
        
    def registerCmd(self):
        
        pm = pluginManager(os.path.join(os.path.dirname(__file__),"cmds"))
        for obj in pm.classes():
            self._command.append(obj)
        
    def commandRecieved(self, cmd):
        #print(cmd)
        lstcmd = cmd.split(" ")
        print(lstcmd)
        print(self._command)
        for c in self._command:
            if c.match(lstcmd[0]):
                c.execute(lstcmd,self)
                self.chgPrompt(os.getcwd())        
        """
        if lstcmd[0] in self._command.keys():
            self._command[lstcmd[0]]
            getattr(self, self._command[lstcmd[0]])(lstcmd)
        else:
            self.page.currentFrame().evaluateJavaScript("addtext('command not found')")
        """
    ####################################
    # command ....
    ####################################
    def cd(self, lstarg): 
        os.chdir(lstarg[1])
        self.chgPrompt(os.getcwd())
            
    def pwd(self, lstarg):
        self.addTextConsole(os.getcwd())
        
        
def main():

    app = QtGui.QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
