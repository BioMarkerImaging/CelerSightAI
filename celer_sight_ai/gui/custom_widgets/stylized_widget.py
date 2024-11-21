from PyQt6 import QtCore, QtGui, QtWidgets

class StylableWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._is_hovering = False
        self.margin_amount = 2
        self.border_width = 0.8
        self.radius = 5  # Rounded corners radius

        # Install event filters for hover detection
        self.setMouseTracking(True)
        self.installEventFilter(self)

    def non_hovering_border_for_painter(self, painter: QtGui.QPainter , path , rect):

        # Create a gradient for the specular highlight border
        gradient = QtGui.QLinearGradient(rect.topLeft() + QtCore.QPointF(160, 0), rect.bottomRight()- QtCore.QPointF(160, 0))
        gradient.setColorAt(0, QtGui.QColor(255, 255, 255, 60))    # Fade to transparent
        gradient.setColorAt(0.5, QtGui.QColor(255, 255, 255, 20))    # Fade to transparent
        gradient.setColorAt(1, QtGui.QColor(255, 255, 255, 0))    # Fade to transparent

        # Set the pen with the gradient
        pen = QtGui.QPen(QtGui.QBrush(gradient), self.border_width)
        painter.setPen(pen)
        painter.drawPath(path)

    def hovering_border_for_painter(self, painter: QtGui.QPainter , path , rect):
        # Create a brighter all-around border for hovering state

        # Create a gradient for the specular highlight border
        gradient = QtGui.QLinearGradient(rect.topLeft() + QtCore.QPointF(160, 0), rect.bottomRight()- QtCore.QPointF(160, 0))
        gradient.setColorAt(0, QtGui.QColor(255, 255, 255, 70))  # Start with a light color
        gradient.setColorAt(0.5, QtGui.QColor(255, 255, 255, 20))    # Fade to transparent
        gradient.setColorAt(0.5, QtGui.QColor(255, 255, 255, 0))    # Fade to transparent

        pen = QtGui.QPen(QtGui.QBrush(gradient), 1.5)  # Slightly thicker pen for visibility
        painter.setPen(pen)
        painter.drawPath(path)

        # Add a subtle inner glow effect
        glow_color = QtGui.QColor(255, 255, 255, 40)  # Very subtle white glow
        glow_pen = QtGui.QPen(glow_color, 0.9)
        painter.setPen(glow_pen)
        painter.drawPath(path.translated(0, 1))  # Draw slightly offset path for glow effect
        
    def checked_border_for_painter(self, painter: QtGui.QPainter, path, rect):
        # Create a more prominent border for the checked state

        # Create a gradient for the border
        gradient = QtGui.QLinearGradient(rect.topLeft(), rect.bottomRight())
        gradient.setColorAt(0, QtGui.QColor(255, 255, 255, 120))  # Brighter start
        gradient.setColorAt(0.5, QtGui.QColor(255, 255, 255, 80))  # Mid-point
        gradient.setColorAt(1, QtGui.QColor(255, 255, 255, 120))  # Brighter end

        # Set the pen with the gradient
        pen = QtGui.QPen(QtGui.QBrush(gradient), 2.0)  # Thicker pen for visibility
        painter.setPen(pen)
        painter.drawPath(path)

        # Add a more pronounced inner glow effect
        glow_color = QtGui.QColor(255, 255, 255, 60)  # Brighter white glow
        glow_pen = QtGui.QPen(glow_color, 1.2)
        painter.setPen(glow_pen)
        painter.drawPath(path.translated(0, 1))  # Draw slightly offset path for glow effect

        # Add a second, outer glow for more emphasis
        outer_glow_color = QtGui.QColor(255, 255, 255, 30)  # Subtle outer glow
        outer_glow_pen = QtGui.QPen(outer_glow_color, 0.8)
        painter.setPen(outer_glow_pen)
        painter.drawPath(path.translated(0, 2))  # Draw another offset path for outer glow

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing, True)

        # Create a rounded rectangle path
        path = QtGui.QPainterPath()
        margin = self.margin_amount
        padding = 0
        rect = QtCore.QRectF(
            margin + padding, 
            margin + padding, 
            self.width() - (2 * margin) - (2 * padding), 
            self.height() - (2 * margin) - (2 * padding)
        )
        path.addRoundedRect(rect, self.radius, self.radius)

        # Determine which border to draw
        if hasattr(self, 'isChecked') and self.isChecked():
            self.checked_border_for_painter(painter, path, rect)
        elif self._is_hovering:
            self.hovering_border_for_painter(painter, path, rect)
        else:
            self.non_hovering_border_for_painter(painter, path, rect)

        super().paintEvent(event)

    def event(self, event: QtCore.QEvent) -> bool:
        if event.type() == QtCore.QEvent.Type.HoverEnter:
            self._is_hovering = True
            self.update()
        elif event.type() == QtCore.QEvent.Type.HoverLeave:
            self._is_hovering = False
            self.update()
        # on mouse press also update
        elif event.type() == QtCore.QEvent.Type.MouseButtonPress:
            self.update()
        return super().event(event)



# class StylableButton(QtWidgets.QPushButton):
#     def __init__(self, text="", parent=None):
#         super().__init__(self, text, parent)

#         self._is_hovering = False
#         self.margin_amount = 2
#         self.border_width = 0.8
#         self.radius = 5  # Rounded corners radius

        
#     def paintEvent(self, event):
#         # First, paint the StylableWidget background
#         StylableWidget.paintEvent(self, event)
        
