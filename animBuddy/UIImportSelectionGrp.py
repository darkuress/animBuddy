import maya.cmds as cmds
import os
from SelectionGrp import Core as SGP
reload(SGP)

#- initialize window
if cmds.window('ImportSelectionWin', ex = True):
    cmds.deleteUI('ImportSelectionWin')    
    
class UIImportSelectionGrp:
    """
    """
    def __init__(self):
        """
        initializing ui
        """
        self.SGP = SGP.SelectionGrp()
        
        self.win = cmds.window('ImportSelectionWin', width=100, title = 'Selection Manager')
        cmds.rowLayout(numberOfColumns = 2)
        
        cmds.columnLayout()
        self.textScrollListGrp = cmds.textScrollList()
        cmds.rowLayout(numberOfColumns = 2)
        self.buttonAddChr = cmds.button(label = 'Import', c = self.importGrp)
        self.buttonDelete = cmds.button(label = 'Delete', c = self.deleteGrp)
        cmds.setParent('..')
        cmds.setParent('..')

        self.rebuildExportedGrps()
        try:
            cmds.textScrollList(self.textScrollListGrp, e = True, sii = 1)
        except:
            print("Exported Group doesn't exist")
        
    def rebuildExportedGrps(self, *args):
        """
        """
        cmds.textScrollList(self.textScrollListGrp, e = True, removeAll = True)
        allGrps = self.SGP.getAllExportedGrps()
        for grp in allGrps:
            cmds.textScrollList(self.textScrollListGrp, 
                                e = True, 
                                append=grp) 
                                #selectCommand = self.rebuildSelections)

    def importGrp(self, *args):
        """
        """
        self.SGP.importGrp(self.getCurrentGrp())
        
        import UISelectionToolBar
        reload(UISelectionToolBar)
        x = UISelectionToolBar.UISelectionToolBar()
        x.loadInMaya()

    def getCurrentGrp(self, *args):
        """
        """
        return cmds.textScrollList(self.textScrollListGrp, q = True, si = True)[0]
    
    def deleteGrp(self, *args):
        """
        """
        currentGrp = self.getCurrentGrp()
        self.SGP.deleteGrp(currentGrp)
        self.rebuildExportedGrps()
 
        
    def loadInMaya(self, *args):
        """
        """
        cmds.showWindow(self.win)
