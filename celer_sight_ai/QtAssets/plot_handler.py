"""
This class will handle all the plot settings ranging
with import functions to variables and multiplot handling
"""
from PyQt6 import QtCore, QtGui, QtWidgets
from celer_sight_ai.QtAssets.UiFiles.plotSpecificWidget import (
    Ui_Form as specificPlotWidgetUi,
)
import seaborn as sns
import matplotlib
from matplotlib import pyplot as plt
from celer_sight_ai.QtAssets.buttons.animate_qpushbutton import myRichTextEdit
import logging

logger = logging.getLogger(__name__)
matplotlib._log.disabled = True
# Turn off sina logging
for name in ["matplotlib", "matplotlib.font", "matplotlib.pyplot"]:
    logger = logging.getLogger(name)
    logger.setLevel(logging.CRITICAL)
    logger.disabled = True

# import seaborn as sns


class PlotViewerHandler:  # instance is --MyVisualPlotHandler!
    def __init__(self, MainWindow):
        """
        This widget handles the visual part of the viewer plot scroll area
        """
        # self.Ui_plot = Ui_plot
        self.MainWindow = MainWindow
        self.CurrentWidget = (
            None  # the widhet which we have selected string object, current opbject in
        )
        # ,the name to be indexted at the dictionary, pg2_graphs_view
        self.WidgetDictionary = {}
        self.hoverRichTextActive = False
        """
        Notes, when widget change:
            update current widget
            update UI by hiding and showing the necessary groups
        """
        self.specificPlotWidgetRef = {}
        self.firstNewAnalysis = True  # reset everytime we analyze

        # load all plot presets on plot page
        self.loadAllPlots("data/palletePresets/plotCombinations/*.png")
        self.mainPlotTitle = ""
        self.xLabelPlotText = ""
        self.yLabelPlotText = ""
        self.hoverLabelText = ""
        self.hoverLabelTextList = []
        self.labelOfInterestText = []
        self.labelsList = None
        self.hoverRichTextBoxSpawned = False
        self.tmpHoverRichText = None

        self.myFontSize = 12
        self.myFontFamily = "helvetica"

        self.myTitleFontSize = None
        self.myTitleFontFamily = None
        self.myXTitleFontSize = None
        self.myYTitleFontSize = None
        self.myXTitleFontFamily = None
        self.myYTitleFontFamily = None
        self.myXTicksFontSize = None
        self.myYTicksFontSize = None
        self.myXTicksFontFamily = None
        self.myYTicksFontFamily = None

        self.prevSelectedTextComboBox = "title"

        self.mainPlotTitleFontDict = {
            "family": "serif",
            "color": "black",
            "weight": "normal",
            "size": 16,
        }
        self.xLabelPlotTextFontDict = {
            "family": "serif",
            "color": "black",
            "weight": "normal",
            "size": 16,
        }

        self.yLabelPlotTextFontDict = {
            "family": "serif",
            "color": "black",
            "weight": "normal",
            "size": 16,
        }

        self.hoverLabelTextFontDict = {
            "family": "serif",
            "color": "black",
            "weight": "normal",
            "size": 16,
        }

    def initInteractionSettings(self, axis):
        self.PatchesColorNOW = []
        self.PatchesColorEdge = []
        self.PatchesIDNOW = []
        self.isOverLegend = []  # label list
        axis.figure.canvas.callbacks.connect(
            "button_press_event", self.onclick_MATPLOTLIB_EVENT
        )
        axis.figure.canvas.callbacks.connect(
            "motion_notify_event", self.underMouse_MATPLOTLIB_EVENT
        )

        # self.hoverLabelTextList = []
        # self.labelOfInterestTextFinal = []
        # self.labelOfInterestTextOriginal = []

        # self.myLegends = []
        # if self.firstNewAnalysis == True:
        # self.firstNewAnalysis = False
        if self.firstNewAnalysis == True:
            self.firstNewAnalysis = False
            self.labelsList = []
            for item in axis.get_children():
                if isinstance(item, matplotlib.axis.XAxis):
                    allXItems = item.get_majorticklabels()
                    for someXItem in allXItems:
                        for SomePreviousItemX in self.labelsList:
                            if (
                                SomePreviousItemX["originalText"]
                                == someXItem.get_text()
                            ):
                                continue
                        tmpDict = self.getLabelDictNewCopy()
                        tmpDict["originalText"] = someXItem.get_text()
                        tmpDict["FinalNewText"] = someXItem.get_text()
                        tmpDict["legendRef"] = someXItem
                        self.labelsList.append(tmpDict)
                if isinstance(item, matplotlib.axis.YAxis):
                    allYItems = item.get_majorticklabels()
                    for someYItem in allYItems:
                        for SomePreviousItemY in self.labelsList:
                            if (
                                SomePreviousItemY["originalText"]
                                == someXItem.get_text()
                            ):
                                continue
                        tmpDict = self.getLabelDictNewCopy()
                        tmpDict["originalText"] = someYItem.get_text()
                        tmpDict["FinalNewText"] = someYItem.get_text()
                        tmpDict["legendRef"] = someYItem
                        self.labelsList.append(tmpDict)
            # for SomeOtheritem in self.myLegends:
            #     self.hoverLabelTextList.append(SomeOtheritem.get_text())
            #     self.labelOfInterestTextOriginal.append(SomeOtheritem.get_text())
            # for i in range(len(self.myLegends)):
            #     self.isOverLegend.append(False)
        return axis

    def getLabelDictNewCopy(self):
        labelDictChanged = {
            "originalText": None,
            "FinalNewText": None,
            "hover": False,
            "legendRef": None,
        }
        return labelDictChanged

    def onclick_MATPLOTLIB_EVENT(self, event):
        print("click event")
        if self.hoverRichTextActive:
            self.removeHoverRichTextBox()
        if event.dblclick:
            # print(event.button)
            # print(self.labelsList)
            for i in range(len(self.labelsList)):
                if self.labelsList[i]["hover"] == True:
                    labelText = self.labelsList[i]["FinalNewText"]
                    cursor = QtGui.QCursor()
                    currentClickPos = self.MainWindow.MainWindow.mapFromGlobal(
                        cursor.pos()
                    )
                    # print('spawning hover rich text')
                    self.spawnHoverRichTextBox(labelText, i, currentClickPos)

    def removeHoverRichTextBox(self):
        QtWidgets.QApplication.processEvents()
        # if self.tmpHoverRichText:
        if self.hoverRichTextActive == True:
            self.tmpHoverRichText.assignTextToPlotHandler()
            self.labelsList[self.tmpHoverRichText.labelListId][
                "FinalNewText"
            ] = self.hoverLabelText
            self.tmpHoverRichText.hide()
            QtWidgets.QApplication.processEvents()

            self.tmpHoverRichText.deleteLater()
            self.tmpHoverRichText = None
            self.hoverRichTextActive = False

    def spawnHoverRichTextBox(self, legendText, labelListId, pos):
        # self.canvas2Frame <-add wiget here
        self.hoverRichTextActive = True
        self.tmpHoverRichText = myRichTextEdit(self.MainWindow)
        self.tmpHoverRichText.setAttributesInit(self.MainWindow, "hover")
        self.tmpHoverRichText.setParent(self.MainWindow.MainWindow)
        self.tmpHoverRichText.setText(legendText)
        self.tmpHoverRichText.labelListId = labelListId
        # print('moving to pos ', pos.x())
        # print(pos.y())

        self.tmpHoverRichText.move(pos)
        self.tmpHoverRichText.setFixedHeight(35)
        self.tmpHoverRichText.setFixedWidth(300)
        self.tmpHoverRichText.setStyleSheet("border-radius: 10px;")
        self.MainWindow.AddShadowToWidget(self.tmpHoverRichText)
        self.tmpHoverRichText.show()

    def underMouse_MATPLOTLIB_EVENT(self, event):
        for i, patch in enumerate(self.PatchesIDNOW):
            patch.set_facecolor(self.PatchesColorNOW[i])
            patch.set_edgecolor(self.PatchesColorNOW[i])
        loops = 0
        self.PatchesColorNOW = []
        self.PatchesIDNOW = []
        LegIter = 0
        for item in self.labelsList:
            if item["legendRef"].contains(event)[0]:
                self.MainWindow.canvas2Frame.setCursor(
                    QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor)
                )
                item["hover"] = True
            else:
                item["hover"] = False
                self.MainWindow.canvas2Frame.setCursor(
                    QtGui.QCursor(QtCore.Qt.CursorShape.ArrowCursor)
                )

            LegIter += 1
        # if self.violinChildren:
        #     for patch in self.violinChildren:
        #         if patch.contains(event)[0] ==True:
        #             if isinstance(patch, PolyCollection): # The whole polygon
        #                 self.recordPatchFace(patch)
        #                 patch.set_facecolor((1,1,0))
        #                 loops +=0.33
        #                 pass
        # if self.barChildren:
        #     for patch in self.barChildren:
        #         if patch.contains(event)[0] == True:
        #             if isinstance(patch, Rectangle): #idk what this is
        #                 self.recordPatchFace(patch)
        #                 patch.set_color((1,1,0))

        self.MainWindow.canvas.draw()
        self.MainWindow.canvas.update()
        pass

    def loadAllPlots(self, loadFolder=""):
        import glob
        import cv2

        allPresetsPNG = glob.glob(loadFolder)
        import os

        for myPreset in allPresetsPNG:
            if myPreset.find("_NORMAL") != -1:
                # keep only imagename
                myPreset_basename = os.path.basename(myPreset)
                self.myPlotImgButtonStyle = plotStylesButton(
                    myPreset_basename, self.MainWindow
                )
                self.MainWindow.pg_2_plot_parameteres_scrollAreaWidgetContentshorizontalLayout_2.addWidget(
                    self.myPlotImgButtonStyle, 1
                )
            else:
                continue

        verticalSpacer = QtWidgets.QSpacerItem(
            40,
            40,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.MainWindow.pg_2_plot_parameteres_scrollAreaWidgetContentshorizontalLayout_2.addItem(
            verticalSpacer
        )

    # @staticmethod
    def DeterminePlotClass(self, ClassString, SuggestedName):
        # print("determine xlass of the plot ", ClassString)
        if str(ClassString) == "Bar Plot":
            BarPlot_usr = BarPlot(self.MainWindow)
            return BarPlot_usr
        if str(ClassString) == "Violin Plot":
            return ViolinPlot(self.MainWindow)
        if str(ClassString) == "Box Plot":
            BoxPlot_usr = BoxPlot(self.MainWindow)
            return BoxPlot_usr
        if str(ClassString) == "Dot Plot":
            DotPlot_usr = DotPlot(self.MainWindow)
            return DotPlot_usr
        if str(ClassString) == "Swarm Plot":
            SwarmPlot_usr = SwarmPlot(self.MainWindow)
            return SwarmPlot_usr
        # if str(ClassString) == "Strip Plot":

        else:
            print("cant find match")

    def getInitSnsPallete(self):
        """
        Gets the first pallete when we add a plot,
        if we have a plot already copy its colorsm otherwise make new pallete
        """
        color_list = []
        if self.MainWindow.pg2_graphs_view.count() <= 1:
            import seaborn as sns

            color_list = sns.color_palette("coolwarm", 50)
            return color_list
        elif self.MainWindow.pg2_graphs_view.count() != 0:
            import matplotlib

            for i in range(
                self.MainWindow.pg_2_graph_colors_groupBox_listWidget.count()
            ):
                itemWidget = (
                    self.MainWindow.pg_2_graph_colors_groupBox_listWidget.itemWidget(
                        self.MainWindow.pg_2_graph_colors_groupBox_listWidget.item(i)
                    )
                )
                myPrimaryColor = itemWidget.findChild(
                    QtWidgets.QPushButton, "PrimaryColor"
                )
                currentHexColor = myPrimaryColor.palette().button().color().name()

                color_list.append(matplotlib.colors.to_rgb(currentHexColor))
            return color_list

    def applyPalleteToListItemWidgetsForPlot(self, color_list):
        """
        applies the color list pallete rgb to pg_2_graph_colors_groupBox_listWidget item widgets
        """
        for i in range(self.MainWindow.pg_2_graph_colors_groupBox_listWidget.count()):
            itemWidget = self.MainWindow.pg_2_graph_colors_groupBox_listWidget.item(i)
            itemWidget.PrimaryColor.setStyleSheet(
                "background-color: rgb("
                + color_list[i][0]
                + ","
                + color_list[i][1]
                + ","
                + color_list[i][2]
                + ");"
            )

    def spawnPalletePicker(self):
        self.myPalleteColorPickerDialog = palleteColorPickerDialog(self.MainWindow)
        self.myPalleteColorPickerDialog.myWidget.exec()

    def getAvaibleMainColors(self, PlotName=None):
        """
        Get the available colors and return a list of the rgb values
        """
        import matplotlib

        outPutColorList = []
        # for i in range(len(self.MyVisualPlotHandler.specificPlotWidgetRef[nameWidget])):
        for myWidgetList in self.specificPlotWidgetRef[PlotName]:
            specificItemWidget = (
                self.MainWindow.pg_2_graph_colors_groupBox_listWidget.itemWidget(
                    myWidgetList
                )
            )

            primarayBtn = specificItemWidget.findChild(
                QtWidgets.QPushButton, "PrimaryColor"
            )
            primarayBtnColor = primarayBtn.palette().button().color().name()
            outPutColorList.append(matplotlib.colors.to_rgb(primarayBtnColor))
        return outPutColorList

    def getCompletePalleteMainColors(self, PlotName=None, amount=30):
        """
        get a complete pallete of all the colors along with the ones used now and ones not used
        """
        import matplotlib

        outPutColorList = []
        iterator = 0
        # for i in range(len(self.MyVisualPlotHandler.specificPlotWidgetRef[nameWidget])):
        for myWidgetList in self.specificPlotWidgetRef[PlotName]:
            specificItemWidget = (
                self.MainWindow.pg_2_graph_colors_groupBox_listWidget.itemWidget(
                    myWidgetList
                )
            )

            primarayBtn = specificItemWidget.findChild(
                QtWidgets.QPushButton, "PrimaryColor"
            )
            primarayBtnColor = primarayBtn.palette().button().color().name()
            outPutColorList.append(matplotlib.colors.to_rgb(primarayBtnColor))
            iterator += 1
        while iterator != amount:
            outPutColorList.append(
                self.MainWindow.MyVisualPlotHandler.WidgetDictionary[
                    PlotName
                ].sdPallete[iterator]
            )
            iterator += 1
        return outPutColorList

    def getAvaibleEdgeColors(self, PlotName=None):
        """
        Get the available colors and return a list of the rgb values
        """
        import matplotlib

        outPutColorList = []
        # for i in range(len(self.MyVisualPlotHandler.specificPlotWidgetRef[nameWidget])):
        for myWidgetList in self.specificPlotWidgetRef[PlotName]:
            specificItemWidget = (
                self.MainWindow.pg_2_graph_colors_groupBox_listWidget.itemWidget(
                    myWidgetList
                )
            )

            primarayBtn = specificItemWidget.findChild(
                QtWidgets.QPushButton, "EdgeColor"
            )
            primarayBtnColor = primarayBtn.palette().button().color().name()
            outPutColorList.append(matplotlib.colors.to_rgb(primarayBtnColor))
        return outPutColorList

    def change_width(self, patches, WidthVal):
        for patch in patches:
            print("patch is ", patch)
            current_width = patch.get_width()
            diff = current_width - WidthVal
            # we change the bar width
            patch.set_width(WidthVal)
            # we recenter the bar
            patch.set_x(patch.get_x() + diff * 0.5)
        return patches

    def change_edgeWidth(self, patches, WidthVal):
        for patch in patches:
            # we change the bar Linewidth
            patch.set_linewidth(WidthVal)
        return patches

    def PlotSeaborn(self, UiPlotSettings, PlotHandler, axis, DataFrame):
        """
                Ui_Plot_tools_widget is UiPlotSettings

                inputs are: self.plot_bar,self.MyVisualPlotHandler, ax1 verticalSpacer = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        layout.addItem(verticalSpacer),dataframe_f
        """
        OverAllZOrder = 1
        import seaborn as sns
        import matplotlib.pyplot as plt

        # print("range of Ui plot settings graphs view is ", UiPlotSettings.pg2_graphs_view.count())
        for i in range(UiPlotSettings.pg2_graphs_view.count()):
            item = UiPlotSettings.pg2_graphs_view.item(i)
            ItemsName = item.text()
            # check with the values form he handler from the dictionary if type ==
            # print(PlotHandler.WidgetDictionary)
            # print(item.text())
            # Create a dictionary of all the "indexes"
            MyGraphItem = PlotHandler.WidgetDictionary[item.text()]

            if "Bar Plot" == PlotHandler.WidgetDictionary[item.text()].type:
                print("running barplot")
                prevAxPatches = axis.patches.copy()
                prevAxLines = axis.lines.copy()
                axis = sns.barplot(
                    data=DataFrame,
                    x="condition",
                    y="values",
                    fill="condition",
                    ax=axis,
                    edgecolor=self.getAvaibleEdgeColors(ItemsName),
                    saturation=MyGraphItem.BarSaturation,
                    orient=MyGraphItem.BarOrient,
                    palette=self.getAvaibleMainColors(ItemsName),
                    capsize=MyGraphItem.BareCapSize,
                    errwidth=MyGraphItem.BareWidth,
                    alpha=MyGraphItem.BarOpacity,
                    zorder=OverAllZOrder,
                )
                # )  # color=MyGraphItem.BarColor,
                OverAllZOrder += 1
                myPatches = list(set(axis.patches) - set(prevAxPatches))
                myLines = list(set(axis.lines) - set(prevAxLines))
                myPatches = self.change_width(myPatches, MyGraphItem.BarWidth)
                myPatches = self.change_edgeWidth(myPatches, MyGraphItem.BoxBorderWidth)
                for line in myLines:
                    line.set(zorder=OverAllZOrder)
                OverAllZOrder += 1

            elif "Swarm Plot" == PlotHandler.WidgetDictionary[item.text()].type:
                print("running swarm plot")
                MyGraphItem = PlotHandler.WidgetDictionary[item.text()]
                axis = sns.swarmplot(
                    x="condition",
                    y="values",
                    data=DataFrame,
                    ax=axis,  # edgecolor=MyGraphItem.self.getAvaibleEdgeColors(ItemsName),
                    linewidth=MyGraphItem.SwarmWidth,
                    palette=self.getAvaibleMainColors(ItemsName),
                    size=MyGraphItem.SwarmSize,
                    orient=MyGraphItem.SwarmOrient,
                    zorder=OverAllZOrder,
                )
                OverAllZOrder += 1
            elif "Box Plot" == PlotHandler.WidgetDictionary[item.text()].type:
                print("running box plot")
                MyGraphItem = PlotHandler.WidgetDictionary[item.text()]
                # sns.set_palette(MyGraphItem.Box_palette)

                # print(MyGraphItem.BoxOrient)
                axis = sns.boxplot(
                    data=DataFrame,
                    x="condition",
                    y="values",
                    ax=axis,
                    width=MyGraphItem.BoxWidth,
                    orient=MyGraphItem.BoxOrient,  # edgecolor=self.getAvaibleEdgeColors(ItemsName),
                    saturation=MyGraphItem.BoxSaturation,
                    linewidth=MyGraphItem.BoxBorderWidth,
                    fliersize=MyGraphItem.BoxFlierSize,
                    palette=self.getAvaibleMainColors(ItemsName),
                    zorder=OverAllZOrder,
                )
                OverAllZOrder += 1
                edgecolors = self.getAvaibleEdgeColors(ItemsName)
                # plt.setp(box.lines, color=edgecolors[0])
                for i, artist in enumerate(axis.artists):
                    # print(artist)

                    col = (0, 0, 0)
                    # This sets the color for the main box
                    artist.set_edgecolor(col)
                    # Each box has 6 associated Line2D objects (to make the whiskers, fliers, etc.)
                    # Loop over them here, and use the same colour as above
                    for j in range(i * 6, i * 6 + 6):
                        line = axis.lines[j]
                        line.set_color(col)
                        line.set_mfc(col)
                        line.set_mec(col)

                plt.setp(axis.artists)
                OverAllZOrder += 1

            elif "Dot Plot" == PlotHandler.WidgetDictionary[item.text()].type:
                MyGraphItem = PlotHandler.WidgetDictionary[item.text()]
                OverAllZOrder += 1

            elif "Strip Plot" == PlotHandler.WidgetDictionary[item.text()].type:
                MyGraphItem = PlotHandler.WidgetDictionary[item.text()]

                sns.stripplot(
                    data=DataFrame,
                    x="condition",
                    y="values",
                    ax=axis,
                    width=MyGraphItem.BoxWidth,
                    orient=MyGraphItem.BoxOrient,
                    saturation=MyGraphItem.BoxSaturation,
                    linewidth=MyGraphItem.BoxBorderWidth,
                    palette=self.getAvaibleMainColors(ItemsName),
                )
                OverAllZOrder += 1

                print(
                    "its not working bro, plot seaborn ",
                    PlotHandler.WidgetDictionary[item.text()].type,
                )
            elif "Violin Plot" == PlotHandler.WidgetDictionary[item.text()].type:
                print("running violin plot")
                MyGraphItem = PlotHandler.WidgetDictionary[item.text()]

                if MyGraphItem.ViolinInner == "none":
                    myViolinInner = None
                else:
                    myViolinInner = MyGraphItem.ViolinInner
                axis = sns.violinplot(
                    data=DataFrame,
                    x="condition",
                    y="values",
                    ax=axis,
                    cut=MyGraphItem.ViolinCut,
                    scale=MyGraphItem.ViolinScale,
                    width=MyGraphItem.ViolinWidth,
                    orient=MyGraphItem.ViolinOrient,
                    edgecolor=self.getAvaibleEdgeColors(ItemsName),
                    linewidth=MyGraphItem.ViolinBorderWidth,
                    pallete=self.getAvaibleMainColors(ItemsName),
                    saturation=MyGraphItem.ViolinSaturation,
                    inner=myViolinInner,
                    zorder=OverAllZOrder,
                )
                OverAllZOrder += 1

        # Axis names and background

        self.MainWindow.pg_2_Title_textedit.assignTextToPlotHandler()
        self.MainWindow.pg_2_y_axis_textedit_2.assignTextToPlotHandler()
        self.MainWindow.pg_2_x_axis_textedit.assignTextToPlotHandler()

        # setTitle

        if self.myTitleFontSize == None:
            fontSizeUsed = self.myFontSize
        else:
            fontSizeUsed = self.myTitleFontSize

        if self.myTitleFontFamily == None:
            fontFamilyUsed = self.myFontFamily
        else:
            fontFamilyUsed = self.myTitleFontFamily

        if self.MainWindow.pg_2_Title_textedit.toPlainText() != None:
            axis.set_title(
                self.mainPlotTitle,
                fontdict=self.mainPlotTitleFontDict,
                fontsize=fontSizeUsed,
                fontfamily=fontFamilyUsed,
            )

        # setXLabel

        if self.myXTitleFontSize == None:
            fontSizeUsed = self.myFontSize
        else:
            fontSizeUsed = self.myXTitleFontSize

        if self.myXTitleFontFamily == None:
            fontFamilyUsed = self.myFontFamily
        else:
            fontFamilyUsed = self.myXTitleFontFamily

        if self.MainWindow.pg_2_y_axis_textedit_2.toPlainText() != None:
            axis.set_xlabel(
                self.xLabelPlotText,
                fontdict=self.xLabelPlotTextFontDict,
                fontsize=fontSizeUsed,
                fontfamily=fontFamilyUsed,
            )
        # setYLabel

        if self.myYTitleFontSize == None:
            fontSizeUsed = self.myFontSize
        else:
            fontSizeUsed = self.myYTitleFontSize

        if self.myYTitleFontFamily == None:
            fontFamilyUsed = self.myFontFamily
        else:
            fontFamilyUsed = self.myYTitleFontFamily

        if self.MainWindow.pg_2_x_axis_textedit.toPlainText() != None:
            axis.set_ylabel(
                self.yLabelPlotText,
                fontdict=self.yLabelPlotTextFontDict,
                fontsize=fontSizeUsed,
                fontfamily=fontFamilyUsed,
            )

        if self.myXTicksFontSize == None:
            fontSizeUsed = self.myFontSize
        else:
            fontSizeUsed = self.myXTicksFontSize

        if self.myXTicksFontFamily == None:
            fontFamilyUsed = self.myFontFamily
        else:
            fontFamilyUsed = self.myXTicksFontFamily

        majorTicks = axis.xaxis.get_majorticklabels()
        # significance visualization
        # print('first analysis iz ',self.firstNewAnalysis)
        # if self.firstNewAnalysis == False:
        # print('labnel list is ', self.labelsList)
        for i in range(len(majorTicks)):
            textToCheck = majorTicks[i].get_text()
            # print('text is ',textToCheck)
            if self.labelsList:
                for someDict in self.labelsList:
                    if someDict["originalText"] == textToCheck:
                        textFinal = someDict["FinalNewText"]
                        # if '_{' not in textFinal and '^{' not in textFinal and '\it{' not in textFinal and '\\bf{' not in  textFinal:
                        #     textFinal = textFinal[1:-1].replace("\ ", " ")
                        majorTicks[i].set_text(textFinal)
        axis.set_xticklabels(
            axis.get_xticklabels(),
            rotation=45,
            horizontalalignment="right",
            fontsize=fontSizeUsed,
            fontfamily=fontFamilyUsed,
        )

        if hasattr(self.MainWindow, "MyStatistics"):
            if self.MainWindow.MyStatistics != None:
                try:
                    from statannot import add_stat_annotation

                    add_stat_annotation(
                        axis,
                        data=DataFrame,
                        x="condition",
                        y="values",
                        box_pairs=self.MainWindow.MyStatistics.significansPairs,
                        test="t-test_welch",
                        text_format="star",
                        loc="inside",
                        verbose=1,
                    )
                except:
                    pass
                # add rows to listWidget Comparison Statistical

        return axis

    @staticmethod
    def CheckDictionaryName(SuggestedName, MyDictionary):
        """
        This functions finds a unique name for a string and a dictionary of choice
        """
        TotalIterations = 0
        GeneratedName = str(SuggestedName)
        Found = False
        DictLength = len(MyDictionary)
        if DictLength == 0:
            return SuggestedName
        else:
            while DictLength > 0:
                """
                This function will run until the DictLenfth reaches 0
                It renews when it finds a match with a new GeneratedName
                if there is a name (Generatore or susggested) thta is not int the list
                it will reach 0 and it will return the Generated Name
                """
                for name, value in MyDictionary.items():  # iterate all items
                    if str(name) == str(GeneratedName):
                        DictLength = len(
                            MyDictionary
                        )  # reset the dictlength to start over
                        if TotalIterations == 0:
                            GeneratedName = str(SuggestedName) + str(
                                TotalIterations + 1
                            )
                            Found = True
                            break
                        elif TotalIterations != 0:
                            str(GeneratedName[: TotalIterations - 1])
                            GeneratedName = str(SuggestedName) + str(
                                TotalIterations + 1
                            )
                            Found = True
                            break
                        else:
                            GeneratedName = str(SuggestedName) + str(
                                TotalIterations + 1
                            )
                            Found = True
                            break
                    else:
                        DictLength -= 1
                        continue
                TotalIterations += 1
                # print(DictLength)

                # DictLength = len(MyDictionary)
        if Found == True:
            return GeneratedName
        return SuggestedName


class MyConditionVisuals:
    """
    This class is responsible for each specific condition
    to have its own Specific properties, such as color etc
    """


class MyPlotHandler:
    def __init__(self, Ui_plot, myfigure, data, ax):
        # init my global variables to class variables
        self.Ui_plot = Ui_plot
        self.MyFigure = myfigure
        self.ax = ax
        """
        general plot settings go here
        """
        self._Xlabel = ""
        self._Ylabel = ""

        self._PlotTitle = ""
        self._Height = 0
        self._Width = 0
        self._Resolution = 0
        self.data = data

    def add_plot_to_final(self, plot_class):
        # Ui_plot.pg2_graphs_view.additem()
        pass
        # for i in range(Ui_plot.pg2_graphs_view.count()):
        #     item = Ui_plot.pg2_graphs_view.item(i)
        #     if

    def plot(self):
        import seaborn as sns

        sns.barplot(
            data=self.data, x="condition", y="values", fill="condition", ax=self.ax
        )
        sns.swarmplot(x="condition", y="values", data=self.data, ax=self.ax)
        return self.ax


class BarPlot:
    def __init__(self, MainWindow=None):
        self.MainWindow = MainWindow
        self.type = "Bar Plot"
        self.x = None
        self.name = None
        self.height = 0
        self.width = 0
        self.data = None
        self.LineWidth = 1
        self.TickLabel = None
        self.eCapStyle = None
        self.JoinStyle = None
        self.LineStyle = None
        self.Bar_Color = []
        self.Bar_EdgeColor = []
        self.Bar_palette = "Custom"
        self.Bar_eWidth = 5
        self.Bar_Opacity = 100
        self.Bar_Saturation = 100
        self.Bar_Condition = "All"
        self.Bar_eColor = []  # color of the errorbars
        self.Bar_Orientation = "v"  # or horizontal
        self.Bar_eCapSize = 0

        self.sdPallete = sns.color_palette("coolwarm", 50)
        self.BoxBorderWidth = 0.1
        self.BarCi = 95  # error bar default, None hides error bars
        # self.Bar_palette = self.MainWindow.pg_2_graph_barplot_pallete_style_combobox.currentText()
        # self.BarEdgeColor = self.MainWindow.pg_2_graph_colors_pallete_1_bar_plot.palette().button().color().name()
        self.BarSaturation = (
            self.MainWindow.pg2_graph_saturation_spinBox_box_plot.value()
        )
        self.BarOrient = (
            self.MainWindow.pg2_graph_orientaitno_combobox_barplot.currentText()
        )
        # self.BareColor = self.MainWindow.pg_2_graph_colors_pallete_3_bar_plot.palette().button().color().name()
        self.BareWidth = self.MainWindow.pg2_graph_bar_errwidth_spinBox_box_plot.value()
        self.BarOpacity = self.MainWindow.pg2_graph_bar_ci_spinBox_box_plot.value()
        self.BareCapSize = self.MainWindow.pg2_graph_flier_size_spinBox_box_plot.value()
        self.BarWidth = self.MainWindow.pg2_graph_bar_width_spinBox_box_plot.value()
        self.CheckedErrorBars = True


class ViolinPlot:
    def __init__(self, MainWindow=None):
        self.MainWindow = MainWindow
        self.type = "Violin Plot"
        self.name = None

        # self.dataset =
        self.vert = True
        self.Widths = 0.5  # space between plots
        self.ShowMeans = False  # show where the mean value is
        self.ShowExtrema = False
        self.ShowMedians = False
        self.BwMethod = None
        self.Violin_palette = "Custom"
        self.Violin_Color = []
        self.Violin_Width = 50
        self.Violin_Orientation = "v"
        self.Violin_Saturation = 100
        self.Violin_Condition = "All"
        self.Violin_eWidth = 10
        self.Violin_ErrorColor = []
        self.Violin_Cut = 0.0
        self.Violin_Scale = "area"

        self.sdPallete = sns.color_palette("coolwarm", 50)
        self.ViolinOrient = (
            self.MainWindow.pg2_graph_violinplot_orienation_combobox.currentText()
        )

        if self.MainWindow.pg2_graph_scale_comboBox_violinplot.currentText() == "area":
            self.ViolinScale = "area"
        elif (
            self.MainWindow.pg2_graph_scale_comboBox_violinplot.currentText() == "count"
        ):
            self.ViolinScale = "count"
        elif (
            self.MainWindow.pg2_graph_scale_comboBox_violinplot.currentText() == "width"
        ):
            self.ViolinScale = "width"
        self.ViolinInner = (
            self.MainWindow.pg2_graph_violinplot_InnerVal_combobox.currentText()
        )
        self.ViolinWidth = (
            self.MainWindow.pg2_graph_just_width_spinbox_violinplot.value()
        )
        # self.ViolinOrient = self.MainWindow.pg2_graph_violinplot_orienation_combobox.currentText()
        # self.ViolinScale = self.MainWindow.pg2_graph_scale_comboBox_violinplot.currentText()
        self.ViolinBorderWidth = (
            self.MainWindow.pg2_graph_border_width_spinBox_violinplot.value()
        )
        self.ViolinSaturation = (
            self.MainWindow.pg2_graph_saturation_spinBox_violinplot.value()
        )
        self.ViolinCut = self.MainWindow.pg2_graph_cut_spinBox_vil.value()


class BoxPlot:
    def __init__(self, MainWindow=None):
        self.MainWindow = MainWindow
        self.type = "Box Plot"
        self.x = None
        self.name = None
        self.Notch = False
        self.Vert = True
        self.Bootstrap = None
        self.UserMedians = None
        self.ConfIntervals = None
        self.Positions = None
        self.PatchArtist = False
        self.ManageTicks = True
        self.MeanLine = False
        self.ShowCaps = True
        self.ShowBox = True
        self.ShowMeans = False
        self.CapProps = None  # the styleLicence = "free" # or premium of the caps
        self.BoxProps = None  # styleLicence = "free" # or premium o the box
        self.WhiskerProps = None
        self.FlierProps = None
        self.MedianProps = None
        self.MeanProps = None
        self.Box_palette = "Custom"
        self.Box_Color = []

        self.sdPallete = sns.color_palette("coolwarm", 50)
        # used by plot seabord , initialize form GUI
        self.BoxWidth = self.MainWindow.pg2_graph_width_spinBox_box_plot.value()
        # self.BoxBorderColor = self.MainWindow.pg_2_graph_colors_pallete_1_box_plot.palette().button().color().name()
        self.BoxSaturation = (
            self.MainWindow.pg2_graph_saturation_spinBox_box_plot.value()
        )
        self.BoxOrient = (
            self.MainWindow.pg_2_graph_boxplot_orientation_combobox.currentText()
        )
        self.BoxBorderWidth = (
            self.MainWindow.pg2_graph_line_width_spinBox_box_plot.value()
        )
        self.BoxFlierSize = self.MainWindow.pg2_graph_cap_size_spinBox_box_plot.value()
        # self.Box_palette =  [self.MainWindow.pg_2_graph_colors_pallete_2_box_plot.palette().button().color().name()]
        # self.BoxIndex = self.MainWindow.pg2_graph_index_combobox_boxplot.currentText()
        self.CheckedErrorBars = True
        # self.BaxWidth = self.MainWindow.pg2_graph_bar_width_spinBox_box_plot.value()


class DotPlot:
    def __init__(self, MainWindow=None):
        self.MainWindow = MainWindow
        self.type = "Dot Plot"
        self.name = None

        self.x = None
        self.y = None
        self.Color = None
        self.MarkerStyle = None
        """
        markers = {'.': 'point', ',': 'pixel', 'o': 'circle', 
        'v': 'triangle_down', '^': 'triangle_up', '<': 'triangle_left',
        '>': 'triangle_right', '1': 'tri_down', '2': 'tri_up',
        '3': 'tri_left', '4': 'tri_right', '8': 'octagon', 's': 'square',
        'p': 'pentagon', '*': 'star', 'h': 'hexagon1', 'H': 'hexagon2'
        '+': 'plus', 'x': 'x', 'D': 'diamond', 'd': 'thin_diamond',
        '|': 'vline', '_': 'hline', 'P': 'plus_filled', 'X': 'x_filled',
        0: 'tickleft', 1: 'tickright', 2: 'tickup', 3: 'tickdown',
        4: 'caretleft', 5: 'caretright', 6: 'caretup', 7: 'caretdown',
        8: 'caretleftbase', 9: 'caretrightbase', 10: 'caretupbase',
        11: 'caretdownbase', 'None': 'nothing', None: 'nothing',
        ' ': 'nothing', '': 'nothing'}
        """
        self.Alpha = 1
        self.LineWidths = None  # none defaults to line.llinewidth
        self.EdgeColors = None


class SwarmPlot:
    def __init__(self, MainWindow=None):
        self.MainWindow = MainWindow
        self.type = "Swarm Plot"
        self.x = None
        self.y = None
        self.Color = None
        self.name = None

        self.MarkerStyle = None
        self.SwarmDodge = None
        self.Swarm_palette = "Custom"
        self.Swarm_Color = []
        self.Swarm_EdgeColor = []
        self.SwarmWidth = (
            self.MainWindow.pg2_graph_border_width_spinBox_swarmplot.value()
        )
        self.Swarm_Condition = "All"
        self.SwarmSize = self.MainWindow.pg2_graph_size_spinBox_swarmplot.value()
        self.SwarmOrient = "v"
        self.sdPallete = sns.color_palette("coolwarm", 50)

        """
            markers = {'.': 'point', ',': 'pixel', 'o': 'circle', 
            'v': 'triangle_down', '^': 'triangle_up', '<': 'triangle_left',
            '>': 'triangle_right', '1': 'tri_down', '2': 'tri_up',
            '3': 'tri_left', '4': 'tri_right', '8': 'octagon', 's': 'square',
            'p': 'pentagon', '*': 'star', 'h': 'hexagon1', 'H': 'hexagon2'
            '+': 'plus', 'x': 'x', 'D': 'diamond', 'd': 'thin_diamond',
            '|': 'vline', '_': 'hline', 'P': 'plus_filled', 'X': 'x_filled',
            0: 'tickleft', 1: 'tickright', 2: 'tickup', 3: 'tickdown',
            4: 'caretleft', 5: 'caretright', 6: 'caretup', 7: 'caretdown',
            8: 'caretleftbase', 9: 'caretrightbase', 10: 'caretupbase',
            11: 'caretdownbase', 'None': 'nothing', None: 'nothing',
            ' ': 'nothing', '': 'nothing'}
            """
        self.Alpha = 1
        self.LineWidths = None  # none defaults to line.llinewidth
        self.EdgeColors = None

        # pg2_graph_index_combobox_swarmplot


class plotStylesHandler:
    def __init__(self, MainWindow):
        self.currentStyle = {}  # a dictionary file
        self.styleName = ""
        self.MainWindow = MainWindow
        self.styleLicence = "free"  # or premium or user

        """ sample style:
            PlotSettings:
            {
                boxplot : {
                bar width: 3 ,
                dasdas: 2 ,
                etc
                    }
                barplot : {
                bar width: 3 ,
                dasdas: 2 ,
                etc
                    }
            }
        """
        self.sampleStyle = {
            "plot settings": {
                "BarPlot": {
                    "Bar_EdgeColor": None,
                    "Bar_palette": "Custom",
                    "Bar_eWidth": 1,
                    "Bar_Opacity": 100,
                    "Bar_Saturation": 100,
                    "Bar_Condition": "All",
                    "Bar_eColor": None,
                    "Bar_Orientation": "v",
                    "Bar_eCapSize": 0,
                }
            },
            "canvas settings": {
                "YLabel": "This is my Y label",
                "XLabel": "This is my X label",
                "Title": "This is my Title",
                "width": 5,
                "height": 5,
                "size_type": "inches",
                "resolution": 300,  # in dpi,
                "resolution_type": "dpi",
                "multiplot": False,
            },
        }

    def loadStyleDictionary(self, customPath=None):
        import json
        import os

        if customPath == None:
            fileLoadPath = self.LoadStyleExplorer()[0]
        else:
            fileLoadPath = customPath
        with open(fileLoadPath) as f:
            DictToRead = json.load(f)
        # print("dict is ", DictToRead)
        WidgetDictionary = self.getPlotInstanceFromStyleD(
            DictToRead
        )  # returns only the class plot items
        # print("read dict is ", WidgetDictionary)
        self.MainWindow.MyVisualPlotHandler.WidgetDictionary = WidgetDictionary
        self.MainWindow.ReadVariablesPlotTools()

        # clear out:
        self.MainWindow.pg_2_graph_colors_groupBox_listWidget.clear()
        self.MainWindow.pg2_graphs_view.clear()

        from celer_sight_ai.QtAssets.plot_handler import specificPlotWidget

        # print("Dictionary is ",WidgetDictionary)
        for key, value in WidgetDictionary.items():
            # print("adding name")
            self.MainWindow.pg2_graphs_view.addItem(value.name)
            color_list = value.palleteMainColor
            counter = 0
            # this needs to be fixed to support larger pallete
            plotItemsList = []
            for key2, value2 in self.MainWindow.DH.BLobj.groups[
                "default"
            ].conds.items():
                # print("color_list is ", color_list)
                C1 = color_list[str(counter)]
                tmpWIdget = specificPlotWidget(
                    self.MainWindow,
                    Condition=key2,
                    myMainColor=self.MainWindow.rgb2hex(C1[0], C1[1], C1[2]),
                    myEdgeColor="#000000",
                )
                listItemTmp = QtWidgets.QListWidgetItem()
                self.MainWindow.pg_2_graph_colors_groupBox_listWidget.addItem(
                    listItemTmp
                )
                plotItemsList.append(listItemTmp)

                listItemTmp.setSizeHint(QtCore.QSize(200, 40))
                self.MainWindow.pg_2_graph_colors_groupBox_listWidget.setItemWidget(
                    listItemTmp, tmpWIdget.MyWidget
                )
                counter += 1
            self.MainWindow.MyVisualPlotHandler.specificPlotWidgetRef[
                value.name
            ] = plotItemsList
        self.MainWindow.plot_seaborn()
        return

    # def saveStyleDictionary(self):
    #     import json
    #     fileLoadPath = self.LoadStyleExplorer()

    #     with open(fileLoadPath) as f:
    #         DictToRead = json.load(f)
    #     print("dict is ", DictToRead)
    #     DictionaryStyle = self.getPlotInstanceFromStyleD(DictToRead)
    #     WidgetDictionary = DictionaryStyle
    #     print(WidgetDictionary)

    def applyLoadedStyleD_ToUi(self):
        """
        Loads the settings and applies them to ui
        """
        pass

    def getPlotInstanceFromStyleD(self, DictToRead):
        """
        when reading a style form a json, convert the current json to a dictinoary instance
        """

        myPlotsSettings = DictToRead["plot settings"]
        myCanvasSettings = DictToRead["canvas settings"]
        # get plot settings
        finalDictionary = {}
        allPlotInstances = []
        for key, value in myPlotsSettings.items():
            parplotInstance = None
            # print("value issss ",value )
            # print("key isss ",key )
            if value["type"] == "Bar Plot":
                parplotInstance = BarPlot(self.MainWindow)
                parplotInstance.name = value["name"]
                parplotInstance.BoxBorderWidth = float(value["BoxBorderWidth"])
                # print("BarCiis ",value['BarCi'])
                if value["BarCi"] != None:
                    parplotInstance.BarCi = float(value["BarCi"])
                else:
                    parplotInstance.BarCi = value["BarCi"]
                parplotInstance.BarSaturation = float(value["BarSaturation"])
                parplotInstance.BarOrient = value["BarOrient"]
                parplotInstance.BareWidth = float(value["BareWidth"])
                parplotInstance.BarOpacity = float(value["BarOpacity"])
                parplotInstance.BareCapSize = float(value["BareCapSize"])
                parplotInstance.CheckedErrorBars = bool(value["CheckedErrorBars"])
                parplotInstance.palleteMainColor = value["palleteMainColor"]
                CurrentItem = parplotInstance.name
                # # make sure that the dictionary name is unique
                # finalDictionary[CurrentItem] = parplotInstance
                if CurrentItem == None:
                    CurrentItem = "Bar Plot"
                CurrentItem = self.MainWindow.MyVisualPlotHandler.CheckDictionaryName(
                    CurrentItem, finalDictionary
                )
                finalDictionary[CurrentItem] = parplotInstance
            if key == "Violin Plot":
                ViolinPlotInstance = ViolinPlot(self.MainWindow)
                ViolinPlotInstance.name = value["name"]
                ViolinPlotInstance.ViolinBorderWidth = float(value["ViolinBorderWidth"])
                ViolinPlotInstance.ViolinWidth = float(value["ViolinWidth"])
                ViolinPlotInstance.ViolinSaturation = float(value["ViolinSaturation"])
                ViolinPlotInstance.ViolinCut = float(value["ViolinCut"])
                ViolinPlotInstance.ViolinScale = value["ViolinScale"]
                ViolinPlotInstance.ViolinOrient = value["ViolinOrient"]
                ViolinPlotInstance.palleteMainColor = value["palleteMainColor"]
                ViolinPlotInstance.ViolinInner = value["ViolinInner"]

                CurrentItem = ViolinPlotInstance.name
                if CurrentItem == None:
                    CurrentItem = "Violin Plot"
                CurrentItem = self.MainWindow.MyVisualPlotHandler.CheckDictionaryName(
                    CurrentItem, finalDictionary
                )
                finalDictionary[CurrentItem] = ViolinPlotInstance

            if value["type"] == "Box Plot":
                parplotInstance = BoxPlot(self.MainWindow)
                parplotInstance.name = value["name"]
                parplotInstance.BoxWidth = float(value["BoxWidth"])
                parplotInstance.BoxSaturation = float(value["BoxSaturation"])
                parplotInstance.BoxOrient = value["BoxOrient"]
                parplotInstance.BoxBorderWidth = float(value["BoxBorderWidth"])
                parplotInstance.BoxFlierSize = float(value["BoxFlierSize"])
                # print("Error Bars is ",value['CheckedErrorBars'])
                parplotInstance.CheckedErrorBars = bool(value["CheckedErrorBars"])
                CurrentItem = parplotInstance.name
                parplotInstance.palleteMainColor = value["palleteMainColor"]
                finalDictionary[CurrentItem] = parplotInstance

            if key == "Dot Plot":
                pass
            if key == "Swarm Plot":
                parplotInstance = SwarmPlot(self.MainWindow)
                parplotInstance.name = value["name"]
                parplotInstance.SwarmWidth = float(value["SwarmWidth"])
                parplotInstance.SwarmSize = float(value["SwarmSize"])
                parplotInstance.SwarmOrient = value["SwarmOrient"]
                CurrentItem = parplotInstance.name
                parplotInstance.palleteMainColor = value["palleteMainColor"]
                finalDictionary[CurrentItem] = parplotInstance

        return finalDictionary

    def ListToDict(self, mylist):
        outDict = {}
        for i in range(len(mylist)):
            outDict[str(i)] = mylist[i]
        return outDict

    def saveStyleDictionary(self):
        import copy

        locationToSave = self.SaveStyleExplorer()
        WidgetDictionary = self.MainWindow.MyVisualPlotHandler.WidgetDictionary
        FINALdictCanvasSettings = {}
        # get plot settings
        allPlotInstances = []
        for key, value in WidgetDictionary.items():
            dictPlotSettings = {}
            if value.type == "Bar Plot":
                dictPlotSettings["name"] = str(key)
                dictPlotSettings["type"] = "Bar Plot"
                dictPlotSettings["BoxBorderWidth"] = str(
                    WidgetDictionary[key].BoxBorderWidth
                )
                dictPlotSettings["BarCi"] = str(WidgetDictionary[key].BarCi)
                dictPlotSettings["BarSaturation"] = str(
                    WidgetDictionary[key].BarSaturation
                )
                dictPlotSettings["BarOrient"] = str(WidgetDictionary[key].BarOrient)
                dictPlotSettings["BareWidth"] = str(WidgetDictionary[key].BareWidth)
                dictPlotSettings["BarOpacity"] = str(WidgetDictionary[key].BarOpacity)
                dictPlotSettings["BareCapSize"] = str(WidgetDictionary[key].BareCapSize)
                dictPlotSettings["CheckedErrorBars"] = str(
                    WidgetDictionary[key].CheckedErrorBars
                )
                dictPlotSettings["palleteMainColor"] = self.ListToDict(
                    self.MainWindow.MyVisualPlotHandler.getCompletePalleteMainColors(
                        key
                    )
                )
            if value.type == "Box Plot":
                dictPlotSettings["type"] = "Box Plot"

                dictPlotSettings["name"] = str(key)
                dictPlotSettings["BoxWidth"] = str(WidgetDictionary[key].BoxWidth)
                dictPlotSettings["BoxSaturation"] = str(
                    WidgetDictionary[key].BoxSaturation
                )
                dictPlotSettings["BoxOrient"] = str(WidgetDictionary[key].BoxOrient)
                dictPlotSettings["BoxBorderWidth"] = str(
                    WidgetDictionary[key].BoxBorderWidth
                )
                dictPlotSettings["BoxFlierSize"] = str(
                    WidgetDictionary[key].BoxFlierSize
                )
                dictPlotSettings["CheckedErrorBars"] = str(
                    WidgetDictionary[key].CheckedErrorBars
                )
                dictPlotSettings["palleteMainColor"] = self.ListToDict(
                    self.MainWindow.MyVisualPlotHandler.getCompletePalleteMainColors(
                        key
                    )
                )

            if value.type == "Swarm Plot":
                dictPlotSettings["type"] = "Swarm Plot"
                dictPlotSettings["name"] = str(key)
                dictPlotSettings["SwarmWidth"] = str(WidgetDictionary[key].SwarmWidth)
                dictPlotSettings["SwarmSize"] = str(WidgetDictionary[key].SwarmSize)
                dictPlotSettings["SwarmOrient"] = str(WidgetDictionary[key].SwarmOrient)
                dictPlotSettings["palleteMainColor"] = self.ListToDict(
                    self.MainWindow.MyVisualPlotHandler.getCompletePalleteMainColors(
                        key
                    )
                )
            if value.type == "Violin Plot":
                dictPlotSettings["type"] = "Violin Plot"
                dictPlotSettings["name"] = str(key)
                dictPlotSettings["ViolinBorderWidth"] = str(
                    WidgetDictionary[key].ViolinBorderWidth
                )
                dictPlotSettings["ViolinWidth"] = str(WidgetDictionary[key].ViolinWidth)
                dictPlotSettings["ViolinSaturation"] = str(
                    WidgetDictionary[key].ViolinSaturation
                )
                dictPlotSettings["ViolinCut"] = str(WidgetDictionary[key].ViolinCut)
                dictPlotSettings["ViolinScale"] = str(WidgetDictionary[key].ViolinScale)
                dictPlotSettings["ViolinOrient"] = str(
                    WidgetDictionary[key].ViolinOrient
                )
                dictPlotSettings["ViolinInner"] = str(WidgetDictionary[key].ViolinInner)
                dictPlotSettings["palleteMainColor"] = self.ListToDict(
                    self.MainWindow.MyVisualPlotHandler.getCompletePalleteMainColors(
                        key
                    )
                )

            FINALdictCanvasSettings[key] = copy.deepcopy(dictPlotSettings)

        outDictCanvas = {}
        outDictCanvas["YLabel"] = "test y"
        outDictCanvas["XLabel"] = "test x"
        outDictCanvas["Title"] = "test title"
        outDictCanvas["width"] = str(5)
        outDictCanvas["height"] = str(5)
        outDictCanvas["size_type"] = "inch"
        outDictCanvas["resolution"] = str(300)
        outDictCanvas["resolution_type"] = "dpi"
        outDictCanvas["multiplot"] = "False"

        DictToSave = {
            "plot settings": FINALdictCanvasSettings,
            "canvas settings": outDictCanvas,
        }
        import json

        # print(DictToSave)
        # print(type(DictToSave))
        # print(locationToSave)
        with open(locationToSave[0], "w", encoding="utf-8") as f:
            json.dump(DictToSave, f, ensure_ascii=False, indent=4)

    def SaveStyleExplorer(self):
        locationToSave = QtWidgets.QFileDialog.getSaveFileName(
            self.MainWindow, "Load styles file"
        )
        return locationToSave

    def LoadStyleExplorer(self):
        return QtWidgets.QFileDialog.getOpenFileName(
            self.MainWindow, "Open styles file"
        )


class specificPlotWidget(specificPlotWidgetUi):
    def __init__(self, MainWindow, Condition, myMainColor, myEdgeColor):
        self.MainWindow = MainWindow
        self.Condition = Condition
        self.visibility = True
        self.myMainColor = myMainColor
        self.myEdgeColor = myEdgeColor

        self.MyWidget = QtWidgets.QWidget()
        self.setupUi(self.MyWidget)

        # setup steps

        self.setCondition(self.Condition)
        self.setMainColor(self.myMainColor)
        self.setEdgeColor(self.myEdgeColor)

        # set up events

        self.PrimaryColor.clicked.connect(
            lambda: self.setMainColorButton(self.PrimaryColor)
        )
        self.EdgeColor.clicked.connect(lambda: self.setMainColorButton(self.EdgeColor))

    def setMainColorButton(self, mybutton):
        """
        open color dialog and assign color to my button
        """
        ColorWidget = QtWidgets.QColorDialog.getColor()
        myColor = ColorWidget.name()
        mybutton.setStyleSheet("background-color:" + myColor + ";")

    def setCondition(self, conditionName):
        """
        sets the widget to the proper condition name
        """
        self.ConditionLabel.setText(self.Condition)

    def setMainColor(self, Color):
        """
        sets the button color that represents the main color of the button/ plot
        """
        self.PrimaryColor.setStyleSheet("background-color:" + Color + ";")

    def setEdgeColor(self, Color):
        """
        sets the button color that represents the main color of the button/ plot
        """
        self.EdgeColor.setStyleSheet("background-color:" + Color + ";")


from celer_sight_ai.QtAssets.UiFiles.plotsColorPalleteSetup import (
    Ui_Dialog as plotsColorPalleteSetupUi,
)


class palleteColorPickerDialog(plotsColorPalleteSetupUi):
    def __init__(self, MainWindow):
        # self.MainWindow = MainWindow
        self.myWidget = QtWidgets.QDialog()
        self.setupUi(self.myWidget)
        self.getAvailableColors()
        self.MainWindow = MainWindow
        self.acceptCancelDialog.accepted.connect(lambda: self.onAccepted())
        btn = self.acceptCancelDialog.button(QtWidgets.QDialogButtonBox.Apply)
        btn.clicked.connect(lambda: self.onApply())

    def getAvailableColors(self, palleteType="All"):
        import os

        fileFolder = "data/palleteColors/"
        from os import listdir
        from os.path import isfile, join

        completeList = []
        if palleteType == "All":
            onlyfiles = [f for f in listdir(fileFolder)]
            for myFile in onlyfiles:
                FileNoExt = os.path.splitext(myFile)[0]
                completeList.append(FileNoExt)
        allPallets = {}
        # for myFile in completeList:
        #     allPallets[myFile] = image = cv2.imread(os.path.join(fileFolder ,myFile + '.png'))
        # add entities to list widget
        for item in completeList:
            widgetToAdd = simplePalleteWidgetSpecificCls(item)
            listItemTmp = QtWidgets.QListWidgetItem()
            self.listWidget.addItem(listItemTmp)
            listItemTmp.setSizeHint(QtCore.QSize(200, 40))
            self.listWidget.setItemWidget(listItemTmp, widgetToAdd.myWidget)

    def onApply(self):
        """
        same as onAccepted but doesnt not close dialog and updates the viewport
        """
        return

    def onAccepted(self):
        """
        here we apply this pallete to the current list widget items (which are reflecting the conditions)
        """
        import seaborn as sns

        itemAtPallete = self.listWidget.itemWidget(self.listWidget.currentItem())
        # print(itemAtPallete)
        currentPalleteStyle = itemAtPallete.findChild(QtWidgets.QLabel, "Name")
        # currentPalleteStyle = itemAtPallete.Name # get the pallete name

        num_shades = self.MainWindow.pg_2_graph_colors_groupBox_listWidget.count()
        color_list = sns.color_palette(currentPalleteStyle, num_shades)
        color_list = color_list
        WSitems = self.MainWindow.MyVisualPlotHandler.specificPlotWidgetRef
        for key, value in WSitems.items():
            currentPos = 0
            for widget1 in WSitems[key]:
                CurrentWidget = (
                    self.MainWindow.pg_2_graph_colors_groupBox_listWidget.itemWidget(
                        widget1
                    )
                )
                primaryColorBtn = CurrentWidget.findChild(
                    QtWidgets.QPushButton, "PrimaryColor"
                )

                primaryColorBtn.setStyleSheet(
                    "background-color:"
                    + rgb2hex(
                        color_list[currentPos][0],
                        color_list[currentPos][1],
                        color_list[currentPos][2],
                    )
                    + ";"
                )
                currentPos += 1
        # print(color_list)
        # myListWidget = self.MainWindow.pg_2_graph_colors_groupBox_listWidget()
        # for i in range(listWidget.count()):
        #     myItem = listWidget.item(i)
        #     myItem.setStyleSheet("background-color: rgb("+str(color_list[i][0]) +"," + str(color_list[i][1] +"," +  str(color_list[i][2] )+ ");"))

        # os.path.join


from celer_sight_ai.QtAssets.UiFiles.simplePalleteWidgetSpecific import (
    Ui_Form as simplePalleteWidgetSpecificUi,
)


class simplePalleteWidgetSpecificCls(simplePalleteWidgetSpecificUi):
    def __init__(self, Name):
        self.Name = Name
        self.myWidget = QtWidgets.QWidget()
        self.setupUi(self.myWidget)
        self.applyColorPalleteToButton(Name)

    def applyColorPalleteToButton(self, Name):
        self.icon = QtGui.QIcon()
        self.icon.addPixmap(
            QtGui.QPixmap("data/palleteColors/" + Name + ".png"),
            QtGui.QIcon.Mode.Normal,
            QtGui.QIcon.State.Off,
        )
        # self.PushButtonPalleteColors.setObjectName(Name)
        self.PushButtonPalleteColors.setIcon(self.icon)
        self.PushButtonPalleteColors.setIconSize(QtCore.QSize(300, 50))
        self.PushButtonPalleteColors.setAttribute(
            QtCore.Qt.WidgetAttribute.WA_TransparentForMouseEvents
        )
        self.palleteLabel.setText(Name)


def rgb2hex(r, g, b):
    import matplotlib

    return matplotlib.colors.to_hex((r, g, b))


from celer_sight_ai.QtAssets.UiFiles.plotStylesDatabaseInspector import (
    Ui_Dialog as autoLoaderPlotDialog,
)


class autoPlotLoader(autoLoaderPlotDialog):
    def __init__(self, parent=None):
        super(autoPlotLoader, self).__init__(parent)
        self.selectedPlot = None

    def loadSettingForPlot(self):
        pass


class plotStylesButton(QtWidgets.QPushButton):
    def __init__(self, myImgNormal=None, MainWindow=None):
        super(plotStylesButton, self).__init__()
        self.MainWindow = MainWindow
        self.zoomMultiplier = 1.2
        self.basePathImg = None
        self.maxHeightStart = 90
        self.maxWidthStart = 45
        self.setParent(self.MainWindow.pg_2_plot_parameteres_scrollAreaWidgetContents)

        self.maxHeightZoom = self.maxHeightStart * self.zoomMultiplier
        self.maxWidthZoom = self.maxWidthStart * self.zoomMultiplier

        self.iconNormalWidth = 86
        self.iconNormalHeight = 86
        self.iconZoomWidth = self.iconNormalWidth * self.zoomMultiplier
        self.iconZoomHeight = self.iconNormalHeight * self.zoomMultiplier

        self.setDimsToNormal()

        import os

        self.clicked.connect(
            lambda: self.MainWindow.myPlotStylesHandler.loadStyleDictionary(
                customPath=os.path.join(
                    "data/palletePresets/plotCombinations", self.basePathImg + ".json"
                )
            )
        )
        self.setObjectName(myImgNormal)
        # print('Obhject name is ',myImgNormal)
        self.myImgNormal = myImgNormal
        self.myImgHover = None
        self.myImgCheck = None
        self.myImgHoverIcon = QtGui.QIcon()
        self.myImgCheckIcon = QtGui.QIcon()
        self.getRestOfImages()
        self.ShadowEffect = QtWidgets.QGraphicsDropShadowEffect()
        self.ShadowEffect.setColor(QtGui.QColor(0, 0, 0, 200))
        self.ShadowEffect.setBlurRadius(30)
        self.ShadowEffect.setOffset(5, 10)
        self.setGraphicsEffect(self.ShadowEffect)
        self.setCheckable(True)
        self.setChecked(False)
        self.setStyleSheet(
            """
            QPushButton{
                background-color: rgba(0,0,0,0);
                border-width: 0px;  
                border-color: rgba(0,0,0,0);  
                border-style: solid;

            }
        
                                    """
        )

        self.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))

    def setDimsToNormal(self):
        self.setMinimumHeight(self.maxHeightStart)
        self.setMinimumWidth(self.maxWidthStart)
        self.setMaximumHeight(self.maxHeightStart)
        self.setMaximumWidth(self.maxWidthStart)

    def setDimsToZoom(self):
        self.setMinimumHeight(self.maxHeightZoom)
        self.setMinimumWidth(self.maxWidthZoom)
        self.setMaximumHeight(self.maxHeightZoom)
        self.setMaximumWidth(self.maxWidthZoom)

    def setIconToNormalSize(self):
        self.setIconSize(QtCore.QSize(self.iconNormalWidth, self.iconNormalHeight))

    def setIconToZoomSize(self):
        self.setIconSize(QtCore.QSize(self.iconZoomWidth, self.iconZoomHeight))

    def enterEvent(self, event):
        if self.isChecked() == False:
            self.setIcon(self.myImgHoverIcon)
            self.setIconToZoomSize()
            self.setDimsToZoom()
        super(plotStylesButton, self).enterEvent(event)

    def leaveEvent(self, event):
        if self.isChecked() == False:
            self.setIcon(self.myIconNormal)
            self.setIconToNormalSize()
            self.setDimsToNormal()
        super(plotStylesButton, self).leaveEvent(event)

    def mousePressEvent(self, event):
        self.setIcon(self.myImgCheckIcon)
        self.setIconToNormalSize()
        self.setDimsToNormal()
        super(plotStylesButton, self).mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        if self.isChecked() == False:
            self.setIcon(self.myIconNormal)
            self.setIconToNormalSize()
            self.setDimsToNormal()
        super(plotStylesButton, self).mouseReleaseEvent(event)

    def getRestOfImages(self):
        import os

        self.basePathImg = self.myImgNormal.replace("_NORMAL.png", "")
        self.myIconNormal = QtGui.QIcon()
        self.myIconNormal.addPixmap(QtGui.QPixmap(self.myImgNormal))
        self.setIcon(self.myIconNormal)
        self.setIconToNormalSize()
        filename, file_extension = os.path.splitext(self.myImgNormal)

        self.myImgHover = self.myImgNormal.replace("_NORMAL", "_hover")
        self.myImgCheck = self.myImgNormal.replace("_NORMAL", "_check")
        self.myImgHoverIcon.addPixmap(QtGui.QPixmap(self.myImgHover))
        self.myImgCheckIcon.addPixmap(QtGui.QPixmap(self.myImgCheck))


from celer_sight_ai.QtAssets.UiFiles.AnnotationLinksUI import (
    Ui_Form as AnnotationLinksUIForm,
)


class AnnotationDialog(AnnotationLinksUIForm):
    def __init__(self, Dataframe, MainWindow):
        super(AnnotationDialog, self).__init__()
        self.myDialog = QtWidgets.QDialog()
        self.setupUi(self.myDialog)
        self.currentDf = Dataframe
        self.setupListWidgets()
        self.MainWindow = MainWindow
        self.down_button_list.clicked.connect(lambda: self.linkSelectedItems())
        self.down_button_list_2.clicked.connect(lambda: self.removeSelectedItems())
        self.MainWindow.MyStatistics.significansPairs = []

    def setupListWidgets(self):
        # iterating the columns
        # print(self.currentDf)
        allConditions = self.currentDf["condition"].unique()
        for col in allConditions:
            self.listWidget.addItem(col)
            self.listWidget_2.addItem(col)

    def linkSelectedItems(self):
        listLeft = self.listWidget.selectedItems()
        listRight = self.listWidget_2.selectedItems()
        for itemLeft in listLeft:
            for itemRight in listRight:
                self.MainWindow.MyStatistics.significansPairs.append(
                    (itemLeft.text(), itemRight.text())
                )
                self.listWidget_3.addItem(itemLeft.text() + " vs " + itemRight.text())

    def removeSelectedItems(self):
        ListOfItemsToRemove = self.listWidget_3.selectedItems()
        for item in ListOfItemsToRemove:
            self.listWidget_3.removeItemWidget(item)


# from celer_sight_ai.QtAssets.UiFiles.VisualPlotPresetWidget import Ui_Form as VisualPlotPresetWidget_UI
# class plotStyleViewButton(VisualPlotPresetWidget_UI):
#     def __init__(self, MainWindow=None, myStyleImg = None ):
#         super(plotStyleViewButton, self).__init__()
#         self.myWidget = plotStylesButton(myStyleImg)
#         self.MainWindow = MainWindow
#         self.setupUi(self.myWidget)
#         self.myWidget.setParent(self.MainWindow.pg_2_plot_parameteres_scrollAreaWidgetContents)
#         self.myStyleImg = myStyleImg

#         self.myWidget.show()


if __name__ == "__main__":
    pass
