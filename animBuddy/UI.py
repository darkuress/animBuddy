import maya.cmds as cmds
import os
from functools import partial
import Preference
reload(Preference)
from Install import version
reload(version)
import License
reload(License)
from Connection import Connection as cn

#- initialize window
if cmds.window('animBuddyWin', ex = True):
    cmds.deleteUI('animBuddyWin')    
try:
    cmds.deleteUI('abToolBar')   
except:
    pass
    
class UI(Preference.Preference):
    """
    Suffix
    EasyInBetween : EIB
    ExFootStep    : EFS
    SelectionGrp  : SGP
    """
    def __init__(self):
        """
        initializing ui
        """
        super(UI, self).__init__()

        #-check license
        self.licenseKey = License.License.readLicense()
        newLicense = False
        if not self.licenseKey:
            result = cmds.promptDialog(title = 'License Registration',
                                       message = 'Enter License Key',
                                       button = ['ok', 'cancel'],
                                       defaultButton = 'ok',
                                       cancelButton = 'cancel',
                                       dismissString = 'cancel')
            if result == 'ok':
                self.licenseKey = cmds.promptDialog(q = True, text = True)
                newLicense = True
            else:
                return
            
        licenseObj = License.License(self.licenseKey)
        self.validator = licenseObj.validate() 
        if self.validator == 'Invalid':
            print "Invalid License"
            return
        elif self.validator == 'Expired':
            print "License Expired"
            return
        elif self.validator == 'Valid':
            if newLicense:
                License.License.writeLicense(self.licenseKey)

        exec(cn.connect('initialize', self.licenseKey))

        self.undoChunk = False

        cmds.frameLayout("main",
                         labelVisible = False,
                         borderVisible = False,
                         bgs = True, 
                         width = 10,
                         marginHeight = 0,
                         marginWidth = 0,
                         labelIndent = 0,
                         collapsable = False)

        self.imagesPath = imagesPath

        # adding widgets
        widgets = ['ShiftKey', 'MicroControl','separator', 
                   'EasyInBetween', 'separator',
                   'FakeConIt', 'ExFootStep', 'MagicLocator', 'SnapIt', 'LockDown', 'vertical',
                   'Decalcomanie', 'ResetIt', 'DrawArc', 'vertical',
                   'SelectionGrp', 'AnimCopySession', 'vertical',
                   'ViewportRefresh', 'bhPlayblast']
        #-mainLayout------------------------------------------------------------------
        self.mainLayout = cmds.rowLayout(numberOfColumns = len(widgets) + 3,
                                         adjustableColumn = 1, 
                                         columnAttach = ([2, 'right', 0]))
        #- logo ---------------------------------------------------------------------
        cmds.image(image = os.path.join(imagesPath, 'beaverLogo.png'))       

        self.sepStyle = 'in'
        self.height = 20
        iconSize = self.iconSize
        self.marginSize = 5
        self.sepWidth = 30
        
        # for freeze tool check 
        cmds.refresh(su = False)

        # ading widgets        
        for widget in widgets:
            self.addWidget(widget)   

        # adding pref button
        cmds.rowLayout(numberOfColumns = 3)
        cmds.separator(hr= False, height = self.height, width = self.sepWidth, style = self.sepStyle)
        self.buttonPref = cmds.iconTextButton(style = 'iconOnly', 
                                              image1 = os.path.join(imagesPath, 'preference.png'), 
                                              hi = os.path.join(imagesPath, 'preference_hi.png'),
                                              width = iconSize/1.7, mw = self.marginSize, height = self.iconSize, mh = self.marginSize,
                                              label = 'preference',
                                              annotation = 'Preference')
        cmds.popupMenu()
        cmds.menuItem(label = "About", c = self.about)
        cmds.menuItem(label = "Check for update", c = self.versionCheck)
        cmds.menuItem(label = "--------------")
        cmds.menuItem(label = "Preference", c = self.prefUI)
        cmds.menuItem(label = "--------------")
        cmds.menuItem(label = "Close", command = self.closeUI)
        
        cmds.separator(hr= False, height = self.height, width = 10, style = "none")
        cmds.setParent("..") 
   
    def prefUI(self, *args):
        """
        """
        import PreferenceUI
        reload(PreferenceUI)
        try:
            self.ui.deleteLater()
        except:
            pass
        
        self.ui = PreferenceUI.PreferenceUI()
        
        try:
            self.ui.show()
        except:
            self.ui.deleteLater()

    def versionCheck(self, *args):
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
                from Install import install
                reload(install)
                install.run()
        else:
            cmds.confirmDialog(title ='Update', 
                               message ='No update is available', 
                               button = ['Ok'], 
                               defaultButton='Ok', 
                               dismissString='Ok' )
   
    def about(self, *args):
        """
        """
        ver = version.getLatestSetupPyFileFromLocal()
        cmds.confirmDialog(title ='Anim Buddy', 
                           message ='Version %s' %ver, 
                           button = ['Ok'], 
                           defaultButton='Ok', 
                           dismissString='Ok' )

    def closeUI(self, *args):
        """
        close the toolbar
        """
        if cmds.window('animBuddyWin', ex = True):
            cmds.deleteUI('animBuddyWin')    
        try:
            cmds.deleteUI('abToolBar')   
        except:
            pass

    def addWidget(self, module):
        """
        """
        if module == 'separator':
            cmds.separator(height = 10, width = 10, style = 'none')
        elif module == 'vertical':
            cmds.separator(hr= False, height = self.height, width = self.sepWidth, style = self.sepStyle)
        else:
            exec("from {} import Widget".format(module))
            exec("reload(Widget)")
            Widget.build(self.mainLayout, 
                         self.imagesPath,
                         iconSize = self.iconSize,
                         height = self.height, 
                         marginSize = self.marginSize)

    def loadInMaya(self, *args):
        """
        """
        # Running
        if self.validator == 'Valid':
            exec(cn.connect('runUI', self.licenseKey))

