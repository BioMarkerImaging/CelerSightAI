from PyQt6 import QtCore, QtGui, QtWidgets


class PopUpPhotoViewer(QtWidgets.QGraphicsView):
    photoClicked = QtCore.pyqtSignal(QtCore.QPoint)
    object_signal = QtCore.pyqtSignal()

    def __init__(self, MainWindow=None):
        super(PopUpPhotoViewer, self).__init__()
        # super(Ui_MainWindow, self).__init__()
        from celer_sight_ai import config

        self.setMouseTracking(True)
        self.installEventFilter(self)
        self.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)
        self.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)
        self.setRenderHint(QtGui.QPainter.RenderHint.SmoothPixmapTransform)
        self._photo = QtWidgets.QGraphicsPixmapItem()
        self._photo.setZValue(-50)
        self._scene = QtWidgets.QGraphicsScene(self)
        self.setScene(self._scene)
        self.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)

    def hasPhoto(self):
        return not self._empty

    def fitInView(self):  # , scale=True):
        self._zoom = 0
        rect = QtCore.QRectF(self._photo.pixmap().rect())
        if not rect.isNull():
            self.setSceneRect(rect)
            if self.hasPhoto():
                unity = self.transform().mapRect(QtCore.QRectF(0, 0, 1, 1))
                # print(unity.width())
                self.scale(1 / unity.width(), 1 / unity.height())
                viewrect = self.viewport().rect()
                scenerect = self.transform().mapRect(rect)
                # print(viewrect.width())
                # print(viewrect.height())
                # print(viewrect.width())
                # print(viewrect.height())
                factor = min(
                    viewrect.width() / scenerect.width(),
                    viewrect.height() / scenerect.height(),
                )
                self.scale(factor, factor)
            self._zoom = 0

    def setPhoto_and_mask(self, pixmap=None):
        self._zoom = 0
        self.Cpixmap = pixmap
        print(type(pixmap))
        # if pixmap and not pixmap.isNull():
        self._empty = False
        # self.setDragMode(QtWidgets.QGraphicsView.DragMode.ScrollHandDrag)
        self._photo.setPixmap(pixmap)
        # else:
        #     self._empty = True
        #     self.setDragMode(QtWidgets.QGraphicsView.DragMode.NoDrag)
        #     self._photo.setPixmap(QtGui.QPixmap())

    def setPhoto(self, pixmap=None, fit_in_view_state=True):
        # self.pixmap = pixmap
        self._zoom = 0
        if pixmap and not pixmap == 0:
            self._empty = False
            self.setDragMode(QtWidgets.QGraphicsView.DragMode.NoDrag)
            # self.setDragMode(QtWidgets.QGraphicsView.DragMode.ScrollHandDrag)
            print("this runs!")
            self._photo.setPixmap(pixmap)
            self._scene.addItem(self._photo)
            print("ok after adding")
        else:
            return
            self._empty = True
            self.setDragMode(QtWidgets.QGraphicsView.DragMode.NoDrag)
            self._photo.setPixmap(QtGui.QPixmap())
        if fit_in_view_state == True:
            self.fitImageInView()
        else:
            pass
        # self.loadPixmap(pixmap)
        # self.setEnabled(True)
        # self.adjustSize()
        # self.update()
        # self._scale = 1
        # self.toggleActions(True)

    def wheelEvent(self, event):
        if self.hasPhoto():
            if event.angleDelta().y() > 0:
                factor = 1.15  # 1.25
                self._zoom += 1
            else:
                factor = 0.9  # 0.8
                self._zoom -= 1
            if self._zoom > 0:
                self.scale(factor, factor)
            elif self._zoom == 0:
                self.fitInView()
            else:
                self._zoom = 0

    def setDragMode_mc(self, mode):
        if mode == QtWidgets.QGraphicsView.DragMode.ScrollHandDrag:
            self.setDragMode(QtWidgets.QGraphicsView.DragMode.NoDrag)
        elif mode == QtWidgets.QGraphicsView.DragMode.NoDrag:
            self.setDragMode(QtWidgets.QGraphicsView.DragMode.ScrollHandDrag)

    def setBrush(self, brush):
        self._brush = brush
        self.update()

    def boundingRect(self):
        return self.rectF

    def paint(self, painter=None, style=None, widget=None):
        painter.fillRect(self.rectF, self._brush)

    def toggleDragMode(self):
        if not self.dragMode() == QtWidgets.QGraphicsView.DragMode.ScrollHandDrag:
            self.setDragMode_mc(QtWidgets.QGraphicsView.DragMode.NoDrag)
        else:
            self.setDragMode_mc(QtWidgets.QGraphicsView.DragMode.ScrollHandDrag)
