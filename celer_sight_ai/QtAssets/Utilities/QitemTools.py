from PyQt6 import QtCore, QtGui, QtWidgets
import scipy
import copy
import numpy as np
from celer_sight_ai.QtAssets.UiFiles.CurrentToolQuickSettings import (
    Ui_Form as QuickSettingsUI,
)
import math

import logging

logger = logging.getLogger(__name__)


class quickToolsWidget(QtWidgets.QWidget):
    def __init__(self, viewer=None):
        super(quickToolsWidget, self).__init__()
        self.animationHiden = False
        self.toolHiden = False


class customeVideoWidget(QtWidgets.QWidget):
    def __init__(self, quickToolsUi=None):
        super(customeVideoWidget, self).__init__()
        self.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.OpenHandCursor))
        self.quickToolsUiRef = quickToolsUi
        self.installEventFilter(self)
        self.toolWidgetSize = 40
        self.setMinimumSize(QtCore.QSize(100, 100))
        self.setObjectName("customeVideoWidget")
        self.hide()

    def mousePressEvent(self, event):
        self.oldPos = event.globalPosition()
        self.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.ClosedHandCursor))
        event.accept()
        # return super(customeVideoWidget,self).mousePressEvent(event)

    def hideME(self):
        logger.debug("hideME")
        # check to see if MainWindow stackedwidget is visible
        if (
            self.quickToolsUiRef.myViewer.MainWindow.stackedWidget.currentWidget().objectName()
            == "MainInterface"
        ):
            x, y, Orientation = self.checkHideToScenePos(
                self.quickToolsUiRef.myquickToolsWidget.pos()
            )
            self.quickToolsUiRef.myViewer.MainWindow.verticalQuickToolsSpotForm.myWidget.hide()
            self.quickToolsUiRef.myViewer.MainWindow.horizontalQuickToolsSpotForm.myWidget.hide()
            if not x == -1:
                if Orientation == "v":
                    self.transformToBorderWidget(x, y)
                if Orientation == "h":
                    self.transformToBorderWidgetH(x, y)
            elif not self.quickToolsUiRef.previousForm == "normal":
                self.transformToNormal()

    def mouseReleaseEvent(self, event):
        logger.debug("mouseReleaseEvent_quickToolsWidget")
        self.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.OpenHandCursor))
        x, y, Orientation = self.checkHideToScenePos(
            self.quickToolsUiRef.myquickToolsWidget.pos()
        )
        self.quickToolsUiRef.myViewer.MainWindow.verticalQuickToolsSpotForm.myWidget.hide()
        self.quickToolsUiRef.myViewer.MainWindow.horizontalQuickToolsSpotForm.myWidget.hide()
        if not x == -1:
            if Orientation == "v":
                self.transformToBorderWidget(x, y)
            if Orientation == "h":
                self.transformToBorderWidgetH(x, y)
        elif not self.quickToolsUiRef.previousForm == "normal":
            self.transformToNormal()
        return super(customeVideoWidget, self).mouseReleaseEvent(event)

    def mouseMoveEvent(self, event):
        #
        try:
            delta = QtCore.QPoint(event.globalPosition() - self.oldPos)
            self.quickToolsUiRef.myquickToolsWidget.move(
                self.quickToolsUiRef.myquickToolsWidget.x() + delta.x(),
                self.quickToolsUiRef.myquickToolsWidget.y() + delta.y(),
            )
            self.oldPos = event.globalPosition()
            self.checkHideToScenePos(self.quickToolsUiRef.myquickToolsWidget.pos())
            # self.transformToBorderWidget()
        except Exception as e:
            print(e)
            pass
        return super(customeVideoWidget, self).mouseMoveEvent(event)

    def setHeightWidgetTight(self):
        # case where we are in isolated ml draw mode
        if self.quickToolsUiRef.myViewer.ML_brush_tool_object_state == True:
            VideoFramePlaceHeight = max(
                50, self.quickToolsUiRef.VideoFramePlace.height()
            )
            RandomForestCellModeFrameHeight = max(
                301, self.quickToolsUiRef.RandomForestCellModeFrame.height()
            )
            TotalHeight = VideoFramePlaceHeight + RandomForestCellModeFrameHeight
            self.quickToolsUiRef.myquickToolsWidget.setFixedHeight(int(TotalHeight))
            self.quickToolsUiRef.myquickToolsWidget.setMaximumHeight(int(TotalHeight))
            return
        else:
            # TODO: this needs to change to iterate all visible items in the annotation frame to
            # determine the height
            itemsToCheck = [
                self.quickToolsUiRef.radiuslabelPolygon,
                self.quickToolsUiRef.lineWidthLabelPolygonTool,
                self.quickToolsUiRef.RadiusSkeletonGB,
                self.quickToolsUiRef.brushSizeGrubCut,
                self.quickToolsUiRef.colorSkeletonGB,
                self.quickToolsUiRef.colorPolygonTool,
            ]

            # Compute total height for all annotation tools
            totalRowHeigh = 0
            for item in itemsToCheck:
                if item.isVisible() == True:
                    totalRowHeigh += 20
            annotation_tools_frame_heigth = max(
                129, self.quickToolsUiRef.annotation_tool_frame.height()
            )
            VideoFramePlaceHeight = max(
                50, self.quickToolsUiRef.VideoFramePlace.height()
            )
            TotalHeight = (
                totalRowHeigh + annotation_tools_frame_heigth + VideoFramePlaceHeight
            )
            self.quickToolsUiRef.myquickToolsWidget.setFixedHeight(int(TotalHeight))
            self.quickToolsUiRef.myquickToolsWidget.setMaximumHeight(int(TotalHeight))
            return

    def checkHideToScenePos(self, pos):
        """
        check to see if the toolbar can be hidden and reutrn true if so and position where it will go

        """

        minXPos = 40
        minYPos = 50
        maxXPos = 150
        maxYPos = 100
        nonHide = False
        if self.quickToolsUiRef.myViewer.ML_brush_tool_object_state == True:
            nonHide = True

        if 0 >= pos.x() - minXPos:
            # then we hide left
            if not nonHide:
                self.quickToolsUiRef.myViewer.MainWindow.verticalQuickToolsSpotForm.myWidget.show()
                self.quickToolsUiRef.myViewer.MainWindow.horizontalQuickToolsSpotForm.myWidget.hide()
            self.quickToolsUiRef.myViewer.MainWindow.verticalQuickToolsSpotForm.myWidget.move(
                0, pos.y()
            )
            return 0, pos.y(), "v"

        elif self.quickToolsUiRef.myViewer.width() <= pos.x() + maxXPos:
            if not nonHide:
                self.quickToolsUiRef.myViewer.MainWindow.verticalQuickToolsSpotForm.myWidget.show()
                self.quickToolsUiRef.myViewer.MainWindow.horizontalQuickToolsSpotForm.myWidget.hide()
            self.quickToolsUiRef.myViewer.MainWindow.verticalQuickToolsSpotForm.myWidget.move(
                self.quickToolsUiRef.myViewer.width() - 80, pos.y()
            )
            return self.quickToolsUiRef.myViewer.width() - 80, pos.y(), "v"
        elif self.quickToolsUiRef.myViewer.height() <= pos.y() + maxYPos:
            if not nonHide:
                self.quickToolsUiRef.myViewer.MainWindow.horizontalQuickToolsSpotForm.myWidget.show()
                self.quickToolsUiRef.myViewer.MainWindow.verticalQuickToolsSpotForm.myWidget.hide()
            self.quickToolsUiRef.myViewer.MainWindow.horizontalQuickToolsSpotForm.myWidget.move(
                pos.x(), self.quickToolsUiRef.myViewer.height() - 80
            )
            return pos.x(), self.quickToolsUiRef.myViewer.height() - 80, "h"
        elif 0 >= pos.y() - minYPos:
            if not nonHide:
                self.quickToolsUiRef.myViewer.MainWindow.horizontalQuickToolsSpotForm.myWidget.show()
                self.quickToolsUiRef.myViewer.MainWindow.verticalQuickToolsSpotForm.myWidget.hide()
            self.quickToolsUiRef.myViewer.MainWindow.horizontalQuickToolsSpotForm.myWidget.move(
                pos.x(), 0
            )
            return pos.x(), 0, "h"
        else:
            if not nonHide:
                self.quickToolsUiRef.myViewer.MainWindow.verticalQuickToolsSpotForm.myWidget.hide()
                self.quickToolsUiRef.myViewer.MainWindow.horizontalQuickToolsSpotForm.myWidget.hide()
            return -1, -1, None

    def transformToBorderWidgetH(self, posx, posy):
        """Transforms the quick tools widget when the widget is docked to the top
        of the viewport

        Args:
            posx (int): pos x where widget was before mouse release
            posy (int): same as x for y
        """
        logger.debug("transformToBorderWidgetH")
        try:
            maxHeight = 40
            self.quickToolsUiRef.myquickToolsWidget.setMaximumHeight(maxHeight)
            self.quickToolsUiRef.myquickToolsWidget.setMaximumWidth(80000)
            self.quickToolsUiRef.annotation_tool_frame.setMinimumHeight(maxHeight)

            self.quickToolsUiRef.myquickToolsWidget.setFixedSize(
                QtCore.QSize(320, maxHeight + 50)
            )  # cha
            self.quickToolsUiRef.toolsFrame.hide()
            self.quickToolsUiRef.annotation_tool_frame.setFixedSize(
                QtCore.QSize(229, maxHeight)
            )  # prev 129
            myLayout = self.quickToolsUiRef.annotation_tool_frame.layout()
            quickLayout = self.quickToolsUiRef.myquickToolsWidget.layout()
            QtWidgets.QApplication.processEvents()
            layoutPos = 0
            widgetsList = []
            quickLayout.addWidget(
                self.quickToolsUiRef.annotation_tool_frame, 1, 1, 1, 1
            )
            for w in self.layout_widgets(myLayout):
                widgetsList.append(w.widget())
            # for w in widgetsList:
            #     myLayout.removeWidget(w)
            for w in widgetsList:
                myLayout.addWidget(w, 0, layoutPos, QtCore.Qt.AlignmentFlag.AlignCenter)
                layoutPos += 1
            myPosInLayout = 0
            # self.quickToolsUiRef.videowidget.move(posy - 500, posx)
            self.quickToolsUiRef.myquickToolsWidget.move(posx, posy)
            self.quickToolsUiRef.previousForm = "vertical"
            self.setHeightWidgetTight()
        except Exception as e:
            print(e)
        QtWidgets.QApplication.processEvents()

    def transformToNormal(self):
        """This function runs when the quick tools widget
        is not docked anyomore to the viewport and its "floating"
        """
        from celer_sight_ai import config

        if self.quickToolsUiRef.myViewer.ML_brush_tool_object_state == True:
            return
        print("transformToNormal")
        # get settings for current analysis
        mw = self.quickToolsUiRef.myViewer.MainWindow
        gl = config.global_params
        an = mw.new_analysis_object

        quickLayout = self.quickToolsUiRef.myquickToolsWidget.layout()
        quickLayout.addWidget(self.quickToolsUiRef.annotation_tool_frame, 2, 0, 1, 1)
        myLayout = self.quickToolsUiRef.annotation_tool_frame.layout()
        QtWidgets.QApplication.processEvents()
        rows = 2
        widgetsList = []
        myLayout.addWidget(
            self.quickToolsUiRef.pushButtonQuickToolsSelectionTool,
            0,
            0,
            1,
            1,
            QtCore.Qt.AlignmentFlag.AlignCenter,
        )
        myLayout.addWidget(
            self.quickToolsUiRef.pushButtonQuickToolsErraseTool,
            0,
            1,
            1,
            1,
            QtCore.Qt.AlignmentFlag.AlignCenter,
        )
        myLayout.addWidget(
            self.quickToolsUiRef.pushButtonQuickToolsRemoveSelectionTool,
            1,
            3,
            1,
            1,
            QtCore.Qt.AlignmentFlag.AlignCenter,
        )
        myLayout.addWidget(
            self.quickToolsUiRef.pushButtonQuickToolsMoveMagicBrush,
            0,
            2,
            1,
            1,
            QtCore.Qt.AlignmentFlag.AlignCenter,
        )
        myLayout.addWidget(
            self.quickToolsUiRef.pushButtonQuickToolsPolygonTool,
            1,
            0,
            1,
            1,
            QtCore.Qt.AlignmentFlag.AlignCenter,
        )
        myLayout.addWidget(
            self.quickToolsUiRef.pushButtonQuickToolsAutoToolBox,
            1,
            1,
            1,
            1,
            QtCore.Qt.AlignmentFlag.AlignCenter,
        )
        myLayout.addWidget(
            self.quickToolsUiRef.pushButtonQuickToolsAutoSpline,
            1,
            2,
            1,
            1,
            QtCore.Qt.AlignmentFlag.AlignCenter,
        )
        myLayout.addWidget(
            self.quickToolsUiRef.pushButtonQuickToolsAutoRF_MODE,
            0,
            3,
            1,
            1,
            QtCore.Qt.AlignmentFlag.AlignCenter,
        )
        if self.quickToolsUiRef.myViewer.ML_brush_tool_object_state == True:
            s1 = (107, 269)
            s2 = (107, 269)
            quickLayout.addWidget(
                self.quickToolsUiRef.annotation_tool_frame, 1, 1, 1, 1
            )
            self.quickToolsUiRef.myquickToolsWidget.setMaximumHeight(80000)
            self.quickToolsUiRef.myquickToolsWidget.setMaximumWidth(80000)
            self.quickToolsUiRef.annotation_tool_frame.setMaximumWidth(
                self.quickToolsUiRef.RandomForestCellModeFrame.width()
            )
            self.quickToolsUiRef.annotation_tool_frame.setMaximumHeight(100)
            self.quickToolsUiRef.annotation_tool_frame.setMinimumWidth(
                self.quickToolsUiRef.RandomForestCellModeFrame.width()
            )
            self.quickToolsUiRef.annotation_tool_frame.setMinimumHeight(100)

            self.quickToolsUiRef.myquickToolsWidget.setFixedSize(QtCore.QSize(*s1))
            self.quickToolsUiRef.RandomForestCellModeFrame.setFixedSize(
                QtCore.QSize(*s2)
            )
            quickLayout = self.quickToolsUiRef.myquickToolsWidget.layout()
            # quickLayout.addWidget(
            #     self.quickToolsUiRef.annotation_tool_frame, 2, 0, 1, 1, QtCore.Qt.AlignmentFlag.AlignCenter)

            self.quickToolsUiRef.pushButton_ML_Polygon.show()
            self.quickToolsUiRef.pushButton_ML_AutoolBox.show()

            # self.quickToolsUiRef.comboBoxQualityML.show()
            self.quickToolsUiRef.BrushRadiusCellRandomForestLabel.show()
            self.quickToolsUiRef.BrushRadiusCellRandomForestSlider.show()

            # self.quickToolsUiRef.MinRadiusspinBox.show()
            # self.quickToolsUiRef.minRadiusLabel.show()
            self.quickToolsUiRef.clearMarksrsCELLbtn.show()
            # self.quickToolsUiRef.CELLS_RM_previewNowbtn.show()
            self.quickToolsUiRef.ApplyAndDoneBtnRandomForestMode.show()

        else:
            # if config.supercategory == "worm":
            s1 = (118, 79)
            s2 = (118, 79)
            self.quickToolsUiRef.pushButtonQuickToolsRemoveSelectionTool.hide()
            self.quickToolsUiRef.pushButtonQuickToolsAutoRF_MODE.hide()
            # else:
            #     s1 = (191, 109)
            #     s2 = (200, 209)
            self.quickToolsUiRef.myquickToolsWidget.setMaximumHeight(80000)
            self.quickToolsUiRef.myquickToolsWidget.setMaximumWidth(80000)
            # self.quickToolsUiRef.myquickToolsWidget.setFixedSize(QtCore.QSize(236,375))
            self.quickToolsUiRef.annotation_tool_frame.setFixedSize(
                QtCore.QSize(*s1)
            )  # prev 129
            self.quickToolsUiRef.myquickToolsWidget.setFixedSize(QtCore.QSize(*s2))

            self.quickToolsUiRef.toolsFrame.show()
        self.quickToolsUiRef.previousForm = "normal"
        self.setHeightWidgetTight()

    def transformToBorderWidget(self, posx, posy):
        logger.debug("transformToBorderWidget")
        print("transformToBorderWidget")

        if self.quickToolsUiRef.myViewer.ML_brush_tool_object_state == True:
            pass
            # self.quickToolsUiRef.myquickToolsWidget.setMaximumHeight(80)
            # self.quickToolsUiRef.myquickToolsWidget.setMaximumWidth(80000)
            # self.quickToolsUiRef.myquickToolsWidget.setFixedSize(
            #     QtCore.QSize(40, 80))
            # self.quickToolsUiRef.RandomForestCellModeFrame.setFixedSize(
            #     QtCore.QSize(40, 80))

            # quickLayout = self.quickToolsUiRef.myquickToolsWidget.layout()
            # quickLayout.addWidget(
            #     self.quickToolsUiRef.annotation_tool_frame, 2, 0, 1, 1, QtCore.Qt.AlignmentFlag.AlignCenter)
            # self.quickToolsUiRef.LiveCELLS_RM_checkbox.hide()
            # self.quickToolsUiRef.BrushRadiusCellRandomForestLabel.hide()
            # self.quickToolsUiRef.BrushRadiusCellRandomForestSlider.hide()
            # self.quickToolsUiRef.MinRadiusspinBox.hide()
            # self.quickToolsUiRef.minRadiusLabel.hide()
            # self.quickToolsUiRef.clearMarksrsCELLbtn.hide()
            # # self.quickToolsUiRef.CELLS_RM_previewNowbtn.hide()
            # self.quickToolsUiRef.ApplyAndDoneBtnRandomForestMode.hide()

        else:
            maxWidth = 40
            self.quickToolsUiRef.myquickToolsWidget.setMaximumHeight(80000)

            self.quickToolsUiRef.myquickToolsWidget.setMaximumWidth(40)
            self.quickToolsUiRef.myquickToolsWidget.setFixedSize(
                QtCore.QSize(maxWidth, 320)
            )
            self.quickToolsUiRef.annotation_tool_frame.setFixedSize(
                QtCore.QSize(maxWidth, 230)
            )  # prev 129400,140
            quickLayout = self.quickToolsUiRef.myquickToolsWidget.layout()
            quickLayout.addWidget(
                self.quickToolsUiRef.annotation_tool_frame,
                2,
                0,
                1,
                1,
                QtCore.Qt.AlignmentFlag.AlignCenter,
            )

            self.quickToolsUiRef.toolsFrame.hide()
            myLayout = self.quickToolsUiRef.annotation_tool_frame.layout()
            myLayout.setContentsMargins(0, 0, 3, 0)
            QtWidgets.QApplication.processEvents()
            layoutPos = 0
            widgetsList = []
            for w in self.layout_widgets(myLayout):
                widgetsList.append(w.widget())
            # for w in widgetsList:
            #     myLayout.removeWidget(w)
            for w in widgetsList:
                myLayout.addWidget(w, layoutPos, 0, QtCore.Qt.AlignmentFlag.AlignCenter)
                layoutPos += 1
            myPosInLayout = 0
        self.quickToolsUiRef.myquickToolsWidget.move(posx, posy)
        self.quickToolsUiRef.previousForm = "vertical"
        QtWidgets.QApplication.processEvents()
        self.setHeightWidgetTight()

    def layout_widgets(self, layout):
        return (layout.itemAt(i) for i in range(layout.count()))


class quickToolsUi(QuickSettingsUI):
    def __init__(self, viewer=None):
        super(quickToolsUi, self).__init__()
        self.animationHiden = False
        self.myViewer = viewer
        self.toolHiden = False
        self.myquickToolsWidget = quickToolsWidget()
        self.setupUi(self.myquickToolsWidget)

        # self.myquickToolsWidget.setAttribute( QtCore.Qt.WidgetAttribute.WA_TransparentForMouseEvents )
        # self.annotation_tool_frame.setAttribute( QtCore.Qt.WidgetAttribute.WA_TransparentForMouseEvents )
        # self.toolsFrame.setAttribute( QtCore.Qt.WidgetAttribute.WA_TransparentForMouseEvents )
        self.myquickToolsWidget.setStyleSheet(
            "QFrame{background-color: rgba(0,0,0,0)};"
        )
        # self.toolsFrame.setStyleSheet("QFrame{background-color: rgba(0,0,0,0)};")
        # self.annotation_tool_frame.setStyleSheet("QFrame{background-color: rgba(0,0,0,0)};")
        # create media player object
        self.previousActiveTool = None
        self.videoWidgetShown = False
        self.previousForm = "normal"  # or "vertical" "horizonal"

        # create videowidget object
        self.videowidget = customeVideoWidget(self)
        self.videowidget.setParent(self.VideoFramePlace)
        # self.videowidget.setStyleSheet("background-color:rgba(255,255,255,255);")
        # self.VideoFramePlace.setStyleSheet("background-color: rbga(225,225,225,255);")
        # self.mediaPlayer.setVideoOutput(self.videowidget)
        self.gridLayout_2.addWidget(self.videowidget)
        # self.mediaPlayer.setMedia(\
        # QMediaContent(QtCore.QUrl.fromLocalFile\
        #     ("data/icons/quickToolGrab.png")))
        # self.mediaPlayer.play()
        self.myquickToolsWidget.setParent(viewer)
        self.myquickToolsWidget.show()
        self.videowidget.hide()
        self.VideoFramePlace.hide()
        self.allTools = [
            self.horizontalSliderPolygonTool,
            self.horizontalSliderlineWidthPolygonTool,
            self.horizontalSliderSkeletonGBTool,
            self.brushSizeSliderGrubCut,
            self.spinBoxPolygonTool,
            self.spinBoxradiusSkeletonGB,
            self.lineWidthSpinBoxPolygonTool,
            self.brushSizeSpinBoxGrabCut,
            self.radiuslabelPolygon,
            self.lineWidthLabelPolygonTool,
            self.RadiusSkeletonGB,
            self.brushSizeGrubCut,
            self.colorSkeletonGB,
            self.colorPolygonTool,
            self.pushButtonColorPolygonTool,
            self.pushButtonColorBGTool,
            self.spinBoxOpacitySkeletonGB,
            self.opacitySkeletonGBLabla,
            self.opacityPolygonLabla,
            self.spinBoxOpacityPolygon,
        ]
        # visible fulltoolox
        self.spinBoxPolygonTool.valueChanged.connect(lambda: self.updatePolygonDot())
        self.lineWidthSpinBoxPolygonTool.valueChanged.connect(
            lambda: self.updatePolygonDot()
        )
        self.pushButtonColorPolygonTool.clicked.connect(
            lambda: self.getColorPolygonDialog()
        )
        self.pushButtonColorPolygonTool.clicked.connect(
            lambda: self.myViewer.updateAllPolygonPen()
        )
        self.brushSizeSliderGrubCut.valueChanged.connect(
            lambda: self.displayCursorBrushSize()
        )
        self.horizontalSliderSkeletonGBTool.valueChanged.connect(
            lambda: self.displayCursorBrushSizeSKGB()
        )
        self.pushButtonColorBGTool.clicked.connect(
            lambda: self.getColorPolygonDialogSKGB()
        )

        self.buttonToolList = [
            self.pushButtonQuickToolsSelectionTool,
            self.pushButtonQuickToolsErraseTool,
            self.pushButtonQuickToolsRemoveSelectionTool,
            self.pushButtonQuickToolsMoveMagicBrush,
            self.pushButtonQuickToolsPolygonTool,
            self.pushButtonQuickToolsAutoToolBox,
            self.pushButtonQuickToolsAutoSpline,
            self.pushButtonQuickToolsAutoRF_MODE,
        ]
        self.myquickToolsWidget.setObjectName("myquickToolsWidget")
        self.myquickToolsWidget.setStyleSheet(
            """QWidget#myquickToolsWidget{
                            background-color: rgba(40, 40, 40,0);
                            border-color: rgba(0,0,0,180);
                            border-style: solid;  
                            border-radius: 3px;  
                            border-width: 1px;
                            }"""
        )

        self.clearMarksrsCELLbtn.clicked.connect(lambda: self.myViewer.cancel_RF_MODE())
        self.videowidget.setHeightWidgetTight()

    def displayCursorBrushSizeSKGB(self):
        rad = self.spinBoxradiusSkeletonGB.value()
        if rad == 0:
            rad = 1
        print("size changed")
        red = self.pushButtonColorBGTool.palette().button().color().red()
        green = self.pushButtonColorBGTool.palette().button().color().green()
        blue = self.pushButtonColorBGTool.palette().button().color().blue()
        circle = self.myViewer.CreateAADissk(
            int(rad / 2),
            blue,
            green,
            red,
            genOpacity=self.spinBoxOpacitySkeletonGB.value(),
        )
        height, width, channel = circle.shape
        bytesPerLine = 3 * width
        mypixmap = QtGui.QPixmap.fromImage(
            QtGui.QImage(
                circle.data,
                circle.shape[1],
                circle.shape[0],
                circle.strides[0],
                QtGui.QImage.Format_ARGB32_Premultiplied,
            )
        )
        # self.myViewer.setCursor(QtGui.QCursor(mypixmap))

    def displayCursorBrushSize(self):
        if self.myViewer.MAGIC_BRUSH_STATE is True:
            print("ipdating mgcBrsRadius")
            # if self.myViewer.magic_brush_radious == None :
            self.myViewer.magic_brush_radious = self.brushSizeSpinBoxGrabCut.value()
            if self.myViewer.magic_brush_cursor:
                self.myViewer.magic_brush_cursor.updateSize(
                    self.brushSizeSpinBoxGrabCut.value()
                )
                circlPainter = self.myViewer.getPainterPathCircle(
                    self.brushSizeSpinBoxGrabCut.value(),
                    self.myViewer.magic_brush_cursor.current_rect.pos(),
                )
                self.myViewer._scene.setSelectionArea(circlPainter)

        if self.myViewer.MAGIC_BRUSH_STATE is True:
            self.magic_click_width = self.brushSizeSpinBoxGrabCut.value()
            if self.myViewer.magic_brush_cursor:
                self.myViewer.magic_brush_cursor.updateSize(self.magic_click_width)

        if self.myViewer.FG_add is True:
            rad = self.brushSizeSpinBoxGrabCut.value()
            if rad == 0:
                rad = 1
            circle = self.myViewer.CreateAADisk(rad, 0, 255, 0)
            # height, width, channel = circle.shape
            # bytesPerLine = 3 * width
            # mypixmap = QtGui.QPixmap.fromImage(
            #     QtGui.QImage(
            #         circle.data,
            #         circle.shape[1],
            #         circle.shape[0],
            #         circle.strides[0],
            #         QtGui.QImage.Format_ARGB32_Premultiplied,
            #     )
            # )

            # self.myViewer.setCursor(QtGui.QCursor(mypixmap))
            # self.setCursor(QtGui.QCursor(QtGui.QPixmap("data\\icons\\icons_aa_tool\\drawGreen.png")))
        elif self.myViewer.FG_add == True:
            rad = self.brushSizeSpinBoxGrabCut.value()
            if rad == 0:
                rad = 1
            # circle = self.myViewer.CreateAADisk(rad, 0, 0, 255)
            # height, width, channel = circle.shape
            # bytesPerLine = 3 * width
            # mypixmap = QtGui.QPixmap.fromImage(
            #     QtGui.QImage(
            #         circle.data,
            #         circle.shape[1],
            #         circle.shape[0],
            #         circle.strides[0],
            #         QtGui.QImage.Format_ARGB32_Premultiplied,
            #     )
            # )

            # self.myViewer.setCursor(QtGui.QCursor(mypixmap))

    def getColorPolygonDialogSKGB(self):
        """
        works only for pushButtonColorPolygonTool that sets the color for the button that
        is connected to  the polygon tool
        """
        color = QtWidgets.QColorDialog.getColor()
        fg = color.name()  # Get hex
        self.pushButtonColorBGTool.setStyleSheet("background-color:" + str(fg) + ";")

    def getColorPolygonDialog(self):
        """
        works only for pushButtonColorPolygonTool that sets the color for the button that
        is connected to  the polygon tool
        """
        color = QtWidgets.QColorDialog.getColor()
        fg = color.name()  # Get hex
        self.pushButtonColorPolygonTool.setStyleSheet(
            "background-color:" + str(fg) + ";"
        )

    def updatePolygonDot(self):
        """
        updates realitime
        """
        if not hasattr(self.myViewer.MainWindow, "prevx_first"):
            prevx = 0
            prevy = 0
        else:
            prevx = self.myViewer.MainWindow.prevx_first
            prevy = self.myViewer.MainWindow.prevy_first
        self.myViewer._scene.removeItem(self.myViewer.startPointDrawingS)
        self.myViewer._scene.removeItem(self.myViewer.startPointDrawingL)

    def hideAllTools(self):
        self.actionButtons = [
            self.pushButtonQuickToolsSelectionTool,
            self.pushButtonQuickToolsRemoveSelectionTool,
            self.pushButtonQuickToolsMoveMagicBrush,
            self.pushButtonQuickToolsPolygonTool,
            self.pushButtonQuickToolsAutoToolBox,
            self.pushButtonQuickToolsAutoSpline,
            self.pushButtonQuickTools_BrushMask,
            self.pushButtonQuickToolsErraseTool,
            self.pushButtonQuickToolsKeypoint,
            self.pushButtonQuickToolsAutoRF_MODE,
        ]
        for button in self.actionButtons:
            button.setStyleSheet("background-color:rgba(63,63,63,255);")
        for tool in self.allTools:
            tool.hide()

    def showToolFor(self, ToolName):
        self.hideAllTools()
        if ToolName == None:
            self.myquickToolsWidget.show()
        if ToolName == "erraseTool":
            self.myquickToolsWidget.show()

            self.pushButtonQuickToolsErraseTool.setStyleSheet(
                """border-width: 2px;  
                border-color: white;  
                border-style: solid;"""
            )
            self.previousActiveTool = "erraseTool"

            return
        if ToolName == "selection":
            if self.previousActiveTool == "selection":
                return
            self.myquickToolsWidget.show()
            self.pushButtonQuickToolsSelectionTool.setStyleSheet(
                """border-width: 2px;  
                border-color: white;  
                border-style: solid;"""
            )
            self.previousActiveTool = "selection"
            return
        if ToolName == "auto":
            if self.previousActiveTool == "auto":
                return
            # self.myquickToolsWidget.show() # 22 px height
            # self.brushSizeSpinBoxGrabCut.show()
            # self.brushSizeGrubCut.show()
            # self.brushSizeSliderGrubCut.show()
            self.pushButtonQuickToolsAutoToolBox.setStyleSheet(
                """border-width: 2px;  
                border-color: white;  
                border-style: solid;"""
            )

            self.previousActiveTool = "auto"

            return
        if ToolName == "lasso":
            if self.previousActiveTool == "lasso":
                return
            self.myquickToolsWidget.show()
            self.previousActiveTool = "lasso"
            return
        if ToolName == "brushMask":
            if self.previousActiveTool == "brushMask":
                return
            # self.myquickToolsWidget.show()
            self.previousActiveTool = "brushMask"
            self.pushButtonQuickTools_BrushMask.setStyleSheet(
                """border-width: 2px;  
                border-color: white;  
                border-style: solid;"""
            )
            return
        if ToolName == "CELL_SPLIT_SEED":
            if self.previousActiveTool == "CELL_SPLIT_SEED":
                return
            self.CELL_SPLIT_TOOL_STATE = True
            self.pushButtonQuickToolsRemoveSelectionTool.setStyleSheet(
                """border-width: 2px;  
                border-color: white;  
                border-style: solid;"""
            )
            self.myquickToolsWidget.show()
            self.previousActiveTool = "CELL_SPLIT_SEED"

        if ToolName == "magic_brush_move":
            if self.previousActiveTool == "magic_brush_move":
                return
            self.pushButtonQuickToolsMoveMagicBrush.setStyleSheet(
                """border-width: 2px;  
                border-color: white;  
                border-style: solid;"""
            )
            self.myquickToolsWidget.show()
            self.brushSizeGrubCut.show()
            self.brushSizeSliderGrubCut.show()

            self.previousActiveTool = "magic_brush_move"
            return
        if ToolName == "polygon":
            if self.previousActiveTool == "polygon":
                return
            self.myquickToolsWidget.show()
            self.lineWidthSpinBoxPolygonTool.show()
            self.horizontalSliderlineWidthPolygonTool.show()
            self.horizontalSliderPolygonTool.show()
            self.spinBoxPolygonTool.show()
            self.radiuslabelPolygon.show()
            self.lineWidthLabelPolygonTool.show()
            self.colorPolygonTool.show()
            self.pushButtonColorPolygonTool.show()
            self.pushButtonQuickToolsPolygonTool.setStyleSheet(
                """border-width: 2px;  
                border-color: white;  
                border-style: solid;"""
            )

            self.previousActiveTool = "polygon"

            return
        if ToolName == "skeleton grabcut":
            if self.previousActiveTool == "skeleton grabcut":
                return
            self.horizontalSliderSkeletonGBTool.show()
            self.opacitySkeletonGBLabla.show()
            self.RadiusSkeletonGB.show()
            self.spinBoxOpacitySkeletonGB.show()
            self.myquickToolsWidget.show()
            self.spinBoxradiusSkeletonGB.show()
            self.pushButtonColorBGTool.show()
            self.pushButtonQuickToolsAutoSpline.setStyleSheet(
                """border-width: 2px;  
                border-color: white;  
                border-style: solid;"""
            )
            self.previousActiveTool = "skeleton grabcut"

            return
        else:
            self.myquickToolsWidget.show()
            self.pushButtonQuickToolsSelectionTool.setStyleSheet(
                """border-width: 2px;  
                border-color: white;  
                border-style: solid;"""
            )
            self.previousActiveTool = None


