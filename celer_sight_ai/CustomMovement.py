import sys

import os
from celer_sight_ai import config


if config.is_executable:
    sys.path.append([str(os.environ["CELER_SIGHT_AI_HOME"])])

from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtCore import pyqtSlot
from PyQt6.QtCore import Qt

## Custome movement widget
if os.name == "nt":
    from win32gui import SetWindowPos
    import win32con


import logging

logger = logging.getLogger(__name__)

if __name__ == "__main__":
    pass
