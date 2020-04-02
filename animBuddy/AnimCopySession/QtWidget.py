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
    button = None
    popupMenu = None
    menuPose = None
    menuAnim = None
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
    #- Reset It---------------------------------------------------------------
    mainLayout = parent
    iconImagePath = os.path.join(imagesPath, 'copy.png')
    iconHoverImagePath = os.path.join(imagesPath, 'copy_hi.png')
    UIData.button = QtWidgets.QPushButton('')
    UIData.button.clicked.connect(copySession)
    UIData.button.setToolTip("copy current animation or pose. Right click for reset tool. Preserves current session")
    UIData.button.setStyleSheet(
    '''
    QPushButton{image:url(%s); border:0px; width:%s; height:%s}
    QPushButton:hover{image:url(%s); border:0px;}
    QPushButton:pressed { background-color: rgba(0, 255,255, 10);}
    ''' %(iconImagePath, iconSize, iconSize, iconHoverImagePath)       
    )            

    # ---- menuItem
    UIData.button.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
    UIData.button.customContextMenuRequested.connect(popupHandler)
    UIData.popupMenu = QtWidgets.QMenu()
    ag = QtWidgets.QActionGroup(UIData.button, exclusive=True)
    UIData.menuPose = ag.addAction(QtWidgets.QAction('Copy Pose of Current Frame', UIData.popupMenu, checkable=True))
    UIData.popupMenu.addAction(UIData.menuPose)
    UIData.menuAnim = ag.addAction(QtWidgets.QAction('Copy Animation', UIData.popupMenu, checkable=True))
    UIData.popupMenu.addAction(UIData.menuAnim)


    UIData.button.show()
    mainLayout.addWidget(UIData.button)
    readACSMode()

def popupHandler(position):
    action = UIData.popupMenu.exec_(UIData.button.mapToGlobal(position))  
    
    if action == UIData.menuPose:
        writeACSMode('pose')
    elif action == UIData.menuAnim:
        writeACSMode('anim')


def copySession(*args):
    """
    """
    mode = 'pose'
    if UIData.menuAnim.isChecked() == True:
        mode = 'anim'
    copy = Core.AnimCopySession()
    result = copy.run(mode=mode)
    cmds.confirmDialog(title='Anim Copy Session',
                       message='Anim {} done!'.format(result),
                       button=['Ok'],
                       defaultButton='Ok',
                       dismissString='Ok')

def copyReset(*args):
    """
    """
    copy = Core.AnimCopySession()
    copy.reset()


def readACSMode():
    """
    """
    UIData.pref = Preference.Preference()
    if UIData.pref.acsMode == 'pose':
        UIData.menuPose.setChecked(True)
        UIData.menuAnim.setChecked(False)
    elif UIData.pref.acsMode == 'anim':
        UIData.menuPose.setChecked(False)
        UIData.menuAnim.setChecked(True)


def writeACSMode(mode, *args):
    """
    """
    UIData.pref = Preference.Preference()
    UIData.pref.acsMode = mode
    UIData.pref.construct()
    UIData.pref.write()
