import os
import sys
import typing
from PyQt6 import QtCore, QtGui, QtWidgets
from celer_sight_ai import config

from PyQt6.QtWidgets import (
    QWidget,
    QLabel,
    QListWidgetItem,
    QVBoxLayout,
    QListWidget,
    QApplication,
    QHBoxLayout,
)
from PyQt6 import QtWidgets, QtCore
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt
import uuid
import logging

logger = logging.getLogger(__name__)


# The `CustomClassListWidget` class is a custom implementation of a QListWidget that allows for
# adding, removing, and managing custom ROI classes.
class CustomClassListWidget(QtWidgets.QListWidget):
    def __init__(self, parent=None, MainWindow=None):
        super().__init__(parent)
        self.setStyleSheet(
            "QListWidget{\n"
            "border-radius:0px;\n"
            "border: 0px solid;\n"
            "}\n"
            "QListWidget::item{\n"
            "border-radius:3px;\n"
            "}"
        )
        self.MainWindow = MainWindow
        self.parent_widget = parent
        self.classes = {}

        self.setDragEnabled(True)
        self.setWordWrap(True)
        # The Custom list widget item is not always clicked when the list widget item is clicked
        # so we have to punch it
        self.itemClicked.connect(self.click_on_child)

        # Drag and drop attributes
        self.setDragEnabled(True)
        self.setAcceptDrops(True)
        self.setDropIndicatorShown(True)
        self.viewport().setAcceptDrops(True)
        # self.setDragDropMode(self.DragDropMode.InternalMove)
        self.setDragDropMode(QtWidgets.QAbstractItemView.DragDropMode.NoDragDrop)

        self.hoverItem = None
        self.hoverTimer = QtCore.QTimer(self)
        self.hoverTimer.timeout.connect(self.handle_hover)

    def get_parental_classes(self, class_uuid):
        # returns a list of all parents of a class
        parents = []
        current_parent = self.classes[class_uuid].parent_class_uuid
        while True:
            if not current_parent:
                break
            parents.append(current_parent)
            current_parent = self.classes[current_parent].parent_class_uuid
        return parents

    def get_class_groups(self):
        """
        All groups that are related to eachtoher in a list [ [parent, child], [parent, child] ]
        if a group has no parent, then the parent is None
        """
        groups = []
        for i in self.classes:
            # case no parent, appent it as one group
            if not self.classes[i].parent_class_uuid:
                groups.append([i])
            else:
                # else extend that parent group
                # find the index where the parent class exists in the group
                for g in groups:
                    if self.classes[i].parent_class_uuid in g:
                        g.append(i)

        return groups

    def reset_state(self):
        while self.count() > 0:
            self.takeItem(0)
        self.classes = {}
        self.hoverItem = None

    def get_all_clild_classes_items(self, current_class_uuid):
        # recursively search for all children
        children = []
        if not current_class_uuid:
            return children
        for i in self.classes:
            if self.classes[i].parent_class_uuid == current_class_uuid:
                children.append(self.classes[i])
                children.extend(self.get_all_clild_classes_items(i))
        return children

    def click_on_child(self, widget_clicked):
        # The Custom list widget item is not always clicked when the list widget item is clicked
        # so we have to punch it
        self.itemWidget(widget_clicked).on_selection()

    def click_on_widget_by_uuid(self, uuid: str):
        """Selects the widget by the widget item"""
        # find widget with uuid
        widget_item = self.classes[uuid]
        return self.click_on_widget(widget_item)

    def click_on_widget(self, item):
        """Selects the widget by the widget item"""

        for i in range(self.count()):
            if item == self.itemWidget(self.item(i)):
                self.setCurrentRow(i)

    def is_widget_selected(self, item):
        for i in range(self.count()):
            if item == self.itemWidget(self.item(i)):
                return self.item(i).isSelected()

    def get_item(self, widget_item):
        for i in range(self.count()):
            if widget_item == self.itemWidget(self.item(i)):
                return self.item(i)

    def get_row_from_uuid(self, class_uuid=None):
        if not class_uuid:
            return None
        for i in range(self.count()):
            if self.getItemWidget(i).unique_id == class_uuid:
                return i
        return None

    def get_class_widget_by_uuid(self, class_uuid):
        return self.classes[class_uuid]

    def get_class_name_by_uuid(self, class_uuid):
        r = self.classes[class_uuid].class_label
        if not r:
            return None
        else:
            return r.text()

    def get_class_uuid_by_class_name(self, class_name):
        r = self.get_class_widget_by_class_name(class_name)
        if r:
            return r
        else:
            return None

    def get_class_widget_by_class_uuid(self, class_uuid):
        return class_uuid if self.classes.get(class_uuid) else None

    def get_class_widget_by_class_name(self, class_name):
        # Finds the widget where the string on the text element
        # equals the querry string and returns the indexed widget.
        class_names = [i for i in self.classes if self.classes[i].text() == class_name]
        if len(class_names) == 0:
            return None
        else:
            return class_names[0]

    def get_parent_class_name_by_class_name(self, class_name):
        # Provided a class name ex "default" we find the parent widget
        # and return the parent class name ex. "default parent"
        c_widget = self.get_class_widget_by_class_name(class_name)
        p_widget = self.classes[c_widget.parent_class_uuid]
        return p_widget.class_label.text()

    def handle_doubtful_classe_name(self, supercategory, class_name):
        """
        Checks if the class exists already, if so return the uuid of that class.
        If the class does not exist, create one and return the uuid
        """
        class_uuid = self.get_class_uuid_by_class_name(class_name)
        if class_uuid:
            return class_uuid
        else:
            # handle as a new class
            # check if config is available, if so add by config
            cfg = self.get_config_by_class(
                supercategory=supercategory, class_name=class_name
            )
            if cfg:
                self.MainWindow.new_analysis_object.scan_class_items(cfg["classes"])
            class_uuid = self.get_class_uuid_by_class_name(class_name)
            return class_uuid

    def get_config_by_class(self, supercategory, class_name):
        """Checks to see if a combination of supercategory and category exist in the predefined configs
        if so, it returns the config as a dictionary"""
        from celer_sight_ai.gui.custom_widgets.grid_button_image_selector import (
            gather_cfgs,
            read_all_experiment_cfgs,
            gather_default_classes,
        )

        cfgs_paths = gather_default_classes()
        cfgs = [read_all_experiment_cfgs(c) for c in cfgs_paths]
        for cfg in cfgs:
            if cfg.get("supercategory") == supercategory:
                if class_name in cfg.get("text").lower():
                    return cfg
        return None

    def get_config_by_class_uuid(self, class_uuid):
        """Checks to see if a combination of supercategory and category exist in the predefined configs
        if so, it returns the config as a dictionary"""
        from celer_sight_ai.gui.custom_widgets.grid_button_image_selector import (
            gather_cfgs,
            read_all_experiment_cfgs,
            gather_default_classes,
        )

        cfgs_paths = gather_default_classes()
        cfgs = [read_all_experiment_cfgs(c) for c in cfgs_paths]
        for cfg in cfgs:
            if cfg.get("uuid") == class_uuid:
                return cfg
        return None

    def get_current_row_class_name(self):
        # Get the selected class widget name
        return self.MainWindow.custom_class_list_widget.itemWidget(
            self.MainWindow.custom_class_list_widget.currentItem()
        ).text()

    def get_current_row_class_id(self):
        # Get the selected class widget uuid
        return self.MainWindow.custom_class_list_widget.itemWidget(
            self.MainWindow.custom_class_list_widget.currentItem()
        ).unique_id

    def currentItemWidget(self):
        # Get the current QWidget of the current QListWidgetItem
        return self.itemWidget(self.currentItem())

    def getItemWidget(self, item_row):
        return self.itemWidget(self.item(item_row))

    def delete_all_classes(self):
        logger.info(f"Deleting all classes")
        while self.count() > 0:
            try:
                # get one key item from the dict self.classes
                c = list(self.classes.keys())[0]

                # case where no children
                if not self.classes[c].children_class_uuids:
                    self.removeClass(c)
                    continue
                # case there are children classes
                while self.classes[c].children_class_uuids:
                    # get the first element
                    cc = self.classes[c].children_class_uuids[0]
                    self.removeClass(self.classes[cc])
                self.removeClass(c)
            except Exception as e:
                self.clear()
                print()

    def ensure_class_list_widget_is_right_hierarchy(self):
        # first clear all items
        self.clear()
        # iterate through all class and make sure that the parent_class_name is assigned if the class exists
        for c in self.classes:
            if (
                self.classes[c].parent_class_name
                and not self.classes[c].parent_class_uuid
            ):
                # find the parent class uuid
                # parent_class_uuid = self.get_class_widget_by_class_name(
                #     self.classes[c].parent_class_name
                # )
                parent_class_name = self.classes[c].parent_class_name
                parent_class_uuid = self.get_class_uuid_by_class_name(parent_class_name)
                if not parent_class_uuid:
                    continue
                if parent_class_name and parent_class_uuid:
                    self.classes[c].parent_class_uuid = parent_class_uuid
                    # assign the children node for that parent
                    if not c in self.classes[parent_class_uuid].children_class_uuids:
                        self.classes[parent_class_uuid].children_class_uuids.append(c)
                else:
                    self.classes[c].parent_class_uuid = None

        # then take all top level items and start adding them in a depth first approach
        # get all classes without parents
        classes_without_parents = [
            i for i in self.classes if not self.classes[i].parent_class_uuid
        ]
        for cwp in classes_without_parents:
            self.addClass(
                class_name=self.classes[cwp].class_label.text(),
                parent_class_uuid=self.classes[cwp].parent_class_uuid,
                class_uuid=cwp,
                color=self.classes[cwp].color,
                is_user_defined=self.classes[cwp].is_user_defined,
                is_particle=self.classes[cwp].is_particle,
                parent_class_name=self.classes[cwp].parent_class_name,
                children_classes_uuids=self.classes[cwp].children_class_uuids,
            )
            # add all children in a depth first approach
            if (
                hasattr(self.classes[cwp], "children_class_uuids")
                and self.classes[cwp].children_class_uuids
            ):
                for cc in self.classes[cwp].children_class_uuids:
                    self.add_children_classes(cc)

    def addClass(
        self,
        class_name=None,
        parent_class_uuid=None,
        class_uuid=None,
        color=None,
        is_user_defined=False,
        is_particle=False,
        parent_class_name=None,
        children_classes_uuids=[],
    ):
        """
        Creates a class item in the dictionary self.class and as a QlistWidget entry
        """
        if not class_name:
            logger.debug("Could not create class.")
            return
        # if color is none, generate one
        if isinstance(color, type(None)):
            # pick a unique color not in use
            available_colors = [
                i
                for i in config.bright_colors
                if i not in [ii.color for ii in self.classes.values()]
            ]
            if not available_colors:
                import random

                color = [random.randint(0, 255) for i in range(3)]
            else:
                color = available_colors[0]
            print()
            # color = config.bright_colors[c]
        list_widget_item = CustomClassListWidgetItem(
            self,
            MainWindow=self.MainWindow,
            class_uuid=class_uuid,
            color=color,
            is_user_defined=is_user_defined,
            parent_class_name=parent_class_name,
            children_classes_uuids=children_classes_uuids,
        )
        indentation = 0
        if parent_class_uuid:
            indentation = self.getItemHierarky(parent_class_uuid) + 1

        self.classes[list_widget_item.unique_id] = list_widget_item
        list_widget_item.addClass(
            class_name=class_name,
            parent_class_uuid=parent_class_uuid,
            indentation=indentation,
            color=color,
            is_particle=is_particle,
        )

        item = QtWidgets.QListWidgetItem()
        # ignore clicks

        if parent_class_uuid:
            icon = QtGui.QIcon("data/icons/enter_icon.png")
        else:
            icon = None
        list_widget_item.setData(class_name, icon, class_color=color)

        item.setSizeHint(QtCore.QSize(50, 15))
        self.addItem(item)

        self.setItemWidget(item, list_widget_item)
        # set current class as selected
        self.setCurrentItem(item)
        return list_widget_item.unique_id

    def get_mask_color_from_class_uuid(self, class_uuid):
        # tet class name
        return self.MainWindow.get_mask_color_from_class(class_uuid)

    def get_item_uuid_with_parent(self, item_name, parent_class_uuid):
        for item in self.classes:
            if (
                self.classes[item].class_name == item_name
                and self.classes[item].parent_class_uuid == parent_class_uuid
            ):
                return item.unique_id

    def removeClass(self, class_uuid):
        # if class_uid if none, or it does not exists, return
        if not class_uuid or class_uuid not in self.classes:
            return
        logger.info(f"Removing class {self.classes[class_uuid].text()}")
        self.takeItem(self.row(self.get_item(self.classes[class_uuid])))
        # find if there are any children and remove them
        if not self.classes[class_uuid].children_class_uuids:
            del self.classes[class_uuid]
            return
        for cid in self.classes[class_uuid].children_class_uuids:
            self.removeClass(self.classes[cid])

        del self.classes[class_uuid]

    def getItemHierarky(self, item_uuid):
        # find the total number of parent classes for this item
        total_parents = 0
        current_parent = None
        while True:
            if not current_parent:
                current_parent = self.classes[item_uuid].parent_class_uuid
            else:
                current_parent = self.classes[current_parent].parent_class_uuid
            if not current_parent:
                break
            total_parents += 1
        return total_parents

    def selectionChanged(self, item, event):
        for key, val in self.classes.items():
            # if its selected set stylesheet on
            if self.is_widget_selected(val):
                val.set_colors_selected(True)
            else:
                val.set_colors_selected(False)

    #### Drag and drop ####
    def dragMoveEvent(self, event):
        super().dragMoveEvent(event)
        item = self.itemAt(event.position().toPoint())
        if item and item != self.hoverItem:
            self.hoverItem = item
            self.hoverTimer.start(1000)  # 1 second hover delay

    def dropEvent(self, event):
        self.hoverTimer.stop()
        self.add_child(self.hoverItem, self.currentItem())
        super().dropEvent(event)

    def handle_hover(self):
        self.hoverTimer.stop()
        if self.hoverItem:
            self.add_child(self.hoverItem, self.currentItem())

    def add_child(self, parent, child):
        if parent and child and parent != child:
            child.setText(f"— {child.text()}")
            parent_index = self.row(parent)
            child_index = self.row(child)
            if parent_index < child_index:
                self.insertItem(parent_index + 1, self.takeItem(child_index))
            else:
                self.insertItem(parent_index, self.takeItem(child_index))

    def add_children_classes(self, class_uuid: str = None) -> None:
        self.addClass(
            class_name=self.classes[class_uuid].class_label.text(),
            parent_class_uuid=self.classes[class_uuid].parent_class_uuid,
            class_uuid=class_uuid,
            color=self.classes[class_uuid].color,
            is_user_defined=self.classes[class_uuid].is_user_defined,
            is_particle=self.classes[class_uuid].is_particle,
            parent_class_name=self.classes[class_uuid].parent_class_name,
        )
        # recursively add children
        if self.classes[class_uuid].children_class_uuids:
            for c in self.classes[class_uuid].children_class_uuids:
                self.add_children_classes(c)

    # def update_and_restructure_classes(self):
    #     # start from the widgets without parents, add those to the
    #     # list widget, then add their childtren in a breath first approatch

    #     # remove all items on the list widget
    #     self.MainWindow.custom_class_list_widget.clear()

    #     # get all classes without parents
    #     classes_without_parents = [
    #         i for i in self.classes if not self.classes[i].parent_class_uuid
    #     ]
    #     # add those to the list widget
    #     # Add parents:
    #     for c in classes_without_parents:
    #         self.addClass(
    #             class_name=self.classes[c].class_label.text(),
    #             parent_class_uuid=self.classes[c].parent_class_uuid,
    #             class_uuid=c,
    #             color=self.classes[c].color,
    #             is_user_defined=self.classes[c].is_user_defined,
    #             is_particle=self.classes[c].is_particle,
    #             parent_class_name=self.classes[c].parent_class_name,
    #             children_classes_uuids=self.classes[c].children_class_uuids,
    #         )
    #         # add all children in a depth first approach
    #         if (
    #             hasattr(self.classes[c], "children_class_uuids")
    #             and self.classes[c].children_class_uuids
    #         ):
    #             for cc in self.classes[c].children_class_uuids:
    #                 self.add_children_classes(cc)
    def update_and_restructure_classes(self):
        self.MainWindow.custom_class_list_widget.clear()
        added_classes = set()
        added_class_names = set()

        def add_class_and_children(class_uuid, depth=0):
            if depth > 100 or class_uuid in added_classes:  # Prevent infinite loops
                return

            class_info = self.classes.get(class_uuid)
            if not class_info:
                logger.warning(f"Class with UUID {class_uuid} not found")
                return

            class_name = class_info.class_label.text()
            if class_uuid in added_classes or class_name in added_class_names:
                config.global_signals.notificationSignal(
                    f"Class {class_name} already added, skipping"
                )
                logger.warning(
                    f"Class '{class_name}' (UUID: {class_uuid}) already added, skipping"
                )
                return

            added_classes.add(class_uuid)
            added_class_names.add(class_name)

            self.addClass(
                class_name=class_name,
                parent_class_uuid=class_info.parent_class_uuid,
                class_uuid=class_uuid,
                color=class_info.color,
                is_user_defined=class_info.is_user_defined,
                is_particle=class_info.is_particle,
                parent_class_name=class_info.parent_class_name,
                children_classes_uuids=class_info.children_class_uuids,
            )

            for child_uuid in class_info.children_class_uuids:
                add_class_and_children(child_uuid, depth + 1)

        classes_without_parents = [
            i for i in self.classes if not self.classes[i].parent_class_uuid
        ]

        for c in classes_without_parents:
            add_class_and_children(c)


