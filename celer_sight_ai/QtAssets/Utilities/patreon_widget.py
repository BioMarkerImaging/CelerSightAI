from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel
import os
import sys
from celer_sight_ai import config
from celer_sight_ai.QtAssets.category_and_contribution_widgets import (
    DialogWidgetTitleHat,
)


class PatreonWidget(QtWidgets.QDialog):
    """
    Widget for managing Patreon account connection and status
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        # Make the dialog modal
        self.setWindowModality(Qt.WindowModality.ApplicationModal)
        self.setupUi()
        self.needs_refresh = False
        self.installEventFilter(self)

    def eventFilter(self, watched_obj, event) -> bool:
        if watched_obj is self and event.type() == QtCore.QEvent.Type.WindowActivate:
            if self.needs_refresh:
                self.refresh_status()
                self.needs_refresh = False
        return super().eventFilter(watched_obj, event)

    def setupUi(self):
        # Main layout
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)

        # Content widget with dark background
        self.content_widget = QWidget()
        self.content_widget.setObjectName("content_widget")
        self.content_widget.setStyleSheet(
            """
            #content_widget {
                background-color: rgb(40,40,40);
                border-bottom-left-radius: 10px;
                border-bottom-right-radius: 10px;
            }
        """
        )

        # Content layout
        self.content_layout = QVBoxLayout(self.content_widget)
        self.content_layout.setContentsMargins(20, 20, 20, 20)
        self.content_layout.setSpacing(15)

        # Status label
        self.status_label = QLabel()
        self.status_label.setStyleSheet("color: rgb(255,255,255);")
        self.status_label.setWordWrap(True)
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.content_layout.addWidget(self.status_label)

        # Connect button
        self.connect_button = QPushButton("Connect to Patreon")
        self.connect_button.setMinimumHeight(40)
        self.connect_button.clicked.connect(lambda: self.connect_patreon())
        self.connect_button.setStyleSheet(
            """
            QPushButton {
                background-color: rgb(50,100,50);
                color: rgb(0,180,0);
                border-radius: 5px;
                padding: 5px;
            }
            QPushButton:hover {
                background-color: rgb(50,155,50);
                color: rgb(0,255,0);
            }
        """
        )
        self.content_layout.addWidget(self.connect_button)

        # Disconnect button
        self.disconnect_button = QPushButton("Disconnect")
        self.disconnect_button.setMinimumHeight(40)
        self.disconnect_button.clicked.connect(lambda: self.disconnect_patreon())
        self.disconnect_button.setStyleSheet(
            """
            QPushButton {
                background-color: rgb(100,50,50);
                color: rgb(180,0,0);
                border-radius: 5px;
                padding: 5px;
            }
            QPushButton:hover {
                background-color: rgb(155,50,50);
                color: rgb(255,0,0);
            }
        """
        )
        self.content_layout.addWidget(self.disconnect_button)

        # Refresh button
        self.refresh_button = QPushButton("Refresh Status")
        self.refresh_button.setMinimumHeight(40)
        self.refresh_button.clicked.connect(lambda: self.refresh_status())
        self.refresh_button.setStyleSheet(
            """
            QPushButton {
                background-color: rgb(45,45,45);
                color: rgb(185,185,185);
                border-radius: 5px;
                padding: 5px;
            }
            QPushButton:hover {
                background-color: rgb(75,75,75);
                color: rgb(255,255,255);
            }
        """
        )
        self.content_layout.addWidget(self.refresh_button)

        self.layout.addWidget(self.content_widget)

        # Modify window flags to show only the close button
        self.setWindowFlags(
            Qt.WindowType.Window
            | Qt.WindowType.CustomizeWindowHint
            | Qt.WindowType.WindowCloseButtonHint
        )

        # Center the dialog on screen
        screen = QtWidgets.QApplication.primaryScreen().geometry()
        self.move(
            (screen.width() - self.width()) // 2, (screen.height() - self.height()) // 2
        )

        # Update initial status
        self.update_status()

    def connect_patreon(self):
        """Initiate Patreon OAuth2 connection"""
        try:
            config.client.connect_patreon()
            # set self.needs_refresh = True after 1 second when this is triggered with slingshot
            QtCore.QTimer.singleShot(1000, lambda: setattr(self, "needs_refresh", True))

            self.update_status()
        except Exception as e:
            config.global_signals.errorSignal.emit(str(e))

    def disconnect_patreon(self):
        """Disconnect Patreon account"""
        try:
            config.client.disconnect_patreon()
            self.update_status()
        except Exception as e:
            config.global_signals.errorSignal.emit(str(e))

    def refresh_status(self):
        """Refresh Patreon connection status"""
        try:
            self.update_status()
        except Exception as e:
            config.global_signals.errorSignal.emit(str(e))

    def update_status(self):
        """Update the status display"""
        # check from the user config if the patreon is connected

        try:
            status = config.client.get_patreon_status()
            membership_type = status.get("membership_type")
            is_connected = status.get("status") != "Not connected"
            if is_connected:
                self.status_label.setText(
                    f"Connected to Patreon\nCurrent Tier: {membership_type}"
                )
                self.connect_button.hide()
                self.disconnect_button.show()
            else:
                self.status_label.setText("Not connected to Patreon")
                self.connect_button.show()
                self.disconnect_button.hide()

        except Exception as e:
            self.status_label.setText("Error checking Patreon status")
            config.global_signals.errorSignal.emit(str(e))


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    patreon_widget = PatreonWidget()
    patreon_widget.show()
    sys.exit(app.exec())
