import os
import sys
import maya.cmds as cmds
import maya.OpenMayaUI as OpenMayaUI 
from shiboken2 import wrapInstance 
import PySide2.QtWidgets as QtWid 
from PySide2 import QtWidgets
from animBuddy import PreferenceUI
reload(PreferenceUI)
from animBuddy import Preference
reload(Preference)
from animBuddy.Install import version
reload(version)
from animBuddy.Install import install
reload(install)
from animBuddy.Install import uninstall
reload(uninstall)
from animBuddy import License
reload(License)

def build(parent, 
          imagesPath, 
          iconSize = 25,
          height = 20, 
          marginSize = 5):
    # adding pref button
    cmds.rowLayout(numberOfColumns = 3)
    cmds.iconTextButton(style = 'iconOnly', 
                        image1 = os.path.join(imagesPath, 'preference.png'), 
                        hi = os.path.join(imagesPath, 'preference_hi.png'),
                        width = iconSize/2, mw = marginSize, height = iconSize, mh = marginSize,
                        label = 'preference',
                        annotation = 'Preference')
    cmds.popupMenu()
    cmds.menuItem(label = "About", c = about)
    cmds.menuItem(label = 'License Number', c = currentLicense)
    cmds.menuItem(label = "Uninstall", c = unInstall)
    cmds.menuItem(label = "Check for update", c = versionCheck)
    cmds.menuItem(divider = True)
    cmds.menuItem(label = "Preference", c = prefUI)
    cmds.menuItem(divider = True)
    cmds.menuItem(label = "Change License Key", c = changeLicence)
    cmds.menuItem(divider = True)
    cmds.menuItem(label = "Close", command = closeUI)
    
    cmds.separator(hr= False, height = height, width = 10, style = "none")
    cmds.setParent("..") 

def getMainWindowPtr(): 
    """
    """
    mayaMainWindowPtr = OpenMayaUI.MQtUtil.mainWindow() 
    mayaMainWindow = wrapInstance(long(mayaMainWindowPtr), QtWid.QWidget) 
    return mayaMainWindow 

def prefUI(*args):
    """
    """

    try:
        cmds.deleteUI("preference_ui")
    except :
        pass

    ui = PreferenceUI.PreferenceUI(parent=getMainWindowPtr())
    ui.setObjectName("preference_ui")
    ui.show()

def versionCheck(*args):
    """
    check version and update
    """
    if version.getVersionDifference():
        question = cmds.confirmDialog(title ='Update', 
                                      message ='New Version is Available\nDo you want to install it?', 
                                      button = ['Yes', 'No'], 
                                      defaultButton='Yes',
                                      cancelButton='No', 
                                      dismissString='No' )
        if question == 'Yes':
            closeUI()
            cmds.evalDeferred("from animBuddy.Install import install;install.run()")
    else:
        cmds.confirmDialog(title ='Update', 
                           message ='No update is available', 
                           button = ['Ok'], 
                           defaultButton='Ok', 
                           dismissString='Ok' )

def about(*args):
    """
    """
    ver = version.getLatestSetupPyFileFromLocal()
    cmds.confirmDialog(title ='Anim Buddy', 
                       message ='Version %s' %ver, 
                       button = ['Ok'], 
                       defaultButton='Ok', 
                       dismissString='Ok' )

def unInstall(*args):
    """
    """
    q = cmds.confirmDialog(title ='Anim Buddy UnInstall', 
                           message ='Do You really want to uninstall?', 
                           button = ['Yes', 'No', 'Cancel'], 
                           defaultButton='Ok', 
                           dismissString='Cancel')   
    if q == 'Yes':
        closeUI()
        uninstall.run()

def closeUI(*args):
    """
    close the toolbar
    """
    if cmds.window('animBuddyWin', ex = True):
        cmds.evalDeferred('cmds.deleteUI("animBuddyWin")')    
    try:
        cmds.evalDeferred('cmds.deleteUI("abToolBar")')  
    except:
        pass

def currentLicense(*args):
    """
    """
    cmds.confirmDialog(title ='License : ', 
                       message = License.License.readLicense(), 
                       button = ['Ok'], 
                       defaultButton='Ok', 
                       dismissString='Ok' )

def changeLicence(*args):
    """
    """
    licenseKey = ""
    result = cmds.promptDialog(title = 'License Registration',
                                message = 'Enter License Key',
                                button = ['ok', 'cancel'],
                                defaultButton = 'ok',
                                cancelButton = 'cancel',
                                dismissString = 'cancel')
    if result == 'ok':
        licenseKey = cmds.promptDialog(q = True, text = True)
    else:
        return

    licenseObj = License.License(licenseKey)
    validator = licenseObj.validate() 
    if validator == 'Invalid':
        print("Invalid License")
        return
    elif validator == 'Expired':
        print("License Expired")
        return
    elif validator == 'Valid':
        License.License.writeLicense(licenseKey)