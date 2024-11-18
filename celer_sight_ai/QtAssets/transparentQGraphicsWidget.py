from PyQt6 import QtGui, QtCore, QtWidgets


class TransparentGraphicsWidget(QtWidgets.QGraphicsProxyWidget):
    def __init__(self):
        super(TransparentGraphicsWidget, self).__init__()

    def mousePressEvent(self, event: "QGraphicsSceneMouseEvent") -> None:
        print("TransparentGraphicsWidget.mousePressEvent")
        if event.type() == QtCore.QEvent.Type.GraphicsSceneMousePress:
            # if its the right click, only spawn the context menu
            if event.button() == QtCore.Qt.MouseButton.RightButton:
                return
            print("TransparentGraphicsWidget.mousePressEvent: GraphicsSceneMousePress")
            MainButton = self.widget().findChild(
                QtWidgets.QPushButton, "MainAssetButton"
            )
            MainButton.click()
        return super().mousePressEvent(event)


if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    # Create the graphics scene and view
    scene = QtWidgets.QGraphicsScene()
    view = QtWidgets.QGraphicsView(scene)
    # view.setRenderHint(QtGui.QPainter.Antialiasing)

    # Create the transparent graphics widget
    transparent_widget = TransparentGraphicsWidget()
    scene.addItem(transparent_widget)

    # Show the view and run the application
    view.show()
    app.exec()
