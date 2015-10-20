import maya.cmds as cmds
from PySide import QtGui
import maya.OpenMayaUI as mui
import shiboken

def get_maya_window():
    pointer = mui.MQtUtil.mainWindow()
    return shiboken.wrapInstance(long(pointer), QtGui.QWidget)


class ExportTool(QtGui.QMainWindow):
    def __init__(self, parent=get_maya_window()):
        QtGui.QMainWindow.__init__(self, parent)
        
        if cmds.window("Export_tool", exists=True):
            cmds.deleteUI("Export_tool", window=True)
            
        widget = QtGui.QWidget()
        self.setCentralWidget(widget)
        self.setWindowTitle("Export tool")
        self.setObjectName("Export_tool")
        layout = QtGui.QVBoxLayout(widget)
        h_layout = QtGui.QHBoxLayout()
        layout.addLayout(h_layout)
        
        self.setMinimumSize(600, 150)
        self.setMaximumSize(1000, 150)
        
        # Create Widgets
        self.dir_name = QtGui.QLineEdit()
        dir_label = QtGui.QLabel("Directory Path : ")
        button_file = QtGui.QPushButton("Select Directory")
        button_file.clicked.connect(self.on_button_file_clicked)
        self.listExt = QtGui.QListWidget()
        self.listExt.itemClicked.connect(self.on_list_item_clicked)
        
        # Set listExt items:
        for i in ["FBX export", "OBJexport", "mayaAscii", "mayaBinary"]:
            new_item = QtGui.QListWidgetItem()
            new_item.setText(i)
            self.listExt.insertItem(-1, new_item)

        # add Widgets
        h_layout.addWidget(dir_label)
        h_layout.addWidget(self.dir_name)
        h_layout.addWidget(button_file)
        layout.addWidget(self.listExt)
        
        # Add Buttons
        button_export = QtGui.QPushButton("Export")
        button_cancel = QtGui.QPushButton("Cancel")
        button_export.setMaximumWidth(120)
        button_cancel.setMaximumWidth(120)
        button_export.clicked.connect(self.on_button_export_clicked)
        button_cancel.clicked.connect(self.close)
        
        b_layout = QtGui.QHBoxLayout()
        layout.addLayout(b_layout)
        b_layout.addWidget(button_export)
        b_layout.addWidget(button_cancel)
        
        self.show()

    def on_button_file_clicked(self):
        get_directory = QtGui.QFileDialog()
        get_directory.setFileMode(QtGui.QFileDialog.Directory)
        self.path = get_directory.getExistingDirectory()
        self.dir_name.setText(self.path)
     
    def on_list_item_clicked(self):
        item = self.listExt.currentItem()
        self.ext = str(item.text())
    
    def on_button_export_clicked(self):
        print "export"
        selection = cmds.ls(selection=True)
        if selection is False:
            for s in selection:
                cmds.file(self.path+"//"+s, pr=1, type=self.ext, es=1,
                          op="groups=0; ptgroups=0; materials=0; smoothing=0; normals=0")
        else:
            cmds.error('Please Select at least one object to export')
     
myWindow = ExportTool()
