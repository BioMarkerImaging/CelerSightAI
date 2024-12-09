import tifffile
import xmltodict
from glob import glob
import cv2
import numpy as np
import os
import sys
import time

import unittest

from celer_sight_ai.io.image_reader import read_specialized_image
import logging

logger = logging.getLogger(__name__)
import lzma
import lz4
import lz4.frame
import zstandard


class MyTest(unittest.TestCase):
    def setUp(self):
        self.path_images_tif = "tests/fixtures/import_images"
        self.all_images_tif = glob(self.path_images_tif + "/*.tif") + glob(
            self.path_images_tif + "/*.TIF"
        )
        self.mock_proprietory_images = {
            "tests/fixtures/tissue_files/TCGA-HC-7820-01A-01-TS1.f9131ac5-c635-42a7-a383-634d90d212d4.svs": None
        }

        self.mock_channels_tif = {
            "4D-series.ome.tif": None,
            "Cell_2.tif": ["gray"],  # z stack from png
            "multi-channel-4D-series.ome.tif": None,
            "multi-channel-time-series.ome.tif": None,
            "time-series.ome.tif": None,
            "multi-channel-z-series.ome.tif": [
                "red",
                "green",
                "blue",
            ],  # z stack from png
            "multi-channel.ome.tif": ["red", "green", "blue"],
            "N2_100x_150ms_4gain_2x2_L1_Image002.tif": ["red", "green", "blue"],
            "neuro_rosella_D2_UA.vsi - 10x_FBW, FGW_Z_22.tif": [
                np.array([255, 0, 0]),
                np.array([0, 255, 0]),
            ],
            "neuro_rosella_D2_UA.vsi - 10x_FBW, FGW_Z_23.tif": [
                np.array([255, 0, 0]),
                np.array([0, 255, 0]),
            ],
            "neuro_rosella_D2_UA.vsi - 10x_FBW, FGW_Z_24.tif": [
                np.array([255, 0, 0]),
                np.array([0, 255, 0]),
            ],
            "neuro_rosella_D2_UA.vsi - 10x_FBW, FGW_Z_25.tif": [
                np.array([255, 0, 0]),
                np.array([0, 255, 0]),
            ],
            "single-channel.ome.tif": ["gray"],
            "TMRE_D1_gsk-3_C_02.tif": ["FGW"],
            "TMRE_D1_gsk-3_C_10.tif": ["FGW"],
            "TMRE_D1_gsk-3_EGTA_Overview.tif": None,  # Dont load more than 1 image with different size for now
            "wt L1 TMRE_Image003.tif": ["red", "green", "blue"],
            "z-series.ome.tif": ["gray"],  # z stack it
            "TMRE_D1_gsk-3_UA+EGTA_06.tif": ["FGW"],
            "neuronal_rosella_D5_C_05.tif": ["FBW", "FGW"],
            "daf-2_D2_aup-1i.tif": ["red", "green", "blue"],
        }  # Specify if result is None -> false or not None -> true

        self.mock_shapes_tif = {
            "control_Bottom Slide_D_p00_0_A01f11d1.TIF": {
                "channels": ["red", "green", "blue"],
                "size_x": 2048,
                "size_y": 1536,
            },
            "4D-series.ome.tif": None,
            "Cell_2.tif": {
                "channels": ["gray"],
                "size_x": 251,
                "size_y": 449,
            },  # z stack from png
            "multi-channel-4D-series.ome.tif": None,
            "multi-channel-time-series.ome.tif": None,
            "time-series.ome.tif": None,
            "multi-channel-z-series.ome.tif": {
                "channels": ["red", "green", "blue"],
                "size_x": 439,
                "size_y": 167,
            },
            "multi-channel.ome.tif": {
                "channels": ["red", "green", "blue"],
                "size_x": 439,
                "size_y": 167,
            },
            "N2_100x_150ms_4gain_2x2_L1_Image002.tif": {
                "channels": ["red", "green", "blue"],
                "size_x": 696,
                "size_y": 520,
            },
            "neuro_rosella_D2_UA.vsi - 10x_FBW, FGW_Z_22.tif": {
                "channels": [np.array([255, 0, 0]), np.array([0, 255, 0])],
                "size_x": 1039,
                "size_y": 1444,
            },
            "neuro_rosella_D2_UA.vsi - 10x_FBW, FGW_Z_23.tif": {
                "channels": [np.array([255, 0, 0]), np.array([0, 255, 0])],
                "size_x": 1484,
                "size_y": 1009,
            },
            "neuro_rosella_D2_UA.vsi - 10x_FBW, FGW_Z_24.tif": {
                "channels": [np.array([255, 0, 0]), np.array([0, 255, 0])],
                "size_x": 1019,
                "size_y": 1672,
            },
            "neuro_rosella_D2_UA.vsi - 10x_FBW, FGW_Z_25.tif": {
                "channels": [np.array([255, 0, 0]), np.array([0, 255, 0])],
                "size_x": 1761,
                "size_y": 643,
            },
            "single-channel.ome.tif": {
                "channels": ["gray"],
                "size_x": 439,
                "size_y": 167,
            },
            "TMRE_D1_gsk-3_C_02.tif": {
                "channels": ["FGW"],
                "size_x": 2457,
                "size_y": 2457,
            },
            "TMRE_D1_gsk-3_C_10.tif": {
                "channels": ["FGW"],
                "size_x": 2457,
                "size_y": 2457,
            },
            "TMRE_D1_gsk-3_EGTA_Overview.tif": None,  # Dont load more than 1 image with different size for now
            "wt L1 TMRE_Image003.tif": {
                "channels": ["red", "green", "blue"],
                "size_x": 1392,
                "size_y": 1040,
            },
            "z-series.ome.tif": {
                "channels": ["gray"],
                "size_x": 439,
                "size_y": 167,
            },
            "TMRE_D1_gsk-3_UA+EGTA_06.tif": {
                "channels": ["FGW"],
                "size_x": 2457,
                "size_y": 2457,
            },
            "neuronal_rosella_D5_C_05.tif": {
                "channels": ["FBW", "FGW"],
                "size_x": 2457,
                "size_y": 2457,
            },
            "daf-2_D2_aup-1i.tif": {
                "channels": ["red", "green", "blue"],
                "size_x": 2740,
                "size_y": 2740,
            },
            "20211005_LHE042_plane1_-324.425_raw-092_Cycle00001_Ch1_000001.ome.tif": None,
        }  # Specify if result is None -> false or not None -> true

        self.mock_high_res_images = {
            "20211005_LHE042_plane1_-324.425_raw-092_Cycle00001_Ch1_000001.ome.tif": None,
            "CMU-1.ndpi": {
                "channels": ["red", "green", "blue"],
                "size_x": 51200,
                "size_y": 38144,
            },
            "CMU-1.tiff": {
                "channels": ["red", "green", "blue"],
                "size_x": 46000,
                "size_y": 32914,
            },
            "Philips-1.tiff": {
                "channels": ["red", "green", "blue"],
                "size_x": 45056,
                "size_y": 35840,
            },
            # "Philips-3.tiff": {
            #     "channels": ["red", "green", "blue"],
            #     "size_x": 131072,
            #     "size_y": 100352,
            # },
        }
        self.ultra_high_res_root_path = "tests/fixtures/import_images_high_res"

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
                image_path = os.path.join(self.ultra_high_res_root_path, image_name)
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
                image_path = os.path.join(self.ultra_high_res_root_path, image_name)
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