#     def event(self, event: QtCore.QEvent) -> bool:
#         if event.type() in (QtCore.QEvent.Type.HoverEnter, QtCore.QEvent.Type.HoverLeave, QEvent.Type.MouseButtonPress, QtCore.QEvent.Type.MouseButtonRelease):
#             if event.type() == QtCore.QEvent.Type.HoverEnter:
#                 self._is_hovering = True
#                 self.update()
#             elif event.type() == QtCore.QEvent.Type.HoverLeave:
#                 self._is_hovering = False
#                 self.update()
#         return super().event(event)


#     # Override isChecked to use QPushButton's implementation
#     def isChecked(self):
#         return QtWidgets.QPushButton.isChecked(self)
    
class StylableButton(StylableWidget, QtWidgets.QPushButton):
    def __init__(self, text="", parent=None):
        QtWidgets.QPushButton.__init__(self, text, parent)
        StylableWidget.__init__(self, parent)
        
        # Ensure the button is checkable
        self.setCheckable(True)
        
    def paintEvent(self, event):
        # First, paint the StylableWidget background
        StylableWidget.paintEvent(self, event)
        
        # Then, paint the button content
        painter = QtGui.QPainter(self)
        option = QtWidgets.QStyleOptionButton()
        option.initFrom(self)
        option.state = self.getState()
        option.text = self.text()
        option.icon = self.icon()
        self.style().drawControl(QtWidgets.QStyle.ControlElement.CE_PushButton, option, painter, self)
        
    def event(self, event):
        # Handle both StylableWidget and QPushButton events
        StylableWidget.event(self, event)
        return QtWidgets.QPushButton.event(self, event)

    def getState(self):
        state = QtWidgets.QStyle.State_None
        if self.isEnabled():
            state |= QtWidgets.QStyle.State_Enabled
        if self.hasFocus():
            state |= QtWidgets.QStyle.State_HasFocus
        if self.isDown():
            state |= QtWidgets.QStyle.State_Sunken
        if self.isChecked():
            state |= QtWidgets.QStyle.State_On
        if self._is_hovering:
            state |= QtWidgets.QStyle.State_MouseOver
        return state

    # Override isChecked to use QPushButton's implementation
    def isChecked(self):
        return QtWidgets.QPushButton.isChecked(self)
    

class StylableToolButton(QtWidgets.QToolButton, StylableWidget):
    def __init__(self, icon=None, text="", parent=None):
        QtWidgets.QToolButton.__init__(self, parent)
        StylableWidget.__init__(self, parent)
        
        # Set icon and text
        if icon:
            self.setIcon(icon)
        if text:
            self.setText(text)
        
        # Ensure the button is checkable
        self.setCheckable(True)
        
    def paintEvent(self, event):
        # First, paint the StylableWidget background
        StylableWidget.paintEvent(self, event)
        
        # Then, paint the QToolButton content
        painter = QtGui.QPainter(self)
        option = QtWidgets.QStyleOptionToolButton()
        option.initFrom(self)
        option.state = self.getState()
        option.text = self.text()
        option.icon = self.icon()
        option.iconSize = self.iconSize()
        self.style().drawComplexControl(QtWidgets.QStyle.ComplexControl.CC_ToolButton, option, painter, self)

    def event(self, event):
        # Handle both StylableWidget and QToolButton events
        StylableWidget.event(self, event)
        return QtWidgets.QToolButton.event(self, event)

    def getState(self):
        state = QtWidgets.QStyle.State_None
        if self.isEnabled():
            state |= QtWidgets.QStyle.State_Enabled
        if self.hasFocus():
            state |= QtWidgets.QStyle.State_HasFocus
        if self.isDown():
            state |= QtWidgets.QStyle.State_Sunken
        if self.isChecked():
            state |= QtWidgets.QStyle.State_On
        if self._is_hovering:
            state |= QtWidgets.QStyle.State_MouseOver
        return state

    # Override isChecked to use QToolButton's implementation
    def isChecked(self):
        return QtWidgets.QToolButton.isChecked(self)
    



class StylableToolButton(QtWidgets.QToolButton, StylableWidget):
    def __init__(self, icon=None, text="", parent=None):
        QtWidgets.QToolButton.__init__(self, parent)
        StylableWidget.__init__(self, parent)
        
        # Set icon and text
        if icon:
            self.setIcon(icon)
        if text:
            self.setText(text)
        
        # Ensure the button is checkable
        self.setCheckable(True)
        
    def paintEvent(self, event):
        # First, paint the StylableWidget background
        StylableWidget.paintEvent(self, event)

        # return super().paintEvent(event)

    def event(self, event):
        # Handle both StylableWidget and QToolButton events
        StylableWidget.event(self, event)
        return QtWidgets.QToolButton.event(self, event)

    def getState(self):
        state = QtWidgets.QStyle.StateFlag.State_None
        if self.isEnabled():
            state |= QtWidgets.QStyle.StateFlag.State_Enabled
        if self.hasFocus():
            state |= QtWidgets.QStyle.StateFlag.State_HasFocus
        if self.isDown():
            state |= QtWidgets.QStyle.StateFlag.State_Sunken
        if self.isChecked():
            state |= QtWidgets.QStyle.StateFlag.State_On
        if self._is_hovering:
            state |= QtWidgets.QStyle.StateFlag.State_MouseOver
        return state

    # Override isChecked to use QToolButton's implementation
    def isChecked(self):
        return QtWidgets.QToolButton.isChecked(self)