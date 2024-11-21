# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\manos\Documents\popup_tool_menu.ui'
#
# Created by: PyQt6 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt6 import QtCore, QtGui, QtWidgets

"""
changes include:
added the installeventhandler for dialog and buttons
added the def to hadnle the enter event
change button state with def state handler
and finally change the stylesheet to handle enabled and disabled instad of normal and hover

"""


class Ui_tool_selection_onscreen_menu(QtWidgets.QDialog):
    tool_signal = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        super(Ui_tool_selection_onscreen_menu, self).__init__()
        self.enterButton = self.pressedButton = None
        self.selected_button = (
            "selection"  # available are: selection, polygon, lasso, auto
        )
        self.installEventFilter(self)
        Ui_tool_selection_onscreen_menu.tool_signal_to_main = self.tool_signal

    def setupUi(self, tool_selection_onscreen_menu):
        self.starting_pos = 0
        # Aded tp be transparent
        tool_selection_onscreen_menu.setWindowFlags(
            QtCore.Qt.WindowType.FramelessWindowHint
            | QtCore.Qt.WindowType.WindowStaysOnTopHint
        )
        tool_selection_onscreen_menu.setAttribute(
            QtCore.Qt.WidgetAttribute.WA_TranslucentBackground
        )

        tool_selection_onscreen_menu.setObjectName("tool_selection_onscreen_menu")
        tool_selection_onscreen_menu.resize(352, 107)
        tool_selection_onscreen_menu.setStyleSheet(
            "QPushButton{\n"
            'font: 14pt "Calibri";\n'
            "border-width: 1px;\n"
            "border-color:  rgb(40, 40, 40);\n"
            "border-style: solid;\n"
            "border-radius:0;\n"
            "    color: rgba(255, 255, 255,25);\n"
            "\n"
            "background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 rgba(102, 102, 102, 255), stop:1 rgba(90, 90, 90, 255));\n"
            "    background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 rgba(227, 227, 227, 255), stop:1 rgba(210, 210, 210, 255));\n"
            "}\n"
            "QPushButton:disabled{\n"
            "border-width: 1px;\n"
            "border-color:  rgb(255, 160, 0);\n"
            "border-style: solid;\n"
            "border-radius:0;\n"
            "    color: black;\n"
            "    background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 rgba(227, 227, 227, 255), stop:1 rgba(210, 210, 210, 255));\n"
            "\n"
            "}\n"
            "\n"
            "QPushButton#tool_selection_menu_auto_cut_btn{\n"
            "image: url(data/icons/icons_aa_tool/tool_selection_menu_auto_cut.png);\n"
            "}\n"
            "QPushButton#tool_selection_menu_auto_cut_btn:disabled{\n"
            "image: url();\n"
            "}\n"
            "QPushButton#tool_selection_menu_selection_btn{\n"
            "image: url(data/icons/icons_aa_tool/tool_selection_menu_selection.png);\n"
            "}\n"
            "QPushButton#tool_selection_menu_selection_btn:disabled{\n"
            "image: url();\n"
            "}\n"
            "QPushButton#tool_selection_menu_polygon_btn{\n"
            "image: url(data/icons/icons_aa_tool/tool_selection_menu_polygon.png);\n"
            "}\n"
            "QPushButton#tool_selection_menu_polygon_btn:disabled{\n"
            "image: url();\n"
            "}QPushButton#tool_selection_menu_lasso_btn{\n"
            "image: url(data/icons/icons_aa_tool/tool_selection_menu_selection – 1.png);\n"
            "}\n"
            "QPushButton#tool_selection_menu_lasso_btn:disabled{\n"
            "image: url();\n"
            "}\n"
            "\n"
            "\n"
            "\n"
            "\n"
            ""
        )
        self.beggin_dra_w_button_radio = QtWidgets.QRadioButton(
            tool_selection_onscreen_menu
        )
        self.beggin_dra_w_button_radio.setGeometry(QtCore.QRect(170, 90, 16, 17))
        self.beggin_dra_w_button_radio.setText("")
        self.beggin_dra_w_button_radio.setObjectName("beggin_dra_w_button_radio")
        self.tool_selection_menu_auto_cut_btn = QtWidgets.QPushButton(
            tool_selection_onscreen_menu
        )
        self.tool_selection_menu_auto_cut_btn.setGeometry(QtCore.QRect(70, 0, 91, 41))

        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(14)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.tool_selection_menu_auto_cut_btn.setFont(font)
        self.tool_selection_menu_auto_cut_btn.setStyleSheet("")
        self.tool_selection_menu_auto_cut_btn.setObjectName(
            "tool_selection_menu_auto_cut_btn"
        )
        self.tool_selection_menu_selection_btn = QtWidgets.QPushButton(
            tool_selection_onscreen_menu
        )
        self.tool_selection_menu_selection_btn.setGeometry(QtCore.QRect(190, 0, 91, 41))
        # self.tool_selection_menu_selection_btn.installEventFilter()

        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(14)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.tool_selection_menu_selection_btn.setFont(font)
        self.tool_selection_menu_selection_btn.setStyleSheet("")
        self.tool_selection_menu_selection_btn.setObjectName(
            "tool_selection_menu_selection_btn"
        )
        self.tool_selection_menu_lasso_btn = QtWidgets.QPushButton(
            tool_selection_onscreen_menu
        )
        self.tool_selection_menu_lasso_btn.setGeometry(QtCore.QRect(260, 60, 91, 41))
        # self.tool_selection_menu_lasso_btn.installEventFilter()

        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(14)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.tool_selection_menu_lasso_btn.setFont(font)
        self.tool_selection_menu_lasso_btn.setStyleSheet("")
        self.tool_selection_menu_lasso_btn.setObjectName(
            "tool_selection_menu_lasso_btn"
        )
        self.tool_selection_menu_polygon_btn = QtWidgets.QPushButton(
            tool_selection_onscreen_menu
        )
        self.tool_selection_menu_polygon_btn.setGeometry(QtCore.QRect(0, 60, 91, 41))
        # self.tool_selection_menu_polygon_btn.installEventFilter()

        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(14)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.tool_selection_menu_polygon_btn.setFont(font)
        self.tool_selection_menu_polygon_btn.setStyleSheet("")
        self.tool_selection_menu_polygon_btn.setObjectName(
            "tool_selection_menu_polygon_btn"
        )

        # install all event filters
        self.beggin_dra_w_button_radio.installEventFilter(self)
        self.tool_selection_menu_selection_btn.installEventFilter(self)
        self.tool_selection_menu_auto_cut_btn.installEventFilter(self)
        self.tool_selection_menu_lasso_btn.installEventFilter(self)
        self.tool_selection_menu_polygon_btn.installEventFilter(self)
        # set everything to enabled
        self.tool_selection_menu_selection_btn.setEnabled(True)
        self.tool_selection_menu_auto_cut_btn.setEnabled(True)
        self.tool_selection_menu_lasso_btn.setEnabled(True)
        self.tool_selection_menu_polygon_btn.setEnabled(True)
        # self.beggin_dra_w_button_radio.setAcceptDrops(False)
        # self.beggin_dra_w_button_radio.setAcceptDrops(True)
        # self.tool_selection_menu_polygon_btn.setMouseTracking(True)

        self.retranslateUi(tool_selection_onscreen_menu)
        QtCore.QMetaObject.connectSlotsByName(tool_selection_onscreen_menu)

    def retranslateUi(self, tool_selection_onscreen_menu):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("tool_selection_onscreen_menu", "Dialog"))
        self.tool_selection_menu_auto_cut_btn.setText(
            _translate("tool_selection_onscreen_menu", "Auto cut")
        )
        self.tool_selection_menu_selection_btn.setText(
            _translate("tool_selection_onscreen_menu", "Selection")
        )
        self.tool_selection_menu_lasso_btn.setText(
            _translate("tool_selection_onscreen_menu", "Lasso")
        )
        self.tool_selection_menu_polygon_btn.setText(
            _translate("tool_selection_onscreen_menu", "Polygon")
        )

    # @staticmethod
    def selected_button_handler(self, source):
        # assign the current button
        # self.setFocusPolicy(QtCore.Qt.FocusPolicy.StrongFocus)
        if source == self.tool_selection_menu_selection_btn:
            self.selected_button = "selection"
            self.tool_selection_menu_selection_btn.setEnabled(False)
            self.tool_selection_menu_auto_cut_btn.setEnabled(True)
            self.tool_selection_menu_lasso_btn.setEnabled(True)
            self.tool_selection_menu_polygon_btn.setEnabled(True)
        if source == self.tool_selection_menu_auto_cut_btn:
            self.selected_button = "auto"
            self.tool_selection_menu_selection_btn.setEnabled(True)
            self.tool_selection_menu_auto_cut_btn.setEnabled(False)
            self.tool_selection_menu_lasso_btn.setEnabled(True)
            self.tool_selection_menu_polygon_btn.setEnabled(True)
        if source == self.tool_selection_menu_lasso_btn:
            self.selected_button = "lasso"
            self.tool_selection_menu_selection_btn.setEnabled(True)
            self.tool_selection_menu_auto_cut_btn.setEnabled(True)
            self.tool_selection_menu_lasso_btn.setEnabled(False)
            self.tool_selection_menu_polygon_btn.setEnabled(True)
        if source == self.tool_selection_menu_polygon_btn:
            self.selected_button = "polygon"
            print("polygon_selected")
            self.tool_selection_menu_selection_btn.setEnabled(True)
            self.tool_selection_menu_auto_cut_btn.setEnabled(True)
            self.tool_selection_menu_lasso_btn.setEnabled(True)
            self.tool_selection_menu_polygon_btn.setEnabled(False)
        else:
            print("source does not match")
        self.tool_signal.emit()
        return

    def initilize_tools(self):
        self.pressedButton = self.beggin_dra_w_button_radio
        self.tool_selection_menu_selection_btn.setEnabled(True)
        self.tool_selection_menu_auto_cut_btn.setEnabled(True)
        self.tool_selection_menu_lasso_btn.setEnabled(True)
        self.tool_selection_menu_polygon_btn.setEnabled(True)

    def eventFilter(self, source, event):

        # if event.type() != QtCore.QEvent.None:

        # print("other one: ", event.type())
        if (
            event.type() == QtCore.QEvent.Type.MouseButtonPress
            and event.button() == QtCore.Qt.MouseButton.RightButton
        ):
            self.setFocus()
            self.pressedButton = source
            return super(Ui_tool_selection_onscreen_menu, self).eventFilter(
                source, event
            )

            # print('this stop')
        elif event.type() == QtCore.QEvent.Type.MouseMove:

            widget = QtWidgets.QApplication.widgetAt(event.globalPosition())
            # print("step1")
            if widget in (
                self.beggin_dra_w_button_radio,
                self.tool_selection_menu_polygon_btn,
                self.tool_selection_menu_lasso_btn,
                self.tool_selection_menu_selection_btn,
                self.tool_selection_menu_auto_cut_btn,
            ):
                # print("step2")
                if widget != self.pressedButton:
                    # print("step3")
                    if self.pressedButton != widget:
                        # print("step4")
                        # print(event.type())
                        self.enterButton = widget
                        self.selected_button_handler(widget)
                        Ui_tool_selection_onscreen_menu.tool_signal_to_main.emit()
                else:
                    self.enterButton = None
        # original was:
        return super(Ui_tool_selection_onscreen_menu, self).eventFilter(source, event)
        # return False
        # return super(Ui_tool_selection_onscreen_menu, self).eventFilter(source, event)

    # def mousePressEvent(self,QMouseEvent):
    #     if QtGui.QMouseEvent.button() == QtCore.Qt.MouseButton.RightButton:
    #         print("right button")


if __name__ == "__main__":
    pass
    # app = QtWidgets.QApplication(sys.argv)
    # tool_selection_onscreen_menu = QtWidgets.QDialog()
    # ui = Ui_tool_selection_onscreen_menu()
    # ui.setupUi(tool_selection_onscreen_menu)
    # # tool_selection_onscreen_menu.installEventFilter(tool_selection_onscreen_menu)
    # tool_selection_onscreen_menu.show()
    # sys.exit(app.exec())
