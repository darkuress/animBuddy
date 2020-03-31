import os
import maya.cmds as cmds
from PySide2 import QtWidgets, QtCore, QtGui
from functools import partial
import Core
reload(Core)

class UIData():
    """
    """
    qLineEditShiftKey = None
    popupMenu = None
    popupReset = None

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
    #- Shift key---------------------------------------------------------------
    mainLayout = parent
    layout = QtWidgets.QHBoxLayout()
    layout.setAlignment(QtCore.Qt.AlignCenter) 

    #---- button left
    iconImagePath = os.path.join(imagesPath, 'left.png')
    iconHoverImagePath = os.path.join(imagesPath, 'left_hi.png')
    buttonLeft = QtWidgets.QPushButton('')
    buttonLeft.clicked.connect(partial(shiftKey, "left"))
    buttonLeft.setToolTip("Shift keys to the left")
    buttonLeft.setStyleSheet(
    '''
    QPushButton{image:url(%s); border:0px; width:%s; height:%s}
    QPushButton:hover{image:url(%s); border:0px;}
    QPushButton:pressed { background-color: rgba(0, 255,255, 10);}
    ''' %(iconImagePath, iconSize, iconSize, iconHoverImagePath)       
    )             
    buttonLeft.show()

    #---- textfield
    UIData.qLineEditShiftKey = QtWidgets.QLineEdit()
    UIData.qLineEditShiftKey.setFixedWidth(30)
    UIData.qLineEditShiftKey.setSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
    UIData.qLineEditShiftKey.setText("1")
    UIData.qLineEditShiftKey.setAlignment(QtCore.Qt.AlignCenter)  
    UIData.qLineEditShiftKey.setToolTip('shifting amount, integer is expected')

    # ---- menuItem
    UIData.qLineEditShiftKey.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
    UIData.qLineEditShiftKey.customContextMenuRequested.connect(popupHandler)
    UIData.popupMenu = QtWidgets.QMenu()
    UIData.popupReset = UIData.popupMenu.addAction("reset")

    #---- button right
    iconImagePath = os.path.join(imagesPath, 'right.png')
    iconHoverImagePath = os.path.join(imagesPath, 'right_hi.png')
    buttonRight = QtWidgets.QPushButton('')
    buttonRight.clicked.connect(partial(shiftKey, "right"))
    buttonRight.setToolTip("Shift keys to the right")
    buttonRight.setStyleSheet(
    '''
    QPushButton{image:url(%s); border:0px; width:%s; height:%s}
    QPushButton:hover{image:url(%s); border:0px;}
    QPushButton:pressed { background-color: rgba(0, 255,255, 10);}
    ''' %(iconImagePath, iconSize, iconSize, iconHoverImagePath)       
    )   
    buttonRight.show()

    layout.addWidget(buttonLeft)
    layout.addWidget(UIData.qLineEditShiftKey)
    layout.addWidget(buttonRight)

    mainLayout.addLayout(layout)

def popupHandler(position):
    action = UIData.popupMenu.exec_(UIData.qLineEditShiftKey.mapToGlobal(position))  

    #- reset popup
    if action == UIData.popupReset:
        shiftKeyClear()
        

def shiftKey(mode='right'):
    """
    """
    val = int(UIData.qLineEditShiftKey.text())
    if mode == 'right':
        Core.run(amount=val)
    elif mode == 'left':
        Core.run(amount=-1 * val)


def shiftKeyClear(*args):
    """
    """
    Core.clear()

