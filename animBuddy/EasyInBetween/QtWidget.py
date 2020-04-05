from PySide2 import QtWidgets, QtCore, QtGui
from animBuddy.QtHelpers import BSlider
reload(BSlider)
from animBuddy import Preference
reload(Preference)
import Core
reload(Core)

class UIData():
    """
    """
    slider                    = None
    labelMode                 = None
    eibMode                   = None
    floatSliderEIBAmount      = None
    menuObject                = None
    menuKeyFrame              = None
    menuLinear                = None
    popupMenu                 = None
    pref = Preference.Preference()

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
    sliderLayout = QtWidgets.QVBoxLayout()
    UIData.labelMode = QtWidgets.QLabel()
    UIData.labelMode.setText('Mode : Object')

    # ---- menuItem
    UIData.labelMode.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
    UIData.labelMode.customContextMenuRequested.connect(popupHandler)
    UIData.popupMenu = QtWidgets.QMenu()
    ag = QtWidgets.QActionGroup(UIData.labelMode, exclusive=True)
    UIData.menuObject = ag.addAction(QtWidgets.QAction('Object', UIData.popupMenu, checkable=True))
    UIData.popupMenu.addAction(UIData.menuObject)
    UIData.menuKeyFrame = ag.addAction(QtWidgets.QAction('Keyframe', UIData.popupMenu, checkable=True))
    UIData.popupMenu.addAction(UIData.menuKeyFrame)
    UIData.menuLinear = ag.addAction(QtWidgets.QAction('Keyframe (no overshoot)', UIData.popupMenu, checkable=True))
    UIData.popupMenu.addAction(UIData.menuLinear)

    UIData.slider = BSlider.BSlider(colorEnum = "blue", width = 280, minValue=-7, maxValue=7, offsetValue = 5, scaleValue = 10.0, startValue=0, presetsStep=1, handleText = "EI")
    UIData.slider.valueChanged.connect(easyInBetweenChange)

    sliderLayout.addWidget(UIData.labelMode)
    sliderLayout.addWidget(UIData.slider)
    mainLayout.addLayout(sliderLayout)

    readEIBMode()


def popupHandler(position):
    action = UIData.popupMenu.exec_(UIData.labelMode.mapToGlobal(position))  

    if action == UIData.menuObject:
        UIData.eibMode = "object"
        writeEIBMode('object')
        UIData.labelMode.setText('Mode : Object')
    elif action == UIData.menuKeyFrame:
        UIData.eibMode = "keyframe"
        writeEIBMode('keyframe')
        UIData.labelMode.setText('Mode : Keyframe')    
    elif action == UIData.menuLinear:
        UIData.eibMode = "linear"
        writeEIBMode('linear')
        UIData.labelMode.setText('Mode : Keyframe (no overshoot)')   

def test(value):
    offsetValue = 10.0
    print(value/offsetValue)

def easyInBetweenChange(value):
    """
    slider
    """
    offsetFalue = 10.0
    amount = value / offsetFalue

    if UIData.eibMode == 'object':
        Core.changeKey(amount)
    elif UIData.eibMode == 'keyframe':
        Core.changeSelectedKey(amount)
    elif UIData.eibMode == 'linear':
        if amount > 1:
            Core.changeSelectedKey(1)
        elif amount < 0:
            Core.changeSelectedKey(0)
        else:
            Core.changeSelectedKey(amount)

def readEIBMode():
    """
    """
    if UIData.pref.eibMode == 'object':
        UIData.menuObject.setChecked(True)
        UIData.menuKeyFrame.setChecked(False)
        UIData.labelMode.setText('Mode : Object')
        UIData.eibMode = 'object'
    elif UIData.pref.eibMode == 'keyframe':
        UIData.menuObject.setChecked(False)
        UIData.menuKeyFrame.setChecked(True)
        UIData.labelMode.setText('Mode : Keyframe')
        UIData.eibMode = 'keyframe'
    elif UIData.pref.eibMode == 'linear':
        UIData.menuObject.setChecked(False)
        UIData.menuKeyFrame.setChecked(True)
        UIData.labelMode.setText('Mode : Keyframe (no overshoot)')
        UIData.eibMode = 'linear'

def writeEIBMode(mode, *args):
    """
    """
    UIData.pref = Preference.Preference()
    UIData.pref.eibMode = mode
    UIData.pref.construct()
    UIData.pref.write()