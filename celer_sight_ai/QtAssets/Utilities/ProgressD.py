from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_Progress_dialog(object):
    def setupUi(self, Progress_dialog):
        Progress_dialog.setObjectName("Progress_dialog")
        Progress_dialog.setWindowModality(QtCore.Qt.WindowModal)
        Progress_dialog.resize(300, 100)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Progress_dialog.sizePolicy().hasHeightForWidth())
        Progress_dialog.setSizePolicy(sizePolicy)
        Progress_dialog.setMinimumSize(QtCore.QSize(300, 100))
        Progress_dialog.setMaximumSize(QtCore.QSize(300, 100))
        Progress_dialog.setWindowFilePath("")
        Progress_dialog.setSizeGripEnabled(False)
        Progress_dialog.setModal(False)
        self.gridLayout = QtWidgets.QGridLayout(Progress_dialog)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setObjectName("gridLayout")
        self.progress_layout_1 = QtWidgets.QVBoxLayout()
        self.progress_layout_1.setContentsMargins(10, 10, 10, 4)
        self.progress_layout_1.setSpacing(0)
        self.progress_layout_1.setObjectName("progress_layout_1")
        spacerItem = QtWidgets.QSpacerItem(
            20,
            11,
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Fixed,
        )
        self.progress_layout_1.addItem(spacerItem)
        Progress_dialog.progressBar = QtWidgets.QProgressBar(Progress_dialog)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            Progress_dialog.progressBar.sizePolicy().hasHeightForWidth()
        )
        Progress_dialog.progressBar.setSizePolicy(sizePolicy)
        Progress_dialog.progressBar.setMinimumSize(QtCore.QSize(0, 33))
        Progress_dialog.progressBar.setLayoutDirection(
            QtCore.Qt.LayoutDirection.LeftToRight
        )
        Progress_dialog.progressBar.setProperty("value", 50)
        Progress_dialog.progressBar.setObjectName("progressBar")
        self.progress_layout_1.addWidget(Progress_dialog.progressBar)
        Progress_dialog.label = QtWidgets.QLabel(Progress_dialog)
        Progress_dialog.label.setObjectName("label")
        self.progress_layout_1.addWidget(Progress_dialog.label)
        self.gridLayout.addLayout(self.progress_layout_1, 0, 0, 1, 1)

        self.retranslateUi(Progress_dialog)
        QtCore.QMetaObject.connectSlotsByName(Progress_dialog)

    def retranslateUi(self, Progress_dialog):
        _translate = QtCore.QCoreApplication.translate
        Progress_dialog.setWindowTitle(
            _translate("Progress_dialog", "Analysis Progress")
        )
        Progress_dialog.label.setText(
            _translate("Progress_dialog", "Analyzing condition 1 out of 3")
        )
