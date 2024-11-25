# ../celer_sight_ai/UiAssets/annotation_assistant_dialog.ui'
#
# Created by: PyQt6 UI code generator 6.6.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(555, 226)
        self.horizontalLayout = QtWidgets.QHBoxLayout(Form)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.roi_assistant_cancel_button = QtWidgets.QPushButton(parent=Form)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.roi_assistant_cancel_button.sizePolicy().hasHeightForWidth()
        )
        self.roi_assistant_cancel_button.setSizePolicy(sizePolicy)
        self.roi_assistant_cancel_button.setObjectName("roi_assistant_cancel_button")
        self.gridLayout.addWidget(self.roi_assistant_cancel_button, 0, 1, 1, 1)
        self.roi_assistant_generate_button = QtWidgets.QPushButton(parent=Form)
        self.roi_assistant_generate_button.setObjectName(
            "roi_assistant_generate_button"
        )
        self.gridLayout.addWidget(self.roi_assistant_generate_button, 0, 2, 1, 1)
        self.roi_assistant_accept_button = QtWidgets.QPushButton(parent=Form)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.roi_assistant_accept_button.sizePolicy().hasHeightForWidth()
        )
        self.roi_assistant_accept_button.setSizePolicy(sizePolicy)
        self.roi_assistant_accept_button.setObjectName("roi_assistant_accept_button")
        self.gridLayout.addWidget(self.roi_assistant_accept_button, 0, 3, 1, 1)
        self.ROI_assistant_label = QtWidgets.QLabel(parent=Form)
        self.ROI_assistant_label.setObjectName("ROI_assistant_label")
        self.gridLayout.addWidget(self.ROI_assistant_label, 0, 0, 1, 1)
        self.roi_assistant_advanced_groupbox = QtWidgets.QGroupBox(parent=Form)
        self.roi_assistant_advanced_groupbox.setObjectName(
            "roi_assistant_advanced_groupbox"
        )
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(
            self.roi_assistant_advanced_groupbox
        )
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.positive_roi_threshold_layout = QtWidgets.QHBoxLayout()
        self.positive_roi_threshold_layout.setObjectName(
            "positive_roi_threshold_layout"
        )
        self.positive_roi_threshold_label = QtWidgets.QLabel(
            parent=self.roi_assistant_advanced_groupbox
        )
        self.positive_roi_threshold_label.setObjectName("positive_roi_threshold_label")
        self.positive_roi_threshold_layout.addWidget(self.positive_roi_threshold_label)
        self.positive_roi_threshold_number = QtWidgets.QLabel(
            parent=self.roi_assistant_advanced_groupbox
        )
        self.positive_roi_threshold_number.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignRight
            | QtCore.Qt.AlignmentFlag.AlignTrailing
            | QtCore.Qt.AlignmentFlag.AlignVCenter
        )
        self.positive_roi_threshold_number.setIndent(10)
        self.positive_roi_threshold_number.setObjectName(
            "positive_roi_threshold_number"
        )
        self.positive_roi_threshold_layout.addWidget(self.positive_roi_threshold_number)
        self.positive_roi_threshold_slider = QtWidgets.QSlider(
            parent=self.roi_assistant_advanced_groupbox
        )
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.positive_roi_threshold_slider.sizePolicy().hasHeightForWidth()
        )
        self.positive_roi_threshold_slider.setSizePolicy(sizePolicy)
        self.positive_roi_threshold_slider.setMaximumSize(QtCore.QSize(250, 16777215))
        self.positive_roi_threshold_slider.setOrientation(
            QtCore.Qt.Orientation.Horizontal
        )
        self.positive_roi_threshold_slider.setObjectName(
            "positive_roi_threshold_slider"
        )
        self.positive_roi_threshold_layout.addWidget(self.positive_roi_threshold_slider)
        self.verticalLayout_3.addLayout(self.positive_roi_threshold_layout)
        self.negative_roi_threshold_layout = QtWidgets.QHBoxLayout()
        self.negative_roi_threshold_layout.setObjectName(
            "negative_roi_threshold_layout"
        )
        self.negative_roi_threshold_label = QtWidgets.QLabel(
            parent=self.roi_assistant_advanced_groupbox
        )
        self.negative_roi_threshold_label.setObjectName("negative_roi_threshold_label")
        self.negative_roi_threshold_layout.addWidget(self.negative_roi_threshold_label)
        self.negative_roi_threshold_number = QtWidgets.QLabel(
            parent=self.roi_assistant_advanced_groupbox
        )
        self.negative_roi_threshold_number.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignRight
            | QtCore.Qt.AlignmentFlag.AlignTrailing
            | QtCore.Qt.AlignmentFlag.AlignVCenter
        )
        self.negative_roi_threshold_number.setIndent(10)
        self.negative_roi_threshold_number.setObjectName(
            "negative_roi_threshold_number"
        )
        self.negative_roi_threshold_layout.addWidget(self.negative_roi_threshold_number)
        self.negative_roi_threshold_slider = QtWidgets.QSlider(
            parent=self.roi_assistant_advanced_groupbox
        )
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.negative_roi_threshold_slider.sizePolicy().hasHeightForWidth()
        )
        self.negative_roi_threshold_slider.setSizePolicy(sizePolicy)
        self.negative_roi_threshold_slider.setMaximumSize(QtCore.QSize(250, 16777215))
        self.negative_roi_threshold_slider.setOrientation(
            QtCore.Qt.Orientation.Horizontal
        )
        self.negative_roi_threshold_slider.setObjectName(
            "negative_roi_threshold_slider"
        )
        self.negative_roi_threshold_layout.addWidget(self.negative_roi_threshold_slider)
        self.verticalLayout_3.addLayout(self.negative_roi_threshold_layout)
        self.shape_similarity_threshold_layout = QtWidgets.QHBoxLayout()
        self.shape_similarity_threshold_layout.setObjectName(
            "shape_similarity_threshold_layout"
        )
        self.shape_roi_threshold_label = QtWidgets.QLabel(
            parent=self.roi_assistant_advanced_groupbox
        )
        self.shape_roi_threshold_label.setObjectName("shape_roi_threshold_label")
        self.shape_similarity_threshold_layout.addWidget(self.shape_roi_threshold_label)
        self.shape_roi_threshold_number = QtWidgets.QLabel(
            parent=self.roi_assistant_advanced_groupbox
        )
        self.shape_roi_threshold_number.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignRight
            | QtCore.Qt.AlignmentFlag.AlignTrailing
            | QtCore.Qt.AlignmentFlag.AlignVCenter
        )
        self.shape_roi_threshold_number.setIndent(10)
        self.shape_roi_threshold_number.setObjectName("shape_roi_threshold_number")
        self.shape_similarity_threshold_layout.addWidget(
            self.shape_roi_threshold_number
        )
        self.shape_roi_threshold_slider = QtWidgets.QSlider(
            parent=self.roi_assistant_advanced_groupbox
        )
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.shape_roi_threshold_slider.sizePolicy().hasHeightForWidth()
        )
        self.shape_roi_threshold_slider.setSizePolicy(sizePolicy)
        self.shape_roi_threshold_slider.setMaximumSize(QtCore.QSize(250, 16777215))
        self.shape_roi_threshold_slider.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.shape_roi_threshold_slider.setObjectName("shape_roi_threshold_slider")
        self.shape_similarity_threshold_layout.addWidget(
            self.shape_roi_threshold_slider
        )
        self.verticalLayout_3.addLayout(self.shape_similarity_threshold_layout)
        self.image_similarity_threshold_layout = QtWidgets.QHBoxLayout()
        self.image_similarity_threshold_layout.setObjectName(
            "image_similarity_threshold_layout"
        )
        self.image_similarity_threshold_label = QtWidgets.QLabel(
            parent=self.roi_assistant_advanced_groupbox
        )
        self.image_similarity_threshold_label.setObjectName(
            "image_similarity_threshold_label"
        )
        self.image_similarity_threshold_layout.addWidget(
            self.image_similarity_threshold_label
        )
        self.image_similarity_threshold_number = QtWidgets.QLabel(
            parent=self.roi_assistant_advanced_groupbox
        )
        self.image_similarity_threshold_number.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignRight
            | QtCore.Qt.AlignmentFlag.AlignTrailing
            | QtCore.Qt.AlignmentFlag.AlignVCenter
        )
        self.image_similarity_threshold_number.setIndent(10)
        self.image_similarity_threshold_number.setObjectName(
            "image_similarity_threshold_number"
        )
        self.image_similarity_threshold_layout.addWidget(
            self.image_similarity_threshold_number
        )
        self.image_similarity_threshold_slider = QtWidgets.QSlider(
            parent=self.roi_assistant_advanced_groupbox
        )
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.image_similarity_threshold_slider.sizePolicy().hasHeightForWidth()
        )
        self.image_similarity_threshold_slider.setSizePolicy(sizePolicy)
        self.image_similarity_threshold_slider.setMaximumSize(
            QtCore.QSize(250, 16777215)
        )
        self.image_similarity_threshold_slider.setOrientation(
            QtCore.Qt.Orientation.Horizontal
        )
        self.image_similarity_threshold_slider.setObjectName(
            "image_similarity_threshold_slider"
        )
        self.image_similarity_threshold_layout.addWidget(
            self.image_similarity_threshold_slider
        )
        self.verticalLayout_3.addLayout(self.image_similarity_threshold_layout)
        self.gridLayout.addWidget(self.roi_assistant_advanced_groupbox, 1, 0, 1, 4)
        self.verticalLayout.addLayout(self.gridLayout)
        self.horizontalLayout.addLayout(self.verticalLayout)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.roi_assistant_cancel_button.setText(_translate("Form", "Cancel"))
        self.roi_assistant_generate_button.setText(_translate("Form", "Generate"))
        self.roi_assistant_accept_button.setText(_translate("Form", "Accept"))
        self.ROI_assistant_label.setText(_translate("Form", "ROI Assistance"))
        self.roi_assistant_advanced_groupbox.setTitle(_translate("Form", "Advanced"))
        self.positive_roi_threshold_label.setText(
            _translate("Form", "Positive ROI threshold")
        )
        self.positive_roi_threshold_number.setText(_translate("Form", "42"))
        self.negative_roi_threshold_label.setText(
            _translate("Form", "Negative ROI threshold")
        )
        self.negative_roi_threshold_number.setText(_translate("Form", "42"))
        self.shape_roi_threshold_label.setText(
            _translate("Form", "Shape similarity threshold")
        )
        self.shape_roi_threshold_number.setText(_translate("Form", "42"))
        self.image_similarity_threshold_label.setText(
            _translate("Form", "Image similarity threshold")
        )
        self.image_similarity_threshold_number.setText(_translate("Form", "42"))
