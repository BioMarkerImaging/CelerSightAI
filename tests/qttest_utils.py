import logging
import os
import sys
import unittest

import numpy as np
import pytest
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtTest import QTest

import celer_sight_ai
from celer_sight_ai import config

logger = logging.getLogger(__name__)

DELAY_TIME = 200  # in ms


# create a decorator that adds 200ms before and after the method
def add_delay(func):
    def wrapper(*args, **kwargs):
        QTest.qWait(DELAY_TIME)
        result = func(*args, **kwargs)
        QTest.qWait(DELAY_TIME)
        return result

    return wrapper


@add_delay
def read_imagej_roi_with_polygon_tool(gui_main, roi_path):
    import roifile

    array = roifile.roiread(roi_path).coordinates()
    draw_mask_by_array(gui_main, array)


@add_delay
def get_gui_main(offline=False):
    """
    This function returns the main GUI widget of a program called Celer Sight AI, after starting the
    program and adding the widget to a Qt testbot.

    Args:
      qtbot: The qtbot parameter is an instance of the pytest-qt plugin's QtBot class. It is used to
    simulate user interaction with the graphical user interface (GUI) and to test the behavior of the
    GUI in response to user actions.

    Returns:
      The function `get_gui_main` returns the `gui_main` object, which is the main graphical user
    interface of the Celer Sight AI application.
    """
    import importlib

    if offline:
        celer_sight_ai.config.user_cfg["OFFLINE_MODE"] = True
    # if the application is frozen
    print("Current path is ", os.getcwd())
    if hasattr(sys, "frozen"):
        print("Frozen")
        # change the path to the current directory
        # print the path
        celer_sight_ai_entry = importlib.import_module(
            "celer_sight_ai.celer_sight_ai_main_import"
        )
        (
            app,
            login_handler,
            gui_main,
            splash_window,
        ) = celer_sight_ai_entry.start_celer_sight_ai()
    else:
        # print the path
        celer_sight_ai_entry = importlib.import_module("celer_sight_ai.Celer Sight AI")
        (
            app,
            login_handler,
            gui_main,
            splash_window,
        ) = celer_sight_ai_entry.start_celer_sight_ai()
    return gui_main


def wait_until_shown(widget):
    """
    This function waits until a widget is shown on the screen.

    Args:
      widget: The widget parameter is a Qt widget object that is being tested.

    Returns:
      The function `wait_until_shown` returns a boolean value indicating whether the widget is
    shown on the screen.
    """
    while not widget.isVisible():
        QTest.qWait(1000)
    return True


@add_delay
def click_on_model_button(
    app: QtWidgets.QApplication, model_button_names: list[str] = ["body"]
):
    # after chosing the supercategory the user needs to select
    # the part of the supercategory for the ROI generation.
    # This method selects the button based on text
    # and clicks on it (from grid_button_image_selector.py)

    # get all buttons
    logger.debug(f"Looking for {model_button_names}")
    all_button = [
        btn
        for btn in app.category_selection_grid.items
        if btn.classes == model_button_names
    ]
    assert (
        len(all_button) > 0
    ), "Could not find button with the specified model_button_names variable"
    if len(all_button) > 0:
        logger.debug("Found model , clicking it")
        all_button[0].setChecked(True)
    return None


@add_delay
def click_on_analysis(app: QtWidgets.QApplication, mode: str = "intensity"):
    if mode == "intensity":
        logger.debug("Clicking on intensity analysis")
        QTest.mouseClick(app.btn_intensity_analysis, QtCore.Qt.MouseButton.LeftButton)
    elif mode == "particles":
        logger.debug("Clicking on particle analysis")
        QTest.mouseClick(app.btn_particle_analysis, QtCore.Qt.MouseButton.LeftButton)
    return app


@add_delay
def do_analysis(app):
    import time

    # click on initialize_analysis_button
    app.initialize_analysis_button.click()
    QtWidgets.QApplication.processEvents()
    total_images = len([i for i in app.DH.BLobj.get_all_image_objects()])
    max_time_per_image = 5
    timeout = total_images * max_time_per_image
    start = time.time()
    # wait until progress dialog is visible
    while app.AnalysisSettings.during_analysis:
        if (time.time() - start) > timeout:
            print("Analysis is taking too long to run")
            return False
        QtWidgets.QApplication.processEvents()

    # check to see if we are on .MasterTabWidgets.setCurrentIndex(1)
    while app.MasterTabWidgets.currentIndex() != 1:
        QtWidgets.QApplication.processEvents()


@add_delay
def click_on_image_button(app, image_idx):
    # get all current buttons
    all_image_objects = app.DH.BLobj.get_all_image_objects()
    image_object = all_image_objects[image_idx]
    image_button = image_object.myButton
    QTest.mouseClick(image_button.button_instance, QtCore.Qt.MouseButton.LeftButton)


@add_delay
def to_main_window(
    app: QtWidgets.QApplication | None,
    mode: str = "intensity",
    model_button_names: list[str] = ["body"],
    organism: str = "worm",  # can also be "on_plate"
):

    if app is None:
        return
    wait_until_shown(app.MainWindow)
    if organism == "on_plate":
        # click on organism on_plate
        QTest.mouseClick(
            app.organism_selection.on_plate_superclass_button,
            QtCore.Qt.MouseButton.LeftButton,
        )
    elif organism == "worm":
        # click on organism worm
        QTest.mouseClick(
            app.organism_selection.CelegansMainButton, QtCore.Qt.MouseButton.LeftButton
        )
    click_on_model_button(app, model_button_names)
    click_on_analysis(app, mode)
    # click on next button when at model selection
    QTest.mouseClick(app.CreateNewVButton_proceed, QtCore.Qt.MouseButton.LeftButton)
    QTest.mouseClick(app.Images, QtCore.Qt.MouseButton.LeftButton)

    # make sure we are at the main window
    assert app.MainWindow.isVisible()
    # maximimze
    app.MainWindow.showMaximized()
    QtWidgets.QApplication.processEvents()
    return app


def go_to_data_tab(app):
    QTest.mouseClick(app.Data, QtCore.Qt.MouseButton.LeftButton)


def get_plain_text(html_text):
    doc = QtGui.QTextDocument()
    doc.setHtml(html_text)
    plain_text = doc.toPlainText()
    return plain_text


def assert_data_equals(app, roi_name="body", treatment_name=None, values_to_check=None):
    """
    values_to_check:
        {
            mean : {channel_name: value},
        }
    """
    if not treatment_name:
        # get the current treatment name
        treatment_name = app.DH.BLobj.get_current_condition()

    for operation_to_check, channel_values in values_to_check.items():
        # change Results_pg2_AnalysisTypeComboBox to "mean" or whatever other value was requested
        # iterate over all items
        FOUND = False
        for i in range(app.Results_pg2_AnalysisTypeComboBox.count()):
            if app.Results_pg2_AnalysisTypeComboBox.itemText(i) == operation_to_check:
                app.Results_pg2_AnalysisTypeComboBox.setCurrentIndex(i)
                FOUND = True
                break
        if not FOUND:
            raise ValueError(f"Could not find {operation_to_check} in the combobox")

        # change ROI_analysis_metrics_combobox to match the roi_name
        FOUND = False
        for i in range(app.ROI_analysis_metrics_combobox.count()):
            if app.ROI_analysis_metrics_combobox.itemText(i) == roi_name:
                app.ROI_analysis_metrics_combobox.setCurrentIndex(i)
                FOUND = True
                break
        if not FOUND:
            raise ValueError(f"Could not find {roi_name} in the combobox")

        for channel_name, value in channel_values.items():
            # change to channel_name == value on the channel_analysis_metrics_combobox widget
            FOUND = False
            for i in range(app.channel_analysis_metrics_combobox.count()):
                if (
                    get_plain_text(
                        app.channel_analysis_metrics_combobox.itemText(i)
                    ).lower()
                    == channel_name
                ):
                    app.channel_analysis_metrics_combobox.setCurrentIndex(i)
                    FOUND = True
                    break
            if not FOUND:
                raise ValueError(f"Could not find {channel_name} in the combobox")

            print()
            # get the value from the table
            df = app.all_condition_analysis_table.model_pandas.dataFrame[
                treatment_name
            ].values
            assert np.allclose(np.round(df[0]), np.round(value), atol=1)


def adjust_bbox_points(point1, point2):
    # Make sure that point 1 is alaways the top left and point 2 is always the bottom right
    x1, y1 = point1
    x2, y2 = point2
    if x1 > x2:
        x1, x2 = x2, x1
    if y1 > y2:
        y1, y2 = y2, y1
    return x1, y1, x2, y2


def adjust_point_from_scene_to_viewport(gui_main, point):
    """
    adjusts the point from the actual coordinate on the scene, which
    should be the same as the image, to the coordinate on the viewport
    Args:
        gui_main: the main gui object
        point: array [x, y]
    """
    return gui_main.viewer.mapFromScene(QtCore.QPointF(point[0], point[1]))


def click_on_action_dialog_with_button(app, text_to_click):
    # clicks on the button  / action that matches the text provided

    # find all widgets that are buttons
    all_buttons = app.DH.warningHandler.warning.WarningDialForm.findChildren(
        QtWidgets.QPushButton
    )
    # if a button matches the text, click it
    for button in all_buttons:
        if button.text().lower() == text_to_click.lower():
            QTest.mouseClick(button, QtCore.Qt.MouseButton.LeftButton)
            return True


@add_delay
def wait_until_current_remote_image_has_been_downloaded(app):
    """
    This function waits until the current image has been downloaded from the remote server
    """
    QTest.qWait(
        DELAY_TIME
    )  # make sure enough time has been set for the image to start download
    while app.DH.BLobj.get_current_image_object()._is_downloading:
        QTest.qWait(DELAY_TIME)
    return app


@add_delay
def zoom_to_box(app, bbox):
    # bbox is a list or tuple of [x1, y1, x2, y2]
    x1, y1, x2, y2 = bbox
    x1, y1, x2, y2 = adjust_bbox_points([x1, y1], [x2, y2])
    # Create a QRectF from the bounding box
    rect = QtCore.QRectF(x1, y1, x2 - x1, y2 - y1)

    # Calculate the target size of the rectangle as a percentage of the viewport's size
    target_percentage = 0.006  # 30%
    viewport_area = app.viewer.viewport().width() * app.viewer.viewport().height()
    target_rect_area = viewport_area * target_percentage

    # Calculate the scale factor needed to resize the rect to the target area
    rect_area = rect.width() * rect.height()
    scale_factor = (target_rect_area / rect_area) ** 0.5

    # Calculate the center of the bounding box in scene coordinates
    center = rect.center()
    # wait
    QTest.qWait(500)
    # Reset any existing transformations
    app.viewer.resetTransform()

    # Scale the view around the center point
    app.viewer.scale(scale_factor, scale_factor)

    # Center the view on the center of the bounding box
    app.viewer.centerOn(center)

    # on ultra high res, update viewport otherwise its blury
    app.viewer.check_and_update_high_res_slides(force_update=True)
    QTest.qWait(500)
    return app


@add_delay
def delete_mask(app, mask_idx=0):
    """
    Assume we are deleting the current group, treatment and image
    zoom in on the mask , and delete it by clicking it
    """
    logger.info(f"Deleting mask {mask_idx}")
    # get the mask object
    mask_object = (
        app.DH.BLobj.group[app.DH.BLobj.current_group]
        .cond[app.DH.BLobj.get_current_condition()]
        .images[app.DH.BLobj.get_current_image_number()]
        .masks[mask_idx]
    )
    # get the qgraphics object from the mask
    mask_qgraphics_object = mask_object.get_annotation_item()
    QTest.qWait(DELAY_TIME)
    mask_qgraphics_object.DeleteMask()
    QTest.qWait(DELAY_TIME)


