import os
from PyQt6 import QtCore, QtGui, QtWidgets
from celer_sight_ai.gui.designer_widgets_py_files.warningDialog import Ui_ErrorWindow
from PyQt6.QtCore import pyqtSlot
from PyQt6.QtCore import Qt
from celer_sight_ai import config
import sys

import logging

logger = logging.getLogger(__name__)


class WarningHandlerClass(object):
    """[this function is responsible for all warnings general or scene notifications
    and warnings]

    Args:
        object ([type]): [description]
    """

    def __init__(self):

        self.notifications = []
        self.notification_spacing = 30
        self.max_notifications = (
            10  # New attribute to limit the number of notifications
        )

        config.global_signals.notificationSignal.connect(self.showNotification)
        config.global_signals.warningSignal.connect(self.showWarning)
        config.global_signals.errorSignal.connect(self.showError)
        config.global_signals.fatalErrorSignal.connect(self.showFatalError)
        config.global_signals.successSignal.connect(self.showCompletedNotification)
        config.global_signals.close_accept_notification_signal.connect(
            self.close_accept_notification
        )
        config.global_signals.actionDialogSignal.connect(
            self.showCompletedNotificationWithAction
        )
        config.global_signals.successSignal_short.connect(
            self.showCompletedNotification_short
        )
        config.global_signals.app_file_signal.connect(self.newFileNotification)
        self.warning = None

    def showNotification(self, text):
        notification = NotificationWidget(text)

        # Remove the oldest notification if we've reached the limit
        if len(self.notifications) >= self.max_notifications:
            oldest_notification = self.notifications.pop(0)
            oldest_notification.close()

        self.notifications.append(notification)
        self.updateNotificationPositions()
        # Start the fade-out timer
        QtCore.QTimer.singleShot(5000, lambda: self.removeNotification(notification))

    def updateNotificationPositions(self):
        # Get the main application window
        main_window = QtWidgets.QApplication.activeWindow()
        if not main_window:
            return

        # Get the geometry of the main window
        window_geometry = main_window.geometry()
        try:
            # Get the right_side_frame_images widget
            right_side_frame = main_window.findChild(
                QtWidgets.QWidget, "right_side_frame_images"
            )
            if not right_side_frame:
                right_side_position_x = 0
            else:
                right_side_position_x = right_side_frame.mapTo(
                    main_window, QtCore.QPoint(0, 0)
                ).x()
            if self.notifications:
                annotations_width = self.notifications[0].width()
            else:
                annotations_width = 0
            # Calculate the x position for notifications
            x = (
                right_side_position_x - annotations_width - 5
            )  # Adjust based on your notification width
            y = window_geometry.top() + 20  # Initial top margin

            for notification in self.notifications:
                # Create animation for smooth movement
                try:
                    animation = QtCore.QPropertyAnimation(notification, b"geometry")
                except:
                    continue
                animation.setDuration(300)  # Duration in milliseconds
                animation.setStartValue(
                    QtCore.QRect(x, y, notification.width(), notification.height())
                )
                animation.setEndValue(
                    QtCore.QRect(x, y, notification.width(), notification.height())
                )
                animation.setEasingCurve(QtCore.QEasingCurve.Type.InOutQuad)
                animation.start()
                y += notification.height() // 2 + 20

            # Ensure notifications stay on top of the main window
            for notification in self.notifications:
                notification.raise_()
        except:
            pass

    def removeNotification(self, notification):
        if notification in self.notifications:
            self.notifications.remove(notification)
            notification.fadeOut()
            self.updateNotificationPositions()

    def addSceneRef(self, scene):
        # runthios function after all of the ui has been set up so that
        # we can connect scene notificaiotns
        self.scene = scene

    def newFileNotification(self, text):
        import time

        print("goiing through new file notriication")
        self.warning = WarningUi(
            message=text,
            title="success",
            OkCancel=False,
            MODE="file",
            onIgnore=None,
            onOk=None,
            onDelete=None,
        )

    def showCompletedNotification(self, text):
        try:
            if self.warning:
                self.warning.WarningDialForm.close()
        except:
            pass
        self.warning = WarningUi(
            message=text, title="success", OkCancel=False, JustOk=True
        )

    def showCompletedNotificationWithAction(self, main_text, actions):
        try:
            if hasattr(self.warning, "WarningDialForm"):
                self.warning.WarningDialForm.close()
        except:
            pass
        self.warning = WarningUi(
            message=main_text,
            title="",
            OkCancel=False,
            actions=actions,
            JustOk=True,
        )

    def showWarning(self, text):
        # Check if an error window is already visible
        if (
            isinstance(self.warning, WarningUi)
            and self.warning.WarningDialForm.isVisible()
        ):
            return
        try:
            if not self.warning:
                return
            self.warning.WarningDialForm.close()
        except:
            pass
        # Show warning
        self.warning = WarningUi(
            message=text, title="warning", OkCancel=False, JustOk=True, MODE="warning"
        )

    def showFatalError(self, text):
        # check if a WarningUi is visible
        if self.warning:
            try:
                self.warning.WarningDialForm.close()
            except:
                pass
        # Show warning
        self.warning = WarningUi(message=text, title="Error", JustOk=True, MODE="error")
        self.warning.add_send_logs_to_dev_button()

    def showError(self, text):
        """
        Display an error message or update an existing error window.

        This method checks if an error window is already visible. If so, it updates
        the text of the existing error. Otherwise, it closes any other visible
        warnings and displays a new error window.

        Args:
            text (str): The error message to display.

        Returns:
            None
        """
        # Check if an error window is already visible
        if (
            isinstance(self.warning, WarningUi)
            and self.warning.WarningDialForm.isVisible()
            and self.warning.MODE == "error"
        ):
            return

        # If there's any other type of warning visible, close it
        if self.warning:
            try:
                self.warning.WarningDialForm.close()
            except:
                pass

        # Show new error
        self.warning = WarningUi(message=text, title="Error", JustOk=True, MODE="error")

    def showCompletedNotification_short(self, text):
        self.warning = WarningUi(
            message=text,
            title="success",
            OkCancel=False,
            MODE="warning",
            timeout=True,
        )

    def close_accept_notification(self):
        try:
            if self.warning:
                self.warning.WarningDialForm.close()
        except:
            pass

    def showSceneNotification(self, text):
        pass

    def showSceneWarning(self, text):
        pass

    def showSceneError(self, text):
        WarningUi()
        pass

    def spawnProgressionInference(self):
        # creates the progression window and leaves it there for feature updates
        pass

    def updateProgressionInference(self, percent):
        # updates / animates the progression to the newpercent
        pass


