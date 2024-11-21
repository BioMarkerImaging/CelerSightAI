import logging

logger = logging.getLogger(__name__)
import onnxruntime

logger.info("Imported Onnxruntime")

# from pyupdater.client import Client
from celer_sight_ai import config

from PyQt6 import QtGui, QtCore, QtWidgets
import os

logger.info("Imported config and Qt")
# import onnx

# import onnxruntime
import numpy as np
import cv2
from PIL import Image

logger.info("Before skimage import")
from skimage.transform import resize
import sys
import celer_sight_ai.configHandle as configHandle
from celer_sight_ai import config
from typing import Literal, Optional, Union, Tuple, Any
import numpy.typing as npt
import numpy as np

# sys.path.insert(0, '.')
# sys.path.insert(0, '..')
logger.info("Starting loading sdknn")

# from fileserver import RunFileServer
# from fileserver import WaitForFileServerToStart
# from fileserver import ShutDownFileServer
global NN_package
NN_package = None


def filter_contours_for_one_ROI(contours, hierarchies):
    """
    The function filters contours to find the contour with the maximum area and returns it along with
    any holes that are contained within it.

    Args:
    contours: A list of contours, where each contour is represented as a numpy array of shape (N, 1,
    2), where N is the number of points in the contour.
    hierarchies: The `hierarchies` parameter is a list of hierarchies for each contour in the
    `contours` list. Each hierarchy is represented as a list of four values: [next, previous, first
    child, parent]. These values represent the relationships between contours.

    Returns:
    two values: the contour with the maximum area (contours[max_area_index]) and a list of contours
    (holes) whose parent contour is the contour with the maximum area.
    """
    logger.debug("Filtering contours for 1 ROI")
    if not contours:
        return []
    # find the index of the contour with the maximum area
    max_area_index = np.argmax([cv2.contourArea(cnt) for cnt in contours])

    # filter out only the contours (holes) whose parent is the max_area_index contour
    holes = [
        contours[i]
        for i, hierarchy in enumerate(hierarchies[0])
        if hierarchy[3] == max_area_index
    ]
    out = []
    out.append(contours[max_area_index])
    out.extend(holes)
    return out


def mask_to_polygon(
    binary_mask,
    image_shape=None,
    tolerance=0.0008,
    offset_x=0,
    offset_y=0,
    resize_factor_x=1,
    resize_factor_y=1,
    min_amount_of_points=18,
):
    import skimage

    logger.debug("Converting mask to polygon")
    if binary_mask.dtype == bool:
        binary_mask = binary_mask.astype(np.uint8)
    contours, hier = cv2.findContours(
        binary_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE
    )
    shape_y, shape_x = image_shape[:2]
    tolerance = (shape_x + shape_y) * tolerance
    all_arrays = []

    contours = filter_contours_for_one_ROI(contours, hier)

    for c in range(len(contours)):
        # if len(contours[c]) < 20:
        #     continue

        pol = []
        it = 0
        mod_tolerance = tolerance
        while len(pol) < min_amount_of_points:
            if it > 0:
                mod_tolerance = tolerance / (it * 3)
            if it > 5:  # after 5 iterations just break
                # pol = contours[c]
                break
            if isinstance(contours[c], np.ndarray):
                cont = contours[c].squeeze()
            else:
                raise Exception("contours[c] is not np.ndarray")
            pol = skimage.measure.approximate_polygon(cont, tolerance=mod_tolerance)
            it += 1
        # offset arrays by offset_x and offset_y
        pol = np.array(pol)
        if (
            offset_y != 0
            or offset_x != 0
            or resize_factor_x != 1
            or resize_factor_y != 1
        ):
            pol = (pol[:, :] / np.array([resize_factor_x, resize_factor_y])) + np.array(
                [offset_x, offset_y]
            )
        all_arrays.append(pol)
        # all_arrays[-1] = all_arrays[-1][:, :]
    return all_arrays


def get_largest_area(input_mask, inverted=False):
    import skimage
    from skimage.measure import label

    labels = label(input_mask)
    # assert( labels.max() != 0 ) # assume at least 1 CC
    largestCC = labels == np.argmax(np.bincount(labels.flat)[1:]) + 1
    return largestCC


class SamPredictorONNX:
    mask_threshold: float = 0.0
    image_format: str = "RGB"
    img_size = config.MAGIC_BOX_2_RESOLUTION
    pixel_mean = np.array([123.675, 116.28, 103.53])[None, :, None, None]
    pixel_std = np.array([58.395, 57.12, 57.375])[None, :, None, None]

    def __init__(self, MainWindow: any, encoder_path: str, decoder_path: str) -> None:
        super().__init__()
        self.encoder = None
        self.decoder = None
        self.encoder_path = encoder_path
        self.decoder_path = decoder_path
        self.disable_tool()

        self.load_models()

        self.MainWindow = MainWindow

        # long term memory
        self.long_term_memory_features = []
        self.long_term_memory_points = []
        self.long_term_memory_image_features = []  # {"size" : (w+h) / 2,

        # Log running inferences, to remove when the inference completes, or is interupted
        self._running_inferences = []

        # wont recompute newmasks
        # mean_color , "points" , vector, tile_bbox, "image_uuid" , sign: "positive" / "negative" ,
        # mask_uuid}
        self.resize_xy = None
        self.infered_boundry_array = None  # array of boundingboxes where we
        self._initial_tile_box = None  # used for mask suggestions
        self._subject_bbox = None  # only needed to compute the overlap of the tiles
        self._latest_celer_sight_object = None
        self._last_used_current_class_uuid = None
        self._positive_roi_threshold = self.get_setting_value(
            config.settings, "roi_suggestor_positive_roi_threshold", 50
        )
        self._negative_roi_threshold = self.get_setting_value(
            config.settings, "roi_suggestor_negative_roi_threshold", 50
        )
        self._shape_similarity_threshold = self.get_setting_value(
            config.settings, "roi_suggestor_shape_similarity_threshold", 50
        )
        self._image_similarity_threshold = self.get_setting_value(
            config.settings, "roi_suggestor_image_similarity_threshold", 50
        )

        # constants
        self.MEMORY_MAX_SIZE = 1000
        self._is_locked = False  # if locked, wait until unlocked to compute

        self.current_image_uuid = None
        self.current_image_features = (
            None  # if image_uuid matches, donr recompute image_features
        )

        self.reset_feature_map()

        config.global_signals.annotation_generator_start_signal.connect(
            self.start_suggested_mask_generator
        )

    def load_models(self, force_provider=None):
        logger.debug(f"Loading models")
        # get filename including version from the full path
        root_dir_encoder = os.path.dirname(self.encoder_path)
        encoder_filename = os.path.basename(self.encoder_path)
        encoder_path_with_version = config.get_latest_file_version(
            root_dir_encoder, encoder_filename
        )
        if not encoder_path_with_version:
            return False

        root_dir_decoder = os.path.dirname(self.decoder_path)
        decoder_filename = os.path.basename(self.decoder_path)
        decoder_path_with_version = config.get_latest_file_version(
            root_dir_decoder, decoder_filename
        )
        if not decoder_path_with_version:
            return False

        try:
            encoder_path_with_version = os.path.join(
                root_dir_encoder, encoder_path_with_version
            )
            decoder_path_with_version = os.path.join(
                root_dir_decoder, decoder_path_with_version
            )
            if not encoder_path_with_version:
                raise Exception("No encoder model found")
            if not decoder_path_with_version:
                raise Exception("No decoder model found")
            providers = ["CPUExecutionProvider"]
            # TODO: needs more validation and support of batch size in some cases
            # Set the execution provider to GPU if available
            if not force_provider:
                # if "CUDAExecutionProvider" in onnxruntime.get_available_providers():
                #     providers = ["CUDAExecutionProvider"]
                if "DmlExecutionProvider" in onnxruntime.get_available_providers():
                    providers = ["DmlExecutionProvider"]
                elif "CoreMLExecutionProvider" in onnxruntime.get_available_providers():
                    providers = ["CoreMLExecutionProvider"]
            else:
                providers = [force_provider]

            sess_options_encoder = onnxruntime.SessionOptions()
            sess_options_decoder = onnxruntime.SessionOptions()

            # if we are profiling, enable it
            if os.environ.get("MODEL_PROFILING", False):
                sess_options_encoder.enable_profiling = True
                sess_options_encoder.profile_file_prefix = (
                    "generic_model_profile_encoder"
                )

                sess_options_decoder.enable_profiling = True
                sess_options_decoder.profile_file_prefix = (
                    "generic_model_profile_decoder"
                )
            self.encoder = onnxruntime.InferenceSession(
                encoder_path_with_version,
                providers=providers,
                sess_options=sess_options_encoder,
            )
            self.decoder = onnxruntime.InferenceSession(
                decoder_path_with_version,
                providers=providers,
                sess_options=sess_options_decoder,
            )

            self.enable_tool()
        except Exception as e:
            logger.error(f"Error loading encoder: {e}")
            # remove from disk if they exist
            if os.path.exists(self.encoder_path):
                os.remove(self.encoder_path)
            if os.path.exists(self.decoder_path):
                os.remove(self.decoder_path)

    def enable_tool(self):
        self.loaded = True
        config.global_signals.set_magic_tool_disabled_signal.emit("Magic ROI (G)")
        config.global_signals.set_magic_tool_enabled_signal.emit("Magic ROI Plus")

    def disable_tool(self):
        self.loaded = False
        config.global_signals.set_magic_tool_enabled_signal.emit("Magic ROI (G)")
        config.global_signals.set_magic_tool_disabled_signal.emit("Magic ROI Plus")

    def cleanup_memory(self):
        self.long_term_memory_features = []
        self.long_term_memory_points = []
        self.long_term_memory_image_features = []

    def get_setting_value(
        self, qsettings: QtCore.QSettings, key: str, default_value: int
    ) -> int:
        if qsettings.contains(key):
            return qsettings.value(key, type=int)
        else:
            return default_value

    def map_coordinates(self, original_point, downsample_factor):
        return (
            original_point[0] // downsample_factor,
            original_point[1] // downsample_factor,
        )

    def calculate_similarity(self, feature_map, target_vector):
        # Calculating Euclidean distance
        distances = np.linalg.norm(feature_map - target_vector, axis=0)
        return distances

    def calculate_similarity_across_grid(self, feature_map, target_vector_grid):
        feature_map_grid = np.tile(feature_map, (64, 64, 1))
        return self.calculate_similarity(feature_map_grid, target_vector_grid)

    def compute_iou(self, mask1, mask2):
        # Compute Intersection over Union for two binary masks
        intersection = np.logical_and(mask1, mask2)
        union = np.logical_or(mask1, mask2)
        if not np.any(union):
            return 0
        return np.sum(intersection) / np.sum(union)

    def decay_score(self, score, iou, method="linear"):
        # Decay function for the score
        if method == "linear":
            return score * (1 - iou)
        elif method == "gaussian":
            return score * np.exp(-(iou**2) / 0.5)  # sigma can be adjusted
        return score

    def soft_nms(self, masks, scores, iou_threshold=0.5, score_threshold=0.001):
        # Soft-NMS implementation
        order = np.argsort(scores)[::-1]
        num_masks = len(masks)
        for i in range(num_masks):
            for j in range(i + 1, num_masks):
                iou = self.compute_iou(masks[order[i]], masks[order[j]])
                if iou > iou_threshold:
                    scores[order[j]] = self.decay_score(scores[order[j]], iou)

        # Filter out low score masks
        keep = [i for i in range(num_masks) if scores[i] > score_threshold]
        return [masks[i] for i in keep], [scores[i] for i in keep]

    def matrix_nms(
        self,
        seg_masks,
        cate_labels,
        cate_scores,
        kernel="gaussian",
        sigma=2.0,
        sum_masks=None,
    ) -> npt.NDArray[Any]:
        """Matrix NMS for multi-class masks in NumPy.

        Args:
            seg_masks (np.ndarray): shape (n, h, w)
            cate_labels (np.ndarray): shape (n), mask labels in descending order
            cate_scores (np.ndarray): shape (n), mask scores in descending order
            kernel (str): 'linear' or 'gaussian'
            sigma (float): std in gaussian method
            sum_masks (np.ndarray): The sum of seg_masks

        Returns:
            np.ndarray: cate_scores_update, array of shape (n)
        """
        n_samples = len(cate_labels)
        if n_samples == 0:
            return np.array([])
        if sum_masks is None:
            sum_masks = seg_masks.reshape(n_samples, -1).sum(axis=1)
        seg_masks = seg_masks.reshape(n_samples, -1).astype(float)

        # inter
        inter_matrix = np.dot(seg_masks, seg_masks.T)

        # union
        sum_masks_x = np.tile(sum_masks, (n_samples, 1))

        # iou
        iou_matrix = np.triu(
            inter_matrix / (sum_masks_x + sum_masks_x.T - inter_matrix), k=1
        )

        # label_specific matrix
        cate_labels_x = np.tile(cate_labels, (n_samples, 1))
        label_matrix = np.triu((cate_labels_x == cate_labels_x.T).astype(float), k=1)

        # IoU compensation
        compensate_iou = np.max(iou_matrix * label_matrix, axis=0)
        compensate_iou = np.tile(compensate_iou, (n_samples, 1)).T

        # IoU decay
        decay_iou = iou_matrix * label_matrix

        # matrix nms
        if kernel == "gaussian":
            decay_matrix = np.exp(-1 * sigma * np.square(decay_iou))
            compensate_matrix = np.exp(-1 * sigma * np.square(compensate_iou))
            decay_coefficient = np.min(decay_matrix / compensate_matrix, axis=0)
        elif kernel == "linear":
            decay_matrix = (1 - decay_iou) / (1 - compensate_iou)
            decay_coefficient = np.min(decay_matrix, axis=0)
        else:
            raise NotImplementedError

        # update the score
        cate_scores_update = cate_scores * decay_coefficient
        return cate_scores_update

    @config.threaded
    @config.group_task("start_suggested_mask_generator")
    def start_suggested_mask_generator(
        self,
        image_object=None,
        celer_sight_object=None,
        initial_bbox=None,  # [x,y,w,h]
        subject_bbox=None,  # [x,y,w,h]
    ):
        # start generating button spinner etc..
        config.global_signals.set_mask_suggestor_generating_signal.emit(True)
        QtWidgets.QApplication.processEvents()
        logger.debug("Starting suggested mask generator")
        if not self.loaded:
            try:
                self.load_models()
            except Exception as e:
                logger.error(f"Error loading models: {e}")
                return
        # self.MainWindow.ai_model_settings_widget._on_roi_assistant_cancel_button_clicked()
        if not config.user_cfg["USER_WORKERS"]:
            QtWidgets.QApplication.processEvents()
        if config.group_stop_flags.get("start_suggested_mask_generator"):
            self.cleanup_mask_suggestions()
            return
        if isinstance(image_object, type(None)):
            # fetch the current image object
            image_object = (
                self.MainWindow.DH.BLobj.groups["default"]
                .conds[self.MainWindow.DH.BLobj.get_current_condition()]
                .images[self.MainWindow.current_imagenumber]
            )
        if isinstance(celer_sight_object, type(None)):
            current_condition = self.MainWindow.DH.BLobj.get_current_condition()
            current_group = self.MainWindow.DH.BLobj.get_current_group()
            treatment_uuid = (
                self.MainWindow.DH.BLobj.groups[current_group]
                .conds[current_condition]
                .unique_id
            )

            celer_sight_object = {
                "image_uuid": image_object.unique_id,
                "condition_uuid": treatment_uuid,
                "group_uuid": current_group,  # should change to uuid when its supported
                "class_uuid": self.MainWindow.DH.BLobj.get_current_class_uuid(),
                "mask_uuid": None,  # not used in roi suggestsions
            }
        if isinstance(initial_bbox, type(None)):
            initial_bbox = self._initial_tile_box
        if isinstance(subject_bbox, type(None)):
            # only needed to compute the overlap
            subject_bbox = self._subject_bbox  # latest bbox of the subjec
        # get all tiles
        from celer_sight_ai.io.image_reader import (
            generate_complete_spiral_tiles,
        )

        config.global_signals.lock_ui_signal.emit(
            [
                "left_group",
                "treatment_image_buttons",
                "condition_buttons",
                "initialize_analysis_button",
            ]
        )
        if config.group_stop_flags.get("start_suggested_mask_generator"):
            self.cleanup_mask_suggestions()
            return
        image_width = image_object.SizeX
        image_height = image_object.SizeY
        overlap = int(max(subject_bbox[2], subject_bbox[3]) * 1.1)
        all_tiles = generate_complete_spiral_tiles(
            image_width, image_height, initial_bbox, overlap
        )

        for i, tile in enumerate(all_tiles):
            # The spinner on the generator button stops every time the tile changes
            # so we have to restart it for now.
            if not config.user_cfg["USER_WORKERS"]:
                QtWidgets.QApplication.processEvents()

            if config.group_stop_flags.get("start_suggested_mask_generator"):
                self.cleanup_mask_suggestions()
                return
            if tile[2] <= overlap or tile[3] <= overlap:
                continue
            effective_tile = [
                max(0, tile[0]),  # x
                max(0, tile[1]),  # y
                min(image_width, tile[0] + tile[2]) - max(0, tile[0]),  # w
                min(image_height, tile[1] + tile[3]) - max(0, tile[1]),  # h
            ]
            # get the image first
            image = image_object.getImage(
                to_uint8=True,
                to_rgb=True,
                fast_load_ram=True,
                bbox=tile,
                avoid_loading_ultra_high_res_arrays_normaly=True,
            )
            if isinstance(image, type(None)):
                continue
            self.get_mask_suggestions(
                image,
                image.shape,
                celer_sight_object,
                tile,
                effective_tile,  # cropped tile from the image bounds
                features=None,
                overlap=overlap,
                stabilize_features=(
                    False if i == 0 else True
                ),  # No need to stabilize the first tile
            )

    def get_representative_feature(self, pred_masks, scores, feature_arr):
        from skimage.morphology import thin

        # get the representative feature from the mask
        best_score_idx = np.argmax(scores[0])
        best_mask = pred_masks[0][best_score_idx]
        # downsample mask by 4
        best_mask = cv2.resize(best_mask, (64, 64))
        # get all points within the mask that are true
        best_mask = best_mask > self.mask_threshold
        best_mask = thin(best_mask, max_num_iter=2)
        points = np.array(np.where(best_mask)).T
        # get a maximum of 10  points and get their average feature
        # these points should be close to the center of the mask
        points = points[
            np.random.choice(points.shape[0], min(3, points.shape[0]), replace=False)
        ]

        # get the feature map for each point
        # for every point pair,
        out_features = np.empty((len(points), 256))
        # convert features from (1, 256, 64, 64) to (1, 64, 64 , 256)
        feature_arr = feature_arr.transpose(0, 2, 3, 1)
        out_features = [feature_arr[0][i[0], i[1]] for i in points]
        # get the average feature
        return out_features

    def get_all_relevent_points_from_feature_map(
        self,
        thresh=0.4,
        mode="cosine",
        image_dump_threshold=0.5,
        image_features_memory=None,
    ) -> np.ndarray:
        from scipy.spatial.distance import cdist

        # The threshold for the cosine range is 0.2 to 0.4. The slider for this
        # Threshold is  from 0 to 100. The value is confidence, and so we need to inverse the value
        # Slider at full -> which means a low threshold of similiartiy.
        thresh = (
            (
                (
                    100
                    - self.MainWindow.ai_model_settings_widget.positive_roi_threshold_slider.value()
                )
                / 100
            )
            * 0.2
        ) + 0.2

        features = self.long_term_memory_features

        positive_features = [
            i for i in image_features_memory if i["sign"] == "positive"
        ]
        negative_feature = [i for i in image_features_memory if i["sign"] == "negative"]
        reshaped_feature_map = features[0].reshape(256, -1).T  # Shape (4096, 256)
        positive_distance_maps = []
        negative_distance_maps = []

        for f in positive_features:
            vectors = f["vectors"]
            for vector in vectors:
                distances = cdist(reshaped_feature_map, [vector], metric=mode)
                # Reshaping the distances back to a 64x64 map
                distance_map = distances.reshape(64, 64)
                positive_distance_maps.append(distance_map)
        if not positive_distance_maps:
            return []
        # for vector in negative_vectors:
        #     distances = cdist(reshaped_feature_map, [vector], metric=mode)
        #     # Reshaping the distances back to a 64x64 map
        #     distance_map = distances.reshape(64, 64)
        #     negative_distance_maps.append(distance_map)

        # cv2.imwrite("test.jpg", (positive_distance_maps[0] * 100).astype(np.uint8))

        # add all positive maps together
        distance_pixmap = np.zeros((64, 64))
        if len(positive_distance_maps) > 0:
            for i in range(len(positive_distance_maps)):
                # for distance_map in positive_distance_maps:
                distance_pixmap += (positive_distance_maps[i] < thresh).astype(np.uint8)

        # checker like pattern
        distance_pixmap[1::2, ::2] = 0
        distance_pixmap[::2, 1::2] = 0
        # print(scipy.stats.signaltonoise(distance_pixmap))
        # get all points
        points = np.where(distance_pixmap)
        points = np.array(points).T

        # for distance_map in positive_distance_maps:
        distance_pixmap = (distance_map < thresh).astype(np.uint8)
        # print(noise_map[(distance_pixmap < 0.7).astype(bool)].mean())

        # checker like pattern
        distance_pixmap[1::2, ::2] = 0
        distance_pixmap[::2, 1::2] = 0
        # cv2.imwrite("test_2.jpg", (distance_pixmap * 255).astype(np.uint8))
        # overlay the values on the image

        # print(scipy.stats.signaltonoise(distance_pixmap))
        # get all points
        points = np.where(distance_pixmap)
        points = np.array(points).T
        # order points clossest to the center
        center = np.array([32, 32])
        points = points[np.argsort(np.linalg.norm(points - center, axis=1))]

        print(len(points))
        return points

    # def predict_relevant_points(
    #     self, mask_candidates, scores, features, rel_pos=4, points_to_keep=5
    # ):
    #     from skimage.morphology import skeletonize

    #     # get the relevant points from the mask candidates
    #     # get the lowest
    #     target_score_idx = scores.index(sorted(scores)[-rel_pos])

    #     # reshape that mask to the feature size
    #     mask = mask_candidates[0][target_score_idx]
    #     mask = cv2.resize((mask > 0).astype(np.uint8), (64, 64))
    #     # skeletonize
    #     mask = skeletonize(mask)
    #     # get all points where the mask is true
    #     points = np.where(mask)
    #     points = np.array(points).T
    #     # shuffle array and pick 10 random points
    #     np.random.seed(43)
    #     points = points[
    #         np.random.choice(
    #             points.shape[0], min(points_to_keep, points.shape[0]), replace=False
    #         )
    #     ]

    #     # rescale to be on the original image size
    #     # points[0] = (points[0] / (64 / self.original_size[0])).astype(np.int32)
    #     # points[1] = (points[1] / (64 / self.original_size[1])).astype(np.int32)
    #     return points

    def signaltonoise_dB(self, a, axis=0, ddof=0):
        a = np.asanyarray(a)
        m = a.mean(axis)
        sd = a.std(axis=axis, ddof=ddof)
        return 20 * np.log10(abs(np.where(sd == 0, 0, m / sd)))

    def magic_box_predict(
        self,
        image,
        celer_sight_object,
        point1,
        point2,
        post_process=True,
        tile_bbox=None,
    ):
        """
        Main predictor method that segments objects by bounding box
        TODO: when using points, add a viewport point1 , point2 to do
        more efficient image cropping and segmentation
        celer_sight_object : dict
        {
            image_uuid: str,
            condition_uuid: str,
            group_uuid: str, # its group name for now
            class_uuid: str,
        }
        """
        if not self.loaded:
            self.load_models()
        if not self.loaded:
            raise Exception("Models not loaded")
        logger.debug(f"Predict at {point1} {point2}")
        # record initial tile_box
        self._last_used_current_class_uuid = celer_sight_object[
            "class_uuid"
        ]  # hold class to use in mask suggestions
        self.cleanup_mask_suggestions(
            is_generating=True
        )  # remove any suggestions generated

        # the tile_bbox is always square and so we need to match it with the max of the image since the
        # image (a crop from the full image) is not always square, but the largest size should always match
        # the size of the tile_bbox
        resize_points = max(image.shape[0], image.shape[1]) / max(
            tile_bbox[2], tile_bbox[3]
        )

        # adjust point to image
        point1[0] = point1[0] * resize_points  # x1
        point1[1] = point1[1] * resize_points  # y1
        point2[0] = point2[0] * resize_points
        point2[1] = point2[1] * resize_points

        self._initial_tile_box = tile_bbox  # used in mask suggestions
        self._subject_bbox = [
            point1[0],
            point1[1],
            point2[0] - point1[0],
            point2[1] - point1[1],
        ]
        self._latest_celer_sight_object = celer_sight_object
        offset_x = 0
        offset_y = 0

        if tile_bbox:
            offset_x = tile_bbox[0]
            offset_y = tile_bbox[1]
        original_shape = image.shape[:2]
        logger.info(f"Image shape : {image.shape}")
        features, points, input_image, _ = self.get_feature_map(
            image, points=[point1, point2]
        )

        self.long_term_memory_features = features
        points = [
            [
                (points[0][0]),
                (points[0][1]),
            ],
            [
                (points[1][0]),
                (points[1][1]),
            ],
        ]  # points
        labels = [2, 3]
        points = np.expand_dims(np.asarray(points), 0)
        labels = np.expand_dims(np.asarray(labels), 0)
        # The above code is declaring a variable named "pred_mask" in Python. However, since there is
        # no assignment or initialization of a value to the variable, it is not clear what the code is
        # intended to do.
        try:
            pred_masks, scores, coords = self.predict(
                features=features,
                point_coords=points,
                point_labels=labels,
                original_size=original_shape,
                post_process=False,
                debug_image=input_image.copy(),
            )
        except Exception as e:
            logger.error(f"Error predicting: {e}")
            logger.info("Switching to default excecutioner")
            self.load_models(force_provider="CPUExecutionProvider")
            pred_masks, scores, coords = self.predict(
                features=features,
                point_coords=points,
                point_labels=labels,
                original_size=original_shape,
                post_process=False,
                debug_image=input_image.copy(),
            )
        pred_mask, score = self.post_process(pred_masks, scores, coords)

        representative_features = self.get_representative_feature(
            pred_masks, scores, features
        )
        features_from_mask = self.get_features_from_image_and_mask(
            pred_mask,
            score,
            image,
            celer_sight_object,  # mask_uuid
            representative_features,
            tile_bbox,
            points,
        )
        if isinstance(features_from_mask, type(None)):
            return None, None, None
        # # register features
        self.long_term_memory_image_features.append(
            # TODO: when image size dont match, crop the image ( or mask )
            features_from_mask
        )

        if post_process:
            pred_mask, score = self.post_process(pred_masks, scores, coords)

            return (
                cv2.resize(pred_mask.astype(np.uint8), original_shape[:2][::-1]),
                offset_x,
                offset_y,
            )

        # calculate if there should be any extra offset (because the  image was cropped and there is extra space on the right and the bottom)

        return pred_masks, offset_x, offset_y

    def cleanup_mask_suggestions(self, is_generating=False):
        import time

        # if there are still qgrahic item bounding boxes to indicated ongoing mask suggestion, remove them from the scene
        for inference_id in self._running_inferences:
            config.global_signals.remove_inference_tile_graphics_item_signal.emit(
                {"inference_uuid": inference_id}
            )
        self._running_inferences = []
        if not config.user_cfg["USER_WORKERS"]:
            QtWidgets.QApplication.processEvents()
        # wait until the cleanup is complete
        while self.MainWindow.viewer.during_mask_suggestion_cleanup:
            time.sleep(0.1)
        config.global_signals.set_mask_suggestor_generating_signal.emit(is_generating)

    def stop_mask_suggestion_generator_process(self):
        # This is a threaded process and we need to mark it as stopped
        # Then wait to confirm it has stopped.
        config.group_queues["start_suggested_mask_generator"] = []
        config.group_stop_flags["start_suggested_mask_generator"] = True
        import time

        if not config.group_running.get("start_suggested_mask_generator", False):
            return
        # wait until not runnning any more
        start = time.time()
        while (
            config.group_running["start_suggested_mask_generator"]
            and not time.time() - start > 1.5  # wait a maximum of 1.5 seconds
        ):
            time.sleep(0.03)
        return

    def accept_current_suggested_annotations(self):
        from celer_sight_ai.gui.custom_widgets.scene import PolygonAnnotation

        # Stop threaded generator process
        # Then convert all suggested annotations to normal annotations

        self.stop_mask_suggestion_generator_process()
        config.global_signals.unlock_ui_signal.emit()

        # Converts all suggested annotations on the current image to nomral annotations
        # and stops the annotation suggestion proccess

        self.MainWindow.ai_model_settings_widget.roi_assistant_generate_button_spinner.stop()
        self.MainWindow.ai_model_settings_widget.roi_assistant_generate_button.show()
        self.MainWindow.ai_model_settings_widget.roi_assistant_generate_button.setText(
            "Generate"
        )
        self.MainWindow.ai_model_settings_widget.roi_assistant_generate_button.setStyleSheet(
            """QPushButton{
            margin-top: 5px;
            color: rgba(90,185,90,140);
            background-color: rgba(60,100,60,40);
            border-radius: 5px;
            }
            QPushButton:hover{
                margin-top: 5px;
                color: rgb(100,255,100);
                background-color: rgba(0,100,0,50);
                border-radius: 5px;
            }
            """
        )

        # cancel the ROI assistant
        # get all masks from the scene that are suggested
        all_polygon_masks = [
            i
            for i in self.MainWindow.viewer._scene.items()
            if isinstance(i, PolygonAnnotation) and i.is_suggested
        ]
        logger.debug(
            f"Found {len(all_polygon_masks)} suggested masks to make to normal masks"
        )
        for mask in all_polygon_masks:
            mask.is_suggested = False

        # set all masks of the current image to is_suggested = False
        current_group = self.MainWindow.DH.BLobj.get_current_group()
        current_condition = self.MainWindow.DH.BLobj.get_current_condition()

        all_masks = (
            self.MainWindow.DH.BLobj.groups[current_group]
            .conds[current_condition]
            .images[self.MainWindow.current_imagenumber]
            .masks
        )
        all_suggested_masks = []
        # set all masks to not is_suggested
        for mask in all_masks:
            if mask.is_suggested:
                all_suggested_masks.append(mask)
            mask.is_suggested = False

        # convert all annotations in the scene to normal annotations
        suggested_items = [
            i
            for i in self.MainWindow.viewer._scene.items()
            if isinstance(i, PolygonAnnotation) and i.is_suggested
        ]
        for item in suggested_items:
            item.set_is_suggested(False)
            item.update_annotation()
            item.update_annotations_color()
            item.set_visible_all()

        # if current image is remote, send every mask to the server
        if (
            self.MainWindow.DH.BLobj.groups[current_group]
            .conds[current_condition]
            .images[self.MainWindow.current_imagenumber]
            .is_remote()
        ):
            image_object = (
                self.MainWindow.DH.BLobj.groups[current_group]
                .conds[current_condition]
                .images[self.MainWindow.current_imagenumber]
            )
            for item in all_suggested_masks:

                class_name = (
                    self.MainWindow.custom_class_list_widget.get_current_row_class_name()
                )
                data = {
                    "annotation_uuid": item.unique_id,
                    "supercategory": config.supercategory,
                    "category": class_name,  # text
                    "type": "polygon",
                    "data": self.MainWindow.numpy_to_python(
                        item.get_array_for_storing()
                    ),  # the array
                    "image_width": None,  # fill in later
                    "image_height": None,  # fill in later
                    "image_uuid": image_object.unique_id,
                    "audited": True,
                    "state": None,
                }
                new_uuid = config.client.insert_remote_annotation(data)
                image_object.change_mask_uuid(
                    new_uuid, item.unique_id
                )  # make sure ids match

    def get_mask_suggestions(
        self,
        image=None,
        original_shape=None,
        celer_sight_object={},
        tile_bbox=None,
        effective_image_tile=None,  # the tile that is actually visible on the file tile, (the cropped tile from the bounds of the image)
        features=None,
        stabilize_features=False,  # use previous features, paste them on the new image and predict
        overlap=None,  # provided along with stabilize_features to calclulate the image_data width to paste
    ):
        # import polygon
        from shapely import Polygon

        inference_uuid = config.get_unique_id()
        # add a polygon shape on the region that we are inferencing
        config.global_signals.add_inference_tile_graphics_item_signal.emit(
            {
                "tile_box": tile_bbox,
                "inference_uuid": inference_uuid,
                "image_uuid": celer_sight_object.get("image_uuid"),
                "is_animated": True,
            }
        )
        self._running_inferences.append(inference_uuid)
        QtWidgets.QApplication.processEvents()
        image_tmp = image.copy()
        if not config.user_cfg["USER_WORKERS"]:
            QtWidgets.QApplication.processEvents()
        from shapely.ops import unary_union

        if not effective_image_tile:
            effective_image_tile = [
                max(0, tile_bbox[0]),  # x
                max(0, tile_bbox[1]),  # y
                min(original_shape[1], tile_bbox[0] + tile_bbox[2]) - tile_bbox[0],  # w
                min(original_shape[0], tile_bbox[1] + tile_bbox[3]) - tile_bbox[1],  # h
            ]
        # calculate resize factor for the mask
        resize_factor_x = image.shape[1] / effective_image_tile[2]
        resize_factor_y = image.shape[0] / effective_image_tile[3]

        if config.group_stop_flags.get("start_suggested_mask_generator"):
            self.cleanup_mask_suggestions()
            return
        # get positive areas with the same class
        memory_image_features = [
            i
            for i in self.long_term_memory_image_features
            if i["sign"] == "positive"
            and i["class_uuid"] == self._last_used_current_class_uuid
        ]
        for i in range(len(self.long_term_memory_image_features)):
            self.long_term_memory_image_features[i]["temporary_center_point"] = None
        # paste every image_data on the right side of the image if stabilize_features, resized to less than the overlap
        if stabilize_features:
            h = 0
            right_bound_without_stabilize_features = float(
                "inf"
            )  # bboxes were we delete any points inside
            # as they are used to stabilize the feaetures only
            for i, item in enumerate(memory_image_features):
                # resize to width of overlap with numpy, keep aspect ratio
                img = item["image_data"]
                resize_factor = (overlap * 0.9) / img.shape[1]
                new_width = int(img.shape[1] * resize_factor)
                new_height = int(img.shape[0] * resize_factor)
                if h + new_height > image.shape[0]:
                    # we dont need to go over the image bounds
                    break
                img = cv2.resize(img, (new_width, new_height))
                try:
                    # paste on the right side of the image
                    image_tmp[
                        h : h + img.shape[0], image_tmp.shape[1] - img.shape[1] :, :
                    ] = img
                except:
                    logger.error(
                        f"Error pasting image {i} on the right side of the image from dims: {img.shape} to {image_tmp.shape}"
                    )
                # save the temporary center point of the pasted small image , [x,y]
                item["temporary_center_point"] = [
                    round(image.shape[1] - (img.shape[1] / 2)),
                    h + round(img.shape[1] / 2),
                ]
                # delete areas will be adjusted later along with
                # temporary center point
                right_bound_without_stabilize_features = min(
                    item["temporary_center_point"][0]
                    / 16,  # convert point to 64x64 from 1024x1024
                    right_bound_without_stabilize_features,
                )
                h += img.shape[0]

        if config.group_stop_flags.get("start_suggested_mask_generator"):
            self.cleanup_mask_suggestions()
            return
        (
            self.long_term_memory_features,
            points,
            input_image,
            adjusted_points,
        ) = self.get_feature_map(
            image_tmp, map_points_to_input_image=[[image_tmp.shape[:2][::-1]]]
        )
        # adjust all temporary_center_points
        for i in range(len(memory_image_features)):
            if not isinstance(
                memory_image_features[i]["temporary_center_point"], type(None)
            ):
                memory_image_features[i]["temporary_center_point"][
                    0
                ] = memory_image_features[i]["temporary_center_point"][0] * (
                    adjusted_points[0][0][0] / image_tmp.shape[1]
                )
                memory_image_features[i]["temporary_center_point"][
                    1
                ] = memory_image_features[i]["temporary_center_point"][1] * (
                    adjusted_points[0][0][1] / image_tmp.shape[0]
                )

        points = self.get_all_relevent_points_from_feature_map(
            image_features_memory=memory_image_features
        )
        logger.debug(f"Points found for mask suggestor: {points}")

        optimal_areas = [
            i["area"] for i in memory_image_features if i["sign"] == "positive"
        ]
        if stabilize_features:
            # adjust the right bound to be in the same scale as the points
            right_bound_without_stabilize_features = (
                right_bound_without_stabilize_features
                * (adjusted_points[0][0][1] / image_tmp.shape[0])
            )
            # skip point as  its within the stabilize features area
            points = [
                p for p in points if p[1] < (right_bound_without_stabilize_features - 2)
            ]

        # for each point, get the mask
        for p in points:

            if not config.user_cfg["USER_WORKERS"]:
                QtWidgets.QApplication.processEvents()

            if config.group_stop_flags.get("start_suggested_mask_generator"):
                self.cleanup_mask_suggestions()
                return

            # tramsfer point to original image
            p *= 16  # -> 1024x1024
            # p[0] /= self.resize_xy s
            # inverse x and y
            p = p[::-1]
            p.astype(np.int32)
            # predict new mask set from point
            # img = cv2.circle(cv2.resize(image.copy() , (1024,1024)) , (int(p[0]) , int(p[1])) , 2 , (255,0 ,0), -1)
            # cv2.imwrite("test.jpg" , img)
            # p_ = (p*16) / self.resize_xy
            pred_masks, scores, coords = self.predict(
                features=self.long_term_memory_features,
                point_coords=np.array([[p]]),
                point_labels=[[1]],
                original_size=original_shape,
                post_process=False,
                # debug_image=input_image.copy(),
            )
            # add best mask to scene
            # post process first
            pred_mask, score = self.post_process(
                pred_masks, scores, coords, optimal_areas=optimal_areas
            )

            # image mask is touching the edges of the image, ignore
            if (
                pred_mask[0, :].sum() > 0
                or pred_mask[-1, :].sum() > 0
                or pred_mask[:, 0].sum() > 0
                or pred_mask[:, -1].sum() > 0
            ):
                continue
            if not self.validate_predicted_mask(pred_mask, image_tmp):
                continue
            poly = mask_to_polygon(
                pred_mask,
                original_shape,
                offset_x=effective_image_tile[0],
                offset_y=effective_image_tile[1],
                resize_factor_x=resize_factor_x,
                resize_factor_y=resize_factor_y,
            )
            if config.group_stop_flags.get("start_suggested_mask_generator"):
                self.cleanup_mask_suggestions()
                return
            # send to annotation object
            config.global_signals.create_annotation_object_signal.emit(
                {
                    "treatment_uuid": celer_sight_object.get("condition_uuid"),
                    "group": celer_sight_object[
                        "group_uuid"
                    ],  # is actually group name for now
                    "array": poly,
                    "image_uuid": celer_sight_object["image_uuid"],
                    "class_id": self._last_used_current_class_uuid,
                    "mask_type": "polygon",
                    "allow_sending_remote": False,  # bc they are temporary masks
                    "mask_uuid": None,
                    "score": score,
                    "is_suggested": True,
                }  # m -> QPolygonF object
            )
            if not config.user_cfg["USER_WORKERS"]:
                QtWidgets.QApplication.processEvents()

        polygon = Polygon(
            [
                (tile_bbox[0], tile_bbox[1]),
                (tile_bbox[0] + tile_bbox[2], tile_bbox[1]),
                (tile_bbox[0] + tile_bbox[2], tile_bbox[1] + tile_bbox[3]),
                (tile_bbox[0], tile_bbox[1] + tile_bbox[3]),
            ]
        )
        if isinstance(self.infered_boundry_array, type(None)):
            self.infered_boundry_array = polygon
        else:
            # create a polygon union

            self.infered_boundry_array = unary_union(
                [self.infered_boundry_array, polygon]
            )
        # add a polygon shape on the region that we are inferencing
        config.global_signals.remove_inference_tile_graphics_item_signal.emit(
            {"inference_uuid": inference_uuid}
        )

        try:
            if inference_uuid in self._running_inferences:
                self._running_inferences.remove(inference_uuid)
        except Exception as e:
            logger.debug(f"Error removing inference uuid: {e}")
        if not config.user_cfg["USER_WORKERS"]:
            QtWidgets.QApplication.processEvents()

    def validate_predicted_mask(self, mask_arr, image_arr):
        """
        Return true if the mask is valid, false otherwise
        """
        bbox = cv2.boundingRect(mask_arr.astype(np.uint8))
        w = self.MainWindow.ai_model_settings_widget
        size_invalid = False
        area_invalid = False
        color_invalid = False

        for image_feature in self.long_term_memory_image_features:
            #  sure that the size is within 40% of the original size
            average_bbox_side = (
                image_feature["size"][2] + image_feature["size"][3]
            ) // 2
            if abs(
                average_bbox_side - ((bbox[2] + bbox[3]) // 2)
            ) >= average_bbox_side * (1 - (w.shape_roi_threshold_slider.value() / 100)):
                logger.debug("Invalid size")
                size_invalid = True

            # make sure area is within 40% of the original area
            if abs(image_feature["area"] - mask_arr.sum()) >= image_feature["area"] * (
                1 - (w.shape_roi_threshold_slider.value() / 100)
            ):
                area_invalid = True
                logger.debug("Invalid Area")
            try:
                # make sure mean color is similar
                if (
                    abs(np.mean(image_arr[mask_arr]) - image_feature["mean_color"])
                    >= (1 - (w.image_similarity_threshold_slider.value() / 100))
                    * 255  # this might not be the best threshold
                ):
                    color_invalid = True
                    logger.debug("Invalid Color")
            except Exception as e:
                pass
        if size_invalid or area_invalid or color_invalid:
            return False

        return True

    def get_features_from_image_and_mask(
        self, mask, score, image, celer_sight_object, vectors, tile_bbox, points
    ):
        # Get the features for an image provided a mask

        # first check bounds
        if not mask.shape == image.shape[:2]:
            return None
        points_future = points // 16  # convert to 64x64
        # get actual object shape with cv2 where the array is nonzero
        object_dict = {
            "area": mask.sum(),
            "size": cv2.boundingRect(mask.astype(np.uint8)),
            "mean_color": np.mean(image[mask], axis=(0, 1)),
            "points": points_future,
            "vectors": vectors,
            "tile_bbox": tile_bbox,
            "image_uuid": celer_sight_object["image_uuid"],
            "mask_uuid": celer_sight_object["mask_uuid"],
            "class_uuid": celer_sight_object["class_uuid"],
            "image_data": image[
                int(points_future[0][0][1]) : int(points_future[0][1][1]),
                int(points_future[0][0][0]) : int(points_future[0][1][0]),
                ...,
            ],  # image data of the bounding box, used to stabilize features across large images
            "sign": "positive",
            "temporary_center_point": None,  # used to stabilize features across large images, different for every tile.
        }
        return object_dict

    def resizeAndPad(
        self, img, size, padColor=0, points=None, map_points_to_input_image=None
    ):
        h, w = img.shape[:2]
        sh, sw = size

        # interpolation method
        if h > sh or w > sw:  # shrinking image
            interp = cv2.INTER_AREA
        else:  # stretching image
            interp = cv2.INTER_CUBIC
        # scale first, then pad
        # find the maximum side
        max_side = max(h, w)
        # scale to fit the max side to size
        scale = sw / max_side if sw / h > sw / w else sh / max_side
        # resize with cv2
        img = cv2.resize(img, (0, 0), fx=scale, fy=scale, interpolation=interp)
        self.input_size = tuple(img.shape[:2])
        if not isinstance(points, type(None)):
            # resize poitns
            points = np.array(points)
            points[..., 0] = np.array(points)[..., 0] * scale
            points[..., 1] = np.array(points)[..., 1] * scale
        # if not isinstance(map_points_to_input_image, type(None)):
        #     # resize poitns
        #     map_points_to_input_image = np.array(map_points_to_input_image) * scale

        # compute scaling and pad sizing
        pad_top = 0
        pad_bot = int(abs(img.shape[0] - sh))
        pad_left = 0
        pad_right = int(abs(img.shape[1] - sw))

        # set pad color
        # color image but only one color provided
        if len(img.shape) == 3 and not isinstance(padColor, (list, tuple, np.ndarray)):
            padColor = [padColor] * 3

        # pad
        scaled_img = cv2.copyMakeBorder(
            img,
            pad_top,
            pad_bot,
            pad_left,
            pad_right,
            borderType=cv2.BORDER_CONSTANT,
            value=padColor,
        )
        return scaled_img, points, map_points_to_input_image

    def get_preprocess_shape(
        self, oldh: int, oldw: int, long_side_length: int
    ) -> Tuple[int, int]:
        """
        Compute the output size given input size and target long side length.
        """
        scale = float(long_side_length) * 1.0 / float(max(oldh, oldw))
        newh, neww = oldh * scale, oldw * scale
        neww = int(neww + 0.5)
        newh = int(newh + 0.5)
        return (newh, neww)

    def get_feature_map(
        self,
        image: np.ndarray,
        image_format: str = "RGB",
        points=None,
        upscale=1,
        map_points_to_input_image=None,  # points mapped to feature map
    ) -> None:
        assert image_format in [
            "RGB",
            "BGR",
        ], f"image_format must be in ['RGB', 'BGR'], is {image_format}."
        if image_format != self.image_format:
            image = image[..., ::-1]
        total_output = np.zeros(
            (1, 256, 64 * (2 ** (upscale - 1)), 64 * (2 ** (upscale - 1))),
            dtype=np.float32,
        )
        # Transform the image to the form expected by the model
        target_size = self.get_preprocess_shape(
            image.shape[0], image.shape[1], self.img_size
        )
        # calculate resize on x

        self.resize_xy = max(target_size[1], target_size[0]) / max(
            image.shape[1], image.shape[0]
        )

        # resize points
        # if points is not None:
        #     points = np.array(points)
        #     points[..., 0] = np.array(points)[..., 0] * self.resize_xy
        #     points[..., 1] = np.array(points)[..., 1] * self.resize_xy
        # if map_points_to_input_image is not None:
        #     map_points_to_input_image = np.array(map_points_to_input_image)
        #     map_points_to_input_image[..., 0] = (
        #         np.array(map_points_to_input_image)[..., 0] * resize_y
        #     )
        #     map_points_to_input_image[..., 1] = (
        #         np.array(map_points_to_input_image)[..., 1] * resize_x
        #     )
        # add the output of the model in a grid fashion to total output
        # pad to self.img_size
        input_image, points, map_points_to_input_image = self.resizeAndPad(
            image,
            (self.img_size, self.img_size),
            points=points,
            map_points_to_input_image=map_points_to_input_image,
        )
        self.reset_feature_map()
        self.original_size = image.shape[:2]

        width_chunk = input_image.shape[1] // upscale
        height_chunk = input_image.shape[0] // upscale
        for i in range(upscale):
            for j in range(upscale):
                input_image_encoder = input_image[
                    i * height_chunk : (i + 1) * height_chunk,
                    j * width_chunk : (j + 1) * width_chunk,
                ]
                input_image_encoder = input_image_encoder.transpose(2, 0, 1)[
                    None, :, :, :
                ]
                input_image_encoder = self.preprocess(input_image_encoder).astype(
                    np.float32
                )

                input_name = self.encoder.get_inputs()[0].name

                outputs = self.encoder.run(
                    None,
                    {
                        input_name: np.expand_dims(input_image_encoder, 0).reshape(
                            1, 3, self.img_size, self.img_size
                        )
                    },
                )
                total_output[:, :, i * 64 : (i + 1) * 64, j * 64 : (j + 1) * 64] = (
                    outputs[0]
                )

        # features, adjusted points, input image, map_points_to_input_image
        return total_output, points, input_image, map_points_to_input_image

    def predict(
        self,
        features=None,
        point_coords=None,
        point_labels=None,
        original_size=None,
        post_process=True,
        debug_image=None,
    ) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
        import copy

        old_h, old_w = original_size[:2]
        new_h, new_w = self.get_preprocess_shape(
            original_size[0], original_size[1], self.img_size
        )
        coords = copy.deepcopy(point_coords).astype(float)

        # make sure all coords are constrained within 0 to img_size
        coords[..., 0] = np.clip(coords[..., 0], 0, self.img_size)
        coords[..., 1] = np.clip(coords[..., 1], 0, self.img_size)

        outputs = self.decoder.run(
            None,
            {
                "image_embeddings": features,
                "point_coords": coords.astype(np.float32),
                "point_labels": np.array(point_labels).astype(np.float32),
            },
        )

        scores, low_res_masks = outputs[0], outputs[1]
        if post_process:
            return self.post_process(low_res_masks, scores, coords=coords)
        else:
            return low_res_masks, scores, coords

    def post_process(self, low_res_masks, scores, coords, optimal_areas=[]):
        masks = self.postprocess_masks(low_res_masks)
        masks = masks > self.mask_threshold
        masks_areas = []
        # resize low res masks
        if optimal_areas:
            masks_areas = [np.sum(i) for i in masks[0]]
        if len(masks) == 0:
            return None
        return self.get_bbox_mask_canditate(
            masks,
            scores,
            coords=coords,
            optimal_areas=optimal_areas,
            masks_areas=masks_areas,
        )

    def get_bbox_mask_canditate(
        self, masks, scores, coords, optimal_areas=None, masks_areas=None
    ):
        # We need to extract the highest scoring mask that does not touch the border of the image
        # if there is no mask that fullfills this criteria, we return the highest scoring mask
        MIN_SCORE = 0.5
        IGNORE_LEFT = False
        IGNORE_RIGHT = False
        IGNORE_TOP = False
        IGNORE_BOTTOM = False

        # order by score
        order = np.argsort(scores[0])[::-1]
        # From highest to lowest score, check if the mask touches the border
        for i in order:
            mask = masks[0][i]
            if not MIN_SCORE < scores[0][i]:
                break
            if len(coords[0]) > 1:  # only for bbox prompts
                # if lef bounds are the bounds of the image, ignore left
                if coords[0][0][0] <= 1:
                    IGNORE_LEFT = True
                if coords[0][1][0] >= self.img_size - 1:
                    IGNORE_RIGHT = True
                if coords[0][0][1] <= 1:
                    IGNORE_TOP = True
                if coords[0][1][1] >= self.img_size - 1:
                    IGNORE_BOTTOM = True

            # check if mask is much larger than the source mask
            if optimal_areas:
                # how many areas do we have that fit the optimal area?
                areas = np.array(masks_areas)
                for optimal_area in optimal_areas:
                    # get the index of the area that is closest to the optimal area
                    area_diffs = np.abs(areas - optimal_area)
                    # check how many areas are within bounds
                    optimal_area_idx = np.where(area_diffs < optimal_area * 0.2)[0]
                    if len(optimal_area_idx) > 0:
                        # get the mask with the highest score out of the selected idxs
                        return (
                            masks[0][optimal_area_idx][
                                np.argmax(scores[0][optimal_area_idx])
                            ],
                            scores[0][optimal_area_idx][
                                np.argmax(scores[0][optimal_area_idx])
                            ],
                        )

            if (
                (np.sum(mask[0, :]) or IGNORE_LEFT) == 0
                or (np.sum(mask[-1, :]) == 0 or IGNORE_RIGHT)
                or (np.sum(mask[:, 0]) == 0 or IGNORE_TOP)
                or (np.sum(mask[:, -1]) == 0 or IGNORE_BOTTOM)
            ):
                return mask, scores[0][i]

        # If no mask touches the border, return the highest scoring mask
        return masks[0][order[0]], scores[0][order[0]]

    def reset_feature_map(self) -> None:
        """Resets the currently set image."""
        self.is_image_set = False
        self.features = None
        self.orig_h = None
        self.orig_w = None
        self.input_h = None
        self.input_w = None

    def preprocess(self, x: np.ndarray):
        x = (x - self.pixel_mean) / self.pixel_std
        h, w = x.shape[-2:]
        padh = self.img_size - h
        padw = self.img_size - w
        x = np.pad(
            x,
            ((0, 0), (0, 0), (0, padh), (0, padw)),
            mode="constant",
            constant_values=0,
        )
        return x

    def postprocess_masks(self, mask: np.ndarray):
        mask = mask.squeeze(0).transpose(1, 2, 0)
        mask = cv2.resize(
            mask, (self.img_size, self.img_size), interpolation=cv2.INTER_LINEAR
        )
        mask = mask[: self.input_size[0], : self.input_size[1], :]
        mask = cv2.resize(
            mask,
            (self.original_size[1], self.original_size[0]),
            interpolation=cv2.INTER_LINEAR,
        )
        mask = mask.transpose(2, 0, 1)[None, :, :, :]
        return mask


class sdknn_tool(object):
    """
    Class for handling mainly onnxmodels
    """

    # from scipy.cluster.vq import *
    def __init__(
        self, MainWindow, load_specialized_model=True, load_general_model=True
    ):
        # self.gbModel = 'QtAssets\\Utilities\\mats\\grub_cut_Ai.onnx'
        # onnxfile = open(self.gbModel , "rb")
        self.MainWindow = MainWindow
        self.specialized_model_loaded = False
        # byte
        # self.gbModelBuffer= onnxfile.read()
        # self.input_image = input_image
        self.orgHeight = None  # of the cut
        self.orgWidth = None  # of the cut
        self.running = False  # if we are currently grabcutting
        self.brush_state = "plus"  # or "minus" or move?
        # self.input_mask =
        from celer_sight_ai import config

        self.totalImportingNum = 1
        self.currentImportingNum = 1
        self.mbx = None
        self.inf_session = None
        self.sess_options = None
        self.currentTMP_FOLDER = None
        self.saved_umask = None
        self.mbx_input_width = config.MBX_INPUT_WIDTH
        self.mbx_input_height = config.MBX_INPUT_HEIGHT

        import os

        self.localCelerSightMatFolder = os.path.join(
            configHandle.getLocal(), "mats/mgb"
        )
        self.magic_box_2 = None
        if load_general_model:
            part1 = os.path.join(
                configHandle.getLocal(),
                "mats/mgb/general_encoder",
            )
            part2 = os.path.join(
                configHandle.getLocal(),
                "mats/mgb/general_decoder",
            )

            # config.global_signals.annotation_generator_stop_signal.connect(lambda)

            self.magic_box_2 = SamPredictorONNX(
                MainWindow=self.MainWindow, encoder_path=part1, decoder_path=part2
            )
        if load_specialized_model:
            self.load_specialized_model()

    def set_specialized_model_loaded(self, value):
        if value:
            self.specialized_model_loaded = True
            config.global_signals.set_magic_tool_disabled_signal.emit("Magic ROI (S)")

        else:
            self.specialized_model_loaded = False
            config.global_signals.set_magic_tool_enabled_signal.emit("Magic ROI (S)")

    def start_suggested_mask_generator(self, *args, **kwargs):
        return self.magic_box_2.start_suggested_mask_generator(*args, **kwargs)

    def load_specialized_model(self, force_execution=None):
        from celer_sight_ai import config

        try:
            model_path = os.path.join(configHandle.getLocal(), "mats/mgb")
            filename = "specialized"
            specialized_model_path = config.get_latest_file_version(
                model_path, filename
            )
            if not specialized_model_path or not os.path.exists(
                os.path.join(model_path, specialized_model_path)
            ):
                self.set_specialized_model_loaded(False)
                return
            from celer_sight_ai import config

            self.downloadFilesList = []
            self.replaceFilesList = []
            self.totalImportingNum = 1
            self.currentImportingNum = 1

            self.startSessWithModel(
                os.path.join(model_path, specialized_model_path),
                force_execution=force_execution,
            )
            self.set_specialized_model_loaded(True)
        except Exception as e:
            logger.error(f"Error loading specialized model: {e}")

    def getCurrentMagicBoxNetName(self):
        logger.debug("Getting current magic box settings")
        AnalObject = self.MainWindow.new_analysis_object
        from celer_sight_ai import config

        ProjectVars = config.global_params

        MyArea = ProjectVars.area_used
        NN_SETTINGS = config.cloud_user_variables
        if MyArea == self.MainWindow.new_analysis_object["body"]:
            PartProc = "ele_wholeBody"
        elif MyArea == self.MainWindow.new_analysis_object["head"]:
            PartProc = "head"
        elif MyArea == self.MainWindow.new_analysis_object["intestine"]:
            PartProc = "Intestine"
        elif MyArea == self.MainWindow.new_analysis_object["muscle"]:
            PartProc = "Muscle"
        elif MyArea == self.MainWindow.new_analysis_object["embryo"]:
            PartProc = "ele_embryo_1"
        elif MyArea == self.MainWindow.new_analysis_object["seam"]:
            PartProc = "Seam"
        elif MyArea == self.MainWindow.new_analysis_object["cellGeneric_CYTO"]:
            PartProc = "cellGeneric_CYTO"
        elif MyArea == self.MainWindow.new_analysis_object["scratch"]:
            PartProc = "scratch"
        elif MyArea == self.MainWindow.new_analysis_object["abnormaly_classification"]:
            PartProc = "abnormaly_classification"
        elif MyArea == self.MainWindow.new_analysis_object["peumothorax_bbox"]:
            PartProc = "peumothorax_bbox"
        elif MyArea == self.MainWindow.new_analysis_object["flies_adult_body"]:
            PartProc = "flies_adult_body"
        else:
            PartProc = "GENERIC"
        from celer_sight_ai import config

        self.mbx_input_width = config.MBX_INPUT_WIDTH
        self.mbx_input_height = config.MBX_INPUT_HEIGHT
        if NN_SETTINGS:  # in offline mode its none
            if PartProc in NN_SETTINGS["LINKERS"].keys():
                logger.info("yes, model has quick annotate!")
                ItemsList = NN_SETTINGS["LINKERS"][PartProc]

                for NN_ITEM in ItemsList:
                    if NN_ITEM["TYPE"] == "magic box":
                        self.mbx_input_width = int(NN_ITEM["dim_x"])
                        self.mbx_input_height = int(NN_ITEM["dim_y"])

                        return NN_ITEM["FILENAME"]

    def updateDownloadProgress(self, value):
        self.MainWindow.MyLoadingAnimationDialogForm.progressBar.setValue(int(value))

        self.MainWindow.MyLoadingAnimationDialogForm.RemainingTimeLabel.setText(
            str(self.currentImportingNum) + " out of " + str(self.totalImportingNum)
        )

    @config.threaded
    def startSessWithModel(self, Model=None, force_execution=None):
        try:
            self.sess_options = onnxruntime.SessionOptions()
            self.sess_options.graph_optimization_level = (
                onnxruntime.GraphOptimizationLevel.ORT_ENABLE_ALL
            )
            if os.environ.get("MODEL_PROFILING", None):
                self.sess_options.enable_profiling = True
                self.sess_options.profile_file_prefix = "speciliazed_model_profile_"
            self.sess_options.intra_op_num_threads = 4
            self.sess_options.log_severity_level = 4
            if Model:
                if force_execution:
                    self.inf_session = onnxruntime.InferenceSession(
                        Model, self.sess_options, providers=[force_execution]
                    )
                else:
                    self.inf_session = onnxruntime.InferenceSession(
                        Model, self.sess_options, providers=["CPUExecutionProvider"]
                    )
        except Exception as e:
            logger.error(e)
            # remove model
            if os.path.exists(Model):
                os.remove(Model)
            raise e

    def get_specialized_bbox_mask(
        self, image, bounding_box: list, tile_bbox: list = None
    ):
        # boundin box is x1,y1,x2,y2
        # tile is x,y,w,h
        image = image[
            max(0, int(bounding_box[1])) : min(int(bounding_box[3]), image.shape[0]),
            max(0, int(bounding_box[0])) : min(int(bounding_box[2]), image.shape[1]),
            ...,
        ]
        offset_x = max(
            0, bounding_box[0] + tile_bbox[0]
        )  # + tile_bbox[0]  # - subject_bbox2[0]  # subject_bbox2[0]  # bounding_box[0] + tile_bbox[0]
        offset_y = max(
            bounding_box[1] + tile_bbox[1], 0
        )  # + tile_bbox[1]  # - subject_bbox2[1]  # subject_bbox2[1]  # bounding_box[1] + tile_bbox[1]

        self.orgHeight = image.shape[1]  # of the cut
        self.orgWidth = image.shape[0]  # of the cut
        if any([i <= 0 for i in image.shape[:2]]):
            return np.zeros((image.shape), dtype=np.uint8), 0, 0
        # image = resizeAndPad(image , (self.gbModel_fixed_size,self.gbModel_fixed_size),padColor = 40 )
        try:
            logger.debug("Image shape: " + str(image.shape))
            logger.debug(
                "cDimX "
                + str(self.mbx_input_width)
                + " cDimY "
                + str(self.mbx_input_height)
            )
        except Exception as e:
            logger.error(e)

        image = resize(image, (self.mbx_input_width, self.mbx_input_height))

        # normalize

        image = self.normalize(image)
        image = image.transpose((2, 0, 1))
        image = image.reshape(1, 3, self.mbx_input_width, self.mbx_input_height)

        logger.debug("Magic inference staring.")
        try:
            d1 = self.inf_session.run(
                [self.inf_session.get_outputs()[0].name],
                {self.inf_session.get_inputs()[0].name: image.astype(np.float32)},
            )
        except Exception as e:
            logger.error("Failed to run session with specialized model")
            logger.error(e)
            # loading startard model and retrying
            self.load_specialized_model(force_execution="CPU")
            try:
                d1 = self.inf_session.run(
                    [self.inf_session.get_outputs()[0].name],
                    {self.inf_session.get_inputs()[0].name: image.astype(np.float32)},
                )
            except Exception as e:
                logger.error("Failed to run session with specialized model")
                logger.error(e)
                config.global_signals.errorSignal.emit(f"Failed to run model : {e}")
                return np.zeros((image.shape), dtype=np.uint8)

        logger.debug("inf_session session run ok")
        img_cut = (d1[0].squeeze() > 0.5).astype(np.uint8)
        imgSum = np.sum(img_cut)
        # here we cut out all values smaller than 40 volume
        if imgSum <= 40:
            print("sum less than 40")
            return None

        # substract edgets for contours problem
        maskOut = cv2.resize(img_cut, (self.orgHeight, self.orgWidth))
        return maskOut, offset_x, offset_y

    def get_bounding_box_mask(
        self,
        image,
        celer_sight_object,
        bounding_box: list,
        tile_bbox: list = None,
    ) -> Tuple[np.ndarray, int, int]:
        """
        bounds a list condtianin (up) , (right) ,(down) ,(left)
        """
        import cv2
        import os
        from celer_sight_ai.config import MagicToolModes

        if self.MainWindow.ai_model_combobox.current_mode in [
            MagicToolModes.MAGIC_BOX_ROI_GENERIC,
            MagicToolModes.MAGIC_BOX_WITH_PREDICT,
        ]:
            try:
                maskOut, offset_x, offset_y = self.magic_box_2.magic_box_predict(
                    image,
                    celer_sight_object,
                    [bounding_box[0], bounding_box[1]],  # bbox point 1
                    [bounding_box[2], bounding_box[3]],  # bbox point 2
                    post_process=True,
                    tile_bbox=tile_bbox,
                )
            except Exception as e:
                logger.error("Failed to run generic model")
                logger.error(e)
                config.global_signals.errorSignal.emit(config.MODEL_UNAVAILABLE_MESSAGE)
                return np.zeros((image.shape), dtype=np.uint8), 0, 0
            if isinstance(maskOut, type(None)):
                return np.zeros((image.shape), dtype=np.uint8), 0, 0
        else:
            if not self.inf_session:
                config.global_signals.errorSignal.emit(config.MODEL_UNAVAILABLE_MESSAGE)
            maskOut, offset_x, offset_y = self.get_specialized_bbox_mask(
                image, bounding_box, tile_bbox
            )

        return maskOut, offset_x, offset_y

    def getHighestIntBorders(self, segMap):
        # here we calculate max value for the cut out
        width = segMap.shape[0]
        height = segMap.shape[1]
        mask = np.zeros(segMap.shape, dtype=np.uint8)
        if self.forgetBounds[0] == 0:  # up
            cv2.line(mask, (0, 0), (mask.shape[1], 0), (255), 2)

        if self.forgetBounds[1] == 0:  # right
            cv2.line(mask, (mask.shape[1], 0), (mask.shape[1], mask.shape[0]), (255), 2)

        if self.forgetBounds[2] == 0:  # down
            cv2.line(mask, (0, mask.shape[0]), (mask.shape[1], mask.shape[0]), (255), 2)

        if self.forgetBounds[3] == 0:  # left
            cv2.line(mask, (0, 0), (0, mask.shape[0]), (255), 2)
        mask = mask.astype(bool)

        return np.max(segMap[mask])

    def normalize(self, image):
        # # normalize image to imagenet standard
        # image = np.array(image).astype(np.float32) / np.max(
        #     image
        # )  # normalize to [0,1] range
        # mean = np.array([0.485, 0.456, 0.406])
        # std = np.array([0.229, 0.224, 0.225])

        tmpImg = np.empty((image.shape[0], image.shape[1], 3))
        img_max = np.max(image)
        if img_max != 0:
            image = image / img_max
        if image.shape[2] == 1:
            tmpImg[:, :, 0] = (image[:, :, 0] - 0.485) / 0.229
            tmpImg[:, :, 1] = (image[:, :, 0] - 0.485) / 0.229
            tmpImg[:, :, 2] = (image[:, :, 0] - 0.485) / 0.229
        else:
            tmpImg[:, :, 0] = (image[:, :, 0] - 0.485) / 0.229
            tmpImg[:, :, 1] = (image[:, :, 1] - 0.456) / 0.224
            tmpImg[:, :, 2] = (image[:, :, 2] - 0.406) / 0.225
        # if len(image.shape) == 3:
        #     if image.shape[2] == 3:
        #         pass
        #     elif image.shape[2] < 3:
        #         # replicate first channel until 3 channels
        #         while len(mean) > image.shape[2]:
        #             image = np.concatenate((image, image[:, :, :1]), axis=2)
        #     elif image.shape[2] > 3:
        #         # colorize channels
        #         channel_list = (
        #             self.MainWindow.DH.BLobj.groups[
        #                 self.MainWindow.DH.BLobj.get_current_group()
        #             ]
        #             .conds[self.MainWindow.DH.BLobj.get_current_condition()]
        #             .images[self.MainWindow.current_imagenumber]
        #             .channel_list
        #         )
        #         image = (
        #             self.MainWindow.DH.BLobj.groups[
        #                 self.MainWindow.DH.BLobj.get_current_group()
        #             ]
        #             .conds[self.MainWindow.DH.BLobj.get_current_condition()]
        #             .combine_channels(image, channel_list)
        #         )
        # elif len(image.shape) == 2:
        #     channel_list = (
        #         self.MainWindow.DH.BLobj.groups[
        #             self.MainWindow.DH.BLobj.get_current_group()
        #         ]
        #         .conds[self.MainWindow.DH.BLobj.get_current_condition()]
        #         .images[self.MainWindow.current_imagenumber]
        #         .channel_list
        #     )
        #     image = (
        #         self.MainWindow.DH.BLobj.groups[
        #             self.MainWindow.DH.BLobj.get_current_group()
        #         ]
        #         .conds[self.MainWindow.DH.BLobj.get_current_condition()]
        #         .combine_channels(image, channel_list)
        #     )
        # return (image - mean) / std

        return tmpImg


class GoogleDriveDownloader:
    """
    Minimal class to download shared files from Google Drive.
    """

    CHUNK_SIZE = 32768
    DOWNLOAD_URL = "https://docs.google.com/uc?export=download"

    @staticmethod
    def download_file_from_google_drive(
        file_id,
        dest_path,
        finalSize,
        callback=None,
        overwrite=False,
        unzip=False,
        showsize=False,
    ):
        """
        Downloads a shared file from google drive into a given folder.
        Optionally unzips it.

        Parameters
        ----------
        file_id: str
            the file identifier.
            You can obtain it from the sharable link.
        dest_path: str
            the destination where to save the downloaded file.
            Must be a path (for example: './downloaded_file.txt')
        overwrite: bool
            optional, if True forces re-download and overwrite.
        unzip: bool
            optional, if True unzips a file.
            If the file is not a zip file, ignores it.
        showsize: bool
            optional, if True print the current download size.
        Returns
        -------
        None
        """
        import requests
        import requests
        import zipfile
        import warnings
        from sys import stdout
        from os import makedirs
        from os.path import dirname
        from os.path import exists

        destination_directory = dirname(dest_path)
        if not exists(destination_directory):
            makedirs(destination_directory)

        if not exists(dest_path) or overwrite:
            session = requests.Session()
            print("Downloading...")
            # print('Downloading {} into {}... '.format(file_id, dest_path), end='')
            sys.stdout.flush()

            response = session.get(
                GoogleDriveDownloader.DOWNLOAD_URL, params={"id": file_id}, stream=True
            )

            token = GoogleDriveDownloader._get_confirm_token(response)
            if token:
                params = {"id": file_id, "confirm": token}
                response = session.get(
                    GoogleDriveDownloader.DOWNLOAD_URL, params=params, stream=True
                )

            if showsize:
                print()  # Skip to the next line

            current_download_size = [0]
            GoogleDriveDownloader._save_response_content(
                response,
                dest_path,
                showsize,
                current_download_size,
                callback,
                finalSize,
            )
            print("Done.")

            if unzip:
                try:
                    # print('Unzipping...', end='')
                    sys.stdout.flush()
                    with zipfile.ZipFile(dest_path, "r") as z:
                        z.extractall(destination_directory)
                    print("Done.")
                except zipfile.BadZipfile:
                    warnings.warn(
                        'Ignoring `unzip` since "{}" does not look like a valid zip file'.format(
                            file_id
                        )
                    )

    @staticmethod
    def _get_confirm_token(response):
        for key, value in response.cookies.items():
            if key.startswith("download_warning"):
                return value
        return None

    @staticmethod
    def _save_response_content(
        response, destination, showsize, current_size, callback=None, finalSize=None
    ):
        totalChuckSize = 0
        from celer_sight_ai import config

        with open(destination, "wb") as f:
            for chunk in response.iter_content(GoogleDriveDownloader.CHUNK_SIZE):
                if chunk:  # filter out keep-alive new chunks
                    f.write(chunk)
                    totalChuckSize += len(chunk)
                    try:
                        callback.emit(
                            int(100 * ((totalChuckSize / 1000) / int(finalSize)))
                        )
                    except Exception as e:
                        print(e)
                        pass
                    if showsize:
                        # print('\r' + GoogleDriveDownloader.sizeof_fmt(current_size[0]), end=' ')
                        sys.stdout.flush()
                        current_size[0] += GoogleDriveDownloader.CHUNK_SIZE

    @staticmethod
    def sizeof_fmt(num, suffix="B"):
        for unit in ["", "Ki", "Mi", "Gi", "Ti", "Pi", "Ei", "Zi"]:
            if abs(num) < 1024.0:
                return "{:.1f} {}{}".format(num, unit, suffix)
            num /= 1024.0
        return "{:.1f} {}{}".format(num, "Yi", suffix)


logger.info("Finised loading sdknn")