@add_delay
def draw_mask_by_array(gui_main, point_array):
    gui_main.PolygonTool.trigger()
    QTest.qWait(50)
    # get all annotations uuids before this one
    all_mask_uuids_old = [i.unique_id for i in gui_main.DH.BLobj.get_all_mask_objects()]

    # zoom to area of interest
    # get the bounding box of the mask
    x1 = min(point_array[:, 0])
    x2 = max(point_array[:, 0])
    y1 = min(point_array[:, 1])
    y2 = max(point_array[:, 1])
    zoom_to_box(gui_main, [x1, y1, x2, y2])
    for point in point_array:
        point = adjust_point_from_scene_to_viewport(gui_main, point)
        QTest.qWait(10)
        QTest.mousePress(
            gui_main.viewer.viewport(), QtCore.Qt.MouseButton.LeftButton, pos=point
        )
        QTest.qWait(10)
        QTest.mouseRelease(
            gui_main.viewer.viewport(), QtCore.Qt.MouseButton.LeftButton, pos=point
        )
        QTest.qWait(10)
    # double clik to close the polygon
    QTest.mouseDClick(
        gui_main.viewer.viewport(), QtCore.Qt.MouseButton.LeftButton, pos=point
    )
    QTest.qWait(1500)  # wait 1.5 seconds
    all_mask_uuids_new = [i.unique_id for i in gui_main.DH.BLobj.get_all_mask_objects()]
    assert (
        len(all_mask_uuids_new) == len(all_mask_uuids_old) + 1
    ), "Got a different number of annotations than expected"
    added_uuid = list(set(all_mask_uuids_new) - set(all_mask_uuids_old))[0]
    return added_uuid


@add_delay
def magic_box_predict(gui_main, prompt_bbox):
    # make sure the magic box tool is selected
    gui_main.actionAutoTool.trigger()
    QTest.qWait(50)
    # make sure that the generic magic box is selected
    gui_main.ai_model_combobox.setIndexAsSelected(1)  # generic magic box
    QTest.qWait(50)
    x1, y1, x2, y2 = prompt_bbox
    point1 = [x1, y1]
    point2 = [x2, y2]
    x1, y1, x2, y2 = adjust_bbox_points(point1, point2)
    point1 = [x1, y1]
    point2 = [x2, y2]
    # get current image object
    img_obj = gui_main.DH.BLobj.get_current_image_object()
    current_condition = gui_main.DH.BLobj.get_current_condition()
    current_group = gui_main.DH.BLobj.get_current_group()
    # get current selected class
    current_class_uuid = gui_main.DH.BLobj.get_current_class_uuid()

    gui_main.viewer.draw_bounding_box_stop(
        bbox=[point1[0], point1[1], point2[0], point2[1]],
        current_condition=current_condition,
        current_group=current_group,
        class_id=current_class_uuid,
        current_image_uuid=img_obj.unique_id,
    )
    return gui_main


@add_delay
def close_notification_dialog():
    config.global_signals.close_accept_notification_signal.emit()
    QtWidgets.QApplication.processEvents()


def clear_all_treatments(gui_main):
    while gui_main.RNAi_list.count() > 0:
        # select the first item
        item_rect = gui_main.RNAi_list.visualItemRect(gui_main.RNAi_list.item(0))
        QTest.mouseClick(
            gui_main.RNAi_list.viewport(),
            QtCore.Qt.MouseButton.LeftButton,
            pos=item_rect.center(),
        )
        # remove the item
        QTest.mouseClick(gui_main.delete_button_list, QtCore.Qt.MouseButton.LeftButton)
        # wait for the item to be removed
        QTest.qWait(500)


@add_delay
def record_DH_data(app):
    import copy

    config.DH_data = copy.deepcopy(data_handler_object_to_dict(app.DH.BLobj))


def data_handler_object_to_dict(data_handler):
    # convert the data handler object to a dictionary
    data = {}
    data["groups"] = {}
    for group_name, group in data_handler.groups.items():
        data["groups"][group_name] = {}
        data["groups"][group_name]["conds"] = {}
        for condition_name, condition in group.conds.items():
            data["groups"][group_name]["conds"][condition_name] = {}
            data["groups"][group_name]["conds"][condition_name]["images"] = []
            for image in condition.images:
                img_dict = {}
                img_dict["imgID"] = image.imgID
                img_dict["treatment_uuid"] = image.treatment_uuid
                img_dict["channels"] = image.channel_list
                img_dict["masks"] = []
                for mask in image.masks:
                    mask_dict = {}
                    mask_dict["class_id"] = mask.class_id
                    mask_dict["polygon_array"] = mask.get_array()
                    img_dict["masks"].append(mask_dict)
                data["groups"][group_name]["conds"][condition_name]["images"].append(
                    img_dict
                )
    return data


@add_delay
def wait_until_ui_settles(app):
    # wait until all images have been loaded
    print("waiting for things to be settled")
    while any(
        [
            app.during_load_main_scene_display,
            app.images_preview_graphicsview._is_updating_buttons,
        ]
    ):
        QTest.qWait(300)


