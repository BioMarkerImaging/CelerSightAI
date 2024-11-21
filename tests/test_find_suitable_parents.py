import unittest
from unittest.mock import MagicMock, patch
import numpy as np
from shapely.geometry import Polygon

# Import the necessary classes and functions
from celer_sight_ai.io.data_handler import ImageObject, maskObj


class TestFindSuitableParents(unittest.TestCase):

    def setUp(self):
        # Create a mock MainWindow and custom_class_list_widget
        self.mock_main_window = MagicMock()
        self.mock_custom_class_list_widget = MagicMock()
        self.mock_main_window.custom_class_list_widget = (
            self.mock_custom_class_list_widget
        )

        # Create an ImageObject instance
        self.img_obj = ImageObject(self.mock_main_window, "root", "filename")

        # Mock the to_shapely method
        self.img_obj.to_shapely = lambda x: Polygon(x[0])

        # Mock the iou method
        self.img_obj.iou = lambda a, b: a.intersection(b).area / a.union(b).area

    def create_mask(self, polygon, class_id):
        mask = maskObj(self.mock_main_window, [np.array(polygon)], class_id=class_id)
        mask.get_array_for_storing = lambda: [np.array(polygon)]
        return mask

    def test_no_parent(self):
        # Test case where the mask has no parent
        mask_A = self.create_mask([(0, 0), (1, 0), (1, 1), (0, 1)], "class_1")
        self.mock_custom_class_list_widget.classes = {
            "class_1": MagicMock(parent_class_uuid=None)
        }

        result = self.img_obj.find_suitable_parents(mask_A, [mask_A])
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0], mask_A)

    def test_single_parent(self):
        # Test case where the mask has a single parent
        mask_A = self.create_mask([(0, 0), (1, 0), (1, 1), (0, 1)], "class_1")
        mask_B = self.create_mask([(0, 0), (2, 0), (2, 2), (0, 2)], "class_2")
        self.mock_custom_class_list_widget.classes = {
            "class_1": MagicMock(parent_class_uuid="class_2"),
            "class_2": MagicMock(parent_class_uuid=None),
        }

        result = self.img_obj.find_suitable_parents(mask_A, [mask_A, mask_B])
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0], mask_A)
        self.assertEqual(result[1], mask_B)

    def test_multiple_parents(self):
        # Test case where the mask has multiple levels of parents
        mask_A = self.create_mask([(0, 0), (1, 0), (1, 1), (0, 1)], "class_1")
        mask_B = self.create_mask([(0, 0), (2, 0), (2, 2), (0, 2)], "class_2")
        mask_C = self.create_mask([(-1, -1), (3, -1), (3, 3), (-1, 3)], "class_3")
        self.mock_custom_class_list_widget.classes = {
            "class_1": MagicMock(parent_class_uuid="class_2"),
            "class_2": MagicMock(parent_class_uuid="class_3"),
            "class_3": MagicMock(parent_class_uuid=None),
        }

        result = self.img_obj.find_suitable_parents(mask_A, [mask_A, mask_B, mask_C])
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0], mask_A)
        self.assertEqual(result[1], mask_B)
        self.assertEqual(result[2], mask_C)

    def test_multiple_parent_candidates(self):
        # Test case where there are multiple parent candidates
        mask_A = self.create_mask([(0, 0), (1, 0), (1, 1), (0, 1)], "class_1")
        mask_B1 = self.create_mask([(0, 0), (2, 0), (2, 2), (0, 2)], "class_2")
        mask_B2 = self.create_mask(
            [(0.5, 0.5), (1.5, 0.5), (1.5, 1.5), (0.5, 1.5)], "class_2"
        )
        self.mock_custom_class_list_widget.classes = {
            "class_1": MagicMock(parent_class_uuid="class_2"),
            "class_2": MagicMock(parent_class_uuid=None),
        }

        result = self.img_obj.find_suitable_parents(mask_A, [mask_A, mask_B1, mask_B2])
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0], mask_A)
        self.assertEqual(result[1], mask_B1)  # B1 should be chosen as it has higher IoU

    def test_no_suitable_parent(self):
        # Test case where there's a parent class but no suitable parent mask
        mask_A = self.create_mask([(0, 0), (1, 0), (1, 1), (0, 1)], "class_1")
        mask_B = self.create_mask([(10, 10), (11, 10), (11, 11), (10, 11)], "class_2")
        self.mock_custom_class_list_widget.classes = {
            "class_1": MagicMock(parent_class_uuid="class_2"),
            "class_2": MagicMock(parent_class_uuid=None),
        }

        result = self.img_obj.find_suitable_parents(mask_A, [mask_A, mask_B])
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0], mask_A)


if __name__ == "__main__":
    unittest.main()
