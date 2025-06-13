        if self._photo.isUnderMouse():
            if event.button() == QtCore.Qt.MouseButton.LeftButton:
                self.leftMouseBtn_autoRepeat = True
                if event.modifiers() & QtCore.Qt.KeyboardModifier.ControlModifier:
                    if self.aa_tool_draw is True:  # if we are drawing a magic bbox
                        # special case that we adjust the precious bbox
                        self.add_point_as_magic_click(
                            self.mapToScene(event.position().toPoint()).toPoint()
                        )
                        return super().mousePressEvent(event)

                if self.mgcClick_STATE:

                    cPos = self.mapToScene(event.position().toPoint())
                    # patch it
                    self.aa_tool_bb_first_x = int(cPos.x() - self.mgcClickWidth / 2)
                    self.aa_tool_bb_first_y = int(cPos.y() - self.mgcClickWidth / 2)
                    self.last_bbox_x = int(cPos.x() + self.mgcClickWidth / 2)
                    self.last_bbox_y = int(cPos.y() + self.mgcClickWidth / 2)
                    self.draw_bounding_box_stop_THREADED(
                        self.mapToScene(event.position().toPoint()).toPoint()
                    )

            self.photoClicked.emit(
                self.mapToScene(event.position().toPoint()).toPoint()
            )
            self.buttonPress = True
        return super().mousePressEvent(event)

    def keyReleaseEvent(self, ev):
        key = ev.key()
        if key == QtCore.Qt.Key.Key_Shift or key == QtCore.Qt.Key.Key_Alt:
            self.POLYGON_MODIFY_MODE = None
        return super().keyReleaseEvent(ev)

    def keyPressEvent(self, event):
        key = event.key()

        if key == QtCore.Qt.Key.Key_Escape:
            if self.i_am_drawing_state is True:
                self.completeDrawingPolygon()
            if self.SkGb_during_drawing == True:
                self.placeSkGbFinish(pos=None, COMPLETE=False)
            if self.aa_tool_draw and self.during_drawing_bbox:
                self.completeDrawing_Bounding_Box()
            return super(PhotoViewer, self).keyPressEvent(event)
        if key == QtCore.Qt.Key.Key_Enter or key == QtCore.Qt.Key.Key_Return:
            if self.i_am_drawing_state == True:
                self.completeDrawingPolygon(MODE="complete")
            if self.aa_tool_draw:
                # when the mask suggestor is on with magic box, complete the process
                # if accept all mask suggestions
                self.MainWindow.sdknn_tool.magic_box_2.accept_current_suggested_annotations()
        if key == QtCore.Qt.Key.Key_Alt:
            self.POLYGON_MODIFY_MODE = self.POLYGON_MODIFY_REMOVE
        if key == QtCore.Qt.Key.Key_Shift:
            self.POLYGON_MODIFY_MODE = self.POLYGON_MODIFY_ADD
        if (
            key == QtCore.Qt.Key.Key_Return
            and event.modifiers() & QtCore.Qt.KeyboardModifier.ControlModifier
        ):
            self.MainWindow.spawn_add_class_dialog()

        return super(PhotoViewer, self).keyPressEvent(event)

    def mouseMoveEvent(self, event):
        scene_pos = self.mapToScene(event.position().toPoint())
        scene_pos_point = scene_pos.toPoint()

        # Update status text less frequently
        if hasattr(self, "_status_update_timer"):
            self._status_update_timer.stop()
        else:
            self._status_update_timer = QtCore.QTimer()
            self._status_update_timer.setSingleShot(True)
            self._status_update_timer.timeout.connect(
                lambda: self.MainWindow.under_window_comments.setText(
                    f"Scene pos: {int(scene_pos.x())} {int(scene_pos.y())}"
                )
            )
        self._status_update_timer.start(50)
        # Zoom-aware tile culling (debounced)
        if hasattr(self, "_zoom_cull_timer"):
            self._zoom_cull_timer.stop()
        else:
            self._zoom_cull_timer = QtCore.QTimer()
            self._zoom_cull_timer.setSingleShot(True)
            self._zoom_cull_timer.timeout.connect(self.cull_inappropriate_zoom_tiles)
        self._zoom_cull_timer.start(100)

        # rubber band mode:
        if self.scaleBarDraw_duringDraw_STATE is True:
            self.scaleBarWhile(scene_pos_point)

        if self.ui_tool_selection.selected_button == "skeleton grabcut":
            if self.SkGb_during_drawing is True:
                self.SkGbWhileDrawing(scene_pos_point)

        if self.MAGIC_BRUSH_DURING_DRAWING is True:
            self.movePointsBrushToolMagic1(
                self.magic_brush_pos_a.x() - scene_pos.x(),
                self.magic_brush_pos_a.y() - scene_pos.y(),
                self.magic_brush_points_set_A,
            )
            self.magic_brush_pos_a = scene_pos

        # FIX RUBBER BAND HERE
        """
        Draw FG or BG at CELL Random Forrest
        """
        if self.rm_Masks_tool_draw is True:
            self.DeleteAllMasksUnderMouse(scene_pos_point)
            return super().mouseMoveEvent(event)
        if self.i_am_drawing_state is True:
            self.CurrentPosOnScene = scene_pos_point
        if self.aa_review_state is True:
            return super().mouseMoveEvent(event)
        if self.aa_tool_draw is True:
            if self.i_am_drawing_state_bbox is True:
                # starts the drawing process
                self.auto_annotate_tool_while_draw(scene_pos_point)
            self.global_pos = self.mapToGlobal(
                QtCore.QPoint(int(scene_pos.x()), int(scene_pos.y()))
            )
            # if magic tool is active

            # update the position of the guides
            pos = self.mapToScene(event.position().toPoint())
            topLeft = self.mapToScene(0, 0)
            bottomRight = self.mapToScene(
                self.viewport().width(), self.viewport().height()
            )
            if self.h_guide_magic_tool not in self.scene().items():
                self.scene().addItem(self.h_guide_magic_tool)
                self.scene().addItem(self.v_guide_magic_tool)
            self.h_guide_magic_tool.setLine(
                topLeft.x(), pos.y(), bottomRight.x(), pos.y()
            )
            self.v_guide_magic_tool.setLine(
                pos.x(), topLeft.y(), pos.x(), bottomRight.y()
            )
            # bring it to the top
            self.h_guide_magic_tool.setZValue(9999)
            self.h_guide_magic_tool.show()
            self.v_guide_magic_tool.setZValue(9999)
            self.v_guide_magic_tool.show()

        if (
            self.ui_tool_selection.selected_button == "polygon"
            and self.hasPhoto()
            and self.pop_up_tool_choosing_state != True
        ):
            # if gui_main.DH.masks_state[gui_main.current_imagenumber] == True or gui_main.DH.masks_state_usr[gui_main.current_imagenumber] == True :

            if self._photo.isUnderMouse() and self.add_mask_btn_state is True:
                if self.MainWindow.counter_tmp > 0 and self.i_am_drawing_state is True:
                    self.draw_while_mouse_move(scene_pos_point)
                    return super().mouseMoveEvent(event)

        if self.ML_brush_tool_draw_is_active is True and self.brushMask_STATE is True:
            if self.ML_brush_tool_draw_foreground_add is True:
                # get pos on scene
                evPos = scene_pos

                currentImg = (
                    self.MainWindow.DH.BLobj.groups["default"]
                    .conds[self.MainWindow.DH.BLobj.get_current_condition()]
                    .getImage(self.MainWindow.current_imagenumber)
                )

                rr, cc = circle(
                    evPos.x(),
                    evPos.y(),
                    self.getML_brush_tool_draw_brush_size(),
                    shape=(currentImg.shape[0], currentImg.shape[1]),
                )
                # Draw on machine learning frame
                self.ML_brush_tool_draw_foreground_array[cc, rr] = True
                # Draw on viewer
                self.CELL_RM_point_drawing = QtWidgets.QGraphicsEllipseItem(
                    evPos.x() - self.getML_brush_tool_draw_brush_size(),
                    evPos.y() - self.getML_brush_tool_draw_brush_size(),
                    self.getML_brush_tool_draw_brush_size(),
                    self.getML_brush_tool_draw_brush_size(),
                )
                pen = QtGui.QPen(QtCore.Qt.GlobalColor.green)
                pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
                self.CELL_RM_point_drawing.setBrush(
                    QtGui.QBrush(
                        QtCore.Qt.GlobalColor.green, QtCore.Qt.BrushStyle.SolidPattern
                    )
                )
                self.CELL_RM_point_drawing.setPen(pen)
                self._scene.addItem(self.CELL_RM_point_drawing)
                self.ML_brush_tool_draw_scene_items.append(self.CELL_RM_point_drawing)
                self.ML_brush_tool_draw_background_added = True
                self.ML_brush_tool_draw_refreshed = False
                return super().mouseMoveEvent(event)

            elif self.ML_brush_tool_draw_background_add is True:
                evPos = scene_pos
                currentImg = (
                    self.MainWindow.DH.BLobj.groups["default"]
                    .conds[self.MainWindow.DH.BLobj.get_current_condition()]
                    .getImage(self.MainWindow.current_imagenumber)
                )
                rr, cc = circle(
                    evPos.x(),
                    evPos.y(),
                    self.getML_brush_tool_draw_brush_size(),
                    shape=(currentImg.shape[0], currentImg.shape[1]),
                )
                # Draw on machine learning frame
                self.ML_brush_tool_draw_background_array[cc, rr] = True
                # Draw on viewer
                self.CELL_RM_point_drawing = QtWidgets.QGraphicsEllipseItem(
                    evPos.x() - self.getML_brush_tool_draw_brush_size(),
                    evPos.y() - self.getML_brush_tool_draw_brush_size(),
                    self.getML_brush_tool_draw_brush_size() * 2.0,
                    self.getML_brush_tool_draw_brush_size() * 2.0,
                )
                pen = QtGui.QPen(QtCore.Qt.GlobalColor.red)
                pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
                self.CELL_RM_point_drawing.setBrush(
                    QtGui.QBrush(
                        QtCore.Qt.GlobalColor.red, QtCore.Qt.BrushStyle.SolidPattern
                    )
                )
                self.CELL_RM_point_drawing.setPen(pen)
                self._scene.addItem(self.CELL_RM_point_drawing)
                self.ML_brush_tool_draw_foreground_added = True
                self.ML_brush_tool_draw_scene_items.append(self.CELL_RM_point_drawing)
                self.ML_brush_tool_draw_refreshed = False
                return super().mouseMoveEvent(event)

        if self.pop_up_tool_choosing_state is True:
            if event.type() == QtCore.QEvent.Type.MouseMove:
                self.ui_tool_selection.MyDialog.mouseMoveEvent(event)
                # return True
        return super().mouseMoveEvent(event)

    def eventFilter(self, source, event):
        """
        mouse move event
        """
        if isinstance(event, QtGui.QNativeGestureEvent):
            # This is mainly for macs and zooming in using the trackpad
            typ = event.gestureType()
            if typ == QtCore.Qt.NativeGestureType.BeginNativeGesture:
                # start of event.
                self.zoomValue = 0.0
                self.target_zoom_pos = self.mapToScene(
                    event.position().toPoint()
                )  # * scale  # * scale
            elif typ == QtCore.Qt.NativeGestureType.ZoomNativeGesture:

                # Improved gesture handling with matrix validation
                current_matrix = self.transform()

                # Check if matrix is valid (determinant should be positive)
                determinant = current_matrix.determinant()

                if (
                    determinant <= 0
                    or abs(current_matrix.m11()) < 0.001
                    or abs(current_matrix.m22()) < 0.001
                ):
                    # Matrix is corrupted, reset to identity and reapply current zoom
                    logger.warning(
                        "Detected corrupted transformation matrix, resetting"
                    )
                    self.resetTransform()
                    # Restore to a reasonable zoom level
                    if hasattr(self, "_last_valid_zoom"):
                        zoom_level = max(0.1, min(10.0, self._last_valid_zoom))
                        self.scale(zoom_level, zoom_level)
                    return True

                # Store last valid zoom for recovery
                self._last_valid_zoom = abs(current_matrix.m11())

                # Apply zoom with safer bounds
                zoom_delta = np.clip(
                    event.value(), -0.5, 0.5
                )  # Reduced range for stability
                zoom_factor = 1.0 + zoom_delta

                # Ensure zoom factor is reasonable
                zoom_factor = max(0.5, min(2.0, zoom_factor))

                self.scale(zoom_factor, zoom_factor)

                if (
                    hasattr(config, "current_photo_viewer")
                    and config.current_photo_viewer
                ):
                    config.current_photo_viewer.request_debounced_high_res_update(
                        force_update=True
                    )
                return True

            elif typ == QtCore.Qt.NativeGestureType.SwipeNativeGesture:
                print(f"other gesture type: {typ}")
            if typ == QtCore.Qt.NativeGestureType.EndNativeGesture:
                print(f"ending gesture {-1 if self.zoomValue < 0 else 1}")
            return True

        if isinstance(event, QtWidgets.QWidgetItem):
            # need to skip this event it will cause errors.
            return True

        if event.type() == QtCore.QEvent.Type.MouseButtonPress:
            # to draw the scale bar
            logger.info("press event at PhotoViewer")
            if self.scaleBarDraw_STATE == True:
                self.scaleBarPlaceFirstPoint(
                    self.mapToScene(event.position().toPoint())
                )
            # if event.type() == QtCore.QEvent.Type.MouseButtonPress:
            if self.rm_Masks_STATE == True:
                logger.info("masks state true")
                # remote masks tool
                self.rm_Masks_tool_draw = True
                self.DeleteAllMasksUnderMouse(event.position())
                return super(PhotoViewer, self).eventFilter(source, event)
            if self.add_mask_btn_state == True:
                logger.info("add_mask_btn_state true")
                if self.during_drawing == False:
                    if self.POLYGON_MODIFY_MODE == None:
                        if len(self.polyPreviousSelectedItems) != 0:
                            circlPainter = self.getPainterPathCircle(
                                0, QtCore.QPoint(0, 0)
                            )
                            self._scene.setSelectionArea(circlPainter)
                            self.polyPreviousSelectedItems = []
                            return super().eventFilter(source, event)
            if event.buttons() == QtCore.Qt.MouseButton.LeftButton:
                if self.ML_brush_tool_object_state is True:
                    if self.brushMask_STATE:
                        logger.info(
                            "ML_brush_tool_object_state true and brushMask_STATE"
                        )
                        self.ML_brush_tool_draw_is_active = True
                        self.brushMask_DuringDrawing = True

        if event.type() == QtCore.QEvent.Type.HoverEnter:
            if self.aa_tool_draw:
                if self.h_guide_magic_tool not in self._scene.items():
                    self._scene.addItem(self.h_guide_magic_tool)
                    self._scene.addItem(self.v_guide_magic_tool)
            if self.mgcClick_STATE == True:
                logger.info("magic click state truwe!")
                self.postoscene = self.mapToScene(event.position().toPoint()).toPoint()
                if self.magic_brush_cursor:
                    if self.magic_brush_cursor in self._scene.items():
                        self.magic_brush_cursor.show()

                    else:
                        posNow = self.mapToScene(event.position().toPoint()).toPoint()
                        self.magic_brush_cursor = mgcClick_cursor_cls(
                            posNow.x(), posNow.y(), self.mgcClickWidth
                        )
                        self._scene.addItem(self.magic_brush_cursor)
                else:
                    posNow = self.mapToScene(event.position().toPoint()).toPoint()
                    self.magic_brush_cursor = mgcClick_cursor_cls(
                        posNow.x(), posNow.y(), self.mgcClickWidth
                    )
                    self.magic_brush_cursor.show()
                    self._scene.addItem(self.magic_brush_cursor)

        if event.type() == QtCore.QEvent.Type.HoverLeave:
            if self.mgcClick_STATE is True or self.mgcBrushT is True:
                if self.magic_brush_cursor:
                    self._scene.removeItem(self.magic_brush_cursor)
            if self.aa_tool_draw:
                if self.h_guide_magic_tool in self._scene.items():
                    self._scene.removeItem(self.h_guide_magic_tool)
                    self._scene.removeItem(self.v_guide_magic_tool)
        if event.type() == QtCore.QEvent.Type.HoverMove:
            if self.mgcClick_STATE or self.MAGIC_BRUSH_STATE:
                posNow = self.mapToScene(event.position().toPoint())
                if not self.magic_brush_cursor:
                    # self.postoscene = self.mapToScene(event.position().toPoint() ).toPoint()
                    if self.MAGIC_BRUSH_STATE:
                        self.magic_brush_cursor = mgcClick_cursor_cls(
                            posNow.x(),
                            posNow.y(),
                            self.magic_brush_radious,
                            mode="circle",
                        )
                    elif self.mgcClick_STATE:
                        self.magic_brush_cursor = mgcClick_cursor_cls(
                            posNow.x(), posNow.y(), self.mgcClickWidth, mode="box"
                        )
                    # self._scene.addItem(self.magic_brush_cursor)
                if self.magic_brush_cursor not in self._scene.items():
                    self._scene.addItem(self.magic_brush_cursor)

                self.magic_brush_cursor.moveToC(posNow.x(), posNow.y())
                # self.magic_brush_cursor.updateSize(self.QuickTools.brushSizeSpinBoxGrabCut.value())
            if self.aa_tool_draw == True:
                if self.buttonPress == True:
                    if (
                        self.i_am_drawing_state_bbox == False
                        and self.during_drawing == False
                        and self.aa_review_state == True
                    ):

                        logger.debug("aa_tool_draw final is true")

                        """
                        Here I need to activate:
                        if on click inside, add to mask and recompute
                        if outside then exit aa_review_state
                        if normal pos is inside the normal pos of the box then draw
                        """
                        # if self.i_am_drawing_state_bbox == False and self.during_drawing == False and self.aa_review_state == True:
                        self.aa_review_state_decider(
                            self.mapToScene(event.position().toPoint()).toPoint()
                        )
                        return super().eventFilter(source, event)

        if event.type() == QtCore.QEvent.Type.MouseButtonPress:
            self.postoscene = self.mapToScene(event.position().toPoint()).toPoint()
            if self.aa_review_state == True:
                self.global_pos_x = self.postoscene.position().x()
                self.global_pos_y = self.postoscene.position().y()

        if event.type() == QtCore.QEvent.Type.MouseButtonPress:
            if event.buttons() == QtCore.Qt.MouseButton.LeftButton:
                self.dragPos = event.globalPosition()
                if self.SelectionStateRegions == True:
                    self.SelectionStateRegions = False
                    self.MainWindow.SelectedMaskDialog.hide()

        if (
            event.type() == QtCore.QEvent.Type.MouseButtonPress
            and event.buttons() == QtCore.Qt.MouseButton.LeftButton
            and self._photo.isUnderMouse()
        ):
            if self.MAGIC_BRUSH_STATE == True:
                if self.MAGIC_BRUSH_DURING_DRAWING == False:
                    self.magic_brush_pos_a = self.mapToScene(event.position().toPoint())
                    print("at press with radius at ", self.magic_brush_radious)
                    circlPainter = self.getPainterPathCircle(
                        self.magic_brush_radious, self.magic_brush_pos_a
                    )
                    self._scene.setSelectionArea(circlPainter)
                    self.magic_brush_points_set_A = self._scene.selectedItems()
                    self.MAGIC_BRUSH_DURING_DRAWING = True
                    self.mgcBrushT_fallOff = []

                    return super(PhotoViewer, self).eventFilter(source, event)

        if (
            event.type() == QtCore.QEvent.Type.MouseButtonPress
            and event.buttons() == QtCore.Qt.MouseButton.LeftButton
            and self._photo.isUnderMouse()
        ):
            self.leftMouseBtn_autoRepeat = True
            if self.ui_tool_selection.selected_button == "CELL_SPLIT_SEED":
                self.placeCELL_SPLIT_SEED_point(
                    self.mapToScene(event.position().toPoint())
                )
                self.CELL_SPLIT_DRAWING = True
                logger.info("button press!! CELL SPLIT")

            if self.ui_tool_selection.selected_button == "skeleton grabcut":
                if self.SkGb_STATE == True:
                    logger.info("self.SkGb_STATE is True")
                    self.placeSkGbAddPoint(self.mapToScene(event.position().toPoint()))
            # and self.MainWindow.DH.masks_state[self.MainWindow.current_imagenumber] == True :
            if self.ui_tool_selection.selected_button == "selection":
                self.global_pos_x = self.MainWindow.pos().x() + 0
                self.global_pos_y = self.MainWindow.pos().y()
                # self.selected_mask_under_mouse(self.mapToScene(event.position().toPoint() ).toPoint(), self.DH.master_mask_list)
            elif self.ui_tool_selection.selected_button == "selection":
                self.selected_mask = -1
                self.final_mask_number = -1

            if self.pop_up_tool_choosing_state == True:
                self.pop_up_tool_choosing_state = False
                self.setDragMode(QtWidgets.QGraphicsView.DragMode.NoDrag)
                self.update_tool()
                print("stops")

        """
        Draw tool auto
        """

        if self.aa_tool_draw == True:
            if (
                event.type() == QtCore.QEvent.Type.MouseButtonPress
                or event.type() == QtCore.QEvent.Type.MouseMove
            ) and event.buttons() == QtCore.Qt.MouseButton.LeftButton:
                if (
                    self.i_am_drawing_state_bbox == False
                    and self.during_drawing == False
                    and self.aa_review_state == True
                ):
                    """
                    Here I need to activate:
                    if on click inside, add to mask and recompute
                    if outside then exit aa_review_state
                    if normal pos is inside the normal pos of the box then draw
                    """
                    # if self.i_am_drawing_state_bbox == False and self.during_drawing == False and self.aa_review_state == True:
                    return True

        if (
            event.type() == QtCore.QEvent.Type.MouseButtonPress
            and self.ui_tool_selection.selected_button == "polygon"
            and self.hasPhoto() == True
            and self.dragMode() != QtWidgets.QGraphicsView.DragMode.ScrollHandDrag
        ):
            if event.buttons() == QtCore.Qt.MouseButton.LeftButton:
                print("its left buttons!")
                self.draw_polygon(self.mapToScene(event.position().toPoint()).toPoint())
                return super(PhotoViewer, self).eventFilter(source, event)

        if (
            event.type() == QtCore.QEvent.Type.MouseButtonPress
            and self.ui_tool_selection.selected_button == "lasso"
            and self.hasPhoto()
            and self.pop_up_tool_choosing_state != True
        ):
            # delete mask
            if (
                self.MainWindow.DH.masks_state[self.MainWindow.current_imagenumber]
                == True
                or self.MainWindow.DH.masks_state_usr[
                    self.MainWindow.current_imagenumber
                ]
                == True
            ):
                if self._photo.isUnderMouse():
                    if (
                        self.mask_under_mouse(
                            self.mapToScene(event.position().toPoint()).toPoint(),
                            self.MainWindow.DH.master_mask_list,
                        )
                        == True
                        and self.MainWindow.selection_state == False
                    ):
                        pass
                    else:
                        self.MainWindow.selected_mask = -1

                        self.MainWindow.final_mask_number = -1
            return False

        if event.type() == QtCore.QEvent.Type.MouseButtonPress:
            if (
                event.button() == QtCore.Qt.MouseButton.LeftButton
                and self.ui_tool_selection.selected_button == "auto"
            ):
                if self.hasPhoto():
                    if self.during_drawing_bbox is True:
                        if len(self._scene.selectedItems()) == 0:
                            self.draw_bounding_box_stop_THREADED(
                                self.mapToScene(event.position().toPoint()).toPoint()
                            )
                            self.completeDrawing_Bounding_Box()
                    elif len(self._scene.selectedItems()) == 0:
                        # if control modifier is pressed, ignore, as we are adjusting
                        # the prompt with points
                        if (
                            event.modifiers()
                            & QtCore.Qt.KeyboardModifier.ControlModifier
                        ):
                            return super().eventFilter(source, event)
                        # bounding box beggins process by setting init points x,y and allows for while to start
                        self.auto_annotate_tool_start(
                            self.mapToScene(event.position().toPoint()).toPoint()
                        )
                        self.MainWindow.selected_mask -= 1
        return super().eventFilter(source, event)

    def combinePolygons(self, pol1, pol2):
        myImageShape = (
            self.MainWindow.DH.BLobj.groups["default"]
            .conds[self.MainWindow.DH.BLobj.get_current_condition()]
            .getImage(self.MainWindow.current_imagenumber)
            .shape
        )
        # create empty images
        pol1Image = np.zeros(
            (myImageShape.shape[0], myImageShape.shape[1]), dtype=np.uint8
        )
        pol2Image = pol1Image.copy()

        pol1mask = skimage.draw.polygon2mask(
            (pol1Image.shape[0], pol1Image.shape[1]), np.asarray(pol1, dtype=np.uint16)
        )
        pol2mask = skimage.draw.polygon2mask(
            (pol2Image.shape[0], pol2Image.shape[1]), np.asarray(pol2, dtype=np.uint16)
        )
        FinalMask = pol1mask + pol2mask
        listAllMasks = []
        contours = skimage.measure.find_contours(FinalMask, 0.85)
        for i in range(len(contours)):
            appr_hand = skimage.measure.approximate_polygon(
                np.asarray(contours[i]), tolerance=0.4
            ).astype(np.uint16)
            listAllMasks.append(
                QtGui.QPolygonF([QtCore.QPointF(p[1], p[0]) for p in appr_hand])
            )

        return listAllMasks

    def placeCELL_SPLIT_SEED_point(self, pos):
        """
        we place the first point of the CELL_SPLIT_STATE
        """
        self.CELL_SPLIT_SPOTS.append((pos.x(), pos.y()))

        itemDotSplitW = QtWidgets.QGraphicsEllipseItem(
            pos.x() - self.getML_brush_tool_draw_brush_size(),
            pos.y() - self.getML_brush_tool_draw_brush_size(),
            self.getML_brush_tool_draw_brush_size() * 3.0,
            self.getML_brush_tool_draw_brush_size() * 3.0,
        )
        pen = QtGui.QPen(QtCore.Qt.GlobalColor.white)
        pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
        itemDotSplitW.setBrush(
            QtGui.QBrush(QtCore.Qt.GlobalColor.green, QtCore.Qt.BrushStyle.SolidPattern)
        )
        itemDotSplitW.setPen(pen)
        self._scene.addItem(itemDotSplitW)
        itemDotSplitR = QtWidgets.QGraphicsEllipseItem(
            pos.x() - self.getML_brush_tool_draw_brush_size(),
            pos.y() - self.getML_brush_tool_draw_brush_size(),
            self.getML_brush_tool_draw_brush_size() * 2.0,
            self.getML_brush_tool_draw_brush_size() * 2.0,
        )
        pen = QtGui.QPen(QtCore.Qt.GlobalColor.red)
        pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
        itemDotSplitR.setBrush(
            QtGui.QBrush(QtCore.Qt.GlobalColor.green, QtCore.Qt.BrushStyle.SolidPattern)
        )
        itemDotSplitR.setPen(pen)
        self._scene.addItem(itemDotSplitR)
        self.sceneCELL_SPLIT_ITEMS.append(itemDotSplitR)

    def end_CELL_SPLIT_SEED(self, pos):
        raise NotImplementedError

    def placeSkGbAddPoint(self, pos):
        """
        we place the first point of the poly line
        """
        print("def placeSkGbAddPoint")

        if len(self.SkGb_points) != 0:
            pen_width = 3
            # self.QuickTools.spinBoxOpacitySkeletonGB.value(),
            pen = QtGui.QPen(QtCore.Qt.GlobalColor.red, 0.3)
            pen.setWidth(pen_width)
            pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
            pen.setStyle(QtCore.Qt.PenStyle.DashLine)
            # add the line between two points
            line = QtWidgets.QGraphicsLineItem(
                QtCore.QLineF(
                    self.SkGb_points[-1][0], self.SkGb_points[-1][1], pos.x(), pos.y()
                )
            )
            # myPen = self.MainWindow.ColorPrefsViewer.getColorSkGc()

            # myPen.setWidth(self.QuickTools.spinBoxradiusSkeletonGB.value())
            line.setPen(pen)
            # self.SkBG_allLineScene.append(line)
            # self._scene.addItem(line)

        self.SkGb_points.append([pos.x(), pos.y()])
        self.SkGb_during_drawing = True

    def SkGbWhileDrawing(self, pos):
        """
        this runs continiusly connected the last pressed point to current position
        """
        myPen = self.MainWindow.ColorPrefsViewer.getColorSkGc()
        myPen.setWidth(self.QuickTools.spinBoxradiusSkeletonGB.value())
        try:
            self._scene.removeItem(self.SkGb_whileLine)
        except:
            print("error")
            pass

        qpp = QtGui.QPainterPath()
        points = self.SkGb_points.copy()
        points.append([pos.x(), pos.y()])

        qpp.addPolygon(QtGui.QPolygonF([QtCore.QPointF(p[0], p[1]) for p in points]))
        self.SkGb_whileLine = QtWidgets.QGraphicsPathItem(qpp)
        self.SkGb_whileLine.setPen(myPen)
        self._scene.addItem(self.SkGb_whileLine)
        # self.SkGb_whileLine = QtWidgets.QGraphicsLineItem(QtCore.QLineF(self.SkGb_points[-1][0],\
        #     self.SkGb_points[-1][1] , pos.x(),pos.y() ))
        # self.SkGb_whileLine.setPen(myPen)
        # self._scene.addItem(self.SkGb_whileLine)

    def placeSkGbFinish(self, pos, COMPLETE=True):
        """
        we end the polyline, either by completing it or deleting it
        """
        from celer_sight_ai import config

        raise NotImplementedError
        import cv2
        import skimage

        print("def placeSkGbFinish")
        from celer_sight_ai.gui.Utilities.QitemTools import (
            drawThickLine,
            skeletonGrabCut,
        )

        if COMPLETE == True:
            self.SkGb_points.append([pos.x(), pos.y()])
            self.SkGb_during_drawing = False
            imageDrawn = drawThickLine(
                self.SkGb_points,
                self.MainWindow.DH.BLobj.groups["default"]
                .conds[self.MainWindow.DH.BLobj.get_current_condition()]
                .getImage(self.MainWindow.current_imagenumber),
                int(self.QuickTools.spinBoxradiusSkeletonGB.value() * 0.66),
            )
            imageDrawnSkeleton = drawThickLine(
                self.SkGb_points,
                self.MainWindow.DH.BLobj.groups["default"]
                .conds[self.MainWindow.DH.BLobj.get_current_condition()]
                .getImage(self.MainWindow.current_imagenumber),
                int(self.QuickTools.spinBoxradiusSkeletonGB.value() * 0.07),
            )
            finalMask = skeletonGrabCut(
                self.MainWindow.DH.BLobj.groups["default"]
                .conds[self.MainWindow.DH.BLobj.get_current_condition()]
                .getImage(self.MainWindow.current_imagenumber),
                imageDrawn,
                imageDrawnSkeleton,
            )
            finalMask = finalMask.astype(bool)
            if np.count_nonzero(finalMask) <= 4:
                return
            contours = skimage.measure.find_contours(
                finalMask.astype(np.uint8).copy(), 0.8
            )
            appr_hand = skimage.measure.approximate_polygon(
                np.asarray(contours[0]), tolerance=2
            )
            QpointPolygonMC = QtGui.QPolygonF(
                [QtCore.QPointF(p[1], p[0]) for p in appr_hand]
            )

            from celer_sight_ai import config

            config.global_signals.create_annotation_object_signal.emit(
                [
                    self.MainWindow.current_imagenumber,
                    self.MainWindow.DH.BLobj.get_current_condition(),
                    QpointPolygonMC,
                ]
            )
            self.MainWindow.selected_mask = (
                len(
                    self.MainWindow.DH.BLobj.groups["default"]
                    .conds[self.MainWindow.DH.BLobj.get_current_condition()]
                    .images[self.MainWindow.current_imagenumber]
                    .masks
                )
                - 1
            )  # last added mask
            self.SkGb_points = []

            try:
                self._scene.removeItem(self.SkGb_whileLine)
            except:
                print("error")
                pass
            # self.MainWindow.load_main_scene(self.MainWindow.current_imagenumber)
        else:
            self.SkGb_points = []
            self.SkGb_during_drawing = False

            try:
                self._scene.removeItem(self.SkGb_whileLine)
            except:
                print("error")
                pass

    def DeleteAllMasksUnderMouse(self, pos):
        for item in self._scene.items():
            if type(item) == PolygonAnnotation:
                if item.isUnderMouse():
                    item.DeleteMask()
                    return

    def clearAllMasksUnderMouse(self, pos):
        self.setFlag(QtWidgets.QGraphicsItem.GraphicsItemFlag.ItemUsesExtendedStyleOption, True)
        self.setFlag(QtWidgets.QGraphicsItem.GraphicsItemFlag.ItemClipsToShape, False)  # Disable for speed
        self.setCacheMode(QtWidgets.QGraphicsItem.CacheMode.ItemCoordinateCache)
        
        # Disable hover events completely
        self.setAcceptHoverEvents(False)

    def getPen(self, ForMask=False, class_id=None):
        """
        if we has assigned a region to the masks then choose that, otherwise take from the settings quick tools
        """
        color = None
        if class_id:
            color = self.Main.custom_class_list_widget.classes[class_id].color
            if not isinstance(color, type(None)):
                color = QtGui.QColor(*color)
        else:
            color = (
                self.Main.pg1_settings_all_masks_color_button.palette().button().color()
            )
        if not color:
            # generate one temporarily
            color = QtGui.QColor([0, 255, 0])
        pen = QtGui.QPen(color)
        pen.setWidth(self.Main.viewer.QuickTools.lineWidthSpinBoxPolygonTool.value())
        pen.setCapStyle(self.MyStyles[self.CurrentPenCapStyle])
        pen.setStyle(self.MyStyles[self.CurrentPenStyle])
        return pen

    def getColorSkGc(self):
        pen = QtGui.QPen(QtGui.QColor(0, 0, 255, 70))
        pen.setWidth(2)
        pen.setCapStyle(self.MyStyles[self.CurrentPenCapStyle])
        pen.setStyle(self.MyStyles[self.CurrentPenStyle])
        return pen

    def getBrush(self, class_id=None):
        if class_id:
            Color = self.Main.get_mask_color_from_class(class_id)
        else:
            Color = self.GetColorSelected()
        brush = QtGui.QBrush(
            QtGui.QColor(Color[0], Color[1], Color[2], self.FillerAlpha)
        )
        return brush

    def CreatePen(self, viewer):
        """
        Creates a pen with the appropriate styles
        """
        pen = QtGui.QPen(self.SelectedColor)
        pen.setWidth(self.MaskWidth)
        pen.setCapStyle(self.MyStyles[self.CurrentPenCapStyle])
        pen.setStyle(self.MyStyles[self.CurrentPenStyle])
        viewer.setPen(pen)

    def FillRect(self, painter=None, style=None, widget=None):
        painter.fillRect(self.scene_rect, self._brush)

    def GetColorNotSelected(self):
        return GetRGB_FromHex(self.SelectedColor.name()) / self.NonSelectedColorDivider

    def GetColorSelected(self):
        return np.asarray(GetRGB_FromHex(self.NotSelectedMaskColor.name()))


class ImagePreviewGraphicsView(QtWidgets.QGraphicsView):

    def _apply_ultra_fast_styling(self):
        """Simplified styling for ultra-large polygons"""
        