import sys

import cv2
import os
import numpy as np
import json

# from detectron2.structures import BoxMode
from PyQt6 import QtGui, QtCore, QtWidgets
from celer_sight_ai.QtAssets.UiFiles.ExportSettingsneural import (
    Ui_ExportNeuralDialog as ExportNeuralDialog,
)


class ExportNeuralSettingsDialog(ExportNeuralDialog):
    def __init__(self, MainWindowRef=None):
        # create the dialog
        self.MainWindow = MainWindowRef
        self.myExportDialog = QtWidgets.QDialog()
        self.setupUi(self.myExportDialog)
        self.retranslateUi(self.myExportDialog)

        self.DictOfImages = {}
        self.DictOfUsedImages = {}

        # Set up the Condition COmbobox
        for Condition, item in self.MainWindow.DH.BLobj.groups["default"].conds.items():
            self.ExportNeuralverticalcomboBoxCondition.addItem(str(Condition))
            self.DictOfImages[str(Condition)] = len(item)
            self.DictOfUsedImages[str(Condition)] = "all"

        self.ExportNeurallineEdit.setText(str("all"))
        self.ExportNeurallineEdit.editingFinished.connect(
            lambda: self.recordCurrentRange()
        )
        self.ExportNeuralbuttonBox.accepted.connect(lambda: self.OnAcceptedRun())
        self.ExportNeuralpushButton.clicked.connect(
            lambda: self.StartExplorerRecordPath()
        )

    def StartExplorerRecordPath(self):
        OutDir = QtWidgets.QFileDialog.getExistingDirectory(
            None, "Select a folder:", "C:\\", QtWidgets.QFileDialog.ShowDirsOnly
        )
        print(OutDir)
        self.ExportNeurallineEdit_2.setText(OutDir)

    def StartSelf(self):
        self.myExportDialog.exec()

    def recordCurrentRange(self):
        self.DictOfUsedImages[
            str(self.ExportNeuralverticalcomboBoxCondition.currentText())
        ] = self.ExportNeurallineEdit.text()

    def GetAllImagesForCondition(self, Condition):
        """
        Gets all numbers for named condition
        """
        allImages = []
        allImagesToString = []
        allImages = (
            self.MainWindow.DH.BLobj.groups["default"].conds[Condition].getAllImages()
        )
        allImagesToString.extend(range(0 - len(allImages)))
        for i in range(len(allImagesToString)):
            allImagesToString[i] = str(allImagesToString[i])
        return allImagesToString

    def OnAcceptedRun(self):
        """
        master function Handles everythign
        """
        self.recordCurrentRange()
        self.DictOfUsedImagesInt = {}
        for key, value in self.MainWindow.DH.BLobj.groups["default"].conds.items():
            self.DictOfUsedImagesInt[key] = self.GetImagePattern(
                self.DictOfUsedImages[key], key
            )

        self.ExportCOCOTools()

    def GetImagePattern(self, TextInput, Condition1):
        """
        gets the patern from the  inpyt string self.ExportNeurallineEdit.text().split(",")
        """
        Stringlist1 = TextInput.split(",")
        if Stringlist1 == ["all"]:
            return self.GetAllImagesForCondition(Condition1)
        for c, item in enumerate(Stringlist1):
            rangeList = []
            try:
                if "-" in item:
                    Stringlist1.remove(item)
                    rangeList = item.split("-")
                    if len(rangeList) != 2:
                        raise Exception("Wrong syntax")
                    Stringlist1.extend(range(int(rangeList[0]), int(rangeList[1]) + 1))
            except:
                pass
        print(Stringlist1)
        for i in range(len(Stringlist1)):
            Stringlist1[i] = int(Stringlist1[i])
        return Stringlist1

    def Check_If_Included_In_ExportList(self, MyCondition, Number):
        """
        Checks if current condition accepts that number
        """
        if self.DictOfUsedImages[MyCondition] == "all":
            return True
        else:
            numb1 = Number + 1
            if numb1 in self.DictOfUsedImagesInt[MyCondition]:
                return True
            else:
                return False

    def ExportCOCOTools(self):
        """
        Function that exports the masks in a json COCO format
        """
        from random import random
        from datetime import datetime
        import skimage
        import MCCocoTools

        ExportDict = {}
        CombinedNameListDict = {}
        CombinedImageListDict = {}
        # Convert the polygons to Bit mask and append everything to COmbined MAsk LIst:
        for Condition, AllImagesOneCondition in self.MainWindow.DH.BLobj.groups[
            "default"
        ].conds.items():  # For every COndition
            CombinedMaskList = []
            CombinedNameList = []
            CombinedImageList = []
            print("for condition: ", Condition)
            # Include all masks with polygons
            for i in range(len(AllImagesOneCondition.images)):  # For every Image
                tmpmask = []
                # temp image list to append to dictionary
                tmpPoints = []

                if self.Check_If_Included_In_ExportList(Condition, i) == True:
                    try:
                        # for every mask
                        for x in range(
                            len(
                                self.MainWindow.DH.BLobj.groups["default"]
                                .conds[Condition]
                                .images[i]
                                .masks
                            )
                        ):
                            raise NotImplementedError(
                                "Fix the .polygon array here to handle more than just polygons"
                            )
                            AllCurrentPoints = self.MainWindow.GetPointsFromQPolygonF(
                                self.MainWindow.DH.BLobj.groups["default"]
                                .conds[Condition]
                                .images[i]
                                .masks[x]
                                .get_array()
                            )

                            if len(AllCurrentPoints) == 0:
                                continue
                            imageShape = (
                                AllImagesOneCondition.getImage(i).shape[0],
                                AllImagesOneCondition.getImage(i).shape[1],
                            )
                            tmpPoints.append(AllCurrentPoints)
                        if len(tmpPoints) == 0:
                            continue
                        CombinedImageList.append(
                            self.MainWindow.DH.BLobj.groups["default"]
                            .conds[Condition]
                            .getImage(i)
                        )
                        CombinedMaskList.append(tmpPoints)
                        CombinedNameList.append(
                            datetime.now().strftime("%m/%d/%Y%H%M%S")
                            + str(int(random() * 100000))
                            + ".png"
                        )
                    except Exception as e:
                        print(e)
                        print("error with condition, skipping...")
            ExportDict[Condition] = CombinedMaskList.copy()
            CombinedNameListDict[Condition] = CombinedNameList.copy()
            CombinedImageListDict[Condition] = CombinedImageList.copy()
        self.MakeDictionaryCOCO(
            FileNameDict=CombinedNameListDict,
            ImageListDict=CombinedImageListDict,
            MaskListDictionary=ExportDict,
            gui_mainLoc=self.MainWindow,
            FolderSaveLocation=self.ExportNeurallineEdit_2.text(),
        )

    def addPaddingToImage(self, imageToAddpad, sizeToPadTo=1360):
        import math

        height = imageToAddpad.shape[1]
        width = imageToAddpad.shape[0]
        print(height)
        print(width)
        print(sizeToPadTo)
        heightIncrease_t = sizeToPadTo - height
        widthIncrease_t = sizeToPadTo - width
        heighIncrease_side = heightIncrease_t / 2
        widthIncrease_side = widthIncrease_t / 2
        leftBorder = math.floor(widthIncrease_side)
        RightBorder = math.ceil(widthIncrease_side)
        TopBorder = math.floor(heighIncrease_side)
        BotBorder = math.ceil(heighIncrease_side)
        imageToAddpad_padded = cv2.copyMakeBorder(
            imageToAddpad,
            int(leftBorder),
            int(RightBorder),
            int(TopBorder),
            int(BotBorder),
            cv2.BORDER_CONSTANT,
            value=(0, 0, 0),
        )
        return imageToAddpad_padded, int(heighIncrease_side), int(widthIncrease_side)

    def convertPointsToPadding(self, allPoints, extended_range):
        outPoints = []
        for point in allPoints:
            outPoints.append(int(point + extended_range))
        return outPoints

    def MakeDictionaryCOCO(
        self,
        FileNameDict,
        ImageListDict,
        MaskListDictionary,
        gui_mainLoc,
        FolderSaveLocation="C:\\Users\\manos\\Documents\\jsonCOCOtest\\train\\",
    ):
        """
        Masks need to be in the following format:
        [[[mask1],[mask2]],[[mask1],[mask2]]
        """
        from pathlib import Path
        import os
        import cv2
        import numpy as np
        import copy

        MasterDict = {}
        # FolderSaveLocation = "C:\\Users\\manos\\Documents\\jsonCOCOtest\\train\\"
        print(FolderSaveLocation)
        print(FileNameDict)
        os.chdir(FolderSaveLocation)
        dict1 = {}
        paddTo = 1320
        for Condition, AllImagesOneCondition in ImageListDict.items():
            print("going through dictionary " + Condition)
            for i in range(len(AllImagesOneCondition)):
                Broke = False
                FileName = FileNameDict[Condition][i]
                # Write Image
                try:
                    FileName = Path(FileName).stem + str(Condition) + ".png"
                except:
                    continue
                FinalFilePath = FolderSaveLocation + "\\" + FileName
                if len(MaskListDictionary[Condition][i]) == 0:
                    continue
                # AllImagesOneCondition[i], extend_height, extend_width = self.addPaddingToImage(AllImagesOneCondition[i])
                cv2.imwrite(FinalFilePath, AllImagesOneCondition[i])
                # Get Image Size
                ImageSizeBytes = int(Path(FinalFilePath).stat().st_size)
                dict2 = {}
                dict3 = {}
                dict4 = {}
                maskiter = 0
                maskNumber = 0
                for mask in range(len(MaskListDictionary[Condition][i])):
                    print("this is list ", MaskListDictionary[Condition][i][mask])
                    try:
                        AllXPoints = np.clip(
                            MaskListDictionary[Condition][i][mask][:, 1].astype(
                                np.uint16
                            ),
                            0,
                            AllImagesOneCondition[i].shape[1] - 1,
                        ).tolist()
                        AllYPoints = np.clip(
                            MaskListDictionary[Condition][i][mask][:, 0].astype(
                                np.uint16
                            ),
                            0,
                            AllImagesOneCondition[i].shape[0] - 1,
                        ).tolist()
                    except Exception as e:
                        print(e)
                        Broke = True
                        break
                    if len(AllXPoints) == 0 or len(AllYPoints) == 0:
                        continue
                    if len(AllXPoints) == 4:
                        # this is a bug, detectron thinks this is a bounding box, repeat last point1-2 times
                        AllXPoints.append(AllXPoints[-1])
                        AllYPoints.append(AllYPoints[-1])
                    if len(AllXPoints) < 4:
                        print("less than 4")

                        continue
                    dict5 = {}
                    dict5["name"] = "polygon"
                    dict5["all_points_x"] = (
                        AllXPoints  # self.convertPointsToPadding(AllXPoints , extend_height)
                    )
                    dict5["all_points_y"] = (
                        AllYPoints  # self.convertPointsToPadding(AllYPoints , extend_width)
                    )
                    dict4["shape_attributes"] = copy.deepcopy(dict5)
                    dict4["region_attributes"] = {}
                    dict3[str(maskiter)] = copy.deepcopy(dict4)
                    maskiter += 1
                    maskNumber += 1
                if Broke == True:
                    continue
                dict2 = {}
                dict2["fileref"] = ""
                dict2["size"] = ImageSizeBytes
                dict2["filename"] = str(FileName)
                dict2["base64_img_data"] = ""
                dict2["file_attributes"] = {}
                dict2["regions"] = copy.deepcopy(dict3)
                dict1[str(FileName) + str(ImageSizeBytes)] = copy.deepcopy(dict2)
        import json

        with open(FolderSaveLocation + "\\via_region_data.json", "w") as fp:
            json.dump(dict1, fp)


if __name__ == "__main__":
    pass