class NotificationWidget(QtWidgets.QWidget):
    def __init__(self, text):
        super().__init__()
        self.setWindowFlags(
            QtCore.Qt.WindowType.WindowStaysOnTopHint
            | QtCore.Qt.WindowType.FramelessWindowHint
        )
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setFixedSize(240, 80)
        window = QtWidgets.QApplication.activeWindow()
        if not window:
            return
        # Set the main window as the parent
        parent_widget = QtWidgets.QApplication.activeWindow()
        if parent_widget:
            self.setParent(parent_widget)

        layout = QtWidgets.QVBoxLayout(self)
        self.label = QtWidgets.QLabel(text)
        self.label.setWordWrap(True)
        self.label.setStyleSheet(
            """
            color: white;
            background-color: rgba(60, 60, 60, 200);
            border-radius: 10px;
            padding: 10px;
        """
        )
        layout.addWidget(self.label)

        self.setLayout(layout)
        self.show()
        self.raise_()  # Ensure the notification is on top

    def fadeOut(self):
        self.anim = QtCore.QPropertyAnimation(self, b"windowOpacity")
        self.anim.setDuration(1000)
        self.anim.setStartValue(1.0)
        self.anim.setEndValue(0.0)
        self.anim.setEasingCurve(QtCore.QEasingCurve.Type.InOutQuad)
        self.anim.valueChanged.connect(self.update)
        self.anim.finished.connect(self.close)
        self.anim.start(QtCore.QAbstractAnimation.DeletionPolicy.DeleteWhenStopped)


