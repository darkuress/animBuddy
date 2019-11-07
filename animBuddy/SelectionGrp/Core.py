import maya.cmds as cmds
import os
import shutil
import json

class SelectionGrp:
    def __init__(self):
        filePath = os.path.dirname(os.path.abspath(__file__))
        self.selectionGrpDataPath = os.path.join(filePath, 'SelectionGrpData')
        
        if not os.path.exists(self.selectionGrpDataPath):
            os.makedirs(self.selectionGrpDataPath) 

    def findSelections(self):
        """
        """
        path = os.path.join(self.selectionGrpDataPath)
        allSelections = next(os.walk(path))[2]
        
        return allSelections

        
    def getSelection(self):
        """
        return all selected objects
        """
        return cmds.ls(sl = True)
      
    def save(self, selection):
        """
        """
        data = {}
        if self.getSelection():
            data['selection'] = self.getSelection()
            file = os.path.join(self.selectionGrpDataPath, selection)
            
            with open(file, 'w') as outfile:
                json.dump(data, outfile)
            
            return True
        
        else:
            return False
            
    def select(self, selection):
        """
        select objects from selection
        """
        location = os.path.join(self.selectionGrpDataPath, selection)
        with open(location) as jsonFile:
            data = json.load(jsonFile)
            cmds.select(data['selection'])

    def addToSelection(self, selection):
        """
        add current selected objects to selection
        """
        sel = self.getSelection()
        
        location = os.path.join(self.selectionGrpDataPath, selection)
        with open(location) as jsonFile:
            data = json.load(jsonFile)
        allSel = data['selection'] + sel
        
        cmds.select(cl = True)
        cmds.select(allSel)
        
        # save as new
        self.save(selection)
        
        cmds.select(cl = True)
        cmds.select(sel)
            
    def removeFromSelection(self, selection):
        """
        remove object from selection grp
        """
        sels = self.getSelection()

        location = os.path.join(self.selectionGrpDataPath, selection)
        with open(location) as jsonFile:
            data = json.load(jsonFile)
        
        allSel = data['selection']    
        for sel in sels:
            allSel.remove(sel)

        cmds.select(cl = True)
        cmds.select(allSel)
        
        # save as new
        self.save(selection)

        cmds.select(cl = True)
        cmds.select(sel)
        
    def deleteSelection(self, selection):
        """
        """
        location = os.path.join(self.selectionGrpDataPath, selection)
        os.remove(location)
    
    def saveColor(self, selection, color):
        """
        color : [ float, float, float ]
        """
        location = os.path.join(self.selectionGrpDataPath, selection)
        
        with open(location) as jsonFile:
            data = json.load(jsonFile)       
        
        data['color'] = color
        
        with open(location, 'w') as outfile:
            json.dump(data, outfile)
            
    def findColor(self, selection):
        """
        """
        location = os.path.join(self.selectionGrpDataPath, selection)
        
        with open(location) as jsonFile:
            data = json.load(jsonFile)   
        
        if data.has_key('color'):
            return data['color']
        else:
            return False