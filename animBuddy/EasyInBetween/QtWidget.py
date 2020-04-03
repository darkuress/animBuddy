from PySide2 import QtWidgets, QtCore, QtGui
from animBuddy.QtHelpers import BSlider
reload(BSlider)

def build(parent, 
          imagesPath, 
          iconSize = 25,
          height = 20, 
          marginSize = 5):
    """
    build widget
    @param parent : parent qt layout 
    @imagesPath : str path
    """
    #- Reset It---------------------------------------------------------------
    mainLayout = parent
    a = BSlider.BSlider(colorEnum = "blue", width = 280, minValue=-7, maxValue=7, offsetValue = 5, scaleValue = 10.0, startValue=0, presetsStep=1, handleText = "EI")
    b = BSlider.BSlider(colorEnum = "green", width = 300, minValue=0, maxValue=100, startValue=0, handleText = "fuck", trail = False)
    c = BSlider.BSlider(colorEnum = "pink", width = 300, minValue=0, maxValue=50, presetsStep=10, startValue=0, handleText = "lalaal", handleSticked=False)
    a.valueChanged.connect(test)
    c.valueChanged.connect(test)
    mainLayout.addWidget(a)
    #mainLayout.addWidget(b)
    #self.mainLayout.addWidget(c)

def test(value):
    offsetValue = 10.0
    print(value/offsetValue)