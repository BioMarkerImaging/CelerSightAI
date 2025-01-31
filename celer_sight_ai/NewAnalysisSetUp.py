import os
import sys

from celer_sight_ai import config

if config.is_executable:
    sys.path.append(str(os.environ["CELER_SIGHT_AI_HOME"]))
import logging

from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtCore import Qt, pyqtSlot

from celer_sight_ai import config
from celer_sight_ai.gui.designer_widgets_py_files.NewMenu2 import (
    Ui_Dialog as NewMenuForm,
)

logger = logging.getLogger(__name__)


class AnalysisWidget(QtWidgets.QDialog):
    def __init__(self):
        super(AnalysisWidget, self).__init__()
        pass


from celer_sight_ai.gui.designer_widgets_py_files.ExitSaveDialog import (
    Ui_Dialog as exitSaveDialog_UI,
)


class exitSaveDialog(exitSaveDialog_UI):
    def __init__(self, MainWindow=None) -> None:
        self.MainWindow: any | None = MainWindow
        self.myDialog = QtWidgets.QDialog()
        self.setupUi(Dialog=self.myDialog)
        # self.myDialog.setParent(MainWindow)
        self.pushButton.clicked.connect(slot=lambda: self.toSave())
        self.pushButton_2.clicked.connect(slot=lambda: self.closeEverything())
        self.pushButton_3.clicked.connect(slot=lambda: self.cancelClose())
        self.myDialog.show()

    def closeEverything(self) -> None:
        self.MainWindow.MainWindow.close()
        self.myDialog.close()

    def cancelClose(self) -> None:
        self.myDialog.close()

    def toSave(self) -> None:
        """
        runs the saves as action
        """
        self.MainWindow.save_celer_sight_file(
            plab_object=self.MainWindow.DH.plab_object_user
        )


from celer_sight_ai.gui.designer_widgets_py_files.OrganismSelectrionDiaolog import (
    Ui_DialogMainSelection as OrgSelDialog,
)


