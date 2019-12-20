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
    """
    def __init__(self):
        """
        initializing ui
        """
        super(UI, self).__init__()

        #-check license
        self.licenseKey = License.License.readLicense()
        self.validator = ''
        
        if not self.licenseKey:
            self.licenseValidation()

        if not self.licenseKey:
            return

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
                   'MagicLocator', 'FakeConIt', 'ExFootStep', 'SnapIt', 'LockDown', 'vertical',
                   'Decalcomanie', 'ResetIt', 'DrawArc', 'vertical',
                   'SelectionGrp', 'AnimCopySession', 'vertical',
                   'ViewportRefresh', 'bhPlayblast', 'vertical',
                   'Misc']
        #-mainLayout------------------------------------------------------------------
        self.mainLayout = cmds.rowLayout(numberOfColumns = len(widgets) + 2,
                                         adjustableColumn = 1, 
                                         columnAttach = ([2, 'right', 0]))
        #- logo ---------------------------------------------------------------------
        cmds.image(image = os.path.join(imagesPath, 'beaverLogo.png'), w = 96, h = 81)       

        self.sepStyle = 'in'
        self.height = 20
        self.marginSize = 0
        self.sepWidth = 30
        
        # for freeze tool check 
        cmds.refresh(su = False)

        # ading widgets        
        for widget in widgets:
            self.addWidget(widget)   

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

    def licenseKeyDialog(self):
        """
        """
        result = cmds.promptDialog(title = 'License Registration',
                                    message = 'Enter License Key',
                                    button = ['ok', 'cancel'],
                                    defaultButton = 'ok',
                                    cancelButton = 'cancel',
                                    dismissString = 'cancel')
        if result == 'ok':
            if cmds.promptDialog(q = True, text = True):
                return cmds.promptDialog(q = True, text = True)
            else:
                return "dummyString"
        else:
            return False       

    def licenseValidation(self):
        """
        """
        self.licenseKey = self.licenseKeyDialog()

        if self.licenseKey:
            licenseObj = License.License(self.licenseKey)
            self.validator = licenseObj.validate() 

            if self.validator == 'Invalid':
                print("Invalid License")
                self.licenseValidation()
            elif self.validator == 'Expired':
                print("License Expired")
                self.licenseValidation()
            elif self.validator == 'Valid':
                License.License.writeLicense(self.licenseKey)

    def loadInMaya(self, *args):
        """
        """
        # Running
        exec(cn.connect('runUI', self.licenseKey))

