import unittest
from celer_sight_ai.io.image_reader import (
    generate_complete_spiral_tiles,
    get_optimal_crop_bbox,
)
from celer_sight_ai.gui.custom_widgets.scene import readImage
import cv2
import numpy
import os


class TestSpiralTileGeneration(unittest.TestCase):
    # Class-level constants for tile dimensions and overlap
    TILE_WIDTH = 1000
    TILE_HEIGHT = 1000
    TILE_OVERLAP = 50

    def setUp(self):
        self.images_locations = [
            "tests/fixtures/image_intensity_test/green_hole.png",
            "tests/fixtures/import_images/N2_mtmKate2_150ms_10x_L1_2_2x2_5gain_Image006.tif",
        ]
        self.images = [
            cv2.imread(image_location) for image_location in self.images_locations
        ]
        self.tile_fixtures = [
            {
                "tile_size": 363.5,
                "image_size": [1024, 1024],
                "overlap": 6,
                "bbox": [0, 0, 1024, 1024],
            }
        ]
        # Define tile dimensions as instance variables
        self.tile_width = self.TILE_WIDTH
        self.tile_height = self.TILE_HEIGHT
        self.overlap = self.TILE_OVERLAP

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
        """Test the generation of spiral tiles with proper dimensions and padding."""
        from celer_sight_ai.io.image_reader import (
            generate_complete_spiral_tiles,
            crop_and_pad_image,
        )

        for fixture in self.tile_fixtures:

            # Test with each image from setUp
            for idx, image in enumerate(self.images):
                with self.subTest(image_path=self.images_locations[idx]):
                    # read image
                    image, metadata = readImage(
                        os.path.abspath(
                            os.path.join(
                                os.path.dirname(os.path.dirname(__file__)),
                                self.images_locations[idx],
                            )
                        )
                    )
                    tile_width = fixture["tile_size"]
                    tile_height = fixture["tile_size"]
                    overlap = fixture["overlap"]
                    image_center = [tile_width / 2, tile_height / 2]
                    initial_bbox = [
                        image_center[0] - (tile_width / 2),
                        image_center[1] - (tile_height / 2),
                        tile_width,
                        tile_height,
                    ]

                    # Generate tiles
                    tiles = generate_complete_spiral_tiles(
                        image.shape[1],
                        image.shape[0],
                        initial_bbox,
                        overlap=overlap,
                    )

                    # Verify each generated tile
                    for tile_idx, tile in enumerate(tiles):
                        img = crop_and_pad_image(image, tile)

                        # Assert tile dimensions
                        self.assertEqual(
                            img.shape[0],
                            self.tile_height,
                            f"Tile height mismatch for image {idx}, tile {tile_idx}",
                        )
                        self.assertEqual(
                            img.shape[1],
                            self.tile_width,
                            f"Tile width mismatch for image {idx}, tile {tile_idx}",
                        )


if __name__ == "__main__":
    unittest.main()
