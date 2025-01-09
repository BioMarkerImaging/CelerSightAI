##########################################################################
##########################################################################
####################                                  ####################
####################    DIALOG SECOND WINDOW          ####################
####################                                  ####################
##########################################################################
##########################################################################

from PyQt6 import QtCore, QtGui, QtWidgets
import cv2
from celer_sight_ai.core.Workers import Worker, WorkerSignals
from celer_sight_ai.gui.custom_widgets.ProgressD import Ui_Progress_dialog
import numpy as np
from celer_sight_ai import config
from celer_sight_ai.io.image_reader import channel_to_color
import logging

logger = logging.getLogger(__name__)
# import CelerSightModules # TODO: implement lost functions
from celer_sight_ai.gui.designer_widgets_py_files.AnalysisDialogUI import Ui_Dialog


def add(a, b):
    # Convert lists or pandas Series to numpy arrays
    import pandas as pd

    if isinstance(a, (list, pd.Series)):
        a = np.array(a, dtype=np.float32)
    if isinstance(b, (list, pd.Series)):
        b = np.array(b, dtype=np.float32)
    try:
        if isinstance(a, np.ndarray) or isinstance(b, np.ndarray):
            result = np.round(a.astype(np.float32) + b.astype(np.float32), 3)
        else:
            result = np.round(float(a) + float(b), 3)
    except Exception as e:
        print(e)
        result = np.nan
    if isinstance(result, np.ndarray):
        result = result.tolist()
    if isinstance(result, tuple) and len(result) == 1:
        result = result[0]
    return result


def subtract(a, b):
    # Convert lists or pandas Series to numpy arrays
    import pandas as pd

    if isinstance(a, (list, pd.Series)):
        a = np.array(a, dtype=np.float32)
    if isinstance(b, (list, pd.Series)):
        b = np.array(b, dtype=np.float32)
    try:
        if isinstance(a, np.ndarray) or isinstance(b, np.ndarray):
            result = np.round(a.astype(np.float32) - b.astype(np.float32), 3)
        else:
            result = np.round(float(a) - float(b), 3)
    except Exception as e:
        print(e)
        result = np.nan
    if isinstance(result, np.ndarray):
        result = result.tolist()
    if isinstance(result, tuple) and len(result) == 1:
        result = result[0]
    return result


def divide(a, b):
    # Convert lists or pandas Series to numpy arrays
    import pandas as pd

    if isinstance(a, (list, pd.Series)):
        a = np.array(a, dtype=np.float32)
    if isinstance(b, (list, pd.Series)):
        b = np.array(b, dtype=np.float32)
    if not isinstance(b, np.ndarray) and b == 0:
        result = float("inf")
    else:
        try:
            if isinstance(a, np.ndarray) or isinstance(b, np.ndarray):
                result = np.round(a.astype(np.float32) / b.astype(np.float32), 3)
            else:
                result = np.round(float(a) / float(b), 3)
        except Exception as e:
            print(e)
            result = np.nan
    if isinstance(result, np.ndarray):
        result = result.tolist()
    if isinstance(result, tuple) and len(result) == 1:
        result = result[0]
    return result


def multiply(a, b):
    # Convert lists or pandas Series to numpy arrays
    import pandas as pd

    if isinstance(a, (list, pd.Series)):
        a = np.array(a, dtype=np.float32)
    if isinstance(b, (list, pd.Series)):
        b = np.array(b, dtype=np.float32)
    try:
        if isinstance(a, np.ndarray) or isinstance(b, np.ndarray):
            result = np.round(a.astype(np.float32) * b.astype(np.float32), 3)
        else:
            result = np.round(float(a) * float(b), 3)
    except Exception as e:
        print(e)
        result = np.nan
    if isinstance(result, np.ndarray):
        result = result.tolist()
    if isinstance(result, tuple) and len(result) == 1:
        result = result[0]
    return result


# Supported Operations for Channels
SUPPORTED_CHANNEL_OPERATIONS = {
    "plus": add,
    "minus": subtract,
    "over": divide,
    "times": multiply,
}

# Supported Operations for ROIs
SUPPORTED_ROI_OPERATIONS = {
    # "plus": add,
    # "minus": subtract,
    "over": divide,
    "times": multiply,
}


class AnalysisDialogWidget(QtWidgets.QDialog):
    def __init__(self):
        super(AnalysisDialogWidget, self).__init__()


class HTMLViewer(QtWidgets.QWidget):  # viewe is used to display html grapher pygwalker
    def __init__(self, html_content):
        super().__init__()
        from PyQt6 import QtWebEngineWidgets
        import tempfile

        layout = QtWidgets.QVBoxLayout(self)
        self.web_engine_view = QtWebEngineWidgets.QWebEngineView(self)
        self.web_engine_view.setHtml(html_content)
        self.web_engine_view.settings().setAttribute(
            QtWebEngineWidgets.QtWebEngineCore.QWebEngineSettings.WebAttribute.WebGLEnabled,
            True,
        )
        self.web_engine_view.settings().setAttribute(
            QtWebEngineWidgets.QtWebEngineCore.QWebEngineSettings.WebAttribute.Accelerated2dCanvasEnabled,
            True,
        )
        self.web_engine_view.settings().setAttribute(
            QtWebEngineWidgets.QtWebEngineCore.QWebEngineSettings.WebAttribute.LocalContentCanAccessRemoteUrls,
            True,
        )
        # Save the HTML content to a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".html") as f:
            f.write(html_content.encode("utf-8"))
            self.temp_file_path = f.name
        # Load the temporary file in the QWebEngineView
        self.web_engine_view.load(QtCore.QUrl.fromLocalFile(self.temp_file_path))
        layout.addWidget(self.web_engine_view)
        self.web_engine_view.loadFinished.connect(self.on_load_finished)
        layout.addWidget(self.web_engine_view)
        self.show()
        self.web_engine_view.show()

    def on_load_finished(self, ok):
        print("load finished", ok)


class HtmlDelegate(QtWidgets.QStyledItemDelegate):
    def paint(self, painter, options, index):
        # options = QtWidgets.QStyleOptionViewItem()
        self.initStyleOption(options, index)

        text = options.text
        options.text = ""
        style = (
            QtWidgets.QApplication.style()
            if options.styleObject is None
            else options.styleObject
        )
        style.drawControl(
            QtWidgets.QStyle.ControlElement.CE_ItemViewItem, options, painter
        )

        doc = QtGui.QTextDocument()
        font = QtGui.QFont()
        font.setFamily(".AI Bayan PUA")
        font.setPointSize(9)
        doc.setHtml(text)
        doc.setDefaultFont(font)

        ctx = QtGui.QAbstractTextDocumentLayout.PaintContext()

        textRect = style.subElementRect(
            QtWidgets.QStyle.SubElement.SE_ItemViewItemText, options, None
        )
        painter.save()
        painter.translate(textRect.topLeft())
        painter.setClipRect(textRect.translated(-textRect.topLeft()))
        doc.documentLayout().draw(painter, ctx)

        painter.restore()

    def sizeHint(self, options, index):
        # options = QtWidgets.QStyleOptionViewItem()
        self.initStyleOption(options, index)
        doc = QtGui.QTextDocument()
        doc.setHtml(options.text)
        doc.setTextWidth(options.rect.width())
        return QtCore.QSize(int(doc.idealWidth()), 15)


