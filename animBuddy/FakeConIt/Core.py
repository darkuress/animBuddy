import maya.cmds as cmds
import os
import json

class FakeConIt:
    def __init__(self):
        filePath = os.path.dirname(os.path.abspath(__file__))
        self.conItDataPath = os.path.join(filePath, 'temp.json')

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
        if not self.getTargets():
            "please select source and destination"
            return

        source = self.getTargets()[0]
        targets = self.getTargets()[1:]
        
        if source and os.path.exists(self.conItDataPath):
            with open(self.conItDataPath) as jsonFile:
                data = json.load(jsonFile)
                if data['source'] == source:
                    targets = data['targets']
                    
                    #create fake locator to constraint
                    loc = cmds.spaceLocator(n = "fakeCon_loc")
                    cmds.xform(loc, t = data['transform'], ro = data['rotation'])
                    for target in data['targets']:
                        try:
                            cmds.parentConstraint(loc, target, mo = True, weight = 1)
                        except:
                            print "destination's translation or rotation might be locked"
                            return
                        
                    #get current transform
                    tr = cmds.xform(source, q = True, ws = True, t = True)
                    ro = cmds.xform(source, q = True, ws = True, ro = True) 

                    #rotate locator
                    cmds.xform(loc, t = tr, ro = ro)
                    
                    for target in data['targets']:
                        pcon = cmds.listRelatives(target, type = "parentConstraint")
                        cmds.delete(pcon)
                    
                    cmds.delete(loc)
                    
                else:
                    os.remove(self.conItDataPath)
        
        data = {}
        data['source'] = source
        data['targets'] = targets
        data['transform'] = cmds.xform(source, q = True, ws = True, t = True)
        data['rotation'] = cmds.xform(source, q = True, ws = True, ro = True)

        with open(self.conItDataPath, 'w') as outfile:
            json.dump(data, outfile)        
        
    def reset(self):
        """
        """
        try:
            cmds.delete(cmds.ls("fakeCon_loc"))
        except:
            pass
            
        if os.path.exists(self.conItDataPath):
            os.remove(self.conItDataPath)