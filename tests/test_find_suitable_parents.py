import unittest
from unittest.mock import MagicMock, patch
import numpy as np
from shapely.geometry import Polygon

from celer_sight_ai.io.data_handler import ImageObject, maskObj


class TestFindSuitableParents(unittest.TestCase):
    def setUp(self):
        self.mock_main_window = MagicMock()
        self.mock_custom_class_list_widget = MagicMock()
        self.mock_main_window.custom_class_list_widget = (
            self.mock_custom_class_list_widget
        )

        # Create ImageObject with proper initialization
        self.img_obj = ImageObject(
            MainWindow=self.mock_main_window,
            rootfile="root",
            filename="filename",
            imgIdx=0,
            image_uuid="test_image_123",
        )

        # Mock necessary methods
        self.img_obj.to_shapely = lambda x: Polygon(x[0])
        self.img_obj.bounding_boxes_overlap = lambda a, b: True
        self.img_obj.inclusion_score = lambda a, b, as_bitmaps=False: (
            0.5 if as_bitmaps else a.intersection(b).area / a.union(b).area
        )

    def create_mask(self, polygon, class_id, mask_type="polygon"):
        """Helper method to create mask objects with proper configuration"""
        mask = maskObj(
            MainWindow=self.mock_main_window,
            polygon_array=[np.array(polygon)],
            class_id=class_id,
            image_uuid=self.img_obj.unique_id,
        )
        mask.mask_type = mask_type
        mask.get_bounding_box = lambda: [0, 0, 2, 2]  # Mock bounding box
        return mask

    def test_no_parent_returns_empty_hierarchy(self):
        """Test when mask has no parent class"""
        mask_A = self.create_mask([(0, 0), (1, 0), (1, 1), (0, 1)], "class_1")
        self.mock_custom_class_list_widget.classes = {
            "class_1": MagicMock(parent_class_uuid=None)
        }

        result = self.img_obj.find_suitable_parents(mask_A, [mask_A])
        self.assertEqual(
            len(result), 0, "Should return empty list when no parent exists"
        )

    def test_bitmap_mask_handling(self):
        """Test handling of bitmap masks"""
        mask_A = self.create_mask(
            [(0, 0), (1, 0), (1, 1), (0, 1)], "class_1", mask_type="bitmap"
        )
        mask_B = self.create_mask(
            [(0, 0), (2, 0), (2, 2), (0, 2)], "class_2", mask_type="bitmap"
        )

        self.mock_custom_class_list_widget.classes = {
            "class_1": MagicMock(parent_class_uuid="class_2"),
            "class_2": MagicMock(parent_class_uuid=None),
        }

        # Mock bitmap-specific methods
        mask_A.get_array = lambda: np.ones((10, 10), dtype=bool)
        mask_B.get_array = lambda: np.ones((10, 10), dtype=bool)

        result = self.img_obj.find_suitable_parents(mask_A, [mask_A, mask_B])
        self.assertEqual(len(result), 1)
        self.assertIn(mask_B, result[0])

    def test_multiple_hierarchy_levels(self):
        """Test handling of multiple hierarchy levels with inclusion thresholds"""
        # Create a hierarchy: class_1 -> class_2 -> class_3
        masks = [
            self.create_mask([(0, 0), (1, 0), (1, 1), (0, 1)], "class_1"),  # Small
            self.create_mask([(0, 0), (2, 0), (2, 2), (0, 2)], "class_2"),  # Medium
            self.create_mask([(-1, -1), (3, -1), (3, 3), (-1, 3)], "class_3"),  # Large
        ]

        self.mock_custom_class_list_widget.classes = {
            "class_1": MagicMock(parent_class_uuid="class_2"),
            "class_2": MagicMock(parent_class_uuid="class_3"),
            "class_3": MagicMock(parent_class_uuid=None),
        }

        result = self.img_obj.find_suitable_parents(masks[0], masks)
        self.assertEqual(len(result), 2, "Should find two levels of parents")
        self.assertIn(masks[1], result[0], "First level should contain medium mask")
        self.assertIn(masks[2], result[1], "Second level should contain large mask")

    def test_threshold_filtering(self):
        """Test that masks below inclusion threshold are filtered out"""
        mask_A = self.create_mask([(0, 0), (1, 0), (1, 1), (0, 1)], "class_1")
        mask_B = self.create_mask([(10, 10), (11, 10), (11, 11), (10, 11)], "class_2")

        self.mock_custom_class_list_widget.classes = {
            "class_1": MagicMock(parent_class_uuid="class_2"),
            "class_2": MagicMock(parent_class_uuid=None),
        }

        # Mock low inclusion score for distant masks
        self.img_obj.inclusion_score = lambda a, b, as_bitmaps=False: 0.05

        result = self.img_obj.find_suitable_parents(mask_A, [mask_A, mask_B])
        self.assertEqual(len(result), 0, "Should filter out masks below threshold")

    def test_overlapping_but_non_inclusive_masks(self):
        """Test masks that overlap but don't meet inclusion criteria"""
        # Create two overlapping but mostly separate masks
        mask_A = self.create_mask([(0, 0), (2, 0), (2, 2), (0, 2)], "class_1")
        mask_B = self.create_mask([(1, 1), (3, 1), (3, 3), (1, 3)], "class_2")

        self.mock_custom_class_list_widget.classes = {
            "class_1": MagicMock(parent_class_uuid="class_2"),
            "class_2": MagicMock(parent_class_uuid=None),
        }

        # Mock low inclusion score for overlapping masks
        self.img_obj.inclusion_score = lambda a, b, as_bitmaps=False: 0.2

        result = self.img_obj.find_suitable_parents(mask_A, [mask_A, mask_B])
        self.assertEqual(len(result), 1, "Should find one level of parents")
        self.assertIn(mask_B, result[0], "Should include overlapping parent")

    def test_exact_threshold_case(self):
        """Test masks that exactly meet the inclusion threshold"""
        mask_A = self.create_mask([(0, 0), (1, 0), (1, 1), (0, 1)], "class_1")
        mask_B = self.create_mask([(0, 0), (2, 0), (2, 2), (0, 2)], "class_2")

        self.mock_custom_class_list_widget.classes = {
            "class_1": MagicMock(parent_class_uuid="class_2"),
            "class_2": MagicMock(parent_class_uuid=None),
        }

        # Mock exact threshold score
        self.img_obj.inclusion_score = (
            lambda a, b, as_bitmaps=False: 0.1
        )  # Assuming INCLUSION_THRESHOLD = 0.1

        result = self.img_obj.find_suitable_parents(mask_A, [mask_A, mask_B])
        self.assertEqual(
            len(result), 1, "Should include masks exactly meeting threshold"
        )
        self.assertIn(mask_B, result[0])

    def test_performance_with_many_masks(self):
        """Test performance with a large number of masks"""
        # Create a large number of masks
        width = 100
        height = 100
        many_masks = [
            self.create_mask(
                [(i, i), (i + width, i), (i + width, i + height), (i, i + height)],
                f"class_{i}",
            )
            for i in range(width * height)
        ]

        # Create class hierarchy
        self.mock_custom_class_list_widget.classes = {
            f"class_{i}": MagicMock(parent_class_uuid=f"class_{i+1}") for i in range(99)
        }
        self.mock_custom_class_list_widget.classes["class_99"] = MagicMock(
            parent_class_uuid=None
        )

        # Test execution time
        import time

        start_time = time.time()
        result = self.img_obj.find_suitable_parents(many_masks[0], many_masks)
        execution_time = time.time() - start_time

        self.assertLess(
            execution_time, 2.0, "Should process many masks within reasonable time"
        )
        self.assertGreater(len(result), 0, "Should find parent masks")


if __name__ == "__main__":
    unittest.main()
