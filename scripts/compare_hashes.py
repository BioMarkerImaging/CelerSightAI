import os
import sys
import celer_sight_ai

from celer_sight_ai.io.image_reader import standardize_and_hash_image


source_image_1 = (
    "/Users/mchaniotakis/Downloads/5629957d-9d36-42c4-92ab-c4e6cb207267.jpg"
)
source_image_2 = "/Users/mchaniotakis/Downloads/test_image_hash.TIF"
TARGET_SIZE = (256, 256)
hashed_image_1, hash_aslgorithm = standardize_and_hash_image(
    source_image_1, TARGET_SIZE=TARGET_SIZE, to_jpg=False
)
hashed_image_2, hash_algorithm = standardize_and_hash_image(
    source_image_2, TARGET_SIZE=TARGET_SIZE, to_jpg=True
)

print(hashed_image_1, hashed_image_2)
print()
