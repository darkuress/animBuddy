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

        # adding widgets
        widgets = ['Justin', 'Warrior', 'vertical', 
                   'ShiftKey', 'MicroControl','vertical', 
                   'EasyInBetween', 'vertical',
                   'MagicLocator', 'separator', 'FakeConIt', 'separator', 'ExFootStep', 'separator', 'SnapIt', 'separator', 'LockDown', 'vertical',
                   'Decalcomanie', 'separator', 'ResetIt', 'separator', 'DrawArc', 'vertical',
                   'SelectionGrp', 'separator', 'AnimCopySession', 'vertical',
                   'ViewportRefresh', 'separator', 'bhPlayblast', 'vertical',
                   'Misc']
        #-mainLayout------------------------------------------------------------------
        self.mainLayout = cmds.rowLayout(numberOfColumns = len(widgets) + 2,
                                         adjustableColumn = 1, 
                                         columnAttach = ([2, 'right', 0]))
        #- logo ---------------------------------------------------------------------
        cmds.image(image = os.path.join(imagesPath, 'beaverLogo.png'), w = 48, h = 41)       

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
            self.iconSize = 20
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
                                   button = ['ok', 'Request License Key', 'cancel'],
                                   defaultButton = 'ok',
                                   cancelButton = 'cancel',
                                   dismissString = 'cancel')
        if result == 'ok':
            if cmds.promptDialog(q = True, text = True):
                return cmds.promptDialog(q = True, text = True)
            else:
                return "dummyString"
        elif result == 'Request License Key':
            x = TrialVersionRequestUI()
            x.run()
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

class TrialVersionRequestUI(object):
    def __init__(self):
        if cmds.window('trialWindow', ex = True):
            cmds.deleteUI('trialWindow')
        self.window = cmds.window('trialWindow', title = 'Trial Request', width = 400, height = 300)
        cmds.columnLayout()
        cmds.rowColumnLayout( numberOfColumns=2, columnAttach=(1, 'right', 0), columnWidth=[(1, 100), (2, 250)] )
        cmds.text(label='User Name')
        self.username = cmds.textField()
        cmds.text(label='Email Address' )
        self.emailAddr = cmds.textField()
        cmds.setParent("..")
        cmds.frameLayout(width = 350, labelVisible = False)
        cmds.rowColumnLayout(numberOfColumns = 3, adjustableColumn = 1, columnAttach=([1, 'right', 0]))
        cmds.separator(style = 'none')
        cmds.button(label = 'Submit', c = self.submit)
        cmds.button(label = 'Cancel', c = self.close)
    
    def submit(self, *args):
        """
        """
        name = cmds.textField(self.username, q = True, text = True)
        email = cmds.textField(self.emailAddr, q = True, text = True)
        import Connection as cn
        licenseKey = cn.Connection.getLicense("addLicense", name, email)

        if licenseKey == 1:
            cmds.confirmDialog(title = 'confirm', message = "Username already exists")
        elif licenseKey == 2:
            cmds.confirmDialog(title = 'confirm', message = "Email already exists")
        else:
            License.License.writeLicense(licenseKey)

            x = UI()
            x.loadInMaya()

            self.close()

    def close(self, *args):
        cmds.deleteUI('trialWindow')

    def run(self):
        cmds.showWindow(self.window)

