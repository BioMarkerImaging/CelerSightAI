# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\manos\Documents\Ntopfluov1\UiAssets\popup_tool_menu_v2.ui'
#
# Created by: PyQt6 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_tool_selection_onscreen_menu(object):
    def setupUi(self, tool_selection_onscreen_menu):
        tool_selection_onscreen_menu.setObjectName("tool_selection_onscreen_menu")
        tool_selection_onscreen_menu.resize(781, 532)
        tool_selection_onscreen_menu.setStyleSheet(
            "\n"
            "QPushButton{\n"
            "\n"
            'font: 16pt "Calibri";\n'
            "border-width: 2px;\n"
            "border-color:  rgb(40, 40, 40);\n"
            "border-style: solid;\n"
            "border-radius:30;\n"
            "    color: rgba(255, 255, 255,25);\n"
            "\n"
            "background-color: rgba(0,0,0,0);\n"
            "}\n"
            "QPushButton:hover{\n"
            "border-width: 2px;\n"
            "border-color:  rgb(255, 160, 0);\n"
            "border-style: solid;\n"
            "border-radius:45;\n"
            "    color: black;\n"
            "background-color: rgba(0,0,0,0);\n"
            "\n"
            "}\n"
            "\n"
            "QPushButton#tool_selection_menu_auto_cut_btn{\n"
            "\n"
            'border-image: url("data/icons/icons_aa_tool/PopUP Menu Magic.png") 178 178 178 178 stretch stretch;\n'
            "\n"
            "}\n"
            "QPushButton#tool_selection_menu_auto_cut_btn:checked {\n"
            "border-image: url();\n"
            "}\n"
            "QPushButton#tool_selection_menu_selection_btn{\n"
            "border-image: url(data/icons/icons_aa_tool/PopUP MenuArrow.png) 178 178 178 178 stretch stretch;\n"
            "}\n"
            "QPushButton#tool_selection_menu_selection_btn:checked {\n"
            "border-image: url();\n"
            "}\n"
            "QPushButton#tool_selection_menu_polygon_btn{\n"
            "border-image: url(data/icons/icons_aa_tool/PopUP Menu DrawPol.png) 178 178 178 178 stretch stretch;\n"
            "}\n"
            "QPushButton#tool_selection_menu_polygon_btn:checked {\n"
            "border-image: url();\n"
            "}QPushButton#tool_selection_menu_erase{\n"
            'border-image: url("data/icons/icons_aa_tool/PopUP Menu Erase.png")  178 178 178 178 stretch stretch;;\n'
            "}\n"
            "QPushButton#tool_selection_menu_erase:checked {\n"
            "border-image: url();\n"
            "}\n"
            "\n"
            "QPushButton#tool_selection_menu_Center{\n"
            'border-image: url("data/icons/icons_aa_tool/PopUP Menu Center.png")  190 190 190 190 stretch stretch;;\n'
            "\n"
            'font: 16pt "Calibri";\n'
            "border-width: 2px;\n"
            "border-color:  rgb(40, 40, 40);\n"
            "border-style: solid;\n"
            "border-radius:30;\n"
            "    color: rgba(255, 255, 255,25);\n"
            "\n"
            "background-color: rgba(0,0,0,0);\n"
            "\n"
            "\n"
            "}\n"
            "QPushButton#tool_selection_menu_Center:hover{\n"
            "\n"
            "border-width: 2px;\n"
            "border-color:   rgb(40, 40, 40);\n"
            "border-style: solid;\n"
            "border-radius:30;\n"
            "    color: black;\n"
            "background-color: rgba(0,0,0,0);\n"
            "\n"
            "}\n"
            "\n"
            "\n"
            "\n"
            "\n"
            "\n"
            ""
        )
        self.gridLayout = QtWidgets.QGridLayout(tool_selection_onscreen_menu)
        self.gridLayout.setObjectName("gridLayout")
        self.OouterFrame = QtWidgets.QFrame(tool_selection_onscreen_menu)
        self.OouterFrame.setStyleSheet(
            "QFrame{\n" "background-color: rgba(255, 255, 255,0);\n" "}\n" ""
        )
        self.OouterFrame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.OouterFrame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.OouterFrame.setObjectName("OouterFrame")
        self.InnerFrame = QtWidgets.QFrame(self.OouterFrame)
        self.InnerFrame.setGeometry(QtCore.QRect(130, 90, 491, 291))
        self.InnerFrame.setStyleSheet(
            "QFrame{\n" "background-color: rgba(255, 255, 255,0);\n" "}\n" ""
        )
        self.InnerFrame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.InnerFrame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.InnerFrame.setObjectName("InnerFrame")
        self.tool_selection_menu_polygon_btn = QtWidgets.QPushButton(self.InnerFrame)
        self.tool_selection_menu_polygon_btn.setGeometry(QtCore.QRect(20, 140, 91, 91))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(16)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.tool_selection_menu_polygon_btn.setFont(font)
        self.tool_selection_menu_polygon_btn.setStyleSheet("")
        self.tool_selection_menu_polygon_btn.setCheckable(True)
        self.tool_selection_menu_polygon_btn.setObjectName(
            "tool_selection_menu_polygon_btn"
        )
        self.tool_selection_menu_selection_btn = QtWidgets.QPushButton(self.InnerFrame)
        self.tool_selection_menu_selection_btn.setGeometry(
            QtCore.QRect(370, 140, 91, 91)
        )
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(16)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.tool_selection_menu_selection_btn.setFont(font)
        self.tool_selection_menu_selection_btn.setStyleSheet("")
        self.tool_selection_menu_selection_btn.setCheckable(True)
        self.tool_selection_menu_selection_btn.setChecked(True)
        self.tool_selection_menu_selection_btn.setObjectName(
            "tool_selection_menu_selection_btn"
        )
        self.tool_selection_menu_erase = QtWidgets.QPushButton(self.InnerFrame)
        self.tool_selection_menu_erase.setGeometry(QtCore.QRect(260, 50, 91, 91))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(16)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.tool_selection_menu_erase.setFont(font)
        self.tool_selection_menu_erase.setStyleSheet("")
        self.tool_selection_menu_erase.setCheckable(True)
        self.tool_selection_menu_erase.setObjectName("tool_selection_menu_erase")
        self.tool_selection_menu_auto_cut_btn = QtWidgets.QPushButton(self.InnerFrame)
        self.tool_selection_menu_auto_cut_btn.setGeometry(QtCore.QRect(130, 50, 91, 91))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(16)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.tool_selection_menu_auto_cut_btn.setFont(font)
        self.tool_selection_menu_auto_cut_btn.setStyleSheet("")
        self.tool_selection_menu_auto_cut_btn.setCheckable(True)
        self.tool_selection_menu_auto_cut_btn.setObjectName(
            "tool_selection_menu_auto_cut_btn"
        )
        self.tool_selection_menu_Center = QtWidgets.QPushButton(self.InnerFrame)
        self.tool_selection_menu_Center.setGeometry(QtCore.QRect(210, 220, 60, 60))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(16)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.tool_selection_menu_Center.setFont(font)
        self.tool_selection_menu_Center.setStyleSheet("")
        self.tool_selection_menu_Center.setText("")
        self.tool_selection_menu_Center.setObjectName("tool_selection_menu_Center")
        self.gridLayout.addWidget(self.OouterFrame, 0, 0, 1, 1)

        self.retranslateUi(tool_selection_onscreen_menu)
        QtCore.QMetaObject.connectSlotsByName(tool_selection_onscreen_menu)

    def retranslateUi(self, tool_selection_onscreen_menu):
        _translate = QtCore.QCoreApplication.translate
        tool_selection_onscreen_menu.setWindowTitle(
            _translate("tool_selection_onscreen_menu", "Dialog")
        )
        self.tool_selection_menu_polygon_btn.setText(
            _translate("tool_selection_onscreen_menu", "Polygon")
        )
        self.tool_selection_menu_selection_btn.setText(
            _translate("tool_selection_onscreen_menu", "Selection")
        )
        self.tool_selection_menu_erase.setText(
            _translate("tool_selection_onscreen_menu", "Eraser")
        )
        self.tool_selection_menu_auto_cut_btn.setText(
            _translate("tool_selection_onscreen_menu", "Magic\n" "Tool")
        )


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    tool_selection_onscreen_menu = QtWidgets.QDialog()
    ui = Ui_tool_selection_onscreen_menu()
    ui.setupUi(tool_selection_onscreen_menu)
    tool_selection_onscreen_menu.show()
    sys.exit(app.exec())
