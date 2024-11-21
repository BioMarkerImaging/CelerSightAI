# custom pushbutton

from PyQt6 import QtGui, QtCore, QtWidgets
import os
import logging

logger = logging.getLogger(__name__)


class RepeatTimer(QtCore.QTimer):
    timeoutCount = QtCore.pyqtSignal(int)
    endRepeat = QtCore.pyqtSignal()
    timeoutNormal = QtCore.pyqtSignal()

    def __init__(self, numberOfRepeats=1, delay=10):
        QtCore.QTimer.__init__(self)
        self.__numberOfRepeats = 1
        self.numberOfRepeats = numberOfRepeats
        self.delay = delay
        self.__internalCounter = 0
        self.timeout.connect(self.__eval)

    @property
    def delay(self):
        return self.__delay

    @delay.setter
    def delay(self, value):
        if value >= 0 and type(value).__name__ == "int":
            self.__delay = value
            self.setInterval(value)

    @property
    def numberOfRepeats(self):
        return self.__numberOfRepeats

    @numberOfRepeats.setter
    def numberOfRepeats(self, value):
        if value >= 0 and type(value).__name__ == "int":
            self.__numberOfRepeats = value

    def __eval(self):
        if self.__internalCounter >= self.__numberOfRepeats - 1:
            self.stop()

            self.endRepeat.emit()
            # self.timeoutCount.emit(self.__internalCounter)
            self.__internalCounter = 0
        else:
            self.__internalCounter += 1

            self.timeoutCount.emit(self.__internalCounter)

    def force_stop(self):
        self.stop()
        self.endRepeat.emit()
        self.__internalCounter = 0

        QtWidgets.QApplication.processEvents


class AnimationCursor(QtGui.QCursor):
    """
    Custom cursor animation widget
    """

    def __init__(self, MainWindow=None):
        QtGui.QCursor.__init__(self)
        # print("NEWWW CURSORRRRRRRR")
        self.MainWindow = MainWindow
        self.__frames = None
        self.__basePath = None
        self.__framesPath = None
        self.__framesSize = None
        self.__numberOfFrames = None
        self._timer = RepeatTimer(10, 100)
        # self.setMouseTracking(True)
        self._timer.timeoutCount.connect(self._setFrame)
        self._timer.timeoutNormal.connect(self.RestoreCursor)

        # self.setIconSize(QtCore.QSize(200, 200))
        # self.installEventFilter(self)

    def natural_keys(self, text):
        import re

        return [self.atoi(c) for c in re.split(r"(\d+)", text)]

    def atoi(self, text):
        return int(text) if text.isdigit() else text

    def list_files(self, path):
        files = [
            f
            for f in os.listdir(path)
            if not f.startswith(".")
            and os.path.splitext(f)[1].lower()
            in (".jpg", ".jpeg", ".TIF", ".tiff", ".tif", ".png", ".PNG")
        ]
        files.sort(key=self.natural_keys)
        return files

    def RestoreCursor(self):
        self.MainWindow.viewer.setCursor(
            QtGui.QCursor(QtCore.Qt.CursorShape.ArrowCursor)
        )
        self.MainWindow.MainWindow.setCursor(
            QtGui.QCursor(QtCore.Qt.CursorShape.ArrowCursor)
        )

    def setFrames(self, basePath=None, frames=[], resizeButton=True, speed=17):
        self.__frames = self._convertFrame(basePath, frames, resizeButton, speed)

    def _convertFrame(self, basePath, frames=[], resizeButton=True, speed=17):
        processed = []
        for i, f in enumerate(frames):
            # print(basePath+"/"+f)
            pix = QtGui.QPixmap(basePath + "/" + f)
            if i == 0:
                self.__frameSize = pix.size()
            im = pix  # QtGui.QIcon(pix)
            processed.append(im)
        self.__numberOfFrames = len(processed)
        self.__basePath = basePath
        self.__framesPath = frames
        self._timer.numberOfRepeats = self.__numberOfFrames
        self._timer.delay = speed

        return processed

    def _setFrame(self, index=0):
        # print(len(self.__frames))
        if (
            self.__frames and self.__frameSize and index <= (self.__numberOfFrames - 1)
        ) == True:
            # print("setting frame! ", self.__frames[index])
            self.MainWindow.viewer.setCursor(QtGui.QCursor(self.__frames[index]))
            #   self.__frames[index])
            # self.setIconSize(self.__frameSize)

    def playAnim(self):
        #
        # Loading Animation 1
        #

        baseP = "data/icons/Tail800"
        # frames = os.listdir(baseP)
        frames = self.list_files(baseP)
        # print(frames)
        self.setFrames(baseP, frames)
        self._timer.start()

    def eventFilter(self, source, event):
        # if event.type() == QtCore.QEvent.Type.HoverEnter:
        #     if self.__frames != None:
        #         self.playAnim()
        return super(AnimationCursor, self).eventFilter(source, event)


class csDesign_Button(QtWidgets.QPushButton):
    def __init__(self, parent=None):
        QtWidgets.QPushButton.__init__(self, parent)
        self.pngImageOn = None
        self.pngImageOff = None
        self.pngImageODisabled = None
        self.pngImageHover = None

        self.installEventFilter(self)
        self.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))

    def eventFilter(self, source, event):
        if event.type() == QtCore.QEvent.Type.HoverEnter:
            if self.__frames != None:
                self.playAnim()
                return super(Animation_Button, self).eventFilter(source, event)

        # check shadows and update
        if event.type() == QtCore.QEvent.Type.HoverEnter:
            self.CheckStateShadow(event.type())
        if event.type() == QtCore.QEvent.Type.HoverLeave:
            self.CheckStateShadow(event.type())
        if event.type() == QtCore.QEvent.Type.MouseButtonPress:
            self.CheckStateShadow(event.type())
        return super(Animation_Button, self).eventFilter(source, event)


