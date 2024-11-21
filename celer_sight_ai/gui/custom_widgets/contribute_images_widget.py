from PyQt6 import QtWidgets, QtCore, QtGui
from celer_sight_ai import config
import os

full_path = os.environ.get("CELER_SIGHT_AI_HOME", "")


class ContributeImagesButton(QtWidgets.QPushButton):

    # the button should be a clickable widget that only displayes the images provided for hover, pressed and normal states
    def __init__(self, parent=None, mode="partially_annotated"):
        super().__init__(parent)
        self.mode = mode
        self.icon_path = None
        self.icon_hover_path = None
        self.icon_pressed_path = None
        self.original_size_w = 250

        self.ratio = 2  # zoom amount
        self.pixmap = None
        # yellow color
        self.color = (255, 255, 0)
        self.uncheck_color = tuple([i // 2 for i in self.color])
        if self.mode == "partially_annotated":
            self.icon_path = os.path.join(
                full_path, "data/icons/partially_annotated_infograph_off.png"
            )
            self.icon_hover_path = os.path.join(
                full_path, "data/icons/partially_annotated_infograph.png"
            )
            self.icon_pressed_path = os.path.join(
                full_path, "data/icons/partially_annotated_infograph_on.png"
            )
        else:
            self.icon_path = os.path.join(
                full_path, "data/icons/fully_annotated_infograph_off.png"
            )
            self.icon_hover_path = os.path.join(
                full_path, "data/icons/fully_annotated_infograph.png"
            )
            self.icon_pressed_path = os.path.join(
                full_path, "data/icons/fully_annotated_infograph_on.png"
            )
        # read image dimentions and create aspect ratio to fit the button
        import cv2

        img_shape = cv2.imread(self.icon_path).shape
        self.aspect_ratio = img_shape[1] / img_shape[0]
        self.original_size_h = int(self.original_size_w / self.aspect_ratio)
        self.setFixedSize(self.original_size_w, self.original_size_h)
        self.setStyleSheet(
            """
            border: 0px;
            background-color: transparent;
            """
        )
        self.setImageAsIcon(self.icon_path)
        self.setupUi()
        self.installEventFilter(self)

    def setupUi(self):
        self.setCheckable(True)
        self.setText("")
        # set the button icon

        # set the button tool tip
        self.setToolTip("Contribute partially annotated images")

    def eventFilter(self, obj, event):
        if obj == self:
            if event.type() == QtCore.QEvent.Type.Enter:
                self.hoverEnterEvent(event)
            elif event.type() == QtCore.QEvent.Type.Leave:
                self.hoverLeaveEvent(event)
            # if clicked set as checked
            if event.type() == QtCore.QEvent.Type.MouseButtonPress:
                self.setChecked(True)
        return super().eventFilter(obj, event)

    def hoverEnterEvent(self, event):
        # set the button icon
        if not self.isChecked():
            self.setImageAsIcon(self.icon_hover_path)

    def setImageAsIcon(self, path=None):
        if path == None:
            if self.isChecked():
                path = self.icon_pressed_path
            # if hover
            elif self.underMouse():
                path = self.icon_hover_path
            else:
                path = self.icon_path
        self.pixmap = QtGui.QPixmap(path)
        self.pixmap.setDevicePixelRatio(self.ratio)
        self.pixmap.scaledToWidth(
            self.original_size_w, QtCore.Qt.TransformationMode.SmoothTransformation
        )
        self.setIcon(QtGui.QIcon(self.pixmap))
        self.setIconSize(self.size())

    def hoverLeaveEvent(self, event):
        # set the button icon
        if not self.isChecked():
            self.setImageAsIcon(self.icon_path)

    def setChecked(self, checked):
        super().setChecked(checked)
        if checked:
            # set the button icon
            self.setImageAsIcon(self.icon_pressed_path)
        else:
            # set the button icon
            self.setImageAsIcon(self.icon_path)


class ContributeImagesWidget(QtWidgets.QWidget):
    # create a signal to update the icon on all other buttons
    updateIcon = QtCore.pyqtSignal()

    def __init__(self, MainWindow=None, parent=None):
        super().__init__(parent)
        self.MainWindow = MainWindow
        self.setupUi()

    def setupUi(self):
        self.outer_layout = QtWidgets.QVBoxLayout(self)
        self.outer_layout.setObjectName("outer_layout")
        self.outer_layout.setContentsMargins(0, 0, 0, 0)
        self.outer_layout.setSpacing(0)
        self.outer_layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.setLayout(self.outer_layout)
        # create a central widget
        self.centralWidget = QtWidgets.QWidget(self)
        self.centralWidget.setObjectName("centralWidget")
        self.outer_layout.addWidget(self.centralWidget)
        # create the layout for the central widget
        self.gridLayout = QtWidgets.QGridLayout(self.centralWidget)
        self.gridLayout.setObjectName("gridLayout")
        # create the label for the title
        self.titleLabel = QtWidgets.QLabel(self.centralWidget)
        self.titleLabel.setObjectName("titleLabel")
        # set the title label text
        self.titleLabel.setText("My images are:")
        # add the title label to the layout
        self.gridLayout.addWidget(self.titleLabel, 0, 0, 1, 4)
        # add first button (partially annotated images)
        self.button_group = QtWidgets.QButtonGroup(self.centralWidget)
        self.partiallyAnnotatedButton = ContributeImagesButton(
            self.centralWidget, mode="partially_annotated"
        )
        self.partiallyAnnotatedButton.setObjectName("partiallyAnnotatedButton")
        self.button_group.addButton(self.partiallyAnnotatedButton)
        self.gridLayout.addWidget(self.partiallyAnnotatedButton, 1, 0, 4, 2)
        # add second button (fully annotated images)
        self.fullyAnnotatedButton = ContributeImagesButton(
            self.centralWidget, mode="fully_annotated"
        )
        self.fullyAnnotatedButton.setObjectName("fullyAnnotatedButton")
        self.button_group.addButton(self.fullyAnnotatedButton)
        self.gridLayout.addWidget(self.fullyAnnotatedButton, 1, 2, 4, 2)
        # both should be autoexclusive
        self.button_group.setExclusive(True)

        self.updateIcon.connect(self.partiallyAnnotatedButton.setImageAsIcon)
        self.updateIcon.connect(self.fullyAnnotatedButton.setImageAsIcon)

        self.partiallyAnnotatedButton.clicked.connect(lambda: self.updateIcon.emit())
        self.fullyAnnotatedButton.clicked.connect(lambda: self.updateIcon.emit())

        self.partiallyAnnotatedButton.setChecked(True)
        self.fullyAnnotatedButton.setChecked(False)

        # contribute text
        self.contribute_text = "Click here to confirm that the images are your own work and that you have the right to contribute them to the CelerSight AI project. Images contributed with the wrong category or with malicious intent will be removed, and the account suspended."

        self.accept_radio_button = QtWidgets.QRadioButton(self.centralWidget)
        self.accept_radio_button.setObjectName("accept_radio_button")
        self.accept_radio_button.setText(self.contribute_text)
        # set wrap
        self.gridLayout.addWidget(self.accept_radio_button, 5, 0, 1, 4)

        # Create accept and cancel button
        self.accept_button = QtWidgets.QPushButton(self)
        self.accept_button.setObjectName("accept_button")
        self.gridLayout.addWidget(self.accept_button, 6, 2, 1, 1)

        self.cancel_button = QtWidgets.QPushButton(self)
        self.cancel_button.setObjectName("cancel_button")
        self.gridLayout.addWidget(self.cancel_button, 6, 1, 1, 1)

        self.accept_button.setText("Accept")
        self.cancel_button.setText("Cancel")
        self.accept_button.setFixedSize(100, 30)
        self.cancel_button.setFixedSize(100, 30)

        self.setStyleSheet(
            """
            QRadioButton{
                font-size: 10px;
                margin-left: 10px;
                margin-right: 10px;
            }
            QRadioButton::indicator {
                width: 13px;
                height: 13px;
                margin-right: 5px;
            }
            #accept_button{
                font-weight: bold;
                font-size: 14px;
            }
            #cancel_button{
                font-weight: bold;
                font-size: 14px;
            }
            #titleLabel{
                font-size: 13px;
            }
            #centralWidget{
                background-color: rgb(40,40,40);
                border-bottom-left-radius: 10px;
                border-bottom-right-radius: 10px;
            }
            #accept_button{
                color: rgb(90,185,90);
                background-color: rgb(20,60,20);
                border-radius: 5px;
            }
            #accept_button:hover{
                color: rgb(100,255,100);
                background-color: rgb(0,90,0);
                border-radius: 5px;
                border: 2px solid rgb(0,100,0);
            }
            #cancel_button{
                color: rgb(185,90,90);
                background-color: rgb(40,20,20);
                border-radius: 5px;
            }
            #cancel_button:hover{
                color: rgb(235,100,100);
                background-color: rgb(80,0,0);
                border-radius: 5px;
            }           

        """
        )
        from celer_sight_ai.gui.custom_widgets.category_and_contribution_widgets import (
            DialogWidgetTitleHat,
        )

        self.title_hat = DialogWidgetTitleHat("Data for Model Training", self)
        self.title_hat.setObjectName("title_hat")
        self.title_hat.show()

        # set minimum dimentions
        self.title_hat.setMinimumWidth(530)
        self.title_hat.setMinimumHeight(465)
        self.title_hat.setMaximumWidth(530)
        if self.parent().parent():
            # center on the parent widget
            self.title_hat.move(
                self.parent().parent().geometry().center()
                - self.title_hat.geometry().center()
            )

        # set window as transparent
        self.setWindowFlags(QtCore.Qt.WindowType.FramelessWindowHint)
        self.cancel_button.clicked.connect(lambda: self.title_hat.close())
        self.accept_button.clicked.connect(lambda: self.on_accept_button_clicked())

    def on_accept_button_clicked(self):
        # check if user has accepted the terms
        if self.accept_radio_button.isChecked():
            # if yes, close the window
            # start sending images to server
            if self.partiallyAnnotatedButton.isChecked():
                state = "partially_annotated"
            elif self.fullyAnnotatedButton.isChecked():
                state = "fully_annotated"
            else:
                state = None
            self.MainWindow.sendAnnotatedImagesToServer(
                force=True, with_dialog=True, state=state
            )
            self.title_hat.close()
        else:
            config.global_signals.errorSignal.emit(
                "Please accept the terms to continue"
            )
            return

    def resizeEvent(self, event):
        # make sure that the self.contribute_tex is wrapped
        if hasattr(self, "accept_radio_button"):
            self.accept_radio_button.setText(
                self.wrap_text(self.contribute_text, self.width() - 60)
            )

    def wrap_text(self, text, max_width):
        # calulate actual width of the text
        font = self.accept_radio_button.font()
        fm = QtGui.QFontMetricsF(font)
        text_width = fm.horizontalAdvance(text)
        # wrap
        if text_width > max_width:
            lines = []
            current_line = []
            # wrap
            words = text.split(" ")
            # Iterate through words, creating lines that fit the max_width
            for word in words:
                # Check if adding the new word exceeds the maximum width
                line_with_word = " ".join(current_line + [word])
                width = fm.horizontalAdvance(line_with_word)
                if width <= max_width:
                    current_line.append(word)
                else:
                    lines.append(" ".join(current_line))
                    current_line = [word]

            # Add the last line
            lines.append(" ".join(current_line))

            text = "\n".join(lines)
        return text


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = ContributeImagesWidget()
    window.show()
    app.exec()