class warningDialMaster(QtWidgets.QDialog):
    def __init__(self, *args, **kwargs):
        super(warningDialMaster, self).__init__()
        self.myDialog = WarningUi(*args, **kwargs)
        self.setFixedHeight(290)
        self.setFixedWidth(370)
        self.move(self.myDialog.WarningDialForm.pos())
        # self.setWindowFlags(QtCore.Qt.ToolTip)
        # pass
        #     // The FramelessWindowHint flag and WA_TranslucentBackground attribute are vital.
        self.setWindowFlags(
            QtCore.Qt.Window
            # | QtCore.Qt.WindowType.SplashScreen
            | QtCore.Qt.WindowSystemMenuHint
            | QtCore.Qt.WindowType.FramelessWindowHint
            | QtCore.Qt.WindowSystemMenuHint
        )
        #  |setWindowFlags(windowFlags()
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)
        self.show()

    def paintEvent(self, event):
        # if (!(windowFlags() & Qt::FramelessWindowHint) && !testAttribute(Qt::WA_TranslucentBackground))
        #     return;  // nothing to do
        print("running")
        radius = 20
        p = QtGui.QPainter(self)
        p.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)

        # # // Have style sheet?
        # if (testAttribute(Qt::WA_StyleSheetTarget)) {
        #     # // Let QStylesheetStyle have its way with us.
        #     QStyleOption opt;
        #     opt.initFrom(this);
        #     style()->drawPrimitive(QStyle::PE_Widget, &opt, &p, this);
        #     p.end();
        #     return;
        # }

        # // Paint thyself.
        rect = QtCore.QRectF(QtCore.QPointF(0, 0), self.size())
        # // Check for a border size.
        penWidth = 2
        # if (penWidth < 0.0) {
        #     QStyleOption opt;
        #     opt.initFrom(this);
        #     penWidth = style()->pixelMetric(QStyle::PM_DefaultFrameWidth, &opt, this);
        # }
        # // Got pen?
        if penWidth > 0.0:
            # p.end()
            p.setPen(QtGui.QPen(QtGui.QColor(255, 255, 255)))
            # // Ensure border fits inside the available space.
            dlta = penWidth * 0.5
            rect.adjust(dlta, dlta, -dlta, -dlta)

        else:
            # // QPainter comes with a default 1px pen when initialized on a QWidget.
            p.setPen(QtCore.Qt.PenStyle.NoPen)
        # // Set the brush from palette role.
        p.setBrush(QtGui.QColor(255, 255, 255))
        # // Got radius?  Otherwise draw a quicker rect.
        if radius > 0.0:
            p.drawRoundedRect(rect, radius, radius, QtCore.Qt.AbsoluteSize)
        else:
            p.drawRect(rect)

        # // C'est finí
        p.end()


warningStyleSheet = """
                    QFrame#WarningDialFormMainFrame{
                        background-color: rgb(45, 45, 45);
                        border-radius: 5px;
                        border: 0px solid rgba(45, 45, 45,0);
                        }
                    QDialog{
                        background-color: rgba(45, 45, 45,0);
                    }
                    QLabel#label_sub_warning_window {
                        color: rgb(205, 205, 205);
                        }
                    """


