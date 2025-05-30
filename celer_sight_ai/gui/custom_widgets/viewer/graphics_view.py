import logging

from PyQt6 import QtCore, QtGui, QtWidgets

from celer_sight_ai import config

logger = logging.getLogger(__name__)


class ImagePreviewGraphicsView(QtWidgets.QGraphicsView):
    def __init__(self, parent=None, MainWindow=None):
        super().__init__(parent)
        from PyQt6.QtOpenGLWidgets import QOpenGLWidget

        self.setMouseTracking(True)
        self.setTransformationAnchor(
            QtWidgets.QGraphicsView.ViewportAnchor.AnchorUnderMouse
        )
        # use OpenGL for gpu acceleration if available

        # gl_widget = QOpenGLWidget()
        # self.setViewport(gl_widget)

        self.MainWindow = MainWindow
        self.button_container = []
        self.visible_buttons = []
        self.visible_buttons_ids = []
        self.selected_buttons = [0]  # list of all buttons selected
        # use shift + click to select multiple buttons
        # use ctrl + click to select multiple buttons or deselect a button

        self.previous_update_pos = None  # update prediodically when scrolling, with spacing of sel.update_spacing
        config.global_signals.ensure_current_image_button_visible_signal.connect(
            self.ensure_current_image_button_visible
        )
        config.global_signals.next_image_signal.connect(self.next_image)
        config.global_signals.previous_image_signal.connect(self.previous_image)
        config.global_signals.ensure_current_image_button_visible_signal.connect(
            self.ensure_current_image_button_visible
        )
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.verticalScrollBar().hide()
        self.verticalScrollBar().resize(0, 0)

        config.global_signals.refresh_image_preview_graphicsscene_signal.connect(
            self.update_visible_buttons
        )
        self.setScene(QtWidgets.QGraphicsScene())

        # show the first 30 buttons by default
        self.start_button_i_to_show = 0
        self.end_button_i_to_show = 30
        self.scene_width = self.get_scene_width()
        # self.MainWindow.splitterImagesRight.setSizes([400, width])
        self.scene().setSceneRect(QtCore.QRectF(0, 0, self.scene_width, 50000))
        # self.MainWindow.statistical_analysis_widget_4.setMinimumWidth(self.scene_width)
        # self.scene().setBackgroundBrush(QtCore.Qt.GlobalColor.black)
        self._is_updating_buttons = False

    def handle_range_selection(self, button_number):
        """
        Handles range selection between the last selected image and the current one
        """
        # If no buttons are currently selected, treat this as a single selection
        if not self.selected_buttons:
            self.selected_buttons.append(button_number)
            return
        # Get the range boundaries
        start = min(self.selected_buttons[-1], button_number)
        end = max(self.selected_buttons[-1], button_number)

        # Clear previous selections
        self.uncheck_all_buttons_except_current()
        self.selected_buttons.clear()

        # Select all buttons in the range
        for image_number in range(start, end + 1):
            # Add to selected buttons list
            self.selected_buttons.append(image_number)

            # Find and check the button
            for button in self.visible_buttons:
                if button.image_number == image_number and button.button_instance:
                    button.button_instance.setChecked(True)
                    button.button_instance.set_label_color(True)

    def reset_state(self):
        self.clear_out_visible_buttons()
        self._is_updating_buttons = False
        self.selected_buttons = [0]

    def set_updating_buttons(self, value):
        self._is_updating_buttons = value

    def next_image(self):
        """
        Moves the image on the viewr to the next image
        """
        # Make sure that the self.MainWindow.current_imagenumber is not out of bounds
        # Because it will cause an error on get_current_image_object()
        self.MainWindow.current_imagenumber = min(
            self.MainWindow.current_imagenumber,
            len(
                self.MainWindow.DH.BLobj.groups[
                    self.MainWindow.DH.BLobj.get_current_group()
                ]
                .conds[self.MainWindow.DH.BLobj.get_current_condition()]
                .images
            )
            - 1,
        )

        # Move to the next image of the same condition
        if any(
            [
                i.is_suggested
                for i in self.MainWindow.DH.BLobj.get_current_image_object().masks
            ]
        ):
            self.MainWindow.ai_model_settings_widget.prompt_user_to_save_or_delete_suggestions()
            return
        # if mask generation is running, but no images found above ^,
        # then stop the mask generation, and clear up any masks generated while doing so
        if config.group_running.get("start_suggested_mask_generator"):
            # stop and wait to stop all threads
            logger.info("Stopping mask generation as we move on to the next image.")
            self.MainWindow.sdknn_tool.magic_box_2.stop_mask_suggestion_generator_process()
        self.MainWindow.sdknn_tool.magic_box_2.cleanup_memory()
        self.MainWindow.previous_imagenumber = self.MainWindow.current_imagenumber
        self.MainWindow.current_imagenumber += 1
        self.MainWindow.load_main_scene(self.MainWindow.current_imagenumber)
        # iter through visible buttons and set label to white
        for i in self.MainWindow.images_preview_graphicsview.visible_buttons:
            if i.image_number == self.MainWindow.current_imagenumber:
                i.button_instance.setChecked(True)
                i.button_instance.set_label_color()
            else:
                if i.button_instance is not None:
                    i.button_instance.setChecked(False)
                    i.button_instance.set_label_color()
        config.global_signals.ensure_current_image_button_visible_signal.emit()

    def previous_image(self):
        if any(
            [
                i.is_suggested
                for i in self.MainWindow.DH.BLobj.get_current_image_object().masks
            ]
        ):
            self.MainWindow.ai_model_settings_widget.prompt_user_to_save_or_delete_suggestions()
            return
        # if mask generation is running, but no images found above ^,
        # then stop the mask generation, and clear up any masks generated while doing so
        if config.group_running.get("start_suggested_mask_generator"):
            # stop and wait to stop all threads
            logger.info("Stopping mask generation as we move on to the next image.")
            self.MainWindow.sdknn_tool.magic_box_2.stop_mask_suggestion_generator_process()
        self.MainWindow.sdknn_tool.magic_box_2.cleanup_memory()
        self.MainWindow.previous_imagenumber = self.MainWindow.current_imagenumber
        self.MainWindow.current_imagenumber -= 1
        self.MainWindow.load_main_scene(self.MainWindow.current_imagenumber)
        # iter through visible buttons and set label to white
        for i in self.MainWindow.images_preview_graphicsview.visible_buttons:
            if i.image_number == self.MainWindow.current_imagenumber:
                i.button_instance.setChecked(True)
                i.button_instance.set_label_color()
            else:
                if i.button_instance is not None:
                    i.button_instance.setChecked(False)
                    i.button_instance.set_label_color()
        config.global_signals.ensure_current_image_button_visible_signal.emit()

    def ensure_current_image_button_visible(self):
        # scroll to ensure visible
        # if lower than the current scroll position, scroll up to button Y + height - button height

        visible_rect = self.mapToScene(self.viewport().rect()).boundingRect()

        button_y_pos = (config.BUTTON_SPACING + config.BUTTON_HEIGHT) * (
            self.MainWindow.current_imagenumber // config.BUTTON_COLS
        )
        if button_y_pos < visible_rect.y():
            self.verticalScrollBar().setValue(int(button_y_pos))
        elif (button_y_pos + config.BUTTON_HEIGHT) > (
            visible_rect.y() + visible_rect.height()
        ):
            # if higher than the current scroll position, scroll down to button Y
            self.verticalScrollBar().setValue(
                int((button_y_pos - visible_rect.height()) + config.BUTTON_HEIGHT)
            )

    def get_scene_width(self):
        return (config.BUTTON_WIDTH * (config.BUTTON_COLS)) + (
            (config.BUTTON_COLS + 1) * config.BUTTON_SPACING
        )

    def uncheck_all_buttons_except_current(self):
        for i in self.selected_buttons:
            # get button instance through uuid
            button_object = self.MainWindow.DH.BLobj.get_button_by_image_number(i)
            if button_object and button_object.button_instance:
                button_object.button_instance.set_checked_to_false()

    def clear_out_visible_buttons(self):
        # When changing conditions, delete all the buttons of the current condition
        currentCondition = self.MainWindow.DH.BLobj.get_current_condition()
        currentGroup = self.MainWindow.DH.BLobj.get_current_group()
        logger.debug(f"Deleting Current condition : {currentCondition}")
        all_graphic_items = self.scene().items()
        for item in all_graphic_items:
            if isinstance(item, QtWidgets.QGraphicsProxyWidget):
                button_holder = item.widget().ButtonHolder
                button_holder.button_instance = None
                self.scene().removeItem(item)
                item.deleteLater()
        self.visible_buttons_ids = []
        self.visible_buttons = []

    def substract_from_all_buttons(self, reference_id=None, amount=1):
        # remove the amount form all buttons (for image_id), is usually triggered when deleting an image
        # only affect images larger than reference_id

        for b in self.MainWindow.DH.BLobj.get_all_buttons(
            self.MainWindow.DH.BLobj.get_current_group(),
            self.MainWindow.DH.BLobj.get_current_condition(),
        ):
            if b.image_number > reference_id:
                b.image_number -= amount
                if b.button_instance is not None:
                    b.button_instance.set_label_number(b.image_number + 1)
        for im, image in enumerate(
            self.MainWindow.DH.BLobj.groups[
                self.MainWindow.DH.BLobj.get_current_group()
            ]
            .conds[self.MainWindow.DH.BLobj.get_current_condition()]
            .images
        ):
            if image.imgID > reference_id:
                self.MainWindow.DH.BLobj.groups[
                    self.MainWindow.DH.BLobj.get_current_group()
                ].conds[self.MainWindow.DH.BLobj.get_current_condition()].images[
                    im
                ].imgID -= amount

    def place_all_image_buttons_to_correct_positions(self):
        """
        Updates every button image widget to its correct position by its id
        """
        for b in self.visible_buttons:
            p = self.MainWindow.DH.BLobj.get_box_position(b.image_number)
            b.button_instance_proxy.setPos(p[0], p[1])

    def update_visible_buttons(self, current_condition_widget=None, force_update=False):
        """
        This method is progressivly spawning and despawning buttons as needed within the
        overview_tabs_image -> image_preview_graphicsview.
        """
        try:
            if self._is_updating_buttons:
                return
            self._is_updating_buttons = True

            if current_condition_widget is None:
                # get the current self.MainWindow.RNAi_list widget
                current_condition_widget = (
                    self.MainWindow.get_current_treatment_widget()
                )
                if isinstance(current_condition_widget, type(None)):
                    logger.warning(
                        "No current condition widget found, skipping update_visible_buttons"
                    )
                    return
            all_conds = self.MainWindow.DH.BLobj.groups["default"].conds
            if current_condition_widget.text() in all_conds:
                current_condition_object = all_conds[current_condition_widget.text()]
            else:
                logger.warning(
                    f"Condition {current_condition_widget.text()} not found in data handler"
                )
                return

            condition_uuid = current_condition_object.unique_id

            visible_rect = self.mapToScene(self.viewport().rect()).boundingRect()
            # make it so that the rect has much less space for intersection
            visible_rect = QtCore.QRectF(
                visible_rect.left(),
                visible_rect.top() - config.IMAGE_PREVIEW_TOP_PAD,
                visible_rect.width(),
                visible_rect.height()
                + config.IMAGE_PREVIEW_BOTTOM_PAD
                + config.IMAGE_PREVIEW_BOTTOM_PAD,
            )

            self.start_button_i_to_show = int(
                (visible_rect.top() - config.BUTTON_SPACING)
                / (config.BUTTON_HEIGHT // config.BUTTON_COLS)
            )
            self.end_button_i_to_show = int(
                (visible_rect.bottom() - config.BUTTON_SPACING)
                / (config.BUTTON_HEIGHT // config.BUTTON_COLS)
            )
            center = visible_rect.center()
            if not center:
                self._is_updating_buttons = False
                return

            # # check if number of buttons // cols is less than height, if it is, update image viewport anyway
            if not len(self.visible_buttons) <= self.end_button_i_to_show:
                # get the difference of the visible rect bottom point and top point and find if its greater than the update spacing
                if not force_update and self.previous_update_pos is not None:
                    # get the center point of the visible rect

                    if (
                        abs(center.y() - self.previous_update_pos)
                        < config.IMAGE_PREVIEW_BUFFER
                    ):
                        self._is_updating_buttons = False
                        return

            self.previous_update_pos = center.y()
            currentGroup = self.MainWindow.DH.BLobj.get_current_group()
            # TODO: This needs to become faster, as it is currently blocking the UI
            # iterate over all existsing buttons and hide the ones that are not visible
            for button in self.visible_buttons:
                if button.image_number not in range(
                    max(self.start_button_i_to_show, 0), self.end_button_i_to_show
                ):
                    try:
                        idx = self.visible_buttons_ids.index(button.image_number)
                        print(
                            f"removing button id {button.image_number} at index {idx}"
                        )
                        if (
                            button.button_instance_proxy is not None
                            and button.button_instance_proxy in self.scene().items()
                        ):
                            self.scene().removeItem(button.button_instance_proxy)
                        self.visible_buttons.remove(button)

                        self.visible_buttons_ids.pop(idx)
                        button.button_instance = None
                        button.button_instance_proxy = None
                    except Exception:
                        pass
            # show buttons needed
            all_buttons_to_create_instance = []
            total_buttons_len = len(
                self.MainWindow.DH.BLobj.get_all_buttons(
                    currentGroup, current_condition_widget.text()
                )
            )
            for i in range(
                max(self.start_button_i_to_show, 0), self.end_button_i_to_show
            ):
                if i < 0:
                    continue
                if i in self.visible_buttons_ids:
                    continue
                if total_buttons_len <= i:
                    continue
                all_buttons_to_create_instance.append(i)
                button = self.MainWindow.DH.BLobj.get_button(
                    currentGroup, current_condition_widget.text(), i
                )

                print(f"Adding button id {button.image_number}")
                self.visible_buttons.append(button)
                self.visible_buttons_ids.append(i)
            # start threaded function that sends signals to create buttons instances

            height = (
                (config.BUTTON_SPACING + config.BUTTON_SPACING + config.BUTTON_HEIGHT)
                * total_buttons_len
                // config.BUTTON_COLS
            )

            self.scene().setSceneRect(
                QtCore.QRectF(0, 0, self.scene_width, max(500, height))
            )

            all_objects = [
                [
                    currentGroup,
                    condition_uuid,
                    i,
                    True if i == all_buttons_to_create_instance[-1] else None,
                ]
                for i in all_buttons_to_create_instance
            ]
            if len(all_objects) == 0:
                self._is_updating_buttons = False

            per_chunk = 5

            # group objects in a list of 5 if possible
            all_objects = [
                all_objects[i : i + per_chunk]
                for i in range(0, len(all_objects), per_chunk)
            ]

            # Loop through each chunk
            for i in range(len(all_objects)):
                config.global_signals.create_button_instance_signal.emit(all_objects[i])

        except Exception as e:
            print(e)
        finally:
            self._is_updating_buttons = False

    def scrollContentsBy(self, dx, dy):
        self.update_visible_buttons()
        super().scrollContentsBy(dx, dy)

    def mousePressEvent(self, event):
        # get position in scene of the press event
        pos = self.mapToScene(event.pos())
        # get the item at that location
        item = self.itemAt(pos.toPoint())
        # if item is not None, then it is the item you want
        if item is not None:
            # item.click()
            print("item clicked")
        super().mousePressEvent(event)

    def contextMenuEvent(self, event):
        """
        Conetext menu for Images inside the image preview area that runs on right click
        """
        menu = QtWidgets.QMenu()
        event_pos = self.mapToGlobal(event.pos())

        proxy_item = self.scene().itemAt(
            self.mapToScene(event.pos()), QtGui.QTransform()
        )
        if proxy_item is None:
            return
        widget_item = proxy_item.widget()
        io = self.MainWindow.DH.BLobj.get_image_object_by_uuid(
            widget_item.ButtonHolder.image_uuid
        )

        # Add ROI submenu for inferenec on this image

        classes = (
            self.MainWindow.DH.BLobj.get_all_classes()
        )  # Assuming this method exists

        if len(self.selected_buttons) > 1:
            image_objects = []
            for button_idx in self.selected_buttons:
                image_objects.append(
                    self.MainWindow.DH.BLobj.get_image_object_by_uuid(
                        self.MainWindow.DH.BLobj.get_button_by_image_number(
                            button_idx
                        ).image_uuid
                    )
                )
            image_objects = [i for i in image_objects if i is not None]
        else:
            image_objects = [io]

        if len(self.selected_buttons) > 1:
            # Get proxy items for all selected buttons
            all_proxies = []
            all_widgets = []
            for button_idx in self.selected_buttons:
                # Find the proxy item and widget for each selected button
                button = self.MainWindow.DH.BLobj.get_button_by_image_number(button_idx)
                if button and button.button_instance_proxy:
                    all_proxies.append(button.button_instance_proxy)
                    all_widgets.append(button.button_instance)

            DeleteAction = QtGui.QAction("Delete All Selected", None)
            DeleteAction.triggered.connect(
                lambda: self.delete_images(all_proxies, all_widgets)
            )
        else:
            DeleteAction = QtGui.QAction("Delete", None)
            DeleteAction.triggered.connect(
                lambda: self.delete_image(proxy_item, widget_item)
            )

        if io.is_remote():
            if len(self.selected_buttons) > 1:
                if any([i for i in image_objects if i.is_remote()]):
                    delete_remote_action = menu.addAction("Delete All Remote Images")
                # get all uuids of the selected buttons
                image_uuids = []
                image_uuids = list(set([i.unique_id for i in image_objects]))
                delete_remote_action.triggered.connect(
                    lambda: config.client.delete_remote_images(image_uuids)
                )
            else:
                delete_remote_action = menu.addAction("Delete Remote Image")
                delete_remote_action.triggered.connect(
                    lambda: config.client.delete_remote_images([io.unique_id])
                )
        roi_menu = menu.addMenu("Get ROI for...")
        roi_all_action = roi_menu.addAction("All")
        roi_all_action.triggered.connect(
            lambda: self.MainWindow.MyInferenceHandler.DoInferenceAllImagesOnlineThreaded(
                provided_classes=[i for i in classes],
                provided_image_objects=image_objects,
            )
        )

        for some_class in classes:
            action = roi_menu.addAction(classes[some_class].text())
            action.triggered.connect(
                lambda: self.MainWindow.MyInferenceHandler.DoInferenceAllImagesOnlineThreaded(
                    provided_classes=[some_class],
                    provided_image_objects=image_objects,
                )
            )

        menu.addAction(DeleteAction)
        menu.addMenu(roi_menu)
        menu.exec(event_pos)

    def delete_image(self, proxy, widget):
        logger.info(f"Deleted image preview item : {widget.image_number}")
        self.scene().removeItem(proxy)
        self.MainWindow.channel_picker_widget.clear_channels()
        widget.deleteCurrentImage()

        return

    def delete_images(self, proxies, widgets):
        for proxy, widget in zip(proxies, widgets):
            self.delete_image(proxy, widget)

    def displace_image_preview_widgets_after_delete(self):
        pass
