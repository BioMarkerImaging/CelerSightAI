import sys

import os
from celer_sight_ai import config

import os

os.chdir(os.environ["CELER_SIGHT_AI_HOME"])
import ssl
import time

ssl._create_default_https_context = ssl._create_unverified_context
import logging

logger = logging.getLogger(__name__)
import cv2
import os
import numpy as np
import json
from PyQt6 import QtGui, QtCore, QtWidgets
import time
from celer_sight_ai import config
import random
from typing import Tuple, List
from celer_sight_ai.historyStack import (
    AddPolygonCommand,
    AddBitMapCommand,
    DeleteMaskCommand,
    DeleteHoleCommand,
)

import logging
from shapely.geometry import Polygon

logger = logging.getLogger(__name__)


def calculate_polygon_width(vertices):
    import numpy as np
    from skimage.draw import polygon
    from scipy.ndimage import distance_transform_edt

    # Calculate the bounds of the polygon
    min_row, min_col = np.min(vertices, axis=0)
    max_row, max_col = np.max(vertices, axis=0)

    # Offset the vertices to the new bounding box
    offset_vertices = vertices - np.array([min_row, min_col])
    mask_shape = (50, 50)
    # get the max size and resize by that
    max_side = max(max_row - min_row + 1, max_col - min_col + 1)

    scale = mask_shape[0] / max_side
    resized_vertices = offset_vertices * scale

    # Create a binary mask with the resized shape
    mask = np.zeros(mask_shape, dtype=bool)
    rr, cc = polygon(resized_vertices[:, 0], resized_vertices[:, 1], shape=mask_shape)
    mask[rr, cc] = True
    # make all sides of the array 0
    mask[0, :] = 0
    mask[-1, :] = 0
    mask[:, 0] = 0
    mask[:, -1] = 0
    print()
    # Compute the distance transform
    # This gives the distance from each pixel to the nearest boundary
    dist_transform = distance_transform_edt(mask)
    if isinstance(dist_transform, type(None)):
        return max_side
    config.dbg_image(dist_transform * 100)
    # Find the radius of the largest inscribed circle
    # (maximum value in the distance transform)
    radius = (np.max(dist_transform) * 2) / scale

    side_weight = 0.1
    distance_weight = 0.9

    return (side_weight * max_side) + (distance_weight * radius)


def is_polygon_close_to_edge(vertices, image_shape, threshold=10):
    """
    Checks if a polygon defined by 'vertices' is close to the boundary of an image of 'image_shape'.

    Parameters:
        vertices (np.array): An array of shape (n, 2) where each row represents the x and y coordinates of a vertex.
        image_shape (tuple): A tuple (height, width) representing the dimensions of the image.
        threshold (int): The distance to the edge below which the polygon is considered close.

    Returns:
        bool: True if the polygon is close to the edge, False otherwise.
    """
    # Get the minimum and maxiamum vertex coordinates
    min_row, min_col = np.min(vertices, axis=0)
    max_row, max_col = np.max(vertices, axis=0)

    # Get the dimensions of the image
    height, width = image_shape

    # Check proximity to each edge
    close_to_top = min_row <= threshold
    close_to_bottom = (height - max_row) <= threshold
    close_to_left = min_col <= threshold
    close_to_right = (width - max_col) <= threshold

    return close_to_top or close_to_bottom or close_to_left or close_to_right


