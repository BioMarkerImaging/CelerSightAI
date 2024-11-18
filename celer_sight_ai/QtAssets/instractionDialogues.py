from PyQt6 import QtGui, QtCore, QtWidgets
import os
from celer_sight_ai.QtAssets.UiFiles.AutoImportInstractions import (
    Ui_Dialog as AutoImportDialog,
)


class ExportNeiralSettingsDialog(AutoImportDialog):
    def __init__(self, MainWindowRef=None, MODE="IMOPRT"):
        self.MainWindow = MainWindowRef
        self.myDialog = QtWidgets.QDialog()
        self.setupUi(self.myDialog)
        if MODE == "IMOPRT":
            myPixmap = QtGui.QPixmap("data\\instractions\\auto_import_instractions.png")
            self.pushButtonSelectFolder.clicked.connect(
                lambda: self.startProccessAutoAnalysis()
            )
        if MODE == "ANALYSIS":
            myPixmap = QtGui.QPixmap(
                "data\\instractions\\auto_analysis_instractions.png"
            )
            self.pushButtonSelectFolder.clicked.connect(
                lambda: self.startProccessAutoAnalysis()
            )

        self.labelInstractions.setPixmap(myPixmap)

        self.myDialog.setStyleSheet(self.MainWindow.styleSheet())
        self.myDialog.exec()

    def startProccessAutoImport(self):
        print("runnign")
        self.myDialog.hide()
        from celer_sight_ai import config

        from celer_sight_ai.QtAssets.UiFiles.LoadingAnimation1 import (
            Ui_Dialog as LoadingAnimationDialogForm,
        )

        LoadingInferenceForm = LoadingAnimationDialogForm()
        LoadingInferenceDialog = QtWidgets.QDialog()
        LoadingInferenceForm.setupUi(LoadingInferenceDialog)
        LoadingInferenceForm.progressBar.hide()
        LoadingInferenceForm.RemainingTimeLabel.hide()
        LoadingInferenceForm.ImportingLabel.setText("Imporing...")
        LoadingInferenceDialog.setWindowTitle("Auto import in progress")
        LoadingInferenceDialog.setWindowFlags(
            QtCore.Qt.Window
            | QtCore.Qt.WindowType.WindowTitleHint
            | QtCore.Qt.CustomizeWindowHint
        )
        LoadingInferenceDialog.show()
        self.MainWindow.OpenFolderTree()
        self.myDialog.close()
        LoadingInferenceDialog.close()

    def startProccessAutoAnalysis(self):
        print("runnign")
        self.myDialog.hide()
        from celer_sight_ai import config

        from celer_sight_ai.QtAssets.UiFiles.LoadingAnimation1 import (
            Ui_Dialog as LoadingAnimationDialogForm,
        )

        LoadingInferenceForm = LoadingAnimationDialogForm()
        LoadingInferenceDialog = QtWidgets.QDialog()
        LoadingInferenceForm.setupUi(LoadingInferenceDialog)
        LoadingInferenceForm.progressBar.hide()
        LoadingInferenceForm.RemainingTimeLabel.hide()
        LoadingInferenceForm.ImportingLabel.setText("Imporing...")
        LoadingInferenceDialog.setWindowTitle("Auto import in progress")
        LoadingInferenceDialog.setWindowFlags(
            QtCore.Qt.Window
            | QtCore.Qt.WindowType.WindowTitleHint
            | QtCore.Qt.CustomizeWindowHint
        )
        LoadingInferenceDialog.show()
        self.MainWindow.OpenFolderTree()
        LoadingInferenceForm.ImportingLabel.setText("Generating masks...")
        LoadingInferenceDialog.setWindowTitle("Mask Generation in progress")
        self.MainWindow.MyDt2Class.DoInferenceAllImagesOnlineThreaded()
        self.myDialog.close()
        LoadingInferenceDialog.close()
        self.MainWindow.RNAi_list.setEnabled(True)