class CustomClassListWidgetItem(QWidget):
    """
    Class item, that is a QListWidget but also holds the properties of the class,
    these will inlcude particle properties
    """

    def __init__(
        self,
        parent=None,
        MainWindow=None,
        class_uuid=None,
        is_user_defined=False,
        color=None,
        parent_class_name=None,
        children_classes_uuids=[],
        REMOVE_EDGE_ANNOTATIONS=None,
        REMOVE_EDGE_ANNOTATION_PERCENT=None,
        REMOVE_HOLES=None,
        REMOVE_HOLES_PERCENT=None,
    ):
        super().__init__(parent)
        self.main_layout = QHBoxLayout(self)
        self.MainWindow = MainWindow
        # icon of "enter" that indicates the current class is a child class
        self.child_icon = QLabel(self)
        self.child_icon.setMaximumWidth(13)  # Set maximum width of the icon
        # icon of visibility (eye)
        self.visibility_button = QtWidgets.QPushButton(self)
        visibility_button_size = 11

        ##########################
        #### Class attributes ####
        ##########################
        self._is_class_visible = True  # directly tied to the eye icon
        # if its not visible --> disable everything exept the eye icon
        if not class_uuid:
            self.unique_id = str(config.get_unique_id())
        else:
            self.unique_id = class_uuid
        self.parent_class_uuid = None
        if isinstance(children_classes_uuids, type(None)):
            children_classes_uuids = []
        self.children_class_uuids = children_classes_uuids
        self.is_particle = False
        self.particle_settings = None
        self.color = None
        self.is_user_defined = is_user_defined
        self.REMOVE_EDGE_ANNOTATIONS = REMOVE_EDGE_ANNOTATIONS
        self.REMOVE_EDGE_ANNOTATION_PERCENT = REMOVE_EDGE_ANNOTATION_PERCENT
        self.REMOVE_HOLES = REMOVE_HOLES
        self.REMOVE_HOLES_PERCENT = REMOVE_HOLES_PERCENT
        self.parent_class_name = (
            parent_class_name  # the plan name in text of a parent class
        )
        # if the parent class does not exist, then when it is added in the future this class will become a child class
        self._annotation_opacity = 1

        self.visibility_button.setMaximumWidth(
            visibility_button_size
        )  # Set maximum width of the icon
        self.visibility_button.setMaximumHeight(
            visibility_button_size
        )  # Set maximum width of the icon
        self.visibility_button.setMinimumWidth(
            visibility_button_size
        )  # Set maximum width of the icon
        self.visibility_button.setMinimumHeight(
            visibility_button_size
        )  # Set maximum width of the icon

        self.indentation = 0  # created during runtime

        self.visibility_button.clicked.connect(lambda: self.on_visibility_icon_click())
        self.visibility_button.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)

        self.setObjectName("classes_listWidget_left_main")
        self.visibility_icon_on = QtGui.QIcon("data/icons/eye_show.png")
        # self.visibility_icon_on
        self.visibility_icon_on.setIsMask(True)
        self.visibility_icon_off = QtGui.QIcon("data/icons/eye_hide.png")
        # self.visibility_icon_off.setIconSize(QtCore.QSize(13, 13))
        self.visibility_icon_off.setIsMask(True)

        self.visibility_button.setIcon(self.visibility_icon_on)
        self.visibility_button.setIconSize(QtCore.QSize(9, 9))
        self.visibility_button.setStyleSheet(
            """
                QPushButton{
                    border: 0px solid rgb(255,255,255);
                    margin: 0px; padding: 0px;
                    border-radius: 4px;

                    color: rgb(255,255,255);
                }
                QPushButton:hover{
                    border: 0px solid rgb(255,255,255);
                    border-radius: 4px;
                    background-color: rgba(0,0,0,30);
                    color: rgb(255,255,255);

            
            
            """
        )
        is_editable = False
        if is_user_defined:
            is_editable = True
        self.class_label = EditableLabel(self, editable=is_editable)
        class_label_height = 15
        self.class_label.setMaximumHeight(class_label_height)
        self.class_label.setStyleSheet(
            """

                border: 1px solid rgb(255,255,255);

            """
        )
        class_color_button_size = 9
        self.class_color_button = QtWidgets.QPushButton(self)
        self.class_color_button.setMaximumHeight(class_color_button_size)
        self.class_color_button.setMaximumWidth(class_color_button_size)
        self.class_color_button.setMinimumHeight(class_color_button_size)
        self.class_color_button.setMinimumWidth(class_color_button_size)
        self.class_color_button.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)

        self.setMaximumHeight(13)

        self.left_margin = 4
        self.top_margin = 2
        self.right_margin = 4
        self.bottom_margin = 0

        self.main_layout.setContentsMargins(
            self.left_margin, self.top_margin, self.right_margin, self.bottom_margin
        )
        self.main_layout.addWidget(self.child_icon)
        self.main_layout.addWidget(self.visibility_button)
        self.main_layout.addWidget(self.class_label)
        self.main_layout.addWidget(self.class_color_button)
        self.main_layout.setSpacing(4)
        # self.layout.addWidget(self.textLabel2)
        self.setLayout(self.main_layout)

        if color:
            self.set_color(color)

    def get_children_classes_uuids(self):
        return self.children_class_uuids

    def get_class_config(self) -> dict:
        # returns a config to be used for inference
        if self.is_particle:
            return {}
        d = {}
        d["supercategory"] = (
            config.supercategory
        )  # current superclass TODO: needs to be variable depending on class
        d["class_name"] = self.class_label.text()
        # fill in attributes from the default experiment config attribute
        for k in config.default_experiment_config:
            if not hasattr(self, k) or not getattr(self, k):
                d[k] = config.default_experiment_config[k]
        return d

    def get_classes(self):
        return self.MainWindow.custom_class_list_widget.classes

    def set_color(self, color=None):
        # Sets the color of the class and updates the class button color
        # Color needs to be in rgb format
        if color:
            if len(color) == 3:
                # get the opacity
                color.append(self.MainWindow.pg1_settings_mask_opasity_slider.value())
            self.color = tuple(color)
            self.class_color_button.setStyleSheet(
                "background-color: rgb"
                + str(self.color[:3])
                + ";\n"
                + "border-radius: 2px;\n"
            )

    def set_opacity(self, opacity):
        if isinstance(self.color, type(None)):
            return None
        self._annotation_opacity = opacity
        self.color = list(self.color)
        self.color[-1] = opacity
        self.color = tuple(self.color)

    def is_class_visible(self):
        return self._is_class_visible

    def on_visibility_switch_set_enabled(self, mode=True):
        items = [
            self.class_label,
            self.child_icon,
        ]
        if mode == True:
            for ii in items:
                ii.setEnabled(True)
        else:
            for ii in items:
                ii.setEnabled(False)

    def on_visibility_icon_click(self):
        self._is_class_visible = not self._is_class_visible
        self.visibility_button.setChecked(self._is_class_visible)
        self.on_visibility_switch_set_enabled(self._is_class_visible)
        self.MainWindow.toggle_mask_class_visibility(
            self._is_class_visible, self.unique_id
        )
        if self._is_class_visible:
            self.visibility_button.setIcon(self.visibility_icon_on)
        else:
            self.visibility_button.setIcon(self.visibility_icon_off)
        # reload scene
        # self.MainWindow.toggle_class_visibility()

    def on_selection(self):
        if self._is_class_visible:
            # make sure class is selected:
            list_widget = self.parent().parent()  # listwidget (parent)
            list_widget.click_on_widget_by_uuid(self.unique_id)
            self.spawn_particle_analysis()

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton and self._is_class_visible:
            self.on_selection()
        super().mousePressEvent(event)

    def spawn_particle_analysis(self):

        # only spawn particle analysis if the class is a particle class
        if self.is_particle:
            # if image is ultra high res, do not spawn particle analysis
            if self.MainWindow.DH.BLobj.get_current_image_object()._is_ultra_high_res:
                config.global_signals.errorSignal.emit(
                    "This image is too large to analyze particles. Please use a lower resoluti image."
                )
                return
            # check if there is a an image in the current condition (or displayed)
            if (
                len(
                    self.MainWindow.DH.BLobj.groups[
                        self.MainWindow.DH.BLobj.get_current_group()
                    ].conds
                )
                == 0
            ):
                channels = []
            elif (
                len(
                    self.MainWindow.DH.BLobj.groups[
                        self.MainWindow.DH.BLobj.get_current_group()
                    ]
                    .conds[self.MainWindow.DH.BLobj.get_current_condition()]
                    .images
                )
                == 0
            ):
                channels = []
            else:
                # obtain the channels for these images
                channels = (
                    self.MainWindow.DH.BLobj.groups[
                        self.MainWindow.DH.BLobj.get_current_group()
                    ]
                    .conds[self.MainWindow.DH.BLobj.get_current_condition()]
                    .images[self.MainWindow.current_imagenumber]
                    .channel_list
                )
            self.MainWindow.viewer.particle_analysis_settings_widget.spawn(channels)

    def text(self):
        return self.class_label.text()

    def contextMenuEvent(self, event):
        """
        Conetext menu for class widgets
        """
        from functools import partial

        menu = QtWidgets.QMenu()
        event_pos = self.mapToGlobal(event.pos())
        self.add_sub_class = QtGui.QAction("add sub-class", None)
        # check if parent class already has a particle class, if so disable the action

        self.add_particle_class_action = QtGui.QAction(
            "add particles / binary roi", None
        )

        # self.single_class_inference_action = QtGui.QAction("get roi (AI)", None)
        # dont allow more than one particle per class yet, will be allowed
        # with colocalization.
        # For the time being, we dont allow more than one child class
        if (
            self.is_particle
            or any(
                [self.get_classes()[i].is_particle for i in self.children_class_uuids]
            )
            or len(self.children_class_uuids) > 0
        ):
            self.add_particle_class_action.setEnabled(False)
        self.get_roi_action = QtGui.QAction("get roi (AI)", None)
        self.get_roi_action.setEnabled(True)
        self.get_roi_action.triggered.connect(
            partial(
                self.MainWindow.MyInferenceHandler.DoInferenceAllImagesOnlineThreaded,
                provided_classes=[self.unique_id],
            )
        )
        self.delete_action = QtGui.QAction("delete", None)
        self.delete_action.triggered.connect(lambda: self.delete_class())
        # self.inference_class.triggered.connect()
        #     self.do_inference_all_images_online_threaded_func
        # )
        if not self.is_user_defined:
            self.delete_action.setEnabled(False)
        menu.addAction(self.delete_action)
        menu.addAction(self.get_roi_action)
        menu.addAction(self.add_particle_class_action)
        menu.exec(event_pos)

    def add_particle_class(self):
        import random

        logger.info("Adding particle class for class: " + self.class_label.text())
        # add a particle class
        self.MainWindow.addClassItem(
            "particles",
            parent_uuid=self.unique_id,
            # generate a unique color
            # color=random.choice(config.bright_colors),
            is_user_defined=True,
            is_particle=True,
        )

    def delete_class(self):
        self.MainWindow.remove_class_item(class_uuid=self.unique_id)

    def set_colors_selected(self, mode=True):
        if mode == True:
            self.class_label.setStyleSheet(
                """
                QLabel{
                color: rgb(20,20,20)    
               }
            """
            )
        else:
            self.class_label.setStyleSheet("")

    def setData(self, text1, child_icon=None, class_color=None):
        if class_color:
            # convert QColor to hex
            class_color = str(class_color[:3])

            self.class_color_button.setStyleSheet(
                """
                QPushButton{
                    border: 0px solid rgb(255,255,255);
                    border-radius: 2px;
                    """
                + f"background-color: rgb{class_color};"
                + """
                }
                QPushButton:hover{
                    border: 1px solid rgb(255,255,255);
                    border-radius: 2px;


            """
            )
        if child_icon:
            self.child_icon.show()
            self.child_icon.setPixmap(child_icon.pixmap(13, 13))  # Keep icon size 13x13
        else:
            self.child_icon.hide()
        self.class_label.setText(text1)

    def addClass(
        self,
        class_name=None,
        parent_class_uuid=None,
        indentation=0,
        color=None,
        is_particle=False,
    ):
        # `class_name` is a parameter that is passed to the `addClass` method of the
        # `CustomClassListWidget` class. It is used to set the text of the
        # `CustomClassListWidgetItem` widget, which represents a class in the list. The
        # `class_name` is displayed as the text of the `class_label` QLabel in the
        # `CustomClassListWidgetItem` widget.

        # get class color
        self.indentation = indentation
        self.setData(class_name, class_color=color)
        if is_particle:
            self.is_particle = True
        if not parent_class_uuid:
            self.child_icon.hide()
        else:  # find the class and add the icon bellow
            indentation_pix = indentation * 3
            self.main_layout.setContentsMargins(
                self.left_margin + indentation_pix,
                self.top_margin,
                self.right_margin,
                self.bottom_margin,
            )

        self.parent_class_uuid = parent_class_uuid
        if parent_class_uuid:
            if (
                self.unique_id
                not in self.get_classes()[parent_class_uuid].children_class_uuids
            ):
                self.get_classes()[parent_class_uuid].children_class_uuids.append(
                    self.unique_id
                )


