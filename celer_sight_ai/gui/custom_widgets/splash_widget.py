import sys

from PyQt6 import QtCore, QtGui, QtWidgets  # + QtWidgets
import logging
from celer_sight_ai import config
import os

logger = logging.getLogger(__name__)


class CustomSplashScreenWithText(QtWidgets.QSplashScreen):
    """ "
    Custom QSplashScreen with text that ignores mouse events
    This widget is the first the user sees during log in, should
    hide during when user is promped to log in
    """

    def __init__(self) -> None:
        import os

        # add a pixmap with the splash screen image
        logger.info(os.environ["CELER_SIGHT_AI_HOME"])
        if not config.is_executable:
            import os
            splash_screen_image = os.path.join(
                os.environ["CELER_SIGHT_AI_HOME"],
                "data/celer_sight_icons/celer_sight_splash.png",
            )
        else:
            import os

            logger.debug("CELER SIGHT AI HOME : ", os.environ["CELER_SIGHT_AI_HOME"])

            splash_screen_image = os.path.join(
                os.environ["CELER_SIGHT_AI_HOME"]
                , "celer_sight_ai/data/celer_sight_icons/celer_sight_splash.png"
            )
            logger.info(f"Loading splash screen image from: {splash_screen_image}")
        my_pix = QtGui.QPixmap(splash_screen_image)
        self.x_scale = 650
        self.y_scale = 650
        my_pix = my_pix.scaledToWidth(
            self.x_scale, QtCore.Qt.TransformationMode.SmoothTransformation
        )
        self.text_position = (50, 250)  # Default position
        super().__init__(my_pix)
        self.message = ""
        self.showMessage("Loading modules...")
        self.show()

    def mousePressEvent(self, event) -> None:
        # Ignore the mouse press event to prevent the splash screen from disappearing
        pass

    def showMessage(self, message) -> None:
        # This method adds text that is displayed on top of the splash screen
        self.message = message
        # get message legth
        metrics = QtGui.QFontMetrics(self.font())
        text_width = metrics.boundingRect(message).width()
        text_height = metrics.boundingRect(message).height()

        self.text_position = (
            (self.x_scale // 2) - (text_width // 2),
            3 * (self.y_scale // 4.63) - (text_height // 2) + 10,
        )
        self.repaint()  # Ask for a repaint

    def drawContents(self, painter) -> None:
        # Call the base implementation
        super().drawContents(painter)

        # Setup the font, color, and position
        painter.setPen(QtGui.QColor(2, 0, 80))
        # font is black and 13
        painter.setFont(QtGui.QFont("Helvetica", 13))
        # Draw the message text at the specific position
        x, y = self.text_position
        # Draw the message text
        painter.drawText(int(x), int(y), self.message)


class loadingWindowAnimation(QtWidgets.QWidget):  # QtWidgets.QWidget
    """
    Loading Splash animatino before and after user log in


    Args:
        parent (MainWInodw): _description_
    """

    def __init__(self):
        super(loadingWindowAnimation, self).__init__()
        self.login_handler = self.ShowSplash()
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_DeleteOnClose)
        self.myDialog_OVER.setAttribute(QtCore.Qt.WidgetAttribute.WA_DeleteOnClose)

    def hide(self):
        self.myDialog_OVER.hide()
        # self.myDialog.hide()

    def show(self):
        self.myDialog_OVER.show()
        # self.myDialog.show()
        # self.myDialog.raise_()
        self.myDialog_OVER.raise_()

    # def eventFilter(self, source, event):
    #     if event.type() == QtCore.QEvent.Type.FocusIn:
    #         # if source == self.myDialog:
    #         self.myDialog_OVER.raise_()
    #     if event.type() == QtCore.QEvent.Type.FocusIn:
    #         # if source == self.myDialog:
    #         self.myDialog_OVER.raise_()
    #     return super(loadingWindowAnimation, self).eventFilter(source, event)

    def ShowSplash(self):
        splash_screen_image = (
            "celer_sight_ai/data/celer_sight_icons/celer_sight_splash.png"
        )
        # add a pixmap with the splash screen image
        my_pix = QtGui.QPixmap(splash_screen_image)
        my_pix = my_pix.scaled(600, 600, QtCore.Qt.AspectRatioMode.KeepAspectRatio)
        self.myDialog_OVER = CustomSplashScreenWithText(my_pix)  # QtWidgets.QDialog()
        self.myDialog_OVER.installEventFilter(self.myDialog_OVER)
        nS = QtCore.QSize(56, 36)
        self.closebtn = QtWidgets.QPushButton("closetbn")
        self.closebtn.setText("")
        # self.closebtn.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)
        self.closebtn.setObjectName("mainCloseBtn")
        self.closebtn.setMinimumSize(nS)
        self.closebtn.clicked.connect(lambda: self.closeWindow_())
        self.closebtn.setStyleSheet(
            """
            QPushButton{
                border: 0px solid;
                border-image: url("celer_sight_ai/data/icons/cursor/CLOSE_NORMAL.png") 0 0 0 0 stretch stretch;
            background-repeat: no-repeat;
            background-position: center;
            background-color:rgba(0,0,0,100);
            border-radius: 4px;
                }
            QPushButton:hover{border-image: url("celer_sight_ai/data/icons/cursor/CLOSE_HOVER.png") 0 0 0 0 stretch stretch;}
            """
        )
        self.myDialog_OVER.setWindowFlag(QtCore.Qt.WindowType.FramelessWindowHint)
        self.myLabel = LabelWidget("Downloading: 18%")
        fnt = QtGui.QFont("Helvetica", 24)
        fnt.setBold(True)
        self.myLabel.setFont(fnt)
        self.myLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft)
        self.myLabel.setParent(self)
        self.closebtn.setParent(self.myDialog_OVER)
        self.myLabel.setStyleSheet(
            """QLabel{background-color: none;
            color:rgba(100,255,0,255);
            background-color:rgba(222,0,0,222);
            background:transparent;}
        """
        )
        # self.myLabel.setGraphicsEffect(self.shadow)

        qtRectangle = self.myDialog_OVER.frameGeometry()
        centerPoint = QtGui.QGuiApplication.primaryScreen().availableGeometry().center()
        # qtRectangle.moveCenter(centerPoint)
        # self.myDialog.move(qtRectangle.topLeft())
        self.myLabel.show()
        print(self.myLabel.width() / 2)
        self.myLabel.move(
            QtCore.QPoint(
                int(qtRectangle.topLeft().x() - self.myLabel.width() / 2),
                int(qtRectangle.topLeft().y() + 510),
            )
        )
        self.closebtn.move(
            QtCore.QPoint(
                int(qtRectangle.topLeft().x() + 525),
                int(qtRectangle.topLeft().y() + 90),
            )
        )
        self.myLabel.raise_()
        # self.mediaPlayer.play()
        self.myDialog_OVER.show()
        self.myDialog_OVER.raise_()
        self.setMainText("Checking for Updates.")
        QtWidgets.QApplication.processEvents()

        return

    def closeWindow_(self):
        self.myDialog_OVER.close()
        # self.myDialog.close()
        sys.exit()
        return

    def setMainText(self, text):
        # sets the text on the bottom part of the animated loading

        self.myLabel.setText(text)
        # self.myLabel.hide()
        QtWidgets.QApplication.processEvents()
        xPos = self.myDialog_OVER.pos().x()
        yPos = self.myDialog_OVER.pos().y()
        width = self.myDialog_OVER.width()
        height = self.myDialog_OVER.width()
        labelWidth = self.myLabel.fontMetrics().boundingRect(text).width()

        print("mocing to pos: ", xPos + ((width - labelWidth) / 2))
        print(xPos)
        print(width)
        print(labelWidth)

        self.myLabel.move(
            QtCore.QPoint(
                int(xPos + ((width - labelWidth) / 2) - (30)),
                int(yPos + int(height * 0.8) - 50),
            )
        )
        self.myLabel.show()
        self.myLabel.raise_()
        QtWidgets.QApplication.processEvents()
        return

    def startAnimation(self):
        self.movie.start()

    # Stop Animation(According to need)
    def stopAnimation(self):
        self.movie.stop()


class LabelWidget(QtWidgets.QLabel):
    def __init__(self, text):
        super().__init__(text, parent=None)
        self.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.setText(text)
        print("widget loaded")


if __name__ == "__main__":
    pass
