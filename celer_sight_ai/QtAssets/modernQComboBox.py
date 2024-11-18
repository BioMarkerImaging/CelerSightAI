import sys
from PyQt6 import QtCore, QtWidgets, QtGui
from PyQt6.QtWidgets import (
    QApplication,
    QComboBox,
    QVBoxLayout,
    QWidget,
    QCompleter,
    QStyledItemDelegate,
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QStandardItemModel, QStandardItem
from celer_sight_ai.config import MagicToolModes
from typing import Optional, Any
from celer_sight_ai import config


class ModernSearchableQComboBox(QComboBox):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setEditable(True)
        # self.setInsertPolicy(QComboBox.InsertPolicy.NoInsert)
        self.setFocusPolicy(Qt.FocusPolicy.ClickFocus)
        self.completer().setCompletionMode(QCompleter.CompletionMode.PopupCompletion)
        self.completer().setFilterMode(Qt.MatchFlag.MatchContains)
        self.completer().setMaxVisibleItems(10)
        self.setCompleter(self.completer())
        self.setMinimumWidth(200)
        self.setStyleSheet(
            """
            QComboBox {
                background-color: #2f2f2f;
                color: #ffffff;
                border: 1px solid #5A5A5A;
                border-radius: 5px;
                padding: 5px;
            }
            QComboBox::drop-down {
                border: none;
                background-color: #3F3F3F;
            }
            QComboBox::drop-down {
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 15px;
                height: 30px;
                border-width: 0px;
                border-left-width: 1px;
                border-left-color: darkgray;
                border-left-style: solid; /* just a single line */
                border-top-right-radius: 0px; /* same radius as the QComboBox */
                border-bottom-right-radius: 0px;
            }
            QComboBox::down-arrow {
                image: url(/path/to/down-arrow-icon.png);
                width: 14px;
                height: 14px;
            }
            QComboBox QAbstractItemView {
                background-color: #2f2f2f;
                border: 1px solid #5A5A5A;
                border-radius: 5px;
                color: #ffffff;
            }
            QComboBox QAbstractItemView::item {
                height: 25px;
            }
            QComboBox QAbstractItemView::item:selected {
                background-color: #3F3F3F;
            }
        """
        )
        self.setFocusPolicy(Qt.FocusPolicy.NoFocus)


class CustomItemDelegate(QStyledItemDelegate):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.setFocusPolicy(Qt.FocusPolicy.NoFocus)

    def sizeHint(self, option, index):
        originalSize = super().sizeHint(option, index)
        return QtCore.QSize(originalSize.width(), 25)  # Set the height to 25 pixels

    def paint(self, painter, option, index):
        # Get style options
        style = QApplication.style()
        opt = QtWidgets.QStyleOptionViewItem(option)

        # Draw background
        style.drawPrimitive(
            QtWidgets.QStyle.PrimitiveElement.PE_PanelItemViewItem,
            opt,
            painter,
            QtWidgets.QWidget(),
        )

        content_height = 25  # Or calculate based on the content
        padding = 0
        if index.data(Qt.ItemDataRole.DecorationRole):
            padding = 5
        new_rect = QtCore.QRect(
            option.rect.x() + padding,
            option.rect.y(),
            option.rect.width() - padding,
            content_height,
        )
        option.rect = new_rect
        # Draw the icon on the right side
        icon = index.data(Qt.ItemDataRole.DecorationRole)
        if icon:
            icon_size = icon.actualSize(option.rect.size())
            icon_rect = QtCore.QRect(
                option.rect.right() - icon_size.width(),
                option.rect.y(),
                icon_size.width(),
                option.rect.height(),
            )
            icon.paint(painter, icon_rect, QtCore.Qt.AlignmentFlag.AlignVCenter)

            # Adjust the option's rect to exclude the area where the icon is drawn
            option.rect.setRight(option.rect.right() - icon_size.width())
            # Draw the text on the left side
            text = index.data(QtCore.Qt.ItemDataRole.DisplayRole)
            text_rect = QtCore.QRect(
                option.rect.x(),
                option.rect.y(),
                option.rect.width() - icon_size.width(),
                option.rect.height(),
            )
            painter.drawText(text_rect, QtCore.Qt.AlignmentFlag.AlignVCenter, text)

        # super().paint(painter, option, index)
        # painter.restore()


class CustomComboBoxWithIconsDelegate(QStyledItemDelegate):
    def sizeHint(self, option, index):
        originalSize = super().sizeHint(option, index)
        self.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        return QtCore.QSize(originalSize.width(), 25)  # Set the height to 25 pixels

    def paint(self, painter, option, index):
        # Get the icon and text for the current index
        icon = index.data(Qt.ItemDataRole.DecorationRole)
        text = index.data(Qt.ItemDataRole.DisplayRole)
        content_height = 25  # Or calculate based on the content
        # padding = 0
        # if index.data(Qt.ItemDataRole.DecorationRole):
        #     padding = 5
        new_rect = QtCore.QRect(
            option.rect.x(),
            option.rect.y(),
            option.rect.width(),
            content_height,
        )
        option.rect = new_rect
        # Set the painter properties
        painter.save()
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)

        # Draw the background
        self.parent().style().drawPrimitive(
            QtWidgets.QStyle.PrimitiveElement.PE_PanelItemViewItem,
            option,
            painter,
            self.parent(),
        )

        # Draw text
        textRect = QtCore.QRect(
            option.rect.left() + 5,
            option.rect.top(),
            option.rect.width() - 30,
            option.rect.height(),
        )
        painter.drawText(
            textRect, Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft, text
        )

        # Draw icon on the right
        if icon:
            iconSize = self.parent().iconSize()
            iconRect = QtCore.QRect(
                option.rect.right() - iconSize.width() - 5,
                option.rect.top(),
                iconSize.width(),
                option.rect.height(),
            )
            pixmap = icon.pixmap(iconSize)
            painter.drawPixmap(iconRect, pixmap)

        painter.restore()


