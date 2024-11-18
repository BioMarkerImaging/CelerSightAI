# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\manos\Documents\topfluov2\UiAssets\quickToolStickAreaForm.ui'
#
# Created by: PyQt6 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(94, 585)
        Form.setStyleSheet(
            "background-color: rgba(85, 255, 255,60);\n"
            "\n"
            "             border-width: 2px;  \n"
            "             border-color:  rgba(85, 255, 255,220);\n"
            "             border-style: solid;  \n"
            "             border-radius: 15;  \n"
            "             padding: 3px;  \n"
            "             font-size: 12px;  \n"
            "             padding-left: 5px;  \n"
            "             padding-right: 5px;  "
        )

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec())
