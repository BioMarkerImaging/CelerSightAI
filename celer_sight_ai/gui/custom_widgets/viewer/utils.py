import logging
import mimetypes

import cv2
import numpy as np

logger = logging.getLogger(__name__)


def is_video_file(filename):
    # Guess the type of a file based on its filename
    filetype, _ = mimetypes.guess_type(filename)

    # Check if the file type is a video
    return filetype is not None and filetype.startswith("video/")


def get_jpeg_memory_size(output_image_size, jpeg_quality, batch=1):
    # returns in mb
    # create a random image to encode
    image = np.random.randint(
        0, 256, (output_image_size[1], output_image_size[0], 3), dtype=np.uint8
    )

    # encode the image using cv2.imencode
    _, encoded_img = cv2.imencode(
        ".jpg", image, [int(cv2.IMWRITE_JPEG_QUALITY), jpeg_quality]
    )

    # calculate the size of the encoded image in bytes
    memory_size = len(encoded_img)

    return (batch * memory_size) / 1_000_000


def image_to_uint8(image, min_val, max_val):
    """
    > The function takes an image, a maximum value, and a minimum value, and returns an image with
    values scaled to the range [0, 255]

    Args:
      image: The image to be converted.
      max_val: The maximum value of the image.
      min_val: The minimum value of the image.

    Returns:
      The image is being returned as a uint8 array.
    """
    diff_val = max_val - min_val
    image = image - min_val
    return ((image / diff_val) * 255).astype(np.uint8)


def map_value_to_dtype(value: float = 0.5, dtype=np.uint8):
    """
    Given a value in the range between 0-1
    calculate the int value from the dtype.
    ex. given 0.5 and np.uint8, return 128
    Parameters:
    - value : float : value between 0-1
    - dtype : numpy.dtype : dtype to convert to

    Returns:
    - int : value in the dtype

    """
    if value < 0 or value > 1:
        logger.warning("Value must be between 0 and 1, cliping")
        value = np.clip(value, 0, 1)
    return np.iinfo(dtype).max * value