class organismSelectionClass(OrgSelDialog):
    def __init__(self, MainWindow=None):

        logger.debug(msg="Initializing organismSelectionClass")
        self.MainWindow = MainWindow

        self.myDialog = QtWidgets.QDialog()
        self.setupUi(DialogMainSelection=self.myDialog)
        self.ShadowEffect = QtWidgets.QGraphicsDropShadowEffect()
        self.ShadowEffect.setColor(QtGui.QColor(0, 0, 0, 250))
        self.ShadowEffect.setBlurRadius(70)
        self.ShadowEffect.setOffset(0)
        from celer_sight_ai import config

        # add layout
        self.scroll_area_layout = QtWidgets.QHBoxLayout(self.scrollArea)
        self.scroll_area_layout.setContentsMargins(0, 0, 0, 0)
        self.scroll_area_layout.setSpacing(0)
        self.scrollAreaWidgetContents.setLayout(self.scroll_area_layout)

        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setVerticalScrollBarPolicy(
            QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )
        self.scrollArea.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarPolicy.ScrollBarAsNeeded
        )

        BUTTON_WIDTH = 380
        BUTTON_HEIGHT = 700
        # add organism buttons
        self.CelegansMainButton = QtWidgets.QPushButton(self.scrollArea)
        self.CelegansMainButton.setObjectName("CelegansMainButton")
        self.CelegansMainButton.setCheckable(True)
        self.CelegansMainButton.setAutoExclusive(True)
        self.CelegansMainButton.setMinimumSize(
            QtCore.QSize(BUTTON_WIDTH, BUTTON_HEIGHT)
        )
        self.CelegansMainButton.setMaximumSize(
            QtCore.QSize(BUTTON_WIDTH, BUTTON_HEIGHT)
        )
        self.CelegansMainButton.setIconSize(QtCore.QSize(BUTTON_WIDTH, BUTTON_HEIGHT))
        self.CellsMainButton = QtWidgets.QPushButton(self.scrollArea)
        self.CellsMainButton.setObjectName("CellsMainButton")
        self.CellsMainButton.setCheckable(True)
        self.CellsMainButton.setAutoExclusive(True)
        self.CellsMainButton.setMinimumSize(QtCore.QSize(BUTTON_WIDTH, BUTTON_HEIGHT))
        self.CellsMainButton.setMaximumSize(QtCore.QSize(BUTTON_WIDTH, BUTTON_HEIGHT))
        self.CellsMainButton.setIconSize(QtCore.QSize(BUTTON_WIDTH, BUTTON_HEIGHT))

        self.TissueMainButton = QtWidgets.QPushButton(self.scrollArea)
        self.TissueMainButton.setObjectName("TissueMainButton")
        self.TissueMainButton.setCheckable(True)
        self.TissueMainButton.setAutoExclusive(True)
        self.TissueMainButton.setMinimumSize(QtCore.QSize(BUTTON_WIDTH, BUTTON_HEIGHT))
        self.TissueMainButton.setMaximumSize(QtCore.QSize(BUTTON_WIDTH, BUTTON_HEIGHT))
        self.TissueMainButton.setIconSize(QtCore.QSize(BUTTON_WIDTH, BUTTON_HEIGHT))

        self.on_plate_superclass_button = QtWidgets.QPushButton(self.scrollArea)
        self.on_plate_superclass_button.setObjectName("on_plate_superclass_button")
        self.on_plate_superclass_button.setCheckable(True)
        self.on_plate_superclass_button.setAutoExclusive(True)
        self.on_plate_superclass_button.setMinimumSize(
            QtCore.QSize(BUTTON_WIDTH, BUTTON_HEIGHT)
        )
        self.on_plate_superclass_button.setMaximumSize(
            QtCore.QSize(BUTTON_WIDTH, BUTTON_HEIGHT)
        )
        self.on_plate_superclass_button.setIconSize(
            QtCore.QSize(BUTTON_WIDTH, BUTTON_HEIGHT)
        )

        all_buttons = [
            self.CelegansMainButton,
            self.on_plate_superclass_button,
            self.CellsMainButton,
            self.TissueMainButton,
        ]

        # self.scrollArea.setMinimumWidth(int(len(all_buttons) * (BUTTON_WIDTH)))

        for b in all_buttons:
            self.scroll_area_layout.addWidget(b)

        # Helper function to set up button images
        def setup_button_images(button, off_image, on_image):
            # make sure tha path exists
            # Create icons for normal and hover states
            normal_icon = QtGui.QIcon(
                os.path.join(
                    os.environ["CELER_SIGHT_AI_HOME"], "data/icons/", off_image
                )
            )
            hover_icon = QtGui.QIcon(
                os.path.join(os.environ["CELER_SIGHT_AI_HOME"], "data/icons/", on_image)
            )

            # Set the normal icon
            button.setIcon(normal_icon)
            button.setIconSize(QtCore.QSize(BUTTON_WIDTH, BUTTON_HEIGHT))

            # Apply minimal styling
            button.setStyleSheet(
                """
                QPushButton {
                    background-color: transparent;
                    border: none;
                }
                QPushButton:hover {
                    background-color: transparent;
                    border: none;
                }
            """
            )

            # Install event filter to handle hover state
            class ButtonHoverFilter(QtCore.QObject):
                def eventFilter(self, obj, event):
                    if event.type() == QtCore.QEvent.Type.Enter:
                        obj.setIcon(hover_icon)
                    elif event.type() == QtCore.QEvent.Type.Leave:
                        obj.setIcon(normal_icon)
                    return False

            hover_filter = ButtonHoverFilter(button)
            button.installEventFilter(hover_filter)
            # Store filter as attribute to prevent garbage collection
            button._hover_filter = hover_filter

        # Set up each button
        setup_button_images(
            self.CelegansMainButton, "selegans_off.png", "selegans_on.png"
        )

        setup_button_images(self.TissueMainButton, "tissue_off.jpg", "tissue_on.jpg")

        setup_button_images(self.CellsMainButton, "cells_off.png", "cells_on.png")

        setup_button_images(
            self.on_plate_superclass_button,
            "on_plate_off.jpg",
            "on_plate_on.jpg",
        )

        if config.user_cfg.ALLOW_ELEGANS is False:
            self.CelegansMainButton.setEnabled(False)
        if config.user_cfg.ALLOW_TISSUE is False:
            self.TissueMainButton.setEnabled(False)
        if config.user_cfg.ALLOW_CELLS is False:
            self.CellsMainButton.setEnabled(False)
        if config.user_cfg.ALLOW_ON_PLATE is False:
            self.on_plate_superclass_button.hide()

        self.CelegansMainButton.clicked.connect(lambda: self.CreateProject("worm"))
        self.CellsMainButton.clicked.connect(lambda: self.CreateProject("cell"))
        self.TissueMainButton.clicked.connect(lambda: self.CreateProject("tissue"))
        self.on_plate_superclass_button.clicked.connect(
            lambda: self.CreateProject("on_plate")
        )

        self.mainframe.setStyleSheet(
            """
            background-color: rgb(15,15,15);
            """
        )

        # from celer_sight_ai.gui.Utilities.tutorialStuff import organismSelectionTutorial
        # self.myTutorialUi = organismSelectionTutorial(self)

    def CreateProject(self, projectType="worm"):
        from celer_sight_ai import config

        self.MainWindow.stackedWidget.setCurrentWidget(
            self.MainWindow.AnalsysisSettingsSection
        )
        self.MainWindow.current_home_display_widget = self.MainWindow.chat
        self.analysisObject = self.MainWindow.new_analysis_object
        self.MainWindow.allButtons = []
        self.Spacer1Pos = None
        self.Spacer2Pos = None
        self.Spacer1Pos = (1, 4, 2, 2)
        self.Spacer2Pos = (4, 1, 2, 2)
        self.MainWindow.stackedWidget.setCurrentWidget(
            self.MainWindow.AnalsysisSettingsSection
        )
        self.MainWindow.HomeButtonMain.click()
        self.MainWindow.ExecNewFile(projectType)


