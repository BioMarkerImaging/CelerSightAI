import logging

from PyQt6 import QtCore, QtGui, QtWidgets

from celer_sight_ai import config

logger = logging.getLogger(__name__)


class DialogWidgetTitleHat(QtWidgets.QWidget):
    def __init__(self, title: str, widget_to_encapsule):
        parent = widget_to_encapsule.parent() if widget_to_encapsule else None
        super(DialogWidgetTitleHat, self).__init__(parent)
        self.title = QtWidgets.QLabel(title)
        # set background to translucent events
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)

        initial_parent = widget_to_encapsule.parent()
        if initial_parent:
            widget_to_encapsule.setParent(self)
            self.setParent(initial_parent)
        # set the layout
        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.setObjectName("layout_hat")
        self.layout.addWidget(self.title)
        self.layout.addWidget(widget_to_encapsule)
        self.setLayout(self.layout)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)

        self.title_font = QtGui.QFont("Arial", 12, QtGui.QFont.Weight.Bold)
        self.title_font.setCapitalization(QtGui.QFont.Capitalization.AllUppercase)
        self.title_font.setLetterSpacing(QtGui.QFont.SpacingType.AbsoluteSpacing, 1)
        self.title_font.setWordSpacing(1)
        self.title_font.setPointSize(12)
        self.title_font.setBold(True)
        self.title_font.setItalic(False)
        self.title_font.setUnderline(False)
        self.title_font.setStrikeOut(False)
        self.title_font.setKerning(True)
        self.title_font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)
        self.title_font.setStyleHint(QtGui.QFont.StyleHint.SansSerif)
        self.title_font.setWeight(75)
        self.title_font.setHintingPreference(
            QtGui.QFont.HintingPreference.PreferDefaultHinting
        )
        self.title_font.setFamily("Arial")
        self.title_font.setStyle(QtGui.QFont.Style.StyleNormal)
        self.title_font.setFixedPitch(False)
        self.title_font.setPointSize(12)
        self.title_font.setStretch(QtGui.QFont.Stretch.Unstretched)
        self.title_font.setOverline(False)
        self.title.setFont(self.title_font)
        self.title.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.title.setMaximumHeight(30)
        self.title.setStyleSheet(
            """
                border : 1px solid;
                font: 17 "Lato";
                border-bottom : 0px solid;
                font-weight:bold;
                font-size: 12px;
                border-color: rgba(102, 102, 102,0);
                subcontrol-origin: margin;
                subcontrol-position: top left;
                border-top-left-radius: 8px;
                border-top-right-radius: 8px;
                background-color: rgb(25, 25, 25);
                color:rgba( 255, 255, 255, 220);
                margin-top:1px;
                padding: 6px ;
                color:rgba( 255, 255, 255, 220);
        """
        )