class InferenceHandler:
    import os
    import math

    def __init__(self, MainWindowRef=None, input_image=None):
        self.MainWindowRef = MainWindowRef
        self.input_image = input_image
        self.height = None  # of the cut
        self.width = None  # of the cut
        self.running = False  # if we are currently grabcutting
        self.brush_state = "plus"  # or "minus" or move?
        self.prevInferenceTimes = [2, 2, 2]
        self.is_inference_running = False
        self.is_inference_completed = True
        config.global_signals.inferenceSessionLabelServer.connect(
            self.message_from_server_during_inference
        )
        config.global_signals.inferenceResultLabelServer.connect(self.onJobComplete)
        self._inference_retrieval_running = False
        self._stop_inference_retrieval = False
        self.inference_uuids = {}

    @config.threaded
    def start_inference_retrival(
        self,
        start_interval=0.5,
        max_interval=2.0,
        ignore_running_inference=False,
        min_wait_time=5,
    ) -> None:
        """
        Retrieves inference results until all of the requests are satisfied,
        a timeout is reached, or the user cancels the process.
        """
        self._inference_retrieval_running = True
        start_time = time.time()
        interval = start_interval
        error_occured = False
        end_time = None
        wait_time_max_for_no_inference_uuids = 4  # seconds
        try:
            while True:
                with config.lock:
                    if self.is_inference_completed:
                        if not self.inference_uuids:
                            # Ensure minimum wait time
                            if not end_time:
                                end_time = time.time()
                                continue
                            elif (
                                abs(time.time() - end_time)
                                > wait_time_max_for_no_inference_uuids
                            ):
                                logger.debug(
                                    "No inference uuids and inference is not running. Exiting."
                                )
                                break
                        elif self._stop_inference_retrieval:

                            logger.debug(
                                "Stopping inference retrieval due to stop flag."
                            )
                            # if there are inference uuids left, wait 3 seconds and retrieve them before exiting
                            if self.inference_uuids:
                                # Retrieve inference results
                                result_data = config.client.retrieve_inference_data(
                                    self.inference_uuids
                                )
                                if result_data.get("completed_inference"):
                                    # Ingest the results
                                    self.ingest_inference_results(result_data)
                                    break

                            break
                    elif self._stop_inference_retrieval:
                        # Ensure minimum wait time
                        if time.time() - start_time < min_wait_time:
                            time.sleep(0.1)
                            continue
                        logger.debug("Stopping inference retrieval due to stop flag.")
                        break

                # Retrieve inference results
                result_data = config.client.retrieve_inference_data(
                    self.inference_uuids
                )
                if not result_data.get("completed_inference"):
                    time.sleep(interval)
                    interval = min(interval * 1.1, max_interval)
                    continue
                else:
                    # Reset interval after successful retrieval
                    interval = start_interval

                # Ingest the results
                self.ingest_inference_results(result_data)

                # Check if there are any remaining inference uuids
                with config.lock:
                    if not self.inference_uuids and not self.is_inference_running:
                        logger.debug("All inference results processed. Exiting.")
                        break

                time.sleep(0.1)

        except Exception as e:
            error_occured = True
            logger.error(f"Error during inference retrieval: {e}")

        finally:
            self._inference_retrieval_running = False
            self._stop_inference_retrieval = False
            config.global_signals.unlock_ui_signal.emit()

            if not error_occured:
                self.complete_inference_sessions(success=True)
            else:
                config.global_signals.errorSignal.emit(
                    "Error occurred during inference"
                )
                self.complete_inference_sessions(success=False)

    def ingest_inference_results(self, results):
        """
        Ingests inference results from the server and updates the masks in the UI.
        """
        import copy

        if not self.inference_uuids:
            return
        if not results.get("completed_inference"):
            return

        for r in results.get("completed_inference"):
            # Get the inference object by UUID
            inference_object = self.inference_uuids.get(r["inference_id"])
            if not inference_object:
                continue
            image_uuid = inference_object.get("image_uuid")
            img_obj = self.MainWindowRef.DH.BLobj.get_image_object_by_uuid(image_uuid)
            if not img_obj:
                # Image object not found, skip
                logger.warning(f"Could not find image object by uuid: {image_uuid}")
                continue
            config.inference_buffer -= 1

            # Remove the tile graphics item associated with this inference
            config.global_signals.remove_inference_tile_graphics_item_signal.emit(
                {"inference_uuid": r["inference_id"]}
            )
            source_tile = copy.deepcopy(inference_object.get("source_tile"))
            # Process the results
            results_to_process = []
            if r.get("result"):
                for rr in r["result"]:
                    if rr.get("confidence", 0) < 0.2:
                        continue
                    if not rr.get("segmentation"):
                        continue
                    if is_polygon_close_to_edge(
                        rr["segmentation"][0],
                        inference_object.get("send_image_dimention"),
                    ):
                        continue
                    results_to_process.append(rr)
                logger.debug(
                    f"Total annotations to process {len(results_to_process)} for tile {inference_object.get('source_tile')}"
                )

            else:
                logger.warning(
                    f"No results found for inference ID {r['inference_id']}."
                )

            config.global_signals.create_annotations_objects_signal.emit(
                [
                    {
                        "array": result_to_process["segmentation"],
                        "image_uuid": image_uuid,
                        "class_id": result_to_process["class"],
                        "mask_type": "polygon",
                        "source_tile": source_tile,
                        "remove_polygons_close_to_edge": True,
                        "processed_tile_dimention": inference_object.get(
                            "send_image_dimention"
                        ),
                    }
                    for result_to_process in results_to_process
                ]
            )
            # Remove the inference UUID
            if self.inference_uuids.get(r["inference_id"]):
                del self.inference_uuids[r["inference_id"]]

            config.global_signals.check_and_end_inference_animation_signal.emit(
                {"image_uuid": image_uuid}
            )

    @config.threaded
    def stop_inference_retrieval(self):
        self._stop_inference_retrieval = True
        # wait for the process to stop
        while self._inference_retrieval_running:
            time.sleep(0.1)
        return True

    def display_time(self, seconds, granularity=2):
        result = []
        intervals = (
            ("weeks", 604800),  # 60 * 60 * 24 * 7
            ("days", 86400),  # 60 * 60 * 24
            ("hours", 3600),  # 60 * 60
            ("minutes", 60),
            ("seconds", 1),
        )

        for name, count in intervals:
            value = seconds // count
            if value:
                seconds -= value * count
                if value == 1:
                    name = name.rstrip("s")
                result.append("{} {}".format(value, name))
        return ", ".join(result[:granularity])

    def cancel_inference(self):
        """
        Gets triggered once the user cancel infrenece by pressing the get_roi_ai_button, which is
        now red with 'cance' text on it."""

        # reconnect all signals
        for t in config.inference_threads:
            t.stop()
        config.stop_inference = True

        # stop inference animation for all image buttons
        config.global_signals.endAllInferenceLoadingSignals.emit()
        # stop the timer
        self.MainWindowRef.get_roi_ai_button.clicked.connect(
            lambda: self.MainWindowRef.get_roi_ai_button._timer.force_stop()
        )
        # process events
        self.MainWindowRef.get_roi_ai_button.clicked.connect(
            lambda: QtWidgets.QApplication.processEvents()
        )

        # stop the inference retrieval, threaded
        self.stop_inference_retrieval()

        # Set to the normal state
        self.MainWindowRef.get_roi_ai_button.clicked.connect(
            lambda: self.MainWindowRef.MyInferenceHandler.DoInferenceAllImagesOnlineThreaded()
        )

        self.revert_get_ai_roi_button_back_to_normal()

    def revert_get_ai_roi_button_back_to_normal(self):
        self.MainWindowRef.get_roi_ai_button.setStyleSheet(
            self.MainWindowRef.get_roi_ai_button.original_stylesheet
        )  # set in DoInferenceAllImagesOnlineThreaded
        self.MainWindowRef.get_roi_ai_button.labelText.setText(
            self.MainWindowRef.get_roi_ai_button.original_text
        )  # set in DoInferenceAllImagesOnlineThreaded

    def DoInferenceAllImagesOnlineThreaded(
        self, ignore_high_load: bool = False, provided_classes=None
    ):
        """
        This function is responsible for doing inference on all images for all conditions and groups. Image uploading and
        result collection is handled by the worker thread.
        """
        from celer_sight_ai import config

        if self.is_inference_running:
            config.global_signals.errorSignal.emit(
                "Cannot run two inference sessions at the same time."
            )
            return
        self.MainWindowRef.get_roi_ai_button.original_text = (
            self.MainWindowRef.get_roi_ai_button.labelText.text()
        )
        self.MainWindowRef.get_roi_ai_button.original_stylesheet = (
            self.MainWindowRef.get_roi_ai_button.styleSheet()
        )

        # set get_roi_button to "cancel" with color red
        self.MainWindowRef.get_roi_ai_button.setText("Cancel")
        self.MainWindowRef.get_roi_ai_button.setStyleSheet(
            """QPushButton{background-color: rgb(100,0,0);
                            color: rgb(185,50,50);
            }
            QPushButton:hover{background-color: rgb(200,0,0);
                        color: rgb(255,100,100);
            }
            """
        )
        # remove all signals from the button
        self.MainWindowRef.get_roi_ai_button.disconnect()
        # connect the button to the cancel function
        self.MainWindowRef.get_roi_ai_button.clicked.connect(
            lambda: self.cancel_inference()
        )

        config.global_signals.loading_dialog_signal_update_progress_percent.connect(
            self.updateQueuePosLoadingAnim
        )
        self.AllCurrentInferenceImages = 0
        self.EstimatedTimeInference = 0  # estimated time in seconds
        for Condition, value in self.MainWindowRef.DH.BLobj.groups[
            "default"
        ].conds.items():
            self.AllCurrentInferenceImages += len(
                self.MainWindowRef.DH.BLobj.groups["default"].conds[Condition]
            )

        # lock ui elements to prevent corruption, unlock after inference ends
        config.global_signals.lock_ui_signal.emit(
            ["condition_buttons", "initialize_analysis_button"]
        )

        logger.debug("Before do_inference_all_images_online_threaded_func")

        self.do_inference_all_images_online_threaded_func(
            ignore_high_load=ignore_high_load, provided_classes=provided_classes
        )

    def updateQueuePosLoadingAnim(self, Position):
        """
        Updates current position in the queue and the estimated time remaining
        """
        # TODO: this is the functiont that updates the (now hidden) dialog, adjust to update something else
        return

    def onJobComplete(self, text=None):
        # TODO:  This function closes the dialog, adjust to update something else
        # try:
        #     self.LoadingInferenceDialog.close()
        # except:
        #     pass
        from celer_sight_ai.gui.designer_widgets_py_files.JobCompleteConfirmationDialog import (
            Ui_JobComplete as JobCompleteForm_UI,
        )

        if text == "Inference complete.":
            config.global_signals.successSignal.emit("AI ROI generation complete.")

    def message_from_server_during_inference(self, text=None):
        self.LoadingInferenceForm.ImportingLabel.setText(text)
        # self.LoadingInferenceForm.show()

    def update_progress_dialog(self, Percent):
        self.EndInferenceTime = time.time()
        self.LoadingInferenceForm.RemainingTimeLabel.setText("")
        if Percent > 25:
            if self.StartInferenceTime != 0:
                timeDiff = self.EndInferenceTime - self.StartInferenceTime
                self.prevInferenceTimes.append(timeDiff)

                self.LoadingInferenceForm.RemainingTimeLabel.setText(
                    "Job complete in :  "
                    + self.display_time(
                        (sum(self.prevInferenceTimes) / len(self.prevInferenceTimes))
                        * ((100 - Percent) / 100)
                        * (self.AllCurrentInferenceImages)
                    )
                )
                if len(self.prevInferenceTimes) > 3:
                    self.prevInferenceTimes.pop(0)
        else:
            self.prevInferenceTimes = []

        # update the progress bar
        self.loadingInferenceForm.progressBar.setValue(int(Percent))
        self.startInferenceTime = time.time()

    def _get_classes_optimal_annotation_range(self):
        """
        Retrieves the optimal annotation size range for each non-particle class in the project.
        The optimal annotation size (compared to the tile size) is then use the the actuall annotation size to compute the tile size
        for inference.

        This method:
        1. Gets all non-particle classes from the custom class list widget
        2. Queries the server for each class's optimal annotation range
        3. Returns a dictionary mapping class UUIDs to their optimal ranges

        Returns:
            dict: A dictionary where:
                - key: class UUID (str)
                - value: optimal annotation range data from server (dict)
                  typically containing min/max size ratios for annotations

        Example return value:
            {
                "class_uuid_1": {"optimal_annotation_range": [0.1, 0.3], "img_size": [640, 640]},
                "class_uuid_2": {"optimal_annotation_range": [0.2, 0.4], "img_size": [1024, 1024]}
            }
        """
        result = {}
        all_classes_uuids = [
            (i.text(), i.unique_id)
            for i in self.MainWindowRef.custom_class_list_widget.classes.values()
            if not i.is_particle
        ]
        for class_name, class_uuid in all_classes_uuids:
            # get best annotation range for this class directly from the trained model
            optimal_annotation_range = config.client.get_optimal_annotation_range(
                class_uuid
            )
            # if the optimal annotation range is not found, assign default values
            if not optimal_annotation_range.get("optimal_annotation_range"):
                # assign default value
                optimal_annotation_range["optimal_annotation_range"] = [
                    config.MAGIC_BOX_2_MIN_ANNOTATION_PERCENT_SIZE,
                    config.MAGIC_BOX_2_MAX_ANNOTATION_PERCENT_SIZE,
                ]
            # if the server fetch fails we also need to assign a default
            # image size
            if not optimal_annotation_range.get("img_size"):
                optimal_annotation_range["img_size"] = [
                    config.MAGIC_BOX_2_RESOLUTION,
                    config.MAGIC_BOX_2_RESOLUTION,
                ]
            result[class_uuid] = optimal_annotation_range
        return result

    def _get_class_mask_sizes(self, mode="bbox"):
        """
        Gathers up to 4 mask bboxes for each class and computes the average size of the mask
        Args:
            mode (str): "bbox" or "distance", bbox uses the average width / height, where distance computes the largest width within the mask
        Returns:
            dict: class uuid : average bbox size per class
        """
        class_mask_sizes = {}
        all_class_items = []
        all_classes_uuids = [
            i.unique_id
            for i in self.MainWindowRef.custom_class_list_widget.classes.values()
            if not i.is_particle
        ]
        all_masks = [i for i in self.MainWindowRef.DH.BLobj.get_all_mask_objects()]
        # get all available classes
        for class_uuid in all_classes_uuids:
            class_mask_sizes[class_uuid] = []
            for mask in all_masks:
                if (
                    class_mask_sizes.get(class_uuid)
                    and len(class_mask_sizes.get(class_uuid)) > 4
                ):
                    break  # just use 4 masks per class
                if mask.class_id == class_uuid:
                    if mode == "bbox":
                        # compute the size of the mask
                        mask_bbox = mask.get_bounding_box()
                        if isinstance(mask_bbox, type(None)):
                            continue
                        average_size = (mask_bbox[2] + mask_bbox[3]) / 2
                    elif mode == "distance":
                        # draw the polygon into a nupy
                        average_size = calculate_polygon_width(
                            mask.get_array()[0].astype(np.uint32)
                        )
                    class_mask_sizes[class_uuid].append(int(average_size))

        # for every class average out the mask sizes
        for class_uuid in class_mask_sizes:
            # case where the user has not annotated any masks
            if len(class_mask_sizes[class_uuid]) == 0:
                # do every 1024 * 1.5 pixels as default
                class_mask_sizes[class_uuid] = None
            else:
                class_mask_sizes[class_uuid] = sum(class_mask_sizes[class_uuid]) / len(
                    class_mask_sizes[class_uuid]
                )
        return class_mask_sizes

    def calculate_tile_size(self, annotation_size: int, percentage: int) -> int:
        """Calculate the tile size based on the annotation size and a given percentage."""
        return annotation_size * (percentage / 100)

    # def check_derived_tile_overlap(min_ranges: list,  max_ranges: list) -> bool:
    #     """Check if two tiles overlap."""
    #     x1, y1, w1, h1 = tile1
    #     x2, y2, w2, h2 = tile2
    #     return not (x1 + w1 <= x2 or x2 + w2 <= x1 or y1 + h1 <= y2 or y2 + h2 <= y1)

    def merge_tiles(
        self, tile1: Tuple[int, int, int, int], tile2: Tuple[int, int, int, int]
    ) -> Tuple[int, int, int, int]:
        """Merge two overlapping tiles into one."""
        x1, y1, w1, h1 = tile1
        x2, y2, w2, h2 = tile2
        x_min = min(x1, x2)
        y_min = min(y1, y2)
        x_max = max(x1 + w1, x2 + w2)
        y_max = max(y1 + h1, y2 + h2)
        return (x_min, y_min, x_max - x_min, y_max - y_min)

    def generate_tiles(
        self, annotations: List[Tuple[int, int, int, int]]
    ) -> List[Tuple[int, int, int, int]]:
        """Generate tiles based on the annotations."""
        tiles = []
        for x, y, width, height in annotations:
            percentage = random.randint(
                3, 25
            )  # Choose a random percentage between 3% and 25%
            tile_size = self.calculate_tile_size(
                (width + height) // 2, percentage
            )  # Calculate the tile size
            tile = (
                x - (tile_size - width) // 2,
                y - (tile_size - height) // 2,
                tile_size,
                tile_size,
            )

            # Check for overlap with existing tiles and merge if necessary
            for i, existing_tile in enumerate(tiles):
                if self.check_overlap(tile, existing_tile):
                    tile = self.merge_tiles(tile, existing_tile)
                    tiles[i] = tile  # Update the existing tile with the merged one
                    break
            else:
                tiles.append(tile)  # Add the new tile if no overlap occurred
        return tiles

    def calculate_dynamic_leeway(self, optimal_ratio, min_leeway=0.2, max_leeway=0.4):
        """
        Calculates flexible bounds around an optimal annotation-to-image size ratio to determine
        acceptable annotation sizes during inference.

        For example, if an annotation typically takes up 30% of an image tile, this method helps
        determine what range of sizes (e.g., 20-40%) should be considered valid during detection.

        Args:
            optimal_ratio (float or list): The target ratio of annotation size to image size.
                                         Can be a single float or a [min, max] list/tuple.
            min_leeway (float): Minimum flexibility factor (default: 0.2 or 20%)
            max_leeway (float): Maximum flexibility factor (default: 0.4 or 40%)

        Returns:
            tuple: (lower_bound, upper_bound) representing the acceptable size range.
                  Values are clamped between 1% and 80% of image size.

        Example:
            If optimal_ratio = 0.3 (30% of image):
            - For small ratios: provides wider relative bounds to account for detection variance
            - For large ratios: provides tighter relative bounds for more precise detection
        """
        import math

        # If optimal_ratio is a range, use its average
        if isinstance(optimal_ratio, (list, tuple)):
            optimal_ratio = (optimal_ratio[0] + optimal_ratio[1]) / 2

        # Calculate how much flexibility to allow, using exponential decay
        # - Small ratios get more relative flexibility
        # - Large ratios get less relative flexibility
        leeway_factor = min_leeway + (max_leeway - min_leeway) * (
            1 - math.exp(-5 * optimal_ratio)
        )

        # Calculate the acceptable range around the optimal ratio
        lower_bound = optimal_ratio * (1 - leeway_factor)
        upper_bound = optimal_ratio * (1 + leeway_factor)

        # Clamp bounds to reasonable limits (1% to 80% of image size)
        return (max(0.01, lower_bound), min(0.80, upper_bound))

    @config.threaded
    def do_inference_all_images_online_threaded_func(
        self,
        provided_classes=None,  #  uuid list
        provided_treatments=None,  #  uuid list
        provided_images=None,  #  uuid list
        ignore_high_load=False,
    ) -> None:
        """
        In this function we multithread send, inference and receive from the server
        provided_images : list of uuids
        """
        from celer_sight_ai.core.threader import workerInference
        from functools import partial
        from celer_sight_ai.io.data_handler import (
            get_tile_range_from_annotation_size,
            find_minimum_groups,
            group_ranges_to_tile_size,
        )
        import copy

        self.is_inference_completed = False
        try:
            # compute the ideal tile size for every class:
            #    - iterate over all classes, and get the average size of the masks
            #    - tile should be around 10-20x times larger than the size of the mask

            class_mask_sizes = self._get_class_mask_sizes(mode="distance")
            # class name : optimal range {min: , max: }

            if provided_classes:
                # only use the provided classes
                class_mask_sizes = {
                    k: v for k, v in class_mask_sizes.items() if k in provided_classes
                }

            # gets the optimal annotation range to the image sent per class
            # Per class we have {"optimal_annotation_range" : [min, max], image_size : [640 x 640]}

            optimal_annotation_ranges_and_image_size = (
                self._get_classes_optimal_annotation_range()
            )

            class_mask_sizes_in_tile = {}
            for class_uuid in class_mask_sizes:
                # calculate the range of annotation sizes that are acceptable for inference
                min_percentage, max_percentage = self.calculate_dynamic_leeway(
                    optimal_annotation_ranges_and_image_size.get(class_uuid, {}).get(
                        "optimal_annotation_range", (0.5, 0.15)
                    )
                )
                average_annotation_size = class_mask_sizes.get(class_uuid, None)
                if not average_annotation_size:
                    # Use the tile size from the api and the optimal annotation range
                    img_size = optimal_annotation_ranges_and_image_size[class_uuid].get(
                        "img_size"
                    )  # (w,h)
                    average_annotation_size = (
                        ((img_size[0] + img_size[1]) / 2)
                        * ((min_percentage + max_percentage))
                        / 2
                    )
                class_mask_sizes_in_tile[class_uuid] = (
                    get_tile_range_from_annotation_size(
                        average_annotation_size, min_percentage, max_percentage
                    )
                )
            self._stop_inference_retrieval = False  # stops retrival of inference results when the user cancels or when the all inferences are completed

            # find minimum amount of groups of classes for inference
            min_groups = find_minimum_groups(copy.deepcopy(class_mask_sizes_in_tile))
            # for any class that has no annotations, get the tile size from the api

            min_tile_groups = group_ranges_to_tile_size(
                min_groups,
                class_mask_sizes_in_tile,
                optimal_annotation_ranges_and_image_size,
            )

            config.stop_inference = (
                False  # reset, goes to True when use cancels inference
            )
            config.inference_buffer = 0
            skip_inferece_due_to_error = False  # catch errors and skip inference.
            self.is_inference_running = True
            # start retrival of inference results

            client = config.client
            logging.info(
                f"Total images for inference {self.MainWindowRef.DH.BLobj.getTotalImages()}"
            )

        except Exception as e:
            logger.debug(f"Error during initialization phase of inference {e}")
            config.global_signals.errorSignal.emit("Failed to initialize AI process.")
            skip_inferece_due_to_error = True
            config.global_signals.unlock_ui_signal.emit()
            self.revert_get_ai_roi_button_back_to_normal()

        # prep all classes with their superclasses and settings for inference
        if not skip_inferece_due_to_error:
            all_class_items = []
            for class_widget_key in self.MainWindowRef.custom_class_list_widget.classes:
                # if class is particle / trehsold skip
                if self.MainWindowRef.custom_class_list_widget.classes[
                    class_widget_key
                ].is_particle:
                    continue
                if provided_classes:
                    # only inlcude class if uuid is inthe provided classes uuid list
                    if class_widget_key in provided_classes:
                        all_class_items.append(
                            self.MainWindowRef.custom_class_list_widget.classes[
                                class_widget_key
                            ].get_class_config()
                        )
                else:
                    all_class_items.append(
                        self.MainWindowRef.custom_class_list_widget.classes[
                            class_widget_key
                        ].get_class_config()
                    )
            try:
                config.STARTED_RETRIEVAL = False

                all_image_objects = [
                    self.MainWindowRef.DH.BLobj.get_image_object_by_uuid(i.unique_id)
                    for i in self.MainWindowRef.DH.BLobj.get_all_image_objects()
                ]

                total_tiles_as_lists = [
                    i.get_all_possible_tiles(min_tile_groups) for i in all_image_objects
                ]
                total_tiles = 0
                for image_groups in total_tiles_as_lists:
                    for k in image_groups:
                        total_tiles += len(image_groups[k])

                logger.info(f"Total tiles for inference: {total_tiles}")

                # request intialization of inference from the server
                response = client.send_initialize_inference(
                    config.supercategory, total_tiles
                )
                logger.info(f"Initialization response: {response}")
                missing_model_categories = response.get("missing_model_categories", [])
                if len(missing_model_categories) > 0:
                    config.global_signals.noModelCategoriesSignal.emit(
                        "Some categories dont have a model yet, skipping them."
                    )
                if response.get("status") == "high_load" and not ignore_high_load:
                    config.global_signals.warningSignal.emit(
                        "The server is currently experiencing high load. Processing will be slower than usual."
                    )
                    # Ask user if they want to continue
                    config.global_signals.actionDialogSignal.emit(
                        "The server is busy, which may result in slower processing times.\nDo you want to continue anyway?",
                        {
                            "Yes": partial(
                                self.DoInferenceAllImagesOnlineThreaded,
                                ignore_high_load=True,
                            ),
                            "No": lambda: None,
                        },
                    )
                    return  # the response will be handled in the actionDialogSignal
                if response.get("status") == "error":
                    config.global_signals.errorSignal.emit(
                        f"Error initializing inference: {response.get('message', 'Unknown error')}"
                    )
                    return

                for io in all_image_objects:
                    # set to inference
                    io._during_inference = True

                    if config.stop_inference:
                        return (None, "")
                    while (
                        config.inference_buffer
                        > config.user_cfg["MAX_CONCURENT_INFERENCE_REQUESTS"]
                    ):
                        time.sleep(0.005)
                        if config.stop_inference:
                            return (None, "")

                    if not config.user_cfg["USER_WORKERS"]:
                        # need to manually start it as threaded in this
                        # case otherwise it will become deadlocked
                        import threading

                        threading.Thread(
                            target=self.start_inference_retrival,
                            kwargs={
                                "min_wait_time": 10,
                            },
                        ).start()

                    z = workerInference(
                        target_function=client.send_image_for_inference,
                        args=(
                            io,
                            config.supercategory,
                            min_tile_groups,
                        ),
                    )
                    z.start()
                    # wait for the thread to finish
                    z.join()
                    config.inference_threads.append(z)

                    if config.inference_buffer > 0 and not config.STARTED_RETRIEVAL:
                        if config.user_cfg["USER_WORKERS"]:
                            self.start_inference_retrival()
                        config.STARTED_RETRIEVAL = True

                is_stopped = False
                try:
                    if config.inference_threads:
                        if config.inference_threads[-1].stop_signal.is_set():
                            pass
                except:
                    is_stopped = False
                if is_stopped or config.stop_inference:
                    config.global_signals.warningSignal.emit(
                        "AI ROI generation interrupted."
                    )

            except Exception as e:
                self.is_inference_running = False
                self.revert_get_ai_roi_button_back_to_normal()
                config.global_signals.unlock_ui_signal.emit()
                config.global_signals.warningSignal.emit(
                    "ROI's were not generated for some of the images."
                )
                logger.error(e)

        self.is_inference_completed = True

    def complete_inference_sessions(self, success=True):
        """
        Stop all inference sessions
        """
        # send signal to stop checking for inference
        self.is_inference_running = False
        if success:
            config.global_signals.successSignal.emit("AI ROI generation complete.")
        config.global_signals.unlock_ui_signal.emit()
        config.global_signals.endAllInferenceLoadingSignals.emit()
        for img_obj in self.MainWindowRef.DH.BLobj.get_all_image_objects():
            img_obj._during_inference = False
        self.revert_get_ai_roi_button_back_to_normal()
        config.global_signals.remove_all_inference_tile_graphics_items_signal.emit()
        return

    def SkipMasksOnEdges(self, allPoints, image, SkipList):
        maskToDelete = []
        # for every ROI in the image
        for i in range(len(allPoints)):
            logger.info("points are ", allPoints)
            if not all(
                p[1] > SkipList[1] and p[1] < image.shape[1] - SkipList[1]
                for p in allPoints[i]
            ):
                maskToDelete.append(i)
                continue
            if not all(
                p[0] > SkipList[0] and p[0] < image.shape[0] - SkipList[0]
                for p in allPoints[i]
            ):
                maskToDelete.append(i)
                continue
        maskToDelete.sort()
        for item in reversed(maskToDelete):
            del allPoints[item]
        # return points that are not near the edges
        return allPoints

    def deleteMaskaFromImage(self, object_dict={}):
        """This function deletes the mask from the image, this is done through the history stackl so that the command is undoable."""
        logger.info("deleteMaskFromImage RUNS")
        mask_unique_id = object_dict.get("mask_uuid")

        # set image as modified
        mask_object = self.MainWindowRef.DH.BLobj.get_mask_object_by_uuid(
            mask_unique_id
        )
        if not mask_object:
            return
        image_object = self.MainWindowRef.DH.BLobj.get_image_object_by_uuid(
            mask_object.image_uuid
        )
        image_object.setUserModifiedAnnotation(True)

        removeCommand = DeleteMaskCommand(mask_unique_id, self.MainWindowRef)
        self.MainWindowRef.undoStack.push(removeCommand)

    def deleteTrackFromMainWindow(self, object_dict={}):
        "Delete track annotation from current treatment"
        image_uuid = object_dict.get("image_uuid")
        treatment_uuid = object_dict.get("treatment_uuid")
        track_unique_id = object_dict.get("track_unique_id")
        class_id = object_dict.get("class_id")
        # iterate over all masks, if the track id is a match, delete that mask
        # for all treatments
        # for all images in this treatment
        treatment_object = (
            self.MainWindowRef.DH.BLobj.get_treatment_object_from_image_uuid(
                treatment_uuid
            )
        )
        for img_obj in treatment_object.images:
            # for all masks in the image
            for mask in img_obj.masks:
                if mask._annotation_track_id == track_unique_id:
                    removeCommand = DeleteMaskCommand(
                        mask.unique_id,
                        self.MainWindowRef,
                        img_obj.unique_id,
                        treatment_uuid,
                        class_id,
                    )
                    self.MainWindowRef.undoStack.push(removeCommand)

    def delete_hole_from_mask(self, MasterList=[]):
        """This function deletes the mask from the image, this is done through the history stackl so that the command is undoable."""
        logger.info("deleteMaskFromImage RUNS")
        array_index = MasterList[0]
        hole_graphics_item = MasterList[1]
        imID = MasterList[2]
        Condition = MasterList[3]
        mask_uuid = MasterList[4]
        class_id = MasterList[5]
        removeCommand = DeleteHoleCommand(
            array_index,
            hole_graphics_item,
            mask_uuid,
            self.MainWindowRef,
            imID,
            Condition,
            class_id,
        )
        self.MainWindowRef.undoStack.push(removeCommand)
        # set image as modified
        self.MainWindowRef.DH.BLobj.groups["default"].conds[Condition].images[
            imID
        ].setUserModifiedAnnotation(True)

    def adjust_polygon_to_source_tile(
        self, polygon, source_tile, processed_tile_dimention
    ):
        """
        Adjusts the polygon to the source tile.
        polygon is a list of polygongs, the first is the outer polygon and the rest are holes.

        """
        if not source_tile or not processed_tile_dimention:
            # dont process polygon
            return polygon
        offset_x = source_tile[0]
        offset_y = source_tile[1]
        scale_x = processed_tile_dimention[0] / source_tile[2]
        scale_y = processed_tile_dimention[1] / source_tile[3]
        for i in range(len(polygon)):
            arr = polygon[i]
            if isinstance(arr, list):
                arr = np.array(arr)
            if not len(arr.shape) == 2 or arr.shape[0] < 3:
                # skip invalid polygopn
                continue
            polygon[i] = [
                [
                    (p[0] / scale_x) + offset_x,
                    (p[1] / scale_y) + offset_y,
                ]
                for p in arr
            ]
        return polygon

    def create_annotations_objects(self, all_objects=[]):
        """
        This method creates multiple annotation objecst at once
        """
        for obj in all_objects:
            self.create_annotation_object(obj)

    def order_and_validate_polygons(
        self, polygons: List[np.ndarray]
    ) -> List[np.ndarray]:
        """
        Orders polygons by area (largest to smallest) and removes invalid polygons.

        Args:
            polygons (List[np.ndarray]): List of polygon vertex arrays


        Returns:
            List[np.ndarray]: Ordered list of valid polygons
        """
        valid_polygons = []

        # Convert polygons to Shapely objects and store with their areas
        for poly in polygons:
            poly = np.array(poly)
            try:
                if not len(poly.shape) == 2 or poly.shape[0] < 4:
                    continue
                shapely_poly = Polygon(poly)
                if shapely_poly.is_valid:
                    # Try to fix invalid polygons
                    if not shapely_poly.is_valid:
                        shapely_poly = shapely_poly.buffer(0)
                        if not shapely_poly.is_valid:
                            continue

                    valid_polygons.append((poly, shapely_poly.area))
            except Exception as e:
                logger.debug(f"Invalid polygon skipped: {e}")
                continue

        # # Sort by area (largest to smallest)
        # valid_polygons.sort(key=lambda x: x[1], reverse=False)

        # Return just the polygon arrays in sorted order
        return [poly[0] for poly in valid_polygons]

    def create_annotation_object(self, MasterList=[]):
        """
        This function puts the Qpoints on their place along with the widgets
        Creates the mask object that holds properties of the mask, runs when the mask is created.
        """

        Condition = None  # if treatment_uuid is not provided
        treatment_uuid = None
        mask_uuid = None
        group = None
        polygon_object = None
        imID = None
        class_id = None
        mask_type = None
        visibility = None
        included_in_analysis = None
        allow_sending_remote = True
        score = float(1)
        is_suggested = False
        source_tile = None
        processed_tile_dimention = None

        treatment_uuid = MasterList.get("treatment_uuid")
        group_uuid = MasterList.get("group_uuid")
        polygon_object = MasterList.get("array")
        image_uuid = MasterList.get("image_uuid")
        class_id = MasterList.get("class_id")
        mask_type = MasterList.get("mask_type")
        visibility = MasterList.get("visibility")
        mask_uuid = MasterList.get("mask_uuid")
        included_in_analysis = MasterList.get("includedInAnalysis")
        allow_sending_remote = MasterList.get("allow_sending_remote", True)
        is_suggested = MasterList.get("is_suggested")
        score = MasterList.get("score", float(1))
        source_tile = MasterList.get("source_tile")
        processed_tile_dimention = MasterList.get("processed_tile_dimention")
        check_overlap = MasterList.get("check_overlap", True)
        adjust_polygon_to_tile = MasterList.get("adjust_polygon_to_tile", True)
        remove_polygons_close_to_edge = MasterList.get(
            "remove_polygons_close_to_edge", False
        )
        start = time.time()
        if not treatment_uuid:
            # obtain from image object if provided
            if image_uuid:
                image_object = self.MainWindowRef.DH.BLobj.get_image_object_by_uuid(
                    image_uuid
                )
                if not image_object:
                    return
                treatment_uuid = image_object.treatment_uuid
            else:
                # the the treatment and group from the image object
                treatment_object = (
                    self.MainWindowRef.DH.BLobj.get_treatment_object_from_image_uuid(
                        imID
                    )
                )
                if not treatment_object:
                    return
                treatment_uuid = treatment_object.unique_id

        # if the class is not in the list of classes, add it
        class_items = [
            [
                self.MainWindowRef.custom_class_list_widget.getItemWidget(i).text(),
                self.MainWindowRef.custom_class_list_widget.getItemWidget(i).unique_id,
            ]
            for i in range(self.MainWindowRef.custom_class_list_widget.count())
            if self.MainWindowRef.custom_class_list_widget.getItemWidget(i).unique_id
            == class_id
        ]
        if len(class_items) == 0 and not class_id:
            return
        # else, add the class id if possible
        elif not class_items or class_items[0][0] not in [
            self.MainWindowRef.custom_class_list_widget.getItemWidget(i).text()
            for i in range(self.MainWindowRef.custom_class_list_widget.count())
        ]:
            # add class from saved classes to the ui
            class_config = (
                self.MainWindowRef.custom_class_list_widget.get_config_by_class_uuid(
                    class_id
                )
            )
            if not class_config:
                config.global_signals.notificationSignal.emit("Class of ROI not found")
                return
            main_class = class_config["classes"][0]
            self.MainWindowRef.custom_class_list_widget.addClass(
                class_name=main_class["class_name"],
                parent_class_uuid=main_class["parent_class"],
                class_uuid=main_class["uuid"],
            )
            class_items = [[main_class["class_name"], main_class["uuid"]]]
            config.global_signals.notificationSignal.emit(
                "Class added: " + main_class["class_name"]
            )
        class_name = class_items[0][0]  # text
        class_id = class_items[0][1]  # uuid

        # if image id is str, then its its a uuid, convert it to int # TODO: this is a hack, fix it
        image_object = self.MainWindowRef.DH.BLobj.get_image_object_by_uuid(image_uuid)
        if not image_object:
            return
        # case for polygon instance mask
        if mask_type == "polygon":
            # Preprocess polygon object once
            polygon_object = [np.array(i).squeeze() for i in polygon_object]
            if not polygon_object:
                return

            try:
                if adjust_polygon_to_tile:
                    logger.info(
                        f"Adjusting polygon to tile {source_tile} {processed_tile_dimention}"
                    )
                    polygon_object = self.adjust_polygon_to_source_tile(
                        polygon_object,
                        source_tile=source_tile,
                        processed_tile_dimention=processed_tile_dimention,
                    )

                # config.dbg_polygon(
                #     polygon_object,
                #     [image_object.SizeX, image_object.SizeY],
                # )

                # remove polygons close to the edge of the image
                if remove_polygons_close_to_edge:
                    if self.is_polygon_close_to_edge(
                        polygon_object,
                        [
                            image_object.SizeX,
                            image_object.SizeY,
                        ],  # in image_object array [ [2N] , ...]
                    ):
                        logger.info("Polygon close to edge, skipping")
                        return

                logger.debug(f"Time taken to process polygon p1: {time.time() - start}")

                # Validate and order polygons once
                polygon_object = self.order_and_validate_polygons(polygon_object)
                if len(polygon_object) == 0:
                    return

                # Create and validate original polygon once
                m_poly_original = Polygon(np.array(polygon_object[0]).squeeze())
                if not m_poly_original.is_valid:
                    m_poly_original = m_poly_original.buffer(0)
                    if not m_poly_original.is_valid:
                        return

                if check_overlap:
                    m_poly_original_area = m_poly_original.area
                    overlap_amount = 0.50

                    # Get all relevant masks once (only polygon masks of same class)
                    relevant_masks = [
                        m
                        for m in image_object.masks
                        if m.mask_type == "polygon" and m.class_id == class_id
                    ]

                    # Use prepared geometry for faster intersection checks
                    from shapely.prepared import prep

                    prepared_original = prep(m_poly_original)

                    for m in relevant_masks:
                        arr = m.get_array()[0]
                        if isinstance(arr, np.ndarray) and len(arr.shape) > 2:
                            arr = arr.squeeze()

                        try:
                            m_poly = Polygon(arr)
                            if not m_poly.is_valid:
                                m_poly = m_poly.buffer(0)
                                if not m_poly.is_valid:
                                    continue

                            # Use prepared geometry for faster checks
                            if prepared_original.intersects(m_poly):
                                # Only calculate intersection area if basic intersection exists
                                intersection_area = m_poly_original.intersection(
                                    m_poly
                                ).area
                                m_poly_area = m_poly.area

                                if intersection_area > (
                                    m_poly_area * overlap_amount
                                ) or intersection_area > (
                                    m_poly_original_area * overlap_amount
                                ):

                                    if m.is_suggested:
                                        if m.score >= score:
                                            # logger.info(
                                            #     "Polygons with the same class overlap and lower score, skipping"
                                            # )
                                            return
                                        else:
                                            image_object.del_by_uuid(m.unique_id)
                                    else:
                                        # logger.debug(
                                        #     "Polygons with the same class overlap, skipping"
                                        # )
                                        return

                        except Exception as e:
                            logger.error(f"Error processing mask: {e}")
                            continue
                # convert to numpy if its a list
                for p in range(len(polygon_object)):
                    if isinstance(polygon_object[p], list):
                        polygon_object[p] = np.array(polygon_object[p])
                logger.debug(f"Time taken to process polygon: {time.time() - start}")
                start = time.time()
                add = AddPolygonCommand(
                    polygon_object,
                    self.MainWindowRef,
                    treatment_uuid=treatment_uuid,
                    image_uuid=image_uuid,
                    class_id=class_id,
                    mask_type=mask_type,
                    visibility=visibility,
                    is_included_in_analysis=included_in_analysis,
                    is_suggested=is_suggested,
                    score=score,
                    mask_uuid=mask_uuid,
                )
                self.MainWindowRef.undoStack.push(add)
                logger.debug(f"Time taken to add polygon: {time.time() - start}")
            except Exception as e:
                logger.error(f"Error in polygon processing: {e}")
        elif mask_type == "bitmap":
            add = AddBitMapCommand(
                polygon_object, self.MainWindowRef, image_uuid, class_id
            )
            self.MainWindowRef.undoStack.push(add)
        # if image is remote, send annotations to celer sight api as a new annotation
        if (
            (image_object.is_remote()) and allow_sending_remote and not is_suggested
        ):  # on suggestion, masks need to be validaded first
            data = {
                "annotation_uuid": add.mask_uuid,
                "supercategory": config.supercategory,
                "category": class_name,  # text
                "type": mask_type,
                "data": self.MainWindowRef.numpy_to_python(polygon_object),  # the array
                "image_width": None,  # fill in later
                "image_height": None,  # fill in later
                "image_uuid": image_object.unique_id,
                "audited": True,
                "state": None,
            }
            new_uuid = config.client.insert_remote_annotation(data)
            image_object.change_mask_uuid(
                add.mask_uuid,
                new_uuid,
            )  # make sure ids match

    def is_polygon_close_to_edge(self, polygon_object, image_shape):
        """If the polygon is close to the edge of the image, remove it"""

        # check only the outer polygon
        arr = np.array(polygon_object[0])
        most_left_point = np.min(arr.T)
        most_right_point = np.max(arr.T)
        most_top_point = np.min(arr.T)
        most_bottom_point = np.max(arr.T)
        boundry_x = image_shape[1] * 0.005
        boundry_y = image_shape[0] * 0.005
        if (
            most_left_point <= boundry_x
            or most_right_point >= image_shape[1] - boundry_x
            or most_top_point <= boundry_y
            or most_bottom_point >= image_shape[0] - boundry_y
        ):
            return True
        return False

    def DoInferenceCurrentImageOnline(self, Image):
        """_summary_

        Args:
            Image (np.array[3,x,x]): image to be inferenced through BioMarker API
        """
        import skimage

        client = config.client
        if self.MainWindowRef.pg1_settings_ContrastAffectsNN_checkbox.isChecked():
            Image = self.MainWindowRef.handle_adjustment_to_image(Image)

        Readlist = client.send_img_for_inference(Image)
        logger.info(Readlist)

        for mask in Readlist:
            logger.info("adding mask")

            config.global_signals.create_annotation_object_signal.emit(
                {
                    "treatment_uuid": self.MainWindowRef.DH.BLobj.get_current_condition_uuid(),  # TODO: Change to uuid in the future
                    "group": self.MainWindowRef.DH.BLobj.get_current_group_uuid(),
                    "array": [mask],
                    "image_uuid": self.MainWindowRef.DH.BLobj.get_current_image_uuid(),
                    "class_id": self.MainWindowRef.custom_class_list_widget.currentItemWidget().text(),
                    "mask_type": "polygon",
                }
            )
        AllMasksPerImage = []
        for maskPOL in Readlist:
            mask = skimage.draw.polygon2mask((Image.shape[0], Image.shape[1]), maskPOL)
            AllMasksPerImage.append(
                get_largerst_area(mask.astype(np.uint8)).astype(bool).copy()
            )
        self.MainWindowRef.load_main_scene(self.MainWindowRef.current_imagenumber)
        return

    def correct_polygon(self, polygon):
        if not polygon.is_valid:
            corrected_polygon = polygon.buffer(0)
            if not corrected_polygon.is_valid:
                # If the polygon cannot be corrected, return None
                return None
            return corrected_polygon
        return polygon

    def get_iou(self, polygon1, polygon2):
        from shapely.geometry import Polygon

        # Convert lists to Polygon objects
        # ignore holes for now.
        polygon1 = self.correct_polygon(Polygon(polygon1[0]))
        polygon2 = self.correct_polygon(Polygon(polygon2[0]))

        # Calculate intersection and union
        intersection = polygon1.intersection(polygon2)

        # Check if there is no intersection
        if intersection.is_empty:
            return 0

        union_area = polygon1.area + polygon2.area - intersection.area

        # Calculate IoU
        iou = intersection.area / union_area

        return iou

    def track_all_masks_by_treatment(self, file_location=None):
        """
        For each treatment create annotation track ids
        to track annoations across images
        on the first frame (which is the first image for now on every treatment)
        create annotation group ids for every annotation

        Does not work for non polygon annotations for now
        """
        import uuid

        # collect all nums in a dict to add to config to be accesible from everywhere
        all_nums = {}
        num_tally = 0
        iou_threshold = 0.2
        # for every treatment
        for treatment_object in self.MainWindowRef.DH.BLobj.groups["default"].conds:
            # for every image in the treatment
            for i, image in enumerate(
                self.MainWindowRef.DH.BLobj.groups["default"]
                .conds[treatment_object]
                .images
            ):
                # for every mask in the image
                for mask in image.masks:
                    # if the mask is not a polygon, skip
                    if not mask.mask_type == "polygon":
                        continue
                    # if the mask is not in the track list, add it
                    if mask._annotation_track_id:
                        mask._annotation_track_id = None

                    # check if the previous image has a mask overlap with this mask
                    if i == 0:
                        # always crate new annotation tracking id
                        mask.set_annotation_track_id(str(config.get_unique_id()))
                        num_tally += 1
                        all_nums[mask._annotation_track_id] = num_tally
                        continue
                    if i > 0:
                        # get the previous image
                        previous_image = (
                            self.MainWindowRef.DH.BLobj.groups["default"]
                            .conds[treatment_object]
                            .images[i - 1]
                        )
                        # for every mask in the previous image
                        all_ious_tmp = {}  # store --> uuid: iou
                        for previous_mask in previous_image.masks:
                            # if the mask is not a polygon, skip
                            if not previous_mask.mask_type == "polygon":
                                continue
                            all_ious_tmp[previous_mask.unique_id] = self.get_iou(
                                mask.get_array(), previous_mask.get_array()
                            )
                            # num_tally += 1
                            # all_nums[mask._annotation_track_id] = num_tally

                        # get the mask iou uuid
                        if not all_ious_tmp:
                            continue
                        mask_iou_uuid = max(all_ious_tmp, key=all_ious_tmp.get)
                        # if its less than threshold, skip
                        if all_ious_tmp[mask_iou_uuid] < iou_threshold:
                            # case where no previous track record is found
                            # create a new track id
                            mask.set_annotation_track_id(str(config.get_unique_id()))
                            num_tally += 1
                            all_nums[mask._annotation_track_id] = num_tally
                            continue
                        # set the current mask to the previous mask track id
                        # get mask by uuid
                        mask_object = (
                            self.MainWindowRef.DH.BLobj.get_mask_object_by_uuid(
                                mask_iou_uuid
                            )
                        )
                        mask.set_annotation_track_id(mask_object._annotation_track_id)
                        # num_tally += 1
                        # all_nums[mask._annotation_track_id] = num_tally
                    # mask.set_annotation_track_id(str(config.get_unique_id()))

        config.track_annotation_map = all_nums

        self.MainWindowRef.AnalysisSettings.calculate_all_velocities_for_tracks(
            file_location
        )


def get_largerst_area(input_mask):
    import skimage
    from skimage import measure

    labels_mask = measure.label(input_mask)
    regions = measure.regionprops(labels_mask)
    regions.sort(key=lambda x: x.area, reverse=True)
    if len(regions) > 1:
        for rg in regions[1:]:
            labels_mask[rg.coords[:, 0], rg.coords[:, 1]] = 0
    labels_mask[labels_mask != 0] = 1
    return labels_mask


if __name__ == "__main__":
    pass
