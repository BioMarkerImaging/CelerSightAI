import os
import sys
import logging

sys.path.append(os.environ["CELER_SIGHT_AI_HOME"])
from celer_sight_ai import config

from PyQt6 import QtWidgets, QtCore

logger = logging.getLogger(__name__)


def import_images_handler():
    file_explorer = FileExplorer()
    accepted = file_explorer.browse_files()
    if accepted:
        return file_explorer.file_dialog.selectedFiles()
    else:
        return None


class CustomFileDialog(QtWidgets.QFileDialog):
    def __init__(self, *args, **kwargs):
        super(CustomFileDialog, self).__init__(*args, **kwargs)
        self.installEventFilter(self)

    def select_all(self):
        view = None
        for child in self.children():
            if isinstance(child, QtWidgets.QAbstractItemView):
                view = child
                break

        if view:
            view.selectAll()


class FileExplorer:
    def __init__(self):
        self.file_dialog = CustomFileDialog()
        self.settings = QtCore.QSettings("BioMarkerImaging", "CelerSight")
        self.last_visited_directory = self.load_last_directory()

    def load_last_directory(self):
        return self.settings.value("last_visited_directory_import_images", "")

    def save_last_directory(self, directory):
        self.settings.setValue("last_visited_directory_import_images", directory)

    def browse_files(self):
        # Set filters for specific file types
        filters = "Images (*.tif *.tiff *.jpeg *.jpg *.png);;All files (*.*)"

        # Set the dialog properties
        self.file_dialog.setFileMode(QtWidgets.QFileDialog.FileMode.ExistingFiles)
        self.file_dialog.setNameFilter(filters)

        # Set the directory to the last visited directory
        if self.last_visited_directory:
            self.file_dialog.setDirectory(self.last_visited_directory)

        if self.file_dialog.exec() == QtWidgets.QFileDialog.DialogCode.Accepted:
            selected_files = self.file_dialog.selectedFiles()
            print("Selected files:", selected_files)

            # Save the last visited directory
            self.last_visited_directory = self.file_dialog.directory().absolutePath()
            self.save_last_directory(self.last_visited_directory)
            return True
        else:
            return False


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    file_explorer = FileExplorer()
    file_explorer.browse_files()
    sys.exit(app.exec())
