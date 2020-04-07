# -*- coding: utf-8 -*-
from PySide2 import QtWidgets, QtCore, QtGui

def separator(vertical = False):
    """
    """
    if vertical:
        separator = QtWidgets.QFrame()
        separator.setFrameShape(QtWidgets.QFrame.VLine)
        separator.setFrameShadow(QtWidgets.QFrame.Sunken)
    else:
        separator = QtWidgets.QSplitter() 
    
    separator.setSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
    return separator