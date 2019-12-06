from PySide2.QtWidgets import *
from maya import OpenMayaUI as omui
from PySide2 import QtCore
from PySide2 import QtGui
from PySide2 import __version__
from shiboken2 import wrapInstance 

import Preference
reload(Preference)

try:
    import maya.cmds as cmds
except: 
    pass

class PreferenceUI(QDialog):
    """"""
 
    def __init__(self, parent=None):
        """Constructor"""
        super(PreferenceUI, self).__init__(parent)

        self.pref = Preference.Preference()

        mainLayout = QVBoxLayout()
 
        layoutIconSize          = QGridLayout()
        labelIconSize           = QLabel("Icon Size")
        self.lineEditIconSize   = QLineEdit("")
        self.lineEditIconSize.setFixedWidth(80)
        self.lineEditIconSize.setText(str(self.pref.iconSize))
        layoutIconSize.addWidget(labelIconSize, 0, 0)
        layoutIconSize.addWidget(self.lineEditIconSize, 0, 1)
        #layoutIconSize.setSpacing(20)

        layoutSplitter1 = QHBoxLayout()
        splitter1 = QSplitter(QtCore.Qt.Horizontal)
        splitter1.setStretchFactor(1, 10)
        layoutSplitter1.addWidget(splitter1)

        layoutLineWidth         = QGridLayout()
        labelLineWidth          = QLabel("Motion Trail Line Width")
        self.lineEditLineWidth  = QLineEdit("")
        self.lineEditLineWidth.setFixedWidth(80)
        self.lineEditLineWidth.setText(str(round(self.pref.lineWidth, 2)))
        layoutLineWidth.addWidget(labelLineWidth, 0, 0)
        layoutLineWidth.addWidget(self.lineEditLineWidth, 0, 1)

        layoutDotSize           = QGridLayout()
        labelDotSize            = QLabel("Motion Trail Dot Size")
        self.lineEditDotSize    = QLineEdit("")
        self.lineEditDotSize.setFixedWidth(80)
        self.lineEditDotSize.setText(str(round(self.pref.dotSize, 2)))
        layoutDotSize.addWidget(labelDotSize, 0, 0)
        layoutDotSize.addWidget(self.lineEditDotSize, 0, 1)
 
        layoutKeyFrame          = QGridLayout()
        labelKeyFrame           = QLabel("Motion Trail KeyFrame Size")
        self.lineEditKeyFrame   = QLineEdit("")
        self.lineEditKeyFrame.setFixedWidth(80)
        self.lineEditKeyFrame.setText(str(round(self.pref.keyFrameSize, 2)))
        layoutKeyFrame.addWidget(labelKeyFrame, 0, 0)
        layoutKeyFrame.addWidget(self.lineEditKeyFrame, 0, 1)
        #layoutKeyFrame.setSpacing(18)

        layoutTimeBuffer        = QGridLayout()
        labelTimeBuffer         = QLabel("Motion Trail Time Bufffe Size")
        self.lineEditTimeBuffer = QLineEdit("")
        self.lineEditTimeBuffer.setFixedWidth(80)
        self.lineEditTimeBuffer.setText(str(round(self.pref.timeBuffer, 0)).split('.')[0])
        layoutTimeBuffer.addWidget(labelTimeBuffer, 0, 0)
        layoutTimeBuffer.addWidget(self.lineEditTimeBuffer, 0, 1)
        #layoutTimeBuffer.setSpacing(18)

        buttonApply = QPushButton('Apply')
 
        mainLayout.addLayout(layoutIconSize,   stretch=1)
        mainLayout.addLayout(layoutSplitter1,  stretch=1)
        mainLayout.addLayout(layoutLineWidth,    stretch=1)
        mainLayout.addLayout(layoutDotSize,    stretch=1)
        mainLayout.addLayout(layoutKeyFrame,   stretch=1)
        mainLayout.addLayout(layoutTimeBuffer, stretch=1)
        mainLayout.addWidget(buttonApply)
        self.setLayout(mainLayout)
    
        #- connect signal 
        buttonApply.clicked.connect(self.apply)

    def apply(self):
        """
        """
        self.pref.iconSize     = int(self.lineEditIconSize.text())
        self.pref.lineWidth    = float(self.lineEditLineWidth.text())
        self.pref.dotSize      = float(self.lineEditDotSize.text())
        self.pref.keyFrameSize = float(self.lineEditKeyFrame.text())
        self.pref.timeBuffer   = int(self.lineEditTimeBuffer.text())

        self.pref.construct()
        self.pref.write()

if __name__ == "__main__":
    app = QApplication([])
    form = PreferenceUI()
    form.show()
    sys.exit(app.exec_())