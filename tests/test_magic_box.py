import unittest
import os
from celer_sight_ai.core.magic_box_tools import SamPredictorONNX, sdknn_tool
import cv2
import numpy as np
import logging as logger
import sys

logger = logger.getLogger(__name__)
memory_profiler = False
try:
    from memory_profiler import memory_usage
except ImportError:
    logger.warning("No memory_profiler found")
    memory_profiler = True
from functools import partial
import psutil

# os.environ["MODEL_PROFILING"] = "true"


class TestMagicBox(unittest.TestCase):
    def setUp(self):
        from celer_sight_ai import configHandle

        part1 = os.path.join(
            configHandle.getLocal(),
            "mats/mgb/general_encoder",
        )
        part2 = os.path.join(
            configHandle.getLocal(),
            "mats/mgb/general_decoder",
        )

        mem_generic_prior = psutil.Process(os.getpid()).memory_info().rss
        self.predictor = SamPredictorONNX(
            MainWindow=None, encoder_path=part1, decoder_path=part2
        )
        self.predictor.load_models(force_provider="CPUExecutionProvider")
        # make the difference
        mem_generic_post = psutil.Process(os.getpid()).memory_info().rss
        print(
            f"Memory difference (MB): {(mem_generic_post - mem_generic_prior) / 1024 / 1024}"
        )

        image_path = os.path.join(
            configHandle.getLocal(),
            "fixtures/daf-2_D2_aup-1i_26.tif",
        )
        self.image = cv2.imread(image_path)
        # resize image to input size
        self.image = cv2.resize(self.image, (1024, 1024))

        # specialized magic box
        # measure ram usage
        mem_generic_prior = psutil.Process(os.getpid()).memory_info().rss
        self.sdknn_tool_instance = sdknn_tool(None, load_general_model=None)
        mem_generic_post = psutil.Process(os.getpid()).memory_info().rss
        print(
            f"Memory difference (MB): {(mem_generic_post - mem_generic_prior) / 1024 / 1024}"
        )

    def test_magic_box_specialized(self):

        if memory_profiler:
            predict_method = partial(
                self.sdknn_tool_instance.get_specialized_bbox_mask,
                image=self.image,
                bounding_box=[10, 10, 1000, 1000],
                tile_bbox=[0, 0, self.image.shape[1], self.image.shape[0]],
            )
            total_runs = 3
            max_memory_usage = 0
            for run in range(total_runs):
                mem_usage = memory_usage(
                    proc=predict_method,
                    interval=0.001,
                    max_usage=True,
                    include_children=True,
                )
                if mem_usage > max_memory_usage:
                    max_memory_usage = mem_usage
            logger.info(f"Max memory usage: {max_memory_usage} MB")
        else:

            self.sdknn_tool_instance.get_specialized_bbox_mask(
                image=self.image,
                bounding_box=[10, 10, 1000, 1000],
                tile_bbox=[0, 0, self.image.shape[1], self.image.shape[0]],
            )

    # def test_magic_box_generic(self):

    #     features, _, _, _ = self.predictor.get_feature_map(self.image)
    #     points = [[100, 100], [300, 300]]  # points
    #     labels = [1, 1]
    #     if memory_profiler:
    #         predict_method = partial(
    #             self.predictor.predict,
    #             features=features,
    #             point_coords=np.array([points]),
    #             point_labels=np.array([labels]),
    #             original_size=self.image.shape[:2],
    #         )
    #         max_memory_usage = 0
    #         total_runs = 3
    #         for run in range(total_runs):
    #             mem_usage = memory_usage(
    #                 proc=predict_method,
    #                 interval=0.001,
    #                 max_usage=True,
    #                 include_children=True,
    #             )
    #             if mem_usage > max_memory_usage:
    #                 max_memory_usage = mem_usage
    #     else:
    #         masks, scores, _ = self.predictor.predict(
    #             point_coords=np.array([points]),
    #             point_labels=np.array([labels]),
    #             original_size=self.image.shape[:2],
    #         )


if __name__ == "__main__":
    unittest.main()