def deep_diff(old, new, path=""):
    """Recursively find differences between two objects."""
    if isinstance(old, dict) and isinstance(new, dict):
        for key in old.keys() | new.keys():
            if key in old and key in new:
                deep_diff(old[key], new[key], path + "." + str(key))
            elif key in old:
                print(f"{path}.{key}: Removed from new")
            else:
                print(f"{path}.{key}: Added in new")
    elif isinstance(old, list) and isinstance(new, list):
        for i, items in enumerate(zip(old, new)):
            o, n = items
            deep_diff(o, n, path + f"[{i}]")
        if len(old) < len(new):
            for i in range(len(old), len(new)):
                print(f"{path}[{i}]: Added {new[i]}")
        elif len(old) > len(new):
            for i in range(len(new), len(old)):
                print(f"{path}[{i}]: Removed {old[i]}")
    else:
        if old != new:
            print(f"{path}: {old} -> {new}")


def get_data(app):
    # get the data from the data handler
    data = data_handler_object_to_dict(app.DH.BLobj)
    return data


def delete_image_on_current_treatment(gui_main, image_idx=0):
    # deletes the image with the specified id on the current treatment
    if image_idx >= len(gui_main.images_preview_graphicsview.visible_buttons):
        image_idx = len(gui_main.images_preview_graphicsview.visible_buttons) - 1
    gui_main.images_preview_graphicsview.visible_buttons[
        image_idx
    ].button_instance.deleteCurrentImage(reload_image=True)


def rename_treatment(gui_main, old_name, new_name):
    # select condition to rename
    all_items = gui_main.RNAi_list.findItems(old_name, QtCore.Qt.MatchFlag.MatchExactly)
    if len(all_items) == 0:
        logger.info(f"Item {old_name} not found in RNAi_list")
        return False
    item_rect = gui_main.RNAi_list.visualItemRect(all_items[0])

    # select item
    QTest.mouseClick(
        gui_main.RNAi_list.viewport(),
        QtCore.Qt.MouseButton.LeftButton,
        pos=item_rect.center(),
    )

    # get the item to rename
    item_rect = gui_main.RNAi_list.visualItemRect(all_items[0])

    # Double-click on the item to enter text-editing mode
    QTest.mouseDClick(
        gui_main.RNAi_list.viewport(),
        QtCore.Qt.MouseButton.LeftButton,
        pos=item_rect.center(),
    )

    # Edit the text in the item
    all_items[0].setText(new_name)

    # Press the Enter key to finish editing
    QTest.keyClick(gui_main.RNAi_list, QtCore.Qt.Key.Key_Enter)
    QTest.mouseClick(
        gui_main.RNAi_list.viewport(),
        QtCore.Qt.MouseButton.LeftButton,
        pos=item_rect.center(),
    )
    return True


@add_delay
def contribute_images(gui_main, mode="partial"):  # or partial
    from celer_sight_ai import config

    # Contribute data through the UI
    # first do: File -> Contribute Data
    QTest.mouseClick(gui_main.menuFile, QtCore.Qt.MouseButton.LeftButton)
    # trigger the action of gui_main.actionSend_for_training, which is not
    # a button but an action
    gui_main.actionSend_for_training.trigger()
    # select the correct box
    if mode == "partial":
        QTest.mouseClick(
            gui_main.contribute_images_widget.partiallyAnnotatedButton,
            QtCore.Qt.MouseButton.LeftButton,
        )
    elif mode == "complete":
        QTest.mouseClick(
            gui_main.contribute_images_widget.fullyAnnotatedButton,
            QtCore.Qt.MouseButton.LeftButton,
        )
    else:
        raise ValueError("Mode must be either 'partial' or 'complete'")
    # click on text box to accept terms
    QTest.qWait(DELAY_TIME)
    QTest.mouseClick(
        gui_main.contribute_images_widget.accept_radio_button,
        QtCore.Qt.MouseButton.LeftButton,
    )
    # accept
    QTest.qWait(DELAY_TIME)
    QTest.mouseClick(
        gui_main.contribute_images_widget.accept_button,
        QtCore.Qt.MouseButton.LeftButton,
    )
    QTest.qWait(DELAY_TIME)

    # wait for images to be send
    while config.contribing_data is True:
        QTest.qWait(DELAY_TIME)


if __name__ == "__main__":
    pass
