import aicsimageio
import sys
import os
from glob import glob
from os import path as osp
import unittest
import time
import pytest
from PyQt6 import QtCore, QtGui, QtWidgets
import logging
import pyautogui
from functools import partial
import time
from celer_sight_ai.configHandle import (
    get_stored_password,
    get_stored_username,
    get_app_settings,
)
from celer_sight_ai import config
from pytestqt.qtbot import QtBot
from celer_sight_ai.gui.custom_widgets.splash_widget import CustomSplashScreenWithText
from typing import Literal

pyautogui.FAILSAFE = True

# add parent directory to path
p_dir: str = os.path.dirname(os.path.abspath(__file__))

list_of_accepted_images: list[str] = [
    ".TIF",
    ".tif",
    ".tiff",
    ".png",
    ".PNG",
    "jpeg",
    "jpg",
    "JPEG",
    "JPG",
]
test_urls_fixure: list[str] = glob(
    osp.join(p_dir, "fixtures/fixture_adding_removing_images_test", "*")
)
list_of_accepted_images = [
    i for i in test_urls_fixure if i.endswith(tuple(list_of_accepted_images))
]


# if mac os
if os.name == "posix":
    import Quartz
    from AppKit import NSWorkspace
    from ScriptingBridge import *
    from screeninfo import get_monitors


os.environ["CELER_SIGHT_TESTING"] = "true"
logger = logging.getLogger(__name__)


def close_notification_dialog(app, qtbot):
    config.global_signals.close_accept_notification_signal.emit()
    QtWidgets.QApplication.processEvents()
    qtbot.wait(50)


def get_gui_main(qtbot):
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

    # if the application is frozen
    print("Current path is ", os.getcwd())
    if hasattr(sys, "frozen"):
        print("Frozen")
        # change the path to the current directory
        # print the path
        celer_sight_ai_entry = importlib.import_module("celer_sight_ai_main_import")
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
    qtbot.addWidget(gui_main)
    return gui_main


def adjust_bbox_points(point1, point2):
    # Make sure that point 1 is alaways the top left and point 2 is always the bottom right
    x1, y1 = point1
    x2, y2 = point2
    if x1 > x2:
        x1, x2 = x2, x1
    if y1 > y2:
        y1, y2 = y2, y1
    return x1, y1, x2, y2


def zoom_to_box(qtbot, app, bbox):
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
    qtbot.wait(500)
    # Reset any existing transformations
    app.viewer.resetTransform()

    # Scale the view around the center point
    app.viewer.scale(scale_factor, scale_factor)

    # Center the view on the center of the bounding box
    app.viewer.centerOn(center)

    # on ultra high res, update viewport otherwise its blury
    app.viewer.check_and_update_high_res_slides(force_update=True)
    qtbot.wait(500)
    return qtbot, app


