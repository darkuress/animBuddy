import maya.cmds as cmds
import os
import json
from animBuddy.Utils import Util
reload(Util)

class AnimCopySession:
    def __init__(self):
        """
        """
        filePath = Util.dataPath()
        #filePath = os.path.dirname(os.path.abspath(__file__))
        self.animData = os.path.join(filePath, 'animCopySession.json')
        
        self.data = {}
        self.sels = cmds.ls(sl = True)
        
    def copyPose(self, sel):
        """
        """
        self.data[sel] = {}
        attrs = cmds.listAttr(sel, keyable = True)
        for attr in attrs:
            self.data[sel][attr] = cmds.getAttr(sel + '.' + attr)

    def copyAnim(self, sel):
        """
        """
        self.data[sel] = {}
        attrs = cmds.listAttr(sel, keyable = True)
        for attr in attrs:
            self.data[sel][attr] = {'tc' : cmds.keyframe(sel + '.' + attr, q = True, tc = True), 
                                    'vc' : cmds.keyframe(sel + '.' + attr, q = True, vc = True)}
                     
    def copy(self):
        """
        """
        with open(self.animData, 'w') as outfile:
            json.dump(self.data, outfile, indent = 2)   

    def paste(self):
        """
        """
        with open(self.animData) as jsonFile:
            self.data = json.load(jsonFile)        

        for obj in self.data.keys():
            for attr in self.data[obj].keys():
                # check if self.data is anim self.data or pose self.data
                if isinstance(self.data[obj][attr], dict):
                    if not self.data[obj][attr]['tc'] == None:
                        for i in range(len(self.data[obj][attr]['tc'])):
                            try:
                                cmds.setKeyframe(obj + '.' + attr, 
                                                t = self.data[obj][attr]['tc'][i],
                                                v = self.data[obj][attr]['vc'][i])
                            except:
                                pass
                else:
                    try:
                        cmds.setAttr(obj + '.' + attr, self.data[obj][attr])
                    except:
                        pass
                        
        os.remove(self.animData) 
    
    def run(self, mode = 'pose'):
        """
        """
        if os.path.exists(self.animData):
            print 'pasting animation...'
            self.paste()
            return "paste"
        else:
            self.data = {}
            for sel in self.sels:
                """
                if cmds.keyframe(sel, q = True, tc = True):
                    print 'copying animation...', sel
                    self.copyAnim(sel)
                else:
                    print 'copying pose........', sel
                    self.copyPose(sel)
                """
                if mode == 'pose':
                    print 'copying pose........', sel
                    self.copyPose(sel)
                elif mode == 'anim':
                    print 'copying animation...', sel
                    self.copyAnim(sel)
            self.copy()
            return "copy"

    def reset(self):
        """
        """
        if os.path.exists(self.animData):
            os.remove(self.animData)        
        