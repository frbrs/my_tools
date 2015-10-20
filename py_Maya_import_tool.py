import maya.cmds as cmds 
from PySide import QtGui
from PySide import QtCore


def import_tool():
    filedial = QtGui.QFileDialog()
    files = filedial.getOpenFileNames()
    dir_name = filedial.directory()
    files = files[0]
    if files is False:
        cmds.warning("No files found")
    
    for f in files: 
        print f
        try:
            cmds.file(f, i=True)
        except:
            pass

import_tool()   