def click_on_model_button(
    app: QtWidgets.QApplication, qtbot: QtBot, model_button_names: list[str] = ["body"]
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
        all_button[0].click()
    return None


def click_on_analysis(
    app: QtWidgets.QApplication, qtbot: QtBot, mode: str = "intensity"
) -> tuple[QtWidgets.QApplication, QtBot]:
    if mode == "intensity":
        logger.debug("Clicking on intensity analysis")
        qtbot.mouseClick(app.btn_intensity_analysis, QtCore.Qt.MouseButton.LeftButton)
    elif mode == "particles":
        logger.debug("Clicking on particle analysis")
        qtbot.mouseClick(app.btn_particle_analysis, QtCore.Qt.MouseButton.LeftButton)
    return app, qtbot


def get_particle(qtbot, app):
    # find a particle
    # loop over all classes, if a particle is present click it
    for c, w_item in app.custom_class_list_widget.classes.items():
        if w_item.is_particle == True:
            # click on the particle
            qtbot.mouseClick(
                w_item,
                QtCore.Qt.MouseButton.LeftButton,
                delay=200,
                pos=QtCore.QPoint(5, 5),
            )
            # process events for the dialog to pop up
            QtWidgets.QApplication.processEvents()
            QtWidgets.QApplication.processEvents()
            # check if the dialog is visible
            assert app.viewer.particle_analysis_settings_widget.isVisible()
            particle_widget = app.viewer.particle_analysis_settings_widget
            # set channel color to red (in the case of rgb)
            particle_widget.channel_combobox.setCurrentIndex(0)
            particle_widget.update_channel_combobox_label(0)
            # set background removal to 5
            particle_widget.background_slider.setValue(5)
            QtWidgets.QApplication.processEvents()
            # set the threshold
            particle_widget.threshold_slider.setValue(5)
            QtWidgets.QApplication.processEvents()
            # accept
            qtbot.mouseClick(
                particle_widget.done_button,
                QtCore.Qt.MouseButton.LeftButton,
                delay=200,
                pos=QtCore.QPoint(5, 5),
            )


def to_main_window(
    qtbot: QtBot,
    app: QtWidgets.QApplication,
    mode: str = "intensity",
    model_button_names: list[str] = ["body"],
) -> tuple[QtWidgets.QApplication, QtBot]:
    # qtbot.addWidget(app)
    qtbot.waitForWindowShown(app)
    # click on organism worm
    qtbot.mouseClick(
        app.organism_selection.CelegansMainButton, QtCore.Qt.MouseButton.LeftButton
    )
    click_on_model_button(app, qtbot, model_button_names)
    click_on_analysis(app, qtbot, mode)
    # click on next button when at model selection
    qtbot.mouseClick(app.CreateNewVButton_proceed, QtCore.Qt.MouseButton.LeftButton)
    # make sure we are at the main window
    assert app.MainWindow.isVisible()
    # maximimze
    app.MainWindow.showMaximized()
    QtWidgets.QApplication.processEvents()
    return app, qtbot


def do_sample_experiemnt(
    app, qtbot, mode="intensity", model_button_names: list[str] = ["body"]
):
    app, qtbot = to_main_window(qtbot, app, mode, model_button_names)

    assert len(list_of_accepted_images) != 0, "Error : No images to import"
    app.viewer.add_new_images_by_drag_and_drop(list_of_accepted_images)
    cond_name = "wt L1 TMRE_Image"
    # only one item can be selected
    assert len(app.RNAi_list.selectedItems()) == 1, "Error : Condition len is not 1"

    # make sure its the same as it is recorded in the viewer
    assert (
        app.RNAi_list.selectedItems()[0].text() == cond_name
    ), "Error : Condition is not selected"

    # wait 5 seconds for the images to load
    # same amount of images in viewer as in list_of_accepted_images
    group_name = "default"
    assert check_total_images_loaded_for_condition(
        qtbot, app, cond_name, group_name, len(list_of_accepted_images)
    ), "Error : Image len are not the same as the ones imported"

    assert app.RNAi_list.selectedItems()[0].text() == cond_name
    get_ROI_AI(qtbot, app)
    if mode == "particles":
        get_particle(qtbot, app)
    return qtbot, app


def get_app_without_credentials(qtbot):
    from PyQt6.QtWidgets import QApplication

    # copied from Celer Sight AI.py
    ########################################
    from celer_sight_ai import celer_sight_main

    # This runs on the firs time CelerSight module is imported
    app = QApplication(sys.argv)
    # splashWindow.myDialog_OVER.raise_()
    QApplication.processEvents()
    ########################################

    # this is only the first part of the start_celer_sight_main method
    login_handler = celer_sight_main.start_celer_sight_main_part_login(app, None)
    QtWidgets.QApplication.processEvents()

    qtbot.addWidget(login_handler.LogInDialog)
    login_handler.pushButton_2.click()
    # wait 3 seconds
    QtWidgets.QApplication.processEvents()
    qtbot.wait(5000)
    login_handler.LogInDialog.show()

    QtWidgets.QApplication.processEvents()
    # check if widget is visible
    if not login_handler.LogInDialog.isVisible():
        print()
    assert login_handler.LogInDialog.isVisible()
    # Make sure we failed with "Please check your credentials and try again."
    if (
        not login_handler.label_ThatshowsError.text()
        == "Please check your credentials and try again."
    ):
        print()
    assert (
        login_handler.label_ThatshowsError.text()
        == "Please check your credentials and try again."
    )
    print("Log in ui  <<failing>> test passed")
    # close widget
    login_handler.LogInDialog.close()

    del login_handler
    del app

    import gc

    gc.collect()
    return True


def assert_treatment_exist(
    qtbot: QtBot, gui_main: QtWidgets.QApplication, treatment_name: str
) -> Literal[True]:
    # needs to exist on main window data handler data and the ui
    # data handler:
    if (
        treatment_name
        not in gui_main.DH.BLobj.groups[gui_main.DH.BLobj.get_current_group()].conds
    ):
        # log that it does not exist, log the treatments that exist
        logger.error(f"Treatment {treatment_name} does not exist")
        treatments_now = gui_main.DH.BLobj.groups[
            gui_main.DH.BLobj.get_current_group()
        ].conds.keys()
        logger.error(f"Here is the list of treatments : {list(treatments_now)}")
        assert (
            treatment_name
            in gui_main.DH.BLobj.groups[gui_main.DH.BLobj.get_current_group()].conds
        ), "Treatment name does not exist in the data handler"
    # check if it exists in the ui
    all_items = gui_main.RNAi_list.findItems(
        treatment_name, QtCore.Qt.MatchFlag.MatchExactly
    )
    # make sure it is only one:
    assert len(all_items) == 1, "Error : Treatment name is not unique"
    logger.info(f"Treatment {treatment_name} exists in data and in UI")
    return True


def rename_treatment(qtbot, gui_main, old_name, new_name):
    # select condition to rename
    all_items = gui_main.RNAi_list.findItems(old_name, QtCore.Qt.MatchFlag.MatchExactly)
    if len(all_items) == 0:
        logger.info(f"Item {old_name} not found in RNAi_list")
        return False
    item_rect = gui_main.RNAi_list.visualItemRect(all_items[0])

    # select item
    qtbot.mouseClick(
        gui_main.RNAi_list.viewport(),
        QtCore.Qt.MouseButton.LeftButton,
        pos=item_rect.center(),
    )

    # get the item to rename
    item_rect = gui_main.RNAi_list.visualItemRect(all_items[0])

    # Double-click on the item to enter text-editing mode
    qtbot.mouseDClick(
        gui_main.RNAi_list.viewport(),
        QtCore.Qt.MouseButton.LeftButton,
        pos=item_rect.center(),
    )

    # Edit the text in the item
    all_items[0].setText(new_name)

    # Press the Enter key to finish editing
    qtbot.keyClick(gui_main.RNAi_list, QtCore.Qt.Key.Key_Enter)
    qtbot.mouseClick(
        gui_main.RNAi_list.viewport(),
        QtCore.Qt.MouseButton.LeftButton,
        pos=item_rect.center(),
    )
    return True


def check_data_corruption(qtbot, app):
    from celer_sight_ai import config

    try:
        if not config.is_executable:
            logger.debug("checking data corruption")
            # assert that every condition visible in the main window is also in the analysis object
            # get all possible conditions:
            raise NotImplementedError("Needs to reconfigure for treatment uuid")
            for i in range(app.RNAi_list.count()):
                condition = app.RNAi_list.item(i).text()
                while app.RNAi_list.itemBeingEdited != None:
                    QtCore.QCoreApplication.processEvents()
                    import time

                    time.sleep(0.1)
                assert (
                    condition
                    in app.DH.BLobj.groups[
                        app.DH.BLobj.get_current_group()
                    ].conds.keys()
                )
                # iterate over all images in the condition and make sure that they all have a continious id
                all_img_ids = []  # list of all image ids
                for img in (
                    app.DH.BLobj.groups[app.DH.BLobj.get_current_group()]
                    .conds[condition]
                    .images
                ):
                    all_img_ids.append(img.imgID)
                    assert img.imgID == len(all_img_ids) - 1
                    assert img.imgID == app.DH.BLobj.groups[
                        app.DH.BLobj.get_current_group()
                    ].conds[condition].images.index(img)
                    assert img.image_uuid == condition
                    assert img.channel_list != None

    except Exception as e:
        logger.error(f"Error checking data corruption {e}")
        deep_diff(config.DH_data, app.DH.BLobj.groups)
        assert False
    record_DH_data(app)


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
                img_dict["condName"] = image.condName
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


def get_data(app):
    # get the data from the data handler
    data = data_handler_object_to_dict(app.DH.BLobj)
    return data


def wait_until_ui_settles(qtbot, app):
    # wait until all images have been loaded
    print("waiting for things to be settled")
    while any(
        [
            app.during_load_main_scene_display,
            app.images_preview_graphicsview._is_updating_buttons,
        ]
    ):
        qtbot.wait(500)


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


def add_condition(
    qtbot: QtBot, gui_main: QtWidgets.QApplication, condition: str = None
) -> Literal[True]:
    """
    This function adds a new condition to a GUI interface and sets its text to a given variable.

    Args:
      qtbot: A pytest-qt fixture that provides methods for simulating user input and events in a Qt
    application.
      gui_main: This is an object representing the main GUI window of the application.
      condition: The text that will be added as a new condition in the GUI. Defaults to Added Condition

    Returns:
      the updated `gui_main` object after adding a new condition to the RNAi list.
    """
    logger.info(f"add_condition: {condition}")
    qtbot.mouseClick(gui_main.addRNAi_button_list, QtCore.Qt.MouseButton.LeftButton)
    # click on the last condition
    last_condition = gui_main.RNAi_list.item(gui_main.RNAi_list.count() - 1)

    item_rect = gui_main.RNAi_list.visualItemRect(last_condition)
    qtbot.mouseClick(
        gui_main.RNAi_list.viewport(),
        QtCore.Qt.MouseButton.LeftButton,
        pos=item_rect.center(),
    )

    # Double-click on the item to enter text-editing mode
    qtbot.mouseDClick(
        gui_main.RNAi_list.viewport(),
        QtCore.Qt.MouseButton.LeftButton,
        pos=item_rect.center(),
    )
    if condition:
        # Edit the text in the item
        last_condition.setText(condition)

    item_rect = gui_main.RNAi_list.visualItemRect(last_condition)
    # Press the Enter key to finish editing
    qtbot.keyClick(gui_main.RNAi_list, QtCore.Qt.Key.Key_Enter)
    qtbot.mouseClick(
        gui_main.RNAi_list.viewport(),
        QtCore.Qt.MouseButton.LeftButton,
        pos=item_rect.center(),
    )
    return True


def remove_condition(qtbot, gui_main, condition="Added Condition"):
    """
    This function removes a specified condition from a list in a GUI using mouse clicks.

    Args:
      qtbot: A pytest-qt fixture that provides methods for simulating user input and events in a Qt
    application.
      gui_main: This is likely an instance of the main GUI window or widget that the user interacts
    with. It probably contains various buttons, lists, and other widgets that allow the user to interact
    with the program.
      condition: The name of the condition to be removed from the RNAi_list. Defaults to Added Condition

    Returns:
      a boolean value indicating whether the specified condition was successfully removed from the
    RNAi_list or not.
    """
    logger.info(f"remove_condition: {condition}")
    # select condition to remove
    all_items = gui_main.RNAi_list.findItems(
        condition, QtCore.Qt.MatchFlag.MatchExactly
    )
    if len(all_items) == 0:
        logger.info(f"Item {condition} not found in RNAi_list")
        return False
    item_rect = gui_main.RNAi_list.visualItemRect(all_items[0])

    # select item
    qtbot.mouseClick(
        gui_main.RNAi_list.viewport(),
        QtCore.Qt.MouseButton.LeftButton,
        pos=item_rect.center(),
    )

    # remove item
    qtbot.mouseClick(gui_main.delete_button_list, QtCore.Qt.MouseButton.LeftButton)

    return True


def clear_all_treatments(qtbot, gui_main):
    while gui_main.RNAi_list.count() > 0:
        # select the first item
        item_rect = gui_main.RNAi_list.visualItemRect(gui_main.RNAi_list.item(0))
        qtbot.mouseClick(
            gui_main.RNAi_list.viewport(),
            QtCore.Qt.MouseButton.LeftButton,
            pos=item_rect.center(),
        )
        # remove the item
        qtbot.mouseClick(gui_main.delete_button_list, QtCore.Qt.MouseButton.LeftButton)
        # wait for the item to be removed
        qtbot.wait(500)


def check_condition_exists(qtbot, gui_main, condition="Added Condition"):
    # list all conditions from RNAi_list
    all_items = gui_main.RNAi_list.findItems(
        condition, QtCore.Qt.MatchFlag.MatchExactly
    )
    if len(all_items) == 0:
        logger.info(f"Item {condition} not found in RNAi_list")
        return -1
    # get item position
    item_pos = gui_main.RNAi_list.row(all_items[0])
    if item_pos == -1:
        logger.info(f"Item {condition} not found in RNAi_list")
        return -1
    return item_pos


def magic_box_predict(qtbot, gui_main, point1, point2):
    # make sure the magic box tool is selected
    gui_main.actionAutoTool.trigger()
    qtbot.wait(50)
    # make sure that the generic magic box is selected
    gui_main.ai_model_combobox.setIndexAsSelected(1)  # generic magic box
    qtbot.wait(50)
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
    qtbot.wait(1000)

    return qtbot, gui_main


def check_confirmation_dialog_and_accept(qtbot, gui_main):
    """
    The function checks if a confirmation dialog is visible and accepts it if it is.

    Args:
      qtbot: The `qtbot` parameter is an instance of the `QTestBot` class, which is used for simulating
    user interactions with the GUI.
      gui_main: The `gui_main` parameter is an instance of the main GUI class in your application. It
    represents the main window or interface of your application.

    Returns:
      a boolean value. If the confirmation dialog is visible, it will click the "yes" button and return
    True. If the confirmation dialog is not visible, it will return False.
    """
    if gui_main.DH.warningHandler.warning.WarningDialForm.isVisible():
        qtbot.mouseClick(
            gui_main.DH.warningHandler.warning.okBtn,
            QtCore.Qt.MouseButton.LeftButton,
        )
        return True
    else:
        return False


def accept_warning_dialog(gui_main):
    gui_main.DH.warningHandler.warning.okBtn.click()


def get_ROI_AI(
    qtbot,
    gui_main,
):
    logger.info("Generating ROIs.")
    gui_main.get_roi_ai_button.click()
    QtWidgets.QApplication.processEvents()
    # check if the AI is running
    total_images = len([i for i in gui_main.DH.BLobj.get_all_image_objects()])
    max_time_per_image = 5
    timeout = max_time_per_image * total_images
    start_time = time.time()
    print("Timeout is ", timeout)
    # manully click the button because it doesnt work with qtbot
    # accept_partial = partial(accept_warning_dialog, gui_main)
    # QtCore.QTimer.singleShot(timeout, lambda: accept_warning_dialog(gui_main))
    while gui_main.MyInferenceHandler.is_inference_running:
        if (time.time() - start_time) > timeout:
            print("AI is taking too long to run")
            return False
        # QtWidgets.QApplication.processEvents()
        # wait 0.5 seconds and check again
        qtbot.wait(500)
    # check if analysis window is success
    return check_confirmation_dialog_and_accept(qtbot, gui_main)


def do_analysis(qtbot, gui_main):
    # click on initialize_analysis_button
    gui_main.initialize_analysis_button.click()
    QtWidgets.QApplication.processEvents()
    total_images = len([i for i in gui_main.DH.BLobj.get_all_image_objects()])
    max_time_per_image = 5
    timeout = total_images * max_time_per_image
    start = time.time()
    # wait until progress dialog is visible
    while gui_main.AnalysisSettings.during_analysis:
        if (time.time() - start) > timeout:
            print("Analysis is taking too long to run")
            return False
        QtWidgets.QApplication.processEvents()

    # check to see if we are on .MasterTabWidgets.setCurrentIndex(1)
    while gui_main.MasterTabWidgets.currentIndex() != 1:
        QtWidgets.QApplication.processEvents()


def check_total_images_loaded_for_condition(
    qtbot, gui_main, condition="Added Condition", group="default", expected_images=0
):
    # for each image, add a total timer to check if size matches expected image size
    # if not, double that timer and check again, raise error if timer exceeds 3rd time
    sec_per_image = 0.5
    total_time = expected_images * sec_per_image
    tot_checks = 3
    while tot_checks > 0:
        qtbot.wait(int(total_time * 1000))  # wait in ms
        all_images = [
            i
            for i in gui_main.DH.BLobj.groups[group]
            .conds[condition]
            .get_all_image_objects()
        ]
        if not expected_images == len(all_images):
            tot_checks -= 1
            continue
        else:
            return True
    logger.info(f"Treatment {condition} has {len(all_images)} images: OK")
    return False


def check_all_images_have_channels(qtbot, gui_main):
    for img_obj in gui_main.DH.BLobj.get_all_image_objects():
        if isinstance(img_obj.channel_list, list):
            if len(img_obj.channel_list) == 0:
                print(f"Image {img_obj.fileName} has no channels")
                # read image
                img, result_dict = img_obj.readImage()
                ch = result_dict["channels"]
                print(f"Shape: {img_obj.shape}")
                print(f"Channels now are : P{ch}")
        if img_obj.channel_list is None:
            print(f"Image {img_obj.fileName} has no channels")
            # read image
            img, result_dict = img_obj.readImage()
            ch = result_dict.get("channels", None)
            print(f"Shape: {img_obj.shape}")
            print("Channels now are : P{ch}")


def switch_to_treatment(qtbot, gui_main, treatment_name):
    # switch to the treatment
    all_items = gui_main.RNAi_list.findItems(
        treatment_name, QtCore.Qt.MatchFlag.MatchExactly
    )
    if len(all_items) == 0:
        logger.info(f"Item {treatment_name} not found in RNAi_list")
        return False
    item_rect = gui_main.RNAi_list.visualItemRect(all_items[0])
    qtbot.mouseClick(
        gui_main.RNAi_list.viewport(),
        QtCore.Qt.MouseButton.LeftButton,
        pos=item_rect.center(),
    )
    return True


def delete_image_on_current_treatment(qtbot, gui_main, image_idx=0):
    # deletes the image with the specified id on the current treatment
    if image_idx >= len(gui_main.images_preview_graphicsview.visible_buttons):
        image_idx = len(gui_main.images_preview_graphicsview.visible_buttons) - 1
    gui_main.images_preview_graphicsview.visible_buttons[
        image_idx
    ].button_instance.deleteCurrentImage(reload_image=True)


def drag_and_drop_urls(gui_main, url_list):
    gui_main.viewer.add_new_images_by_drag_and_drop(url_list)
    return gui_main


def set_main_window_left_half_of_screen(gui_main):
    # get the screen size
    screen_width = QtWidgets.QApplication.screens()[0].size().width()
    screen_height = QtWidgets.QApplication.screens()[0].size().height()
    gui_main.MainWindow.setGeometry(0, 0, screen_width // 2, screen_height)
    gui_main.MainWindow.show()
    QtWidgets.QApplication.processEvents()
    return gui_main


def get_current_screen_mac(mouse_x, mouse_y):
    screens = NSScreen.screens()
    for screen in screens:
        screen_frame = screen.frame()
        screen_origin_x = screen_frame.origin.x
        screen_origin_y = screen_frame.origin.y
        screen_width = screen_frame.size.width
        screen_height = screen_frame.size.height

        if (screen_origin_x <= mouse_x < screen_origin_x + screen_width) and (
            screen_origin_y <= mouse_y < screen_origin_y + screen_height
        ):
            return screen

    return None


def get_finder_window_mac(screen):
    active_apps = NSWorkspace.sharedWorkspace().runningApplications()
    for app in active_apps:
        if app.localizedName() == "Finder":
            finder_pid = app.processIdentifier()
            break
    else:
        return None

    finder_windows = []
    for window in Quartz.CGWindowListCopyWindowInfo(
        Quartz.kCGWindowListOptionOnScreenOnly
        | Quartz.kCGWindowListExcludeDesktopElements,
        Quartz.kCGNullWindowID,
    ):
        if window.get("kCGWindowOwnerPID") == finder_pid:
            window_dict = window.to_dictionary()
            window_origin_x = window_dict["kCGWindowBounds"]["X"]
            window_origin_y = window_dict["kCGWindowBounds"]["Y"]
            window_width = window_dict["kCGWindowBounds"]["Width"]
            window_height = window_dict["kCGWindowBounds"]["Height"]

            if (
                screen.frame().origin.x
                <= window_origin_x
                < screen.frame().origin.x + screen.frame().size.width
            ) and (
                screen.frame().origin.y
                <= window_origin_y
                < screen.frame().origin.y + screen.frame().size.height
            ):
                finder_windows.append(window_dict)

    return finder_windows[0] if finder_windows else None


def click_on_window_mac(window):
    x = window["kCGWindowBounds"]["X"] + window["kCGWindowBounds"]["Width"] / 2
    y = window["kCGWindowBounds"]["Y"] + window["kCGWindowBounds"]["Height"] / 2
    pyautogui.moveTo(x, y)
    pyautogui.click()


def resize_and_position(window, width_ratio, height_ratio, x_pos):
    screen_width, screen_height = pyautogui.size()
    window_width = int(screen_width * width_ratio)
    window_height = int(screen_height * height_ratio)
    window.resizeTo(window_width, window_height)
    window.moveTo(x_pos, 0)


def drag_drop_files(relative_path=None):
    # Open the desired folder

    folder_path = os.path.join(
        os.environ["CELER_SIGHT_AI_HOME"],
        "tests",
        "fixtures",
        "test_experiment",
        "TMRE_D1_N2_UA",
    )
    # if windows
    if os.name == "nt":
        os.startfile(folder_path)
        time.sleep(2)  # Give the folder some time to open
        pyautogui.hotkey("win", "right")
        time.sleep(1)
        # do list view
        pyautogui.hotkey("control", "shift", "6")
        time.sleep(1)
        pyautogui.hotkey("esc")
        time.sleep(1)
        screen_width, screen_height = pyautogui.size()

        # calculate the centerhalf of the explorer window
        x_center = int(screen_width * 0.75)
        y_center = int(screen_height * 0.5)

        # move mouse to the center of the folder
        pyautogui.moveTo(x_center, y_center)

        # click on the center of the folder
        pyautogui.click()

        pyautogui.hotkey("ctrl", "a")

        time.sleep(1)

        drop_x = int(screen_width * 0.25)
        drop_y = int(screen_height * 0.5)

        pyautogui.moveTo(drop_x, drop_y)

        pyautogui.mouseUp()

        time.sleep(1)

        print()

    else:
        pyautogui.hotkey(
            "command", "space", interval=0.2
        )  # pip install pyobjc-framework-ScriptingBridge
        time.sleep(1)
        pyautogui.write("Finder")
        pyautogui.press("enter")
        time.sleep(1)
        pyautogui.hotkey("command", "shift", "g")
        time.sleep(0.5)
        pyautogui.write(folder_path)
        pyautogui.press("enter")
        time.sleep(1)

        mouse_x, mouse_y = pyautogui.position()
        current_screen = get_current_screen_mac(mouse_x, mouse_y)

        if current_screen:
            screen_number = NSScreen.screens().index(current_screen)
            print(f"Mouse is currently on screen {screen_number}")
            finder_window = get_finder_window_mac(current_screen)
            if finder_window:
                click_on_window_mac(finder_window)
                print("Clicked on the Finder window")
            else:
                print("No Finder window found on the current screen")
        else:
            print("Mouse is not on any screen")
