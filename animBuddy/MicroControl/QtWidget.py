import os
import maya.cmds as cmds
from PySide2 import QtWidgets, QtCore, QtGui
from functools import partial
import Core
reload(Core)

class UIData():
    """
    """
    qLineEditMc = None

def build(parent, 
          imagesPath, 
          iconSize = 25,
          height = 20, 
          marginSize = 5):
    """
    build widget
    @param parent : parent qt layout
    @imagesPath : str path
    """
    #- Micro Control---------------------------------------------------------------
    mainLayout = parent


    hlayout = QtWidgets.QHBoxLayout()
    vlayout = QtWidgets.QVBoxLayout()
    hlayout.setAlignment(QtCore.Qt.AlignCenter) 

    #---- button up
    iconImagePath = os.path.join(imagesPath, 'uparrow.png')
    iconHoverImagePath = os.path.join(imagesPath, 'uparrow_hi.png')
    buttonUp = QtWidgets.QPushButton('')
    buttonUp.setSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
    buttonUp.setFixedHeight(iconSize/2.5)
    buttonUp.clicked.connect(partial(microControlRun, "add"))
    buttonUp.setToolTip("Micro Control add Value")
    buttonUp.setStyleSheet(
    '''
    QPushButton{image:url(%s); border:0px; width:%s; height:%s/2}
    QPushButton:hover{image:url(%s); border:0px;}
    QPushButton:pressed { background-color: rgba(0, 255,255, 10);}
    ''' %(iconImagePath, iconSize, iconSize, iconHoverImagePath)       
    )             
    buttonUp.show()

    #---- button down
    iconImagePath = os.path.join(imagesPath, 'dnarrow.png')
    iconHoverImagePath = os.path.join(imagesPath, 'dnarrow_hi.png')
    buttonDn = QtWidgets.QPushButton('')
    buttonDn.setSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
    buttonDn.setFixedHeight(iconSize/2.5)
    buttonDn.clicked.connect(partial(microControlRun, "sub"))
    buttonDn.setToolTip("Micro Control substract Value")
    buttonDn.setStyleSheet(
    '''
    QPushButton{image:url(%s); border:0px; width:%s; height:%s/2}
    QPushButton:hover{image:url(%s); border:0px;}
    QPushButton:pressed { background-color: rgba(0, 255,255, 10);}
    ''' %(iconImagePath, iconSize, iconSize, iconHoverImagePath)       
    )             
    buttonDn.show()

    #---- textfield
    UIData.qLineEditMc = QtWidgets.QLineEdit()
    UIData.qLineEditMc.setFixedWidth(30)
    UIData.qLineEditMc.setSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
    UIData.qLineEditMc.setText("1")
    UIData.qLineEditMc.setAlignment(QtCore.Qt.AlignCenter)  
    UIData.qLineEditMc.setToolTip('shifting amount, integer is expected')
    UIData.qLineEditMc.setStyleSheet(
    '''
    QLineEdit { background-color: #333333; }
    '''   
    )

    hlayout.addWidget(UIData.qLineEditMc)
    vlayout.addWidget(buttonUp)
    vlayout.addWidget(buttonDn)
    hlayout.addLayout(vlayout)

    mainLayout.addLayout(hlayout)

def microControlRun(mode, *args):
    """
    @param mode string "add" or "sub"
    """
    val = round(float((UIData.qLineEditMc.text())), 3)
    if mode == "add":
        Core.run(val)
    else:
        Core.run(val*-1)

