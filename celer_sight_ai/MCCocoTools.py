import sys

import os
from celer_sight_ai import config


if config.is_executable:
    sys.path.append([str(os.environ["CELER_SIGHT_AI_HOME"])])
# MC COCO tools

import logging

logger = logging.getLogger(__name__)


def BitToPoly(BitImage):
    import cv2
    import numpy as np

    if np.amax(BitImage) == 1:
        BitImage = BitImage * 255
    retval, BitImage1 = cv2.threshold(BitImage, 127, 255, 0)
    contours, hierarchy = cv2.findContours(
        BitImage1, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE
    )
    xArray = []
    yArray = []
    for i in range(len(contours[0])):
        xArray.append(int(contours[0][i][0][0]))
        yArray.append(int(contours[0][i][0][1]))
    return xArray, yArray


def PolyToBit(pointsy, pointsx, Image):
    from skimage.draw import polygon
    import numpy as np

    mask = np.zeros((Image.shape[0], Image.shape[1]), dtype=bool)
    if type(pointsx) == int:
        if pointsx == -1:
            return
    rr, cc = polygon(pointsy, pointsx)
    mask[rr, cc] = True
    return mask[:, :]


def apply_mask_simple(image, mask):
    """
    Draws mask on image
    """
    import numpy as np
    import cv2

    redImg = np.zeros(image.shape, image.dtype)
    color = [0, 255, 255]
    redImg[:, :] = color
    redMask = cv2.bitwise_and(redImg, redImg, mask=mask.astype(np.uint8))
    redMask = cv2.addWeighted(redMask, 0.2, image, 1, 0, image)
    return redMask


def DisplayWorm(pointsy, pointsx, Image):
    BoolImage = PolyToBit(pointsy, pointsx, Image)
    image = apply_mask_simple(Image, BoolImage)
    return image


if __name__ == "__main__":
    import cv2
    import numpy as np

    # BitImage= cv2.imread("J:/data/elegans/body_stracture/whole_body/artificial_data/results/masks/_20200219-192826_7928/1.jpg")
    # BitImage = cv2.cvtColor(BitImage, cv2.COLOR_BGR2GRAY)
    # BitToPoly(BitImage)
