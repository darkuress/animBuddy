from PySide2 import QtWidgets, QtCore, QtGui
import maya.OpenMayaUI as OpenMayaUI
from shiboken2 import wrapInstance
import maya.cmds as cmds 
import maya.mel as mel
import time 

COLOR_LIST = {  "red"   : [240, 79, 67],
                "blue"  : [67, 171, 240],
                "pink"  : [230, 99, 223],
                "green" : [99, 230, 147],
                "orange": [245,177,83]}


class SMath(object):

    @staticmethod
    def fit2RangeVal( vMin, vMax, pMin, pMax, pos):
        #get 1% of pos range
        pos_percent = float(pMax - pMin) / float(vMax - vMin) # 2.5
    
        val = (pos - 10) / float(pos_percent)

        val = vMin + val
        
        return int(round(val,0))

    @staticmethod
    def fit2RangePos( vMin, vMax, pMin, pMax, val):
        
        #get 1% of pos range
        pos_percent = (pMax - pMin) / 100.0

        #get 1% of val range
        val_percent = (vMax - vMin) / 100.0

        # what val % in range {vMin, vMax}
        abs_value = abs(vMin) + val
        abs_value_percentage = abs_value / float(val_percent)

        # get pos % in range {pMin, pMax} knowing value percentage
        pos_percentage = pMin + pos_percent * abs_value_percentage

        return int(pos_percentage)




