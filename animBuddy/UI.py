import maya.cmds as cmds
import os
from functools import partial
import Preference
reload(Preference)
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

        cmds.frameLayout("main",
                         labelVisible = False,
                         borderVisible = False, 
                         width = 10,
                         marginHeight = 0,
                         marginWidth = 0,
                         labelIndent = 0,
                         collapsable = False,)
        cmds.rowLayout(numberOfColumns = 11,
                       adjustableColumn = 1, 
                       columnAttach = ([2, 'right', 0]))
        
        filePath = os.path.dirname(os.path.abspath(__file__))
        imagesPath = os.path.join(filePath, 'images')
        
        self.SGP = SelectionGrp.Core.SelectionGrp()
        
        cmds.separator(height = 10, width = 700, style = 'none')
        sepStyle = 'in'
        height = 20
        iconSize = self.iconSize
        marginSize = 5
        sepWidth = 30
        
        #for freeze tool check 
        cmds.refresh(su = False)
        self.frozen = False
        
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
        
        #- Snap Tools   -----------------------------------------------------------------                                   
        cmds.rowLayout(numberOfColumns = 4)
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
        
        
        
        #- Snap It
        self.buttonExFootStep = cmds.iconTextButton(style = 'iconOnly', 
                                                    image1 = os.path.join(imagesPath, 'snapit.png'), 
                                                    hi = os.path.join(imagesPath, 'snapit_hi.png'), 
                                                    width = iconSize, mw = marginSize, height = iconSize, mh = marginSize,
                                                    label = 'manager',
                                                    c = self.snapIt)
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
        cmds.menuItem(label = "Reset", command = self.copyReset)
        cmds.separator(hr= False, height = height, width = sepWidth, style = sepStyle)
        cmds.setParent("..")         
        
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
        cmds.menuItem(label = "Preference", c = self.prefUI)
        cmds.menuItem(label = "--------------")
        cmds.menuItem(label = "Close", command = self.closeUI)
        
        cmds.separator(hr= False, height = height, width = 10, style = "none")
        cmds.setParent("..") 

    #---------------------------------------------------------------------------------   
    def easyInBetweenChange(self, *args):
        """
        """
        amount = cmds.floatSlider(self.floatSliderEIBAmount, q = True, v = True)          
        EIB.changeKey(amount)
     
    def afterDrop(self, *args):
        """
        """
        cmds.floatSlider(self.floatSliderEIBAmount, e = True, v = 0.5) 

    def easyInBetweenChange2(self, value = None, *args):
        """
        """
        cmds.floatSlider(self.floatSliderEIBAmount, e = True, v = value)
        EIB.changeKey(value)
        
    #---------------------------------------------------------------------------------
    def fakeConIt(self, *args):
        """
        """
        conRun = FCI.FakeConIt()
        conRun.run()

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
        copy = ACS.AnimCopySession()
        copy.run()

    def copyReset(self, *args):
        """
        """
        copy = ACS.AnimCopySession()
        copy.reset() 
    
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
        #cmds.showWindow(self.win)
        allowedAreas = ['top', 'bottom']
        abToolBar = cmds.toolBar('abToolBar', area='bottom', content=self.win, allowedArea=allowedAreas )
'''        
myWindow = cmds.window()
buttonForm = cmds.formLayout( parent = myWindow )
cmds.button( parent = buttonForm )
allowedAreas = ['right', 'left']
x = cmds.toolBar( area='bottom', content=myWindow, allowedArea=allowedAreas )
#cmds.deleteUI(x)
'''

