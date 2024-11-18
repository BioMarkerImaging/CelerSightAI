import unittest
from celer_sight_ai.QtAssets.Utilities.image_reader import (
    generate_complete_spiral_tiles,
    get_optimal_crop_bbox,
)
import cv2
import numpy


class TestImageReader(unittest.TestCase):
    # def test_get_optimal_crop_bbox(self):
    #     bbox = get_optimal_crop_bbox(1080, 1920, [100, 100, 150, 150])
    #     bbox = get_optimal_crop_bbox(17515, 17239, [8076, 9003, 8102, 9035])

    #     print()

    # def test_generate_complete_spiral_tiles(self):
    #     # Setup
    #     img_width = 2080
    #     img_height = 2920
    #     initial_bbox = get_optimal_crop_bbox(
    #         img_width, img_height, [700, 700, 750, 750]
    #     )  # bbox is [x1 , y1, x2, y2]
    #     print(initial_bbox)
    #     overlap = 50
    #     # generate_complete_spiral_tiles(img_width, img_height, initial_bbox, overlap)
    #     # generate_complete_spiral_tiles(1303, 2048, (0, 294.625, 1418.75, 1418.75), 135)
    #     # generate_complete_spiral_tiles(3230, 1860, [1147.25, 122.25, 437.5, 437.5], 42)
    #     generate_complete_spiral_tiles(
    #         2048, 1152, [308.625, 45.125, 993.75, 993.75], 94
    #     )
    #     # tiles = generate_complete_spiral_tiles(
    #     #     1202, 2048, (0, 643.125, 1404.875, 1404.875), 140
    #     # )
    #     # assert len(tiles) == 3

    #     # generate_complete_spiral_tiles(img_width, img_height, initial_bbox, overlap)

    def test_generate_complete_spiral_tiles_2(self):
        from celer_sight_ai.QtAssets.Utilities.image_reader import (
            generate_complete_spiral_tiles,
            crop_and_pad_image,
        )
        import time

        image_location = "tests/fixtures/image_intensity_test/green_hole.png"
        image_location = "tests/fixtures/9b0989ac-2a31-4b1b-af0f-cbffbb504a91.png"
        image = cv2.imread(image_location)

        image_center = [image.shape[1] // 2, image.shape[0] // 2]
        tile_width = 1280
        tile_height = 1280
        image_height = image.shape[0]
        image_width = image.shape[1]
        initial_bbox = [
            image_center[0] - (tile_width // 2),
            image_center[1] - (tile_height / 2),
            tile_width,
            tile_height,
        ]
        # [272.0, 96.0, 1280.0, 1280.0]
        tiles = generate_complete_spiral_tiles(
            image.shape[1], image.shape[0], initial_bbox, 50
        )
        for tile in tiles:
            img = crop_and_pad_image(image, tile)
            cv2.imwrite("test.jpg", img)
            assert img.shape[0] == tile_height
            assert img.shape[1] == tile_width
            time.sleep(0.5)
        print()


if __name__ == "__main__":
    unittest.main()
