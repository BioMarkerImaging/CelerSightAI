from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtCore import pyqtSlot
from celer_sight_ai.QtAssets.UiFiles.overview_tabs_widget import (
    Ui_Form as overview_tabs_widget,
)


from celer_sight_ai.QtAssets.buttons.image_button import ButtonAssetClass


class WidgetOverviewTabs(QtWidgets.QWidget):
    def __init__(self, MainWindow):
        QtWidgets.QWidget.__init__(self, None)
        wheelEvent = self.wheelEvent
        self.SizeOfWidget = (170, 140)
        self.MainWindow = MainWindow
        self.IWidthNum = 2  # number which dettermins the with of the buttons
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum
        )
        self.setSizePolicy(sizePolicy)

    def makeLinks(self):  # needs to run after init and overfiew tabs is created
        self.myImLayout = self.MainWindow.image_preview_scrollArea_Contents.layout()

    def wheelEvent(self, event):
        if event.modifiers() == QtCore.Qt.Modifier.CTRL:
            self.makeLinks()
            print(self.myImLayout)
            if event.angleDelta().y() > 0:
                self.IWidthNum += 1
                self.updateButtonsInLayout()
            if event.angleDelta().y() < 0:
                self.IWidthNum -= 1
                self.updateButtonsInLayout()
        return super(WidgetOverviewTabs, self).wheelEvent(event)

    def layout_widgets(self, layout):
        return (layout.itemAt(i).widget() for i in range(layout.count()))

    def updateWidgetPos(self):
        if self.myImLayout.count() != 0:
            allWidgetList = []
            for i in range(self.myImLayout.count()):
                allWidgetList.append(self.myImLayout.itemAt(i).widget())
            for myWid in allWidgetList:
                self.myImLayout.removeWidget(myWid)
            XWithNum = self.getGridsFromWidth()
            outList = self.genTurpleGrid(100, XWithNum)
            allItems = 0
            FinalNum = len(allWidgetList)
            for pos in outList:
                self.myImLayout.addWidget(allWidgetList[allItems], pos[0], pos[1])
                allItems += 1
                if FinalNum == allItems:
                    return

    def getGridsFromWidth(self):
        myWidth = self.MainWindow.image_preview_scrollArea.width()
        import math

        Fit = math.floor(myWidth / self.myImLayout.itemAt(0).widget().width)
        return Fit

    def genTurpleGrid(self, width=2, height=8):
        outList = []
        for x in range(width):
            for y in range(height):
                # print(x,y)
                outList.append((x, y))
        return outList

    # def placeWidgets(self):
    #     xNums = 5
    #     yNums = 5
    #     myPol = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum,\
    #         QtWidgets.QSizePolicy.Policy.Minimum )

    #     for x in range(xNums):
    #         for y in range(yNums):
    #             myB = QtWidgets.QPushButton(Form)
    #             myB.setSizePolicy(myPol)
    #             myB.setMaximumSize(QtCore.QSize(50,50))
    #             myB.setMinimumSize(QtCore.QSize(50,50))

    #             myB.setText(str((xNums * y)+x))
    #             self.gridLayout.addWidget(myB,y,x)

    def updateButtonsInLayout(self):
        for item in self.layout_widgets(self.myImLayout):
            if item.isVisible() and type(item) == ButtonAssetClass:
                item.setParent(None)
                print(item)


class overviewTabsUi(overview_tabs_widget):
    def __init__(self, parent=None):
        self.WidgetOverviewTabs = WidgetOverviewTabs()
        self.setupUi(self.WidgetOverviewTabs)