class TreatmentListWidgetItem(QtWidgets.QListWidgetItem):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.setFlags(self.flags() | QtCore.Qt.ItemFlag.ItemIsEditable)


class RNAiListWidget(QtWidgets.QListWidget):
    def __init__(self, parent=None, MainWindow=None):
        super().__init__(parent)
        self.MainWindow = MainWindow
        self.itemBeingEdited = None
        self.previous_item = None
        self.current_item = None
        self.itemDoubleClicked.connect(self.handleItemDoubleClicked)
        self.setObjectName("RNAi_list")
        self.setStyleSheet(
            """
            border-radius:10px;
            border:0px solid ;
            border-color:rgba(200,200,200,255);
            background-color: rgba(0,0,0,0);
            font-family:"Lato";
            font-weight: bold;
            font-size: 14px;
            QWidget::item:hover{
            border-radius:5px;
            }
            QListWidget::item{
            border-radius:3px;
            margin: 10px;
            background-color: rgba(255,255,255,70);
            }
            QListWidget{
            border-radius:0px;
            border: 0px solid;
            }
            QListWidget::item{
            border-radius:3px;
            }
            """
        )
        self.setWordWrap(False)
        self.setDragDropMode(QtWidgets.QAbstractItemView.DragDropMode.NoDragDrop)
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.DoubleClicked)
        self.installEventFilter(self)
        # self.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger)

    def contextMenuEvent(self, event):
        """
        Conetext menu for treatments
        """
        menu = QtWidgets.QMenu()
        event_pos = self.mapToGlobal(event.pos())
        self.rename_action = QtGui.QAction("rename", None)
        # get the item that was clicked
        item = self.itemAt(event.pos())
        # emit an itemClicked signal for this item
        self.rename_action.triggered.connect(lambda _, b=item: self.rename_treatment(b))
        menu.addAction(self.rename_action)
        menu.exec(event_pos)
        QtWidgets.QApplication.processEvents()
        self.itemClicked.emit(item)

    def rename_treatment(self, item):
        self.handleItemDoubleClicked(item)

    def on_item_double_clicked(self, item):
        # Find the index of the clicked item, and open an editor for it.
        self.prev_index = self.indexFromItem(item)
        self.edit(self.prev_index)

    def addItem(self, item: str) -> None:
        # override method
        treatment_item = TreatmentListWidgetItem(item)
        super().addItem(treatment_item)

    # def edit(self, index):
    #     # item = self.item(index.row())
    #     # The line `item = self.findItems(index, QtCore.Qt.MatchFlag.MatchExactly)[0]` is finding the
    #     # item in the list widget that matches the given index.
    #     # item = self.findItems(index, QtCore.Qt.MatchFlag.MatchExactly)[0]
    #     super().edit(index)
    #     self.edit_item = self.item(index.row())
    #     # self.itemBeingEdited = self.item(index.row())

    def closeEditor(self, editor, hint):
        from celer_sight_ai import config

        # make sure focus is shifted back to the viewer
        self.MainWindow.viewer.setFocus()
        super().closeEditor(editor, hint)
        if self.itemBeingEdited:
            print(f'Finished editing "{self.itemBeingEdited.text()}".')
            self.itemBeingEdited = None
            if not self.previous_item != self.item(self.prev_index).text():
                # case where the item is not changed
                self.item(self.prev_index).setText(self.previous_item)
                self.closePersistentEditor(item=self.item(self.prev_index))
                return
            if self.item(self.prev_index).text() == "":
                # case where the item is empty
                self.item(self.prev_index).setText(self.previous_item)
                self.closePersistentEditor(item=self.item(self.prev_index))
                return
            all_conditions = self.MainWindow.DH.BLobj.groups[
                self.MainWindow.DH.BLobj.get_current_group()
            ].conds.keys()
            if self.item(self.prev_index).text() in all_conditions:
                # case where the item is a valid condition
                self.item(self.prev_index).setText(self.previous_item)
                # make sure that this treatment is the current displayed treatment
                # self.MainWindow.switch_treatment_onchange(condition=self.item(self.prev_index).text())
                self.closePersistentEditor(item=self.item(self.prev_index))
                return
            config.global_signals.RNAi_list_widget_update_signal.emit(
                [self.previous_item, self.item(self.prev_index).text()]
            )
            self.closePersistentEditor(item=self.item(self.prev_index))
            QtWidgets.QApplication.processEvents()
            item = self.item(self.prev_index)
            item.setFlags(item.flags() | QtCore.Qt.ItemFlag.ItemIsEditable)

    def handleItemDoubleClicked(self, item):
        self.openPersistentEditor(item)
        self.itemBeingEdited = item
        self.prev_index = self.indexFromItem(item).row()
        self.previous_item = item.text()
        item.setFlags(item.flags() | QtCore.Qt.ItemFlag.ItemIsEditable)

    def eventFilter(
        self, object: QtCore.QObject | None, event: QtCore.QEvent | None
    ) -> bool:
        # if event is right click, open context menu and dont select item
        # or if its track pad press

        if event.type() == QtCore.QEvent.Type.MouseButtonPress:
            if event.button() == QtCore.Qt.MouseButton.RightButton:
                self.contextMenuEvent(event)
                return True
        return super().eventFilter(object, event)

    def closePersistentEditor(self, item):
        super().closePersistentEditor(item)
        if self.itemBeingEdited == item:
            self.itemBeingEdited = None
            config.global_signals.RNAi_list_widget_update_signal.emit(
                [self.previous_item, self.current_item]
            )
        print(f'Item "{item.text()}" is not being edited.')


class EditableLabel(QLabel):
    """
    Custom editable label used in the class widgets, only editable on user defined classes
    """

    def __init__(self, *args, **kwargs):
        self.is_editable = kwargs.get("editable")
        del kwargs["editable"]
        super().__init__(*args, **kwargs)
        self.edit = QtWidgets.QLineEdit(self)
        self.edit.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.edit.editingFinished.connect(self.finish_editing)
        self.edit.hide()

    def mouseDoubleClickEvent(self, event):
        if self.is_editable:
            self.edit.setGeometry(self.rect())
            self.edit.setText(self.text())
            self.edit.show()
            self.edit.setFocus()

    def finish_editing(self):
        if self.is_editable:
            self.setText(self.edit.text())
            self.edit.hide()


if __name__ == "__main__":
    pass
