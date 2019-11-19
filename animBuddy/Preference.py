import os
import json

class Preference(object):
    def __init__(self):
        """
        preference
        """
        filePath = os.path.dirname(os.path.abspath(__file__))
        self.prefData = os.path.join(filePath, 'pref.json')
        self.pref = {}

        if os.path.exists(self.prefData):
            self.read()

        #-General
        if self.pref.has_key("iconSize"):
            self.iconSize = self.pref["iconSize"]
        else:
            self.iconSize = 30

        #-MotionTrail
        if self.pref.has_key("lineWidth"):
            self.lineWidth = self.pref["lineWidth"]
        else:
            self.lineWidth = 3

        if self.pref.has_key("dotSize"):
            self.dotSize = self.pref["dotSize"]
        else:
            self.dotSize = 0.2
            
        if self.pref.has_key("keyFrameSize"):
            self.keyFrameSize = self.pref["keyFrameSize"]
        else:
            self.keyFrameSize = 0.25

        if self.pref.has_key("timeBuffer"):
            self.timeBuffer = self.pref["timeBuffer"]
        else:
            self.timeBuffer = 10

        if self.pref.has_key("lineColor"):
            self.lineColor = self.pref["lineColor"]
        else:
            self.lineColor = [1.0, 1.0, 1.0]            

    def construct(self):
        """
        construct preference as dict
        """
        self.pref["iconSize"]     = self.iconSize
        self.pref["dotSize"]      = self.dotSize
        self.pref["keyFrameSize"] = self.keyFrameSize
        self.pref["timeBuffer"]   = self.timeBuffer
        
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
