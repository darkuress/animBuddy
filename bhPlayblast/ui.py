import maya.cmds as cmds
import os
import json
import playblast
reload(playblast)

"""
uasage
from rigDoodle import ui
reload(ui)
x = ui.UI()
x.loadInMaya()
"""

#- initialize window
if cmds.window('playblastUI', ex = True):
    cmds.deleteUI('playblastUI')    

class UI:
    def __init__(self):
        """
        initializing ui
        """
        configJson = "config.json"
        basedir = os.path.dirname(os.path.realpath(__file__))
        self.configFile = os.path.join(basedir, configJson)
        
        cmds.window('playblastUI', menuBar=True, width=500, title = 'Beaver House Playblast')
        cmds.columnLayout()

        cmds.rowLayout(numberOfColumns = 2)
        cmds.text(label='Your Student Number : ' )
        self.textFieldStudentNumber = cmds.textField()
        cmds.setParent("..")

        cmds.rowLayout(numberOfColumns = 2)
        cmds.text(label='Assignment Number   : ' )
        self.textFieldProject = cmds.textField()
        cmds.setParent("..")

        
        cmds.rowLayout(numberOfColumns = 2)
        cmds.text(label='Your Initial                   : ' )
        self.textFieldName = cmds.textField()
        cmds.setParent("..")
        
        cmds.rowLayout(numberOfColumns = 3)
        cmds.text(label='Playblast Folder          : ' )
        self.textFieldProjectDir = cmds.textField(width = 300)
        buttonFindDir = cmds.button(label = "Browse", command = self.setProjectDir)
        cmds.setParent("..")        
        
        cmds.separator( height=40, style='in' )
        
        cmds.button(label = 'Playblast', width = 500, command = self.playblastCB)
      
        self.checkStudentNumber()
        self.checkName()
        self.checkProject()
        self.checkDir()
        
    def setProjectDir(self, *args):
        """
        directory for playblast
        """
        dir = cmds.fileDialog2(fileMode = 3)
        cmds.textField(self.textFieldProjectDir, e = True, text = dir[0])

    def checkStudentNumber(self, *args):
        """
        checking name field whether we already have json or not
        """
        if os.path.exists(self.configFile):
            with open(self.configFile) as jsonFile:
                data = json.load(jsonFile)
                if data.has_key("studentNumber"):
                    cmds.textField(self.textFieldStudentNumber, e = True, text = data["studentNumber"])
        
    def checkName(self, *args):
        """
        checking name field whether we already have json or not
        """
        if os.path.exists(self.configFile):
            with open(self.configFile) as jsonFile:
                data = json.load(jsonFile)
                if data.has_key("name"):
                    cmds.textField(self.textFieldName, e = True, text = data["name"])

    def checkDir(self, *args):
        """
        checking dir field whether we already have json or not
        """
        if os.path.exists(self.configFile):
            with open(self.configFile) as jsonFile:
                data = json.load(jsonFile)
                if data.has_key("dir"):
                    cmds.textField(self.textFieldProjectDir, e = True, text = data["dir"])                        

    def checkProject(self, *args):
        """
        checking project field whether we already have json or not
        """
        if os.path.exists(self.configFile):
            with open(self.configFile) as jsonFile:
                data = json.load(jsonFile)
                if data.has_key("project"):
                    cmds.textField(self.textFieldProject, e = True, text = data["project"])     
                    
    def playblastCB(self, *args):
        """
        playblasting 
        """
        data = {}
        data['studentNumber']    = cmds.textField(self.textFieldStudentNumber, q = True, text = True)  
        data['name']             = cmds.textField(self.textFieldName, q = True, text = True)  
        data['project']          = cmds.textField(self.textFieldProject, q = True, text = True)  
        data['dir']              = cmds.textField(self.textFieldProjectDir, q = True, text = True)  
        with open(self.configFile, 'w') as outfile:
            json.dump(data, outfile)
        
        playblastTmpName = data['studentNumber'] + '_' + data['project'] + '_' + data['name'] + '_v'
        version =  self.checkVersion(data['dir'], playblastTmpName)
        
        playblastName = playblastTmpName + str(version).zfill(2) + '.avi'  
        palyblastFile = os.path.join(data['dir'], playblastName)
        playblast.playblast(filename = palyblastFile, stName = playblastName.split('.')[0])
    
    def checkVersion(self, path, playblastTmpName):
        """
        checking for the next version file
        """
        allTheFiles = [f for f in os.listdir(path)]
        
        allFiles = []
        for file in allTheFiles:
            if len(file.split(playblastTmpName)) > 1:
                allFiles.append(file)
        if not allFiles:
            return 1
        else:
            import re
            allVersions = [int(re.findall(r'\d+', x.split('.')[0])[-1]) for x in allFiles] 
            return max(allVersions) + 1
    
    def loadInMaya(self, *args):
        """
        """
        cmds.showWindow()