class WarningUi(object):
    def __init__(
        self,
        message=None,
        title=None,
        JustOk=None,
        OkCancel=False,  # -> options are cancel and ok
        fileAccept=False,
        onIgnore=None,  # -> options are ignore and ? not sure TODO: figure this out
        onOk=None,  # action on ok
        onCancel=None,
        onDelete=None,
        MODE="success",
        is_alert=False,  # -> if true, no ok or cancel buttons, just an alert
        timeout=False,
        timeoutPeriod=2000,
        adjusted_ok_button_text=None,
        ok_action=None,  # --> action when user clicks on
        actions={},
    ):
        if not any([OkCancel, JustOk, is_alert, onIgnore]):
            OkCancel = True
        self.MODE = MODE
        self.WarningDialForm = QtWidgets.QDialog()
        self.WarningDialForm.setObjectName("WarningDialForm")
        self.WarningDialForm.setStyleSheet(warningStyleSheet)
        self.WarningDialForm_layout = QtWidgets.QVBoxLayout(self.WarningDialForm)
        self.WarningDialForm_layout.setObjectName("WarningDialForm_layout")
        self.WarningDialFormMainFrame = QtWidgets.QFrame(self.WarningDialForm)
        self.WarningDialFormMainFrame.setObjectName("WarningDialFormMainFrame")
        self.WarningDialFormMainFrame.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        self.WarningDialForm_layout.addWidget(self.WarningDialFormMainFrame)
        self.title = title
        self.message = message
        self.onCancel = onCancel
        self.onIgnore = onIgnore
        self.onOk = onOk
        self.JustOk = JustOk
        self.onDelete = onDelete
        self.timeoutPeriod = timeoutPeriod
        self.setupUi(self.WarningDialForm)
        self.finalWidth = 370
        self.finalHeight = 290
        self.ok_action = ok_action
        self.actions = actions
        if len(actions) > 0:
            self.label_sub.setWordWrap(True)
            self.label_title.setStyleSheet(
                """color: rgb(100, 235, 100);font:"Lato";font-size: 16px;"""
            )
        elif self.MODE == "success":
            self.label_sub.setWordWrap(True)
            self.label_title.setStyleSheet(
                """color: rgb(100, 235, 100);font:"Lato";font-size: 16px;"""
            )
            self.label_sub.setText(message)
        elif self.MODE == "warning":
            self.label_title.setStyleSheet(
                """color: rgb(205, 205, 100);font:"Lato";font-size: 16px;"""
            )
        elif self.MODE == "error":
            self.finalWidth = 560
            self.label_title.setStyleSheet(
                """color: rgb(235,100 , 100);font:"Lato";font-size: 16px;"""
            )
            # add one more button to send logs to the server
        elif self.MODE == "file":
            self.label_title.setStyleSheet(
                """color: rgb(235,235 , 235);font:"Lato";font-size: 16px;"""
            )
        else:
            self.label_title.setStyleSheet(
                """color: rgb(235,235 , 235);font:"Lato";font-size: 16px;"""
            )

        self.WarningDialForm.setWindowModality(
            QtCore.Qt.WindowModality.ApplicationModal
        )
        self.label_title.setWordWrap(True)
        self.OkCancel = OkCancel
        self.fileAccept = fileAccept
        self.is_alert = is_alert
        self.start()
        self.label_sub.setStyleSheet(
            """
            background-color: rgba(0,0,0,0);
                           """
        )
        self.WarningDialForm.show()

    def setupUi(self, ErrorWindow):
        ErrorWindow.setObjectName(self.MODE)
        ErrorWindow.setWindowFlag(QtCore.Qt.WindowType.FramelessWindowHint)
        # if window, handle background color (still shows)
        if os.name == "nt":
            ErrorWindow.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)
        self.main_layout = QtWidgets.QVBoxLayout(self.WarningDialFormMainFrame)
        self.main_layout.setObjectName("gridLayout_horizontal_warning_window")
        self.main_layout.setContentsMargins(15, 15, 15, 15)
        self.main_layout.setSpacing(20)
        self.label_title = QtWidgets.QLabel(self.WarningDialFormMainFrame)
        self.label_title.setText(self.title)
        self.label_title.setObjectName("label_title_warning_window")
        self.label_title.setFixedHeight(40)
        self.label_title.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignLeft | QtCore.Qt.AlignmentFlag.AlignTop
        )
        self.main_layout.addWidget(self.label_title, QtCore.Qt.AlignmentFlag.AlignLeft)
        # add a scroll area
        self.message_scroll_area = QtWidgets.QScrollArea(self.WarningDialFormMainFrame)
        # add self.label_sub to the scroll area
        self.message_scroll_area.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignLeft | QtCore.Qt.AlignmentFlag.AlignVCenter
        )
        self.message_scroll_area.setStyleSheet(
            """QScrollArea{background-color: rgba(0,0,0,0);border: 0px solid rgba(0,0,0,0);}"""
        )
        self.main_layout.addWidget(
            self.message_scroll_area, QtCore.Qt.AlignmentFlag.AlignLeft
        )

        self.label_sub = QtWidgets.QLabel(self.WarningDialFormMainFrame)
        self.label_sub.setText(self.message)
        self.label_sub.setTextInteractionFlags(
            Qt.TextInteractionFlag.TextSelectableByMouse
        )
        self.label_sub.setObjectName("label_sub_warning_window")
        self.label_sub.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignLeft | QtCore.Qt.AlignmentFlag.AlignVCenter
        )
        self.message_scroll_area.setWidget(self.label_sub)

        # self.main_layout.addWidget(self.label_sub, QtCore.Qt.AlignmentFlag.AlignLeft)

        self.retranslateUi(ErrorWindow)
        QtCore.QMetaObject.connectSlotsByName(ErrorWindow)

    def retranslateUi(self, ErrorWindow):
        _translate = QtCore.QCoreApplication.translate
        ErrorWindow.setWindowTitle(_translate("ErrorWindow", "Error _2"))

    def add_send_logs_to_dev_button(self):
        self.send_to_devs_button = warningPushButton(self.WarningDialForm, "red")
        self.send_to_devs_button.setObjectName("send_logs_to_dev")
        self.send_to_devs_button.setText("Report...")
        # on click, send logs to server and exit dialog
        self.send_to_devs_button.clicked.connect(lambda: self.sent_logs_to_dev_action())
        self.button_frame_layout.addWidget(self.send_to_devs_button)

    def sent_logs_to_dev_action(self):
        from celer_sight_ai import configHandle
        import requests

        server_logs_address = configHandle.get_send_crash_logs_address()
        # send request to server
        ret = requests.post(server_logs_address, json={"production_logs": self.message})
        ret.raise_for_status()
        if ret.status_code == 200:
            resp_j = ret.json()
            if "log_id" in resp_j:
                # spawn another window with the log id so that the user can track the progress
                config.global_signals.actionDialogSignal.emit(
                    f"Log sent to developers with id {resp_j['log_id']}",
                    {
                        "Done": sys.exit,
                    },
                )
                # close the window
                self.WarningDialForm.close()
            else:
                config.global_signals.successSignal.emit(
                    "Logs were send but no log id was returned. Please contact the developers"
                )

    def add_ok_cancel_button(self):
        self.okBtn = warningPushButton(self.WarningDialForm, "green")
        self.okBtn.setObjectName("okBtn")
        self.okBtn.setText("Ok")

        self.CancelBtn = warningPushButton(self.WarningDialForm, "red")
        self.CancelBtn.setObjectName("CancelBtn")
        self.CancelBtn.setText("Cancel")

        if self.onCancel:
            self.CancelBtn.clicked.connect(lambda: self.onCancel())
        else:
            self.CancelBtn.clicked.connect(lambda: self.WarningDialForm.close())
        if self.onOk:
            self.okBtn.clicked.connect(lambda: self.onOk())
        else:
            self.okBtn.clicked.connect(lambda: self.WarningDialForm.close())
            if self.ok_action:
                self.okBtn.clicked.connect(lambda: self.ok_action())
        if not self.JustOk:
            self.button_frame_layout.addWidget(self.CancelBtn)
        else:
            self.CancelBtn.hide()

        self.button_frame_layout.addWidget(self.okBtn)

        self.initSize = QtCore.QSize(self.finalWidth, self.finalHeight)
        self.WarningDialForm.setFixedWidth(self.finalWidth)

    def fadeOut(self, widget: QtWidgets.QDialog) -> None:
        self.anim = QtCore.QPropertyAnimation(widget, b"windowOpacity")
        self.anim.setDuration(self.timeoutPeriod)
        self.anim.setStartValue(1)
        self.anim.setEndValue(0)
        self.anim.setEasingCurve(QtCore.QEasingCurve.Type.InOutQuad)
        self.anim.start()
        self.anim.finished.connect(lambda: widget.close())

    def start(self):
        self.button_frame = QtWidgets.QFrame(self.WarningDialForm)
        self.main_layout.addWidget(self.button_frame)
        self.button_frame.setObjectName("button_frame")
        self.button_frame_layout = QtWidgets.QHBoxLayout(self.button_frame)
        if self.is_alert:
            # timer for 3 seconds and fade out the window
            self.timer = QtCore.QTimer()
            self.timer.setSingleShot(True)
            self.timer.timeout.connect(lambda: self.fadeOut(self.WarningDialForm))
            self.timer.start(2000)
            self.finalWidth = 370
            self.finalHeight = 140
            self.initSize = QtCore.QSize(self.finalWidth, self.finalHeight)
            self.WarningDialForm.setFixedWidth(self.finalWidth)
            self.WarningDialForm.setFixedHeight(self.finalHeight)

        if len(self.actions):
            for i, action in enumerate(self.actions.keys()):
                color = "red"
                if i == 0:
                    color = "green"
                self.add_action_button(action, self.actions[action], color)
        elif self.OkCancel or self.JustOk:
            self.add_ok_cancel_button()

    def add_action_button(self, action_name, action, color="green"):
        self.action_button = warningPushButton(self.WarningDialForm, color)
        self.action_button.setObjectName("action_button")
        self.action_button.setText(action_name)
        self.action_button.clicked.connect(lambda: self.WarningDialForm.hide())
        self.action_button.clicked.connect(
            lambda: QtWidgets.QApplication.processEvents()
        )
        self.action_button.clicked.connect(lambda: action())
        self.action_button.clicked.connect(lambda: self.WarningDialForm.close())
        self.button_frame_layout.addWidget(self.action_button)