class Animation_Button(QtWidgets.QPushButton):
    def __init__(self, parent=None, textLabel="new"):
        QtWidgets.QPushButton.__init__(self, parent)
        self.__frames = None
        self.__basePath = None
        self.__framesPath = None
        self.__framesSize = None
        self.__numberOfFrames = None
        self._timer = RepeatTimer(10, 100)
        self.setMouseTracking(True)
        self._timer.timeoutCount.connect(self._setFrame)
        self.installEventFilter(self)
        self.BR = 5  # blur radius
        self.xo = 3  # xoffset
        self.yo = 3  # yoffset
        self.setStyleSheet(
            """
            border-radius:5px;
            """
        )
        self.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.neurlaNetButton = False
        # layout that holds the label and the button
        self.horLayout = QtWidgets.QHBoxLayout(self)
        self.labelText = QtWidgets.QLabel(self)
        self.labelText.setText(textLabel)

        # removed for now
        # self.animIcon = QtWidgets.QPushButton(self)
        # self.animIcon.setAttribute(QtCore.Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        # self.horLayout.addWidget(self.animIcon)

        self.horLayout.addWidget(self.labelText)
        self.horLayout.setContentsMargins(2, 2, 2, 2)
        self.horLayout.setSpacing(0)
        self.horLayout.setContentsMargins(0, 0, 0, 0)
        self.labelText.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignHCenter | QtCore.Qt.AlignmentFlag.AlignVCenter
        )
        self.labelText.setStyleSheet(
            """padding-left:0px;
                padding-right:10px;
                color:white;
                background-color:rgba(0,0,0,0);
                font-size:12px;
                font-weight:600;
                font-family:Lato Bold;
                """
        )
        # self.animIcon.stackUnder(self.labelText)
        # self.animIcon.setStyleSheet("QPushButton{background-color:rgba(0,0,0,0)}")
        # self.labelText.stackUnder(self.animIcon)

        # self.CheckStateShadow(None)
        self.labelText.raise_()
        self.origR = None
        self.origG = None
        self.origB = None

        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_StyledBackground, True)

    def setIconSize(self, *args, **kwargs):
        return
        # self.animIcon.setIconSize(*args, **kwargs)

    def setIcon(self, *args, **kwargs):
        return
        # self.animIcon.setIcon(*args, **kwargs)

    def setText(self, *args, **kwargs):
        self.labelText.setText(*args, **kwargs)

    def setFont(self, *args, **kwargs):
        self.labelText.setFont(*args, **kwargs)

    def makeNeuralNetBtn(self):
        self.neurlaNetButton = True
        self.labelForNeuralNetState = QtWidgets.QLabel(self)
        self.labelForNeuralNetState.setParent(self)
        self.labelForNeuralNetState.move(10, 10)
        self.labelForNeuralNetState.setText("P")
        self.labelForNeuralNetState.setStyleSheet(
            """   
            background-color: rgba(0,0,0,0);
            color: rgb(150,150,150);
            """
        )

    def setFrames(self, basePath=None, frames=[], resizeButton=True, speed=17):
        self.__frames = self._convertFrame(basePath, frames, resizeButton, speed)
        self._setFrame(0)

    def _convertFrame(self, basePath, frames=[], resizeButton=True, speed=17):
        processed = []
        for i, f in enumerate(frames):
            # print(basePath+"/"+f)
            pix = QtGui.QPixmap(basePath + "/" + f)
            if i == 0:
                self.__frameSize = pix.size()
            im = QtGui.QIcon(pix)
            processed.append(im)
        self.__numberOfFrames = len(processed)
        self.__basePath = basePath
        self.__framesPath = frames
        self._timer.numberOfRepeats = self.__numberOfFrames
        self._timer.delay = speed

        return processed

    # def convertToNeuralLocalRemoteSettings(self):
    #     self.settingsBtn =  QtWidgets.QPushButton(self)
    #     self.settingsBtn.setParent(self)
    #     self.settingsBtn.move(95,5) #120
    #     self.settingsBtn.setStyleSheet("""
    #                                     QPushButton{
    #                                     border-width: 2px;
    #                                     border-color: rgba(0,0,0,255);
    #                                     border-style: solid;
    #                                     border-radius: 3;
    #                                     }

    #                                     """)
    #     icon_RNAi = QtGui.QIcon()
    #     icon_RNAi.addPixmap(QtGui.QPixmap('data/icons/settingsForMaskGeneration.png'))
    #     self.settingsBtn.setIcon(icon_RNAi)
    #     self.settingsBtn.setIconSize(QtCore.QSize(20, 20))
    #     self.settingsBtn.setMinimumSize(QtCore.QSize(15, 15))
    #     self.settingsBtn.setMaximumSize(QtCore.QSize(15, 15))

    def _setFrame(self, index=0):
        # print(len(self.__frames))
        if (
            self.__frames and self.__frameSize and index <= (self.__numberOfFrames - 1)
        ) == True:
            self.animIcon.setIcon(self.__frames[index])
            # self.setIconSize(self.__frameSize)

    def playAnim(self):
        # play only on windows os
        # if os.name == "nt":
        #     self._timer.start()
        return

    def dimColor(self):
        # QtWidgets.QApplication.processEvents()

        color = self.palette().color(QtGui.QPalette.ColorRole.Dark)
        if isinstance(self.origR, type(None)):
            self.origR = color.red()
            self.origG = color.green()
            self.origB = color.blue()
        div = 2
        # p = self.palette()
        fR = str(int(self.origR / div))
        fG = str(int(self.origG / div))
        fB = str(int(self.origB / div))
        self.setStyleSheet(
            """
            border-radius:5px;
            background-color:rgb(75,75,75);
            """
        )
        self.labelText.setStyleSheet("""color: rgb(110,110,110);""")

    def normColor(self):
        color = self.palette().color(QtGui.QPalette.ColorRole.Dark)
        QtWidgets.QApplication.processEvents()
        if self.isEnabled():
            if isinstance(self.origR, type(None)):
                self.origR = color.red()
                self.origG = color.green()
                self.origB = color.blue()
            # p = self.palette()
            fR = str(int(self.origR))
            fG = str(int(self.origG))
            fB = str(int(self.origB))
        self.setStyleSheet(
            """
                           border-radius:5px;
                           background-color:rgb(45,45,45);
                           """
        )
        self.labelText.setStyleSheet(
            """
                                     color: rgb(255,255,255);
                                     """
        )

    def hightLightColor(self):
        color = self.palette().color(QtGui.QPalette.ColorRole.Dark)
        QtWidgets.QApplication.processEvents()

        if self.isEnabled():
            if isinstance(self.origR, type(None)):
                self.origR = color.red()
                self.origG = color.green()
                self.origB = color.blue()
            div = 2
            # p = self.palette()
            fR = str(min(255, int(self.origR * div)))
            fG = str(min(int(self.origG * div), 255))
            fB = str(min(255, int(self.origB * div)))
        self.setStyleSheet("""background-color:rgb(105,105,105);""")

    def setEnabled_(self, val):
        if val == False:
            self.dimColor()
        else:
            self.normColor()
        self.setEnabled(val)

    def eventFilter(self, source, event):
        return super(Animation_Button, self).eventFilter(source, event)


