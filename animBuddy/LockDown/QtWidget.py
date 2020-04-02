import os
import maya.cmds as cmds
from PySide2 import QtWidgets, QtCore, QtGui
from animBuddy import Preference
from functools import partial
import Core
reload(Core)

class UIData():
    """
    """
    qLineEditLockdown = None
    popupMenu = None
    menuTr = None
    menuRo = None
    menuBo = None
    popupReset = None
    pref = None

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
    #- Lockdown---------------------------------------------------------------
    mainLayout = parent
    layout = QtWidgets.QHBoxLayout()
    layout.setAlignment(QtCore.Qt.AlignCenter) 

    #---- button reverse
    iconImagePath = os.path.join(imagesPath, 'lockdown_reverse.png')
    iconHoverImagePath = os.path.join(imagesPath, 'lockdown_reverse_hi.png')
    buttonLeft = QtWidgets.QPushButton('')
    buttonLeft.clicked.connect(partial(run, 'reverse'))
    buttonLeft.setToolTip("lock reverse")
    buttonLeft.setStyleSheet(
    '''
    QPushButton{image:url(%s); border:0px; width:%s; height:%s}
    QPushButton:hover{image:url(%s); border:0px;}
    QPushButton:pressed { background-color: rgba(0, 255,255, 10);}
    ''' %(iconImagePath, iconSize, iconSize, iconHoverImagePath)       
    )             
    buttonLeft.show()

    #---- textfield
    UIData.qLineEditLockdown = QtWidgets.QLineEdit()
    UIData.qLineEditLockdown.setFixedWidth(30)
    UIData.qLineEditLockdown.setSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
    UIData.qLineEditLockdown.setText("3")
    UIData.qLineEditLockdown.setAlignment(QtCore.Qt.AlignCenter)  
    UIData.qLineEditLockdown.setToolTip('shifting amount, integer is expected')
    UIData.qLineEditLockdown.setStyleSheet(
    '''
    QLineEdit { background-color: #333333; }
    '''   
    )

    # ---- menuItem
    UIData.qLineEditLockdown.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
    UIData.qLineEditLockdown.customContextMenuRequested.connect(popupHandler)
    UIData.popupMenu = QtWidgets.QMenu()

    ag = QtWidgets.QActionGroup(UIData.qLineEditLockdown, exclusive=True)
    UIData.menuTr = ag.addAction(QtWidgets.QAction('Translate Only', UIData.popupMenu, checkable=True))
    UIData.popupMenu.addAction(UIData.menuTr)
    UIData.menuRo = ag.addAction(QtWidgets.QAction('Rotate Only', UIData.popupMenu, checkable=True))
    UIData.popupMenu.addAction(UIData.menuRo)
    UIData.menuBo = ag.addAction(QtWidgets.QAction('Both', UIData.popupMenu, checkable=True))
    UIData.popupMenu.addAction(UIData.menuBo)

    UIData.popupMenu.addSeparator()
    UIData.popupReset = UIData.popupMenu.addAction("clear key")

    #---- button forward
    iconImagePath = os.path.join(imagesPath, 'lockdown_forward.png')
    iconHoverImagePath = os.path.join(imagesPath, 'lockdown_forward_hi.png')
    buttonRight = QtWidgets.QPushButton('')
    buttonRight.clicked.connect(partial(run, 'forward'))
    buttonRight.setToolTip("lock forward")
    buttonRight.setStyleSheet(
    '''
    QPushButton{image:url(%s); border:0px; width:%s; height:%s}
    QPushButton:hover{image:url(%s); border:0px;}
    QPushButton:pressed { background-color: rgba(0, 255,255, 10);}
    ''' %(iconImagePath, iconSize, iconSize, iconHoverImagePath)       
    )   
    buttonRight.show()

    layout.addWidget(buttonLeft)
    layout.addWidget(UIData.qLineEditLockdown)
    layout.addWidget(buttonRight)

    mainLayout.addLayout(layout)
    readLDNMode()

def popupHandler(position):
    action = UIData.popupMenu.exec_(UIData.qLineEditLockdown.mapToGlobal(position))  

    #- clear popup
    if action == UIData.popupReset:
        clearKey()
    if action == UIData.menuTr:
        writeLDNMode('translate')
    elif action == UIData.menuRo:
        writeLDNMode('rotate')
    elif action == UIData.menuBo:
        writeLDNMode('both')

def run(mode, *args):
    """
    """
    doReverse = False
    doTranslate = True
    doRotate = True

    frame = int(UIData.qLineEditLockdown.text())

    if mode == 'reverse':
        doReverse = True   
    if UIData.menuTr.isChecked():
        doTranslate = True
        doRotate = False
    elif UIData.menuRo.isChecked():
        doTranslate = False
        doRotate = True
    
    Core.run(frame = frame,
             doTranslate = doTranslate, 
             doRotate = doRotate,
             doReverse = doReverse)

def clearKey(*args):
    """
    """
    Core.clearKey()      

def clearKey(*args):
    """
    """
    Core.clearKey()

def readLDNMode():
    """
    """
    UIData.pref = Preference.Preference()
    if UIData.pref.ldnMode == 'translate':
        UIData.menuTr.setChecked(True)
        UIData.menuRo.setChecked(False)
        UIData.menuBo.setChecked(False)
    elif UIData.pref.ldnMode == 'rotate':
        UIData.menuTr.setChecked(False)
        UIData.menuRo.setChecked(True)
        UIData.menuBo.setChecked(False)
    elif UIData.pref.ldnMode == 'both':
        UIData.menuTr.setChecked(False)
        UIData.menuRo.setChecked(False)
        UIData.menuBo.setChecked(True)


def writeLDNMode(mode, *args):
    """
    """
    UIData.pref = Preference.Preference()
    UIData.pref.ldnMode = mode
    UIData.pref.construct()
    UIData.pref.write()