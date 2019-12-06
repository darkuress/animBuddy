import maya.cmds as cmds
import os
import shutil
import json
from animBuddy.Utils import System
reload(System)

class SelectionGrp:
    def __init__(self):
        filePath = System.dataPath()
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
        if sels:    
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

    def getAllCurrentSelections(self):
        """
        """
        result = []
        for file in os.listdir(self.selectionGrpDataPath):
            if os.path.isfile(os.path.join(self.selectionGrpDataPath, file)):
                result.append(os.path.join(self.selectionGrpDataPath, file))
        return result

    def export(self, name):
        """
        """
        path = os.path.join(self.selectionGrpDataPath, name)
        if os.path.isdir(path):
            print "that group already exists"
            confirm = cmds.confirmDialog(title='Already exists', 
                                         message='This group already exists, Do you want to override?', 
                                         button=['Yes','No'], defaultButton='Yes', cancelButton='No', dismissString='No' )
            if confirm == 'no':
                return
        else:
            os.makedirs(path) 

        for file in self.getAllCurrentSelections(): 
            shutil.copyfile(file, os.path.join(path, os.path.basename(file))) 

    def importGrp(self, group):
        """
        importing selection grp
        """
        self.emptySelectionFolder()
        grpPath = os.path.join(self.selectionGrpDataPath, group)
        selectedGrps = os.listdir(grpPath)
        for grp in selectedGrps: 
            file = os.path.join(grpPath, grp)
            if os.path.isfile(file):
                shutil.copyfile(file, os.path.join(self.selectionGrpDataPath, os.path.basename(file))) 

    def deleteGrp(self, group):
        """
        deleting selection grp
        """
        grpPath = os.path.join(self.selectionGrpDataPath, group)
        if os.path.exists(grpPath):
            shutil.rmtree(grpPath)

    def getAllExportedGrps(self):
        """
        """
        result = []
        for folder in os.listdir(self.selectionGrpDataPath):
            if os.path.isdir(os.path.join(self.selectionGrpDataPath, folder)):
                result.append(folder)
        return result        

    def emptySelectionFolder(self):
        """
        """
        files = self.getAllCurrentSelections()
        for file in files:
            try:
                if os.path.isfile(file):
                    os.remove(file)
            except Exception as e:
                print e