class NewAnalysis(NewMenuForm):
    global mysignals

    def __init__(self, MainWindow=None, hint="worm"):  # hint can be cel cell and tissue
        #
        # Set First variables
        #
        self.MainWindow = MainWindow

        self.init_organism_settings()
        QtWidgets.QApplication.processEvents()

        import pathlib

        CDIR = str(pathlib.Path(__file__).parent.absolute())
        # self.MainWindow.MainWindow.show()

    def set_organism(self, type_of_entity="worm"):
        logger.info(f"Setting organism to {type_of_entity}")
        config.supercategory = type_of_entity
        self.updateSettings()

    def getorganism(self):
        return self.organism

    def init_organism_settings(self):
        # The following piece of code has been deprecated
        from celer_sight_ai import config

        # organism code
        self.organism = config.supercategory

        self.area_map = {
            "body": 0,
            "head": 1,
            "embryo": 2,
            "intestine": 3,
            "muscle": 4,
            "seam": 5,
            "cellGeneric_CYTO": 6,
            "scratch": 7,
            "tissueGeneric": 8,
            "peumothorax_bbox": 9,
            "abnormaly_classification": 10,
            "cellGeneric_NUCLEUS": 11,
            "flies_adult_body": 12,
            "generic": 13,
        }

        # self.class_map = {
        #     # "worm_elegans_body": {"body": ["particles"]},
        #     "worm_elegans_body": ["body"],
        #     "worm_elegans_head": ["head"],
        #     "worm_elegans_embryo": ["embryo"],
        #     "flies_body": ["body"],
        # }

        self.analysis_map = {
            "particles": 0,
            "fragmentation": 1,
            "mean_intensity": 2,
            "colocalization": 3,
        }
        # source channel codes
        self.SourceImageChannels = []
        self.MeasureImageChannels = []
        self.RedChannel = 0
        self.GreenChannel = 1
        self.BlueChannel = 2

        # ui stuff reset

        self.lastSelectedBtn = None
        self.currentInstalledBtns = []

        from celer_sight_ai import config

        if config.user_cfg.ALLOW_COLOC == False:
            self.MainWindow.btn_coloc_analysis.setEnabled(False)
            self.MainWindow.btn_coloc_analysis.hide()
        if config.user_cfg.ALLOW_PARTICLES == False:
            self.MainWindow.btn_particle_analysis.setEnabled(False)
            self.MainWindow.btn_particle_analysis.hide()
        if config.user_cfg.ALLOW_INTENSITY == False:
            self.MainWindow.btn_intensity_analysis.setEnabled(False)
            self.MainWindow.btn_intensity_analysis.hide()

    # def get_organism_complete_text(self):
    #     """
    #     Returns the current expriement organism string. This is usufull for
    #     serverside communication and selecting tools and epexperiements on the server side

    #     The format for this string is {organism class}_{organism name}_{body part}
    #     e.g. "worm_cele_body"
    #     This string is compromized from the short version of words
    #     e.g. "C_elegans" would be "elegans"
    #     """
    #     # get the organismconfig.global_signals.ORGANISM
    #     organism = self.get_organism_text(config.global_params.organism)
    #     if organism == "elegans":
    #         organism_type = "worm"
    #     elif organism == "flies":
    #         organism_type = "flies"
    #     else:
    #         organism_type = "cells"
    #     # get the body part
    #     area = self.get_area_text(config.global_params.area)

    #     return f"{organism_type}_{organism}_{area}"

    def get_entity(self):
        organism = self.get_organism_text(config.global_params.organism)
        if organism == "elegans":
            entity = "worm"
        elif organism == "flies":
            entity = "flies"
        else:
            entity = "cell"

        return entity

    def get_organism_text(self, organism_id: int) -> str:
        """Converts the organism id to the organism text"""
        for k in self.organism_map.keys():
            if self.organism_map[k] == organism_id:
                return k

    def updateSettings(self):
        from celer_sight_ai import config

        cloud_credentials = config.cloud_user_variables
        if cloud_credentials:
            self.MainWindow.User_label_value.setText(cloud_credentials["email"])
        else:  # offline mode
            self.MainWindow.User_label_value.setText("offline")

        self.MainWindow.RegionOfInterest_label_value.setText(self.DisplayNetworkInfo())
        analysis = self.GetAnalysisType()
        anlysisText = ""
        if analysis == self.analysis_map["particles"]:
            anlysisText = "Particles"
        if analysis == self.analysis_map["fragmentation"]:
            anlysisText = "Fragmentation"

        if analysis == self.analysis_map["mean_intensity"]:
            anlysisText = "Intensity"

        if analysis == self.analysis_map["colocalization"]:
            anlysisText = "Colocalization"

        self.MainWindow.Analysis_label_value.setText(anlysisText)
        self.MainWindow.stackedWidget.setCurrentWidget(
            self.MainWindow.AnalsysisSettingsSection
        )

    def ExecNewOrg(self):
        """
        Opens New widnow for new analysis
        """

        self.MainWindow.ExecNewOrg()

    def addShadowToWidget(self, widgetToAddShadow):
        ShadowEffect = QtWidgets.QGraphicsDropShadowEffect()
        ShadowEffect.setColor(QtGui.QColor(0, 0, 0, 200))
        ShadowEffect.setBlurRadius(50)
        ShadowEffect.setOffset(0)
        widgetToAddShadow.setGraphicsEffect(ShadowEffect)
        return widgetToAddShadow

    def makeSureOneIsAlwaysSelected(self, selectedButton):
        logger.info("makeSureOneIsAlwaysSelected runss")
        isAnyChecked = False
        currentChecked = None
        for SomeBtn in self.currentInstalledBtns:
            if SomeBtn.currentShowingSettings == True:
                SomeBtn.startHideAnimationSeq()
            if SomeBtn != self.lastSelectedBtn:
                if SomeBtn.isChecked():
                    isAnyChecked = True

                    # currentChecked = SomeBtn
        if isAnyChecked == False:
            self.lastSelectedBtn.setChecked(True)
        elif selectedButton != self.lastSelectedBtn:
            if self.lastSelectedBtn:
                self.lastSelectedBtn.setChecked(False)
                selectedButton.setChecked(True)
        elif currentChecked:
            self.lastSelectedBtn = currentChecked

    def eventFilter(self, source, event):
        # This is probably for the NN buttons to show  in blur and non blur setting...
        if event.type() == QtCore.QEvent.Type.MouseButtonPress:
            logger.info("release working")
            if event.button() == QtCore.Qt.MouseButton.LeftButton:
                if type(source) != NN_Settings_Popup_Widget:
                    logger.info("not pop up widget")
                    if type(source) == NN_settings_button:
                        logger.info("is not seetings buttons")
                        if source.currentShowingSettings == False:
                            logger.info("source is current hsowing flase")
                            source.startHideAnimationSeq()
                    else:
                        for somebutton in self.currentInstalledBtns:
                            logger.info(
                                "for all buttons we have.. ",
                                somebutton.currentShowingSettings,
                            )
                            if somebutton.currentShowingSettings == True:
                                somebutton.startHideAnimationSeq()

                elif source.currentShowingSettings == False:
                    logger.info("source 2 current shwoign false")
                    for somebutton in self.currentInstalledBtns:
                        logger.info(
                            "for all buttons we have.. ",
                            somebutton.currentShowingSettings,
                        )
                        if somebutton.currentShowingSettings == False:
                            somebutton.startHideAnimationSeq()

        return super(
            type(self.AnalysisWidgetForm), self.AnalysisWidgetForm
        ).eventFilter(source, event)

    def startBlurLayer(self):
        self.myBlurRadius = QtWidgets.QGraphicsBlurEffect()
        self.myBlurRadius.setBlurRadius(0)
        self.myBlurRadius.setBlurHints(
            QtWidgets.QGraphicsBlurEffect.AnimationHint
            | QtWidgets.QGraphicsBlurEffect.QualityHint
        )
        self.BlurFrame.setGraphicsEffect(self.myBlurRadius)
        self.blurAnim = QtCore.QPropertyAnimation(self.myBlurRadius, b"blurRadius")
        self.blurAnim.setDuration(50)
        self.blurAnim.setStartValue(1)
        self.blurAnim.setEndValue(50)
        self.blurAnim.setEasingCurve(
            QtCore.QEasingCurve(QtCore.QEasingCurve.Type.Linear)
        )
        self.blurAnim.start()

    def revertBlurLayer(self):
        self.myBlurRadius = QtWidgets.QGraphicsBlurEffect()
        self.myBlurRadius.setBlurRadius(0)
        self.BlurFrame.setGraphicsEffect(self.myBlurRadius)
        self.blurAnim = QtCore.QPropertyAnimation(self.myBlurRadius, b"blurRadius")
        self.blurAnim.setDuration(50)
        self.blurAnim.setStartValue(49)
        self.blurAnim.setEndValue(1)
        self.blurAnim.setEasingCurve(
            QtCore.QEasingCurve(QtCore.QEasingCurve.Type.Linear)
        )
        self.blurAnim.start()
        self.blurAnim.finished.connect(lambda: self.onRevertBlurLayer_finished())

    def onRevertBlurLayer_finished(self):
        self.BlurFrame.setGraphicsEffect(None)

    def setParametersForArea(self, mytype="particles"):
        if mytype == "particles":
            self.MainWindow.btn_particle_analysis.setEnabled(True)
            self.MainWindow.btn_particle_analysis.click()
            self.MainWindow.viewer.QuickTools.MinRadiusspinBox.setValue(300)
        if mytype is None:
            self.MainWindow.btn_intensity_analysis.setEnabled(True)
            self.MainWindow.btn_particle_analysis.setEnabled(True)
            self.MainWindow.btn_coloc_analysis.setEnabled(True)

    def RatioFrameExposureCheck(self):
        """
        Runs every time we change a channel and in the begging
        """
        amountPressed = 0
        if not self.BBtn2.isChecked():
            amountPressed += 1
        if not self.RBtn2.isChecked():
            amountPressed += 1
        if not self.GBtn2.isChecked():
            amountPressed += 1
        logger.info("amount pressed is ", amountPressed)
        if amountPressed >= 2 and self.ComputeRatiosCheckBox.isChecked():
            self.AnalysisDialog_RGB_RatioFrame.show()
        else:
            self.AnalysisDialog_RGB_RatioFrame.hide()

    def DisplayNetworkInfo(self):

        logger.info("init_user_params STARTED")
        return ""

    def init_user_params(self):
        logger.info("Initializing parameters.")
        import celer_sight_ai.configHandle as configHandle
        from celer_sight_ai import config

        organism_in_use = config.supercategory

        logger.info(f"Send settings to server: {organism_in_use}")
        config.global_params.ORGANISM = organism_in_use
        config.user_attributes.username = configHandle.get_stored_username()
        config.user_attributes.password = configHandle.get_stored_password()

    def setPriorSettings(self, organism=None, Area=None, Analysis=None):
        from celer_sight_ai import config

        # logger.info("setPriorSettings are ", organism, Area, Analysis)
        # if Analysis == self.particles:
        #     self.comboBox.setCurrentText("Intensity Analysis")
        # elif Analysis == self.fragmentation:
        #     self.comboBox.setCurrentText("Fragmentation Analysis")
        # elif Analysis == self.MeanIntensity:
        #     self.comboBox.setCurrentText("Aggregates Analysis")
        # elif Analysis == self.colocalization:
        #     self.comboBox.setCurrentText("Colocalization")

    def GetSourceChannels(self):
        return [1]

    def GetMeasuredChannels(self):
        return [1]

    def apply_uuid_to_all_nodes(self, nodes):
        # nodes is a list of dictionaries
        # this is recursive method
        for node in nodes:
            if not node.get("uuid"):
                node["uuid"] = config.get_unique_id()
            if node.get("children_classes"):
                self.apply_uuid_to_all_nodes(node.get("children_classes"))

    def transverse_classes(self, class_nodes, parent_uuid=None):
        # reads all class items and adds the class to the interface
        import copy

        # add classes from the root node, recursively
        for node in class_nodes:
            if parent_uuid == None and (
                node.get("parent_class") or node.get("parent_class_uuid")
            ):
                if node.get("parent_class"):
                    #     parent_uuid = self.MainWindow.custom_class_list_widget.get_class_widget_by_class_uuid(node.get("parent_class_uuid"))
                    # else:
                    parent_uuid = self.MainWindow.custom_class_list_widget.get_class_widget_by_class_name(
                        node["parent_class"]
                    )
                # make sure its included in the parent class
                if parent_uuid:
                    p_class_obj = self.MainWindow.custom_class_list_widget.classes[
                        parent_uuid
                    ]
                    if isinstance(p_class_obj.children_class_uuids, type(None)):
                        p_class_obj.children_classes_uuids = [node["uuid"]]
                    else:
                        if node["uuid"] not in p_class_obj.children_class_uuids:
                            p_class_obj.children_class_uuids.append(node["uuid"])
            children_classes = node.get("children_classes")
            if children_classes:
                children_classes = [i.get("uuid") for i in children_classes]
            self.MainWindow.addClassItem(
                str(node["class_name"]),
                parent_uuid=parent_uuid,
                class_uuid=str(node["uuid"]),
                is_user_defined=False,
                is_particle=node.get("is_particle"),
                children_classes_uuids=children_classes,
                parent_class_name=node.get("parent_class"),
            )

            if node.get("children_classes"):
                self.transverse_classes(
                    copy.deepcopy(node.get("children_classes")),
                    parent_uuid=str(node["uuid"]),
                )

    def scan_class_items(self, current_nodes, parent_uuid=None):
        # add class
        # get first class

        # get the furthest child in every branch
        self.apply_uuid_to_all_nodes(current_nodes)
        # now we have a node without children
        # add nodes depth first
        self.transverse_classes(current_nodes)

        self.MainWindow.custom_class_list_widget.ensure_class_list_widget_is_right_hierarchy()

    def Record_To_GlobalVars(self):
        """
        Gathers all of the variables and applies them to the instance we are working with
        """
        from celer_sight_ai import config

        config.global_params.analysis = self.GetAnalysisType()

        logger.info(f"record to global isntance organism is {self.organism}")

        logger.info("Record_To_GlobalVars")

        # get all items in the config file specified
        cfgs = config.experiment_config

        for cfg in cfgs:
            # if class items length is 1 and particle or colocalization analysis, add particles as a child to the main class
            if (
                len(cfg["classes"]) == 1
                and not cfg.get("children_classes")
                and self.GetAnalysisType()
                in [
                    self.analysis_map["particles"],
                    self.analysis_map["colocalization"],
                ]
            ):
                cfg["classes"][0]["children_classes"] = [
                    {"class_name": "particles", "is_particle": True}
                ]

            # if there any items in the ```custom_class_list_widget``` groupbox,remove them, start clean!
            for item in range(self.MainWindow.custom_class_list_widget.count()):
                lwidget_item = self.MainWindow.custom_class_list_widget.item(item)
                self.MainWindow.custom_class_list_widget.removeItemWidget(lwidget_item)

            # process events
            QtCore.QCoreApplication.processEvents()

            if config.SHOW_CLASSES:
                self.MainWindow.pg1_settings_groupBox_classes.show()
                # populate classes
            self.scan_class_items(cfg["classes"])
        # Always select the first element
        self.MainWindow.custom_class_list_widget.setCurrentRow(0)

        # spawn initial dialog
        from celer_sight_ai.gui.custom_widgets.particle_analysis_ui import (
            ParticleAnalysisSettingsWidgetUi,
        )

        self.MainWindow.viewer.particle_analysis_settings_widget = (
            ParticleAnalysisSettingsWidgetUi(self.MainWindow.Images, self.MainWindow)
        )
        self.MainWindow.viewer._is_particle_ui_spawned = True

        return

    def checkKeyOrZero(self, dictObj, key):
        # checks dictioanry if no key returns zero
        if key in dictObj.keys():
            return dictObj[key]
        else:
            return 0

    def GetAnalysisType(self):
        """
        Returns the selected Type of Analy sis
        """
        # Analysis = self.comboBox.currentText()
        if self.MainWindow.btn_intensity_analysis.isChecked():
            return self.analysis_map["mean_intensity"]
        # elif self.btn_intensity_analysis.isChecked():
        #     return self.fragmentation
        elif self.MainWindow.btn_particle_analysis.isChecked():
            return self.analysis_map["particles"]
        elif self.MainWindow.btn_coloc_analysis.isChecked():
            return self.analysis_map["colocalization"]