class Ui_AnalysisDialog(QtWidgets.QDialog):
    # signal_dialog = QtCore.pyqtSignal()
    def __init__(self, MainWindow=None):
        super(Ui_AnalysisDialog, self).__init__()
        # Ui_Dialog.finished_analysis = self.signal_dialog
        # TODO: put this somewhere else
        self.MainWindow = MainWindow
        self.during_analysis = False  # true when there is an analysis in progress
        config.global_signals.start_analysis_signal.connect(self.start_analysis)

        self.MainWindow.channel_analysis_metrics_combobox.setEditable(True)
        self.MainWindow.channel_analysis_metrics_combobox.setLineEdit(
            QtWidgets.QLineEdit(self.MainWindow.channel_analysis_metrics_combobox)
        )
        self.MainWindow.channel_analysis_metrics_combobox.lineEdit().setReadOnly(True)
        self.MainWindow.channel_analysis_metrics_combobox.lineEdit().hide()
        if not hasattr(self.MainWindow, "channel_analysis_metrics_combobox_label"):
            self.MainWindow.channel_analysis_metrics_combobox_label = QtWidgets.QLabel(
                self.MainWindow.channel_analysis_metrics_combobox
            )
        font = QtGui.QFont()
        font.setFamily(".AI Buyan PUA")
        font.setPointSize(9)
        self.MainWindow.channel_analysis_metrics_combobox_label.setFont(font)
        self.MainWindow.channel_analysis_metrics_combobox.currentIndexChanged.connect(
            self.update_channel_combobox_label
        )
        c_delegate = HtmlDelegate(self.MainWindow.channel_analysis_metrics_combobox)

        self.MainWindow.channel_analysis_metrics_combobox.setItemDelegate(c_delegate)

        self.channelToMeasureList = [1]
        self.channelToMeasureList_2 = [0]

        self.analysis_channels_named = {}
        self.analysis_roi_named = {}

        self.currentActiveChannel = 1
        self.prevActiveChannel = 1

        AnalObject = self.MainWindow.new_analysis_object

        self.computeRatios = False

        ## Bustract Background signals for slot and spinbox:
        #### Slider to Spinbox
        self.MainWindow.submitted.connect(lambda: self.main_process())

        config.global_signals.complete_analysis_signal.connect(self.complete_analysis)

        self.main_process()

    def reset_state(self):
        self.MainWindow.channel_analysis_metrics_combobox.clear()
        self.MainWindow.channel_analysis_metrics_combobox_label.clear()
        self.MainWindow.channel_analysis_metrics_combobox_label.hide()
        self.MainWindow.channel_analysis_metrics_combobox.lineEdit().hide()
        self.MainWindow.channel_analysis_metrics_combobox.lineEdit().clear()
        self.MainWindow.channel_analysis_metrics_combobox.clearEditText()
        if hasattr(self, "ROI_analysis_metrics_combobox"):
            self.ROI_analysis_metrics_combobox.clear()
        if hasattr(self, "Results_pg2_AnalysisTypeComboBox"):
            self.Results_pg2_AnalysisTypeComboBox.clear()
        self.analysis_channels_named = {}
        self.analysis_roi_named = {}
        if hasattr(self, "all_condition_analysis_table"):
            self.all_condition_analysis_table.setModelCustom()
        self.during_analysis = False

    def update_channel_combobox_label(self, indx):
        self.MainWindow.channel_analysis_metrics_combobox_label.setFixedWidth(
            self.MainWindow.channel_analysis_metrics_combobox.width()
        )
        self.MainWindow.channel_analysis_metrics_combobox_label.setFixedHeight(
            self.MainWindow.channel_analysis_metrics_combobox.height()
        )
        self.MainWindow.channel_analysis_metrics_combobox_label.setContentsMargins(
            10, 0, 0, 0
        )
        text = self.MainWindow.channel_analysis_metrics_combobox.itemText(indx)
        self.MainWindow.channel_analysis_metrics_combobox_label.setText(text)

    def assignComputeRatioState(self):
        if self.computeRatiosCheckBox.isChecked():
            self.MyAnalysisDialogWidget.setFixedHeight(
                self.MyAnalysisDialogWidget.height() + 50
            )
            self.computeRatios = True
            # self.parameters_label_channel_2.show()
            # self.AnalysisDialog_red_channel_button_visual_ch2.show()
            # self.AnalysisDialog_green_channel_button_visual_ch2.show()
            self.AnalysisDialog__blue_channel_button_visual_colocalization_ch2.show()
        else:
            self.MyAnalysisDialogWidget.setFixedHeight(
                self.MyAnalysisDialogWidget.height() - 50
            )

            self.computeRatios = False
            # self.parameters_label_channel_2.hide()
            # self.AnalysisDialog_red_channel_button_visual_ch2.hide()
            # self.AnalysisDialog_green_channel_button_visual_ch2.hide()
            self.AnalysisDialog__blue_channel_button_visual_colocalization_ch2.hide()

    def setAutoExclusive(self, button):
        return

    def setAutoExclusive_2(self, button):
        return

    def initColocChannels(self):
        return

    def initColocChannels_2(self):
        return

    def checkColocStateMultipleAnalysis(self):
        if self.ColocMultipleCheckbox.isChecked():
            self.MultipleColocMethodsListWIdget.setEnabled(True)
            self.ComboboxOneMethodColoc.setEnabled(False)
            self.SingleColocMethodLabel.setEnabled(False)
            self.MainWindow.initialize_all_popup(self.MainWindow.current_imagenumber)
        elif not self.ColocMultipleCheckbox.isChecked():
            self.MultipleColocMethodsListWIdget.setEnabled(False)
            self.ComboboxOneMethodColoc.setEnabled(True)
            self.SingleColocMethodLabel.setEnabled(True)

    def SpawnProgressDialog(self):
        """
        This is the new function
        """
        # Animated Bar for progress on importing images to multichannel importer

        exp = ""
        explanation = ""
        # get experiment type
        if (
            config.global_params.analysis
            == self.MainWindow.new_analysis_object.analysis_map["mean_intensity"]
        ):
            exp = "Intensity Analysis"
            explanation = """
            In an intensity analysis the brightness of every pixel value inside the ROIs is measured.
            Here, we measure these values for every group, every treatment and every channel of the image. 
            Then, various metrics are calculated and displayed on the DATA tab. These metrics allow for
            investigation of the mean, std, max and min values as well as arithmetic operation between channels
            and related ROI's (for example, the ratio between the cytoplasm and the nucleus.)
            """

        elif (
            config.global_params.analysis
            == self.MainWindow.new_analysis_object.analysis_map["particles"]
        ):
            exp = "Particle Analysis"
            explanation = """
            During a particle analysis, the particles properties (area , count , etc.. ) are measured. The particle ROI class, denoted 
            by "particles" on the ROIs box is a special ROI class that is used to measure the properties of 
            particles. Here, we measure these values of these particles for every group, every treatment 
            and every channel of the image. Then, various metrics are calculated and displayed on the DATA tab. 
            These particles can be a "child" class to the parent ROI class. In that case, only the particles 
            that are inside the parent ROI will be measured (same as they ones that are displayed). Intensity 
            values (brightness) of these particles are also measured. 
            """
        elif (
            config.global_params.analysis
            == self.MainWindow.new_analysis_object.analysis_map["colocalization"]
        ):
            exp = "Colocalization Analysis"
        else:
            raise ValueError("Experiment type not found")
        config.global_signals.start_progress_bar_signal.emit(
            {
                "title": f"{exp}",
                "window_title": "Analysis in Progress",
                "main_text": f"{exp} : {explanation}",
            }
        )

        QtWidgets.QApplication.processEvents()

    @config.threaded
    def start_analysis(self):
        from celer_sight_ai import config

        self.during_analysis = True
        try:
            # worker calculate analysis and send progress to the progress dialog
            self.SpawnProgressDialog()
            self.update_new_category_thumbnails()
            self.calculate_all_RNAi()
            self.MainWindow.MyVisualPlotHandler.firstNewAnalysis = True
        except Exception as e:
            logger.error("Error in start_analysis", e)
            self.during_analysis = False
            raise e
        self.during_analysis = False

    @config.threaded
    def update_new_category_thumbnails(self) -> None:
        # all of the categories that need to have their thumbnails updated are stored in config.categories_that_need_thumbnail as cfg
        # remove any categories_that_need_thumbnail items that are not in the current analysis
        class_uuids_in_use = list(
            self.MainWindow.custom_class_list_widget.classes.keys()
        )
        while len(config.categories_that_need_thumbnail) > 0:
            category_cfg = config.categories_that_need_thumbnail.pop()
            first_category = category_cfg["classes"][
                0
            ]  # only in experiements cfgs there will be more, this is a feature to be added in the future
            category_uuid = first_category.get("uuid")
            category_name = first_category.get("class_name")
            if not category_uuid in class_uuids_in_use:
                # skip uuid if not in the current experiement
                continue
            # get the best thumbnail for the category
            # find the annotation that its closest to the center of the image
            all_annos = self.MainWindow.DH.BLobj.get_all_annotations_with_category(
                category_uuid
            )
            # get first image
            all_images = self.MainWindow.DH.BLobj.get_all_image_objects()
            if not all_images:
                logger.info("No images found for category thumbnail update")
                continue
            image = all_images[0]
            img_center = (image.SizeX / 2, image.SizeY / 2)
            # iterate over all annotations and find the one closes (eludiand distance) to the center of the image
            closest_anno = None
            closest_dist = None
            for anno in all_annos:
                # if the annotation if polygon, compute the center
                if anno.mask_type == "polygon":
                    arr = anno.get_array()[0]
                    # get the min on x and y and max on x and y
                    minx = np.min(arr[:, 0])
                    miny = np.min(arr[:, 1])
                    maxx = np.max(arr[:, 0])
                    maxy = np.max(arr[:, 1])
                    # centerpoint
                    anno_center = (minx + (maxx - minx) / 2, miny + (maxy - miny) / 2)
                else:
                    continue
                dist = np.linalg.norm(np.array(anno_center) - np.array(img_center))
                if closest_dist is None or dist < closest_dist:
                    closest_dist = dist
                    closest_anno = anno
                    closest_anno_bbox = (minx, miny, maxx, maxy)
            if closest_anno is None:
                # no annotation found
                continue
            # make sure its square
            width = closest_anno_bbox[2] - closest_anno_bbox[0]
            height = closest_anno_bbox[3] - closest_anno_bbox[1]
            closest_anno_bbox = np.array(closest_anno_bbox)
            if width > height:
                diff = width - height
                closest_anno_bbox[1] -= diff / 2
                closest_anno_bbox[3] += diff / 2
            elif height > width:
                diff = height - width
                closest_anno_bbox[0] -= diff / 2
                closest_anno_bbox[2] += diff / 2

            # bounding box needs to be atleast 400 , 400 width x height
            if closest_anno_bbox[2] - closest_anno_bbox[0] < 400:
                diff = 400 - (closest_anno_bbox[2] - closest_anno_bbox[0])
                closest_anno_bbox[0] -= diff / 2
                closest_anno_bbox[2] += diff / 2
            if closest_anno_bbox[3] - closest_anno_bbox[1] < 400:
                diff = 400 - (closest_anno_bbox[3] - closest_anno_bbox[1])
                closest_anno_bbox[1] -= diff / 2
                closest_anno_bbox[3] += diff / 2
            # extend the bbox by 25%
            extend_amount = 0.25
            closest_anno_bbox = (
                max(
                    0,
                    closest_anno_bbox[0]
                    - extend_amount * (closest_anno_bbox[2] - closest_anno_bbox[0]),
                ),
                max(
                    0,
                    closest_anno_bbox[1]
                    - extend_amount * (closest_anno_bbox[3] - closest_anno_bbox[1]),
                ),
                min(
                    image.SizeX,
                    closest_anno_bbox[2]
                    + extend_amount * (closest_anno_bbox[2] - closest_anno_bbox[0]),
                ),
                min(
                    image.SizeY,
                    closest_anno_bbox[3]
                    + extend_amount * (closest_anno_bbox[3] - closest_anno_bbox[1]),
                ),
            )
            # convert bbox to x,y,w,h
            closest_anno_bbox = (
                closest_anno_bbox[0],
                closest_anno_bbox[1],
                closest_anno_bbox[2] - closest_anno_bbox[0],
                closest_anno_bbox[3] - closest_anno_bbox[1],
            )
            image_array = image.getImage(
                to_uint8=True, to_rgb=True, bbox=closest_anno_bbox
            )
            image_array = cv2.cvtColor(image_array, cv2.COLOR_BGR2RGB)
            # if not category_cfg.get("type") == "local": # TODO: revise this feature
            #     # case of cloud category, we need to update the thumbnail throught he api
            #     config.client.update_category_image(category_uuid, image_array)
            # also write to disk directly
            from celer_sight_ai import configHandle
            import os

            image_path = os.path.join(
                configHandle.getLocal(),
                f"experiment_configs/category_image_cache/" + category_uuid + ".jpg",
            )
            if not os.path.exists(image_path):
                cv2.imwrite(image_path, image_array)

    def complete_analysis(self, result=None):
        from celer_sight_ai import config

        print("THREAD COMPLETE")
        self.setUpAnalysisSpreadSheetAfterFirstAnalysis()
        # make sure that the progress window is closed
        config.global_signals.complete_progress_bar_signal.emit()
        self.MainWindow.compute_transform_and_display_analysis()

        # Swith to Data Sheet tab
        self.MainWindow.MasterTabWidgets.setCurrentIndex(1)

    def setUpAnalysisSpreadSheetAfterFirstAnalysis(self):
        """Adds entries to the UI"""
        print("setUpAnalysisSpreadSheetAfterFirstAnalysis runs")
        self.MainWindow.channel_analysis_metrics_combobox.clear()
        from celer_sight_ai import config

        AnalObject = self.MainWindow.new_analysis_object
        ProjectVars = config.global_params
        # Clear all previous UI entries in Results_pg2_AnalysisTypeComboBox and channel_analysis_metrics_combobox
        self.MainWindow.Results_pg2_AnalysisTypeComboBox.clear()
        self.MainWindow.channel_analysis_metrics_combobox.clear()
        self.MainWindow.ROI_analysis_metrics_combobox.clear()
        # disable signals for the comboboxes
        # Disable signals for the comboboxes
        self.MainWindow.Results_pg2_AnalysisTypeComboBox.blockSignals(True)
        self.MainWindow.channel_analysis_metrics_combobox.blockSignals(True)
        self.MainWindow.ROI_analysis_metrics_combobox.blockSignals(True)
        QtWidgets.QApplication.processEvents()
        if (
            ProjectVars.analysis
            == self.MainWindow.new_analysis_object.analysis_map["mean_intensity"]
        ):

            # TODO: This only works in the first image, fix it by checking all images prior to this step
            # only add metric if it doesnt exist:
            for metric in self.MainWindow.DH.analysis_metrics_named:
                if (
                    self.MainWindow.Results_pg2_AnalysisTypeComboBox.findText(metric)
                    == -1
                ):
                    print(metric)
                    self.MainWindow.Results_pg2_AnalysisTypeComboBox.addItem(metric)
                    logger.info(f"Adding metric {metric}")
            for ch in self.analysis_channels_named:
                if self.MainWindow.channel_analysis_metrics_combobox.findText(ch) == -1:
                    self.MainWindow.channel_analysis_metrics_combobox.addItem(ch)
                    logger.info(f"Adding channel {ch}")
            # get all possible classes names
            for roi in self.analysis_roi_named:
                if self.MainWindow.ROI_analysis_metrics_combobox.findText(roi) == -1:
                    self.MainWindow.ROI_analysis_metrics_combobox.addItem(roi)
                    logger.info(f"Adding ROI {roi}")

        # Re-enable signals for the comboboxes
        self.MainWindow.Results_pg2_AnalysisTypeComboBox.blockSignals(False)
        self.MainWindow.channel_analysis_metrics_combobox.blockSignals(False)
        self.MainWindow.ROI_analysis_metrics_combobox.blockSignals(False)
        # manually trigger to update the tables
        self.MainWindow.compute_transform_and_display_analysis()

    def setUpAnalysisSpreadSheet(self):
        # function to populate the analysis comboboxes

        print("setUpAnalysisSpreadSheet runs")
        self.MainWindow.channel_analysis_metrics_combobox.clear()

        comboboxText1 = self.MainWindow.Results_pg2_AnalysisTypeComboBox.currentText()
        comboboxText2 = self.MainWindow.channel_analysis_metrics_combobox.currentText()

        if comboboxText1 == "Mean intensity":
            # self.MainWindow.channel_analysis_metrics_combobox.hide()

            self.MainWindow.Results_pg2_AnalysisTypeComboBox.addItems(
                self.MainWindow.DH.analysis_metrics_named
            )
            self.MainWindow.Results_pg2_AnalysisTypeComboBox.addItems(
                list(self.analysis_channels_named.keys())
            )
            self.MainWindow.ROI_analysis_metrics_combobox.addItems(
                list(self.analysis_roi_named.keys())
            )
        if comboboxText1 == "Aggregates":
            self.MainWindow.channel_analysis_metrics_combobox.show()
            self.MainWindow.channel_analysis_metrics_combobox.addItems(
                ["Area", "Count"]
            )
            print("added aggregate")
            return
        elif comboboxText1 == "Colocalization":
            self.MainWindow.channel_analysis_metrics_combobox.show()
            if (
                "pearson"
                in self.MainWindow.DH.allAnalysisDataContainer["colocalization"].keys()
            ):
                self.MainWindow.channel_analysis_metrics_combobox.addItems(["pearson"])
            if (
                "kendalls tau"
                in self.MainWindow.DH.allAnalysisDataContainer["colocalization"].keys()
            ):
                self.MainWindow.channel_analysis_metrics_combobox.addItems(
                    ["kendalls tau"]
                )
            if (
                "spearmans"
                in self.MainWindow.DH.allAnalysisDataContainer["colocalization"].keys()
            ):
                self.MainWindow.channel_analysis_metrics_combobox.addItems(
                    ["spearmans"]
                )

            if (
                "manders"
                in self.MainWindow.DH.allAnalysisDataContainer["colocalization"].keys()
            ):
                self.MainWindow.channel_analysis_metrics_combobox.addItems(["manders"])
                self.MainWindow.channel_analysis_metrics_combobox.addItems(
                    ["mandersM1"]
                )
                self.MainWindow.channel_analysis_metrics_combobox.addItems(
                    ["mandersM2"]
                )

            return
        else:
            return

    def Worker_1_analyse_complete_progress(self, prog):
        print("%d%% done" % prog)
        # self.MyLoadingAnimationDialogForm.label.setText("%d%% Done" % prog)
        if hasattr(self, "LoadingAnimationWidget"):
            if self.LoadingAnimationWidget.isVisible():
                self.MyLoadingAnimationDialogForm.progressBar.setValue(prog)

    def newOnkeyPressEvent(self, e):
        if e.key() == QtCore.Qt.Key.Key_Escape:
            print("User has pushed escape2")
        if self.viewer1.hasPhoto():
            if e.key() == QtCore.Qt.Key.Key_Space:
                self.viewer1.toggleDragMode()
                print("spaceee3")
            if e.key() == QtCore.Qt.MouseButton.RightButton:
                print("right button clicked")

        if e.key() == QtCore.Qt.Key.Key_Right and self.MainWindow.imagenumber < (
            len(self.MainWindow.DH.pixon_list_opencv) - 1
        ):
            print("pressed right")
            self.MainWindow.imagenumber = self.MainWindow.imagenumber + 1
            self.MainWindow.loadImage((self.MainWindow.imagenumber))
        if e.key() == QtCore.Qt.Key.Key_Left and self.MainWindow.imagenumber > 0:
            print("pressed left")
            self.MainWindow.imagenumber = self.MainWindow.imagenumber - 1
            self.MainWindow.loadImage(self.MainWindow.imagenumber)
            # self.show()
            print("pressed right")

        if e.key() == QtCore.Qt.Key.Key_Escape:
            self.close()

        if e.key() == QtCore.Qt.MouseButton.RightButton:
            print("right button clicked")

        # MY CHANGES HER ON DOWN

    ######################### create masks buttons

    # copied over from Ui_mainwow...
    def hide_pop_up_widnows(self):
        # self.MainWindow.signal_hide_dialog.emit()
        print("hide_pop_up_widnows")
        self.MainWindow.Win1Dialg.hide()
        self.MainWindow.Win2Dialg.hide()
        self.MainWindow.Win3Dialg.hide()
        self.MyAnalysisDialogWidget.hide()
        self.MyAnalysisDialogWidget.close()
        # self.accept()
        self.MyAnalysisDialogWidget.done(1)
        # self.Progress_dialog.hide()
        print("stuff hidden")

    def update_mask_size(self):
        # need to input all images and display again
        # get all masks predicted get all masks user
        current_mask = self.MainWindow.DH.all_masks[self.MainWindow.current_imagenumber]
        diluted_mask = self.mask_dilution(current_mask, self.mask_size_nmbr.value())
        return diluted_mask

        # add new mask an image

    def mask_dilution(self, mask, increase_mask_value):
        import numpy as np

        kernel = np.ones((5, 5), np.uint8)
        dilated_mask = cv2.dilate(
            mask.copy().astype(np.uint8), kernel, iterations=increase_mask_value
        )
        return dilated_mask

    def switch_binary_mask_state(self, input_state):
        if input_state == True:
            print("switch state is now false")
            config.global_params.masks_state = False
            return
        elif input_state == False:
            print("switch state is now true")
            config.global_params.masks_state = True
            return

    def combine_usr_predicted(self, predicted_masks, user_pointsx, user_pointsy):
        all_masks = []
        for mask in predicted_masks:
            if type(mask) == int:
                continue
            else:
                all_masks.append(mask)
        if self.MainWindow.selected_mask_origin == "mask":
            self.MainWindow.final_mask_number = (
                self.MainWindow.selected_mask
            )  # means that the final mask number is the one we need since combined mask = mask bitwise + user polygon p[opints]
        else:
            self.MainWindow.final_mask_number = self.MainWindow.selected_mask + len(
                self.MainWindow.DH.all_masks[self.MainWindow.current_imagenumber]
            )
        for i in range(len(user_pointsx)):
            if type(user_pointsx[i]) == int:
                continue
            all_masks.append(self.draw_polygon_mask(user_pointsy[i], user_pointsx[i]))

        return all_masks

    # copied over from Ui_mainwow...
    def draw_polygon_mask(self, pointsy, pointsx):
        import skimage

        # print("all points x in draw mask ", pointsx)
        mask = np.zeros(
            self.MainWindow.DH.pixon_list_opencv[
                self.MainWindow.current_imagenumber
            ].shape,
            dtype=bool,
        )
        rr, cc = skimage.draw.polygon(pointsy, pointsx, shape=mask.shape)
        mask[rr, cc] = True
        # print("THIS IS THE GENERATED MAS ", mask)
        return mask[:, :, 0]

    def meanIntensityRations(self, binMask, ImageOver, ImageUnder):
        """
        We get the mean value of image over and divide by image under gray val
        """
        import cv2

        ImageOverMean = cv2.mean(ImageOver, binMask.astype(np.uint8))[0]
        ImageUnderMean = cv2.mean(ImageUnder, binMask.astype(np.uint8))[0]
        if ImageUnderMean == 0:
            return "inf"
        return ImageOverMean / ImageUnderMean

    def meanGrayIntensity(self, binMask, Image):
        """
        Get the mean intensity of a gray Image
        """
        import cv2

        # meanValue = Image[binMask].mean()
        meanValue = cv2.mean(Image, binMask.astype(np.uint8))[0]
        return meanValue

    def mean_intensity_with_mask(self, np_image, bin_mask, colour="green"):
        # print(bin_mask)
        import numpy as np

        colour = "green"
        if colour == "green":
            bin_mask = bin_mask > 0.5
            imgAvg = np_image[bin_mask, 1].mean()
            #  np_image[bin_mask,1].sum()/np.count_nonzero(bin_mask)
            return imgAvg
        # elif colour =="red":

        #     imgAvg = np_image[bin_mask,0].sum()/np.count_nonzero(bin_mask)
        #     return imgAvg
        # elif colour == "blue":
        #     imgAvg = np_image[bin_mask,2].sum()/np.count_nonzero(bin_mask)

        # elif colour == "green_over_red":
        #     imgAvg_grn = np_image[bin_mask,1].sum()/np.count_nonzero(bin_mask)
        #     imgAvg_red = np_image[bin_mask,1].sum()/np.count_nonzero(bin_mask)
        #     return imgAvg_grn/imgAvg_red

    @config.threaded
    def calculate_all_RNAi(self, progress_callback=None):
        """
        This method is the main method that runs when the user clicks on the 'Anlyze' button
        """
        from celer_sight_ai import config

        try:
            # calculates all anlysis for the current exporiment
            ProjectConstants = self.MainWindow.new_analysis_object
            ProjectVars = config.global_params
            print("ProjectVars ", ProjectVars.AnalysisType)
            self.MainWindow.firstNewAnalysis = True
            if ProjectVars.analysis == ProjectConstants.analysis_map["mean_intensity"]:
                logger.info("using intensity on c elegans")
                self.calculate_all_intensities(progress_callback)
                logger.info("finished mean_fluorescent")
            elif ProjectVars.analysis == ProjectConstants.analysis_map["fragmentation"]:
                raise NotImplementedError("fragmentation not implemented")
                self.calculate_all_fragmentation(progress_callback)
                self.Worker_1_analyse.mysignals.finished.emit()
                print("finished Fragmentation")
                return
            elif ProjectVars.analysis == ProjectConstants.analysis_map["particles"]:
                logger.info("using intensity on c elegans")
                self.calculate_all_particles(progress_callback)
                if config.user_cfg["USER_WORKERS"]:
                    self.Worker_1_analyse.mysignals.finished.emit("ok")

                logger.info("finished mean_fluorescent")
                return
            elif (
                ProjectVars.analysis == ProjectConstants.analysis_map["colocalization"]
            ):
                raise NotImplementedError("Colocalization not implemented")
                self.calculate_all_colocalization(progress_callback)
                self.Worker_1_analyse.mysignals.finished.emit()
                print("finished colocalization")
                return
        except Exception as e:
            # in case of the error, close progess and raise error
            config.global_signals.complete_progress_bar_signal.emit()
            config.global_signals.errorSignal.emit("Analysis failed")
            raise ValueError(e)
            if config.user_cfg["USER_WORKERS"]:
                self.Worker_1_analyse.mysignals.finished.emit(e)
        finally:
            config.global_signals.complete_analysis_signal.emit({})

    def getIntenistyWithArea(self, progress_callback):
        """
        Calculates intenisties in addition to Area,
         used mainly for cells
        """
        import skimage
        import cv2
        import numpy as np

        raise NotImplementedError("Intensity with area for cells not implemented yet")

    def getGrayImage(self, image):
        NofChannels = len(config.global_params.MeasuredImageChannels)
        img = np.zeros((image.shape[0], image.shape[1]), dtype=np.uint8)
        for i in range(3):
            if any(config.global_params.MeasuredImageChannels) == i:
                img += (image[:, :, i] / NofChannels).astype(np.uint8)
        return img

    def calculate_all_colocalization(self, progress_callback):
        raise NotImplementedError

    def pearsonColocCS(
        self, image1_in, image2_in, maskIn_in, threshold1=0, threshold2=0
    ):
        raise NotImplementedError
        image1 = image1_in.copy()
        image2 = image2_in.copy()
        mask = maskIn_in.copy()
        image1_slice = image1 < threshold1
        image1[image1_slice] = 0
        image2_slice = image2 < threshold1
        image2[image2_slice] = 0

    def searchCostes(self, image1_in, image2_in, maskIn_in, threshold1=0, threshold2=0):
        raise NotImplementedError
        image1 = image1_in.copy()
        image2 = image2_in.copy()
        mask = maskIn_in.copy()
        image1_slice = image1 > threshold1
        image1[image1_slice] = 0
        image2_slice = image2 > threshold2
        image2[image2_slice] = 0

    def searchPearsonThresh(self, image1_in, image2_in, maskIn_in):
        import scipy

        redMax = np.max(image1_in)
        MeanValFinal = 0
        greenMax = np.max(image2_in)

        if redMax > greenMax:
            largeChannel = redMax
            ratioCh = greenMax / redMax
        else:
            largeChannel = greenMax
            ratioCh = redMax / greenMax
        for i in reversed(range(largeChannel - 1)):
            MeanVal = self.searchCostes(image2_in, image1_in, maskIn_in, i, i)
            if MeanVal <= 0 or np.isnan(MeanVal):
                for x in reversed(range(int(i + 1))):
                    MeanVal = self.searchCostes(
                        image2_in, image1_in, maskIn_in, i + 1, x
                    )
                    if MeanVal <= 0 or np.isnan(MeanVal):
                        outX = x
                        outY = i
                        # MeanValFinal = self.pearsonColocCS(image2_in, image1_in,maskIn_in,x,i)
                        break
                break
        return outX, outY

    def searchKendalsThresh(self, image1_in, image2_in, maskIn_in):
        MeanValFinal = 0
        redMax = np.max(image1_in)
        greenMax = np.max(image2_in)
        if redMax > greenMax:
            largeChannel = redMax
            ratioCh = greenMax / redMax
        else:
            largeChannel = greenMax
            ratioCh = redMax / greenMax
        for i in reversed(range(largeChannel - 1)):
            print("i is ", i)
            MeanVal = self.searchCostesKendals(image2_in, image1_in, maskIn_in, i, i)
            print("value below is ", MeanVal)
            if MeanVal <= 0 or np.isnan(MeanVal):
                for x in reversed(range(int(i + 1))):
                    MeanVal = self.searchCostesKendals(
                        image2_in, image1_in, maskIn_in, i + 1, x
                    )
                    if MeanVal <= 0 or np.isnan(MeanVal):
                        return x, i
                        # MeanValFinal = CelerSightModules.kendalsTau(greenImageIn ,redImageIn,maskIn ,x ,i)
                        break
                break

    def searchCostesKendals(
        self, image1_in, image2_in, maskIn_in, threshold1=0, threshold2=0
    ):
        raise NotImplementedError
        image1 = image1_in.copy()

    def properties_intensities(self, red_val, green_val, blue_val):
        if (
            config.global_params.red_ch == True
            and config.global_params.green_ch == True
            and config.global_params.blue_ch == True
        ):
            # TODO: I need to add some functionality here
            pass
        if (
            config.global_params.red_ch == True
            and config.global_params.green_ch == True
        ):
            """red over green"""
            if (
                config.global_params.first_ratio == "green"
                and config.global_params.second_ratio == "red"
            ):
                return green_val / red_val
            if (
                config.global_params.first_ratio == "red"
                and config.global_params.second_ratio == "green"
            ):
                return red_val / green_val

        if config.global_params.red_ch == True and config.global_params.blue_ch == True:
            """red over green"""
            if (
                config.global_params.first_ratio == "red"
                and config.global_params.second_ratio == "blue"
            ):
                return red_val / blue_val
            if (
                config.global_params.first_ratio == "blue"
                and config.global_params.second_ratio == "red"
            ):
                return blue_val / red_val
        if (
            config.global_params.green_ch == True
            and config.global_params.blue_ch == True
        ):
            if (
                config.global_params.first_ratio == "green"
                and config.global_params.second_ratio == "blue"
            ):
                return green_val / blue_val
            if (
                config.global_params.first_ratio == "blue"
                and config.global_params.second_ratio == "green"
            ):
                return blue_val / green_val

    def calculate_all_fragmentation(self, progress_callback):
        print("calculating fragmentation")
        raise NotImplementedError

    def GetPointsFromQPolygonF(self, polygonF):
        """
        Generates an (N,2) shaped array from a QPolygonF where N is the number of polygons
        """
        import numpy as np

        Startinglist = []
        for Point in polygonF:
            Startinglist.append([int(Point.y()), int(Point.x())])
        return np.asarray(Startinglist)

    def skimage_draw_polygon_with_holes(self, polygons):
        import skimage

        # make sure polygons is a list, not tuple
        if isinstance(polygons[0][0], tuple):
            # convert array to list
            for a in range(len(polygons)):
                polygons[a] = np.array([list(aa) for aa in polygons[a]])
        else:
            polygons = [np.array(i).squeeze() for i in polygons]
        # main polygon

        rr, cc = skimage.draw.polygon(polygons[0][:, 0], polygons[0][:, 1])
        main_polygon_set = set(zip(rr, cc))
        try:
            # subtract holes
            for i in range(1, len(polygons)):
                c_poly = polygons[i].squeeze()
                rr, cc = skimage.draw.polygon(c_poly[:, 0], c_poly[:, 1])
                hole_set = set(zip(rr, cc))
                main_polygon_set -= hole_set
        except Exception as e:
            print(e)
        # get final rr, cc coordinates
        main_polygon_as_list = list(main_polygon_set)
        if len(main_polygon_as_list) > 0:
            rr_final, cc_final = zip(*main_polygon_as_list)
        else:
            rr_final, cc_final = [], []

        return rr_final, cc_final

    def compute_particle_metrics_from_region(self, image, mask):
        """
        Computes the particle metrics from a region of interest
        This is the working function for computing particle metrics
        """
        from skimage.measure import label

        max_possible_val = np.iinfo(image.dtype).max
        label_mask = label(mask, connectivity=mask.ndim)
        # regionprops
        from skimage.measure import regionprops

        props = regionprops(label_mask, intensity_image=image)
        print()

        prop_dict = {
            "Particles (per subject)": len(props),
            "Particles total area (per subject)": np.sum([i.area for i in props]),
            "Particles area (per particle)": [i.area for i in props],
            "Particles eccentricity (mean per subject)": np.mean(
                [i.eccentricity for i in props]
            ),
            "Particles eccentricity (per particle)": [i.eccentricity for i in props],
            "Particles intensity (mean per subject)": np.mean(
                [i.intensity_mean for i in props]
            ),
            "Particles intensity (max per subject)": np.max(
                [i.intensity_max for i in props]
            ),
            "Particles intensity (min per subject)": np.min(
                [i.intensity_min for i in props]
            ),
            "Particles intensity (mean per particle)": [
                i.intensity_mean for i in props
            ],
            "Particles intensity (min per particle)": [i.intensity_min for i in props],
            "Particles intensity (max per particle)": [i.intensity_max for i in props],
            "Particles inverted image intensity (mean per subject)": max_possible_val
            - np.mean([i.intensity_mean for i in props]),
            "Particles inverted image intensity (max per subject)": max_possible_val
            - np.max([i.intensity_max for i in props]),
            "Particles inverted image intensity (min per subject)": max_possible_val
            - np.min([i.intensity_min for i in props]),
            "Particles inverted image intensity (mean per particle)": [
                max_possible_val - i.intensity_mean for i in props
            ],
            "Particles inverted image intensity (min per particle)": [
                max_possible_val - i.intensity_min for i in props
            ],
            "Particles inverted image intensity (max per particle)": [
                max_possible_val - i.intensity_max for i in props
            ],
        }
        return prop_dict

    def compute_intensity_metrics_from_region(self, image, rr, cc):
        """
        Computes the intensity metrics from a region of interest
        This is the working function for computing intensity metrics
        """
        import numpy as np

        # get the maximum possible value from the dtype of the image, possibilities are 8bit, 16 bit and 32 bit
        max_possible_val = np.iinfo(image.dtype).max
        try:
            mean = np.mean(image[cc, rr])
            min_val = np.min(image[cc, rr])
            max_val = np.max(image[cc, rr])
            std = np.std(image[cc, rr])

        except Exception as e:
            # cut off cc and rr larger than the image size
            # iterate and remove in a safe manner for lists
            for i in range(len(cc) - 1, -1, -1):
                if cc[i] >= image.shape[0] or rr[i] >= image.shape[1]:
                    cc.pop(i)
                    rr.pop(i)

        inverse_mean = 1 / (1 + mean)
        inverse_min = 1 / (1 + min_val)
        inverse_std = 1 / (1 + std)
        inverse_max = 1 / (1 + max_val)
        mean_offset = max_possible_val - mean
        min_offset = max_possible_val - min_val
        max_offset = max_possible_val - max_val
        std_offset = max_possible_val - std
        # round all to 3 decimal places
        return {
            "mean": round(mean, 3),
            "min": round(min_val, 3),
            "max": round(max_val, 3),
            "std": round(std, 3),
            "1 / mean": round(inverse_mean, 3),
            "1 / min": round(inverse_min, 3),
            "1 / max": round(inverse_max, 3),
            "1 / std": round(inverse_std, 3),
            "mean (inverted image)": round(mean_offset, 3),
            "min (inverted image)": round(min_offset, 3),
            "max (inverted image)": round(max_offset, 3),
            "std (inverted image)": round(std_offset, 3),
        }

    def PolyArea(self, x, y):
        """
        This function calculates the area of a polygon given its x and y coordinates.

        Args:
          x: The x-coordinates of the vertices of a polygon in order.
          y: The parameter `y` in the `PolyArea` function is a list or array of y-coordinates of the
        vertices of a polygon.

        Returns:
          The function `PolyArea` is returning the area of a polygon defined by the input arrays `x` and
        `y`. The formula used to calculate the area is based on the Shoelace formula, which involves taking
        the absolute value of the difference between the sum of the products of the x-coordinates and
        y-coordinates of adjacent vertices, divided by 2.
        """
        return 0.5 * np.abs(np.dot(x, np.roll(y, 1)) - np.dot(y, np.roll(x, 1)))

    def calculate_all_particles(self, progress_callback=None):
        """
        If a particle has a parent mask, only use that area to get the particles

        """

        print("calculating all particles")
        import skimage
        import cv2
        import numpy as np

        maxProg = 0  # maximum data
        current_round = 0
        for Condition, data in self.MainWindow.DH.BLobj.groups["default"].conds.items():
            maxProg += len(
                self.MainWindow.DH.BLobj.groups["default"].conds[Condition].images
            )
        if maxProg == 0:
            return
        Quant = 100 / maxProg
        AllQuant = 0
        dict_aggs_counts_all_RNAi = {}

        for Condition, data in self.MainWindow.DH.BLobj.groups[
            "default"
        ].conds.items():  # for all pixon images in condition
            current_round += 1

            # for every image
            for i in range(
                len(self.MainWindow.DH.BLobj.groups["default"].conds[Condition].images)
            ):
                AllQuant = AllQuant + Quant
                config.global_signals.update_progress_bar_progress_signal.emit(
                    {"percent": AllQuant}
                )
                channels = (
                    self.MainWindow.DH.BLobj.groups["default"]
                    .conds[Condition]
                    .images[i]
                    .channel_list
                )
                if isinstance(channels, type(None)):
                    continue
                # for every channel get image
                for ch_indx in range(len(channels)):
                    # get image for the current channel
                    img = (
                        self.MainWindow.DH.BLobj.groups["default"]
                        .conds[Condition]
                        .getImage(
                            i,
                            to_uint8=False,
                            to_rgb=False,
                            channel_names_to_filter=[channels[ch_indx]],
                        )
                    )

                    # find the underlying particle annotations (should be bitmap)
                    all_masks = (
                        self.MainWindow.DH.BLobj.groups["default"]
                        .conds[Condition]
                        .images[i]
                        .masks
                    )
                    particle_map = [i for i in all_masks if i.is_particle()]
                    non_particle_map = [i for i in all_masks if i not in particle_map]
                    # In the case of particle map, use the bitmask as particle source
                    # , if the bitmask has a parent mask, segment that area
                    # and compute a metric for each segmeneted instance
                    if len(particle_map) > 0:
                        particle_bitmap = particle_map[0].get_array()

                        for m, mask in enumerate(non_particle_map):
                            rr, cc = self.skimage_draw_polygon_with_holes(
                                mask.get_array()
                            )
                            if isinstance(rr, type(None)):
                                # means that there was an error with the array,
                                # it was probably empty thus, skip
                                continue
                            mask_base = np.zeros(img.shape[:2], dtype=np.uint8)
                            rr = np.clip(rr, 0, img.shape[1] - 1)
                            cc = np.clip(cc, 0, img.shape[0] - 1)
                            mask_base[cc, rr] = 255
                            instance_particles_mask = cv2.bitwise_and(
                                particle_bitmap, mask_base
                            )
                            try:
                                metrics_for_channel = (
                                    self.compute_particle_metrics_from_region(
                                        img, instance_particles_mask
                                    )
                                )
                            except:
                                print("error in compute_particle_metrics_from_region")
                                continue
                            metrics_for_channel["Subject (ROI) area"] = len(rr)

                            channel_key = config.ch_as_str(channels[ch_indx])
                            self.MainWindow.DH.BLobj.groups["default"].conds[
                                Condition
                            ].images[i].masks[m].particle_metrics[
                                channel_key
                            ] = metrics_for_channel
        config.global_signals.update_progress_bar_progress_signal.emit(
            {"title": "Finalizing analysis.", "percent": 100}
        )
        complete_analysis_dataframe = self.gather_all_analysis_data_in_a_df()
        import copy

        print("finaly is", dict_aggs_counts_all_RNAi)
        self.MainWindow.DH.allAnalysisDataContainer["Mean intensity"] = (
            complete_analysis_dataframe
        )
        self.MainWindow.DH.calculated_dictionary_state = (
            True  # indicate that the anlysis is complete
        )
        print("End")

        config.global_signals.complete_progress_bar_signal.emit()

    def calculate_all_intensities(self, progress_callback=None):
        print("calculating all intensities")
        import skimage
        import cv2
        import numpy as np
        import itertools

        self.MainWindow.all_RNAi_green_over_red_int = []
        self.MainWindow.all_RNAi_green_intensities = []
        self.MainWindow.all_RNAi_red_intensities = []

        # for every class and class combination
        # get all class groups
        class_groups = self.MainWindow.custom_class_list_widget.get_class_groups()

        prog = 0
        maxProg = 0  # maximum data
        current_round = 0
        for Condition, data in self.MainWindow.DH.BLobj.groups["default"].conds.items():
            maxProg += len(
                self.MainWindow.DH.BLobj.groups["default"].conds[Condition].images
            )

        if maxProg == 0:
            return
        Quant = 100 / maxProg
        AllQuant = 0
        dict_aggs_counts_all_RNAi = {}

        for Condition, data in self.MainWindow.DH.BLobj.groups[
            "default"
        ].conds.items():  # for all pixon images in condition
            # print("image_RNAi_slots length is ", len (self.MainWindow.DH.BLobj.groups['default'].conds))
            current_round += 1
            # load all temp lists from dictionaries
            # self.MainWindow.load_all_assets_listwidget_global(Condition)

            self.MainWindow.DH.aggs_counts_all_RNAi = []
            self.MainWindow.DH.aggs_volume_all_RNAi = []
            self.MainWindow.DH.summary_counts_RNAi = []
            self.MainWindow.DH.summary_volume_RNAi = []

            self.mean_worm_list = []
            self.mean_all_worms = 0
            # print("processing new IMAGE")

            # for every image
            for i in range(
                len(self.MainWindow.DH.BLobj.groups["default"].conds[Condition].images)
            ):
                # if image is ultra_high_res, raise error and stop
                if (
                    self.MainWindow.DH.BLobj.groups["default"]
                    .conds[Condition]
                    .images[i]
                    ._is_ultra_high_res
                ):
                    config.global_signals.errorSignal.emit(
                        "Image type ( ultra high resolution ) is not supported for this analysis"
                    )
                    return
                AllQuant = AllQuant + Quant
                config.global_signals.update_progress_bar_progress_signal.emit(
                    {"percent": AllQuant}
                )
                channels = (
                    self.MainWindow.DH.BLobj.groups["default"]
                    .conds[Condition]
                    .images[i]
                    .channel_list
                )
                if isinstance(channels, type(None)):
                    continue
                self.MainWindow.DH.BLobj.groups["default"].conds[Condition].images[
                    i
                ].generate_group_ids(
                    class_groups
                )  # by mask parent mask or class, categories masks

                # for every channel get image
                for ch_indx in range(len(channels)):
                    # get image for the current channel
                    img = (
                        self.MainWindow.DH.BLobj.groups["default"]
                        .conds[Condition]
                        .getImage(
                            i,
                            to_uint8=False,
                            to_rgb=False,
                            channel_names_to_filter=[channels[ch_indx]],
                        )
                    )
                    for m, mask in enumerate(
                        self.MainWindow.DH.BLobj.groups["default"]
                        .conds[Condition]
                        .images[i]
                        .masks
                    ):
                        # if mask is not polygon, skip
                        if mask.mask_type != "polygon":
                            continue

                        # These are the metrics for this channel only for these ROIs
                        img_obj = (
                            self.MainWindow.DH.BLobj.groups["default"]
                            .conds[Condition]
                            .images[i]
                        )
                        mask_arrays = img_obj.get_hierarchical_mask(
                            mask_object=mask, unified=False
                        )  # all possibilities
                        # to rr and cc
                        if isinstance(mask_arrays, type(None)) or isinstance(
                            mask_arrays[0], type(None)
                        ):
                            continue
                        rr, cc = self.skimage_draw_polygon_with_holes(mask_arrays[0])
                        if isinstance(rr, type(None)):
                            # means that there was an error with the array,
                            # it was probably empty thus, skip
                            logger.error(
                                f"Error in combined mask array for {Condition} , {i}"
                            )
                            continue
                        # if rr and cc are empty, skip
                        if len(rr) == 0 or len(cc) == 0:
                            logger.info(f"Skipping empty mask {mask.spatial_id}")
                            continue
                        rr = np.clip(rr, 0, img.shape[1] - 1)
                        cc = np.clip(cc, 0, img.shape[0] - 1)

                        try:
                            metrics_for_channel = (
                                self.compute_intensity_metrics_from_region(img, rr, cc)
                            )
                        except Exception as e:
                            logger.error(
                                "error in compute_intensity_metrics_from_region"
                            )
                            logger.error(e)
                            continue
                        metrics_for_channel["area"] = len(rr)

                        channel_key = config.ch_as_str(channels[ch_indx])
                        self.MainWindow.DH.BLobj.groups["default"].conds[
                            Condition
                        ].images[i].masks[m].intensity_metrics[
                            channel_key
                        ] = metrics_for_channel

        # compute all combinations of channels etc..
        complete_analysis_dataframe = self.gather_all_analysis_data_in_a_df()
        import copy

        print("finaly is", dict_aggs_counts_all_RNAi)
        self.MainWindow.DH.allAnalysisDataContainer["Mean intensity"] = (
            complete_analysis_dataframe
        )
        self.MainWindow.DH.calculated_dictionary_state = (
            True  # indicate that the anlysis is complete
        )
        logger.info("Intensity analysis complete")

    def smooth_paths(self, centroids, window_length=3, polyorder=2):
        """
        Apply Savitzky-Golay filter to smooth each component of the centroids.
        Assumes centroids is a list of (x, y) tuples.
        """
        from scipy.signal import savgol_filter

        x_coords = [c[0] for c in centroids if c is not None]
        y_coords = [c[1] for c in centroids if c is not None]

        # Apply the filter to x and y coordinates separately
        x_smooth = savgol_filter(x_coords, window_length, polyorder)
        y_smooth = savgol_filter(y_coords, window_length, polyorder)

        return list(zip(x_smooth, y_smooth))

    def calculate_velocities(self, smooth_centroids):
        """
        Calculate velocities between consecutive centroids.
        Assumes time_interval is the time between frames.
        """
        velocities = []
        for i in range(1, len(smooth_centroids)):
            dx = smooth_centroids[i][0] - smooth_centroids[i - 1][0]
            dy = smooth_centroids[i][1] - smooth_centroids[i - 1][1]
            velocity = np.sqrt(dx**2 + dy**2)
            velocities.append(velocity)
        return velocities

    def calculate_all_velocities_for_tracks(self, file_location):
        # calculate stats for all velocities for the tracks
        tracks_velocities_per_treatment = {}
        min_track_legnth = 10
        for treatment_name, treatment_object in self.MainWindow.DH.BLobj.groups[
            "default"
        ].conds.items():
            treatment_track_centroids = []
            # get all tracks for that treatment
            treatment_tracks = (
                self.MainWindow.DH.BLobj.get_all_annotation_tracks_for_treatment(
                    treatment_object
                )
            )
            for t in treatment_tracks:
                track_path = (
                    self.MainWindow.DH.BLobj.get_centroid_path_for_annotation_track(
                        treatment_object, t
                    )
                )
                # if track path length is less then 3 skip
                if len(track_path) < min_track_legnth:
                    continue
                # smooth track
                smooth_paths = self.smooth_paths(track_path)
                velocities = self.calculate_velocities(smooth_paths)
                treatment_track_centroids.extend(velocities)
            tracks_velocities_per_treatment[
                self.MainWindow.DH.BLobj.get_treatment_name_by_uuid(
                    treatment_object.unique_id
                )
            ] = treatment_track_centroids
        # convert to a dataframe and save to disk
        import pandas as pd

        # padd arrays that are not the same length as max
        max_len = max([len(i) for i in tracks_velocities_per_treatment.values()])
        for k, v in tracks_velocities_per_treatment.items():
            if len(v) < max_len:
                tracks_velocities_per_treatment[k] = v + [np.nan] * (max_len - len(v))
        pd = pd.DataFrame.from_dict(tracks_velocities_per_treatment)
        pd.to_csv(file_location)

    def rgb_to_hex(self, arr):
        return "#{:02x}{:02x}{:02x}".format(arr[0], arr[1], arr[2])

    def gather_all_analysis_data_in_a_df(self):
        """
        The function `gather_all_analysis_data_in_a_df` iterates through images, channels, and masks to
        gather all data and create a pandas dataframe with all metrics. This runs after the measurement step,
        to compute combinations and ratios between channels and ROIs.

        Returns:
          a pandas DataFrame that contains all the analysis data gathered from iterating through images,
        channels, and masks.
        """
        import pandas as pd
        import numpy as np
        import copy
        import itertools
        import webcolors

        from celer_sight_ai.io.data_handler import ImageObject

        # Gather all Class IDs for ROIs
        all_class_ids = list(self.MainWindow.custom_class_list_widget.classes.keys())
        class_combinations = [
            i for i in list(itertools.product(all_class_ids, repeat=2))
        ]

        all_channels = self.MainWindow.DH.BLobj.get_all_channels()
        all_channels = [
            config.ch_as_str(i) for i in all_channels
        ]  # convert the rgb values to string

        # Generate Channel Combinations excluding identical pairs
        channel_combinations = [
            i for i in list(itertools.product(all_channels, repeat=2)) if i[0] != i[1]
        ]

        # Generate ROI Combinations excluding identical pairs
        roi_combinations = [
            i for i in list(itertools.product(all_class_ids, repeat=2)) if i[0] != i[1]
        ]

        SKIPPED_IMAGES_DUE_TO_MISSING_PARTICLES = False
        analysis_metrics_stored = False

        df = pd.DataFrame()

        # Iterate Over Each Condition
        for Condition, data in self.MainWindow.DH.BLobj.groups["default"].conds.items():
            # Iterate Over Each Image in the Condition
            for i in range(
                len(self.MainWindow.DH.BLobj.groups["default"].conds[Condition].images)
            ):
                # Get All Channels for the Current Image
                all_channels = (
                    self.MainWindow.DH.BLobj.groups["default"]
                    .conds[Condition]
                    .images[i]
                    .channel_list
                )
                all_channels_names = [
                    (str(c) if isinstance(all_channels[c], list) else all_channels[c])
                    for c in range(len(all_channels))
                ]

                # Iterate Over Each Channel
                for ch_indx in range(len(all_channels)):
                    ch_key = config.ch_as_str(all_channels[ch_indx])
                    # Iterate Over Each Mask in the Image
                    for m, mask in enumerate(
                        self.MainWindow.DH.BLobj.get_all_annotation_objects_for_image(
                            "default", Condition, i, without_particles=True
                        )
                    ):
                        # Retrieve Metrics
                        if not len(mask.intensity_metrics) == 0:
                            mask_metrics = mask.intensity_metrics[ch_key]
                        elif not len(mask.particle_metrics) == 0:
                            mask_metrics = mask.particle_metrics[ch_key]
                        else:
                            SKIPPED_IMAGES_DUE_TO_MISSING_PARTICLES = True
                            continue

                        # Deep Copy Metrics to Temporary Dictionary
                        tmpDict = copy.deepcopy(mask_metrics)
                        if not analysis_metrics_stored:
                            self.MainWindow.DH.analysis_metrics_named = list(
                                tmpDict.keys()
                            )  # Keys to be displayed
                            analysis_metrics_stored = True

                        # Add Additional Information to tmpDict
                        mask.debug_mask_image()
                        tmpDict["Condition"] = Condition
                        tmpDict["Image"] = i
                        tmpDict["Mask"] = m
                        tmpDict["spatial_id"] = mask.spatial_id
                        tmpDict["class_group_id"] = mask.class_group_id
                        tmpDict["Roi"] = (
                            self.MainWindow.custom_class_list_widget.classes[
                                mask.class_id
                            ].text()
                        )

                        # Determine Channel Name with Color
                        if isinstance(ch_key, list):
                            ch_name = "#{:02x}{:02x}{:02x}".format(*ch_key)
                        else:
                            if not ch_key.startswith("#"):
                                ch_name = "#{:02x}{:02x}{:02x}".format(
                                    *channel_to_color(ch_key)
                                )
                            else:
                                ch_name = (
                                    ch_key  # Assuming ch_key is already a hex string
                                )

                        channel_name = f"<font color={ch_name}>{ch_key}</font>"
                        tmpDict["Channel"] = channel_name
                        self.analysis_channels_named[channel_name] = [
                            ch_key
                        ]  # the actual channel name as stored in the image data

                        # Append to DataFrame
                        df = pd.concat([df, pd.DataFrame([tmpDict])], ignore_index=True)

                # Compute Channel-Based Combinations
                for m, mask in enumerate(
                    self.MainWindow.DH.BLobj.get_all_annotation_objects_for_image(
                        "default", Condition, i, without_particles=True
                    )
                ):
                    for ch1, ch2 in channel_combinations:
                        if ch1 == ch2:
                            continue
                        if isinstance(ch1, str):
                            if ch1.startswith("#"):
                                ch1_name = f"({webcolors.hex_to_name(ch1)})"
                            else:
                                ch1_name = "#{:02x}{:02x}{:02x}".format(
                                    *channel_to_color(ch1)
                                )

                            if ch2.startswith("#"):
                                ch2_name = f"({webcolors.hex_to_name(ch2)})"
                            else:
                                ch2_name = "#{:02x}{:02x}{:02x}".format(
                                    *channel_to_color(ch2)
                                )
                        else:
                            ch1_name = ch1
                            ch2_name = ch2
                        for (
                            operation_ch,
                            op_method_ch,
                        ) in SUPPORTED_CHANNEL_OPERATIONS.items():
                            channel_key_1 = f"<font color={ch1_name}>{ch1}</font>"
                            channel_key_2 = f"<font color={ch2_name}>{ch2}</font>"
                            comb_channel_key = (
                                channel_key_1
                                + f"<font color=white> {operation_ch} </font> "
                                + channel_key_2
                            )
                            # Add as values the displayed names, needed for indexing of the original channel names
                            combination_channel_list = [
                                channel_key_1,
                                operation_ch,
                                channel_key_2,
                            ]

                            # Store the key as shown in the combobox and the channel names as stored
                            # in the image data, this is done to compute channel metrics upon request
                            self.analysis_channels_named[comb_channel_key] = (
                                combination_channel_list
                            )

                # Compute ROI-Based Combinations
                for roi1, roi2 in roi_combinations:
                    roi1_name = self.MainWindow.custom_class_list_widget.classes[
                        roi1
                    ].text()
                    roi2_name = self.MainWindow.custom_class_list_widget.classes[
                        roi2
                    ].text()
                    for (
                        operation_roi,
                        op_method_roi,
                    ) in SUPPORTED_ROI_OPERATIONS.items():
                        comb_roi_key = f"{roi1_name} {operation_roi} {roi2_name}"
                        combination_roi_list = [roi1_name, operation_roi, roi2_name]

                        # Store the key as shown in the combobox and the ROI names
                        self.analysis_roi_named[comb_roi_key] = combination_roi_list
                # add the roi names to the analysis_roi_named (not the combinations)
                for roi in all_class_ids:
                    self.analysis_roi_named[
                        self.MainWindow.custom_class_list_widget.classes[roi].text()
                    ] = [roi]

        # Emit Warning if Any Images Were Skipped
        if SKIPPED_IMAGES_DUE_TO_MISSING_PARTICLES:
            config.global_signals.warningSignal.emit(
                "Some images were skipped due to missing or corrupt ROI data.\nMake sure ROI's have been correctly configured."
            )

        return df

    def calculate_all(self, progress_callback):
        "aggregate analysis"
        raise NotImplementedError

    def colorizeGray(self, imageGray):
        # colorizes the image depending on the
        tmpImage = np.zeros((imageGray.shape[0], imageGray.shape[1], 3))
        if self.currentActiveChannel == 1:  # first channel to measure
            tmpImage[:, :, self.channelToMeasureList[0]] = imageGray
        elif self.currentActiveChannel == 2:  # seoond channel to measure
            tmpImage[:, :, self.channelToMeasureList_2[0]] = imageGray
        return tmpImage

    def sub_background(self, preNum=None):
        if preNum == None:
            valToUse = self.substract_background_nmbr.value()
        else:
            valToUse = preNum
        self.no_background_1 = self.show_background_image(
            self.gray_image.copy(), radius=valToUse
        )
        self.radius_BG = self.substract_background_nmbr.value()

    def sub_background_2(self):
        self.no_background_1_2 = self.show_background_image(
            self.gray_image_2.copy(), radius=self.substract_background_nmbr_2.value()
        )
        self.radius_BG_2 = self.substract_background_nmbr_2.value()

    def get_threshold(self, preNum=None):
        if preNum == None:
            self.ret, self.threshed_image = cv2.threshold(
                self.no_background_1,
                self.adjust_threshold_nmbr.value(),
                255,
                cv2.THRESH_BINARY,
            )
        else:
            self.ret, self.threshed_image = cv2.threshold(
                self.no_background_1, preNum, 255, cv2.THRESH_BINARY
            )

        self.threshold_BG = self.adjust_threshold_nmbr.value()

    def get_threshold_2(self):
        self.ret, self.threshed_image_2 = cv2.threshold(
            self.no_background_1_2,
            self.adjust_threshold_nmbr_2.value(),
            255,
            cv2.THRESH_BINARY,
        )
        self.threshold_BG = self.adjust_threshold_nmbr_2.value()

    def get_image(self):
        self.image_1 = self.MainWindow.DH.pixon_list_opencv[
            self.MainWindow.current_imagenumber
        ]

    def show_background_image(self, gray_image, radius=5):
        from skimage.morphology import disk, white_tophat

        AnalObject = self.MainWindow.new_analysis_object
        ProjectVars = config.global_params
        from skimage.transform import resize

        if radius >= 8:
            gray_orig = gray_image.copy()
            original_shape_1 = gray_image.shape[0]
            original_shape_2 = gray_image.shape[1]
            gray_orig = resize(
                gray_orig,
                (original_shape_1 // (radius / 8), original_shape_2 // (radius / 8)),
                anti_aliasing=False,
                preserve_range=True,
            )
            selem = disk(8)
            w_tophat = white_tophat(gray_orig, selem)
            gray_orig_tophat = resize(
                w_tophat,
                (original_shape_1, original_shape_2),
                anti_aliasing=False,
                preserve_range=True,
            ).astype(np.uint8)

            if ProjectVars.organism == AnalObject.tissue:
                Thresh = cv2.threshold(gray_image.copy(), 252, 255, cv2.THRESH_BINARY)[
                    1
                ].astype(bool)
                print(Thresh.shape)
                gray_orig_tophat[Thresh] = 255
            return gray_orig_tophat
        else:
            selem = disk(radius)
            w_tophat = white_tophat(gray_image, selem)
            if ProjectVars.organism == AnalObject.tissue:
                Thresh = cv2.threshold(gray_image.copy(), 240, 255, cv2.THRESH_BINARY)[
                    1
                ].astype(bool)
                w_tophat[Thresh] = 255
            return w_tophat
        return w_tophat

    def get_green_ch(self, image):
        self.gray_image = image[:, :, 1]

    def get_red_ch(self, image):
        self.gray_image = image[:, :, 0]

    def get_blue_ch(self, image):
        self.gray_image = image[:, :, 2]

    def get_mask_prediction_all(
        self,
    ):
        img_tmp_1 = self.image_1
        # model._make_predict_function()
        results = self.MainWindow.model.detect([img_tmp_1.copy()], verbose=1)
        r = results[0]
        self.mask_prediction = r["masks"]

    def get_mask_prediction(
        self,
    ):
        img_tmp_1 = self.image_1_m
        results = self.MainWindow.model.detect([img_tmp_1], verbose=1)
        r = results[0]
        self.mask_prediction = r["masks"]

    def apply_mask2(self, image, mask):
        redImg = np.zeros(image.shape, image.dtype)
        redImg[:, :] = (0, 0, 255)
        redMask = cv2.bitwise_and(redImg, redImg, mask=mask)
        cv2.addWeighted(redMask, 0.4, image, 1, 0, image)
        return image

    def count_particles_all(self, input_image):
        import statistics

        connectivity = 4
        particles = []
        nlabel, labels, stats, centroids = cv2.connectedComponentsWithStats(
            input_image, connectivity, cv2.CV_32S
        )
        for i in range(1, nlabel):
            # print(stats[i,cv2.CC_STAT_AREA])
            # print(particles.extend(output[2][i,cv2.CC_STAT_AREA]))
            particles.append(stats[i, cv2.CC_STAT_AREA])
            print(particles)
        if len(particles) >= 1:
            mean = statistics.mean(particles)
        else:
            mean = 0
        return mean

    def count_particles(self, input_image):
        connectivity = 4
        output = cv2.connectedComponentsWithStats(input_image, connectivity, cv2.CV_32S)
        for i in range(1, output[0]):
            print(output[2][i, cv2.CC_STAT_AREA])

    def right_button(self):
        if self.MainWindow.current_imagenumber < (
            len(
                self.MainWindow.DH.BLobj.groups["default"]
                .conds[self.MainWindow.DH.BLobj.get_current_condition()]
                .images
            )
            - 1
        ):
            self.MainWindow.current_imagenumber += 1
            self.main_process()

    def left_button(self):
        if self.MainWindow.current_imagenumber >= 0:
            self.MainWindow.current_imagenumber -= 1
            self.main_process()

    def next_condition_action(self):
        conditionAt = 0
        print("next condition action")
        totalConditions = self.MainWindow.RNAi_list.count()
        for i in range(totalConditions):
            if (
                self.MainWindow.RNAi_list.item(i).text()
                == self.MainWindow.DH.BLobj.get_current_condition()
            ):
                conditionAt = i
        if conditionAt < totalConditions - 1:
            itemNext = self.MainWindow.RNAi_list.item(conditionAt + 1)
            self.MainWindow.RNAi_list.setCurrentItem(itemNext)
            self.MainWindow.RNAi_list.itemClicked.emit(itemNext)
            self.MainWindow.DH.BLobj.set_current_condition(itemNext.text())
            QtWidgets.QApplication.processEvents()
            # self.MainWindow.current_imagenumber += 1
            self.main_process()

    def previous_condition_action(self):
        if self.MainWindow.current_imagenumber < (
            len(
                self.MainWindow.DH.BLobj.groups["default"]
                .conds[self.MainWindow.DH.BLobj.get_current_condition()]
                .images
            )
            - 1
        ):
            self.MainWindow.current_imagenumber += 1
            self.main_process()

    ###############################
    ######## SHOW IMAGE ANALYSIS FUNCTIONS
    ###############################

    def main_process(self):
        AnalObject = self.MainWindow.new_analysis_object
        ProjectVars = config.global_params

        return
