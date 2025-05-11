import logging

import numpy as np
from PyQt6 import QtCore, QtGui, QtWidgets

from celer_sight_ai import config
from celer_sight_ai.gui.designer_widgets_py_files.AssetButtonWidget import (
    Ui_Form as AssetButtonWidgetUI,
)

logger = logging.getLogger(__name__)

AssetButtonStyleSheet = """
QPushButton:checked{
background-color: white;
}
QPushButton{
background-color: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #2d2d2d, stop: 0.1 #2b2b2b, stop: 0.5 #292929, stop: 0.9 #282828, stop: 1 #252525);
}
                    """


class ImageButtonPlaceHolderClass:
    """
    A placeholder class for ButtonAsset.

    This class holds the state and data for a ButtonAsset before it is visible.

    Attributes:
        MyIconSize (int): The size of the icon.
        _IsChecked (bool): State to determine whether the user has checked the mask of the images or not.
        _IncludedInAnalysis (bool): State to determine whether the asset is included in analysis.
        image_id (str): The image ID of the asset.
        MainWindow (MainWindow): The main window instance.
        hasBeenChecked (bool): State to determine whether the asset has been checked.
        movie (Movie): The movie instance associated with the asset.
        isDoneSettingUp (bool): State to determine whether the setup is done.
        marked_for_deletion (bool): State to determine whether the asset is marked for deletion.
        button_instance (ButtonAssetClass): The ButtonAssetClass instance associated with the asset.

    Args:
        MainWindow (MainWindow): The main window instance.
        image_uuid (str): The image uuid of the asset.
    """

    def __init__(self, MainWindow=None, image_uuid=None, image_number=None) -> None:
        self.MyIconSize = 170
        self._IsChecked = False  # state to determin weather the user has checked the masked of the images or not
        self._IncludedInAnalysis = True
        self.image_uuid = image_uuid
        self.image_number = image_number
        self.MainWindow = MainWindow
        self.hasBeenChecked = False
        self.movie = None
        self.isDoneSettingUp = False
        self.marked_for_deletion = False
        self.button_instance = None  # ButtonAssetClass instnace goes here once visible
        self.button_instance_proxy = None

    @property
    def button_instance(self):
        """
        Gets the ButtonAssetClass instance.

        Returns:
            ButtonAssetClass: The button instance associated with this placeholder.
        """
        # if the button instance is not set, create a new one
        # if not self._button_instance:
        #     self._button_instance = ButtonAssetClass(MainWindow=self.MainWindow, ButtonHolder=self)
        return self._button_instance

    @button_instance.setter
    def button_instance(self, value):
        """
        Sets the ButtonAssetClass instance.

        Args:
            value (ButtonAssetClass): The button instance to associate with this placeholder.
        """
        self._button_instance = value


