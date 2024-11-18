from PyQt6 import QtCore, QtGui, QtWidgets
from celer_sight_ai.QtAssets.UiFiles.MaskButtonWidgetSofia import (
    Ui_Form as MaskWidget,
)
import numpy as np


class AssetMaskSofia(QtWidgets.QWidget):
    """
    A widget that takes care of the masks on the second tab of overview s
    """

    DeleteMeBOOL = QtCore.pyqtSignal(int)
    DeleteMePOLYGON = QtCore.pyqtSignal(int)
    MaskPropertiesChanged = QtCore.pyqtSignal()

    def __init__(
        self,
        parent,
        NumberIn,
        MaskType,
        MasterCombobox,
        MasterMaskLabelcomboBoxSIGNAL_Inherited,
        MainWindowReference,
        LoadSettings=None,
    ):  # master combo box is a reference to self.MasterMaskLabelcomboBox
        super(AssetMaskSofia, self).__init__(parent)
        self.MaskType = ""  # can be BOOL or POLYGON
        self.LoadSettings = LoadSettings
        self.MasterCombobox = MasterCombobox
        self.CurrentMaskNumber = NumberIn
        self.LoadedSettings = False
        self.setObjectName("SofiaWidget")
        self.BBWidget = MaskWidget()
        self.BBWidget.setupUi(self)
        self.BBWidget.retranslateUi(self)
        self.MaskColor = np.array([255, 255, 255])

        self.eyeIconReference = self.findChild(QtWidgets.QPushButton, "EyeIcon")
        self.eyeIconReference.setCheckable(True)
        self.eyeIconReference.setChecked(True)
        self.eyeIconReference.clicked.connect(
            lambda: MainWindowReference.load_main_scene(
                MainWindowReference.current_imagenumber
            )
        )

        self.AnnotationTypeReference = self.findChild(
            QtWidgets.QPushButton, "ArrayPropertiesWidgetbtn"
        )
        self.AnnotationTypeReference.setCheckable(False)

        self.RegionAttribute = None
        self.SelectedColor = "#ffa02f"
        self.NotSelectedColor = "#5f6678"
        self.MiniMask = []
        self.MasterMaskLabelcomboBoxSIGNAL_Inherited = (
            MasterMaskLabelcomboBoxSIGNAL_Inherited
        )

        self.contextMenu = QtWidgets.QMenu(self)
        IncludeInAnalysisAction = self.contextMenu.addAction("Include in Analysis")
        ExcludeFromAnalysisAction = self.contextMenu.addAction("Exclude from Analysis")
        DeleteButtonAction = self.contextMenu.addAction("Delete Asset")
        DeleteButtonAction.triggered.connect(lambda: self.DelectedCurrent())

    def contextMenuEvent(self, event):
        action = self.contextMenu.exec(self.mapToGlobal(event.position()))

    def DelectedCurrent(self):
        """
        deletes current mask and self (signal)
        """
        if self.MaskType == "BOOL":
            self.DeleteMeBOOL.emit(int(self.CurrentMaskNumber))
        elif self.MaskType == "POLYGON":
            self.DeleteMePOLYGON.emit(int(self.CurrentMaskNumber))

    def UnloadSettingsToDictionary(self):
        """
        Because we cant pickle save the object we need to save all the settings
        to a dictionary sot hat we can load it after
        """
        SettingsDictionary = {}
        SettingsDictionary["RegionAttribute"] = self.RegionAttribute
        SettingsDictionary["MiniMask"] = self.MiniMask
        return SettingsDictionary

    def LoadSettingsDictinoary(self, MyDictionary):
        import numpy as np

        self.LoadedSettings = True
        self.RegionAttribute = MyDictionary["RegionAttribute"]
        if isinstance(MyDictionary["MiniMask"], (list, np.ndarray)):
            self.MiniMask = MyDictionary["MiniMask"].copy()

    def InitFromLoad(self):
        """
        Initialize a mask when loading a plaba object instead of creating one form the UI
        """
        self.LoadSettingsDictinoary(self.LoadSettings)
        # self.UpdatePreview()

        self.MasterMaskLabelcomboBoxSIGNAL_Inherited.connect(self.blockSignals)
        self.MasterMaskLabelcomboBoxSIGNAL_Inherited.connect(
            lambda: QtWidgets.QApplication.processEvents()
        )
        self.MasterMaskLabelcomboBoxSIGNAL_Inherited.connect(
            self.SetColorNameOfAnnotation
        )
        self.MasterMaskLabelcomboBoxSIGNAL_Inherited.connect(self.GetComboboxItems)
        self.MasterMaskLabelcomboBoxSIGNAL_Inherited.connect(
            self.ConnectSingalsAssetMask
        )

    def InitializeAll(self):
        # self.GetComboboxItems()
        # Runs once in the begginin
        # print("parent is 1 ", self.parent())
        self.SetColorNameOfAnnotation()
        self.GetComboboxItems()
        # Runs when changed

        # We need to block the signals so that we dong initiate an infinite loop

        # THIS ONLY WORKS LIKE THIS
        # because if we include parenthsis then we get a nonetype object as a first argument
        # if we include lambda: the signal doesnt get deleted and we crush

        self.MasterMaskLabelcomboBoxSIGNAL_Inherited.connect(self.blockSignals)
        self.MasterMaskLabelcomboBoxSIGNAL_Inherited.connect(
            lambda: QtWidgets.QApplication.processEvents()
        )
        self.MasterMaskLabelcomboBoxSIGNAL_Inherited.connect(
            self.SetColorNameOfAnnotation
        )
        self.MasterMaskLabelcomboBoxSIGNAL_Inherited.connect(self.GetComboboxItems)
        self.MasterMaskLabelcomboBoxSIGNAL_Inherited.connect(
            self.ConnectSingalsAssetMask
        )
        # self.MasterMaskLabelcomboBoxSIGNAL_Inherited.connect(lambda: self.BBWidget.MaskPropertiesWidgetLabelcomboBox.setEnabled(True))
        return

    def blockSignals(self):
        """
        THis becomes a function so that we can disconnecte it later
        it stopes all the signals when we check the combobox
        """
        # print("BlockSingalsAssetMask start")

        self.BBWidget.MaskPropertiesWidgetLabelcomboBox.blockSignals(True)

        # print("BlockSingalsAssetMask mid")

        self.BBWidget.MaskPropertiesWidgetLabelcomboBox.setEnabled(False)
        # print("BlockSingalsAssetMask end")

        pass

    def ConnectSingalsAssetMask(self):
        """
        THis becomes a function so that we can disconnecte it later
        it stopes all the signals when we check the combobox
        """
        # print("ConnectSingalsAssetMask start")
        self.BBWidget.MaskPropertiesWidgetLabelcomboBox.blockSignals(False)
        # print("ConnectSingalsAssetMask mid")

        self.BBWidget.MaskPropertiesWidgetLabelcomboBox.setEnabled(True)
        # print("ConnectSingalsAssetMask end")

        pass

    def DisconnectAllOnDeletion(self, fa, fb, fc, fe):
        try:
            self.MasterCombobox.currentIndexChanged.disconnect(fa)
        except:
            pass
        try:
            self.MasterCombobox.currentIndexChanged.disconnect(fb)
        except:
            pass
        try:
            self.MasterCombobox.currentIndexChanged.disconnect(fc)
        except:
            pass
        try:
            self.MasterCombobox.currentIndexChanged.disconnect(fe)
        except:
            pass

    # @QtCore. pyqtSlot()
    def SetColorNameOfAnnotation(self):
        print("--------------SetColorNameOfAnnotation-----------------")
        combobox = self.MasterCombobox

        print("combobox is ", combobox)
        try:
            for i in range(combobox.count()):
                # print(combobox.itemData(i, QtCore.Qt.BackgroundRole))
                if (
                    self.BBWidget.MaskPropertiesWidgetLabelcomboBox.text()
                    == combobox.itemText(i)
                ):
                    self.setStyleSheet(
                        "background-color:"
                        + combobox.itemData(i, QtCore.Qt.BackgroundRole).name()
                        + ";"
                    )
        except Exception as e:
            print("at SetColorNameOfAnnotation")
            print(e)
            pass

    # @QtCore. pyqtSlot()
    def GetComboboxItems(self):
        # print("---------------GetComboboxItems----------------")
        # combobox =self.MasterCombobox
        # print("combobox is ",combobox)
        try:
            TmpMasterComboboxIndex = self.MasterCombobox.currentIndex()

            print("current new index GetComboboxItems is ", TmpMasterComboboxIndex)

            if self.RegionAttribute == None:
                self.RegionAttribute = str(self.MasterCombobox.currentText())
                self.BBWidget.MaskPropertiesWidgetLabelcomboBox.setText(
                    self.RegionAttribute
                )
            else:
                try:
                    # we get the recorded region anntatino data (qcombobox item last assigned) and make sure its selected

                    self.BBWidget.MaskPropertiesWidgetLabelcomboBox.setText(
                        self.RegionAttribute
                    )
                # if we get an error that means that the item got deleted, so we select the first one
                except Exception as e:
                    print("at GetCOmboboxItem")
                    print(e)
        except Exception as e:
            print(e)
        print("finisehd GetComboboxItems")

    @QtCore.pyqtSlot()
    def UpdatePreview(self, Mask=None):
        """
        Update the preview area of the widget, the cut out mask comes in
        then it gets resized and applied
        """
        import numpy as np

        if self.MiniMask == [] and isinstance(Mask, (list, np.ndarray)):
            if type(Mask[0]) == bool:
                Mask = Mask.astype(np.uint8)
            self.MiniMask = self.MinimizeMask(Mask, 70, 70).astype(np.uint8)
        else:
            return
        MiniMaskicon = QtGui.QIcon()
        import cv2

        Mask = Mask * 255
        # Mask = cv2.cvtColor(Mask, cv2.COLOR_GRAY2RGB)

        PixmapMiniMask = QtGui.QPixmap.fromImage(
            QtGui.QImage(
                self.MiniMask,
                self.MiniMask.shape[1],
                self.MiniMask.shape[0],
                QtGui.QImage.Format_Indexed8,
            )
        )
        MiniMaskicon.addPixmap(
            PixmapMiniMask, QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off
        )

        self.BBWidget.MaskPropertiesWidgetbtn.setIcon(MiniMaskicon)
        self.BBWidget.MaskPropertiesWidgetbtn.setIconSize(QtCore.QSize(70, 70))

    def MinimizeMask(self, Mask, width, height):
        from skimage.transform import resize

        ResizedImage = resize(
            Mask, (width, height), anti_aliasing=False, preserve_range=True
        )
        return ResizedImage
