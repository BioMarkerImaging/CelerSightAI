import requests
import sys
import os
from typing import List, Tuple

# sys.path.append(os.environ["CELER_SIGHT_AI_HOME"])
from celer_sight_ai import config

from celer_sight_ai import configHandle
from celer_sight_ai.configHandle import *
from celer_sight_ai.core.LogTool import LogInHandler
import unittest
from celer_sight_ai.gui.lib import FileClient

# from tests.csight_test_loader import tags
from celer_sight_ai.configHandle import getServerAddress, getServerLogAddress
import logging
from requests.exceptions import ConnectionError, HTTPError, Timeout
import json
from parameterized import parameterized

p = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
import dotenv
import cv2
import time

# load env vars
dotenv.load_dotenv(os.path.join(p, ".env"))
# from celer_sight_ai.gui.net.errors import AuthenticationError
from parameterized import parameterized

logger = logging.getLogger(__name__)

unittest.TestLoader.sortTestMethodsUsing = None

import concurrent.futures
import random
from tqdm import tqdm


class MyTest(unittest.TestCase):
    def setUp(self):
        self.mock_credentials = []
        if os.environ.get("USERNAME_ADMIN") and os.environ.get("PASSWORD_ADMIN"):
            self.mock_credentials.append(
                (os.environ.get("USERNAME_ADMIN"), os.environ.get("PASSWORD_ADMIN"))
            )
        # log user
        self.client = FileClient(getServerAddress())
        self.client.login(*self.mock_credentials[0])

    # @parameterized.expand(
    #     [
    #         # ("tests//fixtures//inference_test_items//worm_plate.png",
    #         # "on_plate",
    #         # ["0888765f-f214-4e24-8cc6-c92735d03e68"]
    #         # ),
    #         # (
    #         #     "tests//fixtures//inference_test_items//worm_celegans_whole_body.png",
    #         #     "worms",
    #         #     ["0888765f-f214-4e24-8cc6-c92735d03e68"],  # body
    #         # ),
    #         (
    #             "tests//fixtures//inference_test_items//tissue_1.jpg",
    #             "tissue",
    #             ["54639-a30491da-528b-4546-9eb4-b6ecc3c6e035"],  # tissue cell
    #         ),
    #         (
    #             "tests//fixtures//inference_test_items//tissue_1.jpg",
    #             "cells",
    #             ["58f00d07-caa7-4bec-8a66-39432f2e1086"],  # cell
    #         ),
    #         # ("tests//fixtures//inference_test_items//worm_celegans_whole_body.png",
    #         # "worms",
    #         # ["ba2d0d66-0bb3-4a8f-b8a3-3a349e7c2ae2"] # head
    #         # ),
    #     ]
    #     # ("tests//fixtures//inference_test_items//cyto_test.png",
    #     # "cell",
    #     # ["cytoplasm"])
    #     # ],
    # )
    # def test_inference(self, image_url, supercategory, class_names):
    #     """
    #     Sends annotation to the server, and checks responce
    #     """
    #     from celer_sight_ai import configHandle, config
    #     import time

    #     image_path = os.path.join(p, image_url)
    #     img_data = cv2.imread(image_path)

    #     # enconde image to jpg
    #     img_encoded = cv2.imencode(".jpg", img_data)[1]
    #     send_image_inference_url = configHandle.get_send_image_inference_address()
    #     retrieve_inference_data_url = configHandle.retrieve_inference_data_address()
    #     start = time.time()
    #     resp = self.client.session.post(
    #         send_image_inference_url,
    #         data={
    #             "json": json.dumps(
    #                 {
    #                     "inference_user_settings": (
    #                         "settings.json",
    #                         None,
    #                         "application/json",
    #                     ),
    #                     "supercategory": supercategory,
    #                     "class_names": class_names,
    #                 }
    #             )
    #         },
    #         files={
    #             "data": ("image.png", img_encoded.tostring(), "image/png"),
    #         },
    #         timeout=60,
    #     )
    #     resp.raise_for_status()
    #     request_id = resp.json()["request_id"]
    #     print()
    #     import time

    #     start_time = time.time()
    #     timeout = 60  # 10 seconds timeout

    #     while True:
    #         try:
    #             result = self.client.retrieve_inference_data([request_id])
    #             if not result["completed_inference"]:
    #                 print("waiting for inference results")
    #                 time.sleep(0.5)
    #                 if time.time() - start_time > timeout:
    #                     raise TimeoutError(
    #                         "Inference took too long (more than 10 seconds)"
    #                     )
    #                 continue
    #             break
    #         except TimeoutError as e:
    #             print(f"Error: {e}")
    #             raise
    #         except Exception as e:
    #             print(e)

    #     print(f"Took {time.time() - start} seconds")
    #     print()
    #     import numpy as np
    #     import copy

    #     # draw the segmentation on the image
    #     tmp_image_data = copy.deepcopy(img_data)
    #     for item in result["completed_inference"]:
    #         # sort result["completed_inference"] by confidence
    #         # item["result"] = sorted(item["result"], key=lambda x: x["confidence"], reverse=True)
    #         for i in range(len(item["result"])):

    #             # Convert segmentation to contour
    #             segmentation = (
    #                 np.array(item["result"][i]["segmentation"][0])
    #                 .reshape((-1, 2))
    #                 .astype(np.int32)
    #             )

    #             # Draw the contour on the image
    #             tmp_image_data = cv2.drawContours(
    #                 tmp_image_data, [segmentation], 0, (0, 255, 0), 2
    #             )

    #             # Add label with class name and confidence
    #             class_name = item["result"][i]["class"]
    #             confidence = item["result"][i]["confidence"]
    #             label = f"{class_name}: {confidence:.2f}"

    #             # Get top-left corner of bounding box for label placement
    #             # x, y = segmentation.min(axis=0)

    #             # Put text on the image
    #             # cv2.putText(tmp_image_data, label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
    #         cv2.imwrite("test.jpg", tmp_image_data)
    #         print(result)

    def test_inference_stress(self, total_requests_per_user=20, users=10, timeout=420):
        """
        Stress test the inference server with multiple concurrent requests.

        Args:
            total_requests_per_user (int): Total number of requests to send per user
            max_concurrent (int): Maximum number of concurrent requests
            timeout (int): Timeout in seconds for each request
        """
        # # Test image paths and their corresponding settings

        test_image_path = (
            "tests//fixtures//inference_test_items//worm_celegans_whole_body.png"
        )
        # get all available categories for user
        categories = [
            {
                "supercategory": i.get("supercategory"),
                "classes": i.get("classes", [{}])[0].get("uuid", None),
                "image_path": test_image_path,
            }
            for i in config.cloud_categories
        ]
        # dont test categories if there are no model for them
        categories = [i for i in categories if i["classes"] is not None]
        # categories
        print(categories)

        def process_single_request(test_case):
            try:
                image_path = os.path.join(p, test_case["image_path"])
                img_data = cv2.imread(image_path)
                img_encoded = cv2.imencode(".jpg", img_data)[1]

                # Send inference request
                resp = self.client.session.post(
                    configHandle.get_send_image_inference_address(),
                    data={
                        "json": json.dumps(
                            {
                                "inference_user_settings": (
                                    "settings.json",
                                    None,
                                    "application/json",
                                ),
                                "supercategory": test_case["supercategory"],
                                "class_names": test_case["class_names"],
                            }
                        )
                    },
                    files={
                        "data": ("image.png", img_encoded.tostring(), "image/png"),
                    },
                    timeout=timeout,
                )
                resp.raise_for_status()
                return {
                    "success": True,
                    "request_id": resp.json()["request_id"],
                    "start_time": time.time(),
                }

            except Exception as e:
                return {"success": False, "error": str(e), "request_id": None}

        def check_completion_status(request_ids):
            try:
                result = self.client.retrieve_inference_data(request_ids)
                completed = []
                pending = []

                for request_id in request_ids:
                    if any(
                        inf["inference_id"] == request_id
                        for inf in result.get("completed_inference", [])
                    ):
                        completed.append(request_id)
                    else:
                        pending.append(request_id)

                return completed, pending
            except Exception as e:
                logger.error(f"Error checking completion status: {e}")
                return [], request_ids

        num_requests = total_requests_per_user * users
        max_concurrent = users * 6
        print(f"Running {num_requests} requests with {max_concurrent} concurrent users")

        results = []
        start_time = time.time()
        with concurrent.futures.ThreadPoolExecutor(
            max_workers=max_concurrent
        ) as executor:
            futures = []
            for _ in range(num_requests):
                test_case = random.choice(test_cases)
                futures.append(executor.submit(process_single_request, test_case))

            for future in tqdm(
                concurrent.futures.as_completed(futures), total=num_requests
            ):
                results.append(future.result())

        # Print statistics
        successful_requests = [r for r in results if r["success"]]
        failed_requests = [r for r in results if not r["success"]]
        print(results)

        print(f"\nStress Test Results:")
        print(f"Total Requests: {num_requests}")
        print(f"Successful: {len(successful_requests)}")
        print(f"Failed: {len(failed_requests)}")

        # Track and display inference retrieval progress
        print("\nRetrieving inference results...")
        start_time = time.time()
        pending = [r["request_id"] for r in successful_requests]
        total_requests = len(pending)

        while True:
            completed, pending = check_completion_status(pending)
            completed_count = total_requests - len(pending)
            print(
                f"Progress: {completed_count}/{total_requests} requests completed",
                end="\r",
            )

            if not pending:
                print("\nAll inference requests completed successfully!")
                break

            if time.time() - start_time > timeout:
                remaining = len(pending)
                raise TimeoutError(
                    f"Inference timeout after {timeout}s. {remaining} requests incomplete."
                )
            time.sleep(1)

        if failed_requests:
            print("\nFailed Request Errors:")
            for r in failed_requests:
                print(f"- {r['error']}")

        print(
            f"\nTotal inference processing time: {time.time() - start_time:.2f} seconds"
        )
        print(
            f"Average time per request: {(time.time() - start_time)/total_requests:.2f} seconds"
        )


if __name__ == "__main__":
    unittest.main()
