import maya.cmds as cmds
import os
import json
from animBuddy.Utils import System
reload(System)

class FakeConIt:
    def __init__(self):
        """
        """
        filePath = System.dataPath()
        self.conItDataPath = os.path.join(filePath, 'fakeConIt.json')

    def getTargets(self):
        """
        first select source, 
        second select target
        """
        if len(cmds.ls(sl = True)) > 0:
            return cmds.ls(sl = True)
        
        else:
            return False
            
    def run(self):
        """
        """       
        if os.path.exists(self.conItDataPath):
            with open(self.conItDataPath) as jsonFile:
                data = json.load(jsonFile)
                source = data['source']
                targets = data['targets']
                print(source)
                print(targets)
                #create fake locator to constraint
                loc = cmds.spaceLocator(n = "fakeCon_loc")
                cmds.xform(loc, t = data['transform'], ro = data['rotation'])
                for target in data['targets']:
                    cmds.xform(target, t = data[target]['targetTransform'], ro = data[target]['targetRotation'])
                    try:
                        cmds.parentConstraint(loc, target, mo = True, weight = 1)
                    except:
                        print("destination's translation or rotation might be locked")
                        return
                    
                #get current transform
                tr = cmds.xform(source, q = True, ws = True, t = True)
                ro = cmds.xform(source, q = True, ws = True, ro = True) 

                #rotate locator
                cmds.xform(loc, t = tr, ro = ro)
                tempXform = {}
                for target in data['targets']:
                    tempXform[target] = {'tr' : cmds.xform(target, q = True, t = True, ws = True),
                                         'ro' : cmds.xform(target, q = True, ro = True, ws = True)}
                    pcon = cmds.listRelatives(target, type = "parentConstraint")
                    cmds.delete(pcon)                
                                
                cmds.delete(loc)

                for target in data['targets']:
                    cmds.xform(target, t = tempXform[target]['tr'], ro = tempXform[target]['ro'], ws = True)

                self.write(source, targets)

        else:
            if not self.getTargets():
                print "please select source and destination"
                return "Failed" 
            
            #- create New
            source = self.getTargets()[0]
            targets = self.getTargets()[1:]

            self.write(source, targets)

            return "Success"

    def write(self, source, targets):
        """
        write data
        """        
        data = {}
        data['source']          = source
        data['targets']         = targets
        data['transform']       = cmds.xform(source, q = True, ws = True, t = True)
        data['rotation']        = cmds.xform(source, q = True, ws = True, ro = True)
        for target in targets:
            data[target] = {} 
            data[target]['targetTransform'] = cmds.xform(target, q = True, ws = True, t = True)
            data[target]['targetRotation']  = cmds.xform(target, q = True, ws = True, ro = True)

        with open(self.conItDataPath, 'w') as outfile:
            json.dump(data, outfile)        
        
    def reset(self):
        """
        """
        try:
            if cmds.objExists("fakeCon_loc"):
                cmds.delete("fakeCon_loc")
        except:
            pass
            
        if os.path.exists(self.conItDataPath):
            os.remove(self.conItDataPath)