import maya.cmds as cmds
import os
from functools import partial
import Preference
reload(Preference)
import MicroControl.Core as MCL
reload(MCL) 
import EasyInBetween.Core as EIB
reload(EIB)
import ExFootStep.Core as EFS
reload(EFS)
import SnapIt.Core as SNI
reload(SNI)
import SelectionGrp.Core 
reload(SelectionGrp.Core)
import UISelectionToolBar
reload(UISelectionToolBar)
import DrawArcToolBar
reload(DrawArcToolBar)
from DrawArc import testRun as DAC
reload(DAC)
from ResetIt import Core as RIT
reload(RIT)
from FakeConIt import Core as FCI
reload(FCI)
from AnimCopySession import Core as ACS
reload(ACS)
from ViewportRefresh import Core as VPR
reload(VPR)
from Decalcomanie import Core as DCN
reload(DCN)
from ShiftKey import Core as SKY
reload(SKY)
from MagicLocator import Core as MGL
reload(MGL)
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

        self.win = cmds.window('animBuddyWin', width = 1000, title = 'Easy Inbetween')
        filePath = os.path.dirname(os.path.abspath(__file__))
        imagesPath = os.path.join(filePath, 'images')
        self.SGP = SelectionGrp.Core.SelectionGrp()

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

        #----------------------------------------------------------------------------
        cmds.rowLayout(numberOfColumns = 16,
                       adjustableColumn = 1, 
                       columnAttach = ([2, 'right', 0]))
        #- logo ---------------------------------------------------------------------
        cmds.image(image = os.path.join(imagesPath, 'beaverLogo.png'))       
                        
        #cmds.separator(height = 10, width = 700, style = 'none')
        sepStyle = 'in'
        height = 20
        iconSize = self.iconSize
        marginSize = 5
        sepWidth = 30
        
        #for freeze tool check 
        cmds.refresh(su = False)
        self.frozen = False
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     
        #- Shift Key- ---------------------------------------------------------------
        cmds.rowLayout(numberOfColumns = 4)
        self.buttonToLeft = cmds.iconTextButton(style = 'iconOnly', 
                                                image1 = os.path.join(imagesPath, 'left.png'), 
                                                hi = os.path.join(imagesPath, 'left_hi.png'),
                                                width = iconSize/1.2, mw = marginSize, height = iconSize/1.2, mh = marginSize,
                                                label = 'sub',
                                                npm = 1,
                                                annotation = 'shift key to left',
                                                c = partial(self.shiftKey, "left"))
        self.textFieldShiftKey = cmds.textField(text = 1, width = 30)
        cmds.popupMenu()
        self.menuItemShiftKeyClear = cmds.menuItem(label='reset',
                                                   c = self.shiftKeyClear)
        self.buttonToRight = cmds.iconTextButton(style = 'iconOnly', 
                                                image1 = os.path.join(imagesPath, 'right.png'), 
                                                hi = os.path.join(imagesPath, 'right_hi.png'),
                                                width = iconSize/1.2, mw = marginSize, height = iconSize/1.2, mh = marginSize,
                                                label = 'add',
                                                npm = 1,
                                                annotation = 'shift key to right',
                                                c = partial(self.shiftKey, "right"))
        cmds.separator(height = 10, width = 10, style = 'none')
        cmds.setParent("..")

        #- Micro Control- ---------------------------------------------------------------
        cmds.rowLayout(numberOfColumns = 3)
        self.textFieldMidroControl = cmds.textField(text = 0.01, width = 50)
        cmds.columnLayout()
        self.buttonAdd = cmds.iconTextButton(style = 'iconOnly', 
                                             image1 = os.path.join(imagesPath, 'uparrow.png'), 
                                             hi = os.path.join(imagesPath, 'uparrow_hi.png'),
                                             width = iconSize/1.3, mw = marginSize, height = iconSize/2, mh = marginSize,
                                             label = 'add',
                                             npm = 1,
                                             annotation = 'add this value to current channel selection',
                                             c = partial(self.microControlRun, "add"))
        self.buttonSub = cmds.iconTextButton(style = 'iconOnly', 
                                             image1 = os.path.join(imagesPath, 'dnarrow.png'), 
                                             hi = os.path.join(imagesPath, 'dnarrow_hi.png'),
                                             width = iconSize/1.3, mw = marginSize, height = iconSize/2, mh = marginSize,
                                             label = 'sub',
                                             npm = 1,
                                             annotation = 'substract this value from current channel selection',
                                             c = partial(self.microControlRun, "sub"))
        cmds.setParent("..")
        cmds.separator(height = 10, width = 10, style = 'none')
        cmds.setParent("..")
        #- Easy inbetween ---------------------------------------------------------------
        wdth = 267
        cmds.rowLayout(numberOfColumns = 2)
        cmds.columnLayout(width = wdth)
        cmds.frameLayout(labelVisible = False,
                         borderVisible = False, 
                         width = wdth,
                         marginHeight = 0,
                         marginWidth = 0,
                         labelIndent = 0,
                         collapsable = False,)
        cmds.rowLayout(numberOfColumns = 11,
                       adjustableColumn = 1, 
                       columnAttach = ([2, 'both', 0]))
        cmds.text(label = "0.0")
        cmds.separator(height = 5, width = 36, style = 'none')        
        cmds.text(label = "0.5")
        cmds.separator(height = 5, width = 70, style = 'none') 
        cmds.text(label = "1.0")
        cmds.separator(height = 5, width = 34, style = 'none') 
        cmds.setParent("..")
        cmds.setParent("..")
        self.floatSliderEIBAmount = cmds.floatSlider(min = -0.2, 
                                                     max = 1.2, 
                                                     width = wdth,
                                                     value = 0.5, 
                                                     step = 0.1,
                                                     annotation = 'Easy Inbetween. Right click to reset the tool.',
                                                     cc = self.afterDrop,
                                                     dc = self.easyInBetweenChange)
        cmds.popupMenu()
        cmds.radioMenuItemCollection()
        self.radioMenuItemModeObject = cmds.menuItem(label='Object Mode', 
                                                     radioButton = True,
                                                     c = partial(self.writeEIBMode, 'object') )
        self.radioMenuItemModeKeyFrame = cmds.menuItem(label='KeyFrame Mode', 
                                                       radioButton = False,
                                                       c = partial(self.writeEIBMode, 'keyframe') )
        cmds.menuItem(divider=True )
        cmds.menuItem(label = "Reset", command = self.afterDrop)

        cmds.frameLayout(labelVisible = False,
                         borderVisible = False, 
                         width = wdth,
                         marginHeight = 0,
                         marginWidth = 0,
                         labelIndent = 0,
                         collapsable = False,)                
        cmds.rowLayout(width = wdth, numberOfColumns = 30 , columnAttach = ([2, 'both', 0]))
        for i in range(-2, 13, 1):
            value = i/10.0
            if i == 0 or i == 5 or i == 10:
                pic = 'dot_big.png'
            else:
                pic = 'dot.png'
            cmds.iconTextButton(style = 'iconOnly', 
                                image1 = os.path.join(imagesPath, pic), 
                                label = str(value),
                                annotation = "set inbetween : " + str(value),
                                c = partial(self.easyInBetweenChange2, value = value) )
            cmds.separator(height = 10, width = 1, style = 'none')
        cmds.setParent("..")
        cmds.setParent("..")
        cmds.setParent("..")
        cmds.separator(hr= False, height = height, width = 40, style = sepStyle)
        cmds.setParent("..")        
        
        self.readEIBMode()

        #- Snap Tools   -----------------------------------------------------------------                                   
        cmds.rowLayout(numberOfColumns = 5)
        self.buttonConIt = cmds.iconTextButton(style = 'iconOnly', 
                                               image1 = os.path.join(imagesPath, 'conit.png'), 
                                               hi = os.path.join(imagesPath, 'conit_hi.png'),
                                               width = iconSize, mw = marginSize, height = iconSize, mh = marginSize,
                                               label = 'conit',
                                               npm = 1,
                                               annotation = 'Fake Constraint, select source and shift select destination. Right click for Reset Menu',
                                               c = self.fakeConIt)
        cmds.popupMenu()
        cmds.menuItem(label = "Reset", command = self.fakeConItReset)

        self.buttonExFootStep = cmds.iconTextButton(style = 'iconOnly', 
                                                    image1 = os.path.join(imagesPath, 'footstep.png'), 
                                                    hi = os.path.join(imagesPath, 'footstep_hi.png'),
                                                    width = iconSize, mw = marginSize, height = iconSize, mh = marginSize,
                                                    label = 'manager',
                                                    annotation = 'Ex Footstep : snaps to the last keyframe',
                                                    c = self.exFootStep)
        
        #- Magic Locator---------------------------------------------------------------
        cmds.rowLayout(numberOfColumns = 1)
        self.buttonMagicLocator = cmds.iconTextButton(style = 'iconOnly', 
                                                      image1 = os.path.join(imagesPath, 'mgloc.png'), 
                                                      hi = os.path.join(imagesPath, 'mgloc_hi.png'),
                                                      width = iconSize*1.2, mw = marginSize, height = iconSize, mh = marginSize,
                                                      label = 'magic locator',
                                                      annotation = 'select object and it will craete locator per option', 
                                                      c = self.runMagicLocator)
        cmds.popupMenu()
        cmds.radioMenuItemCollection()
        self.radioMenuItemMGLModeCont = cmds.menuItem(label='Constraint to object', 
                                                   radioButton = True,
                                                   c = partial(self.writeMGLMode, 'constraint') )
        self.radioMenuItemMGLModeBake = cmds.menuItem(label='Bake', 
                                                   radioButton = False,
                                                   c = partial(self.writeMGLMode, 'bake') )
        self.radioMenuItemMGLModeDrive = cmds.menuItem(label='Drive Object', 
                                                   radioButton = False,
                                                   c = partial(self.writeMGLMode, 'driver') )
        cmds.setParent("..") 
        self.readMGLMode()

        #- Snap It
        self.buttonExFootStep = cmds.iconTextButton(style = 'iconOnly', 
                                                    image1 = os.path.join(imagesPath, 'snapit.png'), 
                                                    hi = os.path.join(imagesPath, 'snapit_hi.png'), 
                                                    width = iconSize, mw = marginSize, height = iconSize, mh = marginSize,
                                                    label = 'manager',
                                                    c = self.snapIt)
        cmds.separator(hr= False, height = height, width = sepWidth, style = sepStyle)
        cmds.setParent("..")

        #- Decalcomanie---------------------------------------------------------------
        cmds.rowLayout(numberOfColumns = 1)
        self.buttonDecalcomanie = cmds.iconTextButton(style = 'iconOnly', 
                                                      image1 = os.path.join(imagesPath, 'decalcomanie.png'), 
                                                      hi = os.path.join(imagesPath, 'decalcomanie_hi.png'),
                                                      width = iconSize*1.2, mw = marginSize, height = iconSize, mh = marginSize,
                                                      label = 'decalcomanie',
                                                      annotation = 'Copy Left or Right anim to Right or Left', 
                                                      c = self.runDecalComanie)
        cmds.popupMenu()
        cmds.radioMenuItemCollection()
        self.radioMenuItemDCNModePose = cmds.menuItem(label='Copy Pose of Current Frame', 
                                                   radioButton = True,
                                                   c = partial(self.writeDCNMode, 'pose') )
        self.radioMenuItemDCNModeAnim = cmds.menuItem(label='Copy Animation', 
                                                   radioButton = False,
                                                   c = partial(self.writeDCNMode, 'anim') )
        cmds.setParent("..") 
        self.readDCNMode()

        #- Reset It---------------------------------------------------------------
        cmds.rowLayout(numberOfColumns = 1)
        self.buttonReset = cmds.iconTextButton(style = 'iconOnly', 
                                               image1 = os.path.join(imagesPath, 'reset.png'), 
                                               hi = os.path.join(imagesPath, 'reset_hi.png'),
                                               width = iconSize, mw = marginSize, height = iconSize, mh = marginSize,
                                               label = 'reset',
                                               annotation = 'Resets values of current selected controller or any object', 
                                               c = self.resetIt)
        cmds.setParent("..") 

        
        #- Draw Arc---------------------------------------------------------------
        cmds.rowLayout(numberOfColumns = 2)
        self.buttonDrawArc = cmds.iconTextButton(style = 'iconOnly', 
                                                 image1 = os.path.join(imagesPath, 'arc_hi.png'), 
                                                 hi = os.path.join(imagesPath, 'arc.png'),
                                                 width = iconSize, mw = marginSize, height = iconSize, mh = marginSize,
                                                 label = 'arc',
                                                 annotation = 'MotionTrail tool',
                                                 c = self.drawArc)  
        cmds.popupMenu()
        cmds.menuItem(label = "Setting", c = self.drawArcToolbar)
        cmds.menuItem(label = "---------------", c = self.drawArcToolbar)
        cmds.menuItem(label = "Delete All", c = self.deleteAll)       
        cmds.separator(hr= False, height = height, width = sepWidth, style = sepStyle)
        cmds.setParent("..") 
        
        #- Selection Group---------------------------------------------------------------
        cmds.rowLayout(numberOfColumns = 1)
        self.buttonSelectionManager = cmds.iconTextButton(style = 'iconOnly', 
                                                          image1 = os.path.join(imagesPath, 'manager.png'),
                                                          hi = os.path.join(imagesPath, 'manager_hi.png'),                                                          
                                                          width = iconSize, mw = marginSize, height = iconSize, mh = marginSize,
                                                          label = 'manager',
                                                          c = self.expandSelectionToolbar)
        cmds.setParent("..")
        #- Copy Paste Animation--------------------------------------------------
        cmds.rowLayout(numberOfColumns = 2)
        self.buttonCopyPaste = cmds.iconTextButton(style = 'iconOnly', 
                                                   image1 = os.path.join(imagesPath, 'copy.png'), 
                                                   hi = os.path.join(imagesPath, 'copy_hi.png'),
                                                   width = iconSize, mw = marginSize, height = iconSize, mh = marginSize,
                                                   label = 'cv',
                                                   npm = 1,
                                                   annotation = 'copy current animation or pose. Right click for reset tool. Preserves current session',
                                                   c = self.copySession)
        cmds.popupMenu()
        cmds.radioMenuItemCollection()
        self.radioMenuItemACSModePose = cmds.menuItem(label='Copy Pose of Current Frame', 
                                                   radioButton = True,
                                                   c = partial(self.writeACSMode, 'pose') )
        self.radioMenuItemACSModeAnim = cmds.menuItem(label='Copy Animation', 
                                                   radioButton = False,
                                                   c = partial(self.writeACSMode, 'anim') )
        cmds.menuItem(divider=True )
        cmds.menuItem(label = "Reset", command = self.copyReset)
        cmds.separator(hr= False, height = height, width = sepWidth, style = sepStyle)
        cmds.setParent("..")         
        
        self.readACSMode()

        #- Freeze Viewport---------------------------------------------------------------
        cmds.rowLayout(numberOfColumns = 1)
        self.buttonReset = cmds.iconTextButton(style = 'iconOnly', 
                                               image1 = os.path.join(imagesPath, 'freeze.png'), 
                                               hi = os.path.join(imagesPath, 'freeze_hi.png'),
                                               width = iconSize, mw = marginSize, height = iconSize, mh = marginSize,
                                               label = 'freeze',
                                               annotation = 'Freeze / unFreeze viewport', 
                                               c = self.freeze)  
        cmds.setParent("..") 
        
        #- BH Playblast------------------------------------------------------------
        cmds.rowLayout(numberOfColumns = 1)
        self.buttonPlayblast = cmds.iconTextButton(style = 'iconOnly', 
                                                   image1 = os.path.join(imagesPath, 'play1_hi.png'), 
                                                   hi = os.path.join(imagesPath, 'play1.png'),
                                                   width = iconSize, mw = marginSize, height = iconSize, mh = marginSize,
                                                   label = 'playblast',
                                                   annotation = 'Beverhouse exclusive Playblast Tool', 
                                                   c = self.playblast)        
        cmds.setParent("..")        

        cmds.rowLayout(numberOfColumns = 3)
        cmds.separator(hr= False, height = height, width = sepWidth, style = sepStyle)
        self.buttonPref = cmds.iconTextButton(style = 'iconOnly', 
                                              image1 = os.path.join(imagesPath, 'preference.png'), 
                                              hi = os.path.join(imagesPath, 'preference_hi.png'),
                                              width = iconSize/1.7, mw = marginSize, height = iconSize, mh = marginSize,
                                              label = 'preference',
                                              annotation = 'Preference')
        cmds.popupMenu()
        cmds.menuItem(label = "About", c = self.about)
        cmds.menuItem(label = "Check for update", c = self.versionCheck)
        cmds.menuItem(label = "--------------")
        cmds.menuItem(label = "Preference", c = self.prefUI)
        cmds.menuItem(label = "--------------")
        cmds.menuItem(label = "Close", command = self.closeUI)
        
        cmds.separator(hr= False, height = height, width = 10, style = "none")
        cmds.setParent("..") 

    #---------------------------------------------------------------------------------
    def shiftKey(self, mode = 'right'):
        """
        """
        val = int(cmds.textField(self.textFieldShiftKey, q = True, text = True))
        if mode == 'right':
            SKY.run(amount = val)
        elif mode == 'left':
            SKY.run(amount = -1 * val)

    def shiftKeyClear(self, *args):
        """
        """
        SKY.clear()

    #---------------------------------------------------------------------------------
    def microControlRun(self, mode, *args):
        """
        @param mode string "add" or "sub"
        """
        val = round ( float(cmds.textField(self.textFieldMidroControl, q = True, text = True)), 3)
        if mode == "add":
            MCL.run(val)
        else:
            MCL.run(val*-1)

    #---------------------------------------------------------------------------------   
    def easyInBetweenChange(self, *args):
        """
        slider
        """
        if not self.undoChunk:
            self.undoChunk = True
            cmds.undoInfo(openChunk = True)
        amount = cmds.floatSlider(self.floatSliderEIBAmount, q = True, v = True)      
        if cmds.menuItem(self.radioMenuItemModeObject, q = True, radioButton = True):
            EIB.changeKey(amount)
        elif cmds.menuItem(self.radioMenuItemModeKeyFrame, q = True, radioButton = True):
            if amount > 1:
                EIB.changeSelectedKey(1)
            elif amount < 0:
                EIB.changeSelectedKey(0)
            else:
                EIB.changeSelectedKey(amount)    
        
    def afterDrop(self, *args):
        """
        """
        self.undoChunk = False
        cmds.undoInfo(closeChunk = True)
        cmds.floatSlider(self.floatSliderEIBAmount, e = True, v = 0.5) 

    def easyInBetweenChange2(self, value = None, *args):
        """
        dots
        """
        cmds.floatSlider(self.floatSliderEIBAmount, e = True, v = value)
        if cmds.menuItem(self.radioMenuItemModeObject, q = True, radioButton = True):
            EIB.changeKey(value)
        elif cmds.menuItem(self.radioMenuItemModeKeyFrame, q = True, radioButton = True):
            if value > 1:
                EIB.changeSelectedKey(1)
            elif value < 0:
                EIB.changeSelectedKey(0)
            else:
                EIB.changeSelectedKey(value)   

    def readEIBMode(self):
        """
        """
        self.pref = Preference.Preference()
        if self.pref.eibMode == 'object':
            cmds.menuItem(self.radioMenuItemModeObject, e = True, radioButton = True)
            cmds.menuItem(self.radioMenuItemModeKeyFrame, e = True, radioButton = False)
        elif self.pref.eibMode == 'keyframe':
            cmds.menuItem(self.radioMenuItemModeObject, e = True, radioButton = False)
            cmds.menuItem(self.radioMenuItemModeKeyFrame, e = True, radioButton = True)
    
    def writeEIBMode(self, mode, *args):
        """
        """
        self.pref = Preference.Preference()
        self.pref.eibMode = mode
        self.pref.construct()
        self.pref.write()

    #---------------------------------------------------------------------------------
    def fakeConIt(self, *args):
        """
        """
        conRun = FCI.FakeConIt()
        result = conRun.run()
        if result == 'Success':
            cmds.confirmDialog(title ='Fake Conit', 
                            message ='Fake Constraint was generatec\nRight Click on button to reset connection', 
                            button = ['Ok'], 
                            defaultButton='Ok', 
                            dismissString='Ok' )
        elif result == 'Failed':
            cmds.confirmDialog(title ='Fake Conit', 
                            message ='please select source and destination(s) to create Fake Constraint', 
                            button = ['Ok'], 
                            defaultButton='Ok', 
                            dismissString='Ok' )
    def fakeConItReset(self, *args):
        """
        """
        conRun = FCI.FakeConIt()
        conRun.reset()        
        
    def exFootStep(self, *args):
        """
        """
        EFS.exFootStep()
    
    def snapIt(self, *args):
        """
        """
        SNI.snap()
    
    #---------------------------------------------------------------------------------
    def expandSelectionToolbar(self, *args):
        """
        """
        if cmds.window('UISelectionToolBar', ex = True):
            cmds.deleteUI('UISelectionToolBar')  
        else:
            ui = UISelectionToolBar.UISelectionToolBar()
            ui.loadInMaya()
    
    #---------------------------------------------------------------------------------  
    def drawArc(self, *args):
        """
        Motion trail 
        """
        self.pref = Preference.Preference()
        
        DAC.run(dotSize       = self.pref.dotSize, 
                keyFrameSize  = self.pref.keyFrameSize, 
                timeBuffer    = self.pref.timeBuffer,
                lineWidth     = self.pref.lineWidth,
                lineColor     = self.pref.lineColor,
                dotColor      = self.pref.dotColor,
                keyFrameColor = self.pref.keyFrameColor)

    def deleteAll(self, *args):
        """
        delete all motion trails
        """
        DAC.deleteAll()

    #---------------------------------------------------------------------------------
    def drawArcToolbar(self, *args):
        """
        """
        ui = DrawArcToolBar.DrawArcToolBar()
        ui.loadInMaya()

    #---------------------------------------------------------------------------------      
    def copySession(self, *args):
        """
        """
        mode = 'pose'
        if cmds.menuItem(self.radioMenuItemACSModeAnim, q = True, radioButton = True):
            mode = 'anim'
        copy = ACS.AnimCopySession()
        result = copy.run(mode = mode)

        cmds.confirmDialog(title ='Anim Copy Session', 
                           message ='Anim {} done!'.format(result), 
                           button = ['Ok'], 
                           defaultButton='Ok', 
                           dismissString='Ok' )

    def copyReset(self, *args):
        """
        """
        copy = ACS.AnimCopySession()
        copy.reset() 

    def readACSMode(self):
        """
        """
        self.pref = Preference.Preference()
        if self.pref.acsMode == 'pose':
            cmds.menuItem(self.radioMenuItemACSModePose, e = True, radioButton = True)
            cmds.menuItem(self.radioMenuItemACSModeAnim, e = True, radioButton = False)
        elif self.pref.acsMode == 'anim':
            cmds.menuItem(self.radioMenuItemACSModePose, e = True, radioButton = False)
            cmds.menuItem(self.radioMenuItemACSModeAnim, e = True, radioButton = True)
    
    def writeACSMode(self, mode, *args):
        """
        """
        self.pref = Preference.Preference()
        self.pref.acsMode = mode
        self.pref.construct()
        self.pref.write()

    #---------------------------------------------------------------------------------
    def runMagicLocator(self):
        """
        """
        mode = 'constraint'
        if cmds.menuItem(self.radioMenuItemMGLModeBake, q = True, radioButton = True):
            mode = 'bake'
        elif cmds.menuItem(self.radioMenuItemMGLModeDrive, q = True, radioButton = True):
            mode = 'driver'
        MGL.run(mode = mode)

    def readMGLMode(self):
        """
        """
        self.pref = Preference.Preference()
        if self.pref.mglMode == 'constraint':
            cmds.menuItem(self.radioMenuItemMGLModeCont, e = True, radioButton = True)
            cmds.menuItem(self.radioMenuItemMGLModeBake, e = True, radioButton = False)
            cmds.menuItem(self.radioMenuItemMGLModeDrive, e = True, radioButton = False)
        elif self.pref.mglMode == 'bake':
            cmds.menuItem(self.radioMenuItemMGLModeCont, e = True, radioButton = False)
            cmds.menuItem(self.radioMenuItemMGLModeBake, e = True, radioButton = True)
            cmds.menuItem(self.radioMenuItemMGLModeDrive, e = True, radioButton = False)
        elif self.pref.mglMode == 'driver':
            cmds.menuItem(self.radioMenuItemMGLModeCont, e = True, radioButton = False)
            cmds.menuItem(self.radioMenuItemMGLModeBake, e = True, radioButton = False)
            cmds.menuItem(self.radioMenuItemMGLModeDrive, e = True, radioButton = True)  

    def writeMGLMode(self, mode, *args):
        """
        """
        self.pref = Preference.Preference()
        self.pref.mglMode = mode
        self.pref.construct()
        self.pref.write()

    #---------------------------------------------------------------------------------
    def runDecalComanie(self):
        """
        """
        mode = 'pose'
        if cmds.menuItem(self.radioMenuItemDCNModeAnim, q = True, radioButton = True):
            mode = 'anim'
        DCN.run(mode =mode)

    def readDCNMode(self):
        """
        """
        self.pref = Preference.Preference()
        if self.pref.acsMode == 'pose':
            cmds.menuItem(self.radioMenuItemDCNModePose, e = True, radioButton = True)
            cmds.menuItem(self.radioMenuItemDCNModeAnim, e = True, radioButton = False)
        elif self.pref.acsMode == 'anim':
            cmds.menuItem(self.radioMenuItemDCNModePose, e = True, radioButton = False)
            cmds.menuItem(self.radioMenuItemDCNModeAnim, e = True, radioButton = True)
    
    def writeDCNMode(self, mode, *args):
        """
        """
        self.pref = Preference.Preference()
        self.pref.dcnMode = mode
        self.pref.construct()
        self.pref.write()

    #---------------------------------------------------------------------------------  
    def resetIt(self, *args):
        """
        Motion trail 
        """
        RIT.run()        
    
    #---------------------------------------------------------------------------------
    def freeze(self, *args):
        """
        """
        if self.frozen == True:
            cmds.refresh(su = False)
            self.frozen = False
        else:
            cmds.refresh(su = True)
            self.frozen = True
    
    #---------------------------------------------------------------------------------
    def playblast(self, *args):
        """
        """
        from bhPlayblast import ui
        reload(ui)

        run = ui.UI()
        run.loadInMaya()
    
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
        
    def loadInMaya(self, *args):
        """
        """
        #-check license
        licenseKey = License.License.readLicense()
        newLicense = False
        if not licenseKey:
            result = cmds.promptDialog(title = 'License Registration',
                                       message = 'Enter License Key',
                                       button = ['ok', 'cancel'],
                                       defaultButton = 'ok',
                                       cancelButton = 'cancel',
                                       dismissString = 'cancel')
            if result == 'ok':
                licenseKey = cmds.promptDialog(q = True, text = True)
                newLicense = True
            else:
                return
            
        licenseObj = License.License(licenseKey)
        validator = licenseObj.validate() 
        if validator == 'Invalid':
            print "Invalid License"
            return
        elif validator == 'Expired':
            print "License Expired"
            return
        elif validator == 'Valid':
            if newLicense:
                License.License.writeLicense(licenseKey)
            # Running
            exec(cn.connect('runUI', licenseKey))