def qt_image_to_array(img, share_memory=False):
    """Creates a numpy array from a QImage.

    If share_memory is True, the numpy array and the QImage is shared.
    Be careful: make sure the numpy array is destroyed before the image,
    otherwise the array will point to unreserved memory!!
    """
    img = img.toImage()
    assert isinstance(img, QtGui.QImage), "img must be a QtGui.QImage object"
    assert (
        img.format() == QtGui.QImage.Format.Format_RGB32
    ), "img format must be QImage.Format.Format_RGB32, got: {}".format(img.format())
    img_size = img.size()
    buffer = img.constBits()
    # Sanity check
    n_bits_buffer = len(buffer) * 8
    n_bits_image = img_size.width() * img_size.height() * img.depth()
    assert n_bits_buffer == n_bits_image, "size mismatch: {} != {}".format(
        n_bits_buffer, n_bits_image
    )
    assert img.depth() == 32, "unexpected image depth: {}".format(img.depth())
    # Note the different width height parameter order!
    arr = np.ndarray(
        shape=(img_size.height(), img_size.width(), img.depth() // 8),
        buffer=buffer,
        dtype=np.uint8,
    )
    if share_memory:
        return arr
    else:
        return copy.deepcopy(arr)


def skeletonGrabCut(inputIamge, inputMaskStart, skeletonMask):
    import numpy as np
    import cv2

    """"
    now i need a new image with the above dimentions, and paste
    
    """
    reduced_by = 2
    print(inputMaskStart.shape)
    print(skeletonMask.shape)
    mask = np.zeros(inputMaskStart.shape[:2], np.uint8)
    mask[inputMaskStart] = cv2.GC_PR_FGD
    kernel = np.ones((3, 3), np.uint8)
    inputMaskStartdile = cv2.dilate(
        inputMaskStart.astype(np.uint8).copy(), kernel, iterations=6
    ).astype(bool)
    # supplied_mask_resized = self.resize_down(supplied_mask)
    mask[inputMaskStartdile] = cv2.GC_PR_BGD
    mask[inputMaskStartdile] = cv2.GC_PR_FGD
    mask[skeletonMask] = cv2.GC_FGD

    bgdModel = np.zeros((1, 65), np.float64)
    fgdModel = np.zeros((1, 65), np.float64)
    iteration = 2
    import skimage
    import scipy

    final_mask, bgdModel, fgdModel = cv2.grabCut(
        inputIamge,
        mask.copy(),
        None,
        bgdModel,
        fgdModel,
        iteration,
        cv2.GC_INIT_WITH_MASK,
    )
    final_mask = np.where((final_mask == 2) | (final_mask == 0), 0, 1).astype("uint8")
    final_mask = get_largerst_area(final_mask)
    final_mask = scipy.ndimage.morphology.binary_fill_holes(final_mask).astype(
        int
    )  # TmpMIni mask so that we can grab it to the label
    return final_mask


def drawThickLine(PointsLine, ImgCanvas, thickness=5):
    import numpy as np
    from PIL import Image
    from PIL import ImageDraw

    # scale = 2
    print(ImgCanvas)
    Offset = int((thickness) / 2)
    img = Image.new("L", (ImgCanvas.shape[1], ImgCanvas.shape[0]), 0)
    draw = ImageDraw.Draw(img)
    for i in range(len(PointsLine) - 1):
        draw.line(
            [
                (PointsLine[i][0], PointsLine[i][1]),
                (PointsLine[i + 1][0], PointsLine[i + 1][1]),
            ],
            fill=255,
            width=thickness,
        )
        draw.ellipse(
            (
                PointsLine[i + 1][0] - Offset,
                PointsLine[i + 1][1] - Offset,
                PointsLine[i + 1][0] + Offset,
                PointsLine[i + 1][1] + Offset,
            ),
            fill=255,
        )
    # img = img.resize((mgCanvas.shape[0]//scale, mgCanvas.shape[1]//scale), Image.ANTIALIAS)
    antialiased = np.asarray(img)
    # first and last
    draw.ellipse(
        (
            PointsLine[0][0] - Offset,
            PointsLine[0][1] - Offset,
            PointsLine[0][0] + Offset,
            PointsLine[0][1] + Offset,
        ),
        fill=255,
    )

    draw.ellipse(
        (
            PointsLine[-1][0] - Offset,
            PointsLine[-1][1] - Offset,
            PointsLine[-1][0] + Offset,
            PointsLine[-1][1] + Offset,
        ),
        fill=255,
    )

    return antialiased.astype(bool)


def get_largerst_area(input_mask):
    import skimage
    from skimage import measure

    labels_mask = measure.label(input_mask)
    regions = measure.regionprops(labels_mask)
    regions.sort(key=lambda x: x.area, reverse=True)
    if len(regions) > 1:
        for rg in regions[1:]:
            labels_mask[rg.coords[:, 0], rg.coords[:, 1]] = 0
    labels_mask[labels_mask != 0] = 1
    return labels_mask