class warningPushButton(QtWidgets.QPushButton):
    def __init__(self, parent=None, style="green"):
        super(warningPushButton, self).__init__(parent)
        self.setParent(parent)
        # def addShadow(self, obj , color = None):
        self.installEventFilter(self)  # obj.shadowColor = color
        self.shadowColor = [0, 0, 0, 0]
        self.shadow = False
        self.setCheckable(True)
        self.setChecked(False)
        self.setAutoExclusive(True)
        self.setMouseTracking(True)
        if style == "green":
            self.setStyleSheet(
                """
            QPushButton{
                    background-color: rgba(0,0,0,0);
                    color: rgb(105,215,105);
                    border: 0px solid rgb(165,255,165);
                    border-radius: 5px;
                    }
            QPushButton:hover{
                    background-color: rgba(105,215,105, 30);
                    color: rgb(155,255,155);
                    }
            """
            )
        elif style == "red":
            self.setStyleSheet(
                """
            QPushButton{
                    background-color: rgba(0,0,0,0);
                    color: rgb(215 ,105,105);
                    border: 0px solid rgb(165,255,165);
                    border-radius: 5px;
                    }
            QPushButton:hover{
                    background-color: rgba(215,105,105, 30);
                    color: rgb(255,155,155);
                    }
            """
            )
        self.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)
        self.setFixedSize(QtCore.QSize(121, 35))


if __name__ == "__main__":
    import os

    # os.chdir("C:\\Users\\manos\\Documents\\topfluov2")

    import sys

    app = QtWidgets.QApplication(sys.argv)
    Win1 = WarningUi()
    sys.exit(app.exec())
