import sys

import os
from celer_sight_ai import config
from typing import List, Dict, Tuple, Any, Union, Optional

if config.is_executable:
    sys.path.append([str(os.environ["CELER_SIGHT_AI_HOME"])])
from PyQt6 import QtWidgets, QtCore, QtGui
import random

# from celer_sight_ai.QtAssets.Utilities.scene import PolygonAnnotation
# import QtAssets.Utilities.scene as scene

import logging
import numpy as np

logger = logging.getLogger(__name__)


class MyShape(QtWidgets.QGraphicsPolygonItem):
    itemMoveSignal = QtCore.pyqtSignal(str, int)

    def __init__(self, MainWindow=None, ID=None):  # HERE
        super(MyShape, self).__init__()
        # self.Type = self.UserType + 1
        self.ID = ID
        self.Condition = ""
        self.MainWindow = MainWindow
        self.m_boxItem = QtGui.QPolygonF()
        self.m_boxItem.append(QtCore.QPointF(0, 0))
        self.m_boxItem.append(QtCore.QPointF(30, 0))
        self.m_boxItem.append(QtCore.QPointF(30, 30))
        self.m_boxItem.append(QtCore.QPointF(0, 30))
        self.setPolygon(self.m_boxItem)
        MainWindow.myPolDict["control"].append(self.m_boxItem)  # HERE
        self.color = QtGui.QColor(
            random.randint(0, 256), random.randint(0, 256), random.randint(0, 256)
        )
        self.brush = QtGui.QBrush(self.color)
        self.setBrush(self.brush)

        self.setFlag(QtWidgets.QGraphicsItem.GraphicsItemFlag.ItemIsMovable)
        self.setFlag(QtWidgets.QGraphicsItem.GraphicsItemFlag.ItemIsSelectable)

    def mouseReleaseEvent(self, value):
        logger.info("mouse release")

        polListTmp = []
        for point in self.polygon():
            polListTmp.append(QtCore.QPointF(self.mapToScene(point)))
        oldPolygon = self.polygon()
        self.MainWindow.myPolDict["control"][self.ID] = QtGui.QPolygonF(polListTmp)
        self.CurrentPolygon = QtGui.QPolygonF(polListTmp)
        self.setPolygon(self.CurrentPolygon)
        self.setPos(0, 0)
        for point in self.MainWindow.myPolDict["control"][self.ID]:
            logger.info(point)
        # self.itemMoveSignal.emit(self.Condition, self.ID)
        self.ShapeMoved(oldPolygon, self.CurrentPolygon)

        return super(MyShape, self).mouseReleaseEvent(value)

    def ShapeMoved(self, oldPolygon, CurrentPolygon):
        move = MoveCommand(
            self, oldPolygon, CurrentPolygon, self.MainWindow
        )  # item is polygon list
        self.MainWindow.undoStack.push(move)


class MyScene(QtWidgets.QGraphicsScene):
    itemMoveSignal = QtCore.pyqtSignal(MyShape, QtCore.QPointF)

    def __init__(self):
        super(MyScene, self).__init__()
        self.m_Item = None
        self.m_oldPos = QtCore.QPointF()
        # self.pointsDict = dict()

    def mousePressEvent(self, event):
        mousePos = QtCore.QPointF(
            event.buttonDownScenePos(QtCore.Qt.MouseButton.LeftButton).x(),
            event.buttonDownScenePos(QtCore.Qt.MouseButton.LeftButton).y(),
        )

        itemList = []
        itemList = self.items(mousePos)
        if len(itemList) > 0:
            self.m_Item = itemList[0]
            logger.info(self.m_Item)
        if (self.m_Item is not None) & (
            event.button() == QtCore.Qt.MouseButton.LeftButton
        ):
            self.m_oldPos = self.m_Item.pos()
            logger.info(self.m_oldPos, self.m_Item.pos())
            # self.pointsDict.
        super(MyScene, self).mousePressEvent(event)


class AddBitMapCommand(QtGui.QUndoCommand):
    def __init__(
        self,
        bitmap,
        MainWindow,
        image_uuid=None,
        class_id=None,
    ):  # HERE
        super(AddBitMapCommand, self).__init__()
        self.MainWindow = MainWindow
        logger.debug("AddBitMapCommand running")
        self.mask_type = "bitmap"
        self.setText("add item")
        self.condition = None
        self.mask_uuid = None  # id of the mask, passed on redo()
        self.bitmap_array = (
            bitmap  # original array for annotation that then gets converted to QPolygon
        )
        if self.condition == None:
            self.condition = self.MainWindow.DH.BLobj.get_current_condition()
        self.class_id = class_id
        self.image_uuid = image_uuid

    def redo(self) -> None:
        """
        the whole process of adding polygons is splited into 3 steps:
        - add the graphics polygon item to scene
        - add the polygon item to dicitonary
        - add the qbuttonwidget for the mask
        """
        # add mask the normal way
        logger.debug("redo running for bitmap")
        image_object = self.MainWindow.DH.BLobj.get_image_object_by_uuid(
            self.image_uuid
        )
        image_object.addMaskWithClass(
            self.bitmap_array,
            self.class_id,
            mask_type=self.mask_type,
        )

        # if current image is the same as the image we are adding mask to then add it to scene
        if self.image_object == self.MainWindow.DH.BLobj.get_current_image_object():
            # get the condition uuid
            image_uuid = image_object.unique_id
            config.global_signals.MaskToSceneSignal.emit(
                {
                    "image_uuid": image_uuid,
                    "mask_uuid": self.mask_uuid,
                    "mask_type": self.mask_type,
                }
            )
        # If inference is computed , then mark the image as modified and to be send to
        #  the server for further training.
        # if (
        #     self.MainWindow.DH.BLobj.groups["default"]
        #     .conds[self.condition]
        #     .images[self.imID]
        #     .computedInference
        #     == True
        # ):
        image_object = self.MainWindow.DH.BLobj.get_image_object_by_uuid(
            self.image_uuid
        )
        image_object.setUserModifiedAnnotation(True)
        self.MainWindow.viewer.updateMaskCountLabel()

    def undo(self):
        from celer_sight_ai.QtAssets.Utilities.scene import BitMapAnnotation

        # if current image is not the one that was modified, then load it
        if self.imID != self.MainWindow.current_imagenumber:
            self.MainWindow.loadImage(self.imID)
            QtWidgets.QApplication.processEvents()

        for someItem in self.MainWindow.viewer._scene.items():
            if type(someItem) == BitMapAnnotation:
                if someItem.PolRef == self.myQPol:
                    self.MainWindow.viewer._scene.removeItem(someItem)
        image_object = self.MainWindow.DH.BLobj.get_image_object_by_uuid(
            self.image_uuid
        )
        image_object.masks.pop()
        # self.shape.DeleteMask()
        self.MainWindow.viewer.updateMaskCountLabel()

    def getPosInDict(self, myList):  # HERE
        return len(myList) - 1


class AddPolygonCommand(QtGui.QUndoCommand):
    def __init__(
        self,
        QpolygonToAdd,
        MainWindow,
        treatment_uuid=None,
        image_uuid=None,
        class_id=None,
        mask_type=None,
        visibility=None,
        is_included_in_analysis=None,
        is_suggested=False,
        score=1.0,
        mask_uuid=None,
    ):  # HERE
        super(AddPolygonCommand, self).__init__()
        self.MainWindow = MainWindow
        # self.itemId = ItemId
        logger.debug("AddPolygonCommand running")
        self.mask_type = mask_type
        self.mask_uuid = None  # id of the mask, passed on redo()
        self.my_qpol_holes = []
        self.setText("add item")
        self.annotation_array = self.sanitize_polygon(
            QpolygonToAdd
        )  # original array for annotation that then gets converted to QPolygon
        self.provided_mask_uuid = mask_uuid
        self.treatment_uuid = treatment_uuid
        self.is_suggested = is_suggested
        self.score = score
        if self.treatment_uuid == None:
            self.treatment_uuid = self.MainWindow.DH.BLobj.get_current_condition_uuid()
        self.class_id = class_id
        self.image_uuid = image_uuid

    def check_if_over_or_under_full_mask_display_threshold(self):
        """
        Check all of the visible images on the scene, if the amount is more than
        the threshold for showing the full mask (text + polygon + center point) and its just 1
        over, send a signal to reload the masks (the value is config.extra_mask_items_threshold)
        """
        image_object = self.MainWindow.DH.BLobj.get_image_object_by_uuid(
            self.image_uuid
        )
        mask_amount = len(image_object.masks)
        if (mask_amount - config.extra_mask_items_threshold) == 1:
            logger.info("Over full mask display threshold, reloading scene")
            config.global_signals.load_main_scene_signal.emit()

    def sanitize_polygon(self, polygon_array):
        """
        Sanitize array by removing small objects etc..
        """
        sanitized_array = []
        for arr in polygon_array:
            if len(arr.shape) == 2 and arr.shape[0] >= 3:
                sanitized_array.append(arr)
        return sanitized_array

    def redo(self) -> None:
        """
        the whole process of adding polygons is splited into 3 steps:
        - add the graphics polygon item to scene
        - add the polygon item to dicitonary
        - add the qbuttonwidget for the mask
        """
        # add mask the normal way
        logger.info("redo running")
        treatment_object = self.MainWindow.DH.BLobj.get_condition_by_uuid(
            self.treatment_uuid
        )
        image_object = self.MainWindow.DH.BLobj.get_image_object_by_uuid(
            self.image_uuid
        )
        if self.provided_mask_uuid:
            self.mask_uuid = image_object.addMaskWithClass(
                self.annotation_array,
                class_id=self.class_id,
                unique_id=self.provided_mask_uuid,
                mask_type=self.mask_type,
                is_suggested=self.is_suggested,
                score=self.score,
            )
        else:
            self.mask_uuid = image_object.addMaskWithClass(
                self.annotation_array,
                class_id=self.class_id,
                mask_type=self.mask_type,
                is_suggested=self.is_suggested,
                score=self.score,
            )

        # if Img id and treatment and group are the same, then add to scene as well.
        if (
            image_object.unique_id
            == self.MainWindow.DH.BLobj.get_current_image_object().unique_id
        ):
            config.global_signals.MaskToSceneSignal.emit(
                {
                    "image_uuid": self.image_uuid,
                    "mask_uuid": self.mask_uuid,
                    "mask_type": self.mask_type,
                }
            )
        # this is a manual annotation, so always mark as corrected during analysis
        image_object.setUserModifiedAnnotation(True)
        self.MainWindow.viewer.updateMaskCountLabel()
        self.check_if_over_or_under_full_mask_display_threshold()

    def undo(self):
        from celer_sight_ai.QtAssets.Utilities.scene import PolygonAnnotation

        for someItem in self.MainWindow.viewer._scene.items():
            if type(someItem) == PolygonAnnotation:
                if someItem.unique_id == self.mask_uuid:
                    self.MainWindow.viewer._scene.removeItem(someItem)
                    # also remove all extra items
                    for item in someItem.poly_hole_scene_items:
                        self.MainWindow.viewer._scene.removeItem(item)
                    if someItem.center_point_graphics_item:
                        self.MainWindow.viewer._scene.removeItem(
                            someItem.center_point_graphics_item
                        )
                    if someItem.class_graphics_text_item:
                        self.MainWindow.viewer._scene.removeItem(
                            someItem.class_graphics_text_item
                        )
        image_object = self.MainWindow.DH.BLobj.get_image_object_by_uuid(
            self.image_uuid
        )
        image_object.masks.pop(-1)
        self.MainWindow.viewer.updateMaskCountLabel()

    def getPosInDict(self, myList):  # HERE
        return len(myList) - 1