class ButtonAssetClass(QtWidgets.QPushButton):
    """
    Class for adding functions and variabels to base widget
    for the Asset buttons
    """

    clicked = QtCore.pyqtSignal()
    ImageEventChanged = QtCore.pyqtSignal()
    # A signal that is emitted when the inference is started and ended.
    # startInfernceLoading = QtCore.pyqtSignal()
    # endInferenceSingal = QtCore.pyqtSignal()

    def __init__(self, MainWindow=None, ButtonHolder=None):
        super(QtWidgets.QPushButton, self).__init__()
        self.ButtonHolder = ButtonHolder
        self.MainWindow = MainWindow
        self.during_animation = (
            False  #  is on during inference to animatin the loading gif
        )
        self.MainWindow.installEventFilter(self)
        self.allowContexMenu = False
        self.marked_for_deletion = False
        self.setCheckable(True)
        if self.allowContexMenu:
            self.contextMenu = QtWidgets.QMenu(self)
            IncludeInAnalysisAction = self.contextMenu.addAction("Include in Analysis")
            ExcludeFromAnalysisAction = self.contextMenu.addAction(
                "Exclude from Analysis"
            )
            DeleteButtonAction = self.contextMenu.addAction("Delete Asset")
            IncludeAllInAnalysis = self.contextMenu.addAction("Include All In Analysis")

            # Connect existing actions
            IncludeInAnalysisAction.triggered.connect(
                lambda: self.SetAnalysisStatus(Status=True)
            )
            ExcludeFromAnalysisAction.triggered.connect(
                lambda: self.SetAnalysisStatus(Status=False)
            )
            DeleteButtonAction.triggered.connect(
                lambda: self.deleteCurrentImage(reload_image=True)
            )

            # Remove the empty action that was there before
            # run_inference_action = self.contextMenu.addAction("")

        self.ui = AssetButtonWidgetUI()
        self.ui.setupUi(self)
        self.ui.MainAssetButton.hide()
        self.ResizedImageQPixMapOn = None
        # if during inference, check if the animation should be running
        if self.MainWindow.MyInferenceHandler.is_inference_running:
            self.startInferenceAnimation(image_uuid=self.ButtonHolder.image_uuid)

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)

        # Draw the round border
        painter.setBrush(QtGui.QBrush(QtCore.Qt.GlobalColor.white))  # Set border color
        round_rect_path = QtGui.QPainterPath()
        round_rect_path.addRoundedRect(self.rect().toRectF(), 7, 7)
        painter.drawPath(round_rect_path)

        # Set the clip path for rounded corners
        painter.setClipPath(round_rect_path)

        # Draw the icon if it exists
        if self.ResizedImageQPixMapOn:
            pixmap = self.ResizedImageQPixMapOn
            target_rect = self.rect()
            pixmap_rect = pixmap.rect()
            if pixmap_rect:
                # Calculate the scaling factor for both width and height
                width_scale = target_rect.width() / pixmap_rect.width()
                height_scale = target_rect.height() / pixmap_rect.height()

                # Choose the larger scaling factor to ensure the pixmap covers the whole widget
                scale_factor = max(width_scale, height_scale)

                # Apply the scaling
                scaled_size = QtCore.QSize(
                    int(pixmap.width() * scale_factor),
                    int(pixmap.height() * scale_factor),
                )

                pixmap = pixmap.scaled(
                    scaled_size,  # Scale to the new size
                    QtCore.Qt.AspectRatioMode.KeepAspectRatio,  # Keep the aspect ratio
                    QtCore.Qt.TransformationMode.SmoothTransformation,  # Use smooth transformation
                )

                # Center the pixmap in the target rectangle
                target_rect.setSize(scaled_size)
            target_rect.moveCenter(self.rect().center())

            # Draw the pixmap
            source_rect = pixmap.rect()
            painter.drawPixmap(target_rect, pixmap, source_rect)

        painter.end()

    # # Draw the button text
    # painter.setPen(QtGui.QPen(QtCore.Qt.GlobalColor.black))  # Set text color
    # painter.drawText(self.rect(), QtCore.Qt.AlignmentFlag.AlignCenter, self.text())

    def set_channels(self, channels: list):
        # TODO: Needs update ot be compatible with ButtonHolder
        # channel is a list of rgb values to create channel buttons from
        MainButton = self.findChild(QtWidgets.QPushButton, "MainAssetButton")
        for i, channel in enumerate(channels):
            button = QtWidgets.QPushButton(self)
            button.setStyleSheet(f"background-color: rgb{tuple(channel)}")
            button.setFixedSize(10, 10)
            button.setSizePolicy(
                QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed
            )
            button.move(
                MainButton.width() - ((i * 5) - 15),
                MainButton.pos().y() + 15,
            )
            button.show()
            button.raise_()

    def startInferenceAnimation(self, image_uuid=None):
        if image_uuid and not self.ButtonHolder.image_uuid == image_uuid:
            return
        else:
            image_uuid = self.ButtonHolder.image_uuid
        # check to make sure that there are inference requests for this image
        image_object = self.MainWindow.DH.BLobj.get_image_object_by_uuid(image_uuid)

        if not image_object._during_inference:
            return

        label_widget = self.findChild(QtWidgets.QWidget, "checkLabel")
        self.during_animation = True
        if not hasattr(self, "movie"):
            self.movie = QtGui.QMovie("data/videos/inference_loading.gif")
            self.movie.setScaledSize(QtCore.QSize(98, 98))
            # set size of label_widget to match the parent frame
            label_widget.setMaximumSize(self.size())
            label_widget.setMinimumSize(self.size())
            label_widget.move(0, 0)
            label_widget.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        # set movei to label
        label_widget.setMovie(self.movie)
        # center label in the parent widget
        label_widget.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        label_widget.setContentsMargins(0, 0, 0, 0)
        self.movie.start()
        label_widget.show()

    def setupSelfPic(self, idNum=0):
        self.mainPicBtn = self.findChild(QtWidgets.QPushButton, "MainAssetButton")
        self.mainPicBtn.clicked.connect(lambda: self.onChecked())
        self._IsChecked = False
        self.image_number = idNum

    def setCurrentButton(self):
        self.MainWindow.set_curent_button(imagenumber=self.ButtonHolder.image_number)
        self.MainWindow.load_main_scene(
            image_number=self.ButtonHolder.image_number, fit_in_view=True
        )
        self.MainWindow.viewer.setDragMode(QtWidgets.QGraphicsView.DragMode.NoDrag)
        self.MainWindow.viewer.setFocus()

    def handle_button_toggled(self, state):
        if state:
            self.onChecked()
        else:
            self.onUnchecked()

    def set_checked_to_false(self):
        self.setChecked(False)
        self.onUnchecked()

    def set_label_number(self, number):
        labelNumber = self.findChild(QtWidgets.QLabel, "AssetButtonLabelNumber")
        labelNumber.setText(str(number))
        labelNumber.setParent(self)
        labelNumber.raise_()
        labelNumber.move(5, 5)
        # make font larger
        labelNumber.setFont(QtGui.QFont("Arial", 68, QtGui.QFont.Weight.Bold))
        labelNumber.setMaximumSize(QtCore.QSize(100, 100))
        labelNumber.setMinimumSize(QtCore.QSize(100, 100))
        labelNumber.setText(str(number))
        # if its current_imagenumber is the same as the buttons number, set to white label
        # if self.MainWindow.current_imagenumber == number - 1:
        #     labelNumber.setStyleSheet("color: rgba(255, 255, 255 , 170);")
        # else:
        labelNumber.setStyleSheet("color: rgba(255, 255, 255 , 30);")

    def set_label_color(self, checked=None):
        if checked is None:
            checked = self.isChecked()
        if checked:
            labelNumber = self.findChild(QtWidgets.QLabel, "AssetButtonLabelNumber")
            labelNumber.setStyleSheet("color: rgba(255, 255, 255 , 170);")
        else:
            labelNumber = self.findChild(QtWidgets.QLabel, "AssetButtonLabelNumber")
            labelNumber.setStyleSheet("color: rgba(255, 255, 255 , 30);")

    def onChecked(self):
        """
        When the button is checked, it handles selection based on modifier keys:
        - No modifier: Single selection
        - Shift: Range selection from last selected to current
        - Ctrl/Cmd: Toggle selection without affecting other selections
        """
        # Get the current keyboard modifiers
        modifiers = QtWidgets.QApplication.keyboardModifiers()

        if modifiers == QtCore.Qt.KeyboardModifier.ShiftModifier:
            # Shift click - select range
            self.MainWindow.images_preview_graphicsview.handle_range_selection(
                self.ButtonHolder.image_number
            )
        elif modifiers == QtCore.Qt.KeyboardModifier.ControlModifier:
            # if this item is already selected, deselect it
            if (
                self.ButtonHolder.image_number
                in self.MainWindow.images_preview_graphicsview.selected_buttons
            ):
                self.onUnchecked()
            # else select it
            else:
                self.set_checked_to_true()
                self.MainWindow.images_preview_graphicsview.selected_buttons.append(
                    self.ButtonHolder.image_number
                )
        else:
            # Normal click - single selection
            self.MainWindow.images_preview_graphicsview.uncheck_all_buttons_except_current()
            self.MainWindow.images_preview_graphicsview.selected_buttons.clear()
            self.MainWindow.images_preview_graphicsview.selected_buttons.append(
                self.ButtonHolder.image_number
            )
            self.setCurrentButton()
            self.set_checked_to_true()
        return

    def set_checked_to_true(self):
        self.set_label_color(True)
        self.hasBeenChecked = True

    def set_checked_to_false(self):
        self.set_label_color(False)
        self.hasBeenChecked = False

    def onUnchecked(self):
        """
        When the button is unchecked, it changes the label color
        """
        self.set_checked_to_false()
        self.MainWindow.images_preview_graphicsview.selected_buttons.remove(
            self.ButtonHolder.image_number
        )
        return

    def rearrange_buttons(self, adjust_image_number=True):
        # TODO: needs to be deprecated
        proxy_items = self.MainWindow.images_preview_graphicsview.scene().items()
        proxy_items = [i for i in proxy_items if i.isVisible()]
        if adjust_image_number:
            for proxy_item in proxy_items:
                item = proxy_item.widget()
                if type(item) == ButtonAssetClass:
                    if item.ButtonHolder.image_number > self.ButtonHolder.image_number:
                        item.ButtonHolder.image_number -= 1
                labelNumber = item.findChild(QtWidgets.QLabel, "AssetButtonLabelNumber")
                labelNumber.setText(str(item.ButtonHolder.image_number + 1))

            # do the same for image objects witht the imgID parameter

            for i in range(
                len(
                    self.MainWindow.DH.BLobj.groups["default"]
                    .conds[self.MainWindow.DH.BLobj.get_current_condition()]
                    .images
                )
            ):
                if i >= self.ButtonHolder.image_number:
                    self.MainWindow.DH.BLobj.groups["default"].conds[
                        self.MainWindow.DH.BLobj.get_current_condition()
                    ].images[i].imgID -= 1
        from celer_sight_ai.core.image_button_handler import get_button_positions

        # order proxy items by the widget id number
        proxy_items = sorted(
            proxy_items,
            key=lambda x: x.widget().ButtonHolder.image_number,
            reverse=False,
        )
        max_imgs = len(
            self.MainWindow.DH.BLobj.groups["default"]
            .conds[self.MainWindow.DH.BLobj.get_current_condition()]
            .images
        )
        # TODO this function needs to be the same as in setupbuttons
        maxNumberOfButtons = max_imgs + 100
        positions = [
            (i, j)
            for i in range(
                int(maxNumberOfButtons / self.MainWindow.myButtonHandler.num_elem_width)
                + 10
            )
            for j in range(self.MainWindow.myButtonHandler.num_elem_width)
        ]
        valuesToSkip = list(range(0, self.image_number))
        values = list(range(0, len(proxy_items)))
        for position, value in zip(positions, values):
            if value in valuesToSkip:
                continue
            proxy_items[value].setPos(
                int((position[1]) * 125) + 10, int((position[0] * 125) + 10)
            )

    def deleteCurrentImage(
        self,
        reload_image=False,
        group_name=None,
        treatment_name=None,
        image_number=None,
        delete_remote=False,  # deletes the remote image as well, requires the image to be remote
    ):
        """
        It deletes the image from the data structure, and then it changes the ID number of all the other
        images in the GUI, and then it loads the mask of the previous image
        """

        if group_name is None:
            group_name = "default"
        if treatment_name is None:
            # get current treatment
            treatment_name = self.MainWindow.DH.BLobj.get_current_condition()
        if image_number is None:
            image_number = self.ButtonHolder.image_number
        # if the current imagenumber is the same one as the image, refresh always
        if (
            self.ButtonHolder.image_number
            == self.MainWindow.DH.BLobj.get_current_image_number()
        ):
            reload_image = True

        if delete_remote:
            # check if image is remote
            try:
                if self.MainWindow.DH.BLobj.get_image_object_by_uuid(
                    self.ButtonHolder.image_uuid
                ).is_remote():
                    config.client.delete_remote_image(self.ButtonHolder.image_uuid)
            except Exception as e:
                logger.error(f"Error deleting remote image: {e}")

        # remove button from visible buttons
        self.MainWindow.images_preview_graphicsview.visible_buttons.pop(
            self.MainWindow.images_preview_graphicsview.visible_buttons.index(
                self.ButtonHolder
            )
        )

        # remove image object from data handler
        self.MainWindow.DH.BLobj.groups["default"].conds[treatment_name].deleteImage(
            image_number
        )

        # Substract 1 from the button id all larger number buttons
        self.MainWindow.images_preview_graphicsview.substract_from_all_buttons(
            self.ButtonHolder.image_number
        )

        self.deleteLater()  # delete the button widget
        # self.MainWindow.images_preview_graphicsview.clear_out_visible_buttons()
        self.MainWindow.images_preview_graphicsview.place_all_image_buttons_to_correct_positions()

        # ensure the imagenumber is within bounds.
        cn = self.MainWindow.DH.BLobj.get_current_image_number()

        if reload_image:
            if self.ButtonHolder.image_number == 0:
                self.MainWindow.load_main_scene(cn)
            else:
                self.MainWindow.load_main_scene(cn)

    def AddPixmapFromImage(self, resized_img: np.array, image_uuid: str) -> None:
        """
        Function to hundle the addiciton of the image
        """
        # if image object is a video, add a "v" to the top right
        image_object = self.MainWindow.DH.BLobj.get_image_object_by_uuid(image_uuid)
        if not image_object:
            return
        if image_object._is_video:
            # add a v to resized_img with cv2 at the top right
            import cv2

            cv2.putText(
                resized_img,
                "v",
                (resized_img.size[0] - 10, resized_img.size[1] - 30),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 0, 255),
                2,
                cv2.LINE_AA,
            )

        (
            ResizedImageQImageOn,
            ResizedImageQImageOff,
        ) = self.MainWindow.DH.BLobj.get_image_pixmap(resized_img, as_QIcon=True)
        self.ResizedImageQPixMapOn = QtGui.QPixmap.fromImage(ResizedImageQImageOn)
        self.ResizedImageQPixMapOff = QtGui.QPixmap.fromImage(
            ResizedImageQImageOff
        )  # Contrstated Image
        self.update()

    def contextMenuEvent(self, event):
        if self.allowContexMenu:
            action = self.contextMenu.exec(self.mapToGlobal(event.position()))

    def SetAnalysisStatus(self, Status=True):
        self._IncludedInAnalysis = Status
        self.ImageEventChanged.emit()
        print("SetAnalysisStatus emited")


if __name__ == "__main__":
    pass
