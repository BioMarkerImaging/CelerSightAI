from PyQt6 import QtCore, QtGui, QtWidgets


class labelAnimation(QtWidgets.QLabel):  # instance is --MyVisualPlotHandler!
    mySignal = QtCore.pyqtSignal(str)

    def __init__(self, MainWindow=None, preOption="loadingOption"):
        super(labelAnimation, self).__init__()

        self.hasStarted = False
        self.MainWindow = MainWindow
        self.timeLine = None
        self.currentNumber = 0
        self.loadingOption = [
            "loading",
            " loading.",
            "  loading..",
            "   loading...",
            "    loading....",
            "loading",
            " loading.",
            "  loading..",
            "   loading...",
            "    loading....",
            "loading",
            " loading.",
            "  loading..",
            "   loading...",
            "    loading....",
            "loading",
            " loading.",
            "  loading..",
            "   loading...",
            "    loading....",
            "loading",
            " loading.",
            "  loading..",
            "   loading...",
            "    loading....",
            "loading",
            " loading.",
            "  loading..",
            "   loading...",
            "    loading....",
            "loading",
            " loading.",
            "  loading..",
            "   loading...",
            "    loading....",
            "loading",
            " loading.",
            "  loading..",
            "   loading...",
            "    loading....",
        ]
        self.PreprocessingOption = [
            "Pre-processing",
            " Pre-processing.",
            "  Pre-processing..",
            "   Pre-processing...",
            "    Pre-processing....",
            "Pre-processing",
            " Pre-processing.",
            "  Pre-processing..",
            "   Pre-processing...",
            "    Pre-processing....",
            "Pre-processing",
            " Pre-processing.",
            "  Pre-processing..",
            "   Pre-processing...",
            "    Pre-processing....",
            "Pre-processing",
            " Pre-processing.",
            "  Pre-processing..",
            "   Pre-processing...",
            "    Pre-processing....",
            "Pre-processing",
            " Pre-processing.",
            "  Pre-processing..",
            "   Pre-processing...",
            "    Pre-processing....",
            "Pre-processing",
            " Pre-processing.",
            "  Pre-processing..",
            "   Pre-processing...",
            "    Pre-processing....",
            "Pre-processing",
            " Pre-processing.",
            "  Pre-processing..",
            "   Pre-processing...",
            "    Pre-processing....",
            "Pre-processing",
            " Pre-processing.",
            "  Pre-processing..",
            "   Pre-processing...",
            "    Pre-processing....",
        ]
        self.trainingOption = [
            "training",
            " training.",
            "  training..",
            "   training...",
            "    training....",
            "training",
            " training.",
            "  training..",
            "   training...",
            "    training....",
            "training",
            " training.",
            "  training..",
            "   training...",
            "    training....",
            "training",
            " training.",
            "  training..",
            "   training...",
            "    training....",
            "training",
            " training.",
            "  training..",
            "   training...",
            "    training....",
            "training",
            " training.",
            "  training..",
            "   training...",
            "    training....",
            "training",
            " training.",
            "  training..",
            "   training...",
            "    training....",
            "training",
            " training.",
            "  training..",
            "   training...",
            "    training....",
        ]
        self.predictingOption = [
            "predicting",
            " predicting.",
            "  predicting..",
            "   predicting...",
            "    predicting....",
            "predicting",
            " predicting.",
            "  predicting..",
            "   predicting...",
            "    predicting....",
            "predicting",
            " predicting.",
            "  predicting..",
            "   predicting...",
            "    predicting....",
            "predicting",
            " predicting.",
            "  predicting..",
            "   predicting...",
            "    predicting....",
            "predicting",
            " predicting.",
            "  predicting..",
            "   predicting...",
            "    predicting....",
            "predicting",
            " predicting.",
            "  predicting..",
            "   predicting...",
            "    predicting....",
            "predicting",
            " predicting.",
            "  predicting..",
            "   predicting...",
            "    predicting....",
            "predicting",
            " predicting.",
            "  predicting..",
            "   predicting...",
            "    predicting....",
        ]

        if preOption == "loadingOption":
            self.textDisplayed = self.loadingOption
        elif preOption == "PreprocessingOption":
            self.textDisplayed = self.PreprocessingOption
        elif preOption == "trainingOption":
            self.textDisplayed = self.trainingOption
        elif preOption == "predictingOption":
            self.textDisplayed = self.predictingOption
        # elif preOption =="loadingOption":
        #     self.textDisplayed = loadingOption
        self.setParent(self.MainWindow.viewer)
        self.move(0, 0)
        self.setFixedWidth(self.MainWindow.viewer.width())
        self.setFixedHeight(self.MainWindow.viewer.height())
        self.setText("loading")
        self.setFont(QtGui.QFont("Arial", 52))
        from celer_sight_ai import config

        config.global_signals.trainingLabelUpdateSignal.connect(
            lambda: self.changeStringToTraining()
        )
        config.global_signals.predictingLabeUpdatelSignal.connect(
            lambda: self.changeStringToPredicting()
        )
        config.global_signals.PreProcessingLabeUpdatelSignal.connect(
            lambda: self.changeStringToPreProcessing()
        )

        self.setStyleSheet(
            """
                                color: rgba(230,230,230,255);
                                background-color: rgba(0,0,0,90);
                            """
        )
        self.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignHCenter | QtCore.Qt.AlignmentFlag.AlignVCenter
        )
        self.show()
        self.setEnabled(False)
        self._total = 1
        self.CLabelA()
        # self.mySignal.connect(self.setMainString)

    def changeStringToTraining(self):
        self.currentNumber = 0
        self.textDisplayed = self.trainingOption
        self.setText(self.textDisplayed[int(self.currentNumber)])

    def changeStringToPredicting(self):
        self.currentNumber = 0
        self.textDisplayed = self.predictingOption
        self.setText(self.textDisplayed[int(self.currentNumber)])

    def changeStringToPreProcessing(self):
        self.currentNumber = 0
        self.textDisplayed = self.PreprocessingOption
        self.setText(self.textDisplayed[int(self.currentNumber)])

    def setMainString(self, StringToPut):
        self.setText(StringToPut)
        print("signal connected")

    # @QtCore.pyqtProperty(int, notify=mySignal)
    # def CLabelA(self):
    #     #self.setText(self.textDisplayed[int(self._total)])
    #     self.mySignal.emit(self.textDisplayed[int(self._total)])
    #     print("emiting2 ", self._total)
    #     return self._total
    def CLabelA(self):
        start = 0
        end = 3
        print("working!")
        print(abs(end - start) * 1000)
        self.timeLine = QtCore.QTimeLine(abs(end - start) * 1000, self)
        self.timeLine.setFrameRange(start, end)
        self.timeLine.frameChanged.connect(self.setCLabelA)
        self.timeLine.setLoopCount(100)
        self.timeLine.start()

    def completeLoad(self):
        self.MainWindow.viewer.ML_brush_tool_object_during_inference = False
        if self.timeLine:
            if self.timeLine.state() == QtCore.QTimeLine.Running:
                self.timeLine.stop()
                self.currentNumber = 0
                self.setText(self.textDisplayed[0])
                self.hide()
        self.hide()

    def setCLabelA(self):
        if self.currentNumber >= len(self.textDisplayed) - 1:
            self.currentNumber = 0
        self.currentNumber += 1
        self.setText(self.textDisplayed[int(self.currentNumber)])

        print("going2 ", self.currentNumber)

    # CLabelA = QtCore.pyqtProperty(int, fset=setCLabelA)

    def startLoadingAnimation(self):
        print("ANIMATION STARTING")
        animation = QtCore.QPropertyAnimation(self, b"CLabelA")
        animation.setStartValue(0)
        animation.setEndValue(3)
        animation.setDuration(1000)
        # animation.setLoopCount(100000)
        animation.start()
