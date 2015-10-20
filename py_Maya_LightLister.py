import maya.cmds as cmds
from PySide import QtGui
import maya.OpenMayaUI as mui
import shiboken
import os

class UI(object):

    def __init__(self):

        self.lights_in_scene()
        self.create_ui()

    def maya_main_window(self):
        pointer = mui.MQtUtil.mainWindow()
        return shiboken.wrapInstance(long(pointer), QtGui.QWidget)

    def lights_in_scene(self):
        """List Lights in scene """

        cmds.select(clear=True)

        self.lights = cmds.ls(type="light")
        if self.lights is False:
            cmds.error("No light in scene")
        cmds.select(self.lights, add=True)
        self.all_lights = cmds.ls(sl=True)

        self.list_spot = []
        self.list_vray = []
        self.list_standard = []

        for s in self.all_lights:
            if cmds.objectType(s, isType='spotLight'):
                self.list_spot.append(s)
            elif cmds.objectType(s, isType='VrayLight'):
                self.list_vray.append(s)
            else:
                self.list_standard.append(s)
        cmds.select(clear=True)
        self.sp_len = len(self.list_spot)
        self.vr_len = len(self.list_vray)
        self.sd_len = len(self.list_standard)

        cmds.select(self.all_lights[-1])

    def create_ui(self):
        # create a window
        parent = self.maya_main_window()
        self.window = QtGui.QMainWindow(parent)
        self.window.setWindowTitle("Light Lister")
        object_name = "pyLightLister"
        self.window.setObjectName(object_name)

        self.height = self.sp_len*40 + self.vr_len*40 + self.sd_len*40 + 200
        self.window.setMinimumSize(1000, self.height)
        self.window.setMaximumSize(1000, self.height)

        widget = QtGui.QWidget()
        self.window.setCentralWidget(widget)
        vertical_layout = QtGui.QVBoxLayout(widget)

        # Create a list of Lights for each type (if in scene):
        if self.list_standard != []:

            sd_title = QtGui.QHBoxLayout()
            sd_title.setContentsMargins(17, 0, 0, 0)
            os.chdir("C:/Users/BRES/Documents/Python")
            path = os.getcwd()
            filename = path+"\\titre_sd.png"
            image = QtGui.QPixmap(filename)
            label_img=QtGui.QLabel()
            label_img.setPixmap(image)
            sd_title.addWidget(label_img)

            vertical_layout.addLayout(sd_title)
            list_layout_sd = QtGui.QHBoxLayout()
            self.sd_list = QtGui.QListWidget()
            list_layout_sd.addWidget(self.sd_list)

            for i in self.list_standard:
                new_item = QtGui.QListWidgetItem()
                new_item.setText(i)
                self.sd_list.insertItem(-1,new_item)
            self.sd_list.setMinimumSize(950, self.sd_len * 30)
            self.sd_list.setMaximumSize(950, self.sd_len * 30)

            self.sd_list.itemClicked.connect(self.sd_connect)
            vertical_layout.addLayout(list_layout_sd)

        if self.list_spot != []:
            sp_title = QtGui.QHBoxLayout()
            sp_title.setContentsMargins(17, 0, 0, 0)
            os.chdir("C:/Users/BRES/Documents/Python")
            path = os.getcwd()
            filename = path+"\\titre_sp.png"
            image = QtGui.QPixmap(filename)
            label_img = QtGui.QLabel()
            label_img.setPixmap(image)
            sp_title.addWidget(label_img)

            vertical_layout.addLayout(sp_title)
            list_layout_sp = QtGui.QHBoxLayout()
            self.sp_list = QtGui.QListWidget()
            list_layout_sp.addWidget(self.sp_list)

            for i in self.list_spot:
                new_item = QtGui.QListWidgetItem()
                new_item.setText(i)
                self.sp_list.insertItem(-1,new_item)
            self.sp_list.setMinimumSize(950,self.sp_len * 30)
            self.sp_list.setMaximumSize(950,self.sp_len * 30)

            self.sp_list.itemClicked.connect(self.sp_connect)
            vertical_layout.addLayout(list_layout_sp)

        if self.list_vray != []:

            vr_title = QtGui.QHBoxLayout()
            os.chdir("C:/Users/BRES/Documents/Python")
            path = os.getcwd()
            filename = path+"\\titre_vr.png"
            image = QtGui.QPixmap(filename)
            label_img=QtGui.QLabel()
            label_img.setPixmap(image)
            vr_title.addWidget(label_img)

            vertical_layout.addLayout(vr_title)
            list_layout_vr= QtGui.QHBoxLayout()
            self.vr_list = QtGui.QListWidget()
            list_layout_vr.addWidget(self.vr_list)

            for i in self.list_vray:
                new_item = QtGui.QListWidgetItem()
                new_item.setText(i)
                self.vr_list.insertItem(-1,new_item)
            self.vr_list.setMinimumSize(950, self.vr_len * 30)
            self.vr_list.setMaximumSize(950, self.vr_len * 30)

            self.vr_list.itemClicked.connect(self.vr_connect)

            vertical_layout.addLayout(list_layout_vr)


        def create_light_layout():
            """Light Parameters"""

            titles = QtGui.QHBoxLayout()
            filename = path+"\\titre_light.png"
            image = QtGui.QPixmap(filename)

            label_img = QtGui.QLabel()
            label_img.setPixmap(image)
            titles.addWidget(label_img)

            vertical_layout.addLayout(titles)
            layout = QtGui.QHBoxLayout()
            layout.setContentsMargins(20, 0, 20, 30)
            vertical_layout.addLayout(layout)

            # Transform Color Type
            c = self.colorL
            c = str(c[0])
            c = c.split(",")
            r = c[0]
            r = r.split("(")
            r = r[-1]
            r = float(r)
            g = c[1]
            g = float(g)
            b = c[-1]
            b = b.split(")")
            b = b[0]
            b = float(b)
            self.clr_l = QtGui.QColor()
            self.clr_l.setRgbF(r, g, b)

            self.color = QtGui.QPushButton()
            self.color.clicked.connect(self.choose_color)
            self.color.setMinimumSize(25, 25)
            self.color.setMaximumSize(25, 25)

            self.multi = QtGui.QDoubleSpinBox()
            self.multi.setMaximumWidth(70)
            self.multi.setMinimumWidth(70)
            self.multi.setMinimum(-100000)
            self.multi.setMaximum(100000)
            self.multi.valueChanged.connect(self.set_multi)

            self.visibility = QtGui.QCheckBox()
            self.visibility.setMaximumWidth(20)
            self.visibility.setMinimumWidth(20)
            self.visibility.stateChanged.connect(self.set_vis)

            self.map = QtGui.QSpinBox()
            self.map.setMinimum(0)
            self.map.setMaximum(100000)
            self.map.setMaximumWidth(70)
            self.map.setMinimumWidth(70)
            self.map.setEnabled(False)
            self.map.valueChanged.connect(self.set_map)

            self.bias = QtGui.QDoubleSpinBox()
            self.bias.setMinimum(0.001)
            self.bias.setMaximumWidth(70)
            self.bias.setMinimumWidth(70)
            self.bias.setDecimals(3)
            self.bias.setEnabled(False)
            self.bias.valueChanged.connect(self.set_bias)

            self.diffuse = QtGui.QCheckBox()
            self.diffuse.setMaximumWidth(30)
            self.diffuse.setMinimumWidth(30)
            self.diffuse.stateChanged.connect(self.set_affect)
            self.spec = QtGui.QCheckBox()
            self.spec.setMaximumWidth(20)
            self.spec.setMinimumWidth(20)
            self.spec.stateChanged.connect(self.set_affect)

            self.shadow = QtGui.QComboBox()
            self.shadow.setMaximumWidth(130)
            self.shadow.setMinimumWidth(130)
            self.shadow.addItems(["Ray Trace Shadows", "Depth Map Shadows", "None"])
            self.shadow.activated[str].connect(self.on_shadow_map)

            self.decay = QtGui.QComboBox()
            self.decay.setMaximumWidth(100)
            self.decay.setMinimumWidth(100)
            self.decay.addItems(["No Decay", "Linear", "Quadratic", "Cubic"])
            self.decay.setCurrentIndex(self.decayL)
            self.decay.activated[str].connect(self.set_decay)

            # Set Attributes
            self.set_attributes()

            # Add Widgets :
            for n in self.color, self.multi, self.visibility, self.shadow, self.map, \
                     self.bias, self.decay, self.diffuse, self.spec:
                layout.addWidget(n)

            if self.list_vray is not False:
                self.subdivs = QtGui.QSpinBox()
                self.subdivs.setMaximumWidth(70)
                self.subdivs.setMinimumWidth(70)
                self.subdivs.setMinimum(0)
                try:
                    self.subdivs.setValue(self.subdivL)
                except Exception:
                    pass
                layout.addWidget(self.subdivs)

            self.angle = QtGui.QDoubleSpinBox()
            self.angle.setMaximumWidth(70)
            self.angle.setMinimumWidth(70)
            self.angle.setMaximum(180)
            self.angle.setDecimals(3)
            self.angle.valueChanged.connect(self.set_angle)

            self.penumbra = QtGui.QDoubleSpinBox()
            self.penumbra.setMaximumWidth(70)
            self.penumbra.setMinimumWidth(70)
            self.penumbra.setMinimum(-10)
            self.penumbra.setMaximum(10)
            self.penumbra.setDecimals(3)
            self.penumbra.valueChanged.connect(self.set_penumbra)

            self.dropoff = QtGui.QDoubleSpinBox()
            self.dropoff.setMaximumWidth(70)
            self.dropoff.setMinimumWidth(70)
            self.dropoff.setMinimum(0)
            self.dropoff.setMaximum(255)
            self.dropoff.setDecimals(3)
            self.dropoff.valueChanged.connect(self.set_dropoff)

            layout.addWidget(self.angle)
            layout.addWidget(self.penumbra)
            layout.addWidget(self.dropoff)

        # Get Attributes
        self.get_attributes()

        # Create Parameters
        create_light_layout()

        # Create Buttons
        button_layout = QtGui.QHBoxLayout()
        vertical_layout.addLayout(button_layout)
        rbutton = QtGui.QPushButton("Reload")
        rbutton.setMaximumWidth(300)
        rbutton.setMinimumWidth(300)
        rbutton.clicked.connect(self.on_reload)
        cbutton = QtGui.QPushButton("Close")
        cbutton.setMaximumWidth(150)
        cbutton.setMinimumWidth(150)
        cbutton.clicked.connect(self.window.close)

        button_layout.addWidget(rbutton)
        button_layout.addWidget(cbutton)

        self.window.show()

    def set_attributes(self):

        self.multi.setValue(self.multiL)
        self.color.setStyleSheet("QPushButton {background-color: %s}" %self.clr_l.name())
        self.spec.setChecked(self.specL)
        self.diffuse.setChecked(self.diffuseL)
        self.bias.setValue(self.biasL)
        self.visibility.setChecked(self.visL)
        self.map.setValue(self.mapL)
        if self.rayShadowL == 0 and self.mapShadowL == 0:
            self.shadow.setCurrentIndex(2)
        elif self.rayShadowL == 1:
            self.shadow.setCurrentIndex(0)
            self.bias.setEnabled(False)
            self.map.setEnabled(False)
        elif self.mapShadowL == 1:
            self.shadow.setCurrentIndex(1)
            self.bias.setEnabled(True)
            self.map.setEnabled(True)
        try :
            self.angle.setValue(self.coneL)
            self.penumbra.setValue(self.penumL)
            self.dropoff.setValue(self.dropL)
        except Exception:
            pass

    def get_attributes(self):

        self.multiL = cmds.getAttr(".intensity")
        self.colorL = cmds.getAttr(".color")
        self.visL = cmds.getAttr(".visibility")
        self.decayL = cmds.getAttr(".decayRate")
        self.diffuseL = cmds.getAttr(".emitDiffuse")
        self.specL = cmds.getAttr(".emitSpecular")
        self.mapL = cmds.getAttr(".dmapResolution")
        self.biasL = cmds.getAttr(".dmapBias")
        self.mapShadowL = cmds.getAttr(".useDepthMapShadows")
        self.rayShadowL = cmds.getAttr(".useRayTraceShadows")
        try:
            self.coneL = cmds.getAttr(".coneAngle")
            self.penumL = cmds.getAttr(".penumbraAngle")
            self.dropL = cmds.getAttr(".dropoff")
            self.subdivL = cmds.getAttr(".subdivisions")
        except Exception:
            pass

    def sd_connect(self):
        if self.list_vray != []:
            self.VRlist.clearSelection()
        if self.list_spot != []:
            self.sp_list.clearSelection()
        current = self.sd_list.currentItem()
        self.selectedItem = current.text()
        cmds.select(self.selectedItem)
        self.angle.setEnabled(False)
        self.penumbra.setEnabled(False)
        self.dropoff.setEnabled(False)
        self.get_attributes()
        self.set_attributes()

    def sp_connect(self):
        if self.list_standard != []:
            self.sd_list.clearSelection()
        if self.list_vray != []:
            self.vr_list.clearSelection()
        current = self.sp_list.currentItem()
        self.selectedItem = current.text()
        cmds.select(self.selectedItem)
        self.angle.setEnabled(True)
        self.penumbra.setEnabled(True)
        self.dropoff.setEnabled(True)
        self.get_attributes()
        self.set_attributes()

    def vr_connect(self):
        if self.list_standard != []:
            self.sd_list.clearSelection()
        if self.list_spot != []:
            self.sp_list.clearSelection()
        current = self.vr_list.currentItem()
        self.selectedItem = current.text()
        cmds.select(self.selectedItem)
        self.angle.setEnabled(False)
        self.penumbra.setEnabled(False)
        self.dropoff.setEnabled(False)
        self.get_attributes()
        self.set_attributes()

    def set_multi(self):
            cmds.setAttr(".intensity", self.multi.value())

    def set_vis(self):
            cmds.setAttr(".visibility", self.visibility.isChecked())

    def on_shadow_map(self):
        if str(self.shadow.currentText()) == "Depth Map Shadows":
            self.map.setEnabled(True)
            self.bias.setEnabled(True)

        else:
            self.map.setEnabled(False)
            self.bias.setEnabled(False)

    def choose_color(self):
        self.col = QtGui.QColorDialog.getColor()
        self.R = self.col.red()
        self.G = self.col.green()
        self.B = self.col.blue()
        print type(self.col.name())
        if self.col.isValid():
            self.color.setStyleSheet("QPushButton {background-color: %s}" %self.col.name())
            cmds.setAttr(".color", self.R, self.G, self.B, type ="double3")

    def set_map(self):
        self.mp = self.map.value()
        cmds.setAttr(".dmapResolution", self.mp)

    def set_bias(self):
        self.bs = self.bias.value()
        cmds.setAttr(".dmapBias", self.bs)

    def set_affect(self):
        self.dif = self.diffuse.isChecked()
        cmds.setAttr(".emitDiffuse", self.dif)
        self.sp = self.spec.isChecked()
        cmds.setAttr(".emitSpecular", self.sp)

    def set_decay(self):
        self.dc = self.decay.currentIndex()
        try:
            cmds.setAttr(".decayRate", self.dc)
        except Exception:
            pass

    def set_angle(self):
        self.an = self.angle.value()
        try:
            cmds.setAttr(".coneAngle", self.an)
        except Exception:
            pass

    def set_penumbra(self):
        self.pe = self.penumbra.value()
        try:
            cmds.setAttr(".penumbraAngle", self.pe)
        except Exception:
            pass

    def set_dropoff(self):
        self.dr = self.dropoff.value()
        try:
            cmds.setAttr(".dropoff", self.dr)
        except Exception:
            pass

    def on_reload(self):
        self.window.close()
        self.__init__()

test = UI()
