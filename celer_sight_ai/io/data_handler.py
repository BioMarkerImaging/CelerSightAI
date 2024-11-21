import logging
import cv2
import time
import os
import numpy as np
import pathlib
from pathlib import Path
from typing import Union

logger = logging.getLogger(__name__)

from celer_sight_ai import config
from celer_sight_ai.config import (
    BUTTON_WIDTH,
    BUTTON_HEIGHT,
    BUTTON_SPACING,
    BUTTON_PADDING_LEFT,
    BUTTON_PADDING_TOP,
    IMAGE_THUMBNAIL_MAX_SIZE,
    IMAGE_THUMBNAIL_JPEG_QUALITY,
    BUTTON_THUMBNAIL_MIN_SIZE,
)

from PyQt6 import QtCore, QtGui, QtWidgets

from celer_sight_ai.gui.custom_widgets.transparent_graphics_widget import TransparentGraphicsWidget

from celer_sight_ai.gui.custom_widgets.scene import readImage

import uuid

from celer_sight_ai.QtAssets.buttons.image_button import ImageButtonPlaceHolderClass

from typing import Generator, Any

from celer_sight_ai.io.image_reader import (
    post_proccess_image,
    combine_channels,
    getImage,
)


class HashList:
    def __init__(self):
        self._list = []
        self._dict = {}
        self._index_to_uuid = {}

    # get idx from uuid
    def get_index(self, uuid):
        for i, k in enumerate(self._dict):
            if k == uuid:
                return i

    # iter method follows list way of iterating
    def __iter__(self):
        return iter(self._list)

    def append(self, item):
        item_uuid = item.unique_id
        self._list.append(item)
        self._dict[item_uuid] = item
        self._index_to_uuid[len(self._list) - 1] = item_uuid

    def insert(self, index, item):
        item_uuid = item.unique_id
        self._list.insert(index, item)
        self._dict[item_uuid] = item
        self._update_index_to_uuid()

    def __getitem__(self, key):
        if isinstance(key, int):
            if key >= len(self._list):
                logger.error("Tried to access items out of bouds. Returning None")
                return None
            return self._list[key]
        elif isinstance(key, str):
            return self._dict[key]
        else:
            raise TypeError("Key must be an integer or a string")

    def __setitem__(self, key, value):
        if isinstance(key, int):
            if key >= len(self._list):
                raise IndexError("List index out of range")
            old_uuid = self._index_to_uuid[key]
            self._list[key] = value
            self._dict[old_uuid] = value
        elif isinstance(key, str):
            if key not in self._dict:
                raise KeyError("Key not found in dictionary")
            self._dict[key] = value
            list_index = list(self._index_to_uuid.values()).index(key)
            self._list[list_index] = value
        else:
            raise TypeError("Key must be an integer or a string")

    # create a pop method idential to __delitem__ and return the item
    def pop(self, key):
        if isinstance(key, int):
            if key >= len(self._list):
                raise IndexError("List index out of range")
            item_uuid = self._index_to_uuid.pop(key)
            item = self._dict.pop(item_uuid)
            del self._list[key]
            self._update_index_to_uuid()
            return item
        elif isinstance(key, str):
            if key not in self._dict:
                raise KeyError("Key not found in dictionary")
            item = self._dict.pop(key)
            list_index = list(self._index_to_uuid.values()).index(key)
            del self._list[list_index]
            del self._index_to_uuid[list_index]
            self._update_index_to_uuid()
            return item
        else:
            raise TypeError("Key must be an integer or a string")

    def __delitem__(self, key):
        if isinstance(key, int):
            # Delete from list by index
            item = self._list.pop(key)
            # Find and delete the corresponding item from the dictionary
            for dict_key, dict_item in list(self._dict.items()):
                if dict_item == item:
                    del self._dict[dict_key]
                    break
        elif isinstance(key, str):
            # Delete from dictionary by key
            item = self._dict.pop(key)
            # Find and delete the corresponding item from the list
            self._list = [x for x in self._list if x != item]
        else:
            raise TypeError("Key must be an integer or a string")
        self._update_index_to_uuid()
        del self.MainWindow.DH.BLobj.object_mapping[item.unique_id]

    def _update_index_to_uuid(self):
        self._index_to_uuid = {i: k for i, k in enumerate(self._dict)}

    def __len__(self):
        return len(self._list)

    def __repr__(self):
        return f"ListDict({self._list})"


def colorize_gray_image(image, rgb_val=(0, 0, 255)):
    """Colorize a grayscale image with the specified RGB color.

    Args:
        image: Grayscale input image
        rgb_val: Tuple of (R,G,B) values from 0-255 to colorize with

    Returns:
        Colorized image as uint8 array
    """
    import cv2
    import numpy as np

    # Create copies for each channel
    b = image.copy()
    g = image.copy()
    r = image.copy()

    # Scale RGB values to 0-1 range
    mr = rgb_val[0] / 255
    mg = rgb_val[1] / 255
    mb = rgb_val[2] / 255

    # Multiply each channel by its color component
    np.multiply(r, mr, out=r, casting="unsafe")
    np.multiply(g, mg, out=g, casting="unsafe")
    np.multiply(b, mb, out=b, casting="unsafe")

    # Merge channels in BGR order for OpenCV
    after = cv2.merge([b, g, r])

    # Normalize to uint8 range
    after = cv2.normalize(after, None, 0, 255, cv2.NORM_MINMAX, cv2.CV_8U)
    return after


def overlaps(a, b):
    return a[0] <= b[1] and b[0] <= a[1]


def build_graph(intervals):
    n = len(intervals)
    graph = {i: [] for i in range(n)}
    for i in range(n):
        for j in range(i + 1, n):
            if overlaps(intervals[i], intervals[j]):
                graph[i].append(j)
                graph[j].append(i)
    return graph


def find_minimum_groups(intervals):
    """
    Find minimum groups of overlapping intervals.
    All intervals in a group need to overlap with each other.
    Handles cases where some classes don't have annotations.
    """
    from networkx import Graph, find_cliques

    # Filter out None values and keep track of original keys
    valid_intervals = {k: v for k, v in intervals.items() if v is not None}

    if not valid_intervals:
        return []

    # Create mapping between original keys and graph indices
    key_to_idx = {key: i for i, key in enumerate(valid_intervals.keys())}
    idx_to_key = {i: key for key, i in key_to_idx.items()}

    # Build graph using indices
    graph = build_graph(list(valid_intervals.values()))
    G = Graph(graph)
    cliques = list(find_cliques(G))

    if not cliques:
        return [
            [k] for k in intervals.keys()
        ]  # Return all keys, including those with None values

    groups = []
    remaining_keys = set(intervals.keys())  # Include all original keys

    # Convert clique indices back to original keys
    for clique in sorted(cliques, key=len, reverse=True):
        if not remaining_keys:
            break

        # Map indices back to original keys
        group = [idx_to_key[i] for i in clique]
        if group:
            groups.append(group)
            remaining_keys -= set(group)

    # Add any remaining keys as individual groups
    groups.extend([[k] for k in remaining_keys])

    return groups


def get_tile_range_from_group(group) -> tuple:
    """
    Finds the maximum minimum and the minimum maximum tile size of the group.
    This ensures that the selected tile size works for all ranges in the group.

    Args:
        group (list): list of tuples of the form (min, max)

    Returns:
        tuple: (min_val, max_val)

    Example:
        >>> ranges = [(100, 500), (200, 800), (150, 400)]
        >>> min_val, max_val = get_tile_range_from_group(ranges)
        >>> print(min_val, max_val)
        200 400
        # 200 is the largest minimum (ensures all ranges start below tile size)
        # 400 is the smallest maximum (ensures all ranges can handle tile size)

        >>> ranges_with_none = [(100, 500), None, (150, 400)]
        >>> min_val, max_val = get_tile_range_from_group(ranges_with_none)
        >>> print(min_val, max_val)
        150 400
        # None values are filtered out before processing
    """
    valid_ranges = [r for r in group if r is not None]
    if not valid_ranges:
        return None, None

    min_val = max(r[0] for r in valid_ranges)
    max_val = min(r[1] for r in valid_ranges)

    return min_val, max_val


def group_ranges_to_tile_size(
    min_groups: list,
    class_mask_sizes: dict,
    optimal_annotation_ranges_and_image_size: dict,
) -> dict:
    """
    Given a group of ranges, find the optimal tile size in each group, it should be the average of the
    allowed min and max range
    """
    result = {}
    for group in min_groups:
        min_val, max_val = get_tile_range_from_group(
            [class_mask_sizes[i] for i in group]
        )
        if min_val is not None and max_val is not None:
            # get the max image size needed for the group
            max_image_size = max(
                [optimal_annotation_ranges_and_image_size[i]["img_size"] for i in group]
            )
            result[tuple(group)] = {
                "tile_size": (min_val + max_val) / 2,
                "image_size": max_image_size,
            }
        else:
            result[tuple(group)] = None
    return result


class DataHandler(object):
    """
    Class for the handling of  'large' arrays that need storing or proccessing
    """

    def __init__(self, MainWindow):
        super(DataHandler, self).__init__()
        self.MainWindow = MainWindow
        self.BLobj = CelerSightObj(self.MainWindow)
        self.BLobj.newAnalysis(self)

        # a list of anlysis metrics computed, this is used to populate the combobox on the analysis page
        self.analysis_metrics_named = []
        # a list of channels that have been computed

        self.AssetMaskDictionary = {}
        self.AssetMaskDictionarySettings = {}
        self.AssetMaskDictionaryBool = {}  # Fixed
        self.AssetMaskListBool = []
        self.AssetMaskDictionaryBoolSettings = {}
        self.AssetMaskListBoolSettings = []
        self.AssetMaskDictionaryPolygon = {}  # Fixed
        self.AssetMaskListPolygon = []
        self.AssetMaskDictionaryPolygonSemasksttings = {}
        self.AssetMaskListPolygonSettings = []
        self.AnnotationRegions = {}
        self.circle_selection_image = cv2.imread(
            "data/icons/circle_Selection.png", -1
        )  # image for the on screen annoation
        self.image_names_all_RNAi = {}  # The name of the file # Fixed
        self.master_mask_list = (
            []
        )  # A mask generated to include all masks in one image for fast indexing with the mouse
        self.all_worm_mask_points_x = []  # The points from the polygon mask
        self.all_worm_mask_points_y = []
        self.image_names = []  # The list version of image_names_all_RNAi
        self.unique_masks_tmp = []  # TODO: This is not used, fix def slect_mask_clicked
        self.masks_state_usr = (
            []
        )  # list that indicates weather there is a mask generated by the user
        self.masks_state = []  # if there is a mask in the current image
        self.pixon_list_opencv = (
            []
        )  # This is a list with the original images in a numpy array
        self.all_masks = []  # This is a list that includes all of the BOOL masks
        self.all_masks_usr = []  # TODO: Remove this, its not used
        self.current_RNAi = 0  # TODO: remove this its not used
        self.dictionary_max_elements = 5  # TODO: remove this its not used
        self.added_to_dictionary_state = True  # TODO: remove this its not used
        self.image_RNAi_slots = {}  # Dictionary for pixon_list_opencv lists
        self.aa_review_state = False

        self.allAnalysisDataContainer = (
            {}
        )  # this dicionary includes all of the data for the spreadsheet,
        # its the carrently used and it usest he dictionaries below and its in the form of [analysis type][analysis subtype]

        # self.view_field_dictionary_slots = {} # TODO: remove this its not used
        self.mask_RNAi_slots = {}  # Dictionary for all_masks lists
        self.usr_mask_RNAi_slots = {}  # Dicitonary for all_masks_usr
        self.calculated_dictionary_state = False  # TODO: remove this its not used
        self.dict_aggs_lables_all_RNAi = {}  # TODO: remove this its not used
        self.dict_aggs_counts_all_RNAi = (
            {}
        )  # Dictionary of all the aggregate counts, after the analysis
        self.dict_aggs_volume_all_RNAi = (
            {}
        )  # Dictionary of all the aggregate volume, after the analysis
        self.dict_master_mask_list = {}  # TODO: remove this its not used
        self.dict_RNAi_attributes_all = (
            {}
        )  # Dictionary for storing masks  state masks state usr, calculated dictionary state, added to dictionary state, predict masks state
        self.all_worm_mask_points_x_slot = {}  # Dicionary for all_worm_mask_points_x
        self.all_worm_mask_points_y_slot = {}
        self.stacked_images_slot = (
            {}
        )  # Same as pixon_list_opencv dictionary? need to see whats going on here
        self.predict_masks_state = (
            False  # if we have generated the masks from the neural network
        )
        self.all_masksQPoints = []
        self.mask_RNAi_slots_QPoints = {}  # One used
        self.mask_RNAi_slots_QPolygon = {}
        # Lists for analysis
        ## lebel adds aggregates only
        self.aggs_lables_all_RNAi = []
        self.aggs_lables_RNAi = []
        self.aggs_lables_worm = []
        self.summary_counts_RNAi = []
        ## per count aggregates only
        self.aggs_counts_all_RNAi = []  #
        self.aggs_counts_RNAi = []
        self.aggs_counts_worm = []
        self.summary_counts_RNAi = []  #
        ## per volume aggregates only
        self.aggs_volume_all_RNAi = []  #
        self.aggs_volume_RNAi = []
        self.aggs_volume_worm = []
        self.summary_volume_RNAi = []  #
        self.dict_RNAi_attributes = {
            "predict_masks_state": self.predict_masks_state,
            "added_to_dictionary_state": self.added_to_dictionary_state,
            "calculated_dictionary_state": self.calculated_dictionary_state,
            "masks_state_usr": self.masks_state_usr,
            "masks_state": self.masks_state,
        }

        from celer_sight_ai.gui.custom_widgets.WarningWindow import WarningHandlerClass

        self.warningHandler = WarningHandlerClass()

    def reset_state(self):
        logger.info("Resetting state")
        self.BLobj = CelerSightObj(self.MainWindow)
        self.BLobj.newAnalysis(self)

    def get_all_buttons(self, group_id: str, condition_id: str) -> list:
        if condition_id:
            return [
                i.myButton
                for i in self.BLobj.groups[group_id].conds[condition_id].images
            ]
        else:
            return []

    def get_button(self, group_id, condition_id, image_id):
        logger.debug(f"Getting button for {group_id}, {condition_id}, {image_id}")
        if condition_id in self.BLobj.groups[group_id].conds:
            return (
                self.BLobj.groups[group_id]
                .conds[condition_id]
                .images[image_id]
                .myButton
            )
        else:
            return None

    def get_button_by_uuid(self, group_id=None, condition_uuid=None, image_uuid=None):
        logger.debug(f"Getting button for {group_id}, {condition_uuid}, {image_uuid}")
        condition_object = self.BLobj.get_condition_by_uuid(condition_uuid)
        if condition_object:
            image_object = condition_object.images[image_uuid]
            if image_object:
                return image_object.myButton
        else:
            return None


class CelerSightObj:  # contains group obj
    def __init__(self, MainWindow=None):
        self.groups = {}
        self.MainWindow = MainWindow

        self.totalGroups = 0
        #
        self.set_current_condition(None)
        self.classes_object_colors = (
            {}
        )  # all classes are here with the name and the color

        self.object_mapping = {}  # a dictionary that maps all uuids to objects

        config.global_signals.endAllInferenceLoadingSignals.connect(
            self.endAllInferenceAnimations
        )
        # initiate spawning of button, this needs to be reconnected
        # the the user quits the session, as the BLobj is deleted
        config.global_signals.create_button_instance_signal.connect(
            self.create_button_instance
        )

        self.importing_images = 0  # set to +1 when we are loading images,set to -1 when all images are loaded. 0 means all images are loaded form all groups
        self.set_current_group("default")

    def get_all_channels(self):
        # get all possible channels from all images
        channels = []
        for group in self.groups:
            for condition in self.groups[group].conds:
                for image in self.groups[group].conds[condition].images:
                    for channel in image.channel_list:
                        channels.append(channel)
        return [i for i in list(set(channels)) if i]

    def set_current_condition(self, condition_name: str | None = None) -> None:
        """
        Set the current condition for the CelerSight object.

        This method updates the current condition both in the CelerSight object
        and in the global user attributes.

        Args:
            condition_name (str, optional): The name of the condition to set as current.
                If None, the current condition will be set to None. Defaults to None.

        Returns:
            None
        """
        self.current_condition = condition_name
        config.user_attributes.current_condition = condition_name

    def get_image_number_from_image_uuid(self, image_uuid):
        # get image object
        image_object = self.get_image_object_by_uuid(image_uuid)
        # get the treatment its located in
        condition_object = self.get_condition_by_uuid(image_object.cond_uuid)
        # index the position of the image object
        return condition_object.images.index(image_object)

    def get_current_image_object(self):
        try:
            io = (
                self.groups[self.get_current_group()]
                .conds[self.get_current_condition()]
                .images
            )
            current_imagenumber = self.get_current_image_number()
            if current_imagenumber >= len(io):
                self.MainWindow.current_imagenumber = max(0, len(io) - 1)
            return io[self.MainWindow.current_imagenumber]
        except:
            config.global_signals.errorSignal.emit(
                "No image found. Please add an image to process."
            )
            if (
                not len(self.groups)
                or not len(self.groups[self.get_current_group()].conds)
                or not len(
                    self.groups[self.get_current_group()]
                    .conds[self.get_current_condition()]
                    .images
                )
            ):
                return None
            # return the latest image and update current imagenumber
            self.MainWindow.current_imagenumber = (
                len(
                    self.groups[self.get_current_group()]
                    .conds[self.get_current_condition()]
                    .images
                )
                - 1
            )
            return (
                self.groups[self.get_current_group()]
                .conds[self.get_current_condition()]
                .images[self.get_current_image_number()]
            )

    def get_image_object_by_uuid(self, image_uuid):
        for group in self.groups:
            for condition in self.groups[group].conds:
                for image in self.groups[group].conds[condition].images:
                    if image.unique_id == image_uuid:
                        return image

    def get_image_object_by_mask_uuid(self, mask_uuid):
        for group in self.groups:
            for condition in self.groups[group].conds:
                for image in self.groups[group].conds[condition].images:
                    for mask in image.masks:
                        if mask.unique_id == mask_uuid:
                            return image

    def get_current_image_number(self, correct_bounbs=True):
        if correct_bounbs:
            # if the current image number is out of bounds, correct it
            if (
                len(self.get_current_condition_object().images)
                <= self.MainWindow.current_imagenumber
            ):
                self.MainWindow.current_imagenumber = (
                    len(self.get_current_condition_object().images) - 1
                )

        return max(0, self.MainWindow.current_imagenumber)

    def get_current_image_uuid(self):
        return (
            self.groups[self.get_current_group()]
            .conds[self.get_current_condition()]
            .images[self.get_current_image_number()]
            .unique_id
        )

    def get_current_condition(self) -> str | None:
        if self.current_condition:
            return self.current_condition
        else:
            # get the first element of the first group
            all_treatments = self.groups[self.get_current_group()].conds
            if not all_treatments:
                return None
            self.current_condition = list(all_treatments.keys())[0]
            # make sure that its available in the ui
            self.MainWindow.switch_treatment_onchange(condition=self.current_condition)
            return self.current_condition

    def get_current_condition_uuid(self):
        return (
            self.groups[self.get_current_group()]
            .conds[self.get_current_condition()]
            .unique_id
        )

    def get_treatment_name_by_uuid(self, uuid_num):
        for group in self.groups:
            for treatment in self.groups[group].conds:
                if self.groups[group].conds[treatment].unique_id == uuid_num:
                    return treatment

    def get_treatment_object_from_image_uuid(self, image_uuid):
        for group in self.groups:
            for treatment in self.groups[group].conds:
                for image in self.groups[group].conds[treatment].images:
                    if image.unique_id == image_uuid:
                        return self.groups[group].conds[treatment]

    def get_group_object_from_image_uuid(self, image_uuid):
        for group in self.groups:
            for treatment in self.groups[group].conds:
                for image in self.groups[group].conds[treatment].images:
                    if image.unique_id == image_uuid:
                        return self.groups[group]

    def get_condition_by_uuid(self, uuid=None):
        for group in self.groups:
            for condition in self.groups[group].conds:
                if self.groups[group].conds[condition].unique_id == uuid:
                    return self.groups[group].conds[condition]

    def get_condition_name_by_uuid(self, uuid=None):
        for group in self.groups:
            for condition in self.groups[group].conds:
                if self.groups[group].conds[condition].unique_id == uuid:
                    return condition

    def get_current_condition_object(self):
        try:
            return self.groups[self.get_current_group()].conds[
                self.get_current_condition()
            ]
        except:
            return None

    def get_current_image_path(self, mode="full_path"):
        img_obj = (
            self.groups[self.get_current_group()]
            .conds[self.get_current_condition()]
            .images[self.get_current_image_number()]
        )
        if mode == "full_path":
            return os.path.join(str(img_obj.fileRootFolder), img_obj.fileName)
        return img_obj.fileName

    def get_current_group_uuid(self):
        return self.groups[self.get_current_group()].unique_id

    def set_current_group(self, group_name):
        self.currentGroup = group_name

    def get_current_group(self) -> str:
        if self.currentGroup:
            return self.currentGroup
        else:
            return "default"

    def get_all_image_objects(self) -> list:
        # iterate over all groups, all conditions, all images and yield the image
        all_objects = []
        for self.group in self.groups:
            for self.condition in self.groups[self.group].conds:
                for self.image in self.groups[self.group].conds[self.condition].images:
                    all_objects.append(self.image)
        return all_objects

    def get_all_annotation_objects_for_image(
        self, group_name, condition_name, image_idx, without_particles=False
    ):
        for m in self.groups[group_name].conds[condition_name].images[image_idx].masks:
            if without_particles:
                if m.is_particle():
                    continue
            yield m

    def get_all_annotations_with_category(self, category):
        # category is the class_id as in uuid
        all_mask_objects = [
            i for i in self.get_all_mask_objects() if i.class_id == category
        ]
        return all_mask_objects

    def get_image_uuid_by_mask_uuid(self, mask_uuid):
        for group in self.groups:
            for condition in self.groups[group].conds:
                for image in self.groups[group].conds[condition].images:
                    for mask in image.masks:
                        if mask.unique_id == mask_uuid:
                            return image.unique_id

    def get_all_mask_objects(self):
        # iterate over all groups, all conditions, all images, all masks and yield the mask
        for group in self.groups:
            for condition in self.groups[group].conds:
                for image in self.groups[group].conds[condition].images:
                    for mask in image.masks:
                        yield mask

    def get_all_annotations_on_image_from_classes_id(
        self, group_name, coondition_id, image_idx, class_id
    ):
        "returns all annotation objects from an image that have the specified class"
        for mask in self.get_all_annotation_objects_for_image(
            group_name,
            coondition_id,
            image_idx,
            without_particles=True,
        ):
            if mask.class_id == class_id:
                yield mask

    def get_all_mask_objects(self, without_particles=False):
        # iterate over all groups, all conditions, all images, all masks and yield the mask
        for group in self.groups:
            for condition in self.groups[group].conds:
                for image in self.groups[group].conds[condition].images:
                    for mask in image.masks:
                        if without_particles:
                            if mask.is_particle():
                                continue
                        yield mask

    def get_all_mask_objects_for_image(
        self, group_name, condition_name, image_idx, without_particles=True
    ):
        for mask in (
            self.groups[group_name].conds[condition_name].images[image_idx].masks
        ):
            if without_particles:
                if mask.is_particle():
                    continue
            yield mask

    def get_all_classes(self):
        # iterate over all groups, all conditions, all images, all masks and return a set of all available classes

        all_classes = []

        for group in self.groups:
            for condition in self.groups[group]:
                for image in condition.images:
                    for self.mask in image.masks:
                        all_classes.append(self.mask.class_id)
        all_classes = set(all_classes)

        return list(all_classes)

    def get_all_annotation_tracks_for_treatment(self, treatment_object):
        # get every mask fr that teatment
        all_tracks = []
        # iterate over all images and masks
        for image_object in treatment_object.images:
            for mask_object in image_object.masks:
                if mask_object._annotation_track_id:
                    all_tracks.append(mask_object._annotation_track_id)
        return list(set(all_tracks))

    def get_centroid_path_for_annotation_track(self, treatment_object, track_id):
        # get the centroid path for a track
        centroid_path = []
        for image in treatment_object.images:
            for mask in image.masks:
                if mask._annotation_track_id == track_id:
                    centroid_path.append(mask.get_centroid())

        return centroid_path

    def get_average_mask_length(self):
        # iterate through all masks and get the average length of all the masks
        raise NotImplementedError()

    def get_average_mask_area(self):
        # Iterate through all masks and get the average area of all the masks
        raise NotImplementedError()

    def get_global_minimum_extreem(self):
        # gets the minimum extreem of all the groups of all the conditions so that intepretated 16 bit images
        # display differences in intensity when compared to the original image
        min_extreem = 65535

    def get_image_pixmap(self, im: np.array = None, as_QIcon=False):
        """
        It takes an image and returns two QImages, one for the off state and one for the on state
        These are used for Qt ,in the button arrea and as the QPushButton area.

        Args:
          im (np.array): the image to be displayed
          as_QIcon (bool): if True, returns a QIcon instead of a QPixmap

        Returns:
           QtGui.QImage ,  QtGui.QImage
        """

        # case of just a normal image -> im is a numpy array , img_id is None
        if len(im.shape) == 3:
            bytesPerLine = im.shape[1] * im.shape[2]
        else:
            bytesPerLine = im.shape[1]

        # Pick a format that matches the image dtype
        if im.dtype == np.dtype(np.uint8):
            if len(im.shape) == 3:
                im_format = QtGui.QImage.Format.Format_RGB888
            else:
                im_format = QtGui.QImage.Format.Format_Grayscale8
        elif im.dtype == np.dtype(np.uint16):
            # Qt returns null pixmap from 16bit images so, convert to 8bit

            if len(im.shape) == 3:
                im_format = QtGui.QImage.Format.Format_RGB16
            else:
                im_format = QtGui.QImage.Format.Format_Grayscale16
        else:
            raise NotImplementedError("Only uint8 and uint16 are supported for now")

        if as_QIcon:
            # case were we get pixmap as qicon, this is primarily for the button area
            ResizedImageQImageOff = QtGui.QImage(
                im.copy(),
                im.shape[1],
                im.shape[0],
                bytesPerLine,
                im_format,
            ).copy()
            ResizedImageQImageOn = QtGui.QImage(
                im.copy(),  # TODO: make this more contrasted, or the off less bright
                im.shape[1],
                im.shape[0],
                bytesPerLine,
                im_format,
            ).copy()
            return ResizedImageQImageOff, ResizedImageQImageOn
        else:  # case were we get pixmap as qimage, this is primarily for the viewer qgraphicsview area
            return QtGui.QPixmap.fromImage(
                QtGui.QImage(
                    im.data.tobytes(),
                    im.shape[1],
                    im.shape[0],
                    bytesPerLine,
                    im_format,
                )
            )

    def get_all_top_level_classes(self):
        # get all the class uuids of classes without any children
        classes = self.MainWindow.custom_class_list_widget.classes
        ans = []
        for c in classes:
            if classes[c].parent_class_uuid == None:
                ans.append(classes[c].unique_id)
        return ans

    def get_current_class_color(self):
        # get the color of the current class
        return self.MainWindow.custom_class_list_widget.classes[
            self.get_current_class_uuid()
        ].color

    def get_current_class_uuid(self):
        w_item = self.MainWindow.custom_class_list_widget.currentItemWidget()
        if not w_item:
            return None
        return w_item.unique_id

    def get_mask_object_by_uuid(self, mask_uuid=None):
        if not mask_uuid:
            return
        # get the mask object from the uuid
        for img_obj in self.get_all_image_objects():
            for mask in img_obj.masks:
                if mask.unique_id == mask_uuid:
                    return mask

    def get_track_num_from_track_uuid(self, track_uuid=None):
        if not track_uuid:
            return None
        all_tracks = []
        # get the track number from the track uuid
        for img_obj in self.get_all_image_objects():
            for track in img_obj.tracks:
                if track.unique_id == track_uuid:
                    return track.track_num

    def is_color_in_any_class(self, color=(255, 0, 0)):
        # Check if the color is contained in any of the classes.
        classes = self.MainWindow.custom_class_list_widget.classes
        for c in classes:
            if classes[c].color == color:
                return True
        return False

    def delete_all_masks_with_class(self, class_uuid=None):
        """
        The function `delete_all_masks_with_class` deletes all masks with a specific class UUID from a list
        of image objects.

        Args:
          class_uuid: The `class_uuid` parameter is a unique identifier for a class. It is used to specify
        which masks should be deleted. If `class_uuid` is not provided or is `None`, the function will
        return without doing anything.

        Returns:
          None
        """
        if class_uuid == None:
            return None
        for img_obj in self.get_all_image_objects():
            for mask in img_obj.masks:
                if mask.class_id == class_uuid:
                    img_obj.del_by_uuid(mask.unique_id)
        return None

    def delete_all_groups(self):
        # remove all groups ( except default ) TODO: fix this in the future, where default group does not always exist
        for g in self.groups:
            while self.groups[g].conds:
                # get a random key
                c = list(self.groups[g].conds.keys())[0]
                self.MainWindow.delete_treatment_item_by_name(c)
        del self.groups
        self.groups = {}
        # create a new default class
        self.groups["default"] = grpObj(self.MainWindow)

    def areAllAnnotatedImagesUploaded(self):
        # check if all of the images that are user corrected
        # after inference has been sent to the server.
        for kg in self.groups:
            for kc in self.groups[kg].conds:
                for ki in self.groups[kg].conds[kc].images:
                    if ki.userModifiedAnnotation:
                        if not ki.hasBeenUploaded:
                            break

    def endAllInferenceAnimations(self):
        # for all groups
        for kg in self.groups.keys():
            # for all conditions
            for kc in self.groups[kg].conds.keys():
                # for all images
                for ki in self.groups[kg].conds[kc].images:
                    # End inference on the button object
                    ki.check_and_end_inference_animation(force=True)

    def getTotalImages(self):
        # loop all groups
        totalImages = 0
        for group in self.groups:
            # loop all conditions
            for condition_key in self.groups[group].conds.keys():
                totalImages += len(self.groups[group].conds[condition_key].images)
        return totalImages

    def get_group_cond_by_id(self, id):
        # figure out by id what group and condition we are currently on.
        for x, group in enumerate(self.groups):
            for y, condition in enumerate(self.groups[group].conds.keys()):
                if x + y == id:
                    return group, condition

    def addGroup(self, groupName, uuid=None):
        self.groups[groupName] = grpObj(self.MainWindow, uuid)

    def newAnalysis(self, MainWindow):
        self.addGroup("default")

    def track_objects_across_images_per_treatment(self):
        NotImplementedError()

    def get_box_position(
        self,
        n: int,
        cols: int = config.BUTTON_COLS,
        spacing: float = config.BUTTON_SPACING,
        box_width: int = config.BUTTON_WIDTH,
        box_height: int = config.BUTTON_HEIGHT,
        padding_left: float = config.BUTTON_PADDING_LEFT,
        padding_top: float = config.BUTTON_PADDING_TOP,
    ) -> tuple[int, int]:
        """
        Given the image button dimentions and padding, compute the button's  position
        Parameters:
            - n: int: the index of the button
            - cols: int: the number of columns
            - spacing: float: the spacing between the buttons
            - box_width: int: the width of the button
            - box_height: int: the height of the button
            - padding_left: float: the padding from the left
            - padding_top: float: the padding from the top
        Returns:
            - tuple[int, int]: the x and y coordinates of the button
        """
        row = n // cols
        col = n % cols
        x = col * (box_width + spacing)
        y = row * (box_height + spacing)
        return (x + padding_left, y + padding_top)

    def create_button_instance(self, signal_objects=None):
        """
        Creates the buttons on the image preview area
        The buttons disapear and apear as the user scrolls through the images
        The ImageButtonPlaceHolderClass holds the basic attributes and this widget
        created here is for the interface.

        signal_object: a list of lists that contains the group id, condition id, image id, and if its the last image to be loaded
        """
        logger.debug(f"Creating button instance for {len(signal_objects)} images")
        for signal_object in signal_objects:
            try:
                group_id = signal_object[0]
                cond_uuid = signal_object[1]
                image_idx = signal_object[2]
                terminal_load = signal_object[3]

                position = self.get_box_position(
                    n=image_idx,
                    cols=3,
                    spacing=BUTTON_SPACING,
                    box_width=BUTTON_WIDTH,
                    box_height=BUTTON_HEIGHT,
                    padding_left=BUTTON_PADDING_LEFT,
                    padding_top=BUTTON_PADDING_TOP,
                )
                logger.debug(f"Spawning button at position: {position}")

                from celer_sight_ai.QtAssets.buttons.image_button import (
                    ButtonAssetClass,
                )

                cond = self.get_condition_by_uuid(cond_uuid)
                if not cond:
                    return
                if not cond.images[image_idx]:
                    return
                image_uuid = cond.images[image_idx].unique_id
                ButtonAssetClassInstance = ButtonAssetClass(
                    self.MainWindow, cond.images[image_uuid].myButton
                )
                ButtonAssetClassInstance.setStyleSheet(
                    """
                background-color: rgb(0, 255, 0 );
                border: 0px solid black;
                color: rgba(0,0,0,0);
                """
                )
                AssetBUttonMainframe1 = ButtonAssetClassInstance.findChild(
                    QtWidgets.QFrame, "AssetBUttonMainframe"
                )

                AssetButtonFrame = ButtonAssetClassInstance.findChild(
                    QtWidgets.QFrame, "AssetButtonFrame"
                )

                cond.images[image_uuid].myButton.button_instance = (
                    ButtonAssetClassInstance
                )

                ButtonAssetClassInstance.setMinimumSize(
                    QtCore.QSize(BUTTON_WIDTH, BUTTON_HEIGHT)
                )
                ButtonAssetClassInstance.setMaximumSize(
                    QtCore.QSize(BUTTON_WIDTH, BUTTON_HEIGHT)
                )

                ButtonAssetClassInstance.setFocusProxy(self.MainWindow.viewer)
                AssetBUttonMainframe1.setFocusProxy(self.MainWindow.viewer)
                checkLabelLoaded = ButtonAssetClassInstance.findChild(
                    QtWidgets.QLabel, "checkLabel"
                )

                checkLabelLoaded.setParent(AssetBUttonMainframe1)
                checkLabelLoaded.raise_()
                checkLabelLoaded.hide()
                checkLabelLoaded.move(AssetBUttonMainframe1.width() + 40, 2)
                image_idx = cond.images.get_index(image_uuid)
                QtWidgets.QApplication.processEvents()

                ButtonAssetClassInstance.set_label_number(image_idx + 1)

                ButtonAssetClassInstance.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
                AssetBUttonMainframe1.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
                ButtonAssetClassInstance.setObjectName("AssetButton" + str(image_idx))
                AssetBUttonMainframe1.setObjectName("AssetButton" + str(image_idx))

                proxy = TransparentGraphicsWidget()
                proxy.setWidget(ButtonAssetClassInstance)
                proxy.setPos(int((position[0])), int((position[1])))
                self.MainWindow.images_preview_graphicsview.scene().addItem(proxy)
                cond.images[image_uuid].myButton.button_instance_proxy = proxy

                # add preview for images
                ButtonAssetClassInstance.setupSelfPic(image_idx)
                # add image data to MainWindow.DH.BLobj
                # use image uuid to avoid conflicts
                config.global_signals.load_image_to_preview_button_signal.emit(
                    [image_uuid, cond_uuid, group_id]
                )  # load the image to the image preview button. (threaded)
                ButtonAssetClassInstance.isDoneSettingUp = True
                ButtonAssetClassInstance.setStyleSheet(
                    """
                        border-radius: 6px;
                        background-color: rgba(0, 0, 0, 0);
                        
                    """
                )
                AssetBUttonMainframe1.setStyleSheet(
                    "QFrame#AssetBUttonMainframe {\n"
                    "    border: 1px solid #A1A1A1;\n"
                    "    border-radius: 6px;\n"
                    "    background-color: rgba(0, 0, 0, 0);\n"
                    "    background-repeat: repeat;\n"
                    "    background-position: center;\n"
                    "}"
                )
                AssetButtonFrame.setStyleSheet(
                    """
                border-radius: 6px;
                background-color: rgba(0, 255, 0,0);
                border: 0px solid black;
                color: rgba(0,0,0,0);
                """
                )
                cond.images[image_uuid].myButton.button_instance = (
                    ButtonAssetClassInstance
                )
                # if during inferece, start inference animation
                if cond.images[image_uuid]._during_inference:
                    cond.images[
                        image_uuid
                    ].myButton.button_instance.startInferenceAnimation()

                if self.MainWindow.MyInferenceHandler.is_inference_running:
                    # button
                    ButtonAssetClassInstance.startInferenceAnimation()
                if self.MainWindow.no_image_displayed:
                    self.MainWindow.no_image_displayed = False
                    # load scene
                    self.MainWindow.load_main_scene(0, fit_in_view=True)

                # QtWidgets.QApplication.processEvents()
                if terminal_load:
                    self.MainWindow.images_preview_graphicsview.set_updating_buttons(
                        False
                    )
                    config.global_signals.refresh_image_preview_graphicsscene_signal.emit()
            except Exception as e:
                print(e)


class grpObj:  # contains group condObj
    def __init__(self, MainWindow, uuid=None):
        self.MainWindow = MainWindow
        self.conds = {}
        self.groupName = "default"
        if not uuid:
            self.unique_id = str(config.get_unique_id())
        else:
            self.unique_id = uuid

    def get_by_uuid(self, uuid: str = None) -> any:
        # Fetch the condition object by its unique ID
        for c in self.conds:
            if self.conds[c].unique_id == uuid:
                return self.conds[c]
        return None

    def addCondition(self, ConditionName, condition_uuid=None):
        self.conds[ConditionName] = condObj(
            self.MainWindow, self.groupName, ConditionName, condition_uuid
        )


class condObj:
    def __init__(self, MainWindow, group_name, condition_name, condition_uuid=None):
        self.MainWindow = MainWindow
        self.images = HashList()  # list of ImageObject

        self.condition_name_set = (
            False  #  Default is "Condition" --> not set, it either
        )
        if not condition_uuid:
            self.unique_id = str(config.get_unique_id())
        else:
            self.unique_id = condition_uuid
        # has to be set from user or from a comon file name
        self.MainWindow.DH.BLobj.object_mapping[self.unique_id] = self

    @property
    def unique_id(self):
        """Get the image ID."""
        return self._unique_id

    @unique_id.setter
    def unique_id(self, value: str):
        """Set the image ID.

        Args:
            value: The new image ID value
        """
        if not isinstance(value, str):
            raise ValueError("UUID must be a string")
        self._unique_id = value

    def get_image_by_uuid(self, uuid):
        return self.images.get(uuid)

    def get_image_id_by_uuid(self, uuid):
        return self.images.get_index(uuid)

    def get_all_image_objects(self):
        """
        This functions iterates through the groups, conditions, and images in a given
        object and yields each image object.
        """
        for group in self.MainWindow.DH.BLobj.groups:
            for cond in self.MainWindow.DH.BLobj.groups[group].conds:
                for img in self.MainWindow.DH.BLobj.groups[group].conds[cond].images:
                    yield img

    def getAllImages(self):
        # Lists all of the images (arrays ,not objects) in this conditions
        listImages = []
        for i in range(len(self.images)):
            listImages.append(self.getImage(i))
        return listImages

    def getPath(self, imgID):
        return self.images[imgID].get_path()

    def is_current_image_on_ram(self):
        current_image_path = self.MainWindow.DH.BLobj.get_current_image_path()
        if not isinstance(config.ram_image, type(None)):
            if config.ram_image_path and config.ram_image_path == current_image_path:
                return True
        return False

    def load_current_ram_image(self, bbox=None) -> None:
        from celer_sight_ai.gui.custom_widgets.scene import readImage

        # bbox: [x,y,w,h]
        # check if the current config.ram_image is the correct image
        # by double checking with the image path, it not read it again.
        if self.is_current_image_on_ram():
            if not isinstance(bbox, type(None)):
                return config.ram_image[
                    bbox[1] : bbox[1] + bbox[3], bbox[0] : bbox[0] + bbox[2]
                ]
            return config.ram_image
        logger.debug("Ram image path different than current image , re-reading.")
        # otherwise read image , assign o ram and return that
        current_image_path = self.MainWindow.DH.BLobj.get_current_image_path()
        return readImage(path=current_image_path, bbox=bbox)[0]

    def getImage(
        self,
        *args,
        **kwargs,
    ):
        args = list(args)
        imID = args.pop(0)
        args = tuple([self.images[imID]] + args)
        try:
            im = getImage(*args, **kwargs)
        except Exception as e:
            # delete current image
            image_object = self.images[imID]
            button = image_object.myButton
            if button:
                object = {
                    "group_name": image_object.group_uuid,
                    "treatment_uuid": image_object.treatment_uuid,
                    "image_uuid": image_object.unique_id,
                }
                config.global_signals.delete_image_with_button_signal.emit(object)

        return im  # only need the image (index 0) since we have already recorded the channels

    def __len__(self):
        return len(self.images)

    def __del__(self):
        # delete all masks
        logger.debug(f"Deleting condition {self.unique_id} and all references")
        for image in self.images:
            for mask in image.masks:
                if mask.unique_id in self.MainWindow.DH.BLobj.object_mapping:
                    del self.MainWindow.DH.BLobj.object_mapping[mask.unique_id]
            if image.unique_id in self.MainWindow.DH.BLobj.object_mapping:
                del self.MainWindow.DH.BLobj.object_mapping[image.unique_id]
        if self.unique_id in self.MainWindow.DH.BLobj.object_mapping:
            del self.MainWindow.DH.BLobj.object_mapping[self.unique_id]

    def get_image_extrema(self, img_id):
        """
        > If the raw image extrema have not been set, then set them and return them. Otherwise, return the
        previously set values

        Args:
          img_id: the id of the image to get the extrema for
        """
        if not self.raw_image_extrema_set:
            im = self.getImage(img_id)
            min_val = np.min(im)
            max_val = np.max(im)
            self.images[img_id].raw_image_max_value = max_val
            self.images[img_id].raw_image_min_value = min_val
            self.raw_image_extrema_set = True
        else:
            min_val = self.images[img_id].raw_image_min_value
            max_val = self.images[img_id].raw_image_max_value
        return min_val, max_val

    # first time import image to class
    def addImage_FROM_DISK(
        self, imagePath, group_uuid, cond_uuid, image_uuid=None, thumbnail=None
    ):
        # adds image ref only
        ROOTFILE, BASEFILE = self.assignPathToImage(imagePath)
        imgIdx = len(self.images)
        image_object = ImageObject(
            self.MainWindow,
            ROOTFILE,
            BASEFILE,
            group_uuid,
            cond_uuid,
            image_uuid=image_uuid,
            imgIdx=imgIdx,
        )
        self.images.append(image_object)
        if thumbnail:
            image_object.thumbnail = thumbnail
            image_object.thumbnailGenerated = True
        return image_object

    def add_video_from_disk(
        self, video_path, group_uuid, cond_uuid, image_id, thumbnail=None
    ):
        # import a video file path from disk
        ROOTFILE, BASEFILE = self.assignPathToImage(video_path)
        self.images.append(
            ImageObject(
                self.MainWindow,
                ROOTFILE,
                BASEFILE,
                group_uuid,
                cond_uuid,
                image_id,
                is_video=True,
            )
        )

    def add_image_from_url(self, image_url, groupId, condId, imageId, thumbnail=None):
        image_object = ImageObject(
            MainWindow=self.MainWindow,
            rootfile="celer_sight_ai:",
            filename=image_url.replace("celer_sight_ai:", ""),
            groupId=groupId,
            condId=condId,
            imgID=imageId,
            image_uuid=image_url.replace("celer_sight_ai:", ""),
        )

        self.images.append(image_object)
        if thumbnail:
            self.images[imageId].thumbnail = thumbnail
            self.images[imageId].thumbnailGenerated = True
        return image_object

    def add_channels_to_image(self, img_id, channels):
        self.images[img_id].channel_list = channels

    def channel_name_to_index(self, img_id, channel_name):
        self.images[img_id].channel_list.index(channel_name)

    def clearAllRamImages(self):
        for someImage in self.images:
            del someImage.image
            someImage.image = None

    def set_thumbnail(self, image_uuid=None, imageRef=None):
        # adds image ref to thumbnail
        logger.debug("Adding thumbnails")
        # handle max size and compression ratio
        majorScale = max(imageRef.shape[0], imageRef.shape[1])
        # case where image is too big
        if majorScale > IMAGE_THUMBNAIL_MAX_SIZE:
            logger.debug("Resizing image to fit in thumbnail")

            # read image from disk
            reduceTo = IMAGE_THUMBNAIL_MAX_SIZE
            scaleChange = reduceTo / majorScale
            imageRef = cv2.resize(
                imageRef,
                (0, 0),
                fx=scaleChange,
                fy=scaleChange,
                interpolation=cv2.INTER_NEAREST,
            )

        self.images[image_uuid].thumbnail = cv2.imencode(".jpg", imageRef)[1].tobytes()
        self.images[image_uuid].thumbnailGenerated = True

    def get_thumbnail(self, image_uuid=None, for_button=False):
        logger.debug(f"Retrieving thumbnail for image {image_uuid}")
        if not isinstance(image_uuid, type(None)):
            image_object = self.images[image_uuid]
        else:
            logger.info("No image ID or image uuid provided")
            raise ValueError("No image ID or image uuid provided")

        if isinstance(image_object.thumbnail, type(bytes())):
            # it is an encoded jpg
            nparr = np.frombuffer(image_object.thumbnail, np.byte)
            img = cv2.imdecode(nparr, cv2.IMREAD_ANYCOLOR)
            if for_button:
                # get smallest dim
                min_dim = min(img.shape[0], img.shape[1])
                scaleChange = BUTTON_THUMBNAIL_MIN_SIZE / min_dim
                img = cv2.resize(
                    img,
                    (0, 0),
                    fx=scaleChange,
                    fy=scaleChange,
                    interpolation=cv2.INTER_AREA,
                )

            return img
        else:
            return image_object.thumbnail

    def deleteImage(self, imID):  # imID can be int or uuid
        del self.MainWindow.DH.BLobj.object_mapping[self.images[imID].unique_id]
        self.images.pop(imID)

    def assignPathToImage(self, PathToAssign):
        # For an already existing image
        mypath = Path(PathToAssign)
        RootDir = mypath.parent
        fileNameBase = os.path.basename(PathToAssign)
        return RootDir, fileNameBase

    def get_channel_list(self, imID: int):
        """
        > If the channel list is not already stored in the image object, read the image and store the
        channel list in the image object

        Args:
          imID (int): the image ID

        Returns:
          A list of channels as string / names
        """
        if not self.images[imID].channel_list:
            self.images[imID].channel_list = readImage(self.getPath(imID))[1].get(
                "channels", None
            )
        return self.images[imID].channel_list

    def loadToRam(self, imgID):
        # For an already existing image
        # Needs adjustment --> read Image
        im, result_dict = readImage(self.getPath(imgID))
        channel_list = result_dict["channels"]
        self.images[imgID].image = im
        if not self.images[imgID].channel_list and channel_list:
            self.images[imgID].channel_list = channel_list
        self.images[imgID].dtype = im.dtype
        self.onRam = True

    def unloadFromRam(self, imgID):
        del self.images[imgID].image
        self.images[imgID].image = None
        self.onRam = False

    def generateThumbNail(self, imID):
        tmpImage = self.images[imID].image.copy()
        ReduceBy = 3
        from skimage.transform import resize

        self.images[imID].thumbnail = resize(
            tmpImage,
            (tmpImage.shape[0] // ReduceBy, tmpImage.shape[1] // ReduceBy),
            anti_aliasing=False,
            preserve_range=True,
        )
        self.thumbnailGenerated = True

    def addButtonToImageObject(self, imID, buttonRef):
        # references the button widget object to the image instance
        self.images[imID].setButtonReference(buttonRef)

    def set_common_condition_name(self, all_image_names=None):
        # get all the filenames of the sub image
        if not all_image_names:
            all_image_names = [
                ".".join(i.fileName.split("/")[-1].split(".")[:-1]) for i in self.images
            ]
        else:
            all_image_names = [
                ".".join(i.split("/")[-1].split(".")[:-1]) for i in all_image_names
            ]
        # find common prefix
        common_prefix = os.path.commonprefix(all_image_names)
        if (
            self.MainWindow.DH.BLobj.groups[
                self.MainWindow.DH.BLobj.get_current_group()
            ]
            .conds[self.MainWindow.DH.BLobj.get_current_condition()]
            .condition_name_set
        ):
            return
        if common_prefix == "":
            return
        try:
            while common_prefix[-1] == "_" or common_prefix[-1].isdigit():
                if len(common_prefix) < 3:
                    return
                while common_prefix[-1] == "_":
                    if len(common_prefix) < 3:
                        return
                    common_prefix = common_prefix[:-1]
                # trancate int at the end
                while common_prefix[-1].isdigit():
                    if len(common_prefix) < 3:
                        return
                    common_prefix = common_prefix[:-1]
                if len(common_prefix) < 3:
                    return
        except:
            return
        if len(common_prefix) < 3:
            # abort
            return
        if (
            common_prefix
            in self.MainWindow.DH.BLobj.groups[
                self.MainWindow.DH.BLobj.get_current_group()
            ].conds
        ):
            return

        # remove old condition name
        del self.MainWindow.DH.BLobj.groups[
            self.MainWindow.DH.BLobj.get_current_group()
        ].conds[self.MainWindow.DH.BLobj.get_current_condition()]
        # set condition name to that
        self.condition_name = common_prefix
        self.MainWindow.DH.BLobj.set_current_condition(self.condition_name)

        # adjust entry in the group object
        self.MainWindow.DH.BLobj.groups[
            self.MainWindow.DH.BLobj.get_current_group()
        ].conds[self.MainWindow.DH.BLobj.get_current_condition()] = self
        # adjust self.RNAi_list widget entry
        self.MainWindow.RNAi_list.item(self.MainWindow.RNAi_list.currentRow()).setText(
            self.MainWindow.DH.BLobj.get_current_condition()
        )
        # adjust condition for all sub items
        for i in self.images:
            i.treatment_uuid = self.MainWindow.DH.BLobj.get_current_condition_uuid()

        # adjust all spawned buttons
        for b in (
            self.MainWindow.DH.BLobj.groups[
                self.MainWindow.DH.BLobj.get_current_group()
            ]
            .conds[self.MainWindow.DH.BLobj.get_current_condition()]
            .images
        ):
            b.myButton.cond_id = self.MainWindow.DH.BLobj.get_current_condition()

        self.condition_name_set = True
        if self.MainWindow.current_imagenumber >= 0:
            # trigger viewer refresh
            self.MainWindow.load_main_scene(
                self.MainWindow.current_imagenumber, fit_in_view=True
            )
        return common_prefix


class ImageObject:
    def __init__(
        self,
        MainWindow,
        rootfile,
        filename,
        groupId=None,
        treatment_uuid=None,
        imgIdx=None,
        image_uuid=None,  # provided for remote annotation to match the uuid of the image on the server
        is_video=False,
    ):
        self.MainWindow = MainWindow
        self.image = None  # image numpy array, not used frequently in the app due to memory limitations
        self.masks = MaskContainer(self.MainWindow)  # list of maskObj objects
        self.thumbnail = None  # thubnail for quickly viewing the image TODO: not sure if this is used
        # correclty for optimal speed while loading images.
        self.thumbnailGenerated = (
            False  # Boolean to check if the thumbnail has been generated
        )
        self.is_cached = False  # if the image is cached
        self.fileRootFolder = rootfile  # parent directory of the image
        self.fileName = filename  # name of the image
        self.bitDepth = (
            None  # should be np.uint8 , np.float16 comming soon TODO implement float16
        )
        # Turns to true when the mask count is over 20 per image --> updateMaskCountLabel
        self._disable_overlay_annotation_items = False

        # remote annotation mode
        self._is_remote = False  # if the image is remote
        self._is_downloading = False  # if the image is being downloaded
        self.guess_remote()

        ############################
        ##### video attributes #####
        ############################

        self._is_video = is_video  # if the image is a video
        # TODO: add current frame number
        self._video_total_frames = None  # total number of frames in the video
        self._video_current_frame = None  # current frame number
        self._video_frame_rate = None

        ############################
        ##### Ultra High Res #######
        ############################

        self._is_ultra_high_res = False  # if the image is ultra high res
        self._deep_zoom_object = None  # the deep zoom object
        self._during_pyramidal_conversion = (
            False  # True while the image is being converted to a pyramidal image
        )
        self._failed_creating_pyramidal = False
        # self._during_scene_update = False
        # if so, use dask to dynamically load the image
        self._is_pyramidal = False  # if the image is ultrahigh res, when it gets converted to a pyramidal image, this becames true
        self.pyramidal_image_path = None

        self.onRam = False  # indicates if the image is loaded in RAM

        if not image_uuid:
            self.unique_id = str(config.get_unique_id())  # unique id of the image
        else:
            self.unique_id = image_uuid

        self.myButton = ImageButtonPlaceHolderClass(
            MainWindow=self.MainWindow, image_uuid=self.unique_id, image_number=imgIdx
        )  # link to the button widget object
        self.group_uuid = groupId  # group name
        self.imgID = imgIdx  # image IDX
        self.treatment_uuid = treatment_uuid

        self.channel_list = None

        self.is_stack = False  # if the image contains other stack image objects, this is set to True
        self.stack_images = []  # list of stack image objects

        self.raw_image_max_value = None  # the maximum value of the raw image
        self.raw_image_min_value = None  # the minimum value of the raw image
        self.raw_image_extrema_set = (
            False  # boolean to check if the extrema have been set
        )

        self._masks_spawned = False  # flag to avoid spawning annotations twice when displaying thumbnail and full image at once.

        ###### OME-TIFF SPECIFIC VARIABLES ######
        self.SignificantBits = None
        self.PhotometricInterpretation = None
        self.ID = None
        self.DimensionOrder = None
        self.SizeX = None  # X Size of the array
        self.SizeY = None  # Y Size of the array
        self.SizeZ = None  # Z-Stack
        self.SizeC = None  # Channels
        self.SizeT = None  # Series
        self.PhysicalSizeX = None  # X physical size of the pixels
        self.PhysicalSizeY = None  # Y physical size of the pixels
        self.PhysicalSizeXUnit = None  # X physical size unit
        self.PhysicalSizeYUnit = None  # Y physical size unit
        self.ExposureTime = None
        self.ExposureTimeUnit = None
        self.ExperiementName = None  # equal to the "Name" variable in OME
        self.AcquisitionDate = None
        self.Software = None  # Aquizition software
        self.resolution = None  # resolution of the image
        self.resolutionunit = None

        # this variable allows us to know if we have infcomputed annotations for this image
        # This is usefull if we would like to send improved annotation results to the server
        # later on if the user changes the annotations.
        self.computedInference = False
        self._during_inference = False  # True while online/offline inference

        # If inference is computed, any change on the annotations would set userModifiedAnnotation to True
        self.userModifiedAnnotation = False

        # variable to hold where the graphics tile item are present during inference
        self.graphics_tile_items = {}  # dict of inference uuid : tile

        self.hasBeenUploaded = (
            False  # only used in conjuction with userModifiedAnnotation, signifies that
        )
        # after the user moodified the annotation the image + annotation has been uploaded to the server
        self.MainWindow.DH.BLobj.object_mapping[self.unique_id] = self

    @property
    def cache_location(self):
        return os.path.join(config.cache_dir, self.unique_id)

    @property
    def imgID(self):
        return self._imgID

    @imgID.setter
    def imgID(self, value: int):
        if not isinstance(value, int):
            raise ValueError("Image ID must be an integer")
        self._imgID = value

    @property
    def unique_id(self):
        """Get the image ID."""
        return self._unique_id

    @unique_id.setter
    def unique_id(self, value: str):
        """Set the image ID.

        Args:
            value: The new image ID value
        """
        if not isinstance(value, str):
            raise ValueError("UUID must be a string")
        self._unique_id = value

    @config.threaded
    def download_remote_image(self):
        # Set the image to download mode,
        # download the image, if the ui updates, its reflected on the viewer
        # once done, or fail, set the image to remote mode
        if self._is_downloading:
            return False
        if not str(self.fileRootFolder).lower().startswith("celer_sight_ai:"):
            logger.warning("Image is not remote, cannot download")
            return
        self._is_downloading = True
        try:
            destination_path = config.client.get_remote_image_high(self.unique_id)
            # set the image path to the destination path
            self.set_path(destination_path)
        except Exception as e:
            logger.error(f"Error downloading remote image {e}")
        self._is_downloading = False
        # trigger a ui refresh
        config.global_signals.load_main_scene_and_fit_in_view_signal.emit()

    def getSizeX(self):
        """
        Returns the width of the image, if not loaded, image needs to be loaded first.
        """
        if not self.SizeX:
            logger.debug(f"Loading image to get size X {self.fileName}")
            self.getImage(avoid_loading_ultra_high_res_arrays_normaly=True)
        return self.SizeX

    def getSizeY(self):
        """
        Returns the height of the image, if not loaded, image needs to be loaded first.
        """
        if not self.SizeY:
            logger.debug(f"Loading image to get size Y {self.fileName}")
            self.getImage(avoid_loading_ultra_high_res_arrays_normaly=True)
        return self.SizeY

    def get_channel_list(self):
        """
        Returns the channel list of the image, if not loaded, image needs to be loaded first.
        """
        if not self.channel_list:
            logger.debug(f"Loading image to get channel list {self.fileName}")
            self.getImage(avoid_loading_ultra_high_res_arrays_normaly=True)
        return self.channel_list

    def check_and_apply_is_ultra_high_res(self):
        # check if the image is ultra high res
        # make sure both sizeX and sizeY axist and are larger than the threshold
        if self.SizeX and self.SizeY:
            if (
                self.SizeX > config.ULTRA_HIGH_RES_THRESHOLD
                or self.SizeY > config.ULTRA_HIGH_RES_THRESHOLD
            ):
                self._is_ultra_high_res = True
                logger.debug(f"Image is ultra high res {self.fileName}")
                return True
        return False

    def set_fast_cache_mode(self, value):
        from celer_sight_ai.gui.custom_widgets.scene import PolygonAnnotation

        # make sure all mask graphics items have the same value
        all_mask_items = [
            i
            for i in self.MainWindow.viewer._scene.items()
            if isinstance(i, PolygonAnnotation)
        ]
        for m in all_mask_items:
            m.set_fast_cache_mode(value)

    def set_disable_overlay_annotation_items(self, value):
        from celer_sight_ai.gui.custom_widgets.scene import PolygonAnnotation

        if value == self._disable_overlay_annotation_items:
            return
        else:
            self._disable_overlay_annotation_items = value
            # make sure all mask graphics items have the same value
            all_mask_items = [
                i
                for i in self.MainWindow.viewer._scene.items()
                if isinstance(i, PolygonAnnotation)
                and i._disable_spawn_extra_items != value
            ]
            for m in all_mask_items:
                m.set_disable_spawn_extra_items_variable(value)
                m.set_fast_cache_mode(value)

    def to_shapely(self, polygon_arr=[]):
        "return a shapely array with holes"
        from shapely.geometry import Polygon

        if any([len(i.shape) > 2 for i in polygon_arr]):
            polygon_arr = [p.squeeze() for p in polygon_arr]
        if len(polygon_arr) > 1:
            return Polygon(polygon_arr[0], polygon_arr[1:])
        else:
            return Polygon(polygon_arr[0])

    def from_shapely(self, shapely_polygon=None):
        "Return a celer sight array from a shapely array"
        if shapely_polygon.geom_type == "Polygon":
            outer_coords = list(shapely_polygon.exterior.coords)
            hole_coords = [list(hole.coords) for hole in shapely_polygon.interiors]
            shapely_polygon = [outer_coords] + hole_coords
            return shapely_polygon

    def getImage(self, *args, **kwargs):
        args = list(args)
        if len(args) == 0:
            args = tuple([self])  # convert imID to image object
        else:
            args.pop(0)
            args = tuple([self] + args)
        return getImage(*args, **kwargs)

    def is_current_image_on_ram(self):
        current_image_path = self.MainWindow.DH.BLobj.get_current_image_path()
        if not isinstance(config.ram_image, type(None)):
            if config.ram_image_path and config.ram_image_path == current_image_path:
                return True
        return False

    def load_current_ram_image(self, bbox=None) -> None:
        from celer_sight_ai.gui.custom_widgets.scene import readImage

        # bbox: [x,y,w,h]
        # check if the current config.ram_image is the correct image
        # by double checking with the image path, it not read it again.
        if self.is_current_image_on_ram():
            if not isinstance(bbox, type(None)):
                padding_right = max(
                    0, int(bbox[0] + bbox[2]) - config.ram_image.shape[1]
                )
                padding_left = min(0, int(bbox[0]))
                padding_top = min(0, int(bbox[1]))
                padding_bottom = max(
                    0, int(bbox[1] + bbox[3]) - config.ram_image.shape[0]
                )
                img = config.ram_image[
                    int(max(0, bbox[1])) : int(
                        min(bbox[1] + bbox[3], config.ram_image.shape[0])
                    ),
                    int(max(0, bbox[0])) : int(
                        min(bbox[0] + bbox[2], config.ram_image.shape[1])
                    ),
                ]
                # pad image
                img = cv2.copyMakeBorder(
                    img,
                    padding_top,
                    padding_bottom,
                    padding_left,
                    padding_right,
                    cv2.BORDER_CONSTANT,
                    value=125,
                )
                return img
            return config.ram_image
        logger.debug("Ram image path different than current image , re-reading.")
        # otherwise read image , assign o ram and return that
        current_image_path = self.MainWindow.DH.BLobj.get_current_image_path()
        return readImage(path=current_image_path, bbox=bbox)[0]

    def channel_name_to_index(self, channel_name):
        if isinstance(channel_name, str):
            return self.channel_list.index(channel_name)
        # other case is a numpy array
        # Find the index of the matching numpy array
        else:
            index = -1
            for i, arr in enumerate(self.channel_list):
                if np.array_equal(arr, channel_name):
                    index = i
                    break
            return index

    def get_all_possible_hierarchical_mask_connections(
        self, mask_uuid=None, mask_object=None
    ):
        # start from the current annotation and go up the hierarchy
        # to all possible connected mask paths, on a depth first approach
        if not mask_object:
            mask_object = self.get_by_uuid(mask_uuid)

        # find the current class
        current_class_id = mask_object.class_id
        class_list = [current_class_id]
        # find all direct parents to that class
        current_class = current_class_id
        while self.MainWindow.custom_list_widget.classes[
            current_class
        ].parent_class_uuid:
            class_list.append(
                self.MainWindow.custom_list_widget.classes[
                    current_class
                ].parent_class_uuid
            )

        # class_list -> {children , parent , grandparent , ...}
        # find all possible routes from children to root node with a depth first approach
        all_possible_paths = []
        while True:
            depth_i = 0

    def get_pyramidal_path(self):
        return self.pyramidal_image_path

    def set_pyramidal_path(self, path):
        self.pyramidal_image_path = path

    def get_path(self):
        if self.fileRootFolder == "celer_sight_ai:":
            return self.fileRootFolder + self.fileName
        else:
            return os.path.join(self.fileRootFolder, self.fileName)

    def guess_remote(self):
        if self.fileRootFolder == "celer_sight_ai:":
            self._is_remote = True
            return
        self._is_remote = False

    def set_path(self, path):
        self.fileRootFolder = os.path.dirname(path)
        self.fileName = os.path.basename(path)

    def iou(
        self, polygon1: np.ndarray, polygon2: np.ndarray, as_bitmaps: bool = False
    ) -> float:
        """
        Calculate the Intersection over Union (IoU) of two polygons.

        Args:
            polygon1 (np.ndarray): The first polygon, represented as a numpy array of coordinates.
            polygon2 (np.ndarray): The second polygon, represented as a numpy array of coordinates.
            as_bitmaps (bool, optional): If True, treat the inputs as bitmap masks instead of polygons. Defaults to False.

        Returns:
            float: The IoU score, ranging from 0 (no overlap) to 1 (perfect overlap).

        Note:
            This method assumes that the input polygons are valid shapely Polygon objects or compatible numpy arrays.
            The 'as_bitmaps' parameter is currently unused and may be implemented in future versions for bitmap mask comparisons.
        """
        if as_bitmaps:
            intersection = np.logical_and(polygon1, polygon2).sum()
            union = np.logical_or(polygon1, polygon2).sum()
        else:
            intersection = polygon1.intersection(polygon2).area
            union = polygon1.union(polygon2).area

        return intersection / union if union > 0 else 0.0

    def inclusion_score(
        self, polygon1: np.ndarray, polygon2: np.ndarray, as_bitmaps: bool = False
    ) -> float:
        """
        Calculate the Inclusion Score between two polygons.

        Args:
            polygon1 (np.ndarray or shapely.geometry.Polygon): The first polygon.
            polygon2 (np.ndarray or shapely.geometry.Polygon): The second polygon.
            as_bitmaps (bool, optional): If True, interpret the inputs as binary masks (numpy arrays).
                                        If False, interpret the inputs as shapely Polygons. Defaults to False.

        Returns:
            float: The Inclusion Score, ranging from 0 (no overlap) to 1 (polygon1 entirely within polygon2).

        Notes:
            - Inclusion Score = Area of (polygon1 ∩ polygon2) / Area of polygon1
            - The method assumes that inputs are valid polygons or compatible numpy arrays.
        """
        if as_bitmaps:
            # Ensure the inputs are boolean numpy arrays
            if polygon1.dtype != bool:
                polygon1 = polygon1.astype(bool)
            if polygon2.dtype != bool:
                polygon2 = polygon2.astype(bool)

            # Calculate the intersection and area
            intersection = np.logical_and(polygon1, polygon2).sum()
            area_polygon1 = polygon1.sum()
        else:
            # Ensure the inputs are shapely.geometry.Polygon instances
            from shapely.geometry import Polygon

            if isinstance(polygon1, np.ndarray):
                polygon1 = Polygon(polygon1)
            if isinstance(polygon2, np.ndarray):
                polygon2 = Polygon(polygon2)

            try:
                # Calculate the intersection and area
                intersection_area = polygon1.intersection(polygon2).area
            except Exception as e:
                logger.error(f"Error calculating intersection area: {e}")
                return 0.0
            area_polygon1 = polygon1.area

        # Avoid division by zero
        if area_polygon1 == 0:
            return 0.0

        return intersection_area / area_polygon1

    def find_suitable_children(self, mask_A, masks):
        """
        Iterate over all masks, find matching masks by child class id
        compute inclusion score over all possible candidates, and keep all children above a certain threshold

        Args:
            mask_A: The mask object to find children for
            masks: List of all mask objects to search through

        Returns:
            list: List of lists of child mask objects, each sublist represents a level in the hierarchy
        """
        INCLUSION_THRESHOLD = 0.1  # Adjust this threshold as needed
        hierarchy_levels = []
        current_level_masks = [mask_A]
        processed_masks = set()  # Keep track of processed masks

        while current_level_masks:
            next_level_masks = []
            for current_mask in current_level_masks:
                if current_mask.unique_id in processed_masks:
                    continue  # Skip already processed masks
                processed_masks.add(current_mask.unique_id)

                potential_children = []
                current_bbox = current_mask.get_bounding_box()

                child_classes = self.MainWindow.custom_class_list_widget.classes[
                    current_mask.class_id
                ].get_children_classes_uuids()

                for mask_B in masks:
                    if mask_B.unique_id in processed_masks:
                        continue  # Skip already processed masks

                    if mask_B.class_id in child_classes:
                        # Check if bounding boxes overlap
                        mask_B_bbox = mask_B.get_bounding_box()
                        if self.bounding_boxes_overlap(current_bbox, mask_B_bbox):
                            inclusion_score = self.calculate_inclusion_score(
                                current_mask, mask_B
                            )

                            if inclusion_score > INCLUSION_THRESHOLD:
                                potential_children.append((mask_B, inclusion_score))

                if potential_children:
                    # Sort potential children by inclusion score in descending order
                    potential_children.sort(key=lambda x: x[1], reverse=True)
                    next_level_masks.extend([child[0] for child in potential_children])

            if next_level_masks:
                hierarchy_levels.append(next_level_masks)
            current_level_masks = next_level_masks

        return hierarchy_levels  # List of lists, each sublist represents a level in the hierarchy

    def calculate_inclusion_score(self, mask_A, mask_B):
        """Calculate the inclusion score between two masks."""
        if mask_A.mask_type == "bitmap" or mask_B.mask_type == "bitmap":
            bit_mask_1 = mask_A.get_array()
            bit_mask_2 = mask_B.get_array()

            if mask_A.mask_type == "polygon":
                canvas = np.zeros_like(bit_mask_2, dtype=bool)
                rr, cc = self.skimage_draw_polygon_with_holes(mask_A.get_array())
                canvas[cc, rr] = True
                bit_mask_1 = canvas
            elif mask_A.mask_type == "bitmap" and mask_B.mask_type == "polygon":
                canvas = np.zeros_like(bit_mask_1, dtype=bool)
                rr, cc = self.skimage_draw_polygon_with_holes(mask_B.get_array())
                canvas[cc, rr] = True
                bit_mask_2 = canvas

            return self.inclusion_score(bit_mask_2, bit_mask_1, as_bitmaps=True)
        else:
            return self.inclusion_score(
                self.to_shapely(mask_B.get_array_for_storing()),
                self.to_shapely(mask_A.get_array_for_storing()),
            )

    def bounding_boxes_overlap(self, bbox1, bbox2):
        """
        Check if two bounding boxes overlap

        Args:
            bbox1: [x1, y1, w1, h1]
            bbox2: [x2, y2, w2, h2]

        Returns:
            bool: True if bounding boxes overlap, False otherwise
        """
        x1, y1, w1, h1 = bbox1
        x2, y2, w2, h2 = bbox2

        return not (x1 + w1 < x2 or x2 + w2 < x1 or y1 + h1 < y2 or y2 + h2 < y1)

    def find_suitable_parents(self, mask_A, masks):
        """
        Iterate over all masks, find matching masks by parent class id
        compute iou over all possible candidates, and keep all parents above a certain threshold

        Args:
            mask_A: The mask object to find parents for
            masks: List of all mask objects to search through

        Returns:
            list: List of lists of parent mask objects, each sublist represents a level in the hierarchy
        """
        INCLUSION_THRESHOLD = 0.1  # Adjust this threshold as needed
        hierarchy_levels = []
        current_mask = mask_A
        current_level_masks = [current_mask]

        while current_level_masks:
            next_level_masks = []
            for current_mask in current_level_masks:
                potential_parents = []
                current_bbox = current_mask.get_bounding_box()
                parent_class = self.MainWindow.custom_class_list_widget.classes[
                    current_mask.class_id
                ].parent_class_uuid

                for mask_B in masks:
                    if mask_B.class_id == parent_class:
                        mask_B_bbox = mask_B.get_bounding_box()

                        # Quick check if bounding boxes overlap
                        if self.bounding_boxes_overlap(current_bbox, mask_B_bbox):
                            if (
                                mask_B.mask_type == "bitmap"
                                or current_mask.mask_type == "bitmap"
                            ):
                                bit_mask_1 = mask_B.get_array()
                                bit_mask_2 = current_mask.get_array()

                                if mask_B.mask_type == "polygon":
                                    canvas = np.zeros_like(bit_mask_2, dtype=bool)
                                    rr, cc = self.skimage_draw_polygon_with_holes(
                                        mask_B.get_array()
                                    )
                                    canvas[cc, rr] = True
                                    bit_mask_1 = canvas
                                elif (
                                    mask_B.mask_type == "bitmap"
                                    and current_mask.mask_type == "polygon"
                                ):
                                    canvas = np.zeros_like(bit_mask_1, dtype=bool)
                                    rr, cc = self.skimage_draw_polygon_with_holes(
                                        current_mask.get_array()
                                    )
                                    canvas[cc, rr] = True
                                    bit_mask_2 = canvas

                                inclusion_score = self.inclusion_score(
                                    bit_mask_2, bit_mask_1, as_bitmaps=True
                                )
                            else:
                                inclusion_score = self.inclusion_score(
                                    self.to_shapely(
                                        current_mask.get_array_for_storing()
                                    ),
                                    self.to_shapely(mask_B.get_array_for_storing()),
                                )

                            if inclusion_score > INCLUSION_THRESHOLD:
                                potential_parents.append((mask_B, inclusion_score))

                if potential_parents:
                    # Sort potential parents by inclusion score in descending order
                    potential_parents.sort(key=lambda x: x[1], reverse=True)
                    next_level_masks.extend([parent[0] for parent in potential_parents])

            if next_level_masks:
                hierarchy_levels.append(next_level_masks)
            current_level_masks = next_level_masks

        return hierarchy_levels  # List of lists, each sublist represents a level in the hierarchy

    def bounding_boxes_overlap(self, bbox1, bbox2):
        """
        Check if two bounding boxes overlap

        Args:
            bbox1: [x1, y1, w1, h1]
            bbox2: [x2, y2, w2, h2]

        Returns:
            bool: True if bounding boxes overlap, False otherwise
        """
        x1, y1, w1, h1 = bbox1
        x2, y2, w2, h2 = bbox2

        return not (x1 + w1 < x2 or x2 + w2 < x1 or y1 + h1 < y2 or y2 + h2 < y1)

    def generate_group_ids(
        self,
        class_groups=None,
    ):
        """
        Assign spatial and class group IDs to masks based on spatial relationships and class hierarchies.

        Args:
            class_groups (List[List[str]], optional): A list of class groups where each sublist contains
                class IDs that belong to the same group. If not provided, class groups are retrieved from
                the custom class list widget.

        Returns:
            tuple: A tuple containing two dictionaries:
                - spatial_group_d (dict): Maps each mask's unique_id to its spatial group ID.
                - class_to_group_d (dict): Maps each class_id to its class group ID.
        """
        import itertools

        spatial_group_counter = 1  # Start spatial group IDs from 1
        spatial_group_d = {}
        class_to_group_d = {}

        if class_groups is None:
            class_groups = self.MainWindow.custom_class_list_widget.get_class_groups()
        all_masks_in_image = [i for i in self.masks]

        for mask in all_masks_in_image:
            # Retrieve parent masks related spatially
            parent_mask_object_list = self.find_suitable_parents(
                mask, all_masks_in_image
            )
            mask.debug_mask_image()
            if not parent_mask_object_list:
                # add the mask to the spatial group 1
                spatial_group_d[mask.unique_id] = spatial_group_counter
                mask.spatial_id = spatial_group_counter
                spatial_group_counter += 1
                logger.warning(f"No parent masks found for mask UUID: {mask.unique_id}")
            else:
                # use itertools to flatten the list
                parent_mask_object_list = list(
                    itertools.chain(*parent_mask_object_list)
                )
                # Check if any parent mask is already assigned to a spatial group
                existing_groups = [
                    spatial_group_d[obj.unique_id]
                    for obj in parent_mask_object_list
                    if obj.unique_id in spatial_group_d
                ]

                if existing_groups:
                    # Use the first existing spatial group ID found
                    base_group_id = existing_groups[0]
                    for obj in parent_mask_object_list:
                        spatial_group_d[obj.unique_id] = base_group_id
                        obj.spatial_id = base_group_id
                    mask.spatial_id = base_group_id
                    spatial_group_d[mask.unique_id] = base_group_id

                else:
                    # Assign a new spatial group ID to all connected masks
                    for obj in parent_mask_object_list:
                        spatial_group_d[obj.unique_id] = spatial_group_counter
                        obj.spatial_id = spatial_group_counter
                    spatial_group_counter += 1

            # Assign class group IDs based on class_groups
            found_class_group = False
            for idx, group in enumerate(class_groups, start=1):
                if mask.class_id in group:
                    # Assign a class
                    class_to_group_d[mask.class_id] = idx
                    mask.class_group_id = idx
                    found_class_group = True
                    break

            if not found_class_group:
                logger.warning(
                    f"Class ID '{mask.class_id}' not found in any provided class group."
                )
                # Optionally, handle masks with undefined class groups here

        return spatial_group_d, class_to_group_d

    def get_hierarchical_mask(self, mask_object=None, mask_uuid=None, unified=True):
        """
        Get a hierarchical mask based on the given mask object or UUID.

        This method retrieves all masks that overlap or contain the current annotation,
        and checks if polygons overlap, returning a list of all possible masks from child to parent.

        Args:
            mask_object (object, optional): The mask object to process. Defaults to None.
            mask_uuid (str, optional): The UUID of the mask to process. Defaults to None.
            unified (bool, optional): Whether to return a unified mask or a list of masks. Defaults to True.

        Returns:
            list or numpy.ndarray: Depending on the 'unified' parameter, either a list of masks or a single unified mask.
        """
        import shapely
        from shapely import ops
        import logging

        logger = logging.getLogger(__name__)

        try:
            if not mask_object:
                if not mask_uuid:
                    raise ValueError("Either mask_object or mask_uuid must be provided")
                mask_object = self.get_by_uuid(mask_uuid)
                if not mask_object:
                    raise ValueError(f"No mask found with UUID: {mask_uuid}")

            pol = mask_object.get_array_for_storing()
            current_polygon = self.to_shapely(pol)
            if not current_polygon.is_valid:
                current_polygon = shapely.make_valid(current_polygon)

            parental_class_ids = (
                self.MainWindow.custom_class_list_widget.get_parental_classes(
                    mask_object.class_id
                )
            )

            if not parental_class_ids:
                return pol if unified else [pol]

            unified_masks = []
            for class_id in parental_class_ids:
                masks_of_class = [
                    self.to_shapely(m.get_array_for_storing())
                    for m in self.masks
                    if m.class_id == class_id
                ]

                if not masks_of_class:
                    logger.warning(f"No masks found for class ID: {class_id}")
                    continue

                try:
                    mu = shapely.ops.unary_union(masks_of_class)
                except Exception as e:
                    logger.warning(f"Error in unary_union for class {class_id}: {e}")
                    mu = shapely.ops.unary_union(
                        [shapely.make_valid(i) for i in masks_of_class]
                    )

                if not unified:
                    intersection = current_polygon.intersection(mu)
                    if not intersection.is_empty:
                        unified_masks.append(self.from_shapely(intersection))
                else:
                    unified_masks.append(mu)

            if unified:
                for m in unified_masks:
                    current_polygon = current_polygon.intersection(m)
                    if current_polygon.is_empty:
                        logger.warning("Intersection resulted in an empty polygon")
                        return []
                return self.from_shapely(current_polygon)
            else:
                return unified_masks if unified_masks else [pol]

        except Exception as e:
            logger.error(f"Error in get_hierarchical_mask: {e}")
            return None

    def get_overlaping_annotation_bitmap(
        self,
        group_name,
        coondition_id,
        image_idx,
        source_class,
        destination_annotation_uuid,
        image_width,
        image_height,
    ):
        """
        returns the overlap between all of the source classes and the destination annotation
        """
        canvas = np.zeros((image_width, image_height))
        anno_object = self.get_by_uuid(destination_annotation_uuid)

        # get all of the source classes
        annotations_of_class = (
            self.MainWindow.DH.BLobj.get_all_annotations_on_image_from_classes_id(
                group_name, coondition_id, image_idx, source_class
            )
        )

        # get all annotations that are polygon and combine them
        poly_annos = [
            i.get_array_for_storing()
            for i in annotations_of_class
            if i.mask_type == "polygon"
        ]
        rr, cc = self.skimage_draw_polygon_with_holes(poly_annos)
        if isinstance(rr, None):
            return canvas
        canvas[rr, cc] = 1
        bitmap_annos = [
            i.get_array_for_storing()
            for i in annotations_of_class
            if i.mask_type == "bitmap"
        ]
        for bitmap_anno in bitmap_annos:
            canvas += bitmap_anno.get_array() // 255
        canvas = np.clip(canvas, 0, 1)

        # get array
        anno_arr = anno_object.get_array()
        if anno_object.mask_type == "polygon":
            rr, cc = self.skimage_draw_polygon_with_holes(anno_arr)
            if isinstance(rr, None):
                return canvas
        canvas[rr, cc] = 0
        return canvas

    def skimage_draw_polygon_with_holes(self, polygons):
        import skimage

        # main polygon
        rr, cc = skimage.draw.polygon(polygons[0][:, 0], polygons[0][:, 1])
        main_polygon_set = set(zip(rr, cc))
        try:
            # subtract holes
            for i in range(1, len(polygons)):
                c_poly = polygons[i].squeeze()
                rr, cc = skimage.draw.polygon(c_poly[:, 0], c_poly[:, 1])
                hole_set = set(zip(rr, cc))
                main_polygon_set -= hole_set
        except Exception as e:
            print(e)
        # get final rr, cc coordinates
        rr_final, cc_final = zip(*list(main_polygon_set))
        return rr_final, cc_final

    def change_mask_uuid(self, existing_uuid, new_uuid):
        if new_uuid == existing_uuid:
            return
        else:
            # Handle scene objects
            # change the uuid on the scene object
            tmp_item = self.masks[existing_uuid]
            self.masks.pop(existing_uuid)
            self.masks[new_uuid] = tmp_item
            self.masks[new_uuid].unique_id = new_uuid

            # change the uuid on the annotation item
            scene_annotation_item = self.masks[new_uuid].get_annotation_item()
            if scene_annotation_item:
                # if item is found, adjust its id
                scene_annotation_item.unique_id = new_uuid

    def get_by_uuid(self, uuid):
        for i in self.masks:
            if i.unique_id == uuid:
                return i

    def del_by_uuid(self, uuid):
        """
        Delete a mask and its children by UUID.

        Args:
            uuid (str): The unique identifier of the mask to delete.

        Returns:
            None
        """
        logger.info(f"Deleting mask with UUID: {uuid}")
        mask_to_delete = self.get_by_uuid(uuid)
        if not mask_to_delete:
            logger.warning(f"No mask found with UUID: {uuid}")
            return

        # Get all masks and find suitable children
        all_masks = list(self.masks)
        child_hierarchy = self.find_suitable_children(mask_to_delete, all_masks)

        # Flatten the hierarchy list and include the original mask
        masks_to_delete = [mask_to_delete] + [
            mask for level in child_hierarchy for mask in level
        ]

        for mask in masks_to_delete:
            self.MainWindow.DH.BLobj.object_mapping[mask.unique_id] = None
            anno_item = mask.get_annotation_item()
            if anno_item:
                anno_item.cleanup_scene_items()
            self._remove_mask_from_scene(mask)
            del self.masks[mask.unique_id]
        self._update_mask_count()

        return masks_to_delete

    def _remove_mask_from_scene(self, mask):
        """Remove the mask from the viewer scene if present."""
        if self.MainWindow.viewer.scene():
            ann_item = mask.get_annotation_item()
            if ann_item:
                self.MainWindow.viewer.scene().removeItem(ann_item)

    def get_all_possible_tiles(self, tile_groups, skip_lower_than_overlap=False):

        from celer_sight_ai.io.image_reader import (
            generate_complete_spiral_tiles,
            crop_and_pad_image,
        )

        image_width = self.getSizeX()
        image_height = self.getSizeY()
        image_center = [image_width / 2, image_height / 2]
        if not image_width or not image_height:
            return {}
        result = {}
        for tile_group in tile_groups:
            # Set default tile size if tile_group is None
            if tile_groups[tile_group] is None:
                tile_width = min(640, image_width)
                tile_height = min(640, image_height)
            else:
                tile_width = tile_groups[tile_group]["tile_size"]
                tile_height = tile_groups[tile_group]["tile_size"]

            overlap = 0.2 * tile_width  # get overlap in pixels
            image_center = [image_width / 2, image_height / 2]

            initial_bbox = [
                image_center[0] - (tile_width / 2),
                image_center[1] - (tile_height / 2),
                tile_width,
                tile_height,
            ]
            tiles = generate_complete_spiral_tiles(
                image_width,
                image_height,
                initial_bbox,
                overlap,
                skip_lower_than_overlap,
            )
            result[tile_group] = tiles
        return result

    def _update_mask_count(self):
        """Update the mask count label in the viewer."""
        self.MainWindow.viewer.updateMaskCountLabel()

    def is_remote(self):
        if self._is_remote or str(self.fileRootFolder).lower().startswith(
            "celer_sight_ai:"
        ):
            return True
        return False

    def is_image_cached(self):
        return self.is_cached

    def cache_image(self, image_array):
        self.is_cached = True
        img_name_on_cache = self.unique_id + ".jpeg"
        # save image to disk
        cv2.imwrite(
            os.path.join(config.cache_dir, img_name_on_cache),
            image_array,
        )

    def readImage(self):
        # Should be adjusted with **kwargs
        image, result_dict = readImage(self.getPath(), self._is_video)
        channels_read = result_dict.get("channels", None)
        if channels_read:
            self.channel_list = channels_read
        return image, result_dict

    def setHasBeenUploaded(self, value):
        self.hasBeenUploaded = value

    def setUserModifiedAnnotation(self, value: bool = False) -> None:
        self.userModifiedAnnotation = value

    def getID(self):
        return self.imgID

    def setID(self, id):
        self.imgID = id

    def get_treatment_uuid(self):
        return self.treatment_uuid

    def set_treatment_uuid(self, treatment_uuid):
        self.treatment_uuid = treatment_uuid

    def setButtonReference(self, buttonRef):
        self.myButton.button_instance = buttonRef

        config.global_signals.startInferenceAnimationSignal.connect(
            self.myButton.button_instance.startInferenceAnimation
        )
        config.global_signals.check_and_end_inference_animation_signal.connect(
            self.check_and_end_inference_animation
        )

    def setup_channels(self):
        from celer_sight_ai.io.image_reader import channel_to_color

        # setups the channels to be visible in the buttons
        if not isinstance(self.channel_list, type(None)):
            self.myButton.button_instance.set_channels(
                [channel_to_color(i) for i in self.channel_list]
            )
        else:
            logger.debug("No channels found for image: " + self.fileName)

    def check_and_end_inference_animation(self, object=None, force=False):
        # ends animation that is playing only when inference is happening on the buttonAsset widget
        # check if current inferenced image is the one that the viewer is currently showing
        # if so, update the viewer
        from celer_sight_ai import config

        # make sure that there is no current inference requests pending

        if not object and force:
            # forcefully stop anyway
            QtWidgets.QApplication.processEvents()

            # check these here so that when the user changes conditions
            # we dont get errors due to non initialized buttons.
            if hasattr(self, "myButton") and hasattr(self.myButton, "button_instance"):
                if not self.myButton.button_instance:
                    return
                try:
                    label_widget = self.myButton.button_instance.findChild(
                        QtWidgets.QWidget, "checkLabel"
                    )
                    label_widget.hide()
                    if hasattr(self.myButton.button_instance, "movie"):
                        self.myButton.button_instance.movie.stop()
                        self.during_animation = False
                except Exception as e:
                    logger.error(e)
                    self.during_animation = False
            return
        image_uuid = object.get("image_uuid")
        if not image_uuid:
            return
        # if the treatment is not provided, get it

        if image_uuid == self.unique_id:  # is the image uuid now
            # make sure that there is no other running inferences, if so abort
            inference_requests_remaining = len(
                [
                    i
                    for i in self.MainWindow.MyInferenceHandler.inference_uuids
                    if self.MainWindow.MyInferenceHandler.inference_uuids[i].get(
                        "image_uuid"
                    )
                    == image_uuid
                ]
            )
            if inference_requests_remaining > 1:
                return
            # check these here so that when the user changes conditions
            # we dont get errors due to non initialized buttons.
            if hasattr(self, "myButton") and hasattr(self.myButton, "button_instance"):
                if not self.myButton.button_instance:
                    return
                try:
                    label_widget = self.myButton.button_instance.findChild(
                        QtWidgets.QWidget, "checkLabel"
                    )
                    label_widget.hide()
                    if hasattr(self.myButton.button_instance, "movie"):
                        self.myButton.button_instance.movie.stop()
                        self.during_animation = False
                except Exception as e:
                    logger.error(e)
                    self.during_animation = False

    def addMaskWithClass(
        self,
        polygon_array,
        class_id=None,
        mask_type=None,
        unique_id=None,
        visibility=True,
        includedInAnalysis=True,
        is_suggested=False,
        score=1.0,
        mask_uuid=None,
    ):
        """
        Creates the mask object directly, appends it to hata handler, returns the uuid of that mask object

        Args:
            polygon_array (np.ndarr): polygon array that describes the annotation.
            classStr (str, optional): class id of the mask. Defaults to None.
            mask_type (str, optional): mask type (polygon, bitmap etc.). Defaults to None.

        Returns:
            str: mask uuid
        """
        if class_id == None:
            class_id = self.custom_class_list_widget.currentItemWidget().unique_id
        mask_obj = maskObj(
            self.MainWindow,
            polygon_array,
            class_id=class_id,
            mask_type=mask_type,
            unique_id=unique_id,
            visibility=visibility,
            includedInAnalysis=includedInAnalysis,
            is_suggested=is_suggested,
            score=score,
            image_uuid=self.unique_id,
        )
        self.masks.append(mask_obj)
        # return the unique id of the mask
        return mask_obj.unique_id

    def change_class(self, mask_uuid, classStr):
        """Change the class on the class object as well as the
           qgraphics item on the scene

        Args:
            mask_uuid (_type_): uuid of the mask to change.
            classStr (_type_): class to change it too.
        """
        self.get_by_uuid(mask_uuid).class_id = classStr
        from celer_sight_ai import config

        config.global_signals.update_class_scene_color_signal.emit(mask_uuid)

    def clearMasks(self):
        self.masks = MaskContainer(self.MainWindow)


# DH.mask_RNAi_slots_QPoints[self.MainWindow.DH.BLobj.get_current_condition()] -->
# DH.BLobj.groups['default'].conds[self.MainWindow.DH.BLobj.get_current_condition()].images[self.MainWindow.current_imagenumber].masks


# DH.mask_RNAi_slots_QPoints[self.MainWindow.DH.BLobj.get_current_condition()][self.MainWindow.current_imagenumber][p] -->
# DH.BLobj.groups['default'].conds[self.MainWindow.DH.BLobj.get_current_condition()].images[self.MainWindow.current_imagenumber].masks


class MaskContainer:
    def __init__(self, MainWindow=None):
        self.MainWindow = MainWindow
        self.data = {}
        self.list = []

    def get(self, item) -> Any | None:
        return self.data.get(item)

    def __len__(self):
        # assert len(self.data) == len(self.list)
        return len(self.list)

    def __getitem__(self, key):
        if isinstance(key, type(uuid.uuid4)):
            key = config.get_unique_id()
        if isinstance(key, int):
            return self.list[key]
        if isinstance(key, str):
            return self.data[key]

    def __setitem__(self, key, value):
        if isinstance(key, maskObj):
            self.list.append(key)
            unique_id = str(config.get_unique_id())
            value.unique_id = unique_id
            self.data[unique_id] = value

        if isinstance(key, int):
            if key < len(self.list):
                self.list[key] = value
            else:
                # Allow for appending to list
                self.list.append(value)
        elif isinstance(key, str):
            value.unique_id = key
            self.data[key] = value

    def __delitem__(self, key):
        if isinstance(key, int):
            # Delete from list by index
            item = self.list.pop(key)
            # Find and delete the corresponding item from the dictionary
            for dict_key, dict_item in list(self.data.items()):
                if dict_item == item:
                    del self.data[dict_key]
                    break
        elif isinstance(key, str):
            # Delete from dictionary by key
            item = self.data.pop(key)
            # Find and delete the corresponding item from the list
            self.list = [x for x in self.list if x != item]
        # delete from the object mapping
        del self.MainWindow.DH.BLobj.object_mapping[key]

    def pop(self, key):
        # pop by key on the dictionary and the list reference
        if isinstance(key, int):
            self.list.pop(key)
        else:
            # remove from dictionary
            val = self.data.pop(key)
            # remove from list
            for i, mask in enumerate(self.list):
                if mask == val:
                    self.list.pop(i)
                    return val

    # handle iterations
    def __iter__(self):
        # use the list to iterate
        return iter(self.list)

    # Append method for adding items to the list
    def append(self, value):  # --> value here is a maskObj
        if not isinstance(value, maskObj):
            raise TypeError("Only maskObj can be added to MaskContainer")
        unique_id = str(value.unique_id)
        value.unique_id = unique_id
        self.list.append(value)
        # create a uuid for the maskObj
        self.data[unique_id] = value


class maskObj:
    """
    masks types can be:
    point
    line
    polygon -> needs to be a list
    bounding_box
    bitmap
    """

    def __init__(
        self,
        MainWindow,
        polygon_array,
        class_id=None,
        mask_type=None,
        unique_id=None,
        visibility=True,
        includedInAnalysis=None,
        is_suggested=False,
        image_uuid=None,
        score=1.0,
    ):
        self.MainWindow = MainWindow
        self.includedInAnalysis = includedInAnalysis
        self.Label = None
        self.visibility = visibility
        self.mask_type = mask_type
        self.set_array(polygon_array)  # numpy array
        self.is_suggested = is_suggested
        self.score = score
        self.class_id = class_id  # is the default
        self.class_group_id = None  # id that designates classes in the same hierarchy
        self.spatial_id = None  # id that designates if the masks are spatialy connected
        self.image_uuid = image_uuid
        # # when a temporary, suggested, mask is generated,
        # # if the user accepts it, it becomes permanent
        # self.is_suggestion_mask = False

        # video attributes
        self._annotation_track_id = None

        if not unique_id:
            self.unique_id = config.get_unique_id()
        else:
            self.unique_id = unique_id
        self.intensity_metrics = (
            {}
        )  #  keys can be: "channel":{ 'mean', 'median', 'std', 'min', 'max' and 'sum'}
        self.particle_metrics = {}
        self.digestifyMask()
        self.MainWindow.DH.BLobj.object_mapping[self.unique_id] = self

    @property
    def unique_id(self):
        """Get the image ID."""
        return self._unique_id

    @unique_id.setter
    def unique_id(self, value: str):
        """Set the image ID.

        Args:
            value: The new image ID value
        """
        if not isinstance(value, str):
            raise ValueError("UUID must be a string")
        self._unique_id = value

    def debug_mask_image(self):
        """
        Generates a crop of the image around the mask and draws the mask on the image
        """
        import copy

        if self.mask_type != "polygon":
            logger.error("Mask type is not polygon")
            NotImplementedError("Mask type is not polygon")
            return
        # get the mask
        polygon_array = copy.deepcopy(self.get_array())  # the array is in coco format
        # coco format of the instance segmentation is [mask , hole , hole,...] and every mask shape is (N, 2)
        bbox = self.get_bounding_box()
        if bbox is None:
            logger.warning("Bounding box is None in maskObj.debug_mask_image")
            return
        # get the image that contains this mask
        image_object = self.MainWindow.DH.BLobj.get_image_object_by_mask_uuid(
            self.unique_id
        )
        # convert bbox from [x1 , y1, x2 , y2] to [x1 , y1, w , h]
        # bbox_wh = [bbox[0], bbox[1], bbox[2]-bbox[0], bbox[3]-bbox[1]]
        img = image_object.getImage(to_uint8=True, to_rgb=True, bbox=bbox)
        # crop the polygon array to the bbox
        polygon_array = polygon_array[0]
        polygon_array[:, 0] = polygon_array[:, 0] - bbox[0]
        polygon_array[:, 1] = polygon_array[:, 1] - bbox[1]
        # draw the polygon
        cv2.drawContours(img, [polygon_array.astype(np.int32)], -1, (0, 255, 0), 2)
        # show the image
        config.dbg_image(img)
        print()

    def set_annotation_track_id(self, id=None):
        if id:
            self._annotation_track_id = id

    def set_array(self, arr):
        from pycocotools import mask as coco_mask

        if self.mask_type == "bitmap":
            # convert to RLE and store to save space
            self.polygon_array = coco_mask.encode(np.asfortranarray(arr))
        else:
            self.polygon_array = arr

    def get_array_for_storing(self):
        import copy

        # used to convert binary object to string for storage
        if self.mask_type == "bitmap":
            # convert to RLE and store to save space
            arr = copy.deepcopy(self.polygon_array)
            arr["counts"] = arr["counts"].hex()
            return arr
        else:
            return self.polygon_array

    def get_array(self) -> Union[np.ndarray, list]:
        """Get the mask array in the appropriate format.

        Returns:
            Union[np.ndarray, list]: For bitmap masks, returns decoded RLE as ndarray.
                                    For polygon masks, returns the polygon array as list.
                                    For unsupported types, returns empty ndarray.
        """
        from pycocotools import mask as coco_mask

        if self.polygon_array:
            if self.mask_type == "bitmap":
                return coco_mask.decode(self.polygon_array) * 255
            elif self.mask_type == "polygon":
                return self.polygon_array  # type: ignore
            else:
                logger.error(f"Mask type {self.mask_type} not supported")
                return np.array([])
        else:
            return np.array([])

    def is_particle(self):
        # Trace the class object and determine if current class
        # is a particles class
        return self.MainWindow.custom_class_list_widget.classes[
            self.class_id
        ].is_particle

    def get_bounding_box(self):
        """
        Compute the bounding box of the annotation
        Returns:
            bbox in shape [minx, miny, width, height]
        """
        arr = self.get_array()
        if self.mask_type == "bitmap":
            logger.error("Cannot compute bounding box for bitmap mask")
            return None
        if self.is_particle():
            # No bounding box for particles
            return None
        minx = np.min(arr[0][:, 0])
        maxx = np.max(arr[0][:, 0])
        miny = np.min(arr[0][:, 1])
        maxy = np.max(arr[0][:, 1])

        return [minx, miny, maxx - minx, maxy - miny]

    def get_centroid(self):
        from shapely.geometry import Polygon

        if self.polygon_array:
            points = self.get_array()[0]
            # Create a Polygon object
            polygon = Polygon(points)
            # Get the centroid of the Polygon
            return [polygon.centroid.x, polygon.centroid.y]
        else:
            return None

    def update_point(self, point_pos=None, new_value=None, array_pos=None):
        """
        Function to update a point in a list of numpy arrays.
        Update the self.polygon_array with the new point
        If the point > len(self.point_index[0]) then modify the next polygon_array and so on

        Args:
        arr_list : list of numpy arrays
        point_pos : position of the point to update
        new_value : new value to be updated at the position
        array_pos: [main polygon , hole1 , hole2 , ...] -> if this value is given we can skip the search
        Returns:
        updated list of numpy arrays
        """
        logger.debug(f"Updating point {point_pos} with value {new_value}")
        if not array_pos:
            # calculate cumulative lengths of arrays
            cumulative_lengths = np.cumsum([len(arr) for arr in self.get_array()])

            # find the array that contains the point
            for i, cum_len in enumerate(cumulative_lengths):
                if point_pos < cum_len:
                    # calculate the index in the found array
                    if i == 0:
                        index_in_arr = point_pos
                    else:
                        index_in_arr = point_pos - cumulative_lengths[i - 1]
                    # update the point
                    array_list = self.get_array()
                    if isinstance(array_list, list) and i < len(array_list):
                        array_list[i][index_in_arr] = new_value
                    break
        else:
            # update the point
            point_pos_sum = sum(
                [len(self.polygon_array[i]) for i in range(array_pos - 1)]
            )
            try:
                self.get_array()[array_pos][point_pos_sum + point_pos] = new_value
            except Exception as e:
                logger.error(e)

    def get_image_id(self):
        # look by mask uuid on the image container
        # Returns image id not uuid
        g = self.MainWindow.DH.BLobj.groups["default"]
        for c in g.conds:
            for i, io in enumerate(g.conds[c].images):
                if io.masks.get(self.unique_id):
                    return i
        return None

    def get_annotation_item(self):
        """
        Returns the annotation item of the scene, if it does not exists, or if the current image
        is not the image of the current mask, return None.
        """
        if self.get_image_id() == self.MainWindow.current_imagenumber:
            items = self.MainWindow.viewer.scene().items()
            matched_items = [
                i
                for i in items
                if hasattr(i, "unique_id") and i.unique_id == self.unique_id
            ]
            if matched_items:
                return matched_items[0]
        return None

    def digestifyMask(self):  # type: ignore
        """
        If there is no mask type assigned, guess it.
        """
        if self.mask_type is None:
            arr = self.get_array()
            if isinstance(arr, (list, np.ndarray)) and len(arr) == 1:
                if not isinstance(arr[0], (np.ndarray, list)):
                    self.mask_type = "point"
            if (
                isinstance(self.get_array(), (list, np.ndarray))
                and len(self.get_array()) == 2
            ):
                self.mask_type = "line"
            if len(arr) == 4:
                try:
                    angles = []
                    # # find angle between points
                    # # if angle is 90 degrees, then it is a bounding box
                    # # if angle is not 90 degrees, then it is a polygon
                    assert len(arr) == 4
                    for i in range(len(arr)):  # should be 4
                        i1 = i
                        i2 = (i + 1) % 4
                        i3 = (i + 2) % 4
                        if isinstance(arr[i1], np.ndarray):
                            a = np.array(
                                [
                                    int(arr[i1][0]),
                                    int(arr[i1][1]),
                                ]
                            )
                            b = np.array(
                                [
                                    int(arr[i2][0]),
                                    int(arr[i2][1]),
                                ]
                            )
                            c = np.array(
                                [
                                    int(arr[i3][0]),
                                    int(arr[i3][1]),
                                ]
                            )
                        else:
                            # Handle case where arr contains QPointF objects
                            a = np.array(
                                [
                                    int(arr[i1].x()),
                                    int(arr[i1].y()),
                                ]
                            )
                            b = np.array(
                                [
                                    int(arr[i2].x()),
                                    int(arr[i2].y()),
                                ]
                            )
                            c = np.array(
                                [
                                    int(arr[i3].x()),
                                    int(arr[i3].y()),
                                ]
                            )

                        ba = a - b
                        bc = c - b

                        cosine_angle = np.dot(ba, bc) / (
                            np.linalg.norm(ba) * np.linalg.norm(bc)
                        )
                        angles.append(int(np.arccos(cosine_angle)))
                    if (
                        angles[0] == 90
                        and angles[1] == 90
                        and angles[2] == 90
                        and angles[3] == 90
                    ):
                        self.mask_type = "bounding_box"
                    else:
                        self.mask_type = "polygon"
                except Exception as e:
                    logger.info(e)
                    self.mask_type = "polygon"
            else:
                self.mask_type = "polygon"

    def setVisibility(self, Viz=True):
        self.visibility = Viz

    def setClass(self, className):
        self.class_id = className

    def getPolyArr(self):
        # returns QPolygonF to numpy array
        # assume [[main polygon , hole 1 , hole 2] , []]
        all_poly = []
        for poly in self.get_array():
            all_poly.append([[i.x(), i.y()] for i in poly])
        return all_poly


def get_tile_range_from_annotation_size(
    annotation_size, min_percentage, max_percentage
):
    """
    Given a percentage of the desired annotation size in the file tile, get the tile size range
    Returns:
        tuple: (min_size, max_size  )
    """
    if not annotation_size:
        return 1024, 1024
    return (
        int(round(annotation_size / max_percentage)),
        int(round(annotation_size / min_percentage)),
    )
