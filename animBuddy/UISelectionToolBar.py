import maya.cmds as cmds
import os
from functools import partial
from SelectionGrp import Core as SGP
reload(SGP)

#- initialize window
if cmds.window('UISelectionToolBar', ex = True):
    cmds.deleteUI('UISelectionToolBar')    
try:
    cmds.deleteUI('sgToolbar')   
except:
    pass 
    
class UISelectionToolBar:
    """
    """
    def __init__(self):
        """
        initializing ui
        """
        filePath = os.path.dirname(os.path.abspath(__file__))
        imagesPath = os.path.join(filePath, 'images')
        iconSize = 22
        marginSize = 5
        self.SGP = SGP.SelectionGrp()
               
        self.win = cmds.window('UISelectionToolBar', width=500, title = 'Selection Manager')
        self.frameLayoutMain = cmds.frameLayout(labelVisible = False, 
                                                w = 10, 
                                                borderVisible = False, 
                                                parent = self.win)
        self.rowLayoutMain = cmds.rowLayout(numberOfColumns = 3, 
                                            adjustableColumn = 1, 
                                            columnAttach = ([2, 'right', 0]), 
                                            parent = self.frameLayoutMain)
                
        # dummy layout
        cmds.separator(height = 10, width = 10, style = 'none')
        self.rowLayoutButtons = cmds.rowLayout(numberOfColumns = 100, 
                                               adjustableColumn = 1, 
                                               columnAttach = ([2, 'right', 0]), 
                                               parent = self.rowLayoutMain)
        cmds.button('asdfsdf')
        cmds.setParent("..")
        
        cmds.rowLayout(numberOfColumns = 4)
        cmds.separator(height = 10, width = 10, style = 'none')
        self.buttonAdd = cmds.iconTextButton(style = 'iconOnly', 
                                             image1 = os.path.join(imagesPath, 'add.png'), 
                                             hi = os.path.join(imagesPath, 'add_hi.png'),
                                             width = iconSize, mw = marginSize, height = iconSize, mh = marginSize,
                                             label = 'add',
                                             annotation = 'Closing Selection ToolBar', 
                                             c = self.add) 
        self.buttonClose = cmds.iconTextButton(style = 'iconOnly', 
                                               image1 = os.path.join(imagesPath, 'close.png'), 
                                               hi = os.path.join(imagesPath, 'close_hi.png'),
                                               width = iconSize, mw = marginSize, height = iconSize, mh = marginSize,
                                               label = 'close',
                                               annotation = 'Closing Selection ToolBar', 
                                               c = self.close) 
        
    def buildButton(self):
        """
        """
        allSelections = self.SGP.findSelections()
        numSelections = len(allSelections)
        
        # delete existing buttons
        existingBtns = cmds.rowLayout(self.rowLayoutButtons, q = True, childArray = True)
        if existingBtns:
            for btns in existingBtns:
                cmds.deleteUI(btns)
        # delete and recreate? 
        cmds.rowLayout(self.rowLayoutButtons, e = True, numberOfColumns = numSelections + 1)
        for selection in allSelections:
            if self.SGP.findColor(selection):
                color = self.SGP.findColor(selection)
            else:
                color = [0.5, 0.5, 0.5]
            buttonSelection = cmds.button(label = selection, 
                                          parent = self.rowLayoutButtons,
                                          backgroundColor = color,
                                          npm = 1,
                                          c = partial(self.select, selection))
            cmds.popupMenu()
            cmds.menuItem(label = "Change Color", command = partial(self.color, selection, buttonSelection))
            cmds.menuItem(label = "Add to Selection", command = partial(self.addToSelection, selection))
            cmds.menuItem(label = "Remove From Selection", command = partial(self.removeFromSelection, selection))
            cmds.menuItem(label = "---------------------")
            cmds.menuItem(label = "Delete", command = partial(self.delete, selection))
    
    def select(self, selection, *args):
        """
        select from button
        """
        self.SGP.select(selection)
        
    def add(self, *args):
        """
        add to selection
        """
        if self.SGP.getSelection():
            result = cmds.promptDialog(
                            title='Choose Name',
                            message='Enter Name:',
                            button=['OK', 'Cancel'],
                            defaultButton='OK',
                            cancelButton='Cancel',
                            dismissString='Cancel')       
            if result == 'OK':
                text = cmds.promptDialog(query=True, text=True)
                
            saved = self.SGP.save(text)
            
            self.buildButton()
        
        else:
            print "please select something"
    
    def addToSelection(self, selection, *args):
        """
        """
        self.SGP.addToSelection(selection)
    
    def removeFromSelection(self, selection, *args):
        """
        """
        self.SGP.removeFromSelection(selection)
    
    def delete(self, selection, *args):
        """
        delete button
        """
        self.SGP.deleteSelection(selection)
        self.buildButton()
    
    def color(self, selection, button, *args):
        """
        change color of button
        """
        result = cmds.colorEditor()
        color = result.split(" ")
        color = [float(x) for x in color if x]
        color = color[:-1]
        
        cmds.button(button, e = True, backgroundColor = color)
        
        self.SGP.saveColor(selection, color)
        
    def close(self, *args):
        """
        """
        try:
            cmds.deleteUI('sgToolbar')   
        except:
            pass     
            
    def loadInMaya(self, *args):
        """
        """
        #cmds.showWindow(self.win)
        allowedAreas = ['top', 'bottom']
        sgToolBar = cmds.toolBar('sgToolbar', area='bottom', content=self.win, allowedArea=allowedAreas )
        self.buildButton()
'''        
myWindow = cmds.window()
buttonForm = cmds.formLayout( parent = myWindow )
cmds.button( parent = buttonForm )
allowedAreas = ['right', 'left']
x = cmds.toolBar( area='bottom', content=myWindow, allowedArea=allowedAreas )
#cmds.deleteUI(x)
'''