class BSlider(QtWidgets.QWidget):

    # widget signals
    valueChanged = QtCore.Signal(int)
    handlePressed = QtCore.Signal(int)
    handleReleased = QtCore.Signal(int)

    def __init__(self,  colorRGB        = [], 
                        colorEnum       = "green", 
                        handleText      = "ab", 
                        handleSticked   = True, 
                        width           = 300, 
                        height          = 20,
                        minValue        = -20,
                        maxValue        = 100,
                        startValue      = 30 ,
                        trail           = True,
                        presetsShow     = True,
                        presetsStep     = 20
                        ):

        super(BSlider, self).__init__()

        # widget settings
        
        if len(handleText) > 2:
            handleText = handleText[0:2]

        if colorRGB: 
            self._uiColor       = colorRGB
        else: 
            self._uiColor       = COLOR_LIST[colorEnum]

        # Common Slider attributes
        self._sliderWidth       = width
        self._sliderHeight      = height
        self._minValue          = minValue
        self._maxValue          = maxValue
        self._startValue        = startValue
        self._prevValue         = 0
        self._outputValue       = 0 # the actual percent on the slider
        self._presetMouseOver   = None

        # HANDLE attributes
        self._hSize             = 20
        self._hText             = handleText.upper()
        self._hGeom             = [[],[]]
        self._hPressed          = False
        self._hClickOffset      = None
        self._hClickPos         = None
        self._hInitClickPos     = None
        self._hTrail            = trail
        self._hStick            = handleSticked
        
        # PRESETS attributes
        self._pShow             = presetsShow
        self._pStep             = presetsStep

        # calculate preset circles position based on min value, max value and steps
        # dependencies: self._pStep
        self._presetPositions   = self.getPresetValues() 


        # qt settings
        self.setFixedSize(self._sliderWidth, self._sliderHeight)
        self.setAutoFillBackground(True)
        self.setMouseTracking(True)
        # self.setBackgroundColor()
        self.handleRect(value = self._startValue)

    def setBackgroundColor(self, rgb = [60,60,60]):
        """
        Public
        """
        self.p = self.palette()
        self.p.setColor(self.backgroundRole(), QtGui.QColor(rgb[0],rgb[1],rgb[2]))
        self.setPalette(self.p)


    def handleRect(self, value = None, position = None):

        # get handle drawing coordinates based on the slider options
        startPos = 0

        if value != None:
            startPos = SMath.fit2RangePos(self._minValue, self._maxValue, 0, self._sliderWidth, value)
        elif position != None:
            startPos = position - 10
        
        #Correct coordinates
        if startPos < 10:
            startPos = 10
        elif startPos > self._sliderWidth - 10:
            startPos = self._sliderWidth - 10

        self._hGeom = [[startPos - 10, startPos + 10],[self._sliderHeight/2 - 10, self._sliderHeight/2 + 10]]


    def handleLeftBorder(self):

        if self._hClickPos and self._hClickOffset:
            position = self._hClickPos.x() - self._hClickOffset
            return position


    def handleCenter(self):

        center = self.handleLeftBorder() + self._hSize/2
 

        if center > self._sliderWidth - self._hSize/2: 
            center = self._sliderWidth - self._hSize/2
        elif center < 10: 
            center = 10


        return center


    def getPresetValues(self):

        outputPositions = []
        for i in range(self._minValue, self._maxValue + 1, self._pStep):
            pos = SMath.fit2RangePos(self._minValue, self._maxValue, 10, self._sliderWidth-10, i)
            outputPositions.append(pos)

        return outputPositions


    def _uiDrawRangeLine(self, painter):

        painter.setPen(QtGui.QColor(40,40,40))
        painter.setBrush(QtGui.QColor(40,40,40))

        if self._hPressed:
            x = 0
            y = self._sliderHeight/2 - self._hSize/2
            width = self._sliderWidth
            height = self._hSize

            painter.drawRoundedRect( QtCore.QRectF(x, y, width, height), 5, 5)

        else:
            x = 0
            y = self._sliderHeight/2 - 5
            width = self._sliderWidth
            height = 10

            painter.drawRoundedRect( QtCore.QRectF(x, y, width, height), 5, 5)


    def _uiDrawHandle(self, painter):

        painter.setPen(QtGui.QColor(self._uiColor[0], self._uiColor[1], self._uiColor[2]))
        painter.setBrush(QtGui.QColor(self._uiColor[0], self._uiColor[1], self._uiColor[2]))

        offset_x = 0
        if self._hPressed:
            # start calculating handle start position on the slider's line
            offset_x = self.handleLeftBorder()
            offset_y = self._sliderHeight/2 - 10

            if offset_x > self._sliderWidth - self._hSize: 
                offset_x = self._sliderWidth - self._hSize
            elif offset_x < 0: 
                offset_x = 0

            painter.drawRoundedRect(QtCore.QRectF( offset_x , offset_y, self._hSize, self._hSize), 5,5)


        else:
            offset_x = self._hGeom[0][0]
            offset_y = self._sliderHeight/2 - 10
            painter.drawRoundedRect(QtCore.QRectF( offset_x , offset_y, self._hSize, self._hSize), 5,5)

        painter.setPen(QtGui.QColor(0,0,0))
        painter.setFont(QtGui.QFont("console", 8, weight = 75))
        painter.drawText(offset_x  + 2, 15, self._hText)


    def _uiPresetCircles(self, painter):

        painter.setPen(QtGui.QColor(self._uiColor[0], self._uiColor[1], self._uiColor[2]))
        painter.setBrush(QtGui.QColor(self._uiColor[0], self._uiColor[1], self._uiColor[2]))

        if not self._hPressed:

            # values = self.getPresetValues()
            for idx, i in enumerate(self._presetPositions):

                if idx == 0 or idx == len(self._presetPositions) - 1:
                    painter.drawRect(i - 3, 10-3, 6, 6)
                else:
                    painter.drawRect(i - 1, 10-1, 2, 2)


    def _uiDrawValueText(self, painter):

        painter.setFont(QtGui.QFont("console", 12))
        painter.setPen(QtGui.QColor(110,110,110))

        if self._hPressed:

            self._outputValue = SMath.fit2RangeVal(self._minValue, self._maxValue, 10, self._sliderWidth-10, self.handleCenter())


            if self.handleCenter() > self._sliderWidth / 2:
                painter.drawText( 10, 16, str(self._outputValue)) 
            else:
                right_border_offset = self._sliderWidth - 25 - pow(len(str(self._outputValue)), 2)
                painter.drawText( right_border_offset, 16, str(self._outputValue)) 

    def _uiDrawHandleTrail(self, painter):

        painter.setPen(QtGui.QColor(self._uiColor[0], self._uiColor[1], self._uiColor[2]))
        painter.setBrush(QtGui.QColor(self._uiColor[0], self._uiColor[1], self._uiColor[2]))

        if self._hPressed:

            x = self._hInitClickPos.x() - self._hClickOffset + self._hSize/2
            y = self._sliderHeight/2 - 1
            width = self.handleCenter() - x
            height = 2
            painter.drawRoundedRect(QtCore.QRectF(x ,y, width, height), 0,0)


    def mousePressEvent(self, event):

        xmin = self._hGeom[0][0]
        xmax = self._hGeom[0][1]
        ymin = self._hGeom[1][0]
        ymax = self._hGeom[1][1]

        posX = event.pos().x()
        posY = event.pos().y()

        if xmin < posX < xmax and ymin < posY < ymax:

            self.handlePressed.emit(self._outputValue)

            self._hPressed = True
            self._hClickPos = event.pos()
            self._hInitClickPos = event.pos()
            self._hClickOffset = posX - xmin
            
            self.update()

        else:
            for i in self._presetPositions:
                if i - 5 < posX < i + 5 and 10 - 3 < posY < 10 + 3: 
                    self._hGeom = [[i - 10, i + 10],[self._sliderHeight/2 - 10, self._sliderHeight/2 + 10]]
                    self.mousePressEvent(event)


    def mouseReleaseEvent(self, event):

        self.handleReleased.emit(self._outputValue)

        if self._hStick:
            self._outputValue = self._startValue
            self.handleRect(value = self._startValue)

        else:
            if self._hPressed:
                if event.pos().x() > self._sliderWidth - self._hSize/2: 
                    self._hGeom        = [[self._sliderWidth - self._hSize, self._sliderWidth],[0,20]]
                elif event.pos().x() < 0: 
                    self._hGeom        = [[0, self._hSize],[0,20]]
                else:
                    self._hGeom = [[event.pos().x() - 10, event.pos().x() + 10],[0,20]]

        self._hClickPos = None
        self._hClickOffset = None     
        self._hPressed = False
        self.update()
        


    def mouseMoveEvent(self, event):

        if self._hPressed:
            self._hClickPos = event.pos()
            self.update()
        

    def paintEvent(self, event):

        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        
        self._uiDrawRangeLine(painter)
        self._uiDrawValueText(painter)

        if self._pShow: 
            self._uiPresetCircles(painter)

        if self._hTrail:
            self._uiDrawHandleTrail(painter)

        self._uiDrawHandle(painter)
        

        

        '''
        We do painter.save() to save the painter state to a stack
        We do painter.restore() to restore painter state from a stack
        All not painting actions must be in between of these two lines
        '''
        painter.save()
        if self._outputValue != self._prevValue:
            self.valueChanged.emit(self._outputValue)
        self._prevValue = self._outputValue
        painter.restore()

