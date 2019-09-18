# genericshelltoolboxpython
This project want to provide a generic terminal with a html display. 
It should be multi platform.
It's writen with python / Qt / WebKit.

This project gibr a toolbox to make an app shell terminal with command are written in python as plugin class in cmds directory.

Then this commands could be invoke in the sheel window , the result could be Html showing the pseudo terminal.
The scrollbar will automaticly set to bottom.

User write command intercept in webkit window , send it to python , the result is give to the webpage by js.

![After Launch](screenshot4.gif)

# Archi 
![After Launch](archi.jpg)

Dependencies:
* python 
* pyside
* PySide.QtWebKit

html/js

* jquery 
* simplelightbox

### Command 
* clear internal of js ptty
* ls 


### Todo 
A lot of thing