class Animation_Button_TAB(QtWidgets.QPushButton):
    def __init__(self, myID=0, parent=None):
        QtWidgets.QPushButton.__init__(self, parent)
        self.__frames = None
        self.myID = myID
        self.__basePath = None
        self.__framesPath = None
        self.__framesSize = None
        self.__numberOfFrames = None
        self._timer = RepeatTimer(10, 100)
        self.setMouseTracking(True)
        self._timer.timeoutCount.connect(self._setFrame)
        self.installEventFilter(self)
        self.CheckStateShadow(None)
        self.BR = 5  # blur radius
        self.xo = 3  # xoffset
        self.yo = 3  # yoffset

    def setInitIcon(self, iconInit):
        self.iconInit = iconInit
        self.setIcon(iconInit)

    def checkCheckState(self):
        if self.isChecked() == False:
            self.setIcon(self.iconInit)
        else:
            pass

    def setFrames(self, basePath=None, frames=[], resizeButton=True, speed=17):
        self.__frames = self._convertFrame(basePath, frames, resizeButton, speed)
        self._setFrame(0)

    def _convertFrame(self, basePath, frames=[], resizeButton=True, speed=17):
        processed = []
        for i, f in enumerate(frames):
            # print(basePath+"/"+f)
            pix = QtGui.QPixmap(basePath + "/" + f)
            if i == 0:
                self.__frameSize = pix.size()
            im = QtGui.QIcon(pix)
            processed.append(im)
        self.__numberOfFrames = len(processed)
        self.__basePath = basePath
        self.__framesPath = frames
        self._timer.numberOfRepeats = self.__numberOfFrames
        self._timer.delay = speed

        return processed

    # def convertToNeuralLocalRemoteSettings(self):
    #     self.settingsBtn =  QtWidgets.QPushButton(self)
    #     self.settingsBtn.setParent(self)
    #     self.settingsBtn.move(95,5) #120
    #     self.settingsBtn.setStyleSheet("""
    #                                     QPushButton{
    #                                     border-width: 2px;
    #                                     border-color: rgba(0,0,0,255);
    #                                     border-style: solid;
    #                                     border-radius: 3;
    #                                     }

    #                                     """)
    #     icon_RNAi = QtGui.QIcon()
    #     icon_RNAi.addPixmap(QtGui.QPixmap('data/icons/settingsForMaskGeneration.png'))
    #     self.settingsBtn.setIcon(icon_RNAi)
    #     self.settingsBtn.setIconSize(QtCore.QSize(20, 20))
    #     self.settingsBtn.setMinimumSize(QtCore.QSize(15, 15))
    #     self.settingsBtn.setMaximumSize(QtCore.QSize(15, 15))

    def _setFrame(self, index=0):
        # print(len(self.__frames))
        if (
            self.__frames and self.__frameSize and index <= (self.__numberOfFrames - 1)
        ) == True:
            self.setIcon(self.__frames[index])
            # self.setIconSize(self.__frameSize)

    def playAnim(self):
        self._timer.start()

    def CheckStateShadow(self, state):
        if state == QtCore.QEvent.Type.HoverEnter and self.isEnabled():
            self.BR = 40  # blur radius
            self.xo = -5  # xoffset
            self.yo = 3  # yoffset
            self.colorGUI = QtGui.QColor(0, 0, 0, 180)
            print("hover enter")
        elif state == QtCore.QEvent.Type.MouseButtonPress and self.isEnabled():
            self.BR = 20  # blur radius
            self.xo = -5  # xoffset
            self.yo = 3  # yoffset
            self.colorGUI = QtGui.QColor(0, 0, 0, 130)
        elif (
            state == QtCore.QEvent.Type.MouseButtonRelease
            and self.isEnabled()
            and self.isUnderMouse()
        ):
            self.BR = 20  # blur radius
            self.xo = -5  # xoffset
            self.yo = 3  # yoffset
            self.colorGUI = QtGui.QColor(0, 0, 0, 180)

        elif (
            state == QtCore.QEvent.Type.HoverLeave
            and not self.isEnabled
            and self.isChecked()
        ):
            self.BR = 20  # blur radius
            self.xo = -5  # xoffset
            self.yo = 3  # yoffset
            self.colorGUI = QtGui.QColor(0, 0, 0, 100)
        elif not self.isEnabled():
            self.BR = 10  # blur radius
            self.xo = 0  # xoffset
            self.yo = 0  # yoffset
            self.colorGUI = QtGui.QColor(0, 0, 0, 80)
        else:  # normal
            self.BR = 10  # blur radius
            self.xo = 0  # xoffset
            self.yo = 0  # yoffset
            self.colorGUI = QtGui.QColor(0, 0, 0, 80)
        shadow = QtWidgets.QGraphicsDropShadowEffect(
            blurRadius=self.BR, xOffset=self.xo, yOffset=self.yo, color=self.colorGUI
        )
        self.setGraphicsEffect(shadow)

    def triggerButtonAnimation(self):
        self.playAnim()
        from celer_sight_ai import config

        config.global_signals.tabChangedbtn.emit(self.myID)

    def eventFilter(self, source, event):
        if event.type() == QtCore.QEvent.Type.MouseButtonPress:
            if event.button() == QtCore.Qt.MouseButton.LeftButton:
                if self.__frames != None:
                    self.playAnim()
                    from celer_sight_ai import config

                    config.global_signals.tabChangedbtn.emit(self.myID)
                    return super(Animation_Button_TAB, self).eventFilter(source, event)

        # check shadows and update
        if event.type() == QtCore.QEvent.Type.HoverEnter:
            self.CheckStateShadow(event.type())
        if event.type() == QtCore.QEvent.Type.HoverLeave:
            self.CheckStateShadow(event.type())
        if event.type() == QtCore.QEvent.Type.MouseButtonPress:
            self.CheckStateShadow(event.type())
        return super(Animation_Button_TAB, self).eventFilter(source, event)


class mainButtonsLeftScreen(QtWidgets.QPushButton):
    def __init__(
        self,
        parent: QtWidgets.QWidget = None,
    ):
        super(mainButtonsLeftScreen, self).__init__(parent)
        self.setParent(parent)
        self._icon_normal = None
        self._icon_over = None
        self._icon_checked = None
        self._icon_checked_over = None

        self.setAutoExclusive(True)
        self.setCheckable(True)
        self.setFlat(True)
        self.clicked.connect(lambda : self.changeIcons())
        self.enterEvent = self.enterEventOverride
        self.leaveEvent = self.leaveEventOverride
        self.setStyleSheet(
            """
                           QPushButton{
                               border-width: 0px;
                               background-color: rgba(0,0,0,0);
                               border-radius: 0px;
                                margin: 4px;
                           }
                           
                           """
        )

    def setIcons(
        self,
        icon_non_selection_non_hover: QtGui.QIcon = None,
        icon_selection_non_hover: QtGui.QIcon = None,
        icon_non_selection_hover: QtGui.QIcon = None,
    ):
        icon_size = QtCore.QSize(35, 35)
        button_size = QtCore.QSize(44, 44)
        self._icon_normal = icon_non_selection_non_hover
        self._icon_over = icon_non_selection_hover
        self._icon_checked = icon_selection_non_hover
        self.setIcon(self._icon_normal)
        self.setIconSize(icon_size)
        self.setMinimumSize(button_size)
        self.setMaximumSize(button_size)

    def enterEventOverride(self, event):
        self.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        if self._icon_over and not self.isChecked():
            self.setIcon(self._icon_over)
        return super(mainButtonsLeftScreen, self).enterEvent(event)

    def leaveEventOverride(self, event):
        self.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.ArrowCursor))
        if self._icon_normal and not self.isChecked():
            self.setIcon(self._icon_normal)
        return super(mainButtonsLeftScreen, self).leaveEvent(event)

    def changeIcons(self):
        # make sure we are auto exclusive between HomeButtonMain , InfoButtonMain and SettingsButtonMain,
        # or even better, for all children of top_menus

        for item in self.parent().children():
            if isinstance(item, mainButtonsLeftScreen):
                if item != self:
                    item.setChecked(False)
                    item.setIcon(item._icon_normal)
        print(self.isChecked())
        if self.isChecked():
            self.setIcon(self._icon_checked)
        else:
            self.setIcon(self._icon_normal)


class QuickToolButton(QtWidgets.QPushButton):
    MeUpdated = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        QtWidgets.QPushButton.__init__(self, parent)
        self.initialMinimumSize = QtCore.QSize(30, 30)
        self.zoomedSize = QtCore.QSize(33, 33)
        self.checkedsize = QtCore.QSize(35, 35)
        self.ParAnimation = QtCore.QParallelAnimationGroup()
        self.setShadowNormal()
        self.installEventFilter(self)
        self.MainWindowRef = None
        self.viewerRef = None

    def setInitIconSize(self, Size):
        self.initIconSize = Size
        self.setIconSize(Size)
        self.iconSizeMax = QtCore.QSize(
            int(Size.width() * 1.3), int(Size.height() * 1.3)
        )
        self.setStyleSheet(
            """background-color:rgba(63,63,63,255);
                            """
        )

        # self.zoomedSize =Size.scale(int(Size.width()*1.4), int(Size.width()*1.4),QtCore.Qt.AspectRatioMode.KeepAspectRatio)
        # self.checkedsize = Size.scale(int(Size.width()*1.2), int(Size.width()*1.2),QtCore.Qt.AspectRatioMode.KeepAspectRatio)

    def eventFilter(self, source, event):
        if type(event) == QtWidgets.QWidgetItem:
            return True
        if hasattr(self, "iconSizeMax"):
            if event.type() == QtCore.QEvent.Type.HoverEnter:
                self.onFocusAnimation(animState="hoverEnter")
            if event.type() == QtCore.QEvent.Type.HoverLeave:
                self.onFocusAnimation(animState="hoverLeave")
                if hasattr(self, "viewerRef"):
                    if self.viewerRef != None:
                        self.viewerRef.setFocus()

        return super(QuickToolButton, self).eventFilter(source, event)

    def setIconCustom(self, path=None):
        icon = QtGui.QIcon()
        icon.addPixmap(
            QtGui.QPixmap(path), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off
        )
        self.setIcon(icon)
        # self.setIconSize(QtCore.QSize(20,20))

    def setAllzEqual(self):
        self.parent().pushButtonQuickToolsSelectionTool.raize_()
        self.parent().pushButtonQuickToolsRemoveSelectionTool.raize_()
        self.parent().pushButtonQuickToolsMoveMagicBrush.raize_()
        self.parent().pushButtonQuickToolsPolygonTool.raize_()
        self.parent().pushButtonQuickToolsAutoToolBox.raize_()
        self.parent().pushButtonQuickToolsKeypoint.raize_()
        self.parent().pushButtonQuickToolsAutoSpline.raize_()

    def whenChecked(self):
        """
        When we check it run the following
        """
        pass

    def setShadowNormal(self):
        self.myShadowEffect = QtWidgets.QGraphicsDropShadowEffect()
        self.myShadowEffect.setColor(QtGui.QColor(0, 0, 0, 220))
        self.myShadowEffect.setBlurRadius(30)
        self.myShadowEffect.setOffset(0)
        self.setGraphicsEffect(self.myShadowEffect)

    def setShadowHover(self):
        self.myShadowEffect = QtWidgets.QGraphicsDropShadowEffect()
        self.myShadowEffect.setColor(QtGui.QColor(0, 0, 0, 190))
        self.myShadowEffect.setBlurRadius(50)
        self.myShadowEffect.setOffset(0)
        self.setGraphicsEffect(self.myShadowEffect)

    def setShadowPressed(self):
        self.myShadowEffect = QtWidgets.QGraphicsDropShadowEffect()
        self.myShadowEffect.setColor(QtGui.QColor(0, 0, 0, 230))
        self.myShadowEffect.setBlurRadius(15)
        self.myShadowEffect.setOffset(0)
        self.setGraphicsEffect(self.myShadowEffect)

    def onFocusAnimation(self, animState="hoverEnter"):
        """
        runs when widget gains focus
        """
        self.raise_()
        self.ParAnimation.stop()
        AnimationDuration = 600

        self.ParAnimation = QtCore.QParallelAnimationGroup()

        self.animminimumSize = QtCore.QPropertyAnimation(self, b"minimumSize")
        self.myShadowAnimationBlurRadius = QtCore.QPropertyAnimation(
            self.myShadowEffect, b"blurRadius"
        )
        self.myShadowAnimationColor = QtCore.QPropertyAnimation(
            self.myShadowEffect, b"color"
        )
        self.iconSizeAnimation = QtCore.QPropertyAnimation(self, b"iconSize")

        self.animminimumSize.setStartValue(
            QtCore.QSize(self.width(), self.height())
        )  # the size we are on now

        if animState == "hoverEnter":
            self.animminimumSize.setEndValue(self.zoomedSize)
            self.myShadowAnimationBlurRadius.setStartValue(30)
            self.myShadowAnimationBlurRadius.setEndValue(50)
            self.myShadowAnimationColor.setStartValue(QtGui.QColor(0, 0, 0, 220))
            self.myShadowAnimationColor.setEndValue(QtGui.QColor(0, 0, 0, 190))
            self.iconSizeAnimation.setStartValue(self.iconSizeMax)
            self.iconSizeAnimation.setEndValue(self.initIconSize)

            curve = QtCore.QEasingCurve(QtCore.QEasingCurve.Type.OutElastic)

        elif animState == "hoverLeave":
            self.animminimumSize.setEndValue(self.initialMinimumSize)
            self.myShadowAnimationBlurRadius.setStartValue(50)
            self.myShadowAnimationBlurRadius.setEndValue(30)
            self.myShadowAnimationColor.setStartValue(QtGui.QColor(0, 0, 0, 190))
            self.myShadowAnimationColor.setEndValue(QtGui.QColor(0, 0, 0, 220))
            self.iconSizeAnimation.setStartValue(self.iconSizeMax)
            self.iconSizeAnimation.setEndValue(self.initIconSize)

            curve = QtCore.QEasingCurve(QtCore.QEasingCurve.Type.OutElastic)

        elif animState == "checked":
            self.animminimumSize.setEndValue(self.checkedsize)
            self.myShadowAnimationBlurRadius.setStartValue(40)
            self.myShadowAnimationBlurRadius.setEndValue(20)
            self.myShadowAnimationColor.setStartValue(QtGui.QColor(0, 0, 0, 220))
            self.myShadowAnimationColor.setEndValue(QtGui.QColor(0, 0, 0, 230))
            self.iconSizeAnimation.setStartValue(self.initIconSize)
            self.iconSizeAnimation.setEndValue(self.iconSizeMax)

            curve = QtCore.QEasingCurve(QtCore.QEasingCurve.Type.OutElastic)

        self.animminimumSize.setDuration(AnimationDuration)
        self.myShadowAnimationBlurRadius.setDuration(AnimationDuration)
        self.myShadowAnimationColor.setDuration(AnimationDuration)
        self.iconSizeAnimation.setDuration(AnimationDuration)

        self.animminimumSize.setEasingCurve(curve)
        self.myShadowAnimationBlurRadius.setEasingCurve(curve)
        self.myShadowAnimationColor.setEasingCurve(curve)
        self.iconSizeAnimation.setEasingCurve(curve)

        self.ParAnimation.addAnimation(self.animminimumSize)
        self.ParAnimation.addAnimation(self.myShadowAnimationBlurRadius)
        self.ParAnimation.addAnimation(self.myShadowAnimationColor)
        self.ParAnimation.addAnimation(self.iconSizeAnimation)

        self.ParAnimation.start()


class TabAnimationButton(QtWidgets.QPushButton):
    def __init__(self, parent=None):
        QtWidgets.QPushButton.__init__(self, parent)
        self.__frames0 = None
        self.__frames1 = None
        self.__frames2 = None
        from celer_sight_ai import config

        self.config = config
        self.__basePath0 = None
        self.__basePath1 = None
        self.__basePath2 = None

        self.__framesPath0 = None
        self.__framesPath1 = None
        self.__framesPath2 = None

        self.__framesSize0 = None
        self.__framesSize1 = None
        self.__framesSize2 = None

        self.__numberOfFrames0 = None
        self.__numberOfFrames1 = None
        self.__numberOfFrames2 = None

        self._timer0 = RepeatTimer(10, 100)
        self._timer1 = RepeatTimer(10, 100)
        self._timer2 = RepeatTimer(10, 100)

        self.__numberOfFrames0 = 0
        self.__numberOfFrames1 = 0
        self.__numberOfFrames2 = 0

        self.setMouseTracking(True)
        self._timer0.timeoutCount.connect(self._setFrame1)
        self._timer1.timeoutCount.connect(self._setFrame2)
        self._timer2.timeoutCount.connect(self._setFrame3)

        self.installEventFilter(self)
        # self.CheckStateShadow(None)
        self.BR = 5  # blur radius
        self.xo = 3  # xoffset
        self.yo = 3  # yoffset
        self.currentBtn = 0
        self.prevBtn = 0
        self.imageBtn = 0
        self.dataBtn = 1
        self.plotBtn = 2

    def eventFilter(self, source, event):
        if event.type() == QtCore.QEvent.Type.HoverMove:
            Quant = self.width() / 3
            if event.position().x() < Quant:
                self.currentBtn = self.imageBtn
            elif Quant < event.position().x() and event.position().x() < (2 * Quant):
                self.currentBtn = self.dataBtn
            elif event.position().x() > (2 * Quant):
                self.currentBtn = self.plotBtn
            if self.currentBtn != self.prevBtn:
                print("change button: ", self.currentBtn)
                self.prevBtn = self.currentBtn
                # if self.__frames0 != None:
                self.playAnim(self.currentBtn)
        if event.type() == QtCore.QEvent.Type.MouseButtonPress:
            Quant = self.width() / 3
            if event.position().x() < Quant:
                self._timer0.stop()
                self._timer1.stop()
                self._timer2.stop()
                self.setIcon(
                    QtGui.QIcon(QtGui.QPixmap("data/videos/imagesChecked.png"))
                )
                self.config.global_signals.tabChangedbtn.emit(0)
            elif Quant < event.position().x() and event.position().x() < (2 * Quant):
                self._timer0.stop()
                self._timer1.stop()
                self._timer2.stop()
                self.setIcon(QtGui.QIcon(QtGui.QPixmap("data/videos/dataChecked.png")))
                self.config.global_signals.tabChangedbtn.emit(1)

            elif event.position().x() > (2 * Quant):
                self._timer0.stop()
                self._timer1.stop()
                self._timer2.stop()
                self.setIcon(QtGui.QIcon(QtGui.QPixmap("data/videos/plotChecked.png")))
                self.config.global_signals.tabChangedbtn.emit(2)

        return super(TabAnimationButton, self).eventFilter(source, event)

    def setCurrentBtnIndex(self, myIndex=0):
        if myIndex == 0:
            self._timer0.stop()
            self._timer1.stop()
            self._timer2.stop()
            self.setIcon(QtGui.QIcon(QtGui.QPixmap("data/videos/imagesChecked.png")))
            self.config.global_signals.tabChangedbtn.emit(0)
        elif myIndex == 1:
            self._timer0.stop()
            self._timer1.stop()
            self._timer2.stop()
            self.setIcon(QtGui.QIcon(QtGui.QPixmap("data/videos/dataChecked.png")))
            self.config.global_signals.tabChangedbtn.emit(1)

        elif myIndex == 2:
            self._timer0.stop()
            self._timer1.stop()
            self._timer2.stop()
            self.setIcon(QtGui.QIcon(QtGui.QPixmap("data/videos/plotChecked.png")))
            self.config.global_signals.tabChangedbtn.emit(2)

    def setFrames(self, basePath=None, frames=[], tabID=0, resizeButton=True, speed=17):
        if tabID == 0:
            self.__frames0 = self._convertFrame0(basePath, frames, resizeButton, speed)
            self._setFrame1()
        if tabID == 1:
            self.__frames1 = self._convertFrame1(basePath, frames, resizeButton, speed)
            self._setFrame2()
        if tabID == 2:
            self.__frames2 = self._convertFrame2(basePath, frames, resizeButton, speed)
            self._setFrame3()

    def _convertFrame0(self, basePath, frames=[], resizeButton=True, speed=17):
        processed = []
        for i, f in enumerate(frames):
            # print(basePath+"/"+f)
            pix = QtGui.QPixmap(basePath + "/" + f)
            if i == 0:
                self.__frameSize0 = pix.size()
            im = QtGui.QIcon(pix)
            processed.append(im)
        self.__numberOfFrames0 = len(processed)
        self.__basePath0 = basePath
        self.__framesPath0 = frames
        self._timer0.numberOfRepeats = self.__numberOfFrames0
        self._timer0.delay = speed
        return processed

    def _convertFrame1(self, basePath, frames=[], resizeButton=True, speed=17):
        processed = []
        for i, f in enumerate(frames):
            # print(basePath+"/"+f)
            pix = QtGui.QPixmap(basePath + "/" + f)
            if i == 0:
                self.__frameSize1 = pix.size()
            im = QtGui.QIcon(pix)
            processed.append(im)
        self.__numberOfFrames1 = len(processed)
        self.__basePath1 = basePath
        self.__framesPath1 = frames
        self._timer1.numberOfRepeats = self.__numberOfFrames1
        self._timer1.delay = speed
        return processed

    def _convertFrame2(self, basePath, frames=[], resizeButton=True, speed=17):
        processed = []
        for i, f in enumerate(frames):
            # print(basePath+"/"+f)
            pix = QtGui.QPixmap(basePath + "/" + f)
            if i == 0:
                self.__frameSize2 = pix.size()
            im = QtGui.QIcon(pix)
            processed.append(im)
        self.__numberOfFrames2 = len(processed)
        self.__basePath2 = basePath
        self.__framesPath2 = frames
        self._timer2.numberOfRepeats = self.__numberOfFrames2
        self._timer2.delay = speed
        return processed

    def _setFrame1(self, index=0):
        if (
            self.__frames0
            and self.__frameSize0
            and index <= (self.__numberOfFrames0 - 1)
        ) == True:
            self.setIcon(self.__frames0[index])

    def _setFrame2(self, index=0):
        if (
            self.__frames1
            and self.__frameSize1
            and index <= (self.__numberOfFrames1 - 1)
        ) == True:
            self.setIcon(self.__frames1[index])

    def _setFrame3(self, index=0):
        if (
            self.__frames2
            and self.__frameSize2
            and index <= (self.__numberOfFrames2 - 1)
        ) == True:
            self.setIcon(self.__frames2[index])

    def playAnim(self, tabID=0):
        if tabID == 0:
            # print("playing 1")
            print(self.__frames1)
            self._timer1.stop()
            self._timer2.stop()
            self._timer0.start()
        elif tabID == 1:
            # print("playing 2")
            self._timer0.stop()
            self._timer2.stop()
            self._timer1.start()
        elif tabID == 2:
            # print("playing 3")
            self._timer1.stop()
            self._timer0.stop()
            self._timer2.start()


class myRichTextEdit(QtWidgets.QTextEdit):
    def __init__(self, parent):
        QtWidgets.QTextEdit.__init__(self)
        self.setParent(parent)

    def setAttributesInit(self, ref, typeTextEdit="title", myConnection=None):
        self.UIref = ref
        self.setParent(self.UIref.MainWindow)
        self.installEventFilter(self)
        # self.o
        self.htmlBold = "<b>"
        self.htmlIt = "<i>"
        self.htmlSub = "<sub>"
        self.htmlSup = "<sup>"

        self.htmlBoldEnd = "</b>"
        self.htmlItEnd = "</i>"
        self.htmlSubEnd = "</sub>"
        self.htmlSupEnd = "</sup>"

        self.typeTextEdit = typeTextEdit

        self.htmlBold_run = len(self.htmlBold)
        self.htmlIt_run = len(self.htmlIt)
        self.htmlSub_run = len(self.htmlSub)
        self.htmlSup_run = len(self.htmlSub)

        self.htmlBoldEnd_run = len(self.htmlBoldEnd)
        self.htmlItEnd_run = len(self.htmlItEnd)
        self.htmlSubEnd_run = len(self.htmlSubEnd)
        self.htmlSupEnd_run = len(self.htmlSubEnd)
        # self.HTML_formater('<b>sumpleText<\b>')
        # self.addToHTML("This is the original text", 'AddedHere!',5, op= [1])
        self.setHtml("")

    def setConnectionToMatplotlib(self):
        if self.typeTextEdit == "title":
            self.UIref.MyVisualPlotHandler.mainPlotTitle = self.convertHTMLtoTeX(
                self.toHtml()
            )
        if self.typeTextEdit == "xlabel":
            self.UIref.MyVisualPlotHandler.xLabelPlotText = self.convertHTMLtoTeX(
                self.toHtml()
            )
        if self.typeTextEdit == "ylabel":
            self.UIref.MyVisualPlotHandler.yLabelPlotText = self.convertHTMLtoTeX(
                self.toHtml()
            )
        if self.typeTextEdit == "hover":
            print("this is hover ")
            self.UIref.MyVisualPlotHandler.hoverLabelText = self.convertHTMLtoTeX(
                self.toHtml()
            )

    def assignTextToPlotHandler(self):
        self.setConnectionToMatplotlib()
        return

    def mouseReleaseEvent(self, event):
        self.setConnectionToMatplotlib()
        return super(myRichTextEdit, self).mouseReleaseEvent(event)

    def keyPressEvent(self, event):
        print("event ", event.key())
        if event.key() == 16777220:  # enter
            print("pressing enter")
            self.setConnectionToMatplotlib()
            QtWidgets.QApplication.processEvents()
            if self.UIref.MyVisualPlotHandler.hoverRichTextActive == True:
                self.UIref.MyVisualPlotHandler.removeHoverRichTextBox()
            majorTicks = self.UIref.currentAxis.xaxis.get_majorticklabels()
            self.UIref.plot_seaborn()
            # self.UIref.canvas.redraw()
            self.UIref.canvas.update()

            return

        return super(myRichTextEdit, self).keyPressEvent(event)

    def mousePressEvent(self, event):
        self.UIref.MyVisualPlotHandler.prevSelectedTextComboBox = self.typeTextEdit
        # cursor = self.textCursor()
        # myformat = QtGui.QTextCharFormat()
        # myformat.setFontWeight(QtGui.QFont.Bold)
        # cursor.mergeCharFormat(myformat)
        return super(myRichTextEdit, self).mousePressEvent(event)

    def setTextBold(self):
        cursor = self.textCursor()
        myformat = QtGui.QTextCharFormat()
        myformat.setFontWeight(QtGui.QFont.Bold)
        cursor.mergeCharFormat(myformat)
        return

    def setTextItalic(self):
        cursor = self.textCursor()
        myformat = QtGui.QTextCharFormat()
        myformat.setFontItalic(True)
        cursor.mergeCharFormat(myformat)
        return

    def setTexSubScript(self):
        cursor = self.textCursor()
        myformat = QtGui.QTextCharFormat()
        myformat.setVerticalAlignment(QtGui.QTextCharFormat.AlignSubScript)
        cursor.mergeCharFormat(myformat)
        return

    def setTexSuperScript(self):
        cursor = self.textCursor()
        myformat = QtGui.QTextCharFormat()
        myformat.setVerticalAlignment(QtGui.QTextCharFormat.AlignSuperScript)
        cursor.mergeCharFormat(myformat)
        return

    def cutHTML(self, OriginalString, positionStart, positionEnd):
        dictWithTags = self.HTML_getBlocks(OriginalString)

    def addToHTML(self, AllText, textToAdd, posToAdd, op=[]):
        # op = 0 # italics
        # op = 1 #bold
        # op = 2 #sup
        # op = 3  #sub
        if 1 in op:
            inTag = self.htmlIt
            outTag = self.htmlItEnd
        finalText = AllText[:posToAdd] + inTag + textToAdd + outTag + AllText[posToAdd:]
        # print(finalText)

    def HTML_getBlocks(self, inputString):
        blocksBold = []
        blocksIt = []
        blocksSub = []
        blocksSup = []

        # if stringOfInterest_End == None
        # stringOfInterest_End = stringOfInterest_Start
        # runLengthStart = len(stringOfInterest_Start)
        # runLengthEnd = len(stringOfInterest_End)

        for i in range(len(inputString)):
            if inputString[i : i + self.htmlBold_run] == self.htmlBold:
                blocksBold.append([i])
            if inputString[i : i + self.htmlBoldEnd_run] == self.htmlBoldEnd:
                blocksBold[-1].append(i)
            if inputString[i : i + self.htmlIt_run] == self.htmlIt:
                blocksIt.append([i])
            if inputString[i : i + self.htmlItEnd_run] == self.htmlItEnd:
                blocksIt[-1].append(i)
            if inputString[i : i + self.htmlSub_run] == self.htmlSub:
                blocksSub.append([i])
            if inputString[i : i + self.htmlSubEnd_run] == self.htmlSubEnd:
                blocksSub[-1].append(i)
            if inputString[i : i + self.htmlSup_run] == self.htmlSub:
                blocksSup.append([i])
            if inputString[i : i + self.htmlSupEnd_run] == self.htmlSubEnd:
                blocksSup[-1].append(i)

        return {
            "blocksBold": blocksBold,
            "blocksIt": blocksIt,
            "blocksSub": blocksSub,
            "blocksSup": blocksSup,
        }

    def checkme(self):
        cursor = self.textCursor()
        # print(cursor.selectionStart())
        # print(cursor.selectionEnd())
        # print(cursor.selection().toHtml())
        self.UIref.pushButton.setCheckable(True)
        self.UIref.pushButton_2.setCheckable(True)
        self.UIref.pushButton_3.setCheckable(True)
        self.UIref.pushButton_4.setCheckable(True)
        self.UIref.pushButton.setChecked(False)
        self.UIref.pushButton_2.setChecked(False)
        self.UIref.pushButton_3.setChecked(False)
        self.UIref.pushButton_4.setChecked(False)
        myHtml = cursor.selection().toHtml()
        if "font-weight:" in myHtml:
            self.UIref.pushButton_2.setChecked(True)
        if "font-style:italic" in myHtml:
            self.UIref.pushButton.setChecked(True)
        return

    def convertHTMLtoTeX(self, myHTMLText):
        return self.ConvertHTML_DICT_to_TeX(self.CropHTML_qt(myHTMLText))

    def CropHTML_qt(self, inputHTML):
        import re

        if inputHTML == "":
            return None
        allWords = []
        hasStarted = False

        i = 0
        while True:
            # re.search(r"text-indent:0px;", inputHTML)
            # result = re.split(r"\s+", inputHTML)
            # print(inputHTML)
            result = re.split('(?<=text-indent:0px;")', inputHTML)
            result.pop(0)
            # completeList = [re.split("(?=<span)", s) for s in result]

            completeList = []
            completeList2 = []
            import itertools

            completeList = [re.split("(?=<span)", s) for s in result]
            completeList = list(itertools.chain.from_iterable(completeList))
            completeList = [re.split("(?=vertical-align:)", s) for s in completeList]
            completeList = list(itertools.chain.from_iterable(completeList))
            completeList = [re.split("(?<=font-style:italic)", s) for s in completeList]
            completeList = list(itertools.chain.from_iterable(completeList))

            completeList = [re.split("(?<=<span)", s) for s in completeList]
            completeList = list(itertools.chain.from_iterable(completeList))
            # print(completeList)
            # for item in completeList:
            #     print(item)
            #     completeList2.extend(re.split("(?<=;)",item[0]))
            completeList = [re.split('(?<=;")', s) for s in completeList]
            completeList = list(itertools.chain.from_iterable(completeList))
            completeList = [re.split("(?=</span>)", s) for s in completeList]
            completeList = list(itertools.chain.from_iterable(completeList))
            completeList = [re.split("(?<=</span>)", s) for s in completeList]
            completeList = list(itertools.chain.from_iterable(completeList))
            completeList = [re.split("(?<=</p></body>)", s) for s in completeList]
            completeList = list(itertools.chain.from_iterable(completeList))
            completeList = [re.split("(?=</p></body>)", s) for s in completeList]
            completeList = list(itertools.chain.from_iterable(completeList))

            # print("item list start")
            # for item in completeList:
            # print('--')
            # print(item)
            if completeList[0] == "><br />":
                return None
            # print("item list ends")
            result = completeList
            skipList = []
            for i in range(len(result)):
                # if 'text-indent:0px;' in result[i]:
                if i in skipList:
                    continue
                hasStarted = True
                if hasStarted == True:
                    if len(result[i]) != 0:
                        if "</span>" in result[i] and "</p></body>" in result[i + 2]:
                            if not (result[i + 1] == allWords[-1]["text"]):
                                allWords.append(self.getCompactDict())
                                allWords[-1]["text"] = result[i + 1]
                                allWords[-1]["subscript"] = False
                                allWords[-1]["superscript"] = False
                                allWords[-1]["italic"] = False
                                break
                        if result[i][0] == ">" or result[i] == "<span":
                            if (
                                "><br />" in result[i]
                                or "><br/>" in result[i]
                                or "</p></body>" in result[i]
                            ):
                                break

                            allWords.append(self.getCompactDict())
                            if result[i][0] == ">":
                                allWords[-1]["text"] = result[i][1:]
                            a = 1
                            while True:
                                # if len(result) < i+a:
                                if result[i + a] == None:
                                    break
                                if (
                                    "<span" in result[i + a]
                                    or "</span>" in result[i + a]
                                    or "</p></body>" in result[i + a]
                                ):
                                    # print("breaking")
                                    skipList = range(i, i + a)
                                    break
                                if len(result[i + a]) != 0:
                                    if result[i + a][0] == ">":
                                        allWords[-1]["text"] = result[i + a][1:]
                                    # if result[i+a] == 'style=\"':
                                    if "vertical-align:sub" in result[i + a]:
                                        allWords[-1]["subscript"] = True
                                        # if 'vertical-align:sub;"' in result[i+a+1]:
                                        #     currentString = result[i+a+1]
                                        #     currentString.replace('vertical-align:sub;"','')
                                        #     if currentString[0] == '>':
                                        #         allWords[-1]['text'] = currentString[1:]
                                    if "vertical-align:super" in result[i + a]:
                                        allWords[-1]["superscript"] = True

                                    if "font-style:italic" in result[i + a]:
                                        allWords[-1]["italic"] = True
                                    if " font-weight:" in result[i + a]:
                                        allWords[-1]["bold"] = True
                                a += 1
            # print(allWords)
            return allWords
            break
            if re.search(r"text-indent:0px;", inputHTML):
                print("Match found")
            else:
                print("Match not found")
            break
            if (
                inputHTML[i : i + html_start] == html_start
                or inputHTML[i] == first_end_html
            ):
                pass

            if inputHTML[i : i + len_first_start_html] == first_start_html:
                hasStartedLooking = True
                continue
            if hasStartedLooking == True:
                if len(blocksBold) <= 1:
                    if skipOne == False:
                        if inputHTML[i] == first_end_html:
                            print("writing block start1")
                            blocksBold.append([i])
                        if inputHTML[i : i + len_html_start] == html_start:
                            print("writing block start2")
                            blocksBold[-1].append(i)
                            blocksBold.append([i])
                            hasStarted = True
                            skipOne = True
            if (
                inputHTML[i : i + len_html_start] == html_start
                or inputHTML[i] == first_end_html
            ) and hasStarted == True:
                if skipOne == False:
                    print("writing block start3")
                    blocksBold.append([i])
                else:
                    skipOne = False
            if inputHTML[i : i + len_html_end] == html_end and hasStarted == True:
                print("writing block end4")
                blocksBold[-1].append(i)
                skipOne = False
            # print(blocksBold)
            # for i in range(len(blocksBold)):
            #     print(inputHTML[blocksBold[i][0]:blocksBold[i][1]])

            return

    def getCompactDict(self):
        return {
            "text": None,
            "italic": False,
            "bold": False,
            "subscript": False,
            "superscript": False,
        }

    def ConvertHTML_DICT_to_TeX(self, inputDicts):
        totalText = ""
        usedchanged = False
        if not inputDicts:
            return ""
        for item in inputDicts:
            currentText = item["text"]
            if currentText == None:
                continue
            if item["subscript"] == True:
                currentText = "_{" + currentText + "}"
                usedchanged = True
            if item["superscript"] == True:
                currentText = "^{" + currentText + "}"
                usedchanged = True

            if item["italic"]:
                currentText = "\\it{" + currentText + "}"
                usedchanged = True

            if item["bold"]:
                currentText = "\\bf{" + currentText + "}"
                usedchanged = True
            if usedchanged == True:
                currentText = currentText.replace(" ", "\ ")
                # currentText = currentText.replace(" ", "\ ")

            totalText += currentText
        # print(totalText)
        if usedchanged == True:
            completeText = "$" + totalText + "$"
        else:
            completeText = totalText
        return completeText


if __name__ == "__main__":
    pass

# def main():
#     app = QtWidgets.QApplication([])
#     tempapp = Animation_Button()
#     baseP = "data/icons/button_test"
#     frames = os.listdir(baseP)

#     tempapp.setFrames(baseP,frames)

#     tempapp.show()
#     app.exec()

# main()