from celer_sight_ai.gui.designer_widgets_py_files.NN_settings_hover import (
    Ui_Form as NN_settings_hover_form,
)


class NN_settings_button(QtWidgets.QPushButton):
    def __init__(self, parent=None, MainWindow=None):
        super().__init__(parent)


class NN_Settings_Popup_Widget(NN_settings_hover_form):
    def __init__(self, myParent, MainWindow):
        self.widgetAttached = myParent
        self.myWidget = QtWidgets.QWidget()
        self.setupUi(self.myWidget)
        self.MainWindow = MainWindow
        self.myParent = (
            MainWindow.frame_2
        )  # myParent.myParent.frame #AnalysisWidgetForm
        self.myWidget.setParent(self.myParent)
        self.myWidget.move(self.getParentPos())
        self.myWidget.hide()
        self.myWidget.raise_()
        self.amIDetached = False
        # animation settings:
        self.show_anim_duration = 200
        self.show_anim_geom_curve = QtCore.QEasingCurve(
            QtCore.QEasingCurve.Type.OutBack
        )
        self.show_anim_opacity_curve = QtCore.QEasingCurve(
            QtCore.QEasingCurve.Type.Linear
        )
        self.myXOffset = -285
        self.myXOffsetStarting = 20
        self.myYOffsetStarting = 20

        self.hasSetWidgetParentPos = False

        self.hide_anim_duration = 200
        self.hide_anim_geom_curve = QtCore.QEasingCurve(
            QtCore.QEasingCurve.Type.OutBack
        )
        self.hide_anim_opacity_curve = QtCore.QEasingCurve(
            QtCore.QEasingCurve.Type.OutBack
        )
        curve = QtCore.QEasingCurve(QtCore.QEasingCurve.Type.Linear)

        self.myShadow = QtWidgets.QGraphicsDropShadowEffect(
            blurRadius=30, xOffset=3, yOffset=3, color=QtGui.QColor(0, 0, 0, 200)
        )

        self.myWidget.setGraphicsEffect(self.myShadow)
        self.myParentWidgetPos = self.widgetAttached.pos()

    def getParentPos(self):
        parentPos = self.myParent.mapTo(
            self.widgetAttached.MainWindow.frame_2, self.widgetAttached.pos()
        )
        return parentPos

    def startShowAnimation(self):
        # self.widgetAttached.MainWindow.blurPlaceHolder.setGeometry(self.widgetAttached.MainWindow.frame.geometry())
        # self.widgetAttached.MainWindow.blurPlaceHolder.show()
        from celer_sight_ai import config

        # self.myBlurRadius =QtWidgets.QGraphicsBlurEffect()
        # self.myBlurRadius.setBlurRadius(0)
        # self.widgetAttached.MainWindow.BlurFrame.setGraphicsEffect(self.myBlurRadius )
        config.global_signals.blurAnimation_NewMenuSignal_ON.emit()
        self.myWidget.show()
        if self.hasSetWidgetParentPos == False:
            self.myParentWidgetPos = self.widgetAttached.pos()
            self.hasSetWidgetParentPos = True
        startingPos = self.myParentWidgetPos
        logger.info(
            "startingPos ", self.myParentWidgetPos.x(), self.myParentWidgetPos.y()
        )
        self.ParAnimation_SHOW = QtCore.QParallelAnimationGroup()
        self.animminimumSize = QtCore.QPropertyAnimation(self.myWidget, b"geometry")
        self.animminimumSize.setDuration(self.show_anim_duration)
        self.animminimumSize.setStartValue(
            QtCore.QRect(
                startingPos.x() + self.myXOffsetStarting,
                startingPos.y() + self.myYOffsetStarting,
                250,
                350,
            )
        )
        self.animminimumSize.setEndValue(
            QtCore.QRect(
                startingPos.x() + self.myXOffsetStarting + self.myXOffset,
                startingPos.y() + self.myYOffsetStarting,
                250,
                350,
            )
        )
        self.animminimumSize.setEasingCurve(self.show_anim_geom_curve)
        logger.info("startingPos ", startingPos.x(), startingPos.y())
        self.ParAnimation_SHOW = QtCore.QParallelAnimationGroup()
        # self.blurAnim = QtCore.QPropertyAnimation(self.myBlurRadius, b"blurRadius ")
        # self.blurAnim.setDuration(self.show_anim_duration)
        # self.blurAnim.setStartValue(0)
        # self.blurAnim.setEndValue(10)
        # self.blurAnim.setEasingCurve(self.show_anim_opacity_curve)
        self.ParAnimation_SHOW.addAnimation(self.animminimumSize)
        self.myWidget.show()
        self.ParAnimation_SHOW.finished.connect(lambda: self.OnParAnimFinish_SHOW())

        self.ParAnimation_SHOW.start()
        logger.info("showing now!")

    def startHideAnimation(self):
        from celer_sight_ai import config

        config.global_signals.blurAnimation_NewMenuSignal_OFF.emit()
        QtWidgets.QApplication.processEvents()
        if self.hasSetWidgetParentPos == False:
            self.myParentWidgetPos = self.widgetAttached.pos()
            self.hasSetWidgetParentPos = True

        startingPos = self.myParentWidgetPos
        self.ParAnimation_HIDE = QtCore.QParallelAnimationGroup()
        animminimumSizeHIDE = QtCore.QPropertyAnimation(self.myWidget, b"geometry")
        animminimumSizeHIDE.setDuration(self.hide_anim_duration)
        start = self.widgetAttached.minimumSize()
        animminimumSizeHIDE.setStartValue(
            QtCore.QRect(
                startingPos.x() + self.myXOffsetStarting + self.myXOffset,
                startingPos.y() + self.myYOffsetStarting,
                250,
                350,
            )
        )
        animminimumSizeHIDE.setEndValue(
            QtCore.QRect(
                startingPos.x() + self.myXOffsetStarting,
                startingPos.y() + self.myYOffsetStarting,
                250,
                350,
            )
        )
        animminimumSizeHIDE.setEasingCurve(self.hide_anim_geom_curve)
        self.ParAnimation_HIDE.addAnimation(animminimumSizeHIDE)
        self.ParAnimation_HIDE.finished.connect(lambda: self.OnParAnimFinish_HIDE())
        self.ParAnimation_HIDE.start()
        self.runningShowAnim = False
        logger.info("hiding now!")

    def OnParAnimFinish_SHOW(self):
        # self.effectOP.setOpacity(1)
        self.myWidget.show()
        self.myWidget.setGraphicsEffect(None)
        self.widgetAttached.runningShowAnim = False

    def OnParAnimFinish_HIDE(self):
        self.myWidget.setGraphicsEffect(None)
        self.myWidget.hide()

        self.widgetAttached.installWidgetToParent()
        self.widgetAttached.runningShowAnim = False

    def setupAnimations(self):
        pass


if __name__ == "__main__":
    import sys

    from PyQt6.QtWidgets import QApplication

    app = QApplication(sys.argv)

    # Create an instance of organismSelectionClass
    organism_selection = organismSelectionClass()

    # Show the dialog
    organism_selection.myDialog.show()

    sys.exit(app.exec())
