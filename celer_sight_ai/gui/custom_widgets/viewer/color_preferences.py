import numpy as np
from PIL.ImageColor import getrgb as GetRGB_FromHex
from PyQt6 import QtCore, QtGui, QtWidgets


class ColorPrefsPhotoViewer:
    """
    This class is responsible for getting all of the colors and color preferences associated with the graphics view
    """

    def __init__(self, MainWindow=None):
        super().__init__()
        self.Main = MainWindow
        self.AvailabelChannels = {"RED": 0, "GREEN": 1, "BLUE": 2}
        self.ChannelsInUse = [0]
        self.NonSelectedColorDivider = (
            0.5  # to get from pg1_settings_mask_opasity_slider
        )
        self.FillerAlpha = 50
        self.NotSelectedMaskColor = QtGui.QColor(0, 0, 255)
        self.SelectedColor = QtGui.QColor(0, 255, 255)
        self.ChannelGreenColor = QtGui.QColor(0, 0, 255)
        self.ChannelRedColor = QtGui.QColor(0, 0, 255)
        self.ChannelBlueColor = QtGui.QColor(0, 0, 255)
        self.MaskWidth = 2
        self.CurrentPenCapStyle = "RoundCap"
        self.CurrentPenStyle = "SolidLine"
        self.CurrentBrushStyle = "SolidPattern"
        self.MyStyles = {
            "SolidLine": QtCore.Qt.PenStyle.SolidLine,
            "DashLine": QtCore.Qt.PenStyle.DashLine,
            "DotLine": QtCore.Qt.PenStyle.DotLine,
            "DashDotLine": QtCore.Qt.PenStyle.DashDotLine,
            "DashDotDotLine": QtCore.Qt.PenStyle.DashDotDotLine,
            "CustomDashLine": QtCore.Qt.PenStyle.CustomDashLine,
            "SquareCap": QtCore.Qt.PenCapStyle.SquareCap,
            "FlatCap": QtCore.Qt.PenCapStyle.FlatCap,
            "RoundCap": QtCore.Qt.PenCapStyle.RoundCap,
            "SolidPattern": QtCore.Qt.BrushStyle.SolidPattern,
        }

    def GetChannelsInUse(self):
        """
        function To aquiar the current channells
        """
        # get call from pg1_settings_all_masks_color_button
        # get colour from pg1_settings_selected_mask_color_button
        pass

    def setCurrentStyle(self, StyleStr="SolidLine"):
        self.CurrentStyle = str(StyleStr)

    def setCurrentCap(self, CapStyleStr="RoundCap"):
        self.CurrentPenCapStyle = str(CapStyleStr)

    def setBrushToViewer(self, viewer):
        viewer.setBursh(self.MyStyles[self.CurrentBrushStyle], self.SelectedColor)

    def getPenSelection(self):
        pen = QtGui.QPen(
            self.Main.pg1_settings_all_masks_color_button.palette().button().color()
        )
        pen.setWidth(self.MaskWidth)
        pen.setCapStyle(self.MyStyles[self.CurrentPenCapStyle])
        pen.setStyle(self.MyStyles[self.CurrentPenStyle])
        return pen

    def getPenStartingPoint(self, color="blue"):
        pen = QtGui.QPen(QtGui.QColor(color), 0.3)
        pen.setWidth(2)
        return pen
        # pen.setCapStyle(self.MyStyles[self.CurrentPenCapStyle])
        # pen.setStyle(self.MyStyles[self.CurrentPenStyle])

    def getPen(self, ForMask=False, class_id=None):
        """
        if we has assigned a region to the masks then choose that, otherwise take from the settings quick tools
        """
        color = None
        if class_id:
            color = self.Main.custom_class_list_widget.classes[class_id].color
            if not isinstance(color, type(None)):
                color = QtGui.QColor(*color)
        else:
            color = (
                self.Main.pg1_settings_all_masks_color_button.palette().button().color()
            )
        if not color:
            # generate one temporarily
            color = QtGui.QColor([0, 255, 0])
        pen = QtGui.QPen(color)
        pen.setWidth(self.Main.viewer.QuickTools.lineWidthSpinBoxPolygonTool.value())
        pen.setCapStyle(self.MyStyles[self.CurrentPenCapStyle])
        pen.setStyle(self.MyStyles[self.CurrentPenStyle])
        return pen

    def getColorSkGc(self):
        pen = QtGui.QPen(QtGui.QColor(0, 0, 255, 70))
        pen.setWidth(2)
        pen.setCapStyle(self.MyStyles[self.CurrentPenCapStyle])
        pen.setStyle(self.MyStyles[self.CurrentPenStyle])
        return pen

    def getBrush(self, class_id=None):
        if class_id:
            Color = self.Main.get_mask_color_from_class(class_id)
        else:
            Color = self.GetColorSelected()
        brush = QtGui.QBrush(
            QtGui.QColor(Color[0], Color[1], Color[2], self.FillerAlpha)
        )
        return brush

    def CreatePen(self, viewer):
        """
        Creates a pen with the appropriate styles
        """
        pen = QtGui.QPen(self.SelectedColor)
        pen.setWidth(self.MaskWidth)
        pen.setCapStyle(self.MyStyles[self.CurrentPenCapStyle])
        pen.setStyle(self.MyStyles[self.CurrentPenStyle])
        viewer.setPen(pen)

    def FillRect(self, painter=None, style=None, widget=None):
        painter.fillRect(self.scene_rect, self._brush)

    def GetColorNotSelected(self):
        return GetRGB_FromHex(self.SelectedColor.name()) / self.NonSelectedColorDivider

    def GetColorSelected(self):
        return np.asarray(GetRGB_FromHex(self.NotSelectedMaskColor.name()))
