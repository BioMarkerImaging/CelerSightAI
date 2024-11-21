# custom pushbutton

from PyQt6 import QtGui, QtCore, QtWidgets
import os


class RepeatTimer(QtCore.QTimer):
    timeoutCount = QtCore.pyqtSignal(int)
    endRepeat = QtCore.pyqtSignal()

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


class QGroupBoxCollapsable_Maker:
    def __init__(self, InstanceToEnhance=None):
        # QGroupBoxCollapsable_Maker.__init__(self)

        InstanceToEnhance.AnimationDuration = 250
        InstanceToEnhance.setCheckable(True)
        InstanceToEnhance.setChecked(True)

        self.AnimateOff(InstanceToEnhance)
        self.AnimateOn(InstanceToEnhance)
        InstanceToEnhance.toggled.connect(
            lambda: self.AnimationDecider(InstanceToEnhance)
        )
        # InstanceToEnhance.toggled.connect(lambda: print("Toggle is working!") )

        InstanceToEnhance.setEnabled(True)

    @staticmethod
    def AnimationDecider(InstanceGroupbox):
        if InstanceGroupbox.isChecked() == False:
            InstanceGroupbox.ParAnimationOn.start()
        elif InstanceGroupbox.isChecked() == True:
            InstanceGroupbox.ParAnimationOff.start()

    @staticmethod
    def AnimateOff(InstanceToEnhance):
        """
        Thisfunction runs every time we Close the groupbox
        """
        AnimationDuration = 220
        InstanceToEnhance.ParAnimationOn = QtCore.QParallelAnimationGroup()

        # Get Initial Variables
        BegginPosX = InstanceToEnhance.pos().x()
        BegginPosY = InstanceToEnhance.pos().y()
        BegginWidth = InstanceToEnhance.width()
        BegginHeight = InstanceToEnhance.maximumHeight()

        #
        # Adjust size policy
        #
        MysizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum
        )
        InstanceToEnhance.setMinimumHeight(0)
        InstanceToEnhance.setSizePolicy(MysizePolicy)
        InstanceToEnhance.setMaximumHeight(BegginHeight)

        InstanceToEnhance.OriginalHeight = BegginHeight  # we need to save this so that when it opens we can jsut go  back to normal
        GeometryAnimation = QtCore.QPropertyAnimation(
            InstanceToEnhance, b"maximumHeight"
        )
        GeometryAnimation.setDuration(AnimationDuration)
        GeometryAnimation.setStartValue(BegginHeight)
        GeometryAnimation.setEndValue(20)

        curve = QtCore.QEasingCurve(QtCore.QEasingCurve.Type.OutExpo)
        GeometryAnimation.setEasingCurve(curve)
        InstanceToEnhance.ParAnimationOn.addAnimation(GeometryAnimation)

    @staticmethod
    def AnimateOn(InstanceToEnhance):
        """
        Thisfunction runs every time we Close the groupbox
        """
        AnimationDuration = 420
        InstanceToEnhance.ParAnimationOff = QtCore.QParallelAnimationGroup()

        GeometryAnimation = QtCore.QPropertyAnimation(
            InstanceToEnhance, b"maximumHeight"
        )
        GeometryAnimation.setDuration(AnimationDuration)
        GeometryAnimation.setStartValue(20)
        GeometryAnimation.setEndValue(InstanceToEnhance.OriginalHeight)

        curve = QtCore.QEasingCurve(QtCore.QEasingCurve.Type.OutExpo)
        GeometryAnimation.setEasingCurve(curve)
        InstanceToEnhance.ParAnimationOff.addAnimation(GeometryAnimation)


class QGroupBoxCollapsable_old(QtWidgets.QGroupBox):
    def __init__(self, parent=None):
        QtWidgets.QGroupBox.__init__(self, parent)
        self._previousvalue = 200  # the value that is before the collapse happens and the value that it will be restored after the collapse happens
        C = 1000
        self.setCheckable(True)
        self.toggled.connect(lambda: self.expand_group_box())
        # self.setMaximumSize(QtCore.QSize(10000, self.frameGeometry().height()))

    def expand_group_box(self):
        """
        Function that animates the QGroupBox to make it close and open.
        """
        print("working animation")

        self.setMinimumSize(QtCore.QSize(10, 10))

        tmp_width = self.frameGeometry().width()
        tmp_height = self.frameGeometry().height()
        tmp_max_height = self.maximumHeight()

        self.animator = QtCore.QParallelAnimationGroup(self)

        self.animation_size = QtCore.QPropertyAnimation(self, b"size")
        self.animation_max_size = QtCore.QPropertyAnimation(self, b"maximumHeight")
        self.animation_min_size = QtCore.QPropertyAnimation(self, b"minimumHeight")

        print("maxfeight : ", tmp_height)
        if tmp_height > 30:
            print("first")
            self._previousvalue = tmp_height
            print(tmp_max_height)
            self._previousMax = tmp_height
            self.animation_size.setEndValue(QtCore.QSize(tmp_width, 30))
            self.animation_max_size.setEndValue(30)
            self.animation_min_size.setEndValue(30)
            self.animator.addAnimation(self.animation_size)
            self.animator.addAnimation(self.animation_max_size)
            self.animator.addAnimation(self.animation_min_size)
            self.animator.start()
            self.animator.finished.connect(self.handleFInished_closed)

        else:

            print("second")
            print(self._previousvalue)

            # self.setMaximumSize(QtCore.QSize(10000, self._previousvalue))

            self.animation_max_size.setEndValue(self._previousvalue)
            self.animation_size.setEndValue(
                QtCore.QSize(tmp_width, self._previousvalue)
            )
            self.animation_min_size.setEndValue(self._previousvalue)

            self.animator.addAnimation(self.animation_size)
            self.animator.addAnimation(self.animation_max_size)
            self.animator.addAnimation(self.animation_min_size)

            # self.animation_size.start()
            print("first animation ok")
            self.animator.start()
            self.animator.finished.connect(self.handleFinshed_open)

        return

    def handleFinshed_open(self):
        self.setMaximumHeight(self._previousMax)
        return

    def handleFInished_closed(self):
        self.setMaximumHeight(30)
        return

    def resizeGroupbox(self):
        self.animation = QtCore.QPropertyAnimation(self, "size")
        # self.animation.setDuration(1000) #Default 250ms
        if self.size().width() == 200:
            self.animation.setEndValue(QtCore.QSize(600, 300))
        else:
            self.animation.setEndValue(QtCore.QSize(200, 100))
        self.animation.start()


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
