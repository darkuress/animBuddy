import maya.cmds as cmds
import os
import json

class AnimCopySession:
    def __init__(self):
        """
        """
        filePath = os.path.dirname(os.path.abspath(__file__))
        self.animData = os.path.join(filePath, 'temp.json')
        
        self.sels = cmds.ls(sl = True)
        
    def copyPose(self):
        """
        """
        data = {}
        for sel in self.sels:
            data[sel] = {}
            attrs = cmds.listAttr(sel, keyable = True)
            for attr in attrs:
                data[sel][attr] = cmds.getAttr(sel + '.' + attr)
            
        with open(self.animData, 'w') as outfile:
            json.dump(data, outfile)        

    def copyAnim(self):
        """
        """
        data = {}
        for sel in self.sels:
            data[sel] = {}
            attrs = cmds.listAttr(sel, keyable = True)
            for attr in attrs:
                data[sel][attr] = {'tc' : cmds.keyframe(sel + '.' + attr, q = True, tc = True), 
                                   'vc' : cmds.keyframe(sel + '.' + attr, q = True, vc = True)}
            
        with open(self.animData, 'w') as outfile:
            json.dump(data, outfile)              

    def paste(self):
        """
        """
        with open(self.animData) as jsonFile:
            data = json.load(jsonFile)        

        for obj in data.keys():
            for attr in data[obj].keys():
                # check if data is anim data or pose data
                if isinstance(data[obj][attr], dict):
                    for i in range(len(data[obj][attr]['tc'])):
                        try:
                            cmds.setKeyframe(obj + '.' + attr, 
                                             t = data[obj][attr]['tc'][i],
                                             v = data[obj][attr]['vc'][i])
                        except:
                            pass
                else:
                    try:
                        cmds.setAttr(obj + '.' + attr, data[obj][attr])
                    except:
                        pass
                        
        os.remove(self.animData) 
    
    def run(self):
        """
        """
        if os.path.exists(self.animData):
            print 'pasting animation...'
            self.paste()
        else:
            if cmds.keyframe(self.sels, q = True, tc = True):
                self.copyAnim()
            else:
                print 'copying animation...'
                self.copyPose()

    def reset(self):
        """
        """
        if os.path.exists(self.animData):
            os.remove(self.animData)        
        