import os
import sys

import cv2

from celer_sight_ai import config
from celer_sight_ai.config import (
    BUTTON_COLS,
    BUTTON_HEIGHT,
    BUTTON_PADDING_LEFT,
    BUTTON_PADDING_TOP,
    BUTTON_SPACING,
    BUTTON_THUMBNAIL_MIN_SIZE,
    BUTTON_WIDTH,
)

if config.is_executable:
    sys.path.append(str(os.environ["CELER_SIGHT_AI_HOME"]))
import logging

from PyQt6 import QtCore, QtGui, QtWidgets

from celer_sight_ai import config
from celer_sight_ai.gui.custom_widgets.scene import readImage

logger = logging.getLogger(__name__)


logger.info("first part addbutton")

from celer_sight_ai.gui.designer_widgets_py_files.MaskButtonWidgetSofia import (
    Ui_Form as MaskWidget,
)
from celer_sight_ai.io.image_reader import (
    post_proccess_image,
)


def get_button_positions(amount_of_buttons, collumns):
    positions = [
        (i, j)
        for i in range(int(amount_of_buttons // collumns) + 1)
        for j in range(collumns)
    ]
    return positions


class AddButtonHandler(QtWidgets.QWidget):
    """
    A class that handles all added buttons,
    It is created right when the program starts
    or
    When we open a file the old istance is deleted and a new is created
    """

    def __init__(self, parent):
        super(QtWidgets.QWidget, self).__init__(parent)
        self.DictThumbnail = {}  # dictionary for all tumbnails
        self.DictVisibility = {}  # Dictionary that "Hides" unsused images
        self.DictIncludeInAnalysis = (
            {}
        )  # Dictionary that shows if an image is included in our analys
        self.DictButtons = {}
        # add default group TODO: this needs to change for group support
        self.DictButtons["default"] = {}
        self.DictMaskThumbnails = {}
        self.DictMaskButtons = {}
        self.num_elem_width = 3
        self._CurrentCondition = ""
        self.SelectedAssetButton = -1

        self.MainWindow = parent
        config.global_signals.loadedImageToRam.connect(self.setButtonLoaded)
        config.global_signals.spawn_button_from_image_url_signal.connect(
            self.spawn_button_from_image_url
        )

        #
        config.global_signals.load_image_to_preview_button_signal.connect(
            self.load_image_to_preview_button
        )

        # update the button mini-image
        config.global_signals.AddPixmapFromImageSignal.connect(
            self.AddPixmapFromImageSignalHandler
        )

    def SelectMaskAssetButton(self):
        """
        This function runs every time
        changes the seelcted mask widget color and updates text
        in the Mastercombobox in overview tabs
        """

        icon_bool = QtGui.QIcon()
        icon_bool.addPixmap(QtGui.QPixmap("data/icons/worm.png"))
        icon_polygon = QtGui.QIcon()
        icon_polygon.addPixmap(QtGui.QPixmap("data/icons/pentagon1.png"))

        try:
            for i in range(
                len(
                    self.parent().DH.AssetMaskDictionary[
                        self.parent().DH.BLobj.get_current_condition()
                    ][self.parent().current_imagenumber]
                )
            ):
                maskAssetItem = self.parent().DH.AssetMaskDictionary[
                    self.parent().DH.BLobj.get_current_condition()
                ][self.parent().current_imagenumber][i]
                maskAssetItem.setStyleSheet(
                    "QFrame#MaskWidgetFrame{"
                    + "border-width: 2px;"
                    + "border-color:"
                    + str(maskAssetItem.SelectedColor)
                    + ";}"
                )

            self.parent().DH.AssetMaskDictionary[
                self.parent().DH.BLobj.get_current_condition()
            ][self.parent().current_imagenumber][
                self.parent().selected_mask
            ].AnnotationTypeReference.setIcon(
                icon_bool
            )
            self.parent().DH.AssetMaskDictionary[
                self.parent().DH.BLobj.get_current_condition()
            ][self.parent().current_imagenumber][
                self.parent().selected_mask
            ].setStyleSheet(
                "QFrame#MaskWidgetFrame{"
                + "border-width: 2px;"
                + "border-color:"
                + str(maskAssetItem.SelectedColor)
                + ";}"
            )
            self.parent().DH.AssetMaskDictionary[
                self.parent().DH.BLobj.get_current_condition()
            ][self.parent().current_imagenumber][
                self.parent().selected_mask
            ].SetColorNameOfAnnotation()
            self.parent().DH.AssetMaskDictionary[
                self.parent().DH.BLobj.get_current_condition()
            ][self.parent().current_imagenumber][
                self.parent().selected_mask
            ].GetComboboxItems()

            # except Exception as e:
            #     logger.info("Error while adding stuleshit to polygon mask")
            #     logger.info(e)
            self.parent().DH.AssetMaskDictionaryPolygon[
                self.parent().DH.BLobj.get_current_condition()
            ][self.parent().current_imagenumber][
                self.parent().selected_mask
                - len(self.parent().DH.all_masks[self.parent().current_imagenumber])
            ].SetColorNameOfAnnotation()
            self.parent().DH.AssetMaskDictionaryPolygon[
                self.parent().DH.BLobj.get_current_condition()
            ][self.parent().current_imagenumber][
                self.parent().selected_mask
                - len(self.parent().DH.all_masks[self.parent().current_imagenumber])
            ].GetComboboxItems()
        except Exception as p:
            logger.info(p)

    def DeleteMaskAssetButton(self, Number, MaskType="BOOL"):
        try:
            self.parent().DH.AssetMaskDictionary[
                self.parent().DH.BLobj.get_current_condition()
            ][self.parent().current_imagenumber][Number].setParent(None)
            self.parent().DH.AssetMaskDictionary[
                self.parent().DH.BLobj.get_current_condition()
            ][self.parent().current_imagenumber][Number].disconnect()
            self.parent().DH.AssetMaskDictionary[
                self.parent().DH.BLobj.get_current_condition()
            ][self.parent().current_imagenumber][Number].deleteLater()
            del self.parent().DH.AssetMaskDictionary[
                self.parent().DH.BLobj.get_current_condition()
            ][self.parent().current_imagenumber][Number]

        except Exception as p:
            logger.info(p)
            logger.info(
                self.parent().DH.AssetMaskDictionary[
                    self.parent().DH.BLobj.get_current_condition()
                ][self.parent().current_imagenumber]
            )

    def ShowNewCondition(self, Mode="IMAGE", condition=None):
        """
        REmoves all the buttons from overview mdoe can be eiuther image or mask
        """
        import numpy as np

        if condition == None:
            condition = self.parent().DH.BLobj.get_current_condition()
        width = 2
        if (
            self.parent().DH.BLobj.get_current_condition()
            not in self.MainWindow.DH.BLobj.groups[
                str(self.parent().DH.BLobj.get_current_group())
            ].conds.keys()
        ):
            return

        if Mode == "IMAGE":
            self.MainWindow.images_preview_graphicsview.clear_out_visible_buttons()  # current condition
            self.MainWindow.images_preview_graphicsview.update_visible_buttons(
                force_update=True
            )  # current condition

    def import_images_with_file_dialog(self, folder_to_read_images_from=None):
        """Opens a prompt to select images and then imports them into the current condition"""
        from celer_sight_ai.gui.custom_widgets.file_explorer_dialogs import (
            import_images_handler,
        )

        if folder_to_read_images_from:
            from glob import glob

            images_urls = glob(os.path.join(folder_to_read_images_from, "*"))
        else:
            images_urls = import_images_handler()
        if not images_urls:
            return
        # check if current condition is none
        if self.MainWindow.DH.BLobj.get_current_condition() == None:
            # create one
            self.MainWindow.addRNAi_button_list.click()
            QtWidgets.QApplication.processEvents()
        self.SetUpButtons(
            self.MainWindow.DH.BLobj.get_current_condition(),
            self.MainWindow,
            imagesUrls=images_urls,
        )
        logger.info(f"Reading image url as individual images {images_urls}")

    def SetUpTextRegionAttribute(self, MaskAssetListDict):
        for key, Item in MaskAssetListDict.items():
            for i in range(len(MaskAssetListDict[key])):  # for every image
                for x in range(len(MaskAssetListDict[key][i])):  # for every mask asset
                    MaskAssetListDict[key][i][
                        x
                    ].BBWidget.MaskPropertiesWidgetLabelcomboBox.setText(
                        MaskAssetListDict[key][i][x].RegionAttribute
                    )

    def AppendMaskWidget(
        self, Mask, MaskType="BOOL", PositionToAddImage=None, PositionToAddMask=None
    ):
        """
        Adds a mask widget per condition BOOL or POLYGON
        NOT USED
        """
        return

    def setButtonLoaded(self, MyList):
        """
        shows that the button has the FULL image loaded to ram
        """
        ConditionName = MyList[0]
        buttonNumber = MyList[1]
        try:
            checkLabel = self.DictButtons["default"][ConditionName][
                buttonNumber
            ].findChild(QtWidgets.QLabel, "checkLabel")
        except:
            return
        checkLabel.show()
        return

    def updateCurrentCondition(
        self,
    ):
        """
        Updates the current condition for the button as its not always in sync with the current condition on CelerSight main
        """
        from celer_sight_ai import config

        logger.debug("updating current condition")
        self.parent().DH.BLobj.set_current_condition(
            self.parent().RNAi_list.currentItem().text()
        )

        return

    # def lunch_thread_load_image_to_preview_button(self, signal_object):
    #     """
    #     Loads the image to the preview button , buttons needs to have been loaded already
    #     """
    #     from celer_sight_ai.gui.Utilities.threader import Threader

    #     if config.user_cfg["USER_WORKERS"]:
    #         t = Threader(
    #             target_function=self.load_image_to_preview_button, args=(signal_object,)
    #         )
    #         t.start()
    #     else:
    #         self.load_image_to_preview_button(signal_object)

    @config.threaded
    def load_image_to_preview_button(self, signal_object):
        # loads image to preview button if image.preview does not exist
        # if its computed then just load it from there
        # create entry
        # check to see if DH has the image preview loaded before:
        image_uuid = signal_object[0]
        cond_uuid = signal_object[1]
        group_id = signal_object[2]
        # wait until we have finished importing to show
        # if its multiprocess only check this:
        if config.user_cfg["USER_WORKERS"]:
            while self.MainWindow.images_preview_graphicsview._is_updating_buttons:
                import time

                time.sleep(0.0005)
        cond_object = self.MainWindow.DH.BLobj.get_condition_by_uuid(cond_uuid)
        if not cond_object:
            return
        image_object = cond_object.images[image_uuid]
        if not image_object:
            return
        img_url = image_object.get_path()
        try:
            if not image_object.thumbnailGenerated:
                # if its a video, read the first frame
                logger.debug("Image preview not found, reading it")
                # use getImage method here to record the variables
                img_arr = cond_object.getImage(
                    image_object.imgID,
                    for_thumbnail=True,
                    avoid_loading_ultra_high_res_arrays_normaly=True,
                )  # this image can still be 16 bit  # this image can still be 16 bit
                channels = image_object.channel_list
                button = self.MainWindow.DH.BLobj.get_button_by_uuid(
                    image_object.unique_id
                )
                if not button:
                    return
                if isinstance(img_arr, type(None)) and image_object.is_remote():
                    logger.debug("Skipping loading nonexistent remote image")
                    return
                elif (
                    isinstance(img_arr, type(None)) and not image_object.is_remote()
                ):  # case image is not read correctly
                    logger.error(f"Error loading image from {img_url}")
                    # emit single delete button
                    button.marked_for_deletion = True
                    # The above code is hiding a button widget in a dictionary of buttons. The button is
                    # identified by its group_id, cond_id, and img_id.
                    # TODO: this needs to be threaded
                    if button.button_instance:
                        object = {
                            "group_name": group_id,
                            "treatment_uuid": cond_uuid,
                            "image_uuid": image_object.unique_id,
                        }
                        config.global_signals.delete_image_with_button_signal.emit(
                            object
                        )

                    return
                else:  # case image is read correctly and preview is to be generated
                    logger.debug("Image is read sucessfully, creating thumbnail image")
                    img_arr_display, min_val, max_val = post_proccess_image(
                        img_arr, channels, to_uint8=True, to_rgb=True, has_min_max=False
                    )
                    image_object.channel_list = channels
                    cond_object.set_thumbnail(
                        image_uuid=image_object.unique_id, imageRef=img_arr_display
                    )
                    # if the image is ultra high res, add the thumbnail to the scene
                    if image_object._is_ultra_high_res:
                        # refresh scene
                        config.global_signals.load_main_scene_signal.emit()
                    #  save time by doing a resize of the original image
                    #  get minimum dimention
                    min_dim = min(img_arr_display.shape[0], img_arr_display.shape[1])
                    # calculate the resize factor using BUTTON_THUMBNAIL_MIN_SIZE
                    scaleChange = BUTTON_THUMBNAIL_MIN_SIZE / min_dim
                    thumbnail = cv2.resize(
                        img_arr_display,
                        (0, 0),
                        fx=scaleChange,
                        fy=scaleChange,
                        interpolation=cv2.INTER_AREA,
                    )
                    logger.debug("Thumbnail created")
            else:
                #  fetching the thumbnail from memory
                logger.debug("Image preview found, fetching it from memory")
                if not cond_object:
                    return
                thumbnail = cond_object.get_thumbnail(
                    image_uuid=image_object.unique_id, for_button=True
                )
            config.global_signals.AddPixmapFromImageSignal.emit(
                [group_id, cond_uuid, image_object.unique_id, thumbnail]
            )
        except Exception as e:
            import traceback

            logger.error(f"Error loading image from {img_url} : {e}")
            # get traceback on debug
            logger.debug(traceback.format_exc())
        return

    def AddPixmapFromImageSignalHandler(self, signal_obj):
        # this function is used to update the p
        group_id = signal_obj[0]
        cond_uuid = signal_obj[1]
        image_uuid = signal_obj[2]
        thumbnail = signal_obj[3]
        # check if button instance exists
        cond_object = self.MainWindow.DH.BLobj.get_condition_by_uuid(cond_uuid)
        if not cond_object:
            return
        try:
            button = self.MainWindow.DH.BLobj.get_button_by_uuid(image_uuid)
            if not button:
                logger.error("Button not found")
                return
        except Exception as e:
            logger.error(f"Error getting button {e}")
            return
        if button.button_instance_proxy is not None:
            if button.button_instance:
                try:
                    button.button_instance.AddPixmapFromImage(
                        thumbnail, image_uuid=image_uuid
                    )
                    image_object = cond_object.images[image_uuid]
                    image_object.thumbnailGenerated = True
                    image_object.setButtonReference(button.button_instance)
                    image_object.setup_channels()
                except Exception as e:
                    logger.info(f"Buton did not load all the way : {e}")

    def append_video_object_to_data_handler(self, signal_object):
        import time

        import numpy as np

        from celer_sight_ai.gui.custom_widgets.scene import image_to_uint8, readImage

        img_id = signal_object.get("image_idx")
        cond_id = signal_object.get("condition_id")
        group_uuid = signal_object.get("group_uuid")
        video_url = signal_object.get("video_url")
        terminal_load = signal_object.get("terminal_load")
        annotations = signal_object.get("annotations")
        raise NotImplementedError("Configure treatment and group ids properly")
        self.MainWindow.DH.BLobj.groups[group_id].conds[cond_id].add_video_from_disk(
            video_url, group_id, cond_id, img_id
        )

    def append_image_object_to_data_handler(self, signal_object):
        # TODO: this method needs to opperate by uuids and not indexes and names.
        # Adds an image object to the data handler.

        img_idx = signal_object.get("image_idx")
        treatment_uuid = signal_object.get("treatment_uuid")
        group_uuid = signal_object.get("group_uuid")
        img_url = signal_object.get("image_url")
        terminal_load = signal_object.get("terminal_load")
        annotations = signal_object.get("annotations")
        check_overlap = signal_object.get("check_overlap")

        condition_object = self.MainWindow.DH.BLobj.get_condition_by_uuid(
            treatment_uuid
        )

        if img_url.startswith("celer_sight_ai:"):
            # add remote annotation
            image_object = condition_object.add_image_from_url(
                img_url,
                group_uuid,
                treatment_uuid,
                imageId=img_idx,  # uuid is in the file's name
            )
            # get remote polygons
            remote_annos = config.client.get_remote_annotations_for_image(
                {"image_uuid": image_object.unique_id}
            )
            config.global_signals.create_annotations_objects_signal.emit(
                [
                    {
                        "treatment_uuid": treatment_uuid,
                        "group_uuid": group_uuid,
                        "array": anno["data"],  # m -> QPolygonF object
                        "image_uuid": image_object.unique_id,
                        "class_id": anno["class"],
                        "mask_type": anno["type"],
                        "allow_sending_remote": False,
                        "mask_uuid": anno.get("annotation_uuid", None),
                        "check_overlap": check_overlap,
                    }
                    for anno in remote_annos
                ]
            )

        else:
            image_object = condition_object.addImage_FROM_DISK(
                img_url, group_uuid, treatment_uuid  # uuid is in the file's name
            )

            #  if provided annotations, populate iamge
            if not isinstance(annotations, type(None)):
                if annotations:
                    config.global_signals.create_annotations_objects_signal.emit(
                        [
                            {
                                "treatment_uuid": treatment_uuid,
                                "group_uuid": group_uuid,
                                "array": m["polygon"],
                                "image_uuid": image_object.unique_id,
                                "class_id": m["class"],
                                "mask_type": "polygon",
                                "check_overlap": check_overlap,
                            }
                            for m in annotations
                        ]
                    )
        # if the image is the current image reload the scene
        if image_object.unique_id == self.MainWindow.DH.BLobj.get_current_image_uuid():
            config.global_signals.load_main_scene_and_fit_in_view_signal.emit()
        if terminal_load:
            config.global_signals.unlock_ui_signal.emit()
            QtWidgets.QApplication.processEvents()
            config.global_signals.refresh_image_preview_graphicsscene_signal.emit()  # loads the thumbnails
            self.MainWindow.custom_class_list_widget.update_and_restructure_classes()
            # refresh the
        # trigger a refresh of the image preview area (graphics view)

    def clean_up_failed_loaded_buttons(self, group_id, cond_id):
        # iterate over all buttons for this conditions
        # Depreciated function - > instead do this while the button is loading.
        all_buttons_to_delete = []
        for b in self.DictButtons[group_id][cond_id]:
            if b.marked_for_deletion:
                all_buttons_to_delete.append(b)
        # sort from biggest .image_id to smallest
        all_buttons_to_delete = sorted(
            all_buttons_to_delete, key=lambda x: x.image_id, reverse=True
        )
        # delete:
        for b in all_buttons_to_delete:
            QtWidgets.QApplication.processEvents()
            b.deleteCurrentImage(reload_image=False)
        QtWidgets.QApplication.processEvents()
        if len(all_buttons_to_delete) != 0:
            all_buttons_to_delete[0].rearrange_buttons(adjust_image_id=False)

    def spawn_button_from_image_url(self, signal_object):
        # starts the process of spawning a button, button is created and image preview is loaded later.
        import time

        img_id_in_frame = signal_object[0]
        cond_uuid = signal_object[1]
        group_uuid = signal_object[2]
        img_url = signal_object[3]
        terminal_load = signal_object[
            4
        ]  # if None then ignore , if list - > instance seg, elif dict -> deside TODO:implement for all annotation types
        annotations = signal_object[5]
        # add image data to MainWindow.DH.BLobj
        self.append_image_object_to_data_handler(
            [
                img_id_in_frame,
                cond_uuid,
                group_uuid,
                img_url,
                terminal_load,
                annotations,
            ]
        )

        # place holder QRectF

    def SetUpButtons(
        self,
        NameOfCondtion,
        Ui_MainWindow,
        FromSavedFile=False,
        PreComputedMask=False,
        loadImages=True,
        imagesUrls=None,
        all_annotations=None,  # precomputed annotations
        check_for_videos=False,
    ):
        """
        This function is responsible for addnig a layout and setting up Assetbuttons
        """
        import numpy as np

        from celer_sight_ai import config
        from celer_sight_ai.gui.custom_widgets.scene import is_video_file

        # if condition already exists and there are images set for it, dont  set_common_name
        # if the text condition or treatment exists within the treatment name , also rename acording to the file filename
        if (
            not len(
                self.MainWindow.DH.BLobj.groups[
                    self.MainWindow.DH.BLobj.get_current_group()
                ]
                .conds[NameOfCondtion]
                .images
            )
            and (
                "condition" not in self.MainWindow.RNAi_list.currentItem().text()
                or "treatment" not in self.MainWindow.RNAi_list.currentItem().text()
            )
            > 0
        ):
            common_condition_name = (
                self.MainWindow.DH.BLobj.groups[
                    self.MainWindow.DH.BLobj.get_current_group()
                ]
                .conds[NameOfCondtion]
                .set_common_condition_name([os.path.basename(i) for i in imagesUrls])
            )
        else:
            common_condition_name = None
        if common_condition_name:
            self._CurrentCondition = common_condition_name
            NameOfCondtion = common_condition_name
            self.MainWindow.DH.BLobj.set_current_condition(common_condition_name)
            # change condition dicts
            prev_text = self.MainWindow.RNAi_list.currentItem().text()
            self.MainWindow.updateDictionariesWithNewKeys(
                [self.MainWindow.RNAi_list.currentItem().text(), common_condition_name]
            )
            self.MainWindow.RNAi_list.currentItem().setText(common_condition_name)

        else:
            self._CurrentCondition = NameOfCondtion

        config.global_signals.lock_ui_signal.emit(["left_group", "image_viewer"])
        QtWidgets.QApplication.processEvents()
        self.MainWindow.DH.BLobj.importing_images += 1  # TODO: add -1 on the last image

        # Calculate the position of Every button
        maxNumberOfButtons = len(imagesUrls) + 10000

        values = np.array([i for i in range(maxNumberOfButtons)])
        iter_buttons = 0

        Ui_MainWindow.DH.included_image_list = []
        Ui_MainWindow.i_am_drawing_state = False
        Ui_MainWindow.add_mask_btn_state = False
        Ui_MainWindow.selection_state = False  # weather or not we can aselect a mask
        Ui_MainWindow.sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Minimum
        )
        Ui_MainWindow.sizePolicy.setHorizontalStretch(0)
        Ui_MainWindow.sizePolicy.setVerticalStretch(0)

        logger.debug("Check to see how to replace image_preview_scrollArea_Contents")
        if (
            self._CurrentCondition
            in self.MainWindow.DH.BLobj.groups["default"].conds.keys()
        ):
            values = list(
                range(
                    0,
                    len(
                        self.MainWindow.DH.BLobj.get_all_buttons(
                            "default", self._CurrentCondition
                        )
                    )
                    + 1
                    + max(values),
                )
            )
            valuesToSkip = list(
                range(
                    0,
                    len(
                        self.MainWindow.DH.BLobj.get_all_buttons(
                            "default", self._CurrentCondition
                        )
                    ),
                )
            )
        else:
            valuesToSkip = []

        condition = self._CurrentCondition
        group = self.MainWindow.DH.BLobj.get_current_group()

        # update graphicsscene in image preview area

        self.MainWindow.images_preview_graphicsview.scene().setSceneRect(
            QtCore.QRectF(
                0,
                0,
                self.MainWindow.images_preview_graphicsview.viewport().width(),
                max(
                    (
                        len(
                            self.MainWindow.DH.BLobj.groups["default"].conds[
                                self.MainWindow.DH.BLobj.get_current_condition()
                            ]
                        )
                        + (len(values) + 1)
                    )
                    * ((BUTTON_HEIGHT // BUTTON_COLS) + BUTTON_SPACING),
                    300,
                ),
            )
        )

        # get treatment uuid
        treatment_uuid = self.MainWindow.DH.BLobj.get_current_condition_uuid()
        group_uuid = self.MainWindow.DH.BLobj.get_current_group_uuid()
        # if current image number is negative, set to positive

        for value in values:
            total_img_id = value
            logger.info(
                f"Adding image for Condition {NameOfCondtion} at position {value} "
            )
            if total_img_id in valuesToSkip:
                continue

            if len(imagesUrls) + len(valuesToSkip) <= total_img_id:
                break

            if iter_buttons == len(imagesUrls) - 1:
                terminal_load = True
            else:
                terminal_load = False
            current_annotation = None
            if not isinstance(all_annotations, type(None)):
                if len(all_annotations) > iter_buttons:
                    current_annotation = all_annotations[iter_buttons]

            if check_for_videos and is_video_file(imagesUrls[iter_buttons]):
                logger.info(
                    f"Importing data for button / video {imagesUrls[iter_buttons]}"
                )
                self.append_video_object_to_data_handler(
                    {
                        "image_idx": total_img_id,
                        "treatment_uuid": treatment_uuid,
                        "group_uuid": group_uuid,
                        "video_url": imagesUrls[iter_buttons],
                        "terminal_load": terminal_load,
                        "annotations": current_annotation,
                    }
                )

            else:
                logger.info(
                    f"Importing data for button / image {imagesUrls[iter_buttons]}"
                )
                self.append_image_object_to_data_handler(
                    {
                        "image_idx": total_img_id,
                        "treatment_uuid": treatment_uuid,
                        "group_uuid": group_uuid,
                        "image_url": imagesUrls[iter_buttons],
                        "terminal_load": terminal_load,
                        "annotations": current_annotation,
                    }
                )

            iter_buttons += 1

    def UpdateDicts(self, OldName, NewName):
        import copy

        """
        A functoin that renames the dictionaries in the add button class
        """
        self.DictButtons["default"][NewName] = copy.copy(
            self.DictButtons["default"][OldName]
        )
        self.DictThumbnail[NewName] = copy.copy(self.DictThumbnail[OldName])
        self.DictVisibility[NewName] = copy.copy(
            self.DictVisibility[OldName]
        )  # Dictionary that "Hides" unsused images
        self.DictIncludeInAnalysis[NewName] = copy.copy(
            self.DictIncludeInAnalysis[OldName]
        )  # Dictionary that shows if an image is included in our analys
        del self.DictButtons["default"][OldName]
        del self.DictThumbnail[OldName]
        del self.DictVisibility[OldName]
        del self.DictIncludeInAnalysis[OldName]

        # Update current conditnion (maybe we can skip this with some udjustments)
        self._CurrentCondition = NewName

    def InitDicts(self, NameOfCondtion, ListOfbuttons, Images):
        if str(NameOfCondtion) in self.DictButtons["default"].keys():
            self.DictButtons["default"][str(NameOfCondtion)].extend(ListOfbuttons)
            self.DictThumbnail[str(NameOfCondtion)].extend(Images)
            self.DictVisibility[str(NameOfCondtion)].extend(
                [
                    True
                    for i in range(
                        len(self.DictButtons["default"][str(NameOfCondtion)])
                    )
                ]
            )  # Dictionary that "Hides" unsused images
            self.DictIncludeInAnalysis[str(NameOfCondtion)].extend(
                [
                    True
                    for i in range(
                        len(self.DictButtons["default"][str(NameOfCondtion)])
                    )
                ]
            )  # Dictionary that shows if an image is included in our analys
        else:
            self.DictButtons["default"][str(NameOfCondtion)] = ListOfbuttons.copy()
            self.DictThumbnail[str(NameOfCondtion)] = Images.copy()
            self.DictVisibility[str(NameOfCondtion)] = [
                True
                for i in range(len(self.DictButtons["default"][str(NameOfCondtion)]))
            ]  # Dictionary that "Hides" unsused images
            self.DictIncludeInAnalysis[str(NameOfCondtion)] = [
                True
                for i in range(len(self.DictButtons["default"][str(NameOfCondtion)]))
            ]  # Dictionary that shows if an image is included in our analys

    def OnImageClickSetActive(self, ImageNumber):
        self.MainWindow.DH.get_button(
            "default", self._CurrentCondition, ImageNumber
        ).toggle()

    def SetCheckToFalse(self, ButtonID):
        """
        When the button is clicked this means that we have seen the picture of itnerest
        and thus it has been processed by the user, creating this way a map for any images
        that we might have missed
        """
        btn = self.MainWindow.DH.get_button("default", self._CurrentCondition, ButtonID)
        if btn:
            btn._IsChecked = True
            if btn.button_instance:
                btn.button_instance.setStyleSheet(
                    """
                QPushButton{
                background-color:#262526 ;  
                }
                
                QPushButton:pressed{
                background-color: #b1b1b1;
                }
                """
                )

    def SetCheckToTrue(self, ButtonID):
        """
        When the button is clicked this means that we have seen the picture of itnerest
        and thus it has been processed by the user, creating this way a map for any images
        thait we might have missed
        """

        btn = self.MainWindow.DH.get_button("default", self._CurrentCondition, ButtonID)
        if btn:
            btn._IsChecked = True
            if btn.button_instance:
                btn.button_instance.setStyleSheet(
                    """
                    QFrame{
                    background-color: #007300;  
                    }
                
                    """
                )

    def CheckAnalysisStatus(self, ButtonId):
        """
        Check the analysis status of all of the buttons
        if one is not included then stylesheed and make red background
        """
        return
        # self.DictIncludeInAnalysis[self._CurrentCondition][ButtonId] = self.DictButtons[self._CurrentCondition][
        #     ButtonId]._IncludedInAnalysis

        # if self.DictIncludeInAnalysis[self._CurrentCondition][ButtonId] == False:
        #     self.DictButtons[self._CurrentCondition][ButtonId].setStyleSheet(
        #         """
        #         QPushButton{
        #         background-color: #FF0000;
        #         }

        #         QPushButton:pressed{
        #         background-color: #FF0000;
        #         }
        #         """
        #     )
        # elif self.DictIncludeInAnalysis[self._CurrentCondition][ButtonId] == True:
        #     # if
        #     self.DictButtons[self._CurrentCondition][ButtonId].setStyleSheet(
        #         """
        #         QPushButton:pressed{
        #         background-color: #b1b1b1;
        #         }

        #         QPushButton{
        #         background-color: #b1b1b1;
        #         }
        #         """
        #     )

    def ResetUserCheckedStatus(self):
        """
        This function resets all the buttons checked
        Status after the masks are generated
        """
        for item, value in self.DictButtons["default"].items():
            for button in self.DictButtons["default"][item]:
                button._IsChecked = False


if __name__ == "__main__":
    pass
