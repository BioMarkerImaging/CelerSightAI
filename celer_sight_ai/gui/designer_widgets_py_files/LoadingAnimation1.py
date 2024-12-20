# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\manos\Desktop\topfluov2\UiAssets\LoadingAnimation1.ui'
#
# Created by: PyQt6 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QPalette, QColor
from PyQt6.QtWidgets import (
    QApplication,
    QDialog,
    QLabel,
    QProgressBar,
    QVBoxLayout,
    QHBoxLayout,
    QTextEdit,
)
import os


class ProgressDialog(QDialog):
    def __init__(self, parent=None):
        super(ProgressDialog, self).__init__()
        from celer_sight_ai import config

        self.setParent(parent)
        self.setWindowTitle("Progress")
        self.setFixedSize(400, 150)  # Increased height to accommodate QTextEdit

        self.main_layout = QVBoxLayout()

        self.label = QLabel("Processing...")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.progress_bar = QProgressBar()
        self.progress_bar.setMinimum(0)
        self.progress_bar.setMaximum(100)
        self.progress_bar.setTextVisible(False)
        self.progress_bar.setMaximumHeight(6)
        # Create layout for the progress bar and percentage
        progress_layout = QHBoxLayout()
        self.percentage_label = QLabel("0%")
        progress_layout.addWidget(self.progress_bar)
        progress_layout.addWidget(self.percentage_label)

        # Create QTextEdit for Markdown (read-only and transparent)
        self.markdown_edit = QTextEdit()
        self.markdown_edit.setPlaceholderText("")
        self.markdown_edit.setReadOnly(True)

        palette = self.markdown_edit.palette()
        palette.setColor(
            QPalette.ColorRole.Base, QColor(0, 0, 0, 0)
        )  # RGBA: Transparent background
        self.markdown_edit.setPalette(palette)
        self.markdown_edit.setWordWrapMode(
            QtGui.QTextOption.WrapMode.WrapAtWordBoundaryOrAnywhere
        )

        self.main_layout.addWidget(self.label)
        self.main_layout.addLayout(progress_layout)
        self.main_layout.addWidget(self.markdown_edit)
        # if windows, somethings is funky with the stylesheet
        if os.name == "nt":
            self.main_layout.setContentsMargins(50, 20, 50, 0)

        config.global_signals.start_progress_bar_signal.connect(self.start_progress)
        config.global_signals.update_progress_bar_progress_signal.connect(
            self.update_progress
        )
        config.global_signals.complete_progress_bar_signal.connect(
            self.complete_progress
        )

        self.setLayout(self.main_layout)

        self.timer = QTimer()
        self.timer.timeout.connect(self.handle_timeout)
        self.counter = 0

        self.setStyleSheet(
            """
            QDialog {
                background-color: rgb(45, 45, 45);
                border: 0px solid black;
                color: white;
                border-radius: 7px;
            }
            QLabel {
                font-size: 12px;
                color: white;
                border: 0px solid black;
                background-color: rgba(71,71,71,0);

            }
            QTextEdit{
                font-size: 12px;
                color: white;
                border: 0px solid black;
                background-color: rgba(71,71,71,0);

            }
            QProgressBar {
                background-color: rgb(71,71,71);
                border: 0px solid black;
                border-radius: 3px;
                text-align: center;
                color: rgba(0, 0, 0, 0);
                
            }
            QProgressBar::chunk {
                background-color: rgb(0, 125, 236);
                border-radius: 3px;

            }
        """
        )
        self.hide()

    def start_progress(self, init_dict=None):
        # center in the middle of the screen
        # TODO: ^^ center in the middle of the screen
        # get parent window center
        parent_window_center = self.parent().geometry().center()
        self.move(
            int(parent_window_center.x() - self.width() / 2),
            int(parent_window_center.y() - self.height() / 2),
        )
        self.show()
        self.raise_()
        # set the progress to zero
        self.progress_bar.setValue(40)
        if init_dict:
            if "window_title" in init_dict.keys():
                self.setWindowTitle(init_dict["window_title"])
            if "title" in init_dict.keys():
                self.label.setText(init_dict["title"])
            if "main_text" in init_dict.keys():
                self.markdown_edit.setMarkdown(init_dict["main_text"])
                # calculate the height of the markdown edit
                height = self.markdown_edit.document().size().height()
                # set the height of the window accordingly
                self.setFixedSize(self.width(), int(height + 110))
            else:
                # adjust the height of the window accordingly
                self.setFixedSize(self.width(), 110)
            if "modal" in init_dict.keys():
                self.setModal(bool(init_dict.get("modal")))
                self.parent().setEnabled(not bool(init_dict.get("modal")))
            if "percent" in init_dict.keys():
                self.progress_bar.setValue(int(init_dict["percent"]))
                self.percentage_label.setText(f"{int(init_dict['percent'])}%")

    def update_progress(self, progress_dict):
        if "title" in progress_dict:
            self.label.setText(progress_dict["title"])
        if "percent" in progress_dict:
            self.progress_bar.setValue(int(progress_dict["percent"]))
            self.percentage_label.setText(f"{int(progress_dict['percent'])}%")
        if "message" in progress_dict:
            self.markdown_edit.setPlainText(progress_dict["message"])

    def complete_progress(self):
        self.label.setText("Done.")
        self.progress_bar.setValue(100)
        self.percentage_label.setText("100%")
        QtCore.QTimer.singleShot(200, lambda: self.hide())
        self.parent().setEnabled(True)

    def update_markdown(self, new_text):
        current_text = self.markdown_edit.toPlainText()
        updated_text = new_text + "\n" + current_text
        self.markdown_edit.setPlainText(updated_text)

    def handle_timeout(self):
        if self.counter >= 100:
            self.timer.stop()
            self.label.setText("Completed!")
            self.percentage_label.setText("100%")
            return

        self.counter += 5
        self.progress_bar.setValue(self.counter)
        self.percentage_label.setText(f"{self.counter}%")


if __name__ == "__main__":
    app = QApplication([])

    dialog = ProgressDialog()
    dialog.show()
    dialog.start_progress(
        init_dict={
            "window_title": "Downloading Updates",
            "title": "test",
            "main_text": "test",
        }
    )

    app.exec()
