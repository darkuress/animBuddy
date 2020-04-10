import os
import maya.cmds as cmds
from PySide2 import QtWidgets, QtCore, QtGui
import Core
reload(Core)

class UIData():
    """
    """
    button = None
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
    #- FakeConit---------------------------------------------------------------
    mainLayout = parent
    iconImagePath = os.path.join(imagesPath, 'conit.png').replace('\\', '/')
    iconHoverImagePath = os.path.join(imagesPath, 'conit_hi.png').replace('\\', '/')
    UIData.button = QtWidgets.QPushButton('')
    UIData.button.clicked.connect(fakeConIt)
    UIData.button.setToolTip('Fake Constraint, select source and shift select destination. Right click for Reset Menu')
    UIData.button.setStyleSheet(
    '''
    QPushButton{image:url(%s); border:0px; width:%s; height:%s}
    QPushButton:hover{image:url(%s); border:0px;}
    QPushButton:pressed { background-color: rgba(0, 255,255, 10);}
    ''' %(iconImagePath, iconSize, iconSize, iconHoverImagePath)       
    )             
    UIData.button.show()

    # ---- menuItem
    UIData.button.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
    UIData.button.customContextMenuRequested.connect(popupHandler)
    UIData.popupMenu = QtWidgets.QMenu()
    UIData.popupReset = UIData.popupMenu.addAction("reset")

    mainLayout.addWidget(UIData.button)

def fakeConIt(*args):
    """
    """
    conRun = Core.FakeConIt()
    result = conRun.run()
    if result == 'Success':
        cmds.confirmDialog(title='Fake Conit',
                           message='Fake Constraint was generatec\nRight Click on button to reset connection',
                           button=['Ok'],
                           defaultButton='Ok',
                           dismissString='Ok')
    elif result == 'Failed':
        cmds.confirmDialog(title='Fake Conit',
                           message='please select source and destination(s) to create Fake Constraint',
                           button=['Ok'],
                           defaultButton='Ok',
                           dismissString='Ok')

def popupHandler(position):
    action = UIData.popupMenu.exec_(UIData.button.mapToGlobal(position))  

    #- reset popup
    if action == UIData.popupReset:
        fakeConItReset()

def fakeConItReset(*args):
    """
    """
    conRun = Core.FakeConIt()
    conRun.reset()