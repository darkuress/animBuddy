from maya import OpenMayaUI as omui
from PySide2 import QtCore
from PySide2 import QtGui
from PySide2 import QtWidgets
from PySide2 import __version__
from shiboken2 import wrapInstance 
from animBuddy.SelectionGrp import Core as SGP
reload(SGP)

def maya_main_window():
    '''
    Return the Maya main window widget as a Python object
    '''
    main_window_ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(long(main_window_ptr), QtWidgets.QWidget)

class ImportUI(QtWidgets.QDialog):
    def __init__(self, parent=maya_main_window()):
        super(ImportUI, self).__init__(parent)
        self.qtSignal = QtCore.Signal()
        self.SGP = SGP.SelectionGrp()
        #################################################################

    def create(self):
        self.setWindowTitle("Import Selection Group")
        self.setWindowFlags(QtCore.Qt.Tool)
        self.resize(300, 400) # re-size the window
        self.mainLayout = QtWidgets.QVBoxLayout(self)
        self.buttonLayout = QtWidgets.QHBoxLayout(self)


        self.listviewGrps = QtWidgets.QListWidget()
        self.listviewGrps.resize(300, 300)
        self.listviewGrps.itemSelectionChanged.connect(self.getCurrentGrp)
        self.rebuildExportedGrps()

        self.importButton = QtWidgets.QPushButton("Import")
        self.importButton.clicked.connect(self.importGrp)
        self.deleteButton = QtWidgets.QPushButton("Delete")
        self.deleteButton.clicked.connect(self.deleteGrp)
        
        self.mainLayout.addWidget(self.listviewGrps)
        self.buttonLayout.addWidget(self.importButton)
        self.buttonLayout.addWidget(self.deleteButton)
        self.mainLayout.addLayout(self.buttonLayout)

    
    def rebuildExportedGrps(self):
        allGrps = self.SGP.getAllExportedGrps()
        if allGrps:
            self.listviewGrps.clear()
            for grp in allGrps:
                self.listviewGrps.addItem(grp)

    def importGrp(self, *args):
        """
        """
        self.SGP.importGrp(self.getCurrentGrp())
        
        import QtUISelectionGrp
        reload(QtUISelectionGrp)
        QtUISelectionGrp.reopen()

    def getCurrentGrp(self):
        if self.listviewGrps.selectedItems():           
            return self.listviewGrps.selectedItems()[0].text()
        else:
            return ""

    def deleteGrp(self, *args):
        """
        """
        currentGrp = self.getCurrentGrp()
        self.SGP.deleteGrp(currentGrp)
        self.rebuildExportedGrps()

if __name__ == "__main__":
    try:
        ui.deleteLater()
    except:
        pass
    ui = ImportUI()
    
    try:
        ui.create()
        ui.show()
    except:
        ui.deleteLater()