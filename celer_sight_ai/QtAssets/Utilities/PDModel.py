from PyQt6 import QtCore, QtGui, QtWidgets
import pandas as pd

listtest_A = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
listtest_B = [12, 32, 43, 54, 65, 76, 87, 78, 69, 150, 4, 2, 10]
df1 = pd.DataFrame(listtest_A)

df2 = pd.DataFrame(listtest_B)

cdf = pd.concat([df1, df2], ignore_index=True, axis=1)
cdf = cdf.fillna("")
cdf.columns = ["test", "test datra2"]
# cdf = pd.DataFrame([listtest_A,listtest_B], columns = ['data', 'also data'])
cdf2 = pd.concat([df1, df2, df1, df1], ignore_index=True, axis=1)


class CustomTableView(QtWidgets.QTableView):
    def __init__(self, MainWin=None):
        super(CustomTableView, self).__init__()
        from celer_sight_ai import config

        self.MainWindow = MainWin
        config.global_signals.CopySpreadSheetToClipboard.connect(
            self.copy_cells_to_clipboard
        )
        # self.installEventFilter(self)

    def setSpreadSheetUnchaged(self):
        # Set the icon to green showing that data is unchanged
        GreenIconStr = (
            "C:/Users/manos/Documents/topfluov2/data/icons/SpreadSheetValuesSame.png"
        )
        iconGreen = QtGui.QIcon()
        iconGreen.addPixmap(QtGui.QPixmap(GreenIconStr))
        self.MainWindow.SpreadSheetState.setIcon(iconGreen)

    def setSpreadSheetChanged(self):
        # Set the icon to green showing that data is unchanged
        GreenIconStr = (
            "C:/Users/manos/Documents/topfluov2/data/icons/SpreadSheetValuesChanged.png"
        )
        iconGreen = QtGui.QIcon()
        iconGreen.addPixmap(QtGui.QPixmap(GreenIconStr))
        self.MainWindow.SpreadSheetState.setIcon(iconGreen)

    def setSpreadSheetAdjusted(self):
        # Set the icon to green showing that data is unchanged
        GreenIconStr = "C:/Users/manos/Documents/topfluov2/data/icons/SpreadSheetValuesSelected.png"
        iconGreen = QtGui.QIcon()
        iconGreen.addPixmap(QtGui.QPixmap(GreenIconStr))
        self.MainWindow.SpreadSheetState.setIcon(iconGreen)

    def setModelCustom(self, Model):
        self.setSpreadSheetUnchaged()

        Dict = Model._dataframe.to_dict()  # converts panads to dictionary
        minCellsWidth = self.width() / 150
        minCellsHeight = self.height() / 60
        CollumnsToAdd = 0
        Dict2 = {}
        # convert from dict{dict, dict} to dict{list, list}
        for key, value in Dict.items():
            Dict2[key] = []
            for key1, value1 in value.items():
                Dict2[key].append(value1)
        # here we add extra rows
        # for key,values in Dict2.items():
        #     rowsToAdd =( minCellsHeight + minCellsHeight*0.66) - len(values)
        #     for i in range(len(values)+ int(rowsToAdd)):
        #         if i < len(values):
        #             if values[i] == None:
        #                 values[i] = ""
        #         else:
        #             values.append("")
        # # add extra collumns
        # # add empty keys, length - minCellsWidth+ minCellsWidth*0.66
        visible_df = pd.DataFrame(Dict2)
        empytString = " "
        print(int(minCellsWidth + minCellsWidth * 0.66))
        # for i in range(int(minCellsWidth+ minCellsWidth*0.66)):
        #     emptyList = []
        #     for x in range(int(minCellsHeight + minCellsHeight*0.66)):
        #         emptyList.append('')
        #     visible_df[empytString] = emptyList.copy()
        #     empytString += empytString
        self.model_pandas = pandasModel(visible_df, self)
        # model_pandas = pandasModel(gui_main.plot_dataframe)
        self.setModel(self.model_pandas)
        self.setEditTriggers(
            QtWidgets.QAbstractItemView.EditTrigger.SelectedClicked
            | QtWidgets.QAbstractItemView.EditTrigger.DoubleClicked
        )

        # self.removeEventFilter(self.tableView)
        # MINE

        # self.tableView.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)   #width: 100%
        # self.tableView.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)    #enlarge-shrink windo

    def eventFilter(self, source, event):
        if event.type() == QtCore.QEvent.Type.KeyPress and event.matches(
            QtGui.QKeySequence.StandardKey.Copy
        ):
            self.copy_cells_to_clipboard()
            return True
        return super(CustomTableView, self).eventFilter(source, event)

    def copy_cells_to_clipboard(self, MODE="dot"):
        """
        Mode can either be comma or dot
        """

        if len(self.selectionModel().selectedIndexes()) > 0:
            # sort select indexes into rows and columns
            previous = self.selectionModel().selectedIndexes()[0]
            allcolumns = {}
            columns = []
            rows = []
            colSet = set(self.selectionModel().selectedIndexes())
            colNum = len(set(self.selectionModel().selectedIndexes()))
            modelRowCount = self.model().rowCount()
            modeColumnCount = self.model().columnCount()
            clipboard = ""
            moveRight = "\t"
            nextRow = "\r\n"

            for i in range(modelRowCount):
                if i == 0:
                    for x in range(modeColumnCount):
                        clipboard += str(
                            self.model().headerData(x, QtCore.Qt.Orientation.Horizontal)
                        )
                        clipboard += moveRight
                    clipboard += nextRow
                for x in range(modeColumnCount):
                    mystringValue = str(self.model().index(i, x).data())
                    if MODE == "comma":
                        clipboard += str(
                            mystringValue.replace(",", "").replace(".", ",")
                        )
                    elif MODE == "dot":
                        clipboard += str(mystringValue.replace(",", "."))
                    clipboard += moveRight
                clipboard += nextRow
            sys_clip = QtWidgets.QApplication.clipboard()
            sys_clip.setText(str(clipboard))
        return


class pandasModel(QtCore.QAbstractTableModel):
    DtypeRole = QtCore.Qt.ItemDataRole.UserRole + 1000
    ValueRole = QtCore.Qt.ItemDataRole.UserRole + 1001

    def __init__(self, df=pd.DataFrame(), tableview=None, parent=None):
        super(pandasModel, self).__init__(parent)
        self._dataframe = df

        self.prevValueCell = None
        self.tableview = tableview
        self.tableview.setEditTriggers(
            QtWidgets.QAbstractItemView.EditTrigger.SelectedClicked
            | QtWidgets.QAbstractItemView.EditTrigger.DoubleClicked
        )
        # self.installEventFilter(self)

    def setDataFrame(self, dataframe):
        self.beginResetModel()
        self._dataframe = dataframe.copy()
        self.endResetModel()

    def dataFrame(self):
        return self._dataframe

    dataFrame = QtCore.pyqtProperty(pd.DataFrame, fget=dataFrame, fset=setDataFrame)

    def headerData(self, section, orientation, role=QtCore.Qt.ItemDataRole.DisplayRole):
        """Return header data for the given section, orientation and role"""
        if role != QtCore.Qt.ItemDataRole.DisplayRole:
            return None

        if orientation == QtCore.Qt.Orientation.Horizontal:
            return str(self._dataframe.columns[section])

        if orientation == QtCore.Qt.Orientation.Vertical:
            return str(self._dataframe.index[section])

        return None

    def rowCount(self, parent=QtCore.QModelIndex()):
        if parent.isValid():
            return 0
        return len(self._dataframe.index)

    def columnCount(self, parent=QtCore.QModelIndex()):
        if parent.isValid():
            return 0
        return self._dataframe.columns.size

    def data(self, index, role=QtCore.Qt.ItemDataRole.DisplayRole):
        # print('role is ',role)
        # print('at ',index.row(),index.column())
        # row = self._dataframe.index[index.row()]
        # col = self._dataframe.columns[index.column()]
        # dt = self._dataframe[col].dtype
        # val = self._dataframe.iloc[row][col]
        # print(row)
        # print(col)
        # print(dt)
        # print(val)
        if not index.isValid() or not (
            0 <= index.row() < self.rowCount()
            and 0 <= index.column() < self.columnCount()
        ):
            # print('at ',index.row(),index.column())
            # print('returning none')
            return None
        if role == QtCore.Qt.ItemDataRole.EditRole:  # when first eded
            row = self._dataframe.index[index.row()]
            col = self._dataframe.columns[index.column()]
            dt = self._dataframe[col].dtype
            val = self._dataframe.iloc[row][col]
            self.prevValueCell = self._dataframe.iloc[row][col]
            return self._dataframe.iloc[row][col]
        if role == QtCore.Qt.ItemDataRole.DisplayRole:
            row = self._dataframe.index[index.row()]
            col = self._dataframe.columns[index.column()]
            val = self._dataframe.iloc[row][col]
            return str(val)
        elif role == pandasModel.ValueRole:
            row = self._dataframe.index[index.row()]
            col = self._dataframe.columns[index.column()]
            val = self._dataframe.iloc[row][col]
            self.prevValueCell = None
            return val
        if role == pandasModel.DtypeRole:
            row = self._dataframe.index[index.row()]
            col = self._dataframe.columns[index.column()]
            dt = self._dataframe[col].dtype
            val = self._dataframe.iloc[row][col]
            return dt

        return None

    def is_almost_equal(self, x, y, epsilon=1 * 10 ** (-2)):
        """Return True if two values are close in numeric value
        By default close is withing 1*10^-8 of each other
        i.e. 0.00000001
        """
        return abs(x - y) >= epsilon

    def setData(self, index, value, role):
        if index.isValid():
            row = index.row()
            col = index.column()
            print(" value now is ")
            print("role is ", role)
            if role == QtCore.Qt.ItemDataRole.EditRole:
                print("prev vlaue is ", self.prevValueCell)
                print("value is ", value)
                try:
                    if self.is_almost_equal(self.prevValueCell, value):
                        self.tableview.setSpreadSheetChanged()
                except:
                    return False
                self._dataframe.iat[row, col] = value
                self.dataChanged.emit(
                    index, index, (QtCore.Qt.ItemDataRole.DisplayRole,)
                )
            return True
        return False

    def roleNames(self):
        roles = {
            QtCore.Qt.ItemDataRole.DisplayRole: b"display",
            pandasModel.DtypeRole: b"dtype",
            pandasModel.ValueRole: b"value",
        }
        return roles

    def eventFilter(self, source, event):
        if event.type() == QtCore.QEvent.Type.KeyPress and event.matches(
            QtGui.QKeySequence.StandardKey.Copy
        ):
            # self.copy_cells_to_clipboard()
            return super(pandasModel, self).eventFilter(source, event)

        return super(pandasModel, self).eventFilter(source, event)

    def flags(self, index):
        fl = super(self.__class__, self).flags(index)
        fl |= QtCore.Qt.ItemFlag.ItemIsEditable
        fl |= QtCore.Qt.ItemFlag.ItemIsSelectable
        fl |= QtCore.Qt.ItemFlag.ItemIsEnabled
        fl |= QtCore.Qt.ItemFlag.ItemIsDragEnabled
        fl |= QtCore.Qt.ItemFlag.ItemIsDropEnabled
        return fl

    def copySelection(self):
        import io
        import csv

        selection = self.tableview.selectionModel().selectedIndexes()
        if selection:
            rows = sorted(index.row() for index in selection)
            columns = sorted(index.column() for index in selection)
            rowcount = rows[-1] - rows[0] + 1
            colcount = columns[-1] - columns[0] + 1
            table = [[""] * colcount for _ in range(rowcount)]
            for index in selection:
                row = index.row() - rows[0]
                column = index.column() - columns[0]
                table[row][column] = index.data()
            stream = io.StringIO()
            thistest = csv.writer(stream, delimiter="\t").writerows(table)
            print(thistest)
        return
