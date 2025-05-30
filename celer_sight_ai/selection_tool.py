import logging

import numpy as np
import skimage
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtCore import Qt, pyqtSlot

from celer_sight_ai import config

logger = logging.getLogger(__name__)
try:
    from skimage.draw import circle, circle_perimeter_aa
except Exception as e:
    logger.error(e)
    from skimage.draw import circle_perimeter as circle


class PhotoViewer_test(QtWidgets.QGraphicsView):
    photoClicked = QtCore.pyqtSignal(QtCore.QPoint)
    object_signal = QtCore.pyqtSignal()

    def __init__(self, parent, Ui_MainWindow):
        super().__init__(parent)
        from celer_sight_ai.gui.custom_widgets.viewer.scene import BackgroundGraphicsItem

        self.Ui_MainWindow = Ui_MainWindow

        self.i_am_drawing_state_bbox = False
        self.i_am_drawing_state = False
        self.add_mask_btn_state = False
        self.Ui_MainWindow.main_viewer_state = False
        self.selection_state = False  # weather or not we can aselect a mask
        self.Ui_MainWindow = self.Ui_MainWindow
        # self.Ui_MainWindow.drop_urls = self.object_signal

        self._zoom = 0
        self._empty = True
        self._scene = QtWidgets.QGraphicsScene(self)
        self._photo = BackgroundGraphicsItem()
        self._photo.setZValue(config.Z_VALUE_BACKGROUND_IMAGE)
        self._scene.addItem(self._photo)
        self.painter = QtGui.QPainter()
        self._brush = QtGui.QBrush(
            QtGui.QColor(255, 170, 255), QtCore.Qt.BrushStyle.SolidPattern
        )
        self.painter.setPen(QtGui.QPen(Qt.green, 5, Qt.SolidLine))

        self.painter.setBrush(QtGui.QBrush(Qt.green, Qt.SolidPattern))

        self.painter.begin(self)
        self.pen = QtGui.QPen(QtGui.QColor(46, 84, 255))  # line width and color
        self.pen.setWidth(5)
        self.pen.setCapStyle(Qt.RoundCap)

        self.setScene(self._scene)
        self.setMouseTracking(True)
        self.setFocusPolicy(QtCore.Qt.FocusPolicy.ClickFocus)
        self.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.setObjectName("graphicsView_main")
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setBackgroundBrush(
            QtGui.QBrush(QtGui.QColor(245, 45, 45), QtCore.Qt.BrushStyle.SolidPattern)
        )
        self.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)

    def dragMoveEvent(self, event):
        pass

    def dragEnterEvent(self, event):
        if event.mimeData().hasText():
            event.setAccepted(True)
            logger.info("ok text")
            self.dragOver = True
            self.update()

            self.dragOver = True
            self.update()

    def dropEvent(self, event):
        import os

        pos = event.position()
        # event.acceptProposedAction()
        if event.mimeData().urls():
            event.acceptProposedAction()
            self.self.Ui_MainWindow.urls_droped = []
            # self.Ui_MainWindow.add_buttons_drop(self,MainWindow,0,added_urls = event.mimeData().urls() )
            for url in event.mimeData().urls():
                # .toLocal8Bit().data()

                # logger.info(path)
                if os.path.isfile(url.toLocalFile()):
                    self.Ui_MainWindow.urls_droped.append(url.toLocalFile())
                # do other stuff with path...event.setAccepted(True)
            self.self.Ui_MainWindow.drop_urls.emit()

    def hasPhoto(self):
        return not self._empty

    def fitImageInView(self, scale=True):
        self._zoom = 0
        rect = QtCore.QRectF(self._photo.pixmap().rect())
        if not rect.isNull():
            self.setSceneRect(rect)
            if self.hasPhoto():
                unity = self.transform().mapRect(QtCore.QRectF(0, 0, 1, 1))
                logger.info(unity.width())
                self.scale(1 / unity.width(), 1 / unity.height())
                viewrect = self.viewport().rect()
                scenerect = self.transform().mapRect(rect)
                logger.info(viewrect.width())
                logger.info(viewrect.height())
                logger.info(viewrect.width())
                logger.info(viewrect.height())
                factor = min(
                    viewrect.width() / scenerect.width(),
                    viewrect.height() / scenerect.height(),
                )
                self.scale(factor, factor)
            self._zoom = 0

    def setPhoto_and_mask(self, pixmap=None):
        self._zoom = 0
        logger.info(type(pixmap))
        # if pixmap and not pixmap.isNull():
        self._empty = False
        # self.setDragMode(QtWidgets.QGraphicsView.DragMode.ScrollHandDrag)
        self._photo.setPixmap(pixmap)
        # else:
        #     self._empty = True
        #     self.setDragMode(QtWidgets.QGraphicsView.DragMode.NoDrag)
        #     self._photo.setPixmap(QtGui.QPixmap())

    def setPhoto(self, pixmap=None, fit_in_view_state=True, rescaled_width=None):
        self._zoom = 0
        logger.info(type(pixmap))
        if pixmap and not pixmap == 0:
            self._empty = False
            self.setDragMode(QtWidgets.QGraphicsView.DragMode.NoDrag)
            # self.setDragMode(QtWidgets.QGraphicsView.DragMode.ScrollHandDrag)
            self._photo.setPixmap(pixmap)
            if rescaled_width:
                scale_factor = rescaled_width / pixmap.width()
                self._photo.setScale(scale_factor)
        else:
            self._empty = True
            self.setDragMode(QtWidgets.QGraphicsView.DragMode.NoDrag)
            self._photo.setPixmap(QtGui.QPixmap())

        if fit_in_view_state == True:
            self.fitImageInView()
        else:
            pass

    def wheelEvent(self, event):
        if self.hasPhoto():
            if event.angleDelta().y() > 0:
                factor = 1.15  # 1.25
                self._zoom += 1
            else:
                factor = 0.9  # 0.8
                self._zoom -= 1
            if self._zoom > 0:
                self.scale(factor, factor)
            elif self._zoom == 0:
                self.fitInView()
            else:
                self._zoom = 0

    def setDragMode_mc(self, mode):
        if mode == QtWidgets.QGraphicsView.DragMode.ScrollHandDrag:
            self.setDragMode(QtWidgets.QGraphicsView.DragMode.NoDrag)
        elif mode == QtWidgets.QGraphicsView.DragMode.NoDrag:
            self.setDragMode(QtWidgets.QGraphicsView.DragMode.ScrollHandDrag)

    def setBrush(self, brush):
        self._brush = brush
        self.update()

    def boundingRect(self):
        return self.rectF

    def paint(self, painter=None, style=None, widget=None):
        painter.fillRect(self.rectF, self._brush)

    def toggleDragMode(self):
        if not self.dragMode() == QtWidgets.QGraphicsView.DragMode.ScrollHandDrag:
            self.setDragMode_mc(QtWidgets.QGraphicsView.DragMode.NoDrag)
        else:
            self.setDragMode_mc(QtWidgets.QGraphicsView.DragMode.ScrollHandDrag)

    def mousePressEvent(self, event):
        if self._photo.isUnderMouse():
            self.photoClicked.emit(
                self.mapToScene(event.position().toPoint()).toPoint()
            )

    def mask_under_mouse(self, pos, mask):
        # logger.info(mask)
        if mask is None:
            logger.info("mask is nan")
            return False
        logger.info("mask is this at under mask")
        # mask = np.asarray(mask)
        logger.info(len(mask))
        logger.info(mask)
        if len(mask) == 1:
            if self.add_mask_btn_state == False:
                # try:
                if mask[0][pos.y(), pos.x()] == True:
                    self.delete_mask_in_master(pos)
                    self.load_main_scene(self.Ui_MainWindow.current_imagenumber)
                    return True
                else:
                    logger.info("nada")
                    return False
        if len(mask) != 0:
            logger.info("mask add btn satete = ", self.add_mask_btn_state)
            if self.add_mask_btn_state == False:
                # try:
                if mask[pos.y(), pos.x()] == True:
                    logger.info("mask under mouse when right clicked")
                    self.delete_mask_in_master(pos)
                    self.load_main_scene(self.Ui_MainWindow.current_imagenumber)
                    return True
                else:
                    logger.info("nada")
                    return False
                # except:
                #     return
        else:
            logger.info("nothing under mask i guess")
            return False

    def aa_review_state_decider(self, pos):
        tmp_x = pos.x()
        tmp_y = pos.y()
        if (
            self.aa_tool_bb_first_x > self.last_bbox_x
            and self.aa_tool_bb_first_y > self.last_bbox_y
        ):
            # if point is in bounds in x and y
            if (
                self.aa_tool_bb_first_x > tmp_x > self.last_bbox_x
                and self.aa_tool_bb_first_y > tmp_y > self.last_bbox_y
            ):
                # this means we are within bounds so we draw
                pass
            else:
                # we are not within bounds
                self.aa_review_state = False
                try:
                    self._scene.removeItem(self.bbox_drawing)
                except:
                    pass

        elif (
            self.aa_tool_bb_first_x > self.last_bbox_x
            and self.aa_tool_bb_first_y < self.last_bbox_y
        ):
            if (
                self.aa_tool_bb_first_x > tmp_x > self.last_bbox_x
                and self.aa_tool_bb_first_y < tmp_y < self.last_bbox_y
            ):
                # this means we are within bounds so we draw
                pass
            else:
                # we are not within bounds
                self.aa_review_state = False
                try:
                    self._scene.removeItem(self.bbox_drawing)
                except:
                    pass

        elif (
            self.aa_tool_bb_first_x < self.last_bbox_x
            and self.aa_tool_bb_first_y > self.last_bbox_y
        ):
            if (
                self.aa_tool_bb_first_x < tmp_x < self.last_bbox_x
                and self.aa_tool_bb_first_y > tmp_y > self.last_bbox_y
            ):
                # this means we are within bounds so we draw
                pass
            else:
                # we are not within bounds
                self.aa_review_state = False
                try:
                    self._scene.removeItem(self.bbox_drawing)
                except:
                    pass
        elif (
            self.aa_tool_bb_first_x < self.last_bbox_x
            and self.aa_tool_bb_first_y < self.last_bbox_y
        ):
            if (
                self.aa_tool_bb_first_x < tmp_x < self.last_bbox_x
                and self.aa_tool_bb_first_y < tmp_y < self.last_bbox_y
            ):
                # this means we are within bounds so we draw
                pass
            else:
                # we are not within bounds
                self.aa_review_state = False
                try:
                    self._scene.removeItem(self.bbox_drawing)
                except:
                    pass

    def auto_annotate_tool_start(self, pos):
        pen_width = 3
        if self.dragMode() == QtWidgets.QGraphicsView.DragMode.ScrollHandDrag:
            return
        if (pos.x() - 10) >= self.Ui_MainWindow.pixon_list_opencv[
            self.Ui_MainWindow.current_imagenumber
        ].shape[1] or (pos.y() - 10) >= self.Ui_MainWindow.pixon_list_opencv[
            self.Ui_MainWindow.current_imagenumber
        ].shape[
            0
        ]:
            return
        logger.info("STARTED")
        self.i_am_drawing_state_bbox = True
        self.during_drawing_bbox = False
        pen = QtGui.QPen(QtCore.Qt.GlobalColor.blue)
        pen.setWidth(pen_width)
        pen.setCapStyle(Qt.RoundCap)
        side = 20
        self.aa_tool_bb_first_x = pos.x()
        self.aa_tool_bb_first_y = pos.y()
        self.prevx = pos.x()
        self.prevy = pos.y()

    def auto_annotate_tool_while_draw(self, pos):
        pen_width = 3
        # if self.add_mask_btn_state == False:
        #     return

        if self.i_am_drawing_state_bbox == False:
            return
        if self.during_drawing_bbox == True:
            try:
                self._scene.removeItem(self.bbox_drawing)
            except:
                pass
        logger.info("while")
        pen = QtGui.QPen(QtCore.Qt.GlobalColor.white)
        # pen.setWidth(pen_width)
        pen.setCapStyle(Qt.RoundCap)
        pen.setCosmetic(True)
        side = 20
        self.bbox_drawing = QtWidgets.QGraphicsRectItem(
            QtCore.QRectF(
                self.aa_tool_bb_first_x,
                self.aa_tool_bb_first_y,
                pos.x() - self.aa_tool_bb_first_x,
                pos.y() - self.aa_tool_bb_first_y,
            )
        )
        self.bbox_drawing.setFlag(
            QtWidgets.QGraphicsItem.GraphicsItemFlag.ItemIgnoresTransformations, True
        )
        self.bbox_drawing.setPen(pen)
        self._scene.addItem(self.bbox_drawing)
        self.during_drawing_bbox = True
        self.last_bbox_x = pos.x()
        self.last_bbox_y = pos.y()

    def select_mask_clicked(self, pos):
        logger.info("Selecting clicked mask")
        # check with master mask

        self.Ui_MainWindow.master_mask_list = self.make_master_mask(
            self.Ui_MainWindow.unique_masks_tmp
        )

        if (
            self.Ui_MainWindow.masks_state[self.Ui_MainWindow.current_imagenumber]
            == False
            and self.Ui_MainWindow.masks_state_usr[
                self.Ui_MainWindow.current_imagenumber
            ]
            == False
        ):
            return False

        for i in range(len(self.Ui_MainWindow.master_mask_list)):
            # logger.info(self.Ui_MainWindow.master_mask_list)
            if self.Ui_MainWindow.master_mask_list[pos.y(), pos.x()][0] == True:
                return True
            else:
                return False

    def select_mask_in_master(self, pos):
        if (
            self.Ui_MainWindow.masks_state[self.Ui_MainWindow.current_imagenumber]
            == True
        ):
            combined_mask = self.combine_usr_predicted(
                self.Ui_MainWindow.all_masks[
                    self.Ui_MainWindow.current_imagenumber
                ].copy(),
                self.Ui_MainWindow.all_worm_mask_points_x[
                    self.Ui_MainWindow.current_imagenumber
                ].copy(),
                self.Ui_MainWindow.all_worm_mask_points_y[
                    self.Ui_MainWindow.current_imagenumber
                ].copy(),
            )
        else:
            combined_mask = self.combine_usr_predicted(
                [],
                self.Ui_MainWindow.all_worm_mask_points_x[
                    self.Ui_MainWindow.current_imagenumber
                ].copy(),
                self.Ui_MainWindow.all_worm_mask_points_y[
                    self.Ui_MainWindow.current_imagenumber
                ].copy(),
            )
        logger.info(len(combined_mask))
        for i in range(len(combined_mask)):
            logger.info("current is ", i)
            if (
                combined_mask[i][pos.y(), pos.x()] == True
            ):  # self.Ui_MainWindow.all_worm_mask_points_x
                if i >= len(
                    self.Ui_MainWindow.all_masks[self.Ui_MainWindow.current_imagenumber]
                ):
                    logger.info(
                        len(
                            self.Ui_MainWindow.all_worm_mask_points_x[
                                self.Ui_MainWindow.current_imagenumber
                            ]
                        )
                    )
                    self.selected_mask = i
                    logger.info(" going through ", i)
                    self.selected_mask_origin = (
                        "usr"  # if the mask we are looking at is from polygon
                    )
                    return
                else:
                    logger.info("not?")
                    self.selected_mask = i
                    self.selected_mask_origin = "mask"  # if its a bitwise mask
                    return

    def place_mask_locators_off(
        self,
        all_points_x,
        all_points_y,
        image_to_draw_on,
        small_image,
        offsetx=-3,
        offsety=-3,
    ):
        # locators:
        l_image = image_to_draw_on
        # Draws the

        for z in range(len(all_points_x)):
            x1 = all_points_x[z] + offsetx
            y1 = all_points_y[z] + offsety
            #
            # logger.info("x1 is ",x1)
            x2 = x1 + small_image.shape[1]
            y2 = y1 + small_image.shape[0]
            # logger.info("x2 is ",x2)
            alpha_s = small_image[:, :, 3] / 255.0
            alpha_l = 1.0 - alpha_s
            for c in range(0, 3):
                l_image[y1:y2, x1:x2, c] = (
                    alpha_s * small_image[:, :, c]
                    + alpha_l * l_image[y1:y2, x1:x2, c].copy()
                )
        return l_image

    def place_mask_locators_off_short(
        self,
        all_points_x,
        all_points_y,
        image_to_draw_on,
        small_image,
        offsetx=-6,
        offsety=-6,
    ):
        # locators:
        l_image = image_to_draw_on

        # logger.info("all points x", all_points_x{0} )

        x1 = all_points_x + offsetx
        y1 = all_points_y + offsety
        # logger.info("x1 is ",x1)
        x2 = x1 + small_image.shape[0]
        y2 = y1 + small_image.shape[1]
        # logger.info("x2 is ",x2)
        alpha_s = small_image[:, :, 3] / 255.0
        alpha_l = 1.0 - alpha_s
        for c in range(0, 3):
            l_image[y1:y2, x1:x2, c] = (
                alpha_s * small_image[:, :, c]
                + alpha_l * l_image[y1:y2, x1:x2, c].copy()
            )
        return l_image

    def draw_polygon(self, pos):
        pen_width = 3
        if self.add_mask_btn_state == False:
            return
        if self.selection_state == True:
            return
        if self.underMouse == False:
            return
        if self.dragMode() == QtWidgets.QGraphicsView.DragMode.ScrollHandDrag:
            return
        if (pos.x() - 10) >= self.Ui_MainWindow.pixon_list_opencv[
            self.Ui_MainWindow.current_imagenumber
        ].shape[1] or (pos.y() - 10) >= self.Ui_MainWindow.pixon_list_opencv[
            self.Ui_MainWindow.current_imagenumber
        ].shape[
            0
        ]:
            return
        logger.info(
            self.Ui_MainWindow.pixon_list_opencv[
                self.Ui_MainWindow.current_imagenumber
            ].shape[0]
        )
        logger.info(
            self.Ui_MainWindow.pixon_list_opencv[
                self.Ui_MainWindow.current_imagenumber
            ].shape[1]
        )

        logger.info("pos x is ", pos.x())
        logger.info("pos y is ", pos.y())
        logger.info("q graphics mode")
        self.i_am_drawing_state = True
        self.during_drawing = False
        pen = QtGui.QPen(QtCore.Qt.GlobalColor.blue)
        pen.setWidth(pen_width)
        pen.setCapStyle(Qt.RoundCap)
        side = 20

        # here on is the normal function
        if self.dragMode() == QtWidgets.QGraphicsView.DragMode.NoDrag:
            self.counter_tmp += 1
            self.temp_mask_to_use_Test_x.append(pos.x())
            self.temp_mask_to_use_Test_y.append(pos.y())
            logger.info(self.counter_tmp)
            # This is initiated right on the first click
            if self.counter_tmp == 1:
                self.list_py = []
                self.list_px = []
                self.first_x = pos.x()
                self.first_y = pos.y()
                self.prevx_first = pos.x()
                self.prevy_first = pos.y()

                self.img_for_mask_tmp = np.zeros(
                    (
                        self.Ui_MainWindow.pixon_list_opencv[
                            self.Ui_MainWindow.current_imagenumber
                        ].shape[0],
                        self.Ui_MainWindow.pixon_list_opencv[
                            self.Ui_MainWindow.current_imagenumber
                        ].shape[1],
                    ),
                    dtype=bool,
                )

                self.img_for_mask_tmp_prev = np.zeros(
                    (
                        self.Ui_MainWindow.pixon_list_opencv[
                            self.Ui_MainWindow.current_imagenumber
                        ].shape[0],
                        self.Ui_MainWindow.pixon_list_opencv[
                            self.Ui_MainWindow.current_imagenumber
                        ].shape[1],
                    ),
                    dtype=bool,
                )

                # Here we draw the first circle
                line_rr, line_cc, line_val = skimage.draw.circle_perimeter_aa(
                    pos.y(), pos.x(), 5
                )
                import time

                start = time.time()
                self.img_for_mask_tmp[line_rr, line_cc] = 1
                logger.info("total time took: ", start)
                img_for_mask_tmp_prev = self.img_for_mask_tmp

                # Here we draw lines
                if (
                    self.Ui_MainWindow.masks_state_usr[
                        self.Ui_MainWindow.current_imagenumber
                    ]
                    == True
                    or self.Ui_MainWindow.masks_state[
                        self.Ui_MainWindow.current_imagenumber
                    ]
                    == True
                ):
                    # draw mask
                    self.mask_image_tmp = self.apply_mask(
                        self.background_mask.copy(),
                        self.img_for_mask_tmp.astype(np.uint8),
                        self.worm_mask_points_x,
                        self.worm_mask_points_y,
                    )
                else:
                    self.mask_image_tmp = self.apply_mask(
                        self.Ui_MainWindow.pixon_list_opencv[
                            self.Ui_MainWindow.current_imagenumber
                        ].copy(),
                        self.img_for_mask_tmp.astype(np.uint8),
                        self.temp_mask_to_use_Test_x,
                        self.temp_mask_to_use_Test_y,
                    )
                self.mask_image_tmp_normal = self.mask_image_tmp.copy()

            # This is during the Second click
            if self.counter_tmp != 1:
                logger.info("placing_mask")
                self.line_drawing_1 = QtCore.QLineF(
                    self.prevx, self.prevy, pos.x(), pos.y()
                )
                self._scene.addLine(self.line_drawing_1, pen)
                self.img_for_mask_tmp = np.maximum(
                    self.img_for_mask_tmp, self.img_for_mask_tmp_prev
                )
                self.mask_image_tmp_prev = self.mask_image_tmp

            if self.counter_tmp > 3:
                # counter more than 3
                logger.info("counter more than 3")
                image_circle = np.zeros(
                    (
                        self.Ui_MainWindow.pixon_list_opencv[
                            self.Ui_MainWindow.current_imagenumber
                        ].shape[0]
                        + 30,
                        self.Ui_MainWindow.pixon_list_opencv[
                            self.Ui_MainWindow.current_imagenumber
                        ].shape[1]
                        + 30,
                    ),
                    dtype=bool,
                )
                rr_circle, cc_circle = circle(pos.y(), pos.x(), 10)

                image_circle[rr_circle, cc_circle] = True
                image_circle2 = image_circle.astype(bool)
                logger.info("works")

                if image_circle2[self.first_y, self.first_x] == True:
                    logger.info("mask finished")
                    # remove last element
                    self.temp_mask_to_use_Test_x = self.temp_mask_to_use_Test_x[:-1]
                    self.temp_mask_to_use_Test_y = self.temp_mask_to_use_Test_y[:-1]

                    rr, cc = skimage.draw.polygon(
                        self.temp_mask_to_use_Test_y, self.temp_mask_to_use_Test_x
                    )
                    self.img_for_mask_tmp[rr, cc] = True
                    self.worm_mask_points_x = self.temp_mask_to_use_Test_x
                    self.worm_mask_points_y = self.temp_mask_to_use_Test_y

                    if (
                        self.Ui_MainWindow.masks_state_usr[
                            self.Ui_MainWindow.current_imagenumber
                        ]
                        == True
                        or self.Ui_MainWindow.masks_state[
                            self.Ui_MainWindow.current_imagenumber
                        ]
                        == True
                    ):
                        self.mask_image_tmp = self.apply_mask(
                            self.background_mask.copy(),
                            self.img_for_mask_tmp.astype(np.uint8),
                            self.worm_mask_points_x,
                            self.worm_mask_points_y,
                        )

                    else:
                        self.mask_image_tmp = self.apply_mask(
                            self.Ui_MainWindow.pixon_list_opencv[
                                self.Ui_MainWindow.current_imagenumber
                            ].copy(),
                            self.img_for_mask_tmp.astype(np.uint8),
                            self.temp_mask_to_use_Test_x,
                            self.temp_mask_to_use_Test_y,
                        )

                        # self.mask_image_tmp = self.place_mask_locators_off(self.worm_mask_points_x[self.Ui_MainWindow.current_imagenumber],
                        # self.worm_mask_points_y[self.Ui_MainWindow.current_imagenumber],
                        # self.mask_image_tmp,
                        # self.circle_selection_image)

                        # self.mask_image_tmp = self.apply_mask(self.Ui_MainWindow.pixon_list_opencv[self.Ui_MainWindow.current_imagenumber].copy(),self.img_for_mask_tmp.astype(bool).astype(np.uint8) )

                        ###FIX THIS....
                        # logger.info(self.Ui_MainWindow.all_masks)
                    if (
                        self.Ui_MainWindow.masks_state_usr[
                            self.Ui_MainWindow.current_imagenumber
                        ]
                        == False
                    ):
                        self.Ui_MainWindow.all_worm_mask_points_x[
                            self.Ui_MainWindow.current_imagenumber
                        ] = []
                        self.Ui_MainWindow.all_worm_mask_points_y[
                            self.Ui_MainWindow.current_imagenumber
                        ] = []
                        self.Ui_MainWindow.masks_state_usr[
                            self.Ui_MainWindow.current_imagenumber
                        ] = True

                    self.mask_image_tmp = QtGui.QPixmap.fromImage(
                        QtGui.QImage(
                            self.mask_image_tmp,
                            self.mask_image_tmp.shape[1],
                            self.mask_image_tmp.shape[0],
                            QtGui.QImage.Format.Format_RGB888,
                        )
                    )

                    # self.viewer.setPhoto_and_mask(self.mask_image_tmp)

                    self.Ui_MainWindow.all_worm_mask_points_x[
                        self.Ui_MainWindow.current_imagenumber
                    ].append(self.worm_mask_points_x)
                    self.Ui_MainWindow.all_worm_mask_points_y[
                        self.Ui_MainWindow.current_imagenumber
                    ].append(self.worm_mask_points_y)

                    logger.info("pass")

                    # self.separate_masks()
                    self.counter_tmp = 0

                    self.temp_mask_to_use_Test_x = []
                    self.temp_mask_to_use_Test_y = []
                    # self.add_mask_btn_state = False
                    self.first_x = -1
                    self.first_y = -1
                    self.Ui_MainWindow.masks_state_usr[
                        self.Ui_MainWindow.current_imagenumber
                    ] = True
                    self.worm_mask_points_x = []
                    self.worm_mask_points_y = []
                    self.i_am_drawing_state = False
                    self.load_main_scene(self.Ui_MainWindow.current_imagenumber)
                    if (
                        self.Ui_MainWindow.masks_state[
                            self.Ui_MainWindow.current_imagenumber
                        ]
                        == True
                    ):
                        combined_mask = self.combine_usr_predicted(
                            self.Ui_MainWindow.all_masks[
                                self.Ui_MainWindow.current_imagenumber
                            ].copy(),
                            self.Ui_MainWindow.all_worm_mask_points_x[
                                self.Ui_MainWindow.current_imagenumber
                            ].copy(),
                            self.Ui_MainWindow.all_worm_mask_points_y[
                                self.Ui_MainWindow.current_imagenumber
                            ].copy(),
                        )
                    else:
                        combined_mask = self.combine_usr_predicted(
                            [],
                            self.Ui_MainWindow.all_worm_mask_points_x[
                                self.Ui_MainWindow.current_imagenumber
                            ].copy(),
                            self.Ui_MainWindow.all_worm_mask_points_y[
                                self.Ui_MainWindow.current_imagenumber
                            ].copy(),
                        )
                    self.make_master_mask(combined_mask)

            self.prevx = pos.x()
            self.prevy = pos.y()
            self.list_px.append(pos.x())
            self.list_py.append(pos.y())
        return

        # super(PhotoViewer_test, self).mousePressEvent(event)
