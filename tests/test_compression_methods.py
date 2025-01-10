import tifffile
import xmltodict
from glob import glob
import cv2
import numpy as np
import os
import sys
import time

import unittest

from tests.base_image_testcase import BaseImageTestCase
import logging

logger = logging.getLogger(__name__)
import lzma
import lz4
import lz4.frame
import zstandard


class MyTest(BaseImageTestCase):
    def setUp(self):
        self.path_images_tif = "tests/fixtures/import_images"
        self.all_images_tif = glob(self.path_images_tif + "/*.tif") + glob(
            self.path_images_tif + "/*.TIF"
        )

    def test_ultra_high_res_compression_from_raw(self):
        import tempfile
        import time

        compression_rations = {
            "zstd": [],
            "lz4": [],
            "lzma": [],
        }
        compression_time = {
            "zstd": [],
            "lz4": [],
            # "lzma": [],
        }
        with tempfile.TemporaryDirectory() as tmpdirname:
            for image_name, image_info in self.mock_high_res_images.items():
                image_path = self.get_high_res_image_path(image_name)
                start = time.time()
                cctx = zstandard.ZstdCompressor(level=3, threads=-1)
                with open(image_path, "rb") as ifh, open(
                    tmpdirname + "/" + image_name, "wb"
                ) as ofh:
                    cctx.copy_stream(
                        ifh, ofh, read_size=1024 * 1024, write_size=1024 * 1024
                    )
                compression_time["zstd"].append(time.time() - start)
                print(f"Compressed {image_path} to {tmpdirname + '/' + image_name}")
                # append ratio
                compression_rations["zstd"].append(
                    os.path.getsize(tmpdirname + "/" + image_name)
                    / os.path.getsize(image_path)
                )
                # compress with lz4
                start = time.time()
                with open(image_path, "rb") as ifh, open(
                    tmpdirname + "/" + image_name, "wb"
                ) as ofh:
                    ofh.write(lz4.frame.compress(ifh.read()))
                compression_time["lz4"].append(time.time() - start)
                print(f"Compressed {image_path} to {tmpdirname + '/' + image_name}")
                # append ratio
                compression_rations["lz4"].append(
                    os.path.getsize(tmpdirname + "/" + image_name)
                    / os.path.getsize(image_path)
                )

            # get the mean of all ratios
            compression_rations["zstd"] = sum(compression_rations["zstd"]) / len(
                compression_rations["zstd"]
            )
            compression_rations["lz4"] = sum(compression_rations["lz4"]) / len(
                compression_rations["lz4"]
            )
            compression_time["zstd"] = sum(compression_time["zstd"]) / len(
                compression_time["zstd"]
            )
            compression_time["lz4"] = sum(compression_time["lz4"]) / len(
                compression_time["lz4"]
            )
            print(compression_time)

        import tempfile
        import time
        from celer_sight_ai.io.image_reader import (
            create_large_compressed_image_from_ultra_high_res_tiled_image,
        )

        compression_rations2 = {
            "zstd_from_jpg": [],
            "lz4_from_jpg": [],
            "jpg": [],
            # "lzma": [],
        }
        compression_time2 = {
            "zstd_from_jpg": [],
            "lz4_from_jpg": [],
            "jpg": [],
            # "lzma": [],
        }
        with tempfile.TemporaryDirectory() as tmpdirname:
            for image_name, image_info in self.mock_high_res_images.items():
                image_path = self.get_high_res_image_path(image_name)
                start = time.time()
                image_path_jpg = (
                    create_large_compressed_image_from_ultra_high_res_tiled_image(
                        image_path, temp_dir=tmpdirname, compress=False
                    )
                )
                compression_time2["jpg"].append(time.time() - start)
                print(f"Compressed {image_path} to {tmpdirname + '/' + image_name}")
                # append ratio
                compression_rations2["jpg"].append(
                    os.path.getsize(image_path_jpg) / os.path.getsize(image_path)
                )
                start = time.time()
                cctx = zstandard.ZstdCompressor(level=3, threads=-1)
                with open(image_path_jpg, "rb") as ifh, open(
                    tmpdirname + "/" + "out_" + image_name, "wb"
                ) as ofh:
                    cctx.copy_stream(
                        ifh, ofh, read_size=1024 * 1024, write_size=1024 * 1024
                    )
                compression_time2["zstd_from_jpg"].append(time.time() - start)
                print(
                    f"Compressed {image_path} to {tmpdirname + '/' + 'out_'+image_name}"
                )
                # append ratio
                compression_rations2["zstd_from_jpg"].append(
                    os.path.getsize(tmpdirname + "/" + "out_" + image_name)
                    / os.path.getsize(image_path_jpg)
                )
                # compress with lz4
                start = time.time()
                with open(image_path, "rb") as ifh, open(
                    tmpdirname + "/" + "out_" + image_name, "wb"
                ) as ofh:
                    ofh.write(lz4.frame.compress(ifh.read()))
                compression_time2["lz4_from_jpg"].append(time.time() - start)

                # append ratio
                compression_rations2["lz4_from_jpg"].append(
                    os.path.getsize(tmpdirname + "/" + "out_" + image_name)
                    / os.path.getsize(image_path_jpg)
                )

        # get the mean of all ratios
        compression_rations2["zstd_from_jpg"] = sum(
            compression_rations2["zstd_from_jpg"]
        ) / len(compression_rations2["zstd_from_jpg"])
        compression_rations2["lz4_from_jpg"] = sum(
            compression_rations2["lz4_from_jpg"]
        ) / len(compression_rations2["lz4_from_jpg"])
        compression_rations2["jpg"] = sum(compression_rations2["jpg"]) / len(
            compression_rations2["jpg"]
        )
        compression_time2["zstd_from_jpg"] = sum(
            compression_time2["zstd_from_jpg"]
        ) / len(compression_time2["zstd_from_jpg"])
        compression_time2["lz4_from_jpg"] = sum(
            compression_time2["lz4_from_jpg"]
        ) / len(compression_time2["lz4_from_jpg"])
        compression_time2["jpg"] = sum(compression_time2["jpg"]) / len(
            compression_time2["jpg"]
        )
        print(f"Compression ratios {compression_rations}")
        print(f"Compression time {compression_time}")
        print(f"Compression ratios from jpg {compression_rations2}")
        print(f"Compression time from jpg {compression_time2}")

        total_compression_ratios_jpg = {
            "zstd": compression_rations2["zstd_from_jpg"] * compression_rations2["jpg"],
            "lz4": compression_rations2["lz4_from_jpg"] * compression_rations2["jpg"],
        }
        total_compression_time_jpg = {
            "zstd": compression_time2["zstd_from_jpg"] + compression_time2["jpg"],
            "lz4": compression_time2["lz4_from_jpg"] + compression_time2["jpg"],
        }
        print(f"Total compression ratios from jpg {total_compression_ratios_jpg}")
        print(f"Total compression time from jpg {total_compression_time_jpg}")


if __name__ == "__main__":
    unittest.main()
