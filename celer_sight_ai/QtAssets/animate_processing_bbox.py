from PyQt6 import QtWidgets, QtCore, QtGui
import logging
import os
import random

logger = logging.getLogger(__name__)


class AnimationProxy(QtCore.QObject):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._value = 0

    @QtCore.pyqtProperty(int)
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value


class ProcessingBox(QtWidgets.QGraphicsRectItem):
    def __init__(self, bbox, scene, parent=None, is_animated=False):
        super().__init__(bbox[0], bbox[1], bbox[2], bbox[3], parent)
        self.setBrush(QtGui.QBrush(QtGui.QColor(255, 255, 255, 0)))
        self.scene_ref = scene
        self.is_animated = is_animated

        # Optimize shadow effect for better performance
        shadow = QtWidgets.QGraphicsDropShadowEffect()
        shadow.setBlurRadius(10)  # Reduced blur radius
        shadow.setColor(QtGui.QColor(0, 0, 0, 150))
        shadow.setOffset(0, 0)
        self.setGraphicsEffect(shadow)

        # Create two pens - one cosmetic for zoomed out, one normal for zoomed in
        self.cosmetic_pen = QtGui.QPen(QtGui.QColor(255, 255, 255, 200))
        self.cosmetic_pen.setWidth(4)
        self.cosmetic_pen.setCosmetic(True)

        self.normal_pen = QtGui.QPen(QtGui.QColor(255, 255, 255, 200))
        self.normal_pen.setWidth(2)
        self.normal_pen.setCosmetic(False)

        self.setPen(self.cosmetic_pen)

        # Cache the item for better rendering performance
        self.setCacheMode(QtWidgets.QGraphicsItem.CacheMode.DeviceCoordinateCache)

        # Add scale change handler
        self.scale_threshold = 2.0  # Adjust this value as needed
        if scene and scene.views():
            view = scene.views()[0]
            view.viewportEvent = self._wrap_viewport_event(view.viewportEvent)

        # Create a grid of circles
        r_len = 10
        c_len = 10
        self.rad = (bbox[2] + bbox[3]) / (c_len * r_len * 2)
        self.circles = []
        self._circle_objects = []
        c_quant = bbox[2] / (c_len - 1)
        r_quant = bbox[3] / (r_len - 1)
        if self.is_animated:
            for r in range(1, r_len - 1):
                for c in range(1, c_len - 1):
                    # randomize size by 100%
                    rad = self.rad * (1 + (0.5 * (1 - 2 * random.random())))
                    # create an eclipse item
                    ec_item = QtWidgets.QGraphicsEllipseItem(
                        0, 0, rad * 2, rad * 2, self
                    )
                    # Make circles more visible
                    ec_item.setBrush(
                        QtGui.QBrush(QtGui.QColor(255, 255, 255, 230))
                    )  # Increased opacity
                    ec_item.setPen(QtGui.QPen(QtGui.QColor(255, 255, 255, 230)))
                    # Make circles cosmetic (maintain size regardless of zoom)
                    ec_item.setFlag(
                        QtWidgets.QGraphicsItem.GraphicsItemFlag.ItemIgnoresTransformations
                    )
                    circle = AnimatedCircle(ec_item, int(rad))
                    self._circle_objects.append(circle)
                    scene.addItem(ec_item)
                    ec_item.setPos(
                        QtCore.QPointF(bbox[0], bbox[1])
                        + QtCore.QPointF(c * c_quant, r * r_quant)
                    )
                    self.circles.append(ec_item)

    def _wrap_viewport_event(self, original_handler):
        def wrapped_event(event):
            if isinstance(event, QtGui.QTransformChangeEvent):
                scale = self.scene_ref.views()[0].transform().m11()
                if scale > self.scale_threshold:
                    self.setPen(self.normal_pen)
                else:
                    self.setPen(self.cosmetic_pen)
            return original_handler(event)

        return wrapped_event

    def animate_circles(self):

        self.is_animated = True
        for ob in self._circle_objects:
            ob.animate()

    def cleanup(self):
        from celer_sight_ai import config

        for i, circle in enumerate(self.circles):
            # stop the animation
            if self.is_animated:
                self._circle_objects[i].animation_group.stop()
            if self.scene_ref is not None:
                self.scene_ref.removeItem(circle)
        if self.scene_ref is not None:
            self.scene_ref.removeItem(self)
        # config.global_signals.annotation_generator_spinner_signal_stop.emit()


class AnimatedCircle:
    def __init__(self, item, radius=0, is_animated=False):
        self._radius = radius
        self._initial_radius = radius
        self.is_animated = is_animated
        self.item = item
        self.animation_proxy = AnimationProxy()
        self.set_radius(radius)
        self.animation_group = QtCore.QSequentialAnimationGroup()

        self.animate()

    def set_radius(self, value):
        self._radius = value
        # move it to the center
        self.item.setRect(
            -self._radius,
            -self._radius,
            self._radius * 2,
            self._radius * 2,
        )

    def animate(self, radius_change=1.4):
        if not self.is_animated:
            return
        duration = 1000
        large_val = self._initial_radius + (self._initial_radius * radius_change)
        # Animation from start_radius to mid_radius
        animation1 = QtCore.QPropertyAnimation(self.animation_proxy, b"value")
        animation1.setDuration(duration)
        animation1.setStartValue(self._initial_radius)
        animation1.setEndValue(large_val)
        animation1.valueChanged.connect(self.set_radius)

        # Animation from mid_radius to start
        animation2 = QtCore.QPropertyAnimation(self.animation_proxy, b"value")
        animation2.setDuration(duration)
        animation2.setStartValue(large_val)
        animation2.setEndValue(self._initial_radius)
        animation2.valueChanged.connect(self.set_radius)

        self.animation_group.addAnimation(animation1)
        self.animation_group.addAnimation(animation2)
        # self.animation_group.addAnimation(animation3)
        # self.animation_group.addAnimation(animation4)
        # loop
        self.animation_group.finished.connect(self.animation_group.start)
        # wait randomly between 0 and 1 seconds
        QtCore.QTimer.singleShot(
            int(random.random() * duration * 10), self.animation_group.start
        )

    def cleanup(self):
        # Stop the animation
        self.animation_group.stop()

        # Disconnect signals
        self.animation_group.finished.disconnect(self.animation_group.start)

        # Delete the animation
        del self.animation_group

        # Remove the item from the scene
        self.scene().removeItem(self)
