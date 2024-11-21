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
from celer_sight_ai.QtAssets.buttons.animate_qpushbutton import AnimationCursor
from celer_sight_ai import config


from celer_sight_ai.QtAssets.UiFiles.popup_tool_menu_v2 import (
    Ui_tool_selection_onscreen_menu as FormUISection,
)
import time


class OnScreenDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__()
        self.parent = parent
        self.BeenShown = False
        self.Stopped = False

        """
        These Captured items are used in case the BeginTimer, which handles the right click pop up menu
        does not reach the TimeInterval to pop up and so we need to forward the events to event filter
        """
        self.CapturedEvent = None
        self.CapturedSource = None

        self.pressedButton = None  # self.tool_selection_menu_Center

        # self.RightButtonIsPressed = False
        self.StartTime = 0  # when we prees button
        self.EndTime = 0  # when we check if we need to show the menu or not
        self.TimeInterval = 0.25  # how much time until the pop up shows
        self.OnGoingPress = False
        self.installEventFilter(self)
        self.setMouseTracking(True)
        # self.setStyleSheet()
        self.start_worker()
        from celer_sight_ai import config

        print("runsssss")

    def start_worker(self):
        from celer_sight_ai.core.Workers import Worker, WorkerSignals

        try:
            del self.threadpool
            del self.Worker_1_analyse
        except:
            pass
        self.Stopped = False
        self.threadpool = QtCore.QThreadPool()
        self.Worker_1_analyse = Worker(self.BeginTimer)

    def BeginTimer(self, progress_callback):
        """
        THis fucntion runs every time we click to begin a timer that when its over, (if we havent release the right
        mousbutton click) then the pop up appears
        """
        from celer_sight_ai import config

        running = True
        print("begine timere runs")
        while running == True:
            TimeDiff = time.time() - self.StartTime
            if self.Stopped == True:
                # this is a premature stop so it counds as a normal Right click
                print("Time is stoped ")
                running = False
                self.Stopped = False
                self.eventFilter(self.CapturedSource, self.CapturedEvent)
                return
            if TimeDiff > self.TimeInterval:
                running = False
                print("result is ", TimeDiff)
                config.global_signals.ShowPopUpWidgetTools.emit()
                QtWidgets.QApplication.processEvents()
                return

            print(self.Stopped)
            time.sleep(0.01)
        return

    def HideSelf(self):
        """
        Activated on emited signal to hide
        """
        self.Stopped = True
        self.hide()
        self.BeenShown = True
        self.EndTime = 0
        self.StartTime = 0
        # self.threadpool.start(self.Worker_1_analyse)
        print("Hiding through HIdeSelf")

    def ShowSelf(self):
        """
        When the Begine timer function is complete this function runs to show the dialog
        """
        print("ENDING ")
        from celer_sight_ai import config

        config.global_signals.StopCursorAnimationSignal.emit()
        self.setFocusPolicy(QtCore.Qt.FocusPolicy.StrongFocus)
        self.setFocus()
        self.BeenShown = True
        self.StartTime = 0  # when we prees button
        self.EndTime = 0  # when we check if we need to show the menu or not
        self.move(self.actualPosX, self.actualPosY)
        config.global_signals.PopUpWindowAnimationSignal.emit()
        QtWidgets.QApplication.processEvents()

        self.show()
        self.raise_()

    def PlayButtonAnimation(self):
        self.CreateParAnimation()
        self.ParAnimation.start()

    def GetButtonsReferences(self):
        """
        Convience to get the references for our buttons
        """
        self.PolBtn = self.findChild(
            QtWidgets.QPushButton, "tool_selection_menu_polygon_btn"
        )
        self.AutoBtn = self.findChild(
            QtWidgets.QPushButton, "tool_selection_menu_auto_cut_btn"
        )
        self.EraseBtn = self.findChild(
            QtWidgets.QPushButton, "tool_selection_menu_erase"
        )
        self.SelBtn = self.findChild(
            QtWidgets.QPushButton, "tool_selection_menu_selection_btn"
        )
        self.mgicBrush = self.findChild(
            QtWidgets.QPushButton, "pushButtonQuickToolsMoveMagicBrush"
        )

    def mouseReleaseEvent(self, event):
        print(" mouse release on ui tool selection dialog")

        if event.button() == QtCore.Qt.MouseButton.RightButton:
            try:
                self.parent.CustomCursor._timer.force_stop()
            except Exception as e:
                print(e)
            # QtWidgets.QApplication.processEvents()

            self.Stopped = True
            self.hide()
            self.BeenShown = True
            self.EndTime = 0
            self.StartTime = 0
            self.OnGoingPress = False
            # self.threadpool.start(self.Worker_1_analyse)
            print("eventFilter pop up meny works2!")
            config.global_signals.StopCursorAnimationSignal.emit()
            config.global_signals.RestoreCursor.emit()
        return super(OnScreenDialog, self).mouseReleaseEvent(event)

    # def eventFilter(self, source, event):

    #     # print("other one: ", event.type())
    #     if event.type() == QtCore.QEvent.Type.MouseButtonPress and event.button() == QtCore.Qt.MouseButton.RightButton:
    #         if self.OnGoingPress == False:
    #             # print("STARINGGG")
    #             self.OnGoingPress = True
    #             self.parent.CustomCursor = AnimationCursor(self.parent)
    #             self.parent.CustomCursor.playAnim()
    #             self.StartTime = time.time()
    #             globalPosStart = event.screenPos()
    #             self.actualPosX = int(globalPosStart.x()) -380
    #             self.actualPosY = int(globalPosStart.y()) -350
    #             self.CapturedEvent = event
    #             self.CapturedSource = source
    #             self.start_worker()
    #             self.threadpool.start(self.Worker_1_analyse)
    #             print("rpess is true")
    #         return super(OnScreenDialog, self).eventFilter(source, event)

    #     if event.type() == QtCore.QEvent.Type.MouseMove:

    #         widget = QtWidgets.QApplication.widgetAt(event.globalPosition())
    #         # print("step1")self.beggin_dra_w_button_radio,
    #         if widget in (self.PolBtn, self.AutoBtn, self.EraseBtn, self.SelBtn):
    #             # print("step2")
    #             if widget != self.pressedButton:
    #                 # print("step3")
    #                 if self.pressedButton != widget:
    #                     # print("step4")
    #                     # print(event.type())
    #                     self.enterButton = widget
    #                     self.selected_button_handler(widget)
    #                     from celer_sight_ai import config

    #                     config.global_signals.tool_signal.emit()
    #             else:
    #                 self.enterButton = None
    #         return super(OnScreenDialog, self).eventFilter(source, event)

    #     return super(OnScreenDialog, self).eventFilter(source, event)
    # def mouseMoveEvent(self,event):
    #     from celer_sight_ai import config

    #     widget = QtWidgets.QApplication.widgetAt(event.globalPosition())
    #     # print("step1")
    #     if widget in (self.PolBtn, self.AutoBtn, self.EraseBtn, self.SelBtn):
    #         # print("step2")
    #         if widget != self.pressedButton:
    #             # print("step3")
    #             if self.pressedButton != widget:
    #                 # print("step4")
    #                 # print(event.type())
    #                 self.enterButton = widget
    #                 self.selected_button_handler(widget)
    #                 # config.global_signals.tool_signal_to_main.emit()
    #         else:
    #             self.enterButton = None
    #     return super(OnScreenDialog, self).mouseMoveEvent( event)

    def selected_button_handler(self, source):
        # assign the current button
        from celer_sight_ai import config

        print(source)
        print(self.SelBtn, self.AutoBtn, self.EraseBtn, self.PolBtn)
        if source == self.SelBtn:
            self.selected_button = "selection"
            self.SelBtn.setChecked(True)
            self.AutoBtn.setChecked(False)
            self.EraseBtn.setChecked(False)
            self.PolBtn.setChecked(False)
            self.mgicBrush.setChecked(False)

            self.parent.ApplyUiSelectionBtn(self.selected_button)
            self.parent.viewer.update_tool(self.selected_button)
            self.parent.viewer.quickToolsUi.myquickToolsWidget.hide()
            print("selection")
        elif source == self.AutoBtn:
            self.selected_button = "auto"
            self.SelBtn.setChecked(False)
            self.AutoBtn.setChecked(True)
            self.EraseBtn.setChecked(False)
            self.PolBtn.setChecked(False)
            self.parent.ApplyUiSelectionBtn(self.selected_button)
            self.mgicBrush.setChecked(False)

            self.parent.viewer.update_tool(self.selected_button)

            print("Auto")
        elif source == self.EraseBtn:
            self.selected_button = "lasso"
            self.SelBtn.setChecked(False)
            self.AutoBtn.setChecked(False)
            self.EraseBtn.setChecked(True)
            self.PolBtn.setChecked(False)
            self.parent.ApplyUiSelectionBtn(self.selected_button)
            self.mgicBrush.setChecked(False)

            self.parent.viewer.update_tool(self.selected_button)

            print("Erase")
        elif source == self.PolBtn:
            self.selected_button = "polygon"
            print("polygon_selected")
            self.SelBtn.setChecked(False)
            self.AutoBtn.setChecked(False)
            self.EraseBtn.setChecked(False)
            self.PolBtn.setChecked(True)
            self.mgicBrush.setChecked(False)

            self.parent.ApplyUiSelectionBtn(self.selected_button)

            self.parent.viewer.update_tool(self.selected_button)

            print("Polugon!")
        elif source == self.mgicBrush:
            self.selected_button = "magic_brush_move"
            self.SelBtn.setChecked(False)
            self.AutoBtn.setChecked(False)
            self.EraseBtn.setChecked(False)
            self.PolBtn.setChecked(False)
            self.mgicBrush.setChecked(True)
            self.parent.ApplyUiSelectionBtn(self.selected_button)
            self.parent.viewer.update_tool(self.selected_button)
        else:
            print("source does not match")
        config.global_signals.tool_signal.emit()
        return

    def CreateParAnimation(self):
        self.ParAnimation = QtCore.QParallelAnimationGroup()
        ListOfWidgets = [self.PolBtn, self.AutoBtn, self.EraseBtn, self.SelBtn]
        for item in ListOfWidgets:
            self.AddItemToParAnimation(item)

    def AddItemToParAnimation(self, widget):
        """
        Fucntion that sets up the animation of the buttons apaeritng
        we need to animate size, position and oppacity THis needs to be applied to alla widgets
        """
        AnimationDuration = 250

        #
        # Position Animation
        #

        MyPosOnScreen = widget.pos()
        print(
            "For widfget ",
            widget.objectName(),
            " pos is ",
        )
        initialX = MyPosOnScreen.x()
        initialY = MyPosOnScreen.y()
        initialWidth = widget.width()
        initialHeight = widget.height()
        GeometryAnimation = QtCore.QPropertyAnimation(widget, b"geometry")
        GeometryAnimation.setDuration(AnimationDuration)
        AnimstartPosX = self.pressedButton.rect().topLeft().x() + 180
        AnimstartPosY = self.pressedButton.rect().topLeft().y() + 200
        GeometryAnimation.setStartValue(
            QtCore.QRect(
                AnimstartPosX, AnimstartPosY, initialWidth / 4, initialHeight / 4
            )
        )
        GeometryAnimation.setEndValue(
            QtCore.QRect(initialX, initialY, initialWidth, initialHeight)
        )
        curve = QtCore.QEasingCurve(QtCore.QEasingCurve.Type.OutExpo)
        GeometryAnimation.setEasingCurve(curve)
        self.ParAnimation.addAnimation(GeometryAnimation)

        #
        # Opacity Animation
        #

        OpacityAnimation = QtCore.QPropertyAnimation(widget, b"opacity")
        OpacityAnimation.setDuration(AnimationDuration)
        OpacityAnimation.setStartValue(0.3)
        self.ParAnimation.addAnimation(OpacityAnimation)