class MToolBar(QtWidgets.QWidget):

    def __init__(self, parent = None, name = None):
        super(MToolBar, self).__init__()

        self.setObjectName(name)

        self.setMinimumHeight(50)
        self.mainLayout = QtWidgets.QHBoxLayout()
        self.mainLayout.setAlignment(QtCore.Qt.AlignLeft)
        self.mainLayout.setSpacing(30)
        self.setLayout(self.mainLayout)

        self.keyValue = 0

        a = BSlider(colorEnum = "red", width = 250, minValue=-100, maxValue=100, startValue=0,handleText = "bro")
        b = BSlider(colorEnum = "green", width = 300, minValue=0, maxValue=100, startValue=0, handleText = "fuck", trail = False)
        c = BSlider(colorEnum = "pink", width = 300, minValue=0, maxValue=50, presetsStep=10, startValue=0, handleText = "lalaal", handleSticked=False)
        a.valueChanged.connect(self.test)
        c.valueChanged.connect(self.test)
        self.mainLayout.addWidget(a)
        self.mainLayout.addWidget(b)
        self.mainLayout.addWidget(c)

        ss = QtWidgets.QSlider()
        ss.setOrientation(QtCore.Qt.Horizontal)
        self.mainLayout.addWidget(ss)

    def test(self, value):
        print(value)
        
def cleanUI(name):

    wgtPtr = OpenMayaUI.MQtUtil.findControl(name)
    if wgtPtr:
        wgt = wrapInstance(long(wgtPtr), QtWidgets.QWidget)
        wgt.deleteLater()

def insertUI():

    ctrl = OpenMayaUI.MQtUtil.findControl('TimeSlider')
    ctrlWgt = wrapInstance(long(ctrl), QtWidgets.QWidget)
    
    x = ctrlWgt.parent().parent().parent()
    x.insertWidget(3, MToolBar(name = 'testWindow'))# QSplitter [1,2,3,4,5,6,]

def main():
  
    cleanUI('testWindow')
    insertUI()
    
main()