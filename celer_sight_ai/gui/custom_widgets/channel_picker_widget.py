import logging

from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon

from celer_sight_ai import config

logger = logging.getLogger(__name__)


class ChannelListWidgetItem(QtWidgets.QWidget):
    """
    A clickable channel widget that toggles visibility. Completely self-contained;
    parent code can check the toggle via MainWindow.toggle_channel_visibility().
    """

    def __init__(
        self,
        parent=None,
        MainWindow=None,
        channel_name: str = "channel",
        channel_color: tuple[int, int, int] = (255, 255, 255),
        is_checked: bool = True,
    ):
        super().__init__(parent)
        self.MainWindow = MainWindow
        self.channel_name = channel_name
        self.channel_color = channel_color
        self._is_checked = is_checked

        # Create layout
        self.layout = QtWidgets.QHBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(8)

        # Create channel label with brightened text color
        self.brightened_color = tuple(
            min(255, int((c + 40) * 1.1)) for c in channel_color
        )
        self.darker_color = tuple(min(255, int(c * 0.5)) for c in channel_color)
        self.channel_label = QtWidgets.QLabel(channel_name)

        # Add widgets to layout
        self.layout.addWidget(self.channel_label)
        self.layout.addStretch()

        self.setLayout(self.layout)

        # Use the current style to reflect visibility
        self.update_style()

        # Enable clicking
        self.setCursor(Qt.CursorShape.PointingHandCursor)

        # set the width to exppand
        self.channel_label.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Fixed,
        )
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Fixed,
        )

    def isChecked(self):
        return self._is_checked

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self._is_checked = not self._is_checked
            self.update_style()
            config.update_visible_channel_cache(
                self.channel_name.lower(), self._is_checked
            )
            if self.MainWindow:
                config.global_signals.load_main_scene_signal.emit()

    def update_style(self):
        """
        Style changes when the channel is toggled off/on
        """
        if self._is_checked:
            self.channel_label.setStyleSheet(
                f"""
            QLabel {{
                color: rgb({self.brightened_color[0]}, {self.brightened_color[1]}, {self.brightened_color[2]});
                font-weight: bold;
                font-size: 12px;
                padding: 1px;
                }}
            """
            )
            self.setStyleSheet(
                f"""
                QWidget {{
                    background-color: rgba({self.channel_color[0]}, {self.channel_color[1]}, {self.channel_color[2]}, 40);
                    border: 2px solid rgb({self.darker_color[0]}, {self.darker_color[1]}, {self.darker_color[2]});
                    border-radius: 4px;
                }}
            """
            )
        else:
            self.channel_label.setStyleSheet(
                f"""
                QLabel {{
                    color: rgba({self.channel_color[0]}, {self.channel_color[1]}, {self.channel_color[2]}, 100);
                    font-weight: bold;
                    font-size: 12px;
                    padding: 1px;
                }}
            """
            )
            self.setStyleSheet(
                f"""
                QWidget {{
                    background-color: rgba({self.darker_color[0]}, {self.darker_color[1]}, {self.darker_color[2]}, 30);
                    border: 2px solid rgb({self.darker_color[0] // 2}, {self.darker_color[1] // 2}, {self.darker_color[2] // 2});
                    border-radius: 4px;
                }}
            """
            )

    def sizeHint(self) -> QtCore.QSize:
        """
        Calculate width based on the text and font, plus some padding for borders and layout.
        """
        # Compute text width
        metrics = QtGui.QFontMetrics(self.channel_label.font())
        text_width = metrics.horizontalAdvance(self.channel_label.text())
        # Add some overhead for the left/right margins, spacing, etc.
        # Adjust as needed for your desired padding.
        overhead = 6
        # Compute height. We'll keep a minimum of 30, but you could base it on font metrics if preferred.
        height = 30
        return QtCore.QSize(text_width + overhead, height)

    def minimumSizeHint(self) -> QtCore.QSize:
        return self.sizeHint()


class ChannelFlowWidget(QtWidgets.QWidget):
    """
    A custom flow container for ChannelListWidgetItem.
    Manually lays out items in rows, wrapping as needed based on each item's sizeHint.
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.channel_items = []
        self.margin = 4
        self.spacing = 4  # Space between items

    def add_channel_item(self, item: ChannelListWidgetItem):
        item.setParent(self)
        item.show()
        self.channel_items.append(item)
        self.update_layout()

    def clear_items(self):
        for item in self.channel_items:
            item.setParent(None)
            item.deleteLater()
        self.channel_items.clear()
        self.update()

    def resizeEvent(self, event: QtGui.QResizeEvent):
        super().resizeEvent(event)
        self.update_layout()

    def update_layout(self):
        """
        Calculate positions (x, y) of each item to create a natural flow layout:
        items flow left->right and wrap to next line when they won't fit.
        """
        width_available = self.width() - 2 * self.margin
        current_row_items = []
        current_row_width = 0
        rows = []
        y = self.margin

        # First pass: group items into rows
        for item in self.channel_items:
            item_width = item.sizeHint().width()

            # If adding this item would exceed available width, start new row
            if (
                current_row_items
                and current_row_width + item_width + self.spacing > width_available
            ):
                rows.append(current_row_items)
                current_row_items = []
                current_row_width = 0

            current_row_items.append(item)
            current_row_width += item_width + (self.spacing if current_row_items else 0)

        # Add the last row if it has items
        if current_row_items:
            rows.append(current_row_items)

        # Second pass: position items in each row
        for row in rows:
            total_min_width = sum(item.sizeHint().width() for item in row)
            spacing_width = (len(row) - 1) * self.spacing
            extra_width = width_available - total_min_width - spacing_width

            # Distribute extra width evenly among items in the row
            extra_per_item = extra_width / len(row)

            x = self.margin
            for item in row:
                item_width = item.sizeHint().width() + extra_per_item
                item.setGeometry(int(x), int(y), int(item_width), 30)
                x += item_width + self.spacing

            y += 30 + self.spacing

        # Update widget height to include bottom margin
        self.setMinimumHeight(int(y + self.margin))


class ChannelPickerWidget(QtWidgets.QWidget):
    """
    Main widget that uses a QScrollArea containing ChannelFlowWidget.
    Provides public methods to add/clear channels.
    """

    def __init__(self, parent=None, MainWindow=None):
        super().__init__(parent)
        self.MainWindow = MainWindow
        self.setupUi()

    def setupUi(self):
        self.main_layout = QtWidgets.QVBoxLayout()
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        self.scroll_area = QtWidgets.QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )
        self.scroll_area.setVerticalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAsNeeded
        )

        self.scroll_area.setStyleSheet(
            """
            QScrollArea {
                border: none;
                background-color: transparent;
            }
        """
        )

        # This is our manual flow container
        self.flow_widget = ChannelFlowWidget()
        self.scroll_area.setWidget(self.flow_widget)
        self.scroll_area.setMaximumHeight(80)
        self.main_layout.addWidget(self.scroll_area)
        self.setLayout(self.main_layout)

        self.setMinimumHeight(80)

    def add_channel(self, channel_name, channel_color, is_checked=True):
        item = ChannelListWidgetItem(
            parent=None,  # will be re-parented in add_channel_item
            MainWindow=self.MainWindow,
            channel_name=channel_name,
            channel_color=channel_color,
            is_checked=is_checked,
        )
        self.flow_widget.add_channel_item(item)

    def clear_channels(self):
        self.flow_widget.clear_items()
        self.channels = {}

    def resizeEvent(self, event: QtGui.QResizeEvent):
        super().resizeEvent(event)
        # We re-layout the flow widget when ChannelPickerWidget changes
        self.flow_widget.update_layout()

    def spawn_channels(self, channels: dict[str, tuple[int, int, int]]):
        logger.info(f"Spawning {len(channels)} channels")
        # clear all old channels
        self.clear_channels()
        # if not channels:
        #     # create rgb for now, and refresh once retrieved from the image
        #     channels = {
        #         "red": (255, 0, 0),
        #         "green": (0, 255, 0),
        #         "blue": (0, 0, 255),
        #     }
        self.channels = channels
        # add new channels
        for channel_name, channel_color in channels.items():
            is_checked = config.get_visible_channel_cache(channel_name.lower(), True)
            self.add_channel(channel_name, channel_color, is_checked=is_checked)

    def get_checked_channels(self):
        return [i.channel_name for i in self.flow_widget.channel_items if i.isChecked()]


if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    widget = ChannelPickerWidget()
    # Add sample microscopy channels with typical colors
    widget.add_channel("DAPI", (50, 50, 255))  # Blue for nuclei
    widget.add_channel("GFP - longer text", (50, 255, 50))  # Green fluorescent protein
    widget.add_channel("RFP", (255, 50, 50))  # Red fluorescent protein
    widget.add_channel("Cy5", (255, 50, 255))  # Far red/magenta
    widget.add_channel("YFP is quite a bit long", (255, 255, 50))
    widget.add_channel("CFP", (50, 255, 255))  # Cyan fluorescent protein
    widget.add_channel("Brightfield", (200, 200, 200))  # Gray for transmitted light

    widget.resize(420, 300)  # A bit wider to see reflow
    widget.show()
    app.exec()
