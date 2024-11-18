# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\manos\Documents\topfluov2\UiAssets\loginuiRegistration1.ui'
#
# Created by: PyQt6 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(461, 602)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Dialog.sizePolicy().hasHeightForWidth())
        Dialog.setSizePolicy(sizePolicy)
        Dialog.setMinimumSize(QtCore.QSize(461, 602))
        Dialog.setMaximumSize(QtCore.QSize(461, 602))
        Dialog.setStyleSheet(
            "        QToolTip  \n"
            "\n"
            "         {  \n"
            "              border: 1px solid black;  \n"
            "              background-color: #ffa02f;  \n"
            "              padding: 1px;  \n"
            "              border-radius: 3px;  \n"
            "              opacity: 100;  \n"
            "         }  \n"
            "           \n"
            "         QWidget  \n"
            "         {  \n"
            "             color: #b1b1b1;  \n"
            "            background-color: rgb(255, 255, 255);\n"
            "         }  \n"
            "           \n"
            "         QWidget:item:hover  \n"
            "         {  \n"
            "             background-color:QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #ffa02f, stop: 1 #d7801a);  \n"
            "             color: #000000;  \n"
            "         }  \n"
            "           \n"
            "         QWidget:item:selected  \n"
            "         {  \n"
            "             background-color: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #ffa02f, stop: 1 #d7801a);  \n"
            "         }  \n"
            "           \n"
            "         QMenuBar::item  \n"
            "         {  \n"
            "             background: transparent;  \n"
            "         }  \n"
            "           \n"
            "         QMenuBar::item:selected  \n"
            "         {  \n"
            "             background: transparent;  \n"
            "             border: 1px solid #ffaa00;  \n"
            "         }  \n"
            "           \n"
            "         QMenuBar::item:pressed  \n"
            "         {  \n"
            "             background: #444;  \n"
            "             border: 1px solid #000;  \n"
            "             background-color: QLinearGradient(  \n"
            "                 x1:0, y1:0,  \n"
            "                 x2:0, y2:1,  \n"
            "                 stop:1 #212121,  \n"
            "                 stop:0.4 #343434/*,  \n"
            "                 stop:0.2 #343434,  \n"
            "                 stop:0.1 #ffaa00*/  \n"
            "             );  \n"
            "             margin-bottom:-1px;  \n"
            "             padding-bottom:1px;  \n"
            "         }  \n"
            "           \n"
            "         QMenu  \n"
            "         {  \n"
            "             border: 1px solid #000;  \n"
            "         }  \n"
            "           \n"
            "         QMenu::item  \n"
            "         {  \n"
            "             padding: 2px 20px 2px 20px;  \n"
            "         }  \n"
            "           \n"
            "         QMenu::item:selected  \n"
            "         {  \n"
            "             color: #000000;  \n"
            "         }  \n"
            "           \n"
            "         QWidget:disabled  \n"
            "         {  \n"
            "             color: #404040;  \n"
            "             background-color: #323232;  \n"
            "         }  \n"
            "           \n"
            "         QAbstractItemView  \n"
            "         {  \n"
            "             background-color: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #4d4d4d, stop: 0.1 #646464, stop: 1 #5d5d5d);  \n"
            "         }  \n"
            "           \n"
            "         QWidget:focus  \n"
            "         {  \n"
            "             /*border: 2px solid QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #ffa02f, stop: 1 #d7801a);*/  \n"
            "         }  \n"
            "           \n"
            "         QLineEdit  \n"
            "         {  \n"
            "             background-color: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #4d4d4d, stop: 0 #646464, stop: 1 #5d5d5d);  \n"
            "             padding: 1px;  \n"
            "             border-style: solid;  \n"
            "             border: 1px solid #1e1e1e;  \n"
            "             border-radius: 5;  \n"
            "         }  \n"
            "           \n"
            "         QPushButton  \n"
            "         {  \n"
            "             color: #b1b1b1;  \n"
            "             background-color: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #565656, stop: 0.1 #525252, stop: 0.5 #4e4e4e, stop: 0.9 #4a4a4a, stop: 1 #464646);  \n"
            "             border-width: 1px;  \n"
            "             border-color: #1e1e1e;  \n"
            "             border-style: solid;  \n"
            "             border-radius: 6;  \n"
            "             padding: 3px;  \n"
            "             font-size: 12px;  \n"
            "             padding-left: 5px;  \n"
            "             padding-right: 5px;  \n"
            "         }  \n"
            "           \n"
            "         QPushButton:pressed  \n"
            "         {  \n"
            "             background-color: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #2d2d2d, stop: 0.1 #2b2b2b, stop: 0.5 #292929, stop: 0.9 #282828, stop: 1 #252525);  \n"
            "         }  \n"
            "           \n"
            "         QComboBox  \n"
            "         {  \n"
            "             selection-background-color: #ffaa00;  \n"
            "             background-color: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #565656, stop: 0.1 #525252, stop: 0.5 #4e4e4e, stop: 0.9 #4a4a4a, stop: 1 #464646);  \n"
            "             border-style: solid;  \n"
            "             border: 1px solid #1e1e1e;  \n"
            "             border-radius: 5;  \n"
            "         }  \n"
            "           \n"
            "         QComboBox:hover,QPushButton:hover  \n"
            "         {  \n"
            "             border: 2px solid QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #ffa02f, stop: 1 #d7801a);  \n"
            "         }  \n"
            "           \n"
            "           \n"
            "         QComboBox:on  \n"
            "         {  \n"
            "             padding-top: 3px;  \n"
            "             padding-left: 4px;  \n"
            "             background-color: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #2d2d2d, stop: 0.1 #2b2b2b, stop: 0.5 #292929, stop: 0.9 #282828, stop: 1 #252525);  \n"
            "             selection-background-color: #ffaa00;  \n"
            "         }  \n"
            "           \n"
            "         QComboBox QAbstractItemView  \n"
            "         {  \n"
            "             border: 2px solid darkgray;  \n"
            "             selection-background-color: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #ffa02f, stop: 1 #d7801a);  \n"
            "         }  \n"
            "           \n"
            "         QComboBox::drop-down  \n"
            "         {  \n"
            "              subcontrol-origin: padding;  \n"
            "              subcontrol-position: top right;  \n"
            "              width: 15px;  \n"
            "           \n"
            "              border-left-width: 0px;  \n"
            "              border-left-color: darkgray;  \n"
            "              border-left-style: solid; /* just a single line */  \n"
            "              border-top-right-radius: 3px; /* same radius as the QComboBox */  \n"
            "              border-bottom-right-radius: 3px;  \n"
            "          }  \n"
            "           \n"
            "         QComboBox::down-arrow  \n"
            "         {  \n"
            "              image: url(:/down_arrow.png);  \n"
            "         }  \n"
            "           \n"
            "         QGroupBox:focus  \n"
            "         {  \n"
            "         border: 2px solid QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #ffa02f, stop: 1 #d7801a);  \n"
            "         }  \n"
            "           \n"
            "         QTextEdit:focus  \n"
            "         {  \n"
            "             border: 2px solid QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #ffa02f, stop: 1 #d7801a);  \n"
            "         }  \n"
            "           \n"
            "         QScrollBar:horizontal {  \n"
            "              border: 1px solid #222222;  \n"
            "              background: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0.0 #121212, stop: 0.2 #282828, stop: 1 #484848);  \n"
            "              height: 7px;  \n"
            "              margin: 0px 16px 0 16px;  \n"
            "         }  \n"
            "           \n"
            "         QScrollBar::handle:horizontal  \n"
            "         {  \n"
            "               background: QLinearGradient( x1: 0, y1: 0, x2: 1, y2: 0, stop: 0 #ffa02f, stop: 0.5 #d7801a, stop: 1 #ffa02f);  \n"
            "               min-height: 20px;  \n"
            "               border-radius: 2px;  \n"
            "         }  \n"
            "           \n"
            "         QScrollBar::add-line:horizontal {  \n"
            "               border: 1px solid #1b1b19;  \n"
            "               border-radius: 2px;  \n"
            "               background: QLinearGradient( x1: 0, y1: 0, x2: 1, y2: 0, stop: 0 #ffa02f, stop: 1 #d7801a);  \n"
            "               width: 14px;  \n"
            "               subcontrol-position: right;  \n"
            "               subcontrol-origin: margin;  \n"
            "         }  \n"
            "           \n"
            "         QScrollBar::sub-line:horizontal {  \n"
            "               border: 1px solid #1b1b19;  \n"
            "               border-radius: 2px;  \n"
            "               background: QLinearGradient( x1: 0, y1: 0, x2: 1, y2: 0, stop: 0 #ffa02f, stop: 1 #d7801a);  \n"
            "               width: 14px;  \n"
            "              subcontrol-position: left;  \n"
            "              subcontrol-origin: margin;  \n"
            "         }  \n"
            "           \n"
            "         QScrollBar::right-arrow:horizontal, QScrollBar::left-arrow:horizontal  \n"
            "         {  \n"
            "               border: 1px solid black;  \n"
            "               width: 1px;  \n"
            "               height: 1px;  \n"
            "               background: white;  \n"
            "         }  \n"
            "           \n"
            "         QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal  \n"
            "         {  \n"
            "               background: none;  \n"
            "         }  \n"
            "           \n"
            "         QScrollBar:vertical  \n"
            "         {  \n"
            "               background: QLinearGradient( x1: 0, y1: 0, x2: 1, y2: 0, stop: 0.0 #121212, stop: 0.2 #282828, stop: 1 #484848);  \n"
            "               width: 7px;  \n"
            "               margin: 16px 0 16px 0;  \n"
            "               border: 1px solid #222222;  \n"
            "         }  \n"
            "           \n"
            "         QScrollBar::handle:vertical  \n"
            "         {  \n"
            "               background: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #ffa02f, stop: 0.5 #d7801a, stop: 1 #ffa02f);  \n"
            "               min-height: 20px;  \n"
            "               border-radius: 2px;  \n"
            "         }  \n"
            "           \n"
            "         QScrollBar::add-line:vertical  \n"
            "         {  \n"
            "               border: 1px solid #1b1b19;  \n"
            "               border-radius: 2px;  \n"
            "               background: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #ffa02f, stop: 1 #d7801a);  \n"
            "               height: 14px;  \n"
            "               subcontrol-position: bottom;  \n"
            "               subcontrol-origin: margin;  \n"
            "         }  \n"
            "           \n"
            "         QScrollBar::sub-line:vertical  \n"
            "         {  \n"
            "               border: 1px solid #1b1b19;  \n"
            "               border-radius: 2px;  \n"
            "               background: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #d7801a, stop: 1 #ffa02f);  \n"
            "               height: 14px;  \n"
            "               subcontrol-position: top;  \n"
            "               subcontrol-origin: margin;  \n"
            "         }  \n"
            "           \n"
            "         QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical  \n"
            "         {  \n"
            "               border: 1px solid black;  \n"
            "               width: 1px;  \n"
            "               height: 1px;  \n"
            "               background: white;  \n"
            "         }  \n"
            "           \n"
            "           \n"
            "         QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical  \n"
            "         {  \n"
            "               background: none;  \n"
            "         }  \n"
            "           \n"
            "         QTextEdit  \n"
            "         {  \n"
            "             background-color: #242424;  \n"
            "         }  \n"
            "           \n"
            "         QPlainTextEdit  \n"
            "         {  \n"
            "             background-color: #242424;  \n"
            "         }  \n"
            "           \n"
            "         QHeaderView::section  \n"
            "         {  \n"
            "             background-color: QLinearGradient(x1:0, y1:0, x2:0, y2:1, stop:0 #616161, stop: 0.5 #505050, stop: 0.6 #434343, stop:1 #656565);  \n"
            "             color: white;  \n"
            "             padding-left: 4px;  \n"
            "             border: 1px solid #6c6c6c;  \n"
            "         }  \n"
            "           \n"
            "\n"
            "         QDockWidget::title  \n"
            "         {  \n"
            "             text-align: center;  \n"
            "             spacing: 3px; /* spacing between items in the tool bar */  \n"
            "             background-color: QLinearGradient(x1:0, y1:0, x2:0, y2:1, stop:0 #323232, stop: 0.5 #242424, stop:1 #323232);  \n"
            "         }  \n"
            "           \n"
            "         QDockWidget::close-button, QDockWidget::float-button  \n"
            "         {  \n"
            "             text-align: center;  \n"
            "             spacing: 1px; /* spacing between items in the tool bar */  \n"
            "             background-color: QLinearGradient(x1:0, y1:0, x2:0, y2:1, stop:0 #323232, stop: 0.5 #242424, stop:1 #323232);  \n"
            "         }  \n"
            "           \n"
            "         QDockWidget::close-button:hover, QDockWidget::float-button:hover  \n"
            "         {  \n"
            "             background: #242424;  \n"
            "         }  \n"
            "           \n"
            "         QDockWidget::close-button:pressed, QDockWidget::float-button:pressed  \n"
            "         {  \n"
            "             padding: 1px -1px -1px 1px;  \n"
            "         }  \n"
            "           \n"
            "         QMainWindow::separator  \n"
            "         {  \n"
            "             background-color: QLinearGradient(x1:0, y1:0, x2:0, y2:1, stop:0 #161616, stop: 0.5 #151515, stop: 0.6 #212121, stop:1 #343434);  \n"
            "             color: white;  \n"
            "             padding-left: 4px;  \n"
            "             border: 1px solid #4c4c4c;  \n"
            "             spacing: 3px; /* spacing between items in the tool bar */  \n"
            "         }  \n"
            "           \n"
            "         QMainWindow::separator:hover  \n"
            "         {  \n"
            "           \n"
            "             background-color: QLinearGradient(x1:0, y1:0, x2:0, y2:1, stop:0 #d7801a, stop:0.5 #b56c17 stop:1 #ffa02f);  \n"
            "             color: white;  \n"
            "             padding-left: 4px;  \n"
            "             border: 1px solid #6c6c6c;  \n"
            "             spacing: 3px; /* spacing between items in the tool bar */  \n"
            "         }  \n"
            "           \n"
            "         QToolBar::handle  \n"
            "         {  \n"
            "              spacing: 3px; /* spacing between items in the tool bar */  \n"
            "              background: url(:/images/handle.png);  \n"
            "         }  \n"
            "           \n"
            "         QMenu::separator  \n"
            "         {  \n"
            "             height: 2px;  \n"
            "             background-color: QLinearGradient(x1:0, y1:0, x2:0, y2:1, stop:0 #161616, stop: 0.5 #151515, stop: 0.6 #212121, stop:1 #343434);  \n"
            "             color: white;  \n"
            "             padding-left: 4px;  \n"
            "             margin-left: 10px;  \n"
            "             margin-right: 5px;  \n"
            "         }  \n"
            "           \n"
            "         QProgressBar  \n"
            "         {  \n"
            "             border: 2px solid grey;  \n"
            "             border-radius: 5px;  \n"
            "             text-align: center;  \n"
            "         }  \n"
            "           \n"
            "         QProgressBar::chunk  \n"
            "         {  \n"
            "             background-color: #d7801a;  \n"
            "             width: 2.15px;  \n"
            "             margin: 0.5px;  \n"
            "         }  \n"
            "           \n"
            "         QTabBar::tab {  \n"
            "             color: #b1b1b1;  \n"
            "             border: 1px solid #444;  \n"
            "             border-bottom-style: none;  \n"
            "             background-color: #323232;  \n"
            "             padding-left: 10px;  \n"
            "             padding-right: 10px;  \n"
            "             padding-top: 3px;  \n"
            "             padding-bottom: 2px;  \n"
            "             margin-right: -1px;  \n"
            "         }  \n"
            "           \n"
            "         QTabWidget::pane {  \n"
            "             border: 1px solid #444;  \n"
            "             top: 1px;  \n"
            "         }  \n"
            "           \n"
            "         QTabBar::tab:last  \n"
            "         {  \n"
            "             margin-right: 0; /* the last selected tab has nothing to overlap with on the right */  \n"
            "             border-top-right-radius: 3px;  \n"
            "         }  \n"
            "           \n"
            "         QTabBar::tab:first:!selected  \n"
            "         {  \n"
            "          margin-left: 0px; /* the last selected tab has nothing to overlap with on the right */  \n"
            "           \n"
            "           \n"
            "             border-top-left-radius: 3px;  \n"
            "         }  \n"
            "           \n"
            "         QTabBar::tab:!selected  \n"
            "         {  \n"
            "             color: #b1b1b1;  \n"
            "             border-bottom-style: solid;  \n"
            "             margin-top: 3px;  \n"
            "             background-color: QLinearGradient(x1:0, y1:0, x2:0, y2:1, stop:1 #212121, stop:.4 #1c0009);  \n"
            "         }  \n"
            "           \n"
            "         QTabBar::tab:selected  \n"
            "         {  \n"
            "             border-top-left-radius: 3px;  \n"
            "             border-top-right-radius: 3px;  \n"
            "             margin-bottom: 0px;  \n"
            "         }  \n"
            "           \n"
            "         QTabBar::tab:!selected:hover  \n"
            "         {  \n"
            "             /*border-top: 2px solid #ffaa00;  \n"
            "             padding-bottom: 3px;*/  \n"
            "             border-top-left-radius: 3px;  \n"
            "             border-top-right-radius: 3px;  \n"
            "             background-color: QLinearGradient(x1:0, y1:0, x2:0, y2:1, stop:1 #212121, stop:0.4 #350012, stop:0.2 #4e001a, stop:0.1 #4e001a);  \n"
            "         }  \n"
            "           \n"
            "         QRadioButton::indicator:checked, QRadioButton::indicator:unchecked{  \n"
            "             color: #b1b1b1;  \n"
            "             background-color: #323232;  \n"
            "             border: 1px solid #b1b1b1;  \n"
            "             border-radius: 6px;  \n"
            "         }  \n"
            "           \n"
            "         QRadioButton::indicator:checked  \n"
            "         {  \n"
            "             background-color: qradialgradient(  \n"
            "                 cx: 0.5, cy: 0.5,  \n"
            "                 fx: 0.5, fy: 0.5,  \n"
            "                 radius: 1.0,  \n"
            "                 stop: 0.25 #ffaa00,  \n"
            "                 stop: 0.3 #323232  \n"
            "             );  \n"
            "         }  \n"
            "           \n"
            "         QCheckBox::indicator{  \n"
            "             color: #b1b1b1;  \n"
            "             background-color: #323232;  \n"
            "             border: 1px solid #b1b1b1;  \n"
            "             width: 9px;  \n"
            "             height: 9px;  \n"
            "         }  \n"
            "           \n"
            "         QRadioButton::indicator  \n"
            "         {  \n"
            "             border-radius: 6px;  \n"
            "         }  \n"
            "           \n"
            "         QRadioButton::indicator:hover, QCheckBox::indicator:hover  \n"
            "         {  \n"
            "             border: 1px solid #ffaa00;  \n"
            "         }  \n"
            "           \n"
            "         QCheckBox::indicator:disabled, QRadioButton::indicator:disabled  \n"
            "         {  \n"
            "             border: 1px solid #444;  \n"
            "         }  \n"
            "\n"
            "         QTableWidget::item {  \n"
            "              background-color: #FFFFFF  \n"
            "          }  \n"
            "\n"
            "         QTabBar::tab { height: 30px; width: 200px; }  \n"
            "          \n"
            "         QScrollBar { \n"
            "             border: rgba(255, 255, 255,0); \n"
            "         } \n"
            "\n"
            "         QGroupBox {  \n"
            "             border: rgba(255, 255, 255,0); \n"
            "         }  \n"
            "         QScrollArea { \n"
            "         border: rgba(255, 255, 255,0); \n"
            "          }  +     \n"
            "        QPushButton#Add_mask_btn{\n"
            "            background-color: #E5E5E5;\n"
            "        }\n"
            "        QPushButton#Add_mask_btn:hover{\n"
            "            border-color: #000000;\n"
            "            background-color: #CCCCCC;\n"
            "        }\n"
            "\n"
            "        QPushButton#Add_mask_btn:checked{\n"
            "            border-color: #2A828F;\n"
            "            background-color: #2A828F;\n"
            "        }\n"
            "        QPushButton#Delete_selected_btn{\n"
            "            background-color: #E5E5E5;\n"
            "        }\n"
            "        QPushButton#Delete_selected_btn:hover{\n"
            "            border-color: #000000;\n"
            "            background-color: #CCCCCC;\n"
            "        }\n"
            "\n"
            "        QDockWidget::title{\n"
            "        background-color: QLinearGradient(x1:0, y1:0, x2:0, y2:1, stop:0 #273232, stop: 0.5 #242424, stop:1 #242424);\n"
            "        }\n"
            "        QDockWidget::close-button, QDockWidget::float-button{\n"
            "        color: #FFFFFF\n"
            "        background-color:  #273232\n"
            "        }\n"
            "        QDockWidget::close-button:hover, QDockWidget::float-button:hover{\n"
            "        color: #FFFFFF\n"
            "        background-color:  #273232   \n"
            "        }\n"
            "\n"
            "        QSlider::groove{\n"
            "        background-color: white\n"
            "        border: 0px solid black\n"
            "        height: 5px\n"
            "        border-radius: 1px\n"
            "        }\n"
            "\n"
            "        QSlider::handle{\n"
            "        background-color: white;\n"
            "        border: 2px solid black; \n"
            "        width: 16px; \n"
            "        height: 20px; \n"
            "        line-height: 20px; \n"
            "        margin-top: -10px; \n"
            "        margin-bottom: -10px; \n"
            "        border-radius: 10px;\n"
            "        \n"
            "        }\n"
            "        QGroupBox {\n"
            "            border: 1px solid;\n"
            "            border-color: rgb(20, 20, 20);\n"
            "            margin-top: 20px;\n"
            "            border-top-left-radius: 15px;\n"
            "            border-top-right-radius:15px;\n"
            "            border-bottom-left-radius: 15px;\n"
            "            border-bottom-right-radius: 15px;\n"
            "            background-color: rgb(90, 90, 90);\n"
            "        }\n"
            "        QGroupBox::title {\n"
            "            font-size: 12px;\n"
            "            border-top-color: rgb(255, 255, 255);\n"
            "            subcontrol-origin: margin;\n"
            "            subcontrol-position: top left;\n"
            "            border-top-left-radius: 15px;\n"
            "            border-top-right-radius:15px;\n"
            "            padding: 2px 10px;\n"
            "            background-color: rgba(255, 255, 255,0);\n"
            "            color:rgba(255, 255, 255,220);\n"
            "        }\n"
            "\n"
            "\n"
            "        QGroupBox::indicator{\n"
            "        background-color: rgba(0, 170, 127,0);\n"
            "        color: rgba(85, 255, 0,0);\n"
            "        }\n"
            "    \n"
            "\n"
            "\n"
            "\n"
            "\n"
            "\n"
            "\n"
            "\n"
            "\n"
            "\n"
            "\n"
            "\n"
            "\n"
            "        "
        )
        self.gridLayout_4 = QtWidgets.QGridLayout(Dialog)
        self.gridLayout_4.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_4.setSpacing(0)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.widget = QtWidgets.QWidget(Dialog)
        self.widget.setObjectName("widget")
        self.gridLayout_5 = QtWidgets.QGridLayout(self.widget)
        self.gridLayout_5.setContentsMargins(100, 40, 100, 58)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.gridLayout_3 = QtWidgets.QGridLayout()
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.label_8 = QtWidgets.QLabel(self.widget)
        self.label_8.setMaximumSize(QtCore.QSize(16777215, 20))
        self.label_8.setStyleSheet("color: rgb(70, 70, 70);")
        self.label_8.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignBottom
            | QtCore.Qt.AlignmentFlag.AlignLeading
            | QtCore.Qt.AlignmentFlag.AlignLeft
        )
        self.label_8.setObjectName("label_8")
        self.gridLayout_3.addWidget(self.label_8, 12, 0, 1, 3)
        self.pushButton_back = QtWidgets.QPushButton(self.widget)
        self.pushButton_back.setMinimumSize(QtCore.QSize(0, 40))
        self.pushButton_back.setMaximumSize(QtCore.QSize(50, 16777215))
        self.pushButton_back.setStyleSheet(
            "         QPushButton  \n"
            "         {  \n"
            "             color:rgb(215, 215, 215);\n"
            "             background-color: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #2d2d2d, stop: 0.1 #2b2b2b, stop: 0.5 #292929, stop: 0.9 #282828, stop: 1 #252525);  \n"
            "             border-width: 2px;  \n"
            "             border-color: #1e1e1e;  \n"
            "             border-style: solid;  \n"
            "             border-radius: 6;  \n"
            "             padding: 3px;  \n"
            "             font-size: 17px;  \n"
            "             padding-left: 10px;  \n"
            "             padding-right: 10px;  \n"
            "         }  \n"
            "QPushButton:hover{  \n"
            "\n"
            "color:rgb(255, 255, 255);\n"
            "}\n"
            "         QPushButton:pressed  \n"
            "         {  \n"
            "             background-color: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #2d2d2d, stop: 0.1 #2b2b2b, stop: 0.5 #292929, stop: 0.9 #282828, stop: 1 #252525);  \n"
            "         }  "
        )
        self.pushButton_back.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(
            QtGui.QPixmap(
                "C:\\Users\\manos\\Documents\\topfluov2\\UiAssets\\../data/icons/arrow-leftcustom1.png"
            ),
            QtGui.QIcon.Mode.Normal,
            QtGui.QIcon.State.Off,
        )
        self.pushButton_back.setIcon(icon)
        self.pushButton_back.setIconSize(QtCore.QSize(30, 30))
        self.pushButton_back.setObjectName("pushButton_back")
        self.gridLayout_3.addWidget(self.pushButton_back, 16, 2, 1, 1)
        self.ActivationLabel = QtWidgets.QLabel(self.widget)
        self.ActivationLabel.setMinimumSize(QtCore.QSize(0, 82))
        self.ActivationLabel.setMaximumSize(QtCore.QSize(16777215, 100))
        font = QtGui.QFont()
        font.setPointSize(19)
        self.ActivationLabel.setFont(font)
        self.ActivationLabel.setStyleSheet("color: rgb(70, 70, 70);")
        self.ActivationLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.ActivationLabel.setObjectName("ActivationLabel")
        self.gridLayout_3.addWidget(self.ActivationLabel, 0, 0, 1, 3)
        spacerItem = QtWidgets.QSpacerItem(
            20,
            37,
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Fixed,
        )
        self.gridLayout_3.addItem(spacerItem, 14, 0, 1, 1)
        self.ActivatePushButton = QtWidgets.QPushButton(self.widget)
        self.ActivatePushButton.setMinimumSize(QtCore.QSize(0, 40))
        self.ActivatePushButton.setMaximumSize(QtCore.QSize(100000, 16777215))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.ActivatePushButton.setFont(font)
        self.ActivatePushButton.setStyleSheet(
            "         QPushButton  \n"
            "         {  \n"
            "             color:rgb(215, 215, 215);\n"
            "             background-color: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #2d2d2d, stop: 0.1 #2b2b2b, stop: 0.5 #292929, stop: 0.9 #282828, stop: 1 #252525);  \n"
            "             border-width: 2px;  \n"
            "             border-color: #1e1e1e;  \n"
            "             border-style: solid;  \n"
            "             border-radius: 6;  \n"
            "             padding: 3px;  \n"
            "             font-size: 17px;  \n"
            "             padding-left: 10px;  \n"
            "             padding-right: 10px;  \n"
            "         }  \n"
            "QPushButton:hover{  \n"
            "\n"
            "color:rgb(255, 255, 255);\n"
            "}\n"
            "         QPushButton:pressed  \n"
            "         {  \n"
            "             background-color: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #2d2d2d, stop: 0.1 #2b2b2b, stop: 0.5 #292929, stop: 0.9 #282828, stop: 1 #252525);  \n"
            "         }  "
        )
        self.ActivatePushButton.setObjectName("ActivatePushButton")
        self.gridLayout_3.addWidget(self.ActivatePushButton, 16, 0, 1, 2)
        self.label_5 = QtWidgets.QLabel(self.widget)
        self.label_5.setMaximumSize(QtCore.QSize(16777215, 20))
        self.label_5.setStyleSheet("color: rgb(70, 70, 70);")
        self.label_5.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignBottom
            | QtCore.Qt.AlignmentFlag.AlignLeading
            | QtCore.Qt.AlignmentFlag.AlignLeft
        )
        self.label_5.setObjectName("label_5")
        self.gridLayout_3.addWidget(self.label_5, 6, 0, 1, 3)
        self.label_3 = QtWidgets.QLabel(self.widget)
        self.label_3.setMaximumSize(QtCore.QSize(16777215, 20))
        self.label_3.setStyleSheet("color: rgb(70, 70, 70);")
        self.label_3.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignBottom
            | QtCore.Qt.AlignmentFlag.AlignLeading
            | QtCore.Qt.AlignmentFlag.AlignLeft
        )
        self.label_3.setObjectName("label_3")
        self.gridLayout_3.addWidget(self.label_3, 2, 0, 1, 3)
        self.label_4 = QtWidgets.QLabel(self.widget)
        self.label_4.setMaximumSize(QtCore.QSize(16777215, 20))
        self.label_4.setStyleSheet("color: rgb(70, 70, 70);")
        self.label_4.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignBottom
            | QtCore.Qt.AlignmentFlag.AlignLeading
            | QtCore.Qt.AlignmentFlag.AlignLeft
        )
        self.label_4.setObjectName("label_4")
        self.gridLayout_3.addWidget(self.label_4, 4, 0, 1, 3)
        self.label_7 = QtWidgets.QLabel(self.widget)
        self.label_7.setMaximumSize(QtCore.QSize(16777215, 20))
        self.label_7.setStyleSheet("color: rgb(70, 70, 70);")
        self.label_7.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignBottom
            | QtCore.Qt.AlignmentFlag.AlignLeading
            | QtCore.Qt.AlignmentFlag.AlignLeft
        )
        self.label_7.setObjectName("label_7")
        self.gridLayout_3.addWidget(self.label_7, 10, 0, 1, 3)
        self.label_6 = QtWidgets.QLabel(self.widget)
        self.label_6.setMaximumSize(QtCore.QSize(16777215, 20))
        self.label_6.setStyleSheet("color: rgb(70, 70, 70);")
        self.label_6.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignBottom
            | QtCore.Qt.AlignmentFlag.AlignLeading
            | QtCore.Qt.AlignmentFlag.AlignLeft
        )
        self.label_6.setObjectName("label_6")
        self.gridLayout_3.addWidget(self.label_6, 8, 0, 1, 3)
        self.lineEdit_2 = QtWidgets.QLineEdit(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_2.sizePolicy().hasHeightForWidth())
        self.lineEdit_2.setSizePolicy(sizePolicy)
        self.lineEdit_2.setMaximumSize(QtCore.QSize(16777215, 26))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)
        self.lineEdit_2.setFont(font)
        self.lineEdit_2.setStyleSheet(
            "         QLineEdit  \n"
            "\n"
            "         {  \n"
            "\n"
            "                color: rgb(90,90, 90);\n"
            "               border: 0px solid black;  \n"
            "            border-bottom: 1px solid rgba(0, 0, 0,50);\n"
            "\n"
            "              background-color: #ffa02f;  \n"
            "              padding: 1px;  \n"
            "              border-radius: 0px;  \n"
            "              opacity: 100;  \n"
            "             background-color: rgba(85, 85, 85,0);\n"
            "         }  \n"
            "         QLineEdit:hover\n"
            "\n"
            "         {  \n"
            "               border: 0px solid black;  \n"
            "            border-bottom: 1px solid rgba(0, 0, 0,200);\n"
            "    \n"
            "              background-color:  rgb(255, 85, 255);\n"
            "\n"
            "              padding: 1px;  \n"
            "              border-radius: 0px;  \n"
            "              opacity: 100;  \n"
            "             background-color: rgba(85, 85, 85,0);\n"
            "         }  \n"
            "         QLineEdit:focus\n"
            "\n"
            "         {  \n"
            "               border: 0px solid black;  \n"
            "                border-bottom: 1px solid  rgba(0, 0, 200);  \n"
            "              background-color: #ffa02f;  \n"
            "              padding: 1px;  \n"
            "              border-radius: 0px;  \n"
            "              opacity: 100;  \n"
            "             background-color: rgba(85, 85, 85,0);\n"
            "         }  \n"
            ""
        )
        self.lineEdit_2.setInputMethodHints(QtCore.Qt.InputMethodHint.ImhNone)
        self.lineEdit_2.setEchoMode(QtWidgets.QLineEdit.EchoMode.Normal)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.gridLayout_3.addWidget(self.lineEdit_2, 13, 0, 1, 3)
        self.lineEdit_3 = QtWidgets.QLineEdit(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_3.sizePolicy().hasHeightForWidth())
        self.lineEdit_3.setSizePolicy(sizePolicy)
        self.lineEdit_3.setMaximumSize(QtCore.QSize(16777215, 26))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)
        self.lineEdit_3.setFont(font)
        self.lineEdit_3.setStyleSheet(
            "         QLineEdit  \n"
            "\n"
            "         {  \n"
            "\n"
            "                color: rgb(90,90, 90);\n"
            "               border: 0px solid black;  \n"
            "            border-bottom: 1px solid rgba(0, 0, 0,50);\n"
            "\n"
            "              background-color: #ffa02f;  \n"
            "              padding: 1px;  \n"
            "              border-radius: 0px;  \n"
            "              opacity: 100;  \n"
            "             background-color: rgba(85, 85, 85,0);\n"
            "         }  \n"
            "         QLineEdit:hover\n"
            "\n"
            "         {  \n"
            "               border: 0px solid black;  \n"
            "            border-bottom: 1px solid rgba(0, 0, 0,200);\n"
            "    \n"
            "              background-color:  rgb(255, 85, 255);\n"
            "\n"
            "              padding: 1px;  \n"
            "              border-radius: 0px;  \n"
            "              opacity: 100;  \n"
            "             background-color: rgba(85, 85, 85,0);\n"
            "         }  \n"
            "         QLineEdit:focus\n"
            "\n"
            "         {  \n"
            "               border: 0px solid black;  \n"
            "                border-bottom: 1px solid  rgba(0, 0, 200);  \n"
            "              background-color: #ffa02f;  \n"
            "              padding: 1px;  \n"
            "              border-radius: 0px;  \n"
            "              opacity: 100;  \n"
            "             background-color: rgba(85, 85, 85,0);\n"
            "         }  \n"
            ""
        )
        self.lineEdit_3.setInputMethodHints(QtCore.Qt.InputMethodHint.ImhNone)
        self.lineEdit_3.setEchoMode(QtWidgets.QLineEdit.EchoMode.Normal)
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.gridLayout_3.addWidget(self.lineEdit_3, 11, 0, 1, 3)
        self.lineEdit_4 = QtWidgets.QLineEdit(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_4.sizePolicy().hasHeightForWidth())
        self.lineEdit_4.setSizePolicy(sizePolicy)
        self.lineEdit_4.setMaximumSize(QtCore.QSize(16777215, 26))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)
        self.lineEdit_4.setFont(font)
        self.lineEdit_4.setStyleSheet(
            "         QLineEdit  \n"
            "\n"
            "         {  \n"
            "\n"
            "                color: rgb(90,90, 90);\n"
            "               border: 0px solid black;  \n"
            "            border-bottom: 1px solid rgba(0, 0, 0,50);\n"
            "\n"
            "              background-color: #ffa02f;  \n"
            "              padding: 1px;  \n"
            "              border-radius: 0px;  \n"
            "              opacity: 100;  \n"
            "             background-color: rgba(85, 85, 85,0);\n"
            "         }  \n"
            "         QLineEdit:hover\n"
            "\n"
            "         {  \n"
            "               border: 0px solid black;  \n"
            "            border-bottom: 1px solid rgba(0, 0, 0,200);\n"
            "    \n"
            "              background-color:  rgb(255, 85, 255);\n"
            "\n"
            "              padding: 1px;  \n"
            "              border-radius: 0px;  \n"
            "              opacity: 100;  \n"
            "             background-color: rgba(85, 85, 85,0);\n"
            "         }  \n"
            "         QLineEdit:focus\n"
            "\n"
            "         {  \n"
            "               border: 0px solid black;  \n"
            "                border-bottom: 1px solid  rgba(0, 0, 200);  \n"
            "              background-color: #ffa02f;  \n"
            "              padding: 1px;  \n"
            "              border-radius: 0px;  \n"
            "              opacity: 100;  \n"
            "             background-color: rgba(85, 85, 85,0);\n"
            "         }  \n"
            ""
        )
        self.lineEdit_4.setInputMethodHints(
            QtCore.Qt.InputMethodHint.ImhHiddenText
            | QtCore.Qt.InputMethodHint.ImhNoAutoUppercase
            | QtCore.Qt.InputMethodHint.ImhNoPredictiveText
            | QtCore.Qt.InputMethodHint.ImhSensitiveData
        )
        self.lineEdit_4.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
        self.lineEdit_4.setObjectName("lineEdit_4")
        self.gridLayout_3.addWidget(self.lineEdit_4, 9, 0, 1, 3)
        self.lineEdit_5 = QtWidgets.QLineEdit(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_5.sizePolicy().hasHeightForWidth())
        self.lineEdit_5.setSizePolicy(sizePolicy)
        self.lineEdit_5.setMaximumSize(QtCore.QSize(16777215, 26))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)
        self.lineEdit_5.setFont(font)
        self.lineEdit_5.setStyleSheet(
            "         QLineEdit  \n"
            "\n"
            "         {  \n"
            "\n"
            "                color: rgb(90,90, 90);\n"
            "               border: 0px solid black;  \n"
            "            border-bottom: 1px solid rgba(0, 0, 0,50);\n"
            "\n"
            "              background-color: #ffa02f;  \n"
            "              padding: 1px;  \n"
            "              border-radius: 0px;  \n"
            "              opacity: 100;  \n"
            "             background-color: rgba(85, 85, 85,0);\n"
            "         }  \n"
            "         QLineEdit:hover\n"
            "\n"
            "         {  \n"
            "               border: 0px solid black;  \n"
            "            border-bottom: 1px solid rgba(0, 0, 0,200);\n"
            "    \n"
            "              background-color:  rgb(255, 85, 255);\n"
            "\n"
            "              padding: 1px;  \n"
            "              border-radius: 0px;  \n"
            "              opacity: 100;  \n"
            "             background-color: rgba(85, 85, 85,0);\n"
            "         }  \n"
            "         QLineEdit:focus\n"
            "\n"
            "         {  \n"
            "               border: 0px solid black;  \n"
            "                border-bottom: 1px solid  rgba(0, 0, 200);  \n"
            "              background-color: #ffa02f;  \n"
            "              padding: 1px;  \n"
            "              border-radius: 0px;  \n"
            "              opacity: 100;  \n"
            "             background-color: rgba(85, 85, 85,0);\n"
            "         }  \n"
            ""
        )
        self.lineEdit_5.setInputMethodHints(QtCore.Qt.InputMethodHint.ImhNone)
        self.lineEdit_5.setEchoMode(QtWidgets.QLineEdit.EchoMode.Normal)
        self.lineEdit_5.setObjectName("lineEdit_5")
        self.gridLayout_3.addWidget(self.lineEdit_5, 7, 0, 1, 3)
        self.lineEdit_6 = QtWidgets.QLineEdit(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_6.sizePolicy().hasHeightForWidth())
        self.lineEdit_6.setSizePolicy(sizePolicy)
        self.lineEdit_6.setMaximumSize(QtCore.QSize(16777215, 26))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)
        self.lineEdit_6.setFont(font)
        self.lineEdit_6.setStyleSheet(
            "         QLineEdit  \n"
            "\n"
            "         {  \n"
            "\n"
            "                color: rgb(90,90, 90);\n"
            "               border: 0px solid black;  \n"
            "            border-bottom: 1px solid rgba(0, 0, 0,50);\n"
            "\n"
            "              background-color: #ffa02f;  \n"
            "              padding: 1px;  \n"
            "              border-radius: 0px;  \n"
            "              opacity: 100;  \n"
            "             background-color: rgba(85, 85, 85,0);\n"
            "         }  \n"
            "         QLineEdit:hover\n"
            "\n"
            "         {  \n"
            "               border: 0px solid black;  \n"
            "            border-bottom: 1px solid rgba(0, 0, 0,200);\n"
            "    \n"
            "              background-color:  rgb(255, 85, 255);\n"
            "\n"
            "              padding: 1px;  \n"
            "              border-radius: 0px;  \n"
            "              opacity: 100;  \n"
            "             background-color: rgba(85, 85, 85,0);\n"
            "         }  \n"
            "         QLineEdit:focus\n"
            "\n"
            "         {  \n"
            "               border: 0px solid black;  \n"
            "                border-bottom: 1px solid  rgba(0, 0, 200);  \n"
            "              background-color: #ffa02f;  \n"
            "              padding: 1px;  \n"
            "              border-radius: 0px;  \n"
            "              opacity: 100;  \n"
            "             background-color: rgba(85, 85, 85,0);\n"
            "         }  \n"
            ""
        )
        self.lineEdit_6.setInputMethodHints(QtCore.Qt.InputMethodHint.ImhNone)
        self.lineEdit_6.setEchoMode(QtWidgets.QLineEdit.EchoMode.Normal)
        self.lineEdit_6.setObjectName("lineEdit_6")
        self.gridLayout_3.addWidget(self.lineEdit_6, 5, 0, 1, 3)
        self.lineEdit = QtWidgets.QLineEdit(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit.sizePolicy().hasHeightForWidth())
        self.lineEdit.setSizePolicy(sizePolicy)
        self.lineEdit.setMaximumSize(QtCore.QSize(16777215, 26))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)
        self.lineEdit.setFont(font)
        self.lineEdit.setStyleSheet(
            "         QLineEdit  \n"
            "\n"
            "         {  \n"
            "\n"
            "                color: rgb(90,90, 90);\n"
            "               border: 0px solid black;  \n"
            "            border-bottom: 1px solid rgba(0, 0, 0,50);\n"
            "\n"
            "              background-color: #ffa02f;  \n"
            "              padding: 1px;  \n"
            "              border-radius: 0px;  \n"
            "              opacity: 100;  \n"
            "             background-color: rgba(85, 85, 85,0);\n"
            "         }  \n"
            "         QLineEdit:hover\n"
            "\n"
            "         {  \n"
            "               border: 0px solid black;  \n"
            "            border-bottom: 1px solid rgba(0, 0, 0,200);\n"
            "    \n"
            "              background-color:  rgb(255, 85, 255);\n"
            "\n"
            "              padding: 1px;  \n"
            "              border-radius: 0px;  \n"
            "              opacity: 100;  \n"
            "             background-color: rgba(85, 85, 85,0);\n"
            "         }  \n"
            "         QLineEdit:focus\n"
            "\n"
            "         {  \n"
            "               border: 0px solid black;  \n"
            "                border-bottom: 1px solid  rgba(0, 0, 200);  \n"
            "              background-color: #ffa02f;  \n"
            "              padding: 1px;  \n"
            "              border-radius: 0px;  \n"
            "              opacity: 100;  \n"
            "             background-color: rgba(85, 85, 85,0);\n"
            "         }  \n"
            ""
        )
        self.lineEdit.setInputMethodHints(QtCore.Qt.InputMethodHint.ImhNone)
        self.lineEdit.setEchoMode(QtWidgets.QLineEdit.EchoMode.Normal)
        self.lineEdit.setObjectName("lineEdit")
        self.gridLayout_3.addWidget(self.lineEdit, 3, 0, 1, 3)
        self.ErrorLabel = QtWidgets.QLabel(self.widget)
        self.ErrorLabel.setStyleSheet("color: rgb(255, 0, 0);")
        self.ErrorLabel.setText("")
        self.ErrorLabel.setObjectName("ErrorLabel")
        self.gridLayout_3.addWidget(self.ErrorLabel, 1, 0, 1, 3)
        self.gridLayout_5.addLayout(self.gridLayout_3, 0, 0, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(
            20,
            21,
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )
        self.gridLayout_5.addItem(spacerItem1, 1, 0, 1, 1)
        self.gridLayout_4.addWidget(self.widget, 0, 0, 1, 1)
        self.label_3.setBuddy(self.lineEdit)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
        Dialog.setTabOrder(self.lineEdit, self.lineEdit_6)
        Dialog.setTabOrder(self.lineEdit_6, self.lineEdit_5)
        Dialog.setTabOrder(self.lineEdit_5, self.lineEdit_4)
        Dialog.setTabOrder(self.lineEdit_4, self.lineEdit_3)
        Dialog.setTabOrder(self.lineEdit_3, self.lineEdit_2)
        Dialog.setTabOrder(self.lineEdit_2, self.ActivatePushButton)
        Dialog.setTabOrder(self.ActivatePushButton, self.pushButton_back)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label_8.setText(_translate("Dialog", "Activation Code"))
        self.pushButton_back.setShortcut(_translate("Dialog", "Ctrl+R"))
        self.ActivationLabel.setText(_translate("Dialog", "Activation"))
        self.ActivatePushButton.setText(_translate("Dialog", "Activate"))
        self.label_5.setText(_translate("Dialog", "Username"))
        self.label_3.setText(_translate("Dialog", "First Name"))
        self.label_4.setText(_translate("Dialog", "Last Name"))
        self.label_7.setText(_translate("Dialog", "Email Address"))
        self.label_6.setText(_translate("Dialog", "Password"))


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec())
