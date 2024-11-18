from PyQt6 import QtCore, QtGui, QtWidgets


class MybuttonWidget(QtWidgets.QWidget):
    ImageEventChanged = QtCore.pyqtSignal()
    ButtonClicked = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        super(MybuttonWidget, self).__init__(parent)
        self.MyIconSize = 160
        # self.setStyleSheet(AssetButtonStyleSheet)
        self._IsChecked = False  # state to determin weather the user has checked the masked of the images or not
        self._IncludedInAnalysis = True
        # self.installEventFilter(self)

        self.contextMenu = QtWidgets.QMenu(self)
        IncludeInAnalysisAction = self.contextMenu.addAction("Include in Analysis")
        ExcludeFromAnalysisAction = self.contextMenu.addAction("Exclude from Analysis")
        DeleteButtonAction = self.contextMenu.addAction("Delete Asset")

        IncludeInAnalysisAction.triggered.connect(
            lambda: self.SetAnalysisStatus(Status=True)
        )
        ExcludeFromAnalysisAction.triggered.connect(
            lambda: self.SetAnalysisStatus(Status=False)
        )

    def ResetTools(self):
        """
        Resets all variabels of the mainwindow
        """
        self.parent().i_am_drawing_state_bbox = False
        self.parent().i_am_drawing_state = False
        self.parent().FG_add = True
        self.parent().BG_add = False
        self.parent().during_drawing = False
        self.parent().during_drawing_bbox = False
        self.parent().aa_tool_draw = False
        self.parent().pop_up_tool_choosing_state = False
        self.parent().aa_review_state = False
        self.parent().add_mask_btn_state = True
        self.parent().selection_state = False
        self.parent().worm_mask_points_x = []
        self.parent().worm_mask_points_y = []
        self.parent().temp_mask_to_use_Test_x = []
        self.parent().temp_mask_to_use_Test_y = []
        self.parent().first_x = -1
        self.parent().first_y = -1
        self.parent().list_py = []
        self.parent().list_px = []
        self.parent().temp_mask_to_use_Test_x = []
        self.parent().temp_mask_to_use_Test_y = []
        self.parent().aa_tool_bb_first_x = -1
        self.parent().aa_tool_bb_first_y = -1
        self.parent().prevx = -1
        self.parent().prevx = -1

    def AddPixmapFromImage(self, Image):
        """
        Function to hundle the addiciton of the image
        """
        import cv2

        IconON = QtGui.QIcon()
        IconOFF = QtGui.QIcon()

        # Image = np.require(Image, np.uint8, 'C')

        # Create the On and off variants of the picture by increasing the
        # intensity on th eon vatriant
        try:
            print(Image.shape)
            # Image = cv2.cvtColor(Image.copy(), cv2.COLOR_BGR2RGB)
            ResizedImageQImageOff = QtGui.QImage(
                Image.copy(),
                Image.shape[1],
                Image.shape[0],
                Image.strides[0],
                QtGui.QImage.Format.Format_RGB888,
            ).copy()
            ResizedImageQImageOn = QtGui.QImage(
                cv2.convertScaleAbs(Image.copy(), alpha=4, beta=4),
                Image.shape[1],
                Image.shape[0],
                Image.strides[0],
                QtGui.QImage.Format.Format_RGB888,
            ).copy()

            ResizedImageQPixMapOn = QtGui.QPixmap.fromImage(ResizedImageQImageOn)
            ResizedImageQPixMapOff = QtGui.QPixmap.fromImage(
                ResizedImageQImageOff
            )  # Contrstated Image
            IconON.addPixmap(
                ResizedImageQPixMapOn.copy(),
                QtGui.QIcon.Mode.Normal,
                QtGui.QIcon.State.On,
            )
            IconON.addPixmap(
                ResizedImageQPixMapOff.copy(),
                QtGui.QIcon.Mode.Normal,
                QtGui.QIcon.State.Off,
            )
            self.setIcon(IconON)
            # self.setIcon(IconOFF)
            self.setIconSize(QtCore.QSize(self.MyIconSize, self.MyIconSize))
        except Exception as e:
            print("Cant add image.", e)

    def SetCheckToFalse(self):
        self._IsChecked = False
        self.setStyleSheet(
            """
        QPushButton{
        background-color: #b1b1b1;  
        }
        
        QPushButton:pressed{
        background-color: #b1b1b1;
        }
        """
        )

    def SetCheckToTrue(self):
        self._IsChecked = True
        self.setStyleSheet(
            """
        QPushButton{
        background-color: green;  
        }
        
        QPushButton:pressed{
        background-color: green;
        }
        """
        )

    def contextMenuEvent(self, event):
        action = self.contextMenu.exec(self.mapToGlobal(event.position()))

    def SetAnalysisStatus(self, Status=True):
        self._IncludedInAnalysis = Status
        self.ImageEventChanged.emit()
        print("SetAnalysisStatus emited")