class GripItemMoveCommand(QtGui.QUndoCommand):
    def __init__(
        self,
        polygon_item: QtWidgets.QGraphicsPathItem = None,
        grip_items_indexes: List = [],
        grip_new_items_pos: List = [],
        grip_old_items_pos: List = [],
        mask_uuid: str = None,
        condition_uuid: str = None,
        group_name: str = None,  # TODO: support this in the future
        MainWindow: QtWidgets.QMainWindow = None,
    ) -> None:
        super(GripItemMoveCommand, self).__init__()
        self.grip_items_indexes = grip_items_indexes
        self.grip_new_items_pos = grip_new_items_pos
        self.grip_old_items_pos = grip_old_items_pos
        self.mask_uuid = mask_uuid
        self.condition_uuid = condition_uuid
        self.MainWindow = MainWindow
        self.polygon_item = polygon_item

    def redo(self) -> None:
        # set the position to the new item pos
        # this way, during the first redo, the points are just left as is
        # However, in undo -> redo the points again take their expected positions
        # First, changet he polygon array items to the new positions
        try:
            for i, item in enumerate(
                zip(
                    self.grip_items_indexes,
                    self.grip_old_items_pos,
                    self.grip_new_items_pos,
                )
            ):
                # arr_pos -> [outer shape , hole 1 , hole 2 ....]
                # index pos -> idx within the shape ^
                arr_pos, idx_pos = self.polygon_item.get_modified_index(item[0])
                self.MainWindow.DH.BLobj.groups["default"].get_by_uuid(
                    self.condition_uuid
                ).images[self.MainWindow.current_imagenumber].get_by_uuid(
                    self.mask_uuid
                ).polygon_array[
                    arr_pos
                ][
                    idx_pos
                ] = item[
                    2
                ]
                # print(self.polygon_item.m_points)
                # print(item[0])
                # print(self.polygon_item.m_items)
                # Then adjust the scene items
                self.polygon_item.m_items[item[0]].setPos(
                    QtCore.QPointF(item[2][0], item[2][1])
                )
                # if current image is remote, update the server
                if (
                    self.MainWindow.DH.BLobj.groups["default"]
                    .get_by_uuid(self.condition_uuid)
                    .images[self.MainWindow.current_imagenumber]
                    .is_remote()
                ):
                    from celer_sight_ai import config

                    mask_obj = (
                        self.MainWindow.DH.BLobj.groups["default"]
                        .get_by_uuid(self.condition_uuid)
                        .images[self.MainWindow.current_imagenumber]
                        .get_by_uuid(self.mask_uuid)
                    )
                    class_name = self.MainWindow.custom_class_list_widget.classes[
                        mask_obj.class_id
                    ].text()

                    d = {
                        "annotation_uuid": self.mask_uuid,
                        "data": self.MainWindow.numpy_to_python(
                            mask_obj.get_array_for_storing()
                        ),
                        "category": class_name,
                        "supercategory": config.supercategory,
                        "audited": True,
                    }
                    config.global_signals.update_remote_annotation_signal.emit(d)
        except Exception as e:
            logger.error(f"Error updating remote annotation: {e}")

    def undo(self) -> None:
        # TODO this needs to be implemented / fixed
        return
        # for i, item in enumerate(
        #     zip(
        #         self.grip_items_indexes,
        #         self.grip_old_items_pos,
        #         self.grip_new_items_pos,
        #     )
        # ):
        #     # arr_pos -> [outer shape , hole 1 , hole 2 ....]
        #     # index pos -> idx within the shape ^
        #     arr_pos, idx_pos = self.polygon_item.get_modified_index(item[0])
        #     mask_object = self.MainWindow.DH.BLobj.get_mask_object_by_uuid(
        #         self.mask_uuid
        #     )
        #     if not mask_object:
        #         return
        #     mask_object.polygon_array[arr_pos, idx_pos] = item[1]
        #     # Then adjust the scene items
        #     self.polygon_item.grip_items[item[0]].move(QtCore.QPointF(item[1]))


class DeleteHoleCommand(QtGui.QUndoCommand):
    def __init__(
        self,
        hole_index,
        hole_graphics_item,
        mask_uuid,
        MainWindow,
        imID=None,
        condition=None,
        className=None,
    ):  # HERE
        super(DeleteHoleCommand, self).__init__()
        self.hole_index = hole_index
        self.hole_graphics_item = hole_graphics_item
        self.MainWindow = MainWindow
        self.condition = condition
        self.imID = imID
        self.mask_uuid = mask_uuid
        self.className = className
        self.hole_array = None

    def redo(self):
        # remove the array from the polygon_array and store it here to be instarted during undo
        self.hole_array = (
            self.MainWindow.DH.BLobj.groups["default"]
            .conds[self.condition]
            .images[self.imID]
            .get_by_uuid(self.mask_uuid)
            .polygon_array.pop(self.hole_index)
        )
        # remove the hole from the scene if it exists there
        if self.hole_graphics_item in self.MainWindow.viewer.scene().items():
            annotation_item = self.hole_graphics_item.annotation_item
            self.MainWindow.viewer.scene().removeItem(self.hole_graphics_item)
            QtWidgets.QApplication.processEvents()
            annotation_item.update_annotation()
            annotation_item.removeAllPoints()
            annotation_item.initPoints()

        # delete from remote if the session is remote
        if (
            self.MainWindow.DH.BLobj.groups["default"]
            .conds[self.condition]
            .images[self.imID]
            .is_remote()
        ):
            mask_obj = (
                self.MainWindow.DH.BLobj.groups["default"]
                .conds[self.condition]
                .images[self.imID]
                .get_by_uuid(self.mask_uuid)
            )
            d = {
                "image_uuid": self.MainWindow.DH.BLobj.groups["default"]
                .conds[self.condition]
                .images[self.imID]
                .unique_id,
                "annotation_uuid": self.mask_uuid,
                "data": self.MainWindow.numpy_to_python(
                    mask_obj.get_array_for_storing()
                ),
                "category": self.className,
                "supercategory": config.supercategory,
                "audited": True,
            }
            config.global_signals.update_remote_annotation_signal.emit(d)

    def undo(self):
        # insert the hole back to the polygon_array
        self.MainWindow.DH.BLobj.groups["default"].conds[self.condition].images[
            self.imID
        ].get_by_uuid(self.mask_uuid).polygon_array.insert(
            self.hole_index, self.hole_array
        )

        # add the hole back to the scene
        self.MainWindow.viewer.scene().addItem(self.hole_graphics_item)