class IconTextComboBox(QComboBox):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setItemDelegate(CustomComboBoxWithIconsDelegate(self))
        self.setIconSize(QtCore.QSize(20, 20))
        self.view().parentWidget().setStyleSheet(
            """
                                                 background-color: #2e2e2e;
                                                 border-radius: 3px;"""
        )


class ModernQComboBox(QComboBox):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setEditable(False)
        # self.setInsertPolicy(QComboBox.InsertPolicy.NoInsert)
        self.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.setMinimumWidth(200)
        self.setStyleSheet(
            """
            QComboBox {
                background-color: #2f2f2f;
                color: #ffffff;
                border: 1px solid #5A5A5A;
                border-radius: 5px;
                padding: 5px;
            }
            QComboBox::drop-down{
                border: none;
                background-color: #3F3F3F;
            }
            QComboBox::down-arrow{
                image: url(/path/to/down-arrow-icon.png);
                width: 14px;
                height: 14px;
            }
            QAbstractItemView{
                background-color: rgb(75,75,75);
                border: 1px solid #5A5A5A;
                border-radius: 5px;
                color: #ffffff;
            }
            QAbstractItemView::item{
                height: 25px;
            }
            QAbstractItemView::item:selected{
                background-color: #3F3F3F;
            }
            QAbstractItemView::item:hover{
                background-color: rgb(255, 255, 255);
            }
        """
        )


class ModernQComboBoxAlternative(QWidget):
    currentTextChanged = QtCore.pyqtSignal(str)  # Custom signal

    def __init__(self, items=[], parent=None):
        super().__init__(parent)
        self.button = QtWidgets.QPushButton("", self)
        self.menu = QtWidgets.QMenu(self)  # Use QMenu for options
        self.button.setMenu(self.menu)  # Associate the menu with the button
        self.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        self.listWidget = QtWidgets.QListWidget(self)
        self.listWidget.hide()  # Initially hide the list
        self.items = items

        for item in items:
            self.listWidget.addItem(item)

        self.initUI()
        self.menu.aboutToShow.connect(
            self.adjustMenuWidth
        )  # Adjust menu width before showing

        self.setStyleSheet(
            """
        QPushButton{
            background-color: rgb(32, 32, 32);
            color: #ffffff;
            border: 0px solid #5A5A5A;
            border-radius: 5px;
                padding: 5px;

        }

        QPushButton::menu-indicator {

                subcontrol-position: right center;
                subcontrol-origin: padding;
                left: -10px;
            }
                                   QMenu{
            background-color: rgb(32, 32, 32);
            border: 1px solid #5A5A5A;
            border-radius: 5px;
            color: #ffffff;
        }
        QMenu::item{
            height: 25px;
        }
        QMenu::item:selected{
            background-color: #3F3F3F;
        }
                           

    """
        )

    def adjustMenuWidth(self):
        # Adjust only the width of the menu to match the button width
        # The height will automatically adjust to fit the content
        actionRect = (
            self.menu.actionGeometry(self.menu.actions()[0])
            if self.menu.actions()
            else QtCore.QRect()
        )
        width = self.button.width()
        height = actionRect.height() * len(self.menu.actions())
        self.menu.setFixedSize(QtCore.QSize(width, height + 6))

    def initUI(self):
        layout = QVBoxLayout(self)
        layout.addWidget(self.button)
        layout.addWidget(self.listWidget)
        self.setLayout(layout)

    def setCurrentIndex(self, index):
        self.setCurrentText(self.items[index])

    def setCurrentText(self, text):
        self.button.setText(text)

    def currentText(self):
        return self.button.text()

    def setItem(self, action):
        self.button.setText(action.text())
        self.currentTextChanged.emit(
            action.text()
        )  # Emit the signal with the current text

    def addItem(self, item):
        action = self.menu.addAction(item)
        action.triggered.connect(
            lambda: self.setItem(action)
        )  # Connect each action to setItem

    def clear(self):
        self.menu.clear()
        self.button.setText("")  # Reset button text

    def addItems(self, items):
        for item in items:
            self.addItem(item)
        if len(items) > 0:
            self.button.setText(items[0])


class CustomComboBoxWithIcons(QtWidgets.QPushButton):
    selectionChanged = QtCore.pyqtSignal(QWidget)

    def __init__(self, parent=None):
        super().__init__(parent)
        # set no margin in the layout
        self.setObjectName("model_selector_main")
        self.layout = QtWidgets.QHBoxLayout(self)
        self.layout.setContentsMargins(10, 0, 10, 0)
        self.layout.setSpacing(0)
        # self.layout.addStretch(1)
        self.main_label = QtWidgets.QLabel("Select Item", self)
        self.clicked.connect(lambda: self.toggleDropdown())

        config.global_signals.set_magic_tool_enabled_signal.connect(
            self.set_mode_enabled
        )
        config.global_signals.set_magic_tool_disabled_signal.connect(
            self.set_mode_disbaled
        )

        self.dropdown = QWidget(self, Qt.WindowType.Popup)
        self.dropdown.setObjectName("dropdown_model_type")
        self.dropdown.setStyleSheet(
            """
            background-color: transparent;
            """
        )
        self.current_mode = None  # MagicToolModes
        self.selected_index = 0
        self.selected_text = None
        self.icon_label = QtWidgets.QLabel("", self)
        self.layout.addWidget(
            self.icon_label,
            alignment=QtCore.Qt.AlignmentFlag.AlignLeft
            | QtCore.Qt.AlignmentFlag.AlignVCenter,
        )
        # alighn center and left
        self.layout.addWidget(
            self.main_label,
            alignment=QtCore.Qt.AlignmentFlag.AlignLeft
            | QtCore.Qt.AlignmentFlag.AlignVCenter,
        )
        self.layout.addStretch(1)
        self.height_fixed = 25  # 30
        self.width_fixed = 200
        button_effective_width = self.width_fixed - 40
        self.setMinimumWidth(self.width_fixed)
        self.setMaximumHeight(self.height_fixed)

        self.dropdownLayoutOuter = QVBoxLayout(self.dropdown)
        self.dropdownLayoutOuter.setContentsMargins(0, 0, 0, 0)
        # add the inner widget
        self.inner_widget = QWidget(self.dropdown)
        self.inner_widget.setObjectName("dropdown_model_type_inner")
        self.inner_widget.setStyleSheet(
            """

            background-color: #2f2f2f;
            border: 0px solid #5A5A5A;
            border-radius: 5px;

            """
        )
        self.dropdownLayoutOuter.addWidget(self.inner_widget)
        self.dropdownLayout = QVBoxLayout(self.inner_widget)
        self.dropdownLayout.setContentsMargins(3, 3, 3, 3)
        self.dropdownLayout.setSpacing(3)

        self.icon_label.setMinimumWidth(int(self.height_fixed))
        self.icon_label.setMinimumHeight(int(self.height_fixed))
        self.icon_label.setStyleSheet(
            """
            padding-right: 5 px;
            background-color:transparent;
            """
        )
        self.main_label.setStyleSheet(
            """
            font-size: 12px;
            font-weight: bold;
            background-color:transparent;
            """
        )
        self.items = []
        self.setStyleSheet(
            """
            QLabel{
                color: #ffffff;
            }

            QPushButton{
                background-color: #2f2f2f;
                color: #ffffff;
                border: 1px solid #5A5A5A;
                border-radius: 5px;
                padding: 5px;
            }

            """
        )

    def addItem(
        self,
        text: str,
        icon_path: Optional[str] = None,
        mode: Optional[Any] = None,
        label_icon_width=30,
    ) -> None:
        """
        Adds an item to the combo box, usually with an icon path to generate the pixmap,
        The mode is required and the available modes are in celer_sight_ai.config.MagicToolModes
        """
        assert mode in MagicToolModes, f"mode must be one of {MagicToolModes}"
        # Create a QWidget
        widget = QWidget()
        widget.setObjectName("ItemWidget")
        widget.setStyleSheet(
            """

            #ItemWidget{
                background-color: #2f2f2f;
                color: #ffffff;
                border: 0px solid #5A5A5A;
                padding:0px;
                }
            #ItemWidget:hover{
                background-color: #3F3F3F;
                }
            QLabel{
                font-size: 12px;
                font-weight: bold;
                color: #ffffff;
                border: 0px solid #5A5A5A;
                padding: 0px;
                padding-left: 3px;
                padding-right: 3px;
                background-color: transparent;
            }
            """
        )
        # Create a QHBoxLayout
        layout = QtWidgets.QHBoxLayout()
        layout.setContentsMargins(0, 0, 8, 0)
        layout.setSpacing(0)
        widget.setMinimumHeight(self.height_fixed)
        widget.setMaximumHeight(self.height_fixed)
        # Create a QLabel for the text
        text_label = QtWidgets.QLabel(text)
        text_label.setObjectName("text_label")
        # Create a QLabel for the icon
        icon_label = QtWidgets.QLabel(widget)
        icon_label.setObjectName("icon_label")

        icon_label_is_selected = QtWidgets.QLabel(widget)
        if icon_path:
            pxmap = QtGui.QPixmap(icon_path)
            # set antializing
            pxmap = pxmap.scaledToWidth(
                label_icon_width,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            icon_label.setPixmap(pxmap)  # Replace with the path to your icon
            icon_label.setAlignment(
                QtCore.Qt.AlignmentFlag.AlignHCenter
                | QtCore.Qt.AlignmentFlag.AlignVCenter
            )
        # get padding of icon
        pxmap_green = QtGui.QPixmap("data/icons/SpreadSheetValuesSame.png")
        pxmap_green = pxmap_green.scaledToWidth(
            self.height_fixed // 5,
            QtCore.Qt.TransformationMode.SmoothTransformation,
        )
        icon_label_is_selected.setPixmap(
            pxmap_green
        )  # Replace with the path to your icon
        icon_label_is_selected.setObjectName("icon_label_is_selected")
        # Add the QLabel for the text and the icon to the QHBoxLayout
        layout.addWidget(icon_label)
        # layout.addStretch(1)
        layout.addWidget(text_label)
        # add a spacer
        layout.addStretch(1)
        layout.addWidget(icon_label_is_selected)
        icon_label.setMinimumHeight(self.height_fixed)
        icon_label.setMinimumWidth(35)
        icon_label_is_selected.setMinimumHeight(self.height_fixed)
        # icon_label.setMaximumWidth(40)
        # icon_label.setMinimumWidth(40)
        # Set the QHBoxLayout as the layout for the QWidget
        widget.setLayout(layout)

        # Add the QWidget to the dropdown layout
        self.dropdownLayout.addWidget(widget)
        widget.item_mode = mode
        self.items.append(widget)
        if icon_path:
            widget.mouseReleaseEvent = self.makeSelectFunction(
                widget, text, mode, pxmap
            )
        else:
            widget.mouseReleaseEvent = self.makeSelectFunction(widget, mode, text)

    def text(self):
        # return the visible text on the widget, which is self.main_label.text()
        return self.main_label.text()

    def set_mode_enabled(self, tool_name):
        # Enables the magic tool that mathches the text provided
        for i, item in enumerate(self.items):
            if item.findChild(QtWidgets.QLabel, "text_label") == tool_name:
                self.items[i].setEnabled(True)

    def set_mode_disbaled(self, tool_name):
        # Disables the magic tool that matches the text provided
        for i, item in enumerate(self.items):
            if item.findChild(QtWidgets.QLabel, "text_label") == tool_name:
                self.items[i].setEnabled(False)

    def makeSelectFunction(self, widget, text, mode, pixmap=None):
        def selectItem(event) -> None:
            self.main_label.setText(text)
            if pixmap:
                self.icon_label.setPixmap(pixmap)
            self.dropdown.hide()
            self.selectionChanged.emit(widget)
            self.current_mode = mode

        return selectItem

    def get_mode(self):
        return self.current_mode

    def setIndexAsSelected(self, index):
        self.main_label.setText(self.items[index].children()[-1].text())
        self.dropdown.hide()
        self.selectionChanged.emit(self.items[index])
        self.selected_index = index
        self.selected_text = self.items[index].findChild(QtWidgets.QLabel, "text_label")
        self.icon_label.setPixmap(
            self.items[index].findChild(QtWidgets.QLabel, "icon_label").pixmap()
        )

        self.current_mode = self.items[index].item_mode

    def toggleDropdown(self):
        self.dropdown.setFixedSize(
            self.width(), len(self.items) * self.height_fixed + 10
        )  # Adjust size as needed
        self.dropdown.move(
            self.mapToGlobal(self.pos()).x() - 5,
            self.mapToGlobal(self.pos()).y() + self.height(),
        )
        self.dropdown.show()
        # iterate over all items, if the items is selected set icon_label_is_selected.setVisible(True) else False
        for item in self.items:
            text_label = item.findChild(QtWidgets.QLabel, "text_label")
            green_icon = item.findChild(QtWidgets.QLabel, "icon_label_is_selected")
            if text_label.text() == self.selected_text:
                green_icon.setVisible(True)
            else:
                green_icon.setVisible(False)


if __name__ == "__main__":
    ui = QtWidgets.QApplication(sys.argv)
    window = QtWidgets.QMainWindow()
    window.setWindowTitle("Modern QComboBox")
    window.resize(400, 300)
    widget = QtWidgets.QWidget()
    layout = QtWidgets.QVBoxLayout(widget)
    layout.setContentsMargins(0, 0, 0, 0)
    layout.setSpacing(0)
    # mc = ModernSearchableQComboBox()
    # mc.addItem("test1")
    # mc.addItem("test2")
    # mc.addItem("test3")
    # layout.addWidget(mc)
    cc = CustomComboBoxWithIcons()
    cc.addItem(
        "ROI with Suggestions",
        "data/icons/suggested_ROI_icon.png",
    )
    cc.addItem("Generic Magic ROI", "data/icons/magic_star_icon.png")
    cc.addItem("test3")
    layout.addWidget(cc)

    # layout.addWidget(ModernSearchableQComboBox())
    # layout.addWidget(IconTextComboBox())
    # layout.addWidget(CustomComboBoxWithIcons())
    #
    window.setCentralWidget(widget)
    window.show()
    sys.exit(ui.exec())
