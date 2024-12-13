from PyQt6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QLabel,
    QProgressBar,
    QSpacerItem,
    QMessageBox,
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QMovie
from celer_sight_ai import config

from PyQt6.QtCore import Qt, QEvent
from PyQt6.QtGui import QKeyEvent


class LoadingDialog(QDialog):
    progress_updated = pyqtSignal(int)

    def __init__(self, parent=None, title="Loading", message="Please wait..."):
        super().__init__(parent)
        self.hide()
        self.setWindowTitle(title)
        self.setWindowModality(Qt.WindowModality.ApplicationModal)
        self.setFixedSize(300, 150)
        self.setWindowFlags(
            self.windowFlags()
            | Qt.WindowType.FramelessWindowHint
            | Qt.WindowType.WindowStaysOnTopHint
        )
        self.action_completed = False
        layout = QVBoxLayout()
        config.global_signals.loading_dialog_signal_update_progress_percent.connect(
            self.update_progress
        )
        config.global_signals.loading_dialog_set_text.connect(
            self.set_pretext_paragraph
        )
        config.global_signals.loading_dialog_show.connect(self.show)
        config.global_signals.loading_dialog_signal_close.connect(self.hide)
        self.message_label = QLabel(message)
        layout.addWidget(self.message_label)

        self.progress_bar = QProgressBar()
        layout.addWidget(self.progress_bar)

        self.setLayout(layout)

        self.progress_updated.connect(self.update_progress)
        self.pretext_paragraph = ""
        self.apply_dark_theme()
        self.center()
        self.setupCleanupFunction(self.close)

    def set_pretext_paragraph(self, text):
        self.pretext_paragraph = text
        self.message_label.setText(
            f"{self.pretext_paragraph} {self.progress_bar.value()}%"
        )

    def setupCleanupFunction(self, cleanup_function):
        self.cleanup = cleanup_function

    def center(self):
        frame_geo = self.frameGeometry()
        screen = self.parent().geometry().center()
        frame_geo.moveCenter(screen)
        self.move(frame_geo.topLeft())

    def keyPressEvent(self, event: QKeyEvent):
        if event.key() == Qt.Key.Key_Escape:
            self.closeEvent(QEvent(QEvent.Type.Close))
            event.accept()
        else:
            super().keyPressEvent(event)

    def completed(self):
        self.action_completed = True
        self.cleanup()

    def closeEvent(self, event):
        event.ignore()
        if not self.action_completed:
            reply = QMessageBox.question(
                self,
                "Confirm Exit",
                "Are you sure you want to exit?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            )

            if reply == QMessageBox.StandardButton.Yes:
                self.cleanup()
                event.accept()
            else:
                event.ignore()

    def nn_download_cleanupfunction(self, path):
        import os

        if os.path.exists(path):
            os.remove(path)

    def update_progress(self, value):
        self.show()
        self.progress_bar.setValue(int(value))
        self.message_label.setText(f"{self.pretext_paragraph} {round(value,2)}%")

    def set_callback(self, callback):
        self.callback = callback

    def start(self):
        if self.callback:
            self.callback(self.progress_updated)

    def apply_dark_theme(self):
        dark_palette = """
        QWidget {{
            background-color: #333;
            color: #CCC;
            font-weight: bold;
        }}
        QProgressBar {{
            background-color: #555;
            border: 2px solid #888;
            border-radius: 5px;
            text-align: center;
        }}
        QProgressBar::chunk {{
            background-color: #3D7848;
            border-radius: 3px;
        }}
        """

        self.setStyleSheet(dark_palette)


def update_progress_bar(count, block_size, total_size):
    percentage = int(count * block_size * 100 / total_size)
    config.global_signals.loading_dialog_signal_update_progress_percent.emit(percentage)


if __name__ == "__main__":
    from PyQt6.QtWidgets import QApplication
    import sys

    app = QApplication(sys.argv)
    dialog = LoadingDialog()
    dialog.show()
    app.exec()