class DeleteMaskCommand(QtGui.QUndoCommand):
    def __init__(
        self, mask_unique_id, MainWindow, treatment_uuid=None, class_id=None
    ):  # HERE
        super(DeleteMaskCommand, self).__init__()
        self.MainWindow = MainWindow
        # self.itemId = ItemId
        logger.info("DeletePolygonCommand running")

        self.setText("delete item")
        self.unique_id = mask_unique_id  # --> needs to be renamed to

        self.treatment_uuid = treatment_uuid
        if self.treatment_uuid == None:
            self.treatment_uuid = self.MainWindow.DH.BLobj.get_current_condition_uuid()
        self.class_id = class_id

        # find index of the mask to be removed
        self.previous_mask_object = self.MainWindow.DH.BLobj.get_mask_object_by_uuid(
            self.unique_id
        )
        # get the polygon to remove
        self.polygon_array = self.previous_mask_object.get_array()
        self.mask_items_removed = []
        self.mask_pos = None

    def redo(self):
        from celer_sight_ai.QtAssets.Utilities.scene import PolygonAnnotation

        logger.info("redo running")
        for someItem in self.MainWindow.viewer._scene.items():
            if type(someItem) == PolygonAnnotation:
                if someItem.unique_id == self.unique_id:
                    # remove any holes in the mask
                    for h in someItem.poly_hole_scene_items:
                        self.MainWindow.viewer._scene.removeItem(h)
                    self.MainWindow.viewer._scene.removeItem(someItem)

        mask_obj = self.previous_mask_object
        if not mask_obj:
            logger.error(f"Mask object with uuid {self.unique_id} not found")
            return
        self.mask_type = mask_obj.mask_type

        self.MainWindow.viewer.updateMaskCountLabel()
        image_object = self.MainWindow.DH.BLobj.get_image_object_by_uuid(
            mask_obj.image_uuid
        )
        if not image_object:
            logger.error(f"Image object with uuid {mask_obj.image_uuid} not found")
            return
        self.mask_items_removed = image_object.del_by_uuid(self.unique_id)

        if image_object.is_remote():
            config.client.delete_remote_annotation(
                {
                    "annotation_uuid": self.unique_id,
                    "supercategory": config.supercategory,
                    "image_uuid": image_object.unique_id,
                }
            )

    def undo(self):
        """
        the whole process of adding polygons is splited into 3 steps:
        - add the graphics polygon item to scene
        - add the polygon item to dicitonary
        - add the qbuttonwidget for the mask
        """
        from celer_sight_ai.QtAssets.Utilities.scene import PolygonAnnotation

        # get image uuid from the mask uuid
        mask_obj = self.previous_mask_object
        if not mask_obj:
            logger.error(f"Mask object with uuid {self.unique_id} not found")
            return
        image_uuid = mask_obj.image_uuid
        config.global_signals.create_annotation_object_signal.emit(
            {
                "treatment_uuid": self.treatment_uuid,
                "array": self.polygon_array,
                "group": "default",
                "image_uuid": image_uuid,
                "class_id": self.class_id,
                "mask_type": self.mask_type,
            }
        )

        image_object = self.MainWindow.DH.BLobj.get_image_object_by_uuid(image_uuid)
        image_object.setUserModifiedAnnotation(True)
        self.MainWindow.viewer.updateMaskCountLabel()

    def getPosInDict(self, myList):  # HERE
        return len(myList) - 1


class MoveCommand(QtGui.QUndoCommand):
    def __init__(self, PolItem, OldPolygon, CurrentPolygon, MainWindow):
        super(MoveCommand, self).__init__()
        self.PolItem = PolItem
        self.OldPolygon = OldPolygon
        self.CurrentPolygon = self.PolItem.polygon()
        self.MainWindow = MainWindow

    def redo(self):
        self.PolItem.setPolygon(self.CurrentPolygon)
        self.PolItem.setPos(0, 0)
        self.MainWindow.myPolDict["control"].append(self.CurrentPolygon)
        # self.setText("Move Item %d %d" % (self.shape.pos().x(), self.shape.pos().y()))

    def undo(self):
        self.PolItem.setPolygon(self.OldPolygon)
        self.PolItem.setPos(0, 0)

        # # self.shape.scene().update()
        # self.setText("Move Item %d %d" % (self.shape.pos().x(), self.shape.pos().y()))

    def getPosInDict(self, myList):  # HERE
        return len(myList) - 1


if __name__ == "__main__":
    pass
