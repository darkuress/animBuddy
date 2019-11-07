import maya.cmds as cmds
import Core
reload(Core)

#- initialize window
if cmds.window('easyInbetweenUI', ex = True):
    cmds.deleteUI('easyInbetweenUI')    

class UI:
    def __init__(self):
        """
        initializing ui
        """
        self.win = cmds.window('easyInbetweenUI', width=500, title = 'Easy Inbetween')
        cmds.columnLayout()
        
        self.floatSliderAmount = cmds.floatSlider(min = 0, 
                                                  max = 1, 
                                                  value = 0.5, 
                                                  step = 0.1,
                                                  dc = self.change)        
        
    
    def change(self, *args):
        amount = cmds.floatSlider(self.floatSliderAmount, q = True, v = True)
        Core.changeKey(amount)
        
    def loadInMaya(self, *args):
        """
        """
        cmds.showWindow(self.win)
'''        
myWindow = cmds.window()
buttonForm = cmds.formLayout( parent = myWindow )
cmds.button( parent = buttonForm )
allowedAreas = ['right', 'left']
x = cmds.toolBar( area='bottom', content=myWindow, allowedArea=allowedAreas )
#cmds.deleteUI(x)
'''

