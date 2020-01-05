import os
import json
from Utils import System
reload(System)

class Preference(object):
    def __init__(self):
        """
        preference
        """
        filePath = System.dataPath()
        self.prefData = os.path.join(filePath, 'pref.json')
        self.pref = {}

        if os.path.exists(self.prefData):
            self.read()

        #-General
        if self.pref.has_key("iconSize"):
            self.iconSize = self.pref["iconSize"]
        else:
            self.iconSize = 30

        #-EasyInbetween
        if self.pref.has_key("eibMode"):
            self.eibMode = self.pref["eibMode"]
        else:
            self.eibMode = 'object'        

        #-MotionTrail
        if self.pref.has_key("lineWidth"):
            self.lineWidth = self.pref["lineWidth"]
        else:
            self.lineWidth = 3

        if self.pref.has_key("dotSize"):
            self.dotSize = self.pref["dotSize"]
        else:
            self.dotSize = 5
            
        if self.pref.has_key("keyFrameSize"):
            self.keyFrameSize = self.pref["keyFrameSize"]
        else:
            self.keyFrameSize = 7

        if self.pref.has_key("timeBuffer"):
            self.timeBuffer = self.pref["timeBuffer"]
        else:
            self.timeBuffer = 6

        if self.pref.has_key("lineColor"):
            self.lineColor = self.pref["lineColor"]
        else:
            self.lineColor = [1.0, 1.0, 1.0]            

        if self.pref.has_key("dotColor"):
            self.dotColor = self.pref["dotColor"]
        else:
            self.dotColor = [0.0, 0.0, 1.0]   

        if self.pref.has_key("keyFrameColor"):
            self.keyFrameColor = self.pref["keyFrameColor"]
        else:
            self.keyFrameColor = [1.0, 0.0, 0.0]  

        #- Anim Copy Session
        if self.pref.has_key("acsMode"):
            self.acsMode = self.pref["acsMode"]
        else:
            self.acsMode = 'pose'

        #- Decalcomanie
        if self.pref.has_key("dcnMode"):
            self.dcnMode = self.pref["dcnMode"]
        else:
            self.dcnMode = 'pose'

        #- MagicLocator
        if self.pref.has_key("mglMode"):
            self.mglMode = self.pref["mglMode"]
        else:
            self.mglMode = 'pose'

        #-Lockdown
        if self.pref.has_key("ldnMode"):
            self.ldnMode = self.pref["ldnMode"]
        else:
            self.ldnMode = 'translate'

    def construct(self):
        """
        construct preference as dict
        """
        self.pref["iconSize"]        = self.iconSize
        self.pref['eibMode']         = self.eibMode
        self.pref['lineWidth']       = self.lineWidth
        self.pref["dotSize"]         = self.dotSize
        self.pref["keyFrameSize"]    = self.keyFrameSize
        self.pref["timeBuffer"]      = self.timeBuffer
        self.pref["lineColor"]       = self.lineColor
        self.pref["dotColor"]        = self.dotColor
        self.pref["keyFrameColor"]   = self.keyFrameColor
        self.pref['acsMode']         = self.acsMode
        self.pref['dcnMode']         = self.dcnMode
        self.pref['mglMode']         = self.mglMode
        self.pref['ldnMode']         = self.ldnMode

    def write(self):
        """
        write as new pref file
        """
        self.construct()
        with open(self.prefData, 'w') as outfile:
            json.dump(self.pref, outfile, indent = 2)   
    
    def read(self):
        """
        reading from pref.json file
        return dict
        """
        with open(self.prefData) as jsonFile:
            self.prefJson = json.load(jsonFile)

        for key in self.prefJson.keys():
            self.pref[key] = self.prefJson[key]