class Ui_tool_selection_onscreen_menu(FormUISection):
    def __init__(self, MainWindow=None):
        super().__init__()
        self.MainWindow = MainWindow
        self.enterButton = self.pressedButton = None
        self.selected_button = (
            "selection"  # available are: selection, polygon, lasso, auto
        )
        from celer_sight_ai import config

        # self.MyDialog = OnScreenDialog()
        # self.setupUi(self.MyDialog)
        # self.retranslateUi(self.MyDialog)
        # self.MyDialog.setMouseTracking(True)
        # self.MyDialog.GetButtonsReferences()
        # self.MyDialog.hide()
        # self.MyDialog.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground )
        # self.MyDialog.setAttribute(QtCore.Qt.WidgetAttribute.WA_TransparentForMouseEvents, False)
        # config.global_signals.ShowPopUpWidgetTools.connect(lambda: self.MyDialog.ShowSelf())
        # config.global_signals.HidePopUpWidgetTools.connect(lambda: self.MyDialog.HideSelf)
        # config.global_signals.PopUpWindowAnimationSignal.connect( lambda: self.MyDialog.PlayButtonAnimation())
        # self.MyDialog.setWindowFlags(QtCore.Qt.WindowType.FramelessWindowHint | QtCore.Qt.WindowType.WindowStaysOnTopHint)
        # self.initilize_tools()
        # listToAddShadow1 = [
        # self.tool_selection_menu_Center,
        # self.tool_selection_menu_selection_btn,
        # self.tool_selection_menu_auto_cut_btn,
        # self.tool_selection_menu_erase,
        # self.tool_selection_menu_polygon_btn
        # ]
        # for widget in listToAddShadow1:
        #     self.MainWindow.AddShadowToWidget(widget)
        # self.MyDialog.setParent(None)

    # @staticmethod

    def initilize_tools(self):
        self.pressedButton = self.tool_selection_menu_Center
        # self.MyDialog.pressedButton = self.tool_selection_menu_Center
        self.tool_selection_menu_selection_btn.setEnabled(True)
        self.tool_selection_menu_auto_cut_btn.setEnabled(True)
        self.tool_selection_menu_erase.setEnabled(True)
        self.tool_selection_menu_polygon_btn.setEnabled(True)


if __name__ == "__main__":
    pass
