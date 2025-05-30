from PyQt6 import QtCore, QtGui, QtWidgets


class ArrowChangeImageButton(QtWidgets.QPushButton):
    valueChangedSignal = QtCore.pyqtSignal(int)

    def __init__(
        self,
        imageLocation=None,
        Viewer=None,
        StartingPositionXMOD=0,
        StartingPositionYMOD=0,
        MODE="left",
    ):
        super().__init__()
        self.ViewerRef = Viewer
        self.setParent(self.ViewerRef)
        import cv2

        self.installEventFilter(self)
        self.StartingPosY = self.ViewerRef.height() / 2
        self.StartingPosX = self.ViewerRef.width()
        self.StartingPosX_MODIFIER = StartingPositionXMOD
        self.StartingPosY_MODIFIER = StartingPositionYMOD
        self.duringAnim = False
        self.posVisible = False
        self.MODE = MODE
        # Add arrow left and right
        if self.MODE == "left":
            self.move(
                QtCore.QPoint(
                    int(self.StartingPosX_MODIFIER),
                    int(self.StartingPosY + self.StartingPosY_MODIFIER),
                )
            )

        if self.MODE == "right":
            self.move(
                QtCore.QPoint(
                    int(self.StartingPosX + self.StartingPosX_MODIFIER),
                    int(self.StartingPosY + self.StartingPosY_MODIFIER),
                )
            )
        self.setMaximumSize(QtCore.QSize(75, 75))
        self.setMinimumSize(QtCore.QSize(75, 75))
        pixmap = QtGui.QPixmap(imageLocation)
        size = QtCore.QSize(60, 60)
        self.setIcon(QtGui.QIcon(pixmap))
        self.setIconSize(size)
        self.setStyleSheet(
            """
        QPushButton{
            background-color:rgba(0,0,0,50);
            border-radius: 35;
        }
        QPushButton:hover{
            background-color:rgba(0,0,0,20);
            border-color: rgba(0,0,0,0);
        }
        """
        )
        self.valueChangedSignal.connect(self.onValueChanged)
        self.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))

        if MODE == "right":
            animationStart = self.StartingPosX_MODIFIER
            animationEnd = self.StartingPosX_MODIFIER + 50
        elif MODE == "left":
            animationStart = self.ViewerRef.width() + self.StartingPosX_MODIFIER
            animationEnd = self.ViewerRef.width() + self.StartingPosX_MODIFIER - 50
        self.show_animation = QtCore.QVariantAnimation(
            self,
            startValue=animationStart,
            endValue=animationEnd,
            # valueChanged=self.valueChangedSignal,
            duration=200,
            easingCurve=QtCore.QEasingCurve.Type.InOutCubic,
        )
        self.hide_animation = QtCore.QVariantAnimation(
            self,
            startValue=animationEnd,
            endValue=animationStart,
            # valueChanged=self.valueChangedSignal,
            duration=1000,
            easingCurve=QtCore.QEasingCurve.Type.InOutCubic,
        )
        self.show_animation.finished.connect(lambda: self.setPosVisible(True))
        self.hide_animation.finished.connect(lambda: self.setPosVisible(False))
        if self.MODE == "right":
            self.hide_animation.setStartValue(self.pos().x())
            self.hide_animation.setEndValue(
                self.ViewerRef.width() + self.StartingPosX_MODIFIER
            )
            self.duringAnim = True
            self.posVisible = False
            self.hide_animation.start()
        if self.MODE == "left":
            self.hide_animation.setStartValue(self.pos().x())
            self.hide_animation.setEndValue(self.StartingPosX_MODIFIER)

            self.duringAnim = True
            self.posVisible = False
            self.hide_animation.start()

        # self.hide_animation.start()

    # @QtCore. pyqtSlot(bool)
    # def onToggled(self, checked):
    #     self.m_animation.setDirection(
    #         QtCore.QAbstractAnimation.Forward
    #         if checked
    #         else QtCore.QAbstractAnimation.Backward
    #     )
    #     self.m_animation.start()
    def setPosVisible(self, Viz):
        print("SETTING VISIBLE")
        self.posVisible = Viz
        self.duringAnim = False

    @QtCore.pyqtSlot(int)
    def onValueChanged(self, value):
        self.move(
            QtCore.QPoint(
                int(value),
                int(self.ViewerRef.height() / 2 + self.StartingPosY_MODIFIER),
            )
        )
        # print(value)

    def updatePositionViewer(self):
        if self.MODE == "left":
            self.move(
                QtCore.QPoint(
                    int(self.StartingPosX_MODIFIER),
                    int(self.ViewerRef.height() / 2 + self.StartingPosY_MODIFIER),
                )
            )
        if self.MODE == "right":
            self.move(
                QtCore.QPoint(
                    int(self.ViewerRef.width() + self.StartingPosX_MODIFIER),
                    int(self.ViewerRef.height() / 2 + self.StartingPosY_MODIFIER),
                )
            )

    def leaveEvent(self, event):
        if self.MODE == "right":
            if self.duringAnim is True:
                self.show_animation.stop()
                self.duringAnim = False
            if self.duringAnim is False:
                self.hide_animation.setStartValue(self.pos().x())
                self.hide_animation.setEndValue(
                    self.ViewerRef.width() + self.StartingPosX_MODIFIER
                )
                self.duringAnim = True
                self.posVisible = False
                self.hide_animation.start()
        if self.MODE == "left":
            if self.duringAnim is True:
                self.hide_animation.setStartValue(self.pos().x())
                self.hide_animation.setEndValue(self.StartingPosX_MODIFIER - 50)
                # self.show_animation.stop()
                self.duringAnim = False
                self.hide_animation.start()
            if self.duringAnim is False:
                self.hide_animation.setStartValue(self.pos().x())
                self.hide_animation.setEndValue(self.StartingPosX_MODIFIER)
                self.duringAnim = True
                self.posVisible = False
                self.hide_animation.start()
        return super().leaveEvent(event)

    def enterEvent(self, event):
        if self.duringAnim is True:
            # self.show_animation.stop()
            self.hide_animation.stop()
            self.duringAnim = False
        if self.MODE == "left":
            if self.duringAnim is False:
                self.show_animation.setStartValue(self.StartingPosX_MODIFIER)
                self.show_animation.setEndValue(self.StartingPosX_MODIFIER + 40)
                self.duringAnim = True
                self.show_animation.start()
        if self.MODE == "right":
            if self.duringAnim is False:
                self.show_animation.setStartValue(
                    self.ViewerRef.width() + self.StartingPosX_MODIFIER
                )
                self.show_animation.setEndValue(
                    self.ViewerRef.width() + self.StartingPosX_MODIFIER - 40
                )
                self.duringAnim = True
                self.show_animation.start()
        return super().enterEvent(event)
