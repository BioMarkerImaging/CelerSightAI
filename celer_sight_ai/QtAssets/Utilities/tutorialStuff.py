from PyQt6 import QtCore, QtGui, QtWidgets
from celer_sight_ai.QtAssets.UiFiles.OrganismSelectrionDiaolog_tutorial import (
    Ui_Form as OrgTutorialUi,
)
from celer_sight_ai.QtAssets.UiFiles.NewMenu_tutorial import (
    Ui_Form as NewMenuForm_UI,
)


class NewMenu_tutorial(NewMenuForm_UI):
    def __init__(self, parent):
        super(NewMenu_tutorial, self).__init__()
        self.myWidget = QtWidgets.QWidget()
        self.setupUi(self.myWidget)
        self.myParent = parent
        self.myWidget.setParent(parent.AnalysisWidgetForm)
        self.positionsMoveBtn = [(650, 430), (25, 30), (25, 590)]
        self.positionsMoveWidget = [(100, 70), (500, 300), (100, 100)]

        self.elementOrder = [
            self.myParent.WholeBodyBtn,
            self.myParent.comboBox,
            self.myParent.CreateNewVButton,
        ]
        self.arrowWidget = QtWidgets.QPushButton(self.myParent.AnalysisWidgetForm)
        self.arrowWidget.setMinimumSize(QtCore.QSize(200, 200))
        self.arrowWidget.setMaximumSize(QtCore.QSize(200, 200))
        self.arrowWidget.setStyleSheet(
            """
                                        QPushButton{
                                            border: 0px solid;
                                        background-color: rgba(0,0,0,0)};
                                        QPushButton:hover{
                                        border: 0px solid;};
                                        """
        )
        icon = QtGui.QIcon()
        icon.addPixmap(
            QtGui.QPixmap("data//icons//icons_aa_tool//point_tutorial_newMenu_2.png"),
            QtGui.QIcon.Mode.Normal,
            QtGui.QIcon.State.Off,
        )
        self.arrowWidget.setIcon(icon)
        self.arrowWidget.setIconSize(QtCore.QSize(200, 200))
        #    (self.myParent.WholeBodyBtn.pos().x()-10,self.myParent.WholeBodyBtn.pos().y()+150))
        # (self.myParent.comboBox.pos().x()+10,self.myParent.comboBox.pos().y()+35))
        # (self.myParent.WholeBodyBtn.pos().x()-10,self.myParent.WholeBodyBtn.pos().y()+150))

        self.CreateNewVButton.clicked.connect(lambda: self.moveNextInstraction())

        text_info_1 = "To start off your analysis let's select the region you would like to measure! If you dont want to measure a specific region thats fine, select any part for now. For this tutorial lets say you would like to measure C.elegan's head..!"
        text_inst_1 = "Select C.elegan's head to move on."
        btn1 = "Skip"

        text_info_2 = "Great! CelerSight has set up everything for you to measure in the area of the head, now we need to select what we would like to measure! Lets say we would like to measure particles in the area of the head."
        text_inst_2 = "Select Aggregates in the analysis drop down menu."
        btn2 = "Skip"

        text_info_3 = "That's it! Now you are ready to start analyzing."
        text_inst_3 = "Select Procced to move on."
        btn3 = "Ok"

        self.btnText = [btn1, btn2, btn3]
        self.textInfo = [text_info_1, text_info_2, text_info_3]
        self.textInstraction = [text_inst_1, text_inst_2, text_inst_3]
        self.currentInstNum = 0
        self.FinalInstNum = 2
        self.moveNextInstraction()

    def createConnections(self):
        self.myParent.HeadBtn.clicked.connect(lambda: self.moveNextInstraction(1))
        self.myParent.comboBox.currentIndexChanged.connect(self.checkComboBoxIndex)

    def checkComboBoxIndex(self, index):
        if index == 2:
            self.moveNextInstraction(2)

    # def addLinks(self,Seq):
    #     if Seq == 0:
    #     if Seq == 1:

    def moveNextInstraction(self, presetToMove=None):
        if presetToMove:
            self.currentInstNum = presetToMove
            print("going to 2")
            self.updateTut()
            return
        self.updateTut()
        if self.currentInstNum + 1 >= self.FinalInstNum:
            return
        self.currentInstNum += 1

    def updateTut(self):
        self.pg1_settings_contras_label.setText(self.textInfo[self.currentInstNum])
        self.pg1_settings_contras_label_2.setText(
            self.textInstraction[self.currentInstNum]
        )
        self.CreateNewVButton.setText(self.btnText[self.currentInstNum])
        self.arrowWidget.move(
            self.positionsMoveBtn[self.currentInstNum][0],
            self.positionsMoveBtn[self.currentInstNum][1],
        )
        self.myWidget.move(
            self.positionsMoveWidget[self.currentInstNum][0],
            self.positionsMoveWidget[self.currentInstNum][1],
        )


class organismSelectionTutorial(OrgTutorialUi):
    def __init__(self, parent):
        super(organismSelectionTutorial, self).__init__()
        self.myWidget = QtWidgets.QWidget()
        self.setupUi(self.myWidget)
        self.myWidget.setParent(parent.myDialog)
        self.myWidget.setFixedWidth(parent.myDialog.width())
        self.myWidget.setFixedHeight(150)
        # self.myWidget.setFixedWidth(1000)
        self.myParent = parent
        self.myWidget.setStyleSheet("""background-color: rgba(250,250,250,255);""")
        self.myWidget.show()

        myeff = QtWidgets.QGraphicsBlurEffect()
        myeff.setBlurRadius(10)
        parent.mainframe.setGraphicsEffect(myeff)
        self.CreateNewVButton.clicked.connect(lambda: self.onAccept())
        self.myWidget.move(0, 200)

    def onAccept(self):
        self.myWidget.hide()
        self.myParent.mainframe.setGraphicsEffect(None)


if __name__ == "__main__":
    pass
