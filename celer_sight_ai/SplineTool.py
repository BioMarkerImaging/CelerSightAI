# Spline interpolator
import sys

import os
from celer_sight_ai import config


if config.is_executable:
    sys.path.append([str(os.environ["CELER_SIGHT_AI_HOME"])])
from PyQt6 import QtCore, QtGui, QtWidgets
from celer_sight_ai import config


import logging

logger = logging.getLogger(__name__)


class LineDragItem(QtWidgets.QGraphicsLineItem):
    photoChanged = QtCore.pyqtSignal()

    def __init__(self, *args, **kwargs):
        self._line = QtCore.QLineF()
        super().__init__(*args, **kwargs)
        # Flags to allow dragging and tracking of dragging.
        self.setFlags(
            self.flags()
            | QtWidgets.QGraphicsItem.GraphicsItemFlag.ItemSendsGeometryChanges
            | QtWidgets.QGraphicsItem.GraphicsItemFlag.ItemIsMovable
            | QtWidgets.QGraphicsItem.GraphicsItemFlag.ItemIsSelectable
        )

    @property
    def line(self):
        return self._line

    @line.setter
    def line(self, line):
        self._line = line

    def itemChange(self, change, value):
        if (
            change == QtWidgets.QGraphicsItem.ItemPositionChange
            and self.isSelected()
            and not self.line.isNull()
        ):
            logger.info("emiting!")
            config.global_signals.photoChanged.emit()
            # http://www.sunshine2k.de/coding/java/PointOnLine/PointOnLine.html
            p1 = self.line.p1()
            p2 = self.line.p2()
            e1 = p2 - p1
            e2 = value - p1
            dp = QtCore.QPointF.dotProduct(e1, e2)
            l = QtCore.QPointF.dotProduct(e1, e1)
            p = p1 + dp * e1 / l
            return p
        return super().itemChange(change, value)