class NewCategoryWidget(QtWidgets.QWidget):
    def __init__(self, parent=None, on_success=None):
        """
        on_success :  function to call when the category is successfully added
        """
        super(NewCategoryWidget, self).__init__(parent)
        from celer_sight_ai.gui.custom_widgets.modern_qcombobox_widgets import (
            ModernQComboBox,
            ModernQComboBoxAlternative,
        )

        self.on_success = on_success
        self.super_categories = {
            "worm": "Worm",
            "cell": "Cell",
            "on_plate": "On Plate",
            "tissue": "Tissue",
            "other": "Other",
        }
        self.category_types = [
            "Local",
            "Community - Self Improving (AI)",
            "Private - Self Improving (AI)",
        ]

        self.layout_outer = QtWidgets.QVBoxLayout(self)
        self.layout_outer.setObjectName("layout_outer")
        self.layout_outer.setContentsMargins(0, 0, 0, 0)

        self.outer_widget = QtWidgets.QWidget(self)
        self.outer_widget.setObjectName("outer_widget")
        self.outer_widget.setStyleSheet("background-color: rgb(23, 23, 23 );")

        self.layout_outer_2 = QtWidgets.QVBoxLayout(self.outer_widget)
        self.layout_outer_2.setObjectName("layout_outer_2")
        self.layout_outer_2.setContentsMargins(0, 0, 0, 0)
        self.layout_outer_2.setSpacing(0)
        self.layout_outer.addWidget(self.outer_widget)
        self.outer_widget.setLayout(self.layout_outer_2)

        self.stackedWidget = QtWidgets.QStackedWidget()
        self.layout_outer_2.addWidget(self.stackedWidget)
        # self.setLayout(self.layout_outer_2)
        #### PAGE 1 ####

        self.page_1 = QtWidgets.QWidget(self.stackedWidget)

        self.stackedWidget.addWidget(self.page_1)
        # create a grid layout
        self.layout_page_1 = QtWidgets.QGridLayout()
        self.layout_page_2 = QtWidgets.QGridLayout()
        self.layout_page_3 = QtWidgets.QGridLayout()

        self.page_1.setLayout(self.layout_page_1)
        self.sub_layout_1 = QtWidgets.QVBoxLayout()
        self.sub_layout_2 = QtWidgets.QVBoxLayout()
        self.sub_layout_3 = QtWidgets.QVBoxLayout()
        self.sub_layout_4 = QtWidgets.QVBoxLayout()

        self.layout_page_1.addLayout(self.sub_layout_1, 0, 0)
        self.layout_page_1.addLayout(self.sub_layout_2, 1, 0)
        # self.layout_page_2.addLayout(self.sub_layout_3, 0, 0)
        # self.layout_page_2.addLayout(self.sub_layout_4, 1, 0)

        # self.layout_page_1.addLayout(self.sub_layout_3, 2, 0)
        # self.layout_page_1.addLayout(self.sub_layout_4, 3, 0)

        TITLE_FONT_SIZE = 16
        NORMAL_FONT_SIZE = 12
        SUBTITLE_FONT_SIZE = 11
        # sub layout 1
        self.super_category_label = QtWidgets.QLabel(
            f"Super Category : {config.supercategory}"
        )
        self.super_category_label.setFont(
            QtGui.QFont("Arial", TITLE_FONT_SIZE, QtGui.QFont.Weight.Bold)
        )

        self.sub_layout_1.addWidget(self.super_category_label)
        self.super_category_label.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Maximum
        )

        # sub layout 2
        self.category_name_label = QtWidgets.QLabel("Category Name : ")
        self.category_name_label.setFont(
            QtGui.QFont("Arial", TITLE_FONT_SIZE, QtGui.QFont.Weight.Bold)
        )
        self.category_name_label.setWordWrap(True)

        self.category_name_input = QtWidgets.QLineEdit()
        self.category_name_input.setPlaceholderText("Enter a new category name")
        # set to only accept alphanumeric characters and underscores and lowercase
        self.category_name_input.setValidator(
            QtGui.QRegularExpressionValidator(
                QtCore.QRegularExpression("[a-z0-9 _\-\+]+")
            )
        )
        # set font size
        self.category_name_input.setFont(
            QtGui.QFont("Arial", NORMAL_FONT_SIZE, QtGui.QFont.Weight.Normal)
        )
        self.category_name_input.setStyleSheet(
            """
            color: rgb(120, 120, 120);
            """
        )
        # Create horizontal layout for category name label and input
        category_name_layout = QtWidgets.QHBoxLayout()
        category_name_layout.addWidget(self.category_name_label)
        category_name_layout.addWidget(self.category_name_input)

        self.sub_layout_2.addLayout(category_name_layout)

        text_1 = "Please choose a name that is unique and generalisable enough to be applicable in many cases with similar phenotypes."
        self.category_name_sub_label = QtWidgets.QLabel(text_1)
        self.category_name_sub_label.setFont(
            QtGui.QFont("Arial", SUBTITLE_FONT_SIZE, QtGui.QFont.Weight.Normal)
        )
        self.category_name_sub_label.setWordWrap(True)
        self.category_name_sub_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)
        self.sub_layout_2.addWidget(self.category_name_sub_label)

        # Category Type
        self.category_type_label = QtWidgets.QLabel("Category type :")
        self.category_type_label.setFont(
            QtGui.QFont("Arial", TITLE_FONT_SIZE, QtGui.QFont.Weight.Bold)
        )
        self.category_type_label.setWordWrap(True)
        self.category_type_label.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.Maximum, QtWidgets.QSizePolicy.Policy.Maximum
        )

        self.category_type_dropdown = ModernQComboBoxAlternative()
        self.category_type_dropdown.addItems(self.category_types)

        # Create horizontal layout for category type label and dropdown
        category_type_layout = QtWidgets.QHBoxLayout()
        category_type_layout.addWidget(self.category_type_label)
        category_type_layout.addWidget(self.category_type_dropdown)

        self.sub_layout_2.addLayout(category_type_layout)

        # sub layout 5
        self.parent_category_label = QtWidgets.QLabel("Parent Category")
        self.parent_category_label.setFont(
            QtGui.QFont("Arial", TITLE_FONT_SIZE, QtGui.QFont.Weight.Bold)
        )
        self.parent_category_label.setWordWrap(True)
        self.parent_category_label.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.Maximum, QtWidgets.QSizePolicy.Policy.Maximum
        )
        self.parent_category_dropdown = ModernQComboBoxAlternative()
        self.parent_category_dropdown.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum
        )
        self.category_items = read_default_config_classes()

        # Create horizontal layout for parent category label and dropdown
        parent_category_layout = QtWidgets.QHBoxLayout()
        parent_category_layout.addWidget(self.parent_category_label)
        parent_category_layout.addWidget(self.parent_category_dropdown)

        self.sub_layout_2.addLayout(parent_category_layout)

        # Add description label and input box
        self.description_label = QtWidgets.QLabel("Description (Optional)")
        self.description_label.setFont(
            QtGui.QFont("Arial", TITLE_FONT_SIZE, QtGui.QFont.Weight.Bold)
        )
        self.description_label.setWordWrap(True)
        self.description_label.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.Maximum, QtWidgets.QSizePolicy.Policy.Maximum
        )

        self.description_input = QtWidgets.QTextEdit()
        self.description_input.setPlaceholderText(
            "Enter a description for the category"
        )
        self.description_input.setFont(
            QtGui.QFont("Arial", NORMAL_FONT_SIZE, QtGui.QFont.Weight.Normal)
        )
        self.description_input.setStyleSheet(
            """
            color: rgb(120, 120, 120);
            border: 1px solid rgb(75, 75, 75);
            border-radius: 5px;
            padding: 5px;
            background-color: rgb(45, 45, 45);
        """
        )
        self.description_input.setMinimumHeight(100)

        # Create vertical layout for description label and input
        description_layout = QtWidgets.QVBoxLayout()
        description_layout.addWidget(self.description_label)
        description_layout.addWidget(self.description_input)

        # Add the description layout to the main layout
        self.sub_layout_2.addLayout(description_layout)

        # add next and back / cancel buttons
        self.next_button = QtWidgets.QPushButton("Create")
        self.next_button.setObjectName("next_button")
        self.next_button.clicked.connect(lambda: self.next_button_clicked())
        self.back_button = QtWidgets.QPushButton("Back")
        self.back_button.setObjectName("back_button")
        self.back_button.clicked.connect(lambda: self.back_button_clicked())
        self.cancel_button = QtWidgets.QPushButton("Cancel")
        self.cancel_button.setObjectName("cancel_button")
        self.cancel_button.clicked.connect(lambda: self.cancel_button_clicked())
        self.button_layout = QtWidgets.QHBoxLayout()
        self.button_layout.addWidget(self.cancel_button)
        self.button_layout.addWidget(self.back_button)
        self.button_layout.addWidget(self.next_button)
        self.button_layout.setContentsMargins(6, 6, 6, 6)
        self.button_layout.setSpacing(6)
        self.next_button.setMinimumHeight(25)
        self.next_button.setMinimumWidth(100)
        self.back_button.setMinimumHeight(25)
        self.back_button.setMinimumWidth(100)
        self.cancel_button.setMinimumHeight(25)
        self.cancel_button.setMinimumWidth(100)

        # fix font size
        self.next_button.setFont(
            QtGui.QFont("Arial", NORMAL_FONT_SIZE, QtGui.QFont.Weight.Bold)
        )
        self.back_button.setFont(
            QtGui.QFont("Arial", NORMAL_FONT_SIZE, QtGui.QFont.Weight.Bold)
        )
        self.cancel_button.setFont(
            QtGui.QFont("Arial", NORMAL_FONT_SIZE, QtGui.QFont.Weight.Bold)
        )

        self.layout_outer_2.addLayout(self.button_layout)

        self.back_button.setEnabled(False)
        self.on_supercategory_change()

        # add title hat
        self.title_hat = DialogWidgetTitleHat("Create New Category", self)
        self.title_hat.setObjectName("title_hat")
        self.title_hat.show()

        # set minimum dimentions
        self.title_hat.setMinimumWidth(400)
        self.title_hat.setMinimumHeight(400)
        self.title_hat.setFixedSize(400, 400)
        self.title_hat.setMaximumSize(400, 400)
        # frameless window
        self.title_hat.setWindowFlags(QtCore.Qt.WindowType.FramelessWindowHint)
        # modal
        self.setStyleSheet(
            """

            #layout_outer{
                background-color: rgb(45, 45, 45 );
            }
            QWidget{
                background-color: rgb(45, 45, 45);
            }
            #next_button{
                color: rgb(90,185,90);
                background-color: rgb(20,60,20);
                border-radius: 5px;
            }
            #next_button:hover{
                color: rgb(100,255,100);
                background-color: rgb(0,90,0);
                border-radius: 5px;
                border: 2px solid rgb(0,100,0);
            }
                           
            #cancel_button{
                color: rgb(185,90,90);
                background-color: rgb(40,20,20);
                border-radius: 5px;
            }
            #cancel_button:hover{
                color: rgb(235,100,100);
                background-color: rgb(80,0,0);
                border-radius: 5px;
            }
            #back_button{
                color: rgb(185,185,185);
                background-color: rgb(45,45,45);
                border-radius: 5px;
            }
            #back_button:hover{
                color: rgb(255,255,255);
                background-color: rgb(75,75,75);
                border-radius: 5px;
            }
                                     
            
            #layout_hat{
                            background-color: rgb(45, 45, 45);
                                     }                  
                                     
            QLabel{
                color: rgb(255, 255, 255);
            }
            QLineEdit{
                color: rgb(255, 255, 255);
                border: 1px solid rgb(75, 75, 75 );
                border-radius: 5px;
                padding: 5px;
                background-color: rgb(45, 45, 45 );
                }

        """
        )
        self.title_hat.show()

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key.Key_Escape:
            self.title_hat.close()
        if event.key() == QtCore.Qt.Key.Key_Return:
            self.next_button_clicked()

    def cancel_button_clicked(self):
        self.parent().close()
        self.close()

    def next_button_clicked(self):
        current_index = self.stackedWidget.currentIndex()
        current_supercategory = config.supercategory
        if current_index == 0:
            if not self.category_name_input.text():
                self.category_name_input.setStyleSheet("border: 1px solid red")
                config.global_signals.errorSignal.emit("Category name is empty.")
                return
            # if the category name already exists, throw an error
            if self.category_name_input.text() in [
                i["category"]
                for i in self.category_items.values()
                if i["supercategory"] == current_supercategory
            ]:
                self.category_name_input.setStyleSheet("border: 1px solid red")
                config.global_signals.errorSignal.emit(
                    "Category name already exists, please choose another name."
                )
                return
            self.category_name_input.setStyleSheet("border: 0px solid red")
            # self.next_button.setText("Create")
            # self.back_button.setEnabled(True)
            # self.stackedWidget.setCurrentIndex(1)
            # save the category
            self.save_category()
            # refresh the grid category widget
            config.global_signals.refresh_categories_signal.emit()
            self.close()

    def save_category(self):
        logger.info("Saving category")
        import json
        import os
        from datetime import datetime

        from celer_sight_ai import configHandle

        category_type = self.category_type_dropdown.currentText()
        supercategory = config.supercategory
        name = self.category_name_input.text()
        if not self.parent_category_dropdown.currentText() == " - ":
            parent_class_uuid = [
                i["uuid"]
                for i in self.category_items.values()
                if i["category"] == self.parent_category_dropdown.currentText()
            ][0]
        else:
            parent_class_uuid = None

        category_uuid = config.get_unique_id()
        # we can create the uuid here because we are saving the cateogry locally
        while category_uuid in [i["uuid"] for i in self.category_items.values()]:
            category_uuid = config.get_unique_id()
        category_uuid = str(category_uuid)
        if category_type == "Local":
            logger.info(f"Saving category locally {name}")
            # save the category locally
            data = {
                "supercategory": supercategory,
                "text": name,  # TODO: Add Display Name (optional)
                "uuid": str(category_uuid),
                "classes": [
                    {
                        "class_name": name,
                        "uuid": category_uuid,
                        "parent_class_uuid": parent_class_uuid,
                    }
                ],
                "type": "local",
                "updated_at": datetime.now().strftime("%a, %d %b %Y %H:%M:%S GMT"),
                "created_at": datetime.now().strftime("%a, %d %b %Y %H:%M:%S GMT"),
                "lab": None,
                "description": self.description_input.toPlainText(),  # Add description to the data
            }
            # Local and cloud categories needs to be saved in different directories
            # because the cloud categories are synced with the server on every log in.
            if os.path.exists(
                os.path.join(configHandle.getLocal(), config.LOCAL_CATEGORIES_FILE)
            ):
                with open(
                    os.path.join(configHandle.getLocal(), config.LOCAL_CATEGORIES_FILE),
                ) as f:
                    current_local_categories = json.load(f)
            else:
                current_local_categories = []
            current_local_categories.append(data)
            with open(
                os.path.join(configHandle.getLocal(), config.LOCAL_CATEGORIES_FILE),
                "w",
            ) as f:
                json.dump(current_local_categories, f, indent=4)
            config.global_signals.refresh_categories_signal.emit()
            QtWidgets.QApplication.processEvents()
            self.title_hat.close()
            self.close()

        else:
            logger.info(
                f"Saving category to cloud {name} {self.category_type_dropdown.currentText()}"
            )
            if (
                self.category_type_dropdown.currentText()
                == "Community - Self Improving (AI)"
            ):
                cat_type = "global"
            elif (
                self.category_type_dropdown.currentText()
                == "Private - Self Improving (AI)"
            ):
                cat_type = "private"
            else:
                raise ValueError("Invalid category type")

            data = {
                "category": self.category_name_input.text(),
                "supercategory": config.supercategory,
                "type": cat_type,
                # parent category gets converted to uuid on the server
                "parent_category": self.parent_category_dropdown.currentText(),
                "username": config.user_attributes.username,
                "text": name,
                "description": self.description_input.toPlainText(),
            }

            config.client.create_new_category_cloud(data)
            if self.on_success:
                self.on_success()
            # refresh all categories
            config.global_signals.refresh_categories_signal.emit()
            QtWidgets.QApplication.processEvents()

            self.title_hat.close()
            self.close()

    def back_button_clicked(self):
        current_index = self.stackedWidget.currentIndex()
        if current_index == 1:
            self.stackedWidget.setCurrentIndex(0)
            self.next_button.setText("Next")
            self.back_button.setEnabled(False)


    def on_supercategory_change(self):
        self.parent_category_dropdown.clear()

        QtWidgets.QApplication.processEvents()
        try:
            sup = config.supercategory
        except:
            return
        items = [
            i["category"]
            for i in self.category_items.values()
            if i["supercategory"] == sup
        ]
        if items:
            self.parent_category_dropdown.addItems(items)

        self.parent_category_dropdown.addItem(" - ")
        # set none as the default
        self.parent_category_dropdown.setCurrentText(" - ")
        # disable the category type dropdown, as only the current supercategory is allowed


def read_default_config_classes():

    from celer_sight_ai.gui.custom_widgets.grid_button_image_selector import (
        gather_cfgs,
    )

    all_cfgs = gather_cfgs()
    all_categories = {}
    for c in all_cfgs:
        if len(c["classes"]) == 1:
            # only one classes will be displayed
            all_categories[c["classes"][0]["uuid"]] = {
                "supercategory": c["supercategory"],
                "category": c["classes"][0]["class_name"],
                "uuid": c["classes"][0]["uuid"],
            }
            # otherwise its an experiment (multiple classes)
    return all_categories

if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    w = NewCategoryWidget()
    w.show()
    sys.exit(app.exec())
