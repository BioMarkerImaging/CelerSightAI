import logging
import os
import sys
import time
import unittest
from glob import glob

import cv2
import numpy as np
import tifffile
import xmltodict

from celer_sight_ai import config

logger = logging.getLogger(__name__)


path_images = "tests/fixtures/import_images"
all_images = glob(path_images + "/*.tif")
from celer_sight_ai.config import DEEPZOOM_TILE_SIZE


def get_tif_tags(tag_vals):
    tif_tags = {}
    for tag in tag_vals:
        name, value = tag.name, tag.value
        tif_tags[name] = value
    return tif_tags


def get_description_metadata(tif_tags):
    if "ImageDescription" not in tif_tags:
        print("No ImageDescription tag")
    desc = xmltodict.parse(tif_tags["ImageDescription"])
    if "OME" not in desc:
        print("No OME tag")

    return


def getImage(
    image_object,
    to_uint8: bool = True,
    to_rgb=True,
    do_channel_filter=False,  # wether to apply the filter or not
    channel_names_to_filter=None,  # channels to filter
    fast_load_ram=False,  # load image quickly from config.ram_image, used in brightness adjustment
    for_interactive_zoom=False,  # When loading a viewport array, use tricks to load it faster
    for_thumbnail=False,
    bbox=None,  # use bounding box to extract only a portion of the image [x,y,w,h]
    avoid_loading_ultra_high_res_arrays_normaly=False,
    applied_threshold=None,  # Value is out of 0-1 to map between uint8 and uint16 values easily
    # bbox is [x,y,w,h]
):
    from celer_sight_ai import config

    logger.debug(f"Getting image {image_object.fileName} with getImage")
    # if its on ram, jusrt return that
    start = time.time()
    result_dict = {}
    if image_object.onRam or isinstance(image_object.image, (np.ndarray, np.generic)):
        # case image is on ram or is remote image object and its loaded already
        if bbox:
            image = image_object.image[
                bbox[1] : bbox[1] + bbox[3], bbox[0] : bbox[0] + bbox[2]
            ]
        return image
    else:
        if not fast_load_ram:
            logger.debug(f"Loading {image_object.fileName} from disk.")
            # load normal
            from celer_sight_ai.gui.custom_widgets.scene import readImage

            image_path = None
            if for_thumbnail or for_interactive_zoom and image_object._is_pyramidal:
                # if the image is pyramidal, get the pyramidal image path instead of the original
                image_path = image_object.get_pyramidal_path()
            if not image_path:
                image_path = image_object.get_path()
            if (
                "celer_sight_ai:" in image_object.get_path()
                and image_object._is_ultra_high_res
            ):
                # ultra high resolution images need to be downloaded first, and then loaded
                logger.debug(f"Still loading remote image {image_object.fileName}")
                return None
            im, result_dict = readImage(
                image_path,
                for_interactive_zoom=for_interactive_zoom,
                for_thumbnail=for_thumbnail,
                bbox=bbox,
                avoid_loading_ultra_high_res_arrays_normaly=avoid_loading_ultra_high_res_arrays_normaly,
                is_pyramidal=image_object._is_pyramidal,  # once the image is pyramidal, we load it with openslide / tiffslide
                applied_threshold=applied_threshold,  # if its ultra high res + scene load, load the view with the tresholded image
            )
            if result_dict == {}:
                return None
            # if the image needs downloading first, download it
            if result_dict.get("is_remote", False):
                from celer_sight_ai import config

                # download thumbnail and use that for now, right after set the high quality image for download
                result_dict = config.client.get_remote_image(
                    image_object.get_path(), quality="low"
                )
                config.global_signals.download_remote_image_signal.emit(image_object)
                return result_dict["image_data"]
            if (
                result_dict.get("needs_pyramidal_conversion", False)
                and avoid_loading_ultra_high_res_arrays_normaly is True
                and for_thumbnail is True
                and for_interactive_zoom is False
                and result_dict.get("is_remote", False)
            ):
                from celer_sight_ai import config

                # Case where we are loading the thumbnail for the button during the first time
                # This means that if the .tif file is ultra high res, we need to start the conversion
                # to .svs . If the file is converted, this path would not be used.
                config.global_signals.download_remote_image_signal.emit(image_object)
                return
            elif result_dict.get("needs_pyramidal_conversion", True):
                # first ,set the image on the viewer as the preview image until the tiles start generating
                from celer_sight_ai import config

                config.global_signals.create_pyramidal_tiff_for_image_object_signal.emit(
                    image_object
                )

            channels = result_dict["channels"]

            if isinstance(image_object.SizeX, type(None)):
                image_object.SizeX = result_dict["size_x"]
                image_object.SizeY = result_dict["size_y"]

            # check for ultrahigh res
            image_object.check_and_apply_is_ultra_high_res()

            if not for_interactive_zoom:
                # case when the user is updating the viewport,
                # we dont need to record the variables again, they have
                # already been stored when this method runs for thumbnail
                if result_dict["is_ultra_high_res"]:
                    # enable ultra high res proccessing
                    image_object._is_ultra_high_res = True
                if image_object.SizeX is None:
                    image_object.SizeX = result_dict["size_x"]
                if image_object.SizeY is None:
                    image_object.SizeY = result_dict["size_y"]
                if image_object.PhysicalSizeX is None:
                    image_object.PhysicalSizeX = result_dict.get(
                        "physical_pixel_size_x", None
                    )
                if image_object.PhysicalSizeY is None:
                    image_object.PhysicalSizeY = result_dict.get(
                        "physical_pixel_size_y", None
                    )
                if image_object.PhysicalSizeXUnit is None:
                    image_object.PhysicalSizeXUnit = result_dict.get(
                        "physical_pixel_size_x_unit", "μm"
                    )
                if image_object.PhysicalSizeYUnit is None:
                    image_object.PhysicalSizeYUnit = result_dict.get(
                        "physical_pixel_size_y_unit", "μm"
                    )

                if channels:
                    image_object.channel_list = channels

            if isinstance(im, type(None)):
                return None
        elif fast_load_ram and image_object._is_ultra_high_res:
            logger.debug("Loading fast ultra high res")
            # load normal
            from celer_sight_ai.gui.custom_widgets.scene import readImage

            im, result_dict = readImage(
                image_object.get_path(),
                for_interactive_zoom=for_interactive_zoom,
                for_thumbnail=for_thumbnail,
                bbox=bbox,
                avoid_loading_ultra_high_res_arrays_normaly=avoid_loading_ultra_high_res_arrays_normaly,
                is_pyramidal=image_object._is_pyramidal,
                channel_names_to_filter=channel_names_to_filter,  # TODO: add support for channels on WSI
            )
        else:
            from celer_sight_ai import config

            im = image_object.load_current_ram_image(bbox)
        if isinstance(im, type(None)) or im.shape[0] == 0 or im.shape[1] == 0:
            return None

        image_channels = image_object.channel_list
        if isinstance(image_channels, type(None)):
            image_channels = result_dict.get("channels")
        im, min_val, max_val = post_proccess_image(
            im,
            image_channels,
            to_uint8=to_uint8,
            to_rgb=to_rgb,
            has_min_max=image_object.raw_image_extrema_set,
            min_val=image_object.raw_image_min_value,
            max_val=image_object.raw_image_max_value,
        )
        if isinstance(im, type(None)):
            return None
        if to_uint8 and not bbox:
            # (bbox) cant infer min and max when the image is cropped.
            image_object.raw_image_min_value = True
            image_object.raw_image_min_value = min_val
            image_object.raw_image_max_value = max_val

        if image_object and result_dict.get("channels"):
            # assign channnels
            logger.debug(
                f"Assigning channels {result_dict['channels']} to image {image_object.fileName}"
            )
            image_object.channel_list = result_dict["channels"]
        # filter channels
        if do_channel_filter:
            if (
                not isinstance(channel_names_to_filter, type(None))
                and len(channel_names_to_filter) == 0
            ):
                # return a blank images
                im = np.zeros_like(im)
            else:
                im = filter_channels(
                    im, image_object, channel_names_to_filter, to_rgb=to_rgb
                )
                if to_rgb:
                    channel_names_with_colors = (
                        image_object.get_channel_name_and_colors()
                    )
                    channel_names_with_colors = {
                        i: channel_names_with_colors[i] for i in channel_names_to_filter
                    }
                    im = colorize_image(im, channel_names_with_colors)

        logger.debug(
            f"Time taken to read image: {time.time() - start} at size {im.shape }"
        )

        return im  # only need the image (index 0) since we have already recorded the channels


def colorize_image(
    source_image, channel_names_with_colors: dict[str, tuple[int, int, int]]
) -> np.ndarray:
    source_dtype = source_image.dtype
    destination_image = np.zeros(
        [source_image.shape[0], source_image.shape[1], 3],
        dtype=np.float32,
    )
    if not len(source_image.shape) == 2:
        assert (
            len(channel_names_with_colors) == source_image.shape[2]
        ), "The number of channel colors must match the number of channels in the source image"
    else:
        source_image = np.stack((source_image,) * 3, axis=-1)

        assert (
            len(channel_names_with_colors) == 1
        ), "The number of channel colors must be 1 for a single channel image"
    weight_per_channel = 1 / len(channel_names_with_colors)
    # get min max per channel
    min_max_per_channel = {}
    for i, channel_name in enumerate(channel_names_with_colors):
        channel_color = channel_names_with_colors[channel_name]
        min_val = np.min(source_image[:, :, i])
        max_val = np.max(source_image[:, :, i])
        min_max_per_channel[channel_name] = (min_val, max_val)

        # scale the channel to 0-255, handling uniform intensity case
        if max_val > min_val:  # Only normalize if there's a range
            source_image_channel = (source_image[:, :, i] - min_val) / (
                max_val - min_val
            )
        else:
            # For uniform intensity, use the value directly (normalized to 0-1)
            source_image_channel = np.full_like(
                source_image[:, :, i], min_val / max(min_val, 1)
            )

        destination_image += (
            np.stack((source_image_channel,) * 3, axis=-1)
            * channel_color
            * weight_per_channel
        )
    # scale the image to 0-255
    destination_image_max = np.max(destination_image)
    destination_image_min = np.min(destination_image)
    destination_image = (destination_image - destination_image_min) / (
        destination_image_max - destination_image_min
    )
    destination_image = destination_image * 255

    return destination_image.astype(source_dtype)


def filter_channels(
    image: np.ndarray,
    image_object,
    channel_names_to_filter: list[str],
    to_rgb: bool = True,
):
    """
    Filters the channels from an image, channel
    Parameters:
    - image: The image to filter
    - image_object: The image object
    - channel_names_to_filter: The channel names to filter

    Returns:
    - image: The filtered image
    """
    channel_list_lower = [
        config.ch_as_str(i).lower() for i in image_object.channel_list
    ]
    channel_names_to_filter_lower = [i.lower() for i in channel_names_to_filter]
    # Get the channel indices
    channel_indices = [
        channel_list_lower.index(channel) for channel in channel_names_to_filter_lower
    ]
    # Filter the channels
    if len(image.shape) == 3:
        image = image[:, :, channel_indices]
    return image


def post_proccess_image(
    image,
    channel_list,
    to_uint8,
    to_rgb,
    has_min_max=False,
    min_val=None,
    max_val=None,
):
    if isinstance(channel_list, type(None)):
        return image, None, None
    if to_rgb:
        # TODO: add a more sophisticated method for this conversion
        image = combine_channels(image, channel_list)
    if to_uint8 and not image.dtype == np.uint8:
        if not has_min_max:
            min_val = np.min(image)
            max_val = np.max(image)

        diff_val = max_val - min_val
        image = (((image - min_val) / diff_val) * 255).astype(np.uint8)
    return image, min_val, max_val


def channel_to_color(channel_var):
    # channel_var can be either a string or a a numpy array rgb value
    # converts microscope channel to a emmision color
    from celer_sight_ai import config

    if isinstance(channel_var, list):
        return channel_var

    if channel_var.lower() in config.channel_colors.keys():
        return config.channel_colors[channel_var.lower()]
    else:
        return [255, 255, 255]


def combine_channels(array, channel_colors):
    # if array.shape[2] != len(channel_colors):
    #     raise ValueError("The number of channel colors must match the number of channels in the input array.")
    original_dtype = array.dtype
    if len(array.shape) == 2:
        # for images with no 1 single channel, we need to add a dimension
        array = np.stack((array,) * 3, axis=-1)

    # Initialize a new array with the same dimensions as the input array, but with 3 channels for RGB
    combined = np.zeros((array.shape[0], array.shape[1], 3), dtype=np.float32)

    if isinstance(channel_colors, type(None)) and array.shape[2] == 3:
        channel_colors = ["red", "green", "blue"]
    if isinstance(channel_colors, type(None)) and array.shape[2] == 4:
        channel_colors = ["red", "green", "blue", "alpha"]

    if not (
        len(channel_colors) == 3
        and set(channel_colors) == set(["red", "green", "blue"])
    ) and not (
        len(channel_colors) == 4
        and set(channel_colors) == set(["red", "green", "blue", "alpha"])
    ):
        # Iterate through the channels of the input array
        for i, color in enumerate(channel_colors):
            # Multiply the channel with the corresponding RGB value and add it to the combined array
            if isinstance(color, str):
                color = channel_to_color(color)
            color = np.array(color) / 255
            # Handle alpha channel separately
            if len(color) == 4:  # RGBA color
                alpha = color[3]
                combined[:, :, 0] += array[:, :, i] * color[0] * alpha
                combined[:, :, 1] += array[:, :, i] * color[1] * alpha
                combined[:, :, 2] += array[:, :, i] * color[2] * alpha
            else:  # RGB color
                combined[:, :, 0] += array[:, :, i] * color[0]
                combined[:, :, 1] += array[:, :, i] * color[1]
                combined[:, :, 2] += array[:, :, i] * color[2]
    else:
        combined = array
        # If RGBA, only keep RGB channels
        if combined.shape[-1] == 4:
            combined = combined[:, :, :3]
    return combined


def remove_at_symbol(dictionary):
    new_dict = {}
    if isinstance(dictionary, list):
        for i in range(len(dictionary)):
            new_dict = remove_at_symbol(dictionary[i])

    elif isinstance(dictionary, dict):
        for key, value in dictionary.items():
            if key.startswith("@"):
                new_key = key.lstrip("@")
            else:
                new_key = key
            if isinstance(value, dict) or isinstance(value, list):
                new_dict[new_key] = remove_at_symbol(value)
            else:
                new_dict[new_key] = value
    return new_dict


def get_tif_rgb_channe_imageJ_from_metadata(tif_metadata, channel):
    # if isinstance("channels", list):
    #     for ch in tif_metadata["channels"]:
    #         if ch["name"] == channel:
    #             return ch["color"]")

    return None


def max_projection(input_array, axis):
    if "z" not in axis.lower():
        return input_array, axis
    if not isinstance(input_array, np.ndarray):
        raise ValueError("Input must be a numpy array")

    if len(input_array.shape) > 5:
        raise ValueError("Input array must have up to 5 dimensions")

    if axis.lower().index("z") >= len(input_array.shape) or axis.lower().index("z") < 0:
        raise ValueError("Invalid Z axis index")
    logger.debug(f"Max projection along axis {axis}")
    return np.max(input_array, axis=axis.lower().index("z")), axis.replace("Z", "")


def extract_YXC(array, dim_order):
    """
    Extract the YXC dimensions from the input array, discarding the rest.

    Args:
    array (np.ndarray): An array with arbitrary dimensions, including X, Y, Z, T, and C.
    dim_order (str): A string specifying the order of dimensions in the input array, e.g., 'XYCTZ'.

    Returns:
    np.ndarray: A new array with only YXC dimensions.
    """
    if not isinstance(array, np.ndarray):
        raise ValueError("Input must be a NumPy array.")

    if len(array.shape) != len(dim_order):
        raise ValueError(
            "Dimension order string length must match the number of dimensions in the input array."
        )

    dim_indices = {dim: i for i, dim in enumerate(dim_order)}

    X, Y, Z, T, C = [
        array.shape[dim_indices[dim]] if dim in dim_indices else 1 for dim in "XYZTC"
    ]

    # Auto-project Z-stack if there's no time dimension and Z > 1
    if T == 1 and Z > 1 and "Z" in dim_indices:
        # Perform max projection along Z axis
        array = np.max(array, axis=dim_indices["Z"])
        # Remove Z from dimension order
        dim_order = dim_order.replace("Z", "")
        dim_indices = {dim: i for i, dim in enumerate(dim_order)}
        config.global_signals.notificationSignal.emit(
            "Z-stack auto-projected, max projection along Z axis"
        )
    if "C" not in dim_indices:
        ordered_array = np.moveaxis(array, [dim_indices["Y"], dim_indices["X"]], [0, 1])
        ordered_array = np.squeeze(ordered_array)
    else:
        # Rearrange the array so that the dimensions are in the desired order (YXC)
        ordered_array = np.moveaxis(
            array, [dim_indices["Y"], dim_indices["X"], dim_indices["C"]], [0, 1, 2]
        )
        # Only attempt reshape if the total size matches
        total_size = Y * X * C
        if ordered_array.size == total_size:
            ordered_array = ordered_array.reshape(Y, X, C)
        else:
            return None
            logger.warning(
                f"Cannot reshape array of size {ordered_array.size} into shape ({Y},{X},{C})"
            )
    return ordered_array


def get_tiff_tags(tags):
    tiff_tags = {}
    for tag in tags:
        name, value = tag.name, tag.value
        tiff_tags[name] = value
    return tiff_tags


# def convert_image_to_svs(image_path, output_path):
#     import os

#     # pyvips must be loaded after the environment has vips-dev-8.14\bin in it's path
#     import pyvips

#     def mrxs_to_ome_tiff(input_file, output_file):
#         # load the input image
#         image = pyvips.Image.new_from_file(input_file, access="sequential")

#         # get the metadata from the input image
#         metadata = image.get_fields()
#         dtype = image.format

#         # save the image as ome-tiff with the metadata
#         image.tiffsave(
#             output_file,
#             compression="jpeg",
#             pyramid=True,
#             bigtiff=True,
#             tile=True,
#             tile_width=DEEPZOOM_TILE_SIZE,
#             tile_height=DEEPZOOM_TILE_SIZE,
#             # sample_format="uint16" if dtype == np.uint16 else "int8",
#             xres=image.xres,
#             yres=image.yres,
#             # Xoffset=image.xoffset,
#             # Yoffset=image.yoffset,
#         )

#     mrxs_to_ome_tiff(image_path, output_path)
#     return


def create_pyramidal_tiff(source_file, destination_file, qualitty=90):
    import pyvips

    from celer_sight_ai import config

    im = pyvips.Image.new_from_file(source_file, access="sequential")
    if im.hasalpha():
        im = im[:-1]
    try:
        im.tiffsave(
            destination_file,
            compression="jpeg",
            Q=config.ULTRA_HIGH_RES_COMPRESSION_QUALITY,
            pyramid=True,
            bigtiff=True,
            tile=True,
            tile_width=DEEPZOOM_TILE_SIZE,
            tile_height=DEEPZOOM_TILE_SIZE,
        )
    except Exception as e:
        logger.error(f"Error creating pyramidal tiff: {e}")
    return True


def open_preview_with_tiffslide_image_reader(image_path):
    """
    Get the image array and channels if available
    If the image is too large, only get the preview.
    Dont use this method other than for qgraphicsview items
    """
    from tiffslide import TiffSlide

    from celer_sight_ai.config import IMAGE_THUMBNAIL_MAX_SIZE

    image = TiffSlide(image_path)
    # get the original x size
    x_size = image.level_dimensions[0][0]
    y_size = image.level_dimensions[0][1]
    arr = image.get_thumbnail((IMAGE_THUMBNAIL_MAX_SIZE, IMAGE_THUMBNAIL_MAX_SIZE))
    # convert to numpy from pil
    arr = np.array(arr)
    # get the image channels, only rgb supported for now
    channels = ["red", "green", "blue"]
    out_dict = {"channels": channels, "size_x": x_size, "size_y": y_size}
    out_dict["is_ultra_high_res"] = True
    return arr, out_dict


def open_preview_with_openslide_image_reader(image_path):
    """
    Get the image array and channels if available
    If the image is too large, only get the preview.
    Dont use this method other than for qgraphicsview items
    """
    import openslide

    from celer_sight_ai.config import IMAGE_THUMBNAIL_MAX_SIZE

    try:
        slide = openslide.OpenSlide(
            image_path
        )  # pyvips.Image.thumbnail(image_path, IMAGE_THUMBNAIL_MAX_SIZE)
    except Exception as e:
        logger.error(f"Error opening slide {e}, trying with tiffslide")
        from tiffslide import TiffSlide

        slide = TiffSlide(image_path)
    arr = slide.get_thumbnail((IMAGE_THUMBNAIL_MAX_SIZE, IMAGE_THUMBNAIL_MAX_SIZE))
    # convert to numpy from pil
    arr = np.array(arr)
    # get the image channels, only rgb supported for now
    channels = ["red", "green", "blue"]
    out_dict = {
        "channels": channels,
        "size_x": slide.dimensions[0],
        "size_y": slide.dimensions[1],
    }
    out_dict["is_ultra_high_res"] = True
    return arr, out_dict


def get_deep_zoom_by_tiffslide(image_path, viewport_bounding_box):
    """
    Image is read directly from disk, tiffslide is efficient enough to handle large images
    metadta read quickly. If this turns out to be a problem in the future, we can store the
    metadata memory and go form there.
    viewport_bounding_box : (x, y, width,height) bounding box of the viewport
    The coordinates of the bounding box are analogous to the coordinates of the image
    """

    import time

    from tiffslide import TiffSlide
    from tiffslide.deepzoom import MinimalComputeAperioDZGenerator

    image_position = (
        viewport_bounding_box[0] + viewport_bounding_box[2] // 2,
        viewport_bounding_box[1] + viewport_bounding_box[3] // 2,
    )
    image_size = (viewport_bounding_box[2], viewport_bounding_box[3])

    start = time.time()
    _dzgen = MinimalComputeAperioDZGenerator(image_path)
    tiles, idx = compute_tile_request_level(
        _dzgen._im_levels, image_position, image_size
    )
    # get all requested tiles and fuse to an image
    all_tile_jpgs = []
    all_bounding_boxes = []
    mapped_idx = [k for k, v in _dzgen._mapped_levels.items() if v == idx][0]
    for tile in tiles:
        tile_jpg = _dzgen.get_tile(mapped_idx, tile[0], tile[1])
        all_tile_jpgs.append(tile_jpg)
        lvl_width = _dzgen._im_levels[idx][0]
        lvl_height = _dzgen._im_levels[idx][1]
        bbox = (
            tile[0] * lvl_width,
            tile[1] * lvl_height,
            lvl_width,
            lvl_height,
        )
        all_bounding_boxes.append(bbox)
    print(f"dzgen took {time.time() - start} seconds")

    return all_tile_jpgs, all_bounding_boxes


def get_exact_tile_with_openslide(slide_path, tile_bbox, tile_minimum_resolution=1024):
    """
    Provided an exact coordinate tile, get the jpeg/png tile with openslide
    tile_bbox : [x,y,w,h]

    """
    from openslide import OpenSlide

    # convert tile_bbox to [x,y,x2,y2]
    # tile_bbox = [tile_bbox[0], tile_bbox[1], tile_bbox[0] + tile_bbox[2], tile_bbox[1] + tile_bbox[3]]
    try:
        # Open the slide
        slide = OpenSlide(slide_path)
    except Exception as e:
        logger.error(f"Error opening slide {e}, trying with tiffslide")
        from tiffslide import TiffSlide

        slide = TiffSlide(slide_path)
    best_level = np.argmin(
        abs(np.array(slide.level_downsamples) - (tile_bbox[2] / 4000))
    )
    best_level = max(best_level, 0)

    # Calculate the size of the region to extract
    size = (np.array(tile_bbox[2:]) // slide.level_downsamples[best_level]).astype(
        np.int32
    )

    # # Get the tile
    # tile = slide.read_region(
    #     (np.array(tile_bbox[:2]) // slide.level_downsamples[best_level]).astype(
    #         np.int32
    #     ),
    #     best_level,
    #     size,
    # )

    # Get the tile
    tile = slide.read_region(
        (np.array(tile_bbox[:2])).astype(np.int32),
        best_level,
        size,
    )

    # # Resize the tile to the desired resolution
    tile = tile.resize((tile_minimum_resolution, tile_minimum_resolution))

    # Convert the tile to JPEG/PNG format
    tile = tile.convert("RGB")
    # save tile to disk for debug
    # cv2.imwrite("test.jpg", np.array(tile))
    return np.array(tile)


# the parent method is threaded so this shouldnt be threaded within the thread
def get_deep_zoom_by_openslide(image_path, viewport_bounding_box=None):
    """
    Image is read direcly from disk, tiffslide is efficient enough to handle large images
    metadta read quickly. If this turns out to be a problem in the future, we can store the
    metadata memory and go form there.
    viewport_bounding_box : (x, y, width,height) bounding box of the viewport
    The coordinates of the bounding box are analogous to the coordinates of the image

    bbox: [x,y,w,h] exact tile to extract from the image
    This bbox tile needs to match the size of the interactive magic box
    size
    """
    import base64
    import zlib
    from io import BytesIO
    from unicodedata import normalize

    from PIL import Image, ImageCms

    Image.MAX_IMAGE_PIXELS = 1933120000

    import time

    import openslide
    from openslide import ImageSlide, open_slide
    from openslide.deepzoom import DeepZoomGenerator
    from tiffslide import TiffSlide

    SLIDE_NAME = "slide"
    try:
        print(f"Reading {os.path.basename(image_path)}")
        slide = open_slide(image_path)
    except Exception as e:
        logger.error(f"Error opening slide {e}, trying with tiffslide")
        from tiffslide import TiffSlide

        slide = TiffSlide(image_path)

    enforce_one_tile = False
    if config.group_stop_flags.get("update_scene_ultra_high_res_plane"):
        slide.close()
        return None, None
    if isinstance(viewport_bounding_box, type(None)):
        # get the largest one patch tile
        enforce_one_tile = True
        viewport_bounding_box = (0, 0, slide.dimensions[0], slide.dimensions[1])
    else:
        # make sure bbox is between 0 and max width and height
        viewport_bounding_box = (
            max(0, viewport_bounding_box[0]),
            max(0, viewport_bounding_box[1]),
            min(viewport_bounding_box[2], slide.dimensions[0]),
            min(viewport_bounding_box[3], slide.dimensions[1]),
        )
    # get downsample from boundingbox
    best_level = slide.get_best_level_for_downsample(
        (slide.dimensions[0] / config.VIEWPORT_MIN_RESOLUTION)
        * (viewport_bounding_box[2] / slide.dimensions[0])
    )
    downsample = slide.level_downsamples[best_level]
    adjusted_region = np.array(viewport_bounding_box) / downsample
    if config.group_stop_flags.get("update_scene_ultra_high_res_plane"):
        slide.close()
        return None, None
    # generate tiles manually
    tiles = find_tiles_efficient(
        np.array(slide.dimensions) / downsample,
        (DEEPZOOM_TILE_SIZE, DEEPZOOM_TILE_SIZE),
    ).astype(np.int32)
    relevant_tiles = get_relevant_tiles_numpy(adjusted_region, tiles)

    if config.group_stop_flags.get("update_scene_ultra_high_res_plane"):
        slide.close()
        return None, None
    past_tile_set = set([str(i[1].tolist()) for i in config._deepzoom_pixmaps])
    # tiles to compute
    relevant_tiles = [
        i
        for i in relevant_tiles
        if str((i * downsample).astype(np.int32).tolist()) not in past_tile_set
    ]
    # order the tiles with the one closest to the center of the viewport first
    tiles_pos = sorted(
        relevant_tiles,
        key=lambda x: np.linalg.norm(
            np.array([x[0] + (x[2] // 2), x[1] + (x[3] // 2)])
            - np.array(
                [
                    viewport_bounding_box[0] + (viewport_bounding_box[2] // 2),
                    viewport_bounding_box[1] + (viewport_bounding_box[3] // 2),
                ]
            )
        ),
    )
    for tile_pos in tiles_pos:
        if config.group_stop_flags.get("update_scene_ultra_high_res_plane"):
            slide.close()
            return None, None
        read_and_display_tile_deepzoom(
            tile_pos, slide, best_level, downsample, os.path.basename(image_path)
        )
        # if its threaded, wait 100 ms for less stuttering
        # if config.user_cfg["USER_WORKERS"]:
        #     time.sleep(0.05)
    slide.close()

    return None, None


def find_tiles_efficient(image_size, tile_size):
    """
    Find all the tiles for a given image size and tile size using numpy for efficiency.

    :param image_size: Tuple (width, height) of the image
    :param tile_size: Tuple (width, height) of each tile
    :return: Numpy array of tiles as [x, y, width, height]
    """
    image_width, image_height = image_size
    tile_width, tile_height = tile_size

    # Calculate the number of tiles in each dimension
    num_tiles_x = image_width // tile_width
    num_tiles_y = image_height // tile_height

    # Create grid of tile positions
    x_positions = np.arange(0, image_width, tile_width)
    y_positions = np.arange(0, image_height, tile_height)

    # Create a meshgrid and reshape
    x_grid, y_grid = np.meshgrid(x_positions, y_positions)
    tiles = np.stack(
        [
            x_grid.ravel(),
            y_grid.ravel(),
            np.full(x_grid.size, tile_width),
            np.full(y_grid.size, tile_height),
        ],
        axis=1,
    )

    return tiles


def get_relevant_tiles_numpy(bounding_box, tiles):
    """
    Get all tiles that intersect with a given bounding box using numpy for efficiency.

    :param bounding_box: List [x, y, width, height] of the bounding box
    :param tiles: Numpy array of tiles as [x, y, width, height]
    :return: Numpy array of relevant tiles
    """
    bbox_x, bbox_y, bbox_width, bbox_height = bounding_box

    # Calculate the bounding box end coordinates
    bbox_x_end = bbox_x + bbox_width
    bbox_y_end = bbox_y + bbox_height

    # Calculate the end coordinates of the tiles
    tiles_x_end = tiles[:, 0] + tiles[:, 2]
    tiles_y_end = tiles[:, 1] + tiles[:, 3]

    # Check for intersection
    intersects_x = np.logical_and(tiles[:, 0] < bbox_x_end, tiles_x_end > bbox_x)
    intersects_y = np.logical_and(tiles[:, 1] < bbox_y_end, tiles_y_end > bbox_y)
    intersects = np.logical_and(intersects_x, intersects_y)

    return tiles[intersects]


def read_and_display_tile_deepzoom(tile_pos, slide, best_level, downsample, image_name):
    import time
    from io import BytesIO

    import openslide
    from PyQt6 import QtCore, QtGui, QtWidgets

    try:
        logger.debug("Reading tile data")
        start = time.time()
        tile_arr = slide.read_region(
            (tile_pos[:2] * downsample).astype(np.int32),
            best_level,
            tuple(tile_pos[2:]),
        )
        print(f"Took {time.time() - start} seconds")
        tile_pos = (tile_pos * downsample).astype(np.int32)
        # tile_pos[2:] = (tile_pos[2:]).astype(np.int32)
        # Create an in-memory bytes buffer
        bytes_io = BytesIO()
        # Save the PIL image to the bytes buffer using the JPEG format
        tile_arr.convert("RGB").save(bytes_io, format="JPEG")
        try:
            tile_arr.verify()  # verify that it is, in fact, an image
        except (OSError, SyntaxError):
            logger.error("Bad tile")
        # Get the byte data from the buffer
        tile_arr = bytes_io.getvalue()

        if isinstance(tile_arr, bytes):
            # Convert the byte string to QByteArray
            byte_array = QtCore.QByteArray(tile_arr)
            # Create QPixmap from QByteArray
            pixmap = QtGui.QPixmap()
            success = pixmap.loadFromData(
                byte_array, "JPEG"
            )  # Specify the format if known
            if not success:
                logger.error("Failed to load tile")
                return
        else:
            bytesPerLine = tile_arr.shape[1] * tile_arr.shape[2]
            # load from numpy array
            qimage = QtGui.QImage(
                tile_arr.copy(),
                tile_arr.shape[1],
                tile_arr.shape[0],
                bytesPerLine,
                QtGui.QImage.Format.Format_RGB888,
            )
            pixmap = QtGui.QPixmap.fromImage(qimage)
        # add pixmap to scene
        config.global_signals.add_partial_slide_images_to_scene_signal.emit(
            {
                "image_data": [pixmap],
                "image_bounding_box": [tile_pos],
                "image_name": image_name,
                "downsample": downsample,
            }
        )
    except Exception as e:
        logger.error(f"Skipping due to error: {e}")


def get_tile_pixel_scale(_dzgen, level, x_max, y_max):
    # x_max is the real x max size of the full sized image
    all_tiles_x, all_tiles_y = _dzgen.level_tiles[level]
    # if there are more than one tiles in x or in y, use those to get the scale
    if all_tiles_x > 1:
        # get the first and second tile coordinates
        x_tile_1 = _dzgen.get_tile_coordinates(level, (0, 0))
        x_tile_2 = _dzgen.get_tile_coordinates(level, (1, 0))
        width_of_sample_tile = x_tile_1[2][0]
        x_coord_tile_1 = x_tile_1[0][0]
        x_coord_tile_2 = x_tile_2[0][0]
        x_scale = width_of_sample_tile / (x_coord_tile_2 - x_coord_tile_1)
    else:
        x_tile_1 = _dzgen.get_tile_coordinates(level, (0, 0))
        width_of_sample_tile = x_tile_1[2][0]
        x_scale = width_of_sample_tile / x_max
    if all_tiles_y > 1:
        y_tile_1 = _dzgen.get_tile_coordinates(level, (0, 0))
        y_tile_2 = _dzgen.get_tile_coordinates(level, (0, 1))
        height_of_sample_tile = y_tile_1[2][1]
        y_coord_tile_1 = y_tile_1[0][1]
        y_coord_tile_2 = y_tile_2[0][1]
        y_scale = height_of_sample_tile / (y_coord_tile_2 - y_coord_tile_1)
    else:
        y_tile_1 = _dzgen.get_tile_coordinates(level, (0, 0))
        height_of_sample_tile = y_tile_1[2][1]
        y_scale = height_of_sample_tile / y_max
    return x_scale, y_scale


def calculate_best_level(
    slide, _dzgen, viewport_bounding_box, min_width=2000, enforce_one_tile=False
):
    """
    Calculate the best level to retrieve tiles from OpenSlide.

    :param slide: An OpenSlide object.
    :param viewport_width: Width of the viewport in pixels.
    :param viewport_height: Height of the viewport in pixels.
    :param min_width: Minimum width required for the total image (default 2000 pixels).
    :return: Best level to use for retrieving tiles.
    """
    # Calculate the zoom factor based on the viewport and the full image size
    full_width, full_height = slide.dimensions
    zoom_factor = min(
        full_width / viewport_bounding_box[2], full_height / viewport_bounding_box[3]
    )

    if enforce_one_tile:
        # find a resolution that is total more than 2k by 2k
        for idx, res in enumerate(_dzgen.level_dimensions):
            if (
                res[0] * _dzgen.level_tiles[idx][0] > min_width
                and res[1] * _dzgen.level_tiles[idx][1] > min_width
            ):
                return idx
        return len(_dzgen.level_dimensions) - 1
        # fuse tiles into one object
    # Find the best level where the width at that level is above the minimum width
    if not _dzgen.level_count:
        return 0
    best_level = 0

    actual_required_width = viewport_bounding_box[2]
    percent_of_full_image = actual_required_width / full_width
    # find the level where this percent is atleast 2000 pixel wide
    obtained_resolution = (
        np.array(_dzgen.level_tiles)[:, 1] * percent_of_full_image * DEEPZOOM_TILE_SIZE
    )
    # find the first available resolution that is just larger than 2000
    best_idx = None
    for idx, res in enumerate(obtained_resolution):
        if res > min_width:
            best_idx = idx
            break
    if not best_idx:
        # get the largest available resolution
        best_idx = np.argmax(obtained_resolution)
    return best_idx


def get_all_possible_image_hashes(
    image_path, is_ultra_high_res=False, TARGET_SIZE=(256, 256)
):
    all_hashes = []
    for jpg_quality in [100, 95, 90]:
        all_hashes.append(
            standardize_and_hash_image(
                image_path,
                is_ultra_high_res=is_ultra_high_res,
                TARGET_SIZE=TARGET_SIZE,
                to_jpg=True,
                jpg_quality=jpg_quality,
            )
        )
    # compute png hash
    all_hashes.append(
        standardize_and_hash_image(
            image_path,
            is_ultra_high_res=is_ultra_high_res,
            TARGET_SIZE=TARGET_SIZE,
            to_jpg=False,
        )
    )
    return all_hashes


def standardize_and_hash_image(
    image_path,
    is_ultra_high_res=False,
    TARGET_SIZE=(256, 256),
    to_jpg=False,
    jpg_quality=95,
):
    """
    Standardizes an image to 256x256 int8 format and generates a hash.
    Works with both regular and ultra-high-res images.

    Args:
        image_path (str): Path to the image file
        is_ultra_high_res (bool): Whether the image is ultra high resolution

    Returns:
        str: SHA-256 hash of the standardized image
    """
    import hashlib

    import cv2
    import numpy as np
    from tiffslide import TiffSlide

    hash_method = "sha256_" + str(TARGET_SIZE[0])
    if is_ultra_high_res:
        try:
            # Use TiffSlide for ultra-high-res images
            with TiffSlide(image_path) as slide:
                # Get thumbnail at approximately 256x256
                thumb = slide.get_thumbnail(TARGET_SIZE)
                # Convert PIL image to numpy array
                img_array = np.array(thumb)

                # Convert to grayscale if RGB
                if len(img_array.shape) == 3:
                    img_array = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)

        except Exception as e:
            logger.error(f"Error processing ultra-high-res image: {e}")
            raise
    else:
        # Regular image processing
        img_array = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        if to_jpg:
            cv2.imwrite(
                "test.jpg", img_array, [int(cv2.IMWRITE_JPEG_QUALITY), jpg_quality]
            )
            img_array = cv2.imread("test.jpg", cv2.IMREAD_GRAYSCALE)
        if img_array is None:
            raise ValueError(f"Could not read image at {image_path}")

        # Resize to target size
        img_array = cv2.resize(img_array, TARGET_SIZE, interpolation=cv2.INTER_AREA)

    # Ensure int8 format
    if img_array.dtype != np.uint8:
        # Normalize and convert higher bit depth images
        img_array = cv2.normalize(img_array, None, 0, 255, cv2.NORM_MINMAX)
        img_array = img_array.astype(np.uint8)

    # Generate hash from standardized image
    return hashlib.sha256(img_array.tobytes()).hexdigest(), hash_method


def compute_tile_request_level(level_resolution, image_position, image_size):
    # Every level is half the resolution of the previous level, level 0 has only 1 tile, level 1 has 4.
    # Uses the minimum resolution and the available image level sizes to compute the level of the tile request
    # level_resolution: level of the slide to extract tiles from
    # image_position:

    import math

    from celer_sight_ai.config import ZOOM_OUT_REZ

    minx = max(0, image_position[0] - (image_size[0] // 2))
    miny = max(0, image_position[1] - (image_size[1] // 2))
    maxx = image_position[0] + (image_size[0] // 2)
    maxy = image_position[1] + (image_size[1] // 2)
    # Start fom the lowest resolution possible and work our way up

    lowest_res_posible = min(
        [i for i in level_resolution if i[0] > ZOOM_OUT_REZ], key=lambda x: x[0]
    )

    idx = level_resolution.index(lowest_res_posible)
    max_res_x = max(level_resolution, key=lambda x: x[0])[0]
    max_res_y = max(level_resolution, key=lambda x: x[1])[1]
    # calculate tiles needed for that resolution from minx to maxx ,  clip to min max
    from_tile_x = np.clip(math.floor(minx / level_resolution[idx][0]), 0, max_res_x)
    to_tile_x = np.clip(math.ceil(maxx / level_resolution[idx][0]), 0, max_res_x)
    from_tile_y = np.clip(math.floor(miny / level_resolution[idx][1]), 0, max_res_y)
    to_tile_y = np.clip(math.ceil(maxy / level_resolution[idx][1]), 0, max_res_y)

    all_tiles_needed = [
        (x, y)
        for x in range(from_tile_x, to_tile_x)
        for y in range(from_tile_y, to_tile_y)
    ]
    return all_tiles_needed, idx


def is_tif_ultra_high_res(tif_path):
    with tifffile.TiffFile(tif_path) as tif:
        # get dimenions of the first image
        print("*" * 100)
        print(tif_path)
        print(len(tif.series))
        print(tif.series[0].shape)
        print("*" * 100)
        x_size = list(tif.series[0]._axes_squeezed.lower()).index("x")
        y_size = list(tif.series[0]._axes_squeezed.lower()).index("y")

        if max([x_size, y_size]) > config.ULTRA_HIGH_RES_THRESHOLD:
            return True
    return False


def extract_more_metadata_if_available(tif_path, dict_out):
    tif = tifffile.TiffFile(tif_path)
    if dict_out.get("channels") and any(
        [isinstance(c, str) and "channel:" in c.lower() for c in dict_out["channels"]]
    ):
        if hasattr(tif, "ome_metadata") and tif.ome_metadata is not None:
            dict_out = extract_ome_metadata(tif_path, dict_out)
        # case of imagej metadata, override any channels found in ome metadata
        if hasattr(tif, "imagej_metadata") and tif.imagej_metadata is not None:
            dict_out = extract_channels_from_imagej_metadata(
                dict_out, tif.imagej_metadata
            )

        else:
            # manual extraction of metadata
            dict_out = extract_metadata_from_tiff_tags(tif, dict_out)
    return dict_out


def read_ome_tiff(tif_path):
    """
    Reads an OME-TIFF file using tifffile and returns a YXC array.
    If there are time or Z dimensions, performs max projection along those axes.
    Also extracts physical pixel size information if available.
    """
    import logging

    import numpy as np
    import tifffile

    logger = logging.getLogger(__name__)

    try:
        with tifffile.TiffFile(tif_path) as tif:
            # Read the full data
            data = tif.asarray()

            # Get dimension order from OME metadata
            if not tif.ome_metadata:
                return None, None
            ome_metadata = xmltodict.parse(tif.ome_metadata)
            dimension_order = (
                ome_metadata.get("ome:OME", {})
                .get("ome:Image", {})
                .get("ome:Pixels", {})
                .get("@DimensionOrder", "XYZCT")
                .upper()
            )
            dimension_size = []
            metadata_extracted = extract_ome_metadata(tif_path, {})
            for dim in dimension_order:
                dimension_size.append(metadata_extracted.get(f"size_{dim}".lower(), 1))
            channels = metadata_extracted.get("channels", None)

            # If array shape doesn't match metadata dimensions, try to infer correct order
            if len(data.shape) != len(dimension_order) or data.shape != tuple(
                dimension_size
            ):
                # Create mapping of sizes to dimensions
                size_to_dim = {}
                found_dims = set()
                for i, size in enumerate(data.shape):
                    matching_dims = [
                        dim
                        for dim, dim_size in zip(dimension_order, dimension_size)
                        if int(dim_size) == size and dim not in found_dims
                    ]
                    if matching_dims:
                        size_to_dim[i] = matching_dims[0]
                        found_dims.add(matching_dims[0])

                # Reconstruct dimension order based on array shape
                dimension_order = "".join(
                    [
                        size_to_dim.get(
                            i, ""
                        )  # Use empty string if no matching dimension
                        for i in range(len(data.shape))
                    ]
                )

                # If we couldn't match all dimensions, fall back to standard order
                if len(dimension_order) != len(data.shape):
                    if len(data.shape) == 2:
                        dimension_order = "XY"
                    elif len(data.shape) == 3:
                        dimension_order = "XYC"
                    elif len(data.shape) == 4:
                        dimension_order = "ZXYC"
                    elif len(data.shape) == 5:
                        dimension_order = "TZXYC"

                # adjust the dimension size
                dimension_size = [
                    dimension_size[dimension_order.index(dim)]
                    for dim in dimension_order
                ]
            # Build a mapping from dimension character to axis index
            dim_map = {dim: idx for idx, dim in enumerate(dimension_order)}
            # Perform max projection along T and Z if necessary
            axes_to_project = []
            # Check if 'T' and 'Z' are in the dimension order and if their sizes >1
            for dim in ("T", "Z"):
                if dim in dim_map and data.shape[dim_map[dim]] > 1:
                    axes_to_project.append(dim_map[dim])

            if axes_to_project:

                data = np.max(data, axis=tuple(axes_to_project), keepdims=False)
                # Remove projected dimensions from dimension_order
                dimension_order = "".join([d for d in dimension_order if d not in "TZ"])
                dim_map = {dim: idx for idx, dim in enumerate(dimension_order)}

            # Ensure 'C' dimension is present
            if "C" not in dimension_order:
                data = np.expand_dims(data, axis=-1)
                dimension_order += "C"
                dim_map["C"] = len(dimension_order) - 1

            # Rearrange data to YXC format if necessary
            desired_order = "XYC"
            if dimension_order != desired_order:
                # Get the axes to transpose
                rearrange_axes = [dim_map[dim] for dim in desired_order]
                data = np.transpose(data, axes=rearrange_axes)

            return np.ascontiguousarray(data), {
                "channels": channels,
                "size_x": int(dimension_size[0]),
                "size_y": int(dimension_size[1]),
                "physical_pixel_size_x": (
                    float(metadata_extracted.get("physical_pixel_size_x"))
                    if metadata_extracted.get("physical_pixel_size_x") is not None
                    else None
                ),
                "physical_pixel_size_y": (
                    float(metadata_extracted.get("physical_pixel_size_y"))
                    if metadata_extracted.get("physical_pixel_size_y") is not None
                    else None
                ),
                "physical_pixel_size_x_unit": metadata_extracted.get(
                    "physical_pixel_size_x_unit"
                ),
                "physical_pixel_size_y_unit": metadata_extracted.get(
                    "physical_pixel_size_y_unit"
                ),
            }

    except Exception as e:
        logger.error(f"Error reading OME-TIFF file {tif_path}: {e}")
        return None, None


def extract_ome_metadata(tif_path, dict_out):
    from pyometiff import OMETIFFReader

    reader = OMETIFFReader(fpath=tif_path)
    with tifffile.TiffFile(tif_path) as tif:
        if not hasattr(tif, "ome_metadata") or tif.ome_metadata is None:
            return dict_out
        try:
            parsed_metadata = reader.parse_metadata(tif.ome_metadata)
            if parsed_metadata is None:
                raise Exception("No parsed metadata found")

            # Extract dimension sizes and order
            dict_out["size_x"] = parsed_metadata.get("SizeX")
            dict_out["size_y"] = parsed_metadata.get("SizeY")
            dict_out["size_z"] = parsed_metadata.get("SizeZ")
            dict_out["size_c"] = parsed_metadata.get("SizeC")
            dict_out["size_t"] = parsed_metadata.get("SizeT")
            dict_out["dimension_order"] = parsed_metadata.get("DimensionOrder")

            if (
                parsed_metadata.get("Channels")
                and len(parsed_metadata["Channels"].keys()) == parsed_metadata["SizeC"]
            ):
                if not list(parsed_metadata["Channels"].keys()) == [None]:
                    all_channels = list(parsed_metadata["Channels"].keys())
                    dict_out["channels"] = [
                        parsed_metadata["Channels"][i]["Name"]
                        for i in all_channels
                        if i is not None
                    ]
                # Extract physical units if available
                dict_out["physical_pixel_size_x_unit"] = parsed_metadata.get(
                    "PhysicalSizeXUnit", None
                )
                dict_out["physical_pixel_size_y_unit"] = parsed_metadata.get(
                    "PhysicalSizeYUnit", None
                )
                dict_out["physical_pixel_size_x"] = parsed_metadata.get(
                    "PhysicalSizeX", None
                )
                dict_out["physical_pixel_size_y"] = parsed_metadata.get(
                    "PhysicalSizeY", None
                )
        except Exception:
            m_ome = remove_at_symbol(xmltodict.parse(tif.ome_metadata))

            # Check for different possible namespace prefixes
            possible_prefixes = ["ome:", "xmlns:", ""]
            image_key = None
            pixels_key = None
            channel_key = None

            # Find the correct keys based on what exists in the metadata
            for prefix in possible_prefixes:
                if f"{prefix}OME" in m_ome:
                    m_ome = m_ome[f"{prefix}OME"]
                    for img_prefix in possible_prefixes:
                        if f"{img_prefix}Image" in m_ome:
                            image_key = f"{img_prefix}Image"
                            for pix_prefix in possible_prefixes:
                                if f"{pix_prefix}Pixels" in m_ome[image_key]:
                                    pixels_key = f"{pix_prefix}Pixels"
                                    for ch_prefix in possible_prefixes:
                                        if (
                                            f"{ch_prefix}Channel"
                                            in m_ome[image_key][pixels_key]
                                        ):
                                            channel_key = f"{ch_prefix}Channel"
                                            break
                                    break
                            break
                    break

            if all([image_key, pixels_key, channel_key]):
                channels = m_ome[image_key][pixels_key][channel_key]
                channels = remove_at_symbol(channels)

                # Extract dimension sizes and order from pixels metadata
                pixels = m_ome[image_key][pixels_key]
                dict_out["size_x"] = int(pixels.get("SizeX", 0))
                dict_out["size_y"] = int(pixels.get("SizeY", 0))
                dict_out["size_z"] = int(pixels.get("SizeZ", 1))
                dict_out["size_c"] = int(pixels.get("SizeC", 1))
                dict_out["size_t"] = int(pixels.get("SizeT", 1))
                dict_out["dimension_order"] = pixels.get("DimensionOrder", "XYZCT")

                # Continue with existing channel extraction
                if isinstance(channels, list):
                    for ii in range(len(channels)):
                        if "Name" in channels[ii].keys():
                            dict_out["channels"].append(channels[ii]["Name"])
                    dict_out["channels"] = [
                        channel["ID"] for channel in remove_at_symbol(channels)
                    ]
                else:
                    if "Name" in channels.keys():
                        dict_out["channels"] = channels["Name"]
                    elif channels["ID"] == "Channel:0:2":  # --> rgb
                        dict_out["channels"] = ["red", "green", "blue"]
                    elif (
                        channels["ID"] == "Channel:0:0"
                        or channels["ID"] == "Channel:d1"
                    ):  # --> grayscale
                        dict_out["channels"] = ["gray"]
                    else:
                        logger.error(f"No channel found for {tif.filename}")

                # Extract physical units from XML if available
                if pixels_key in m_ome[image_key]:
                    pixels = m_ome[image_key][pixels_key]
                    dict_out["physical_pixel_size_x_unit"] = pixels.get(
                        "PhysicalSizeXUnit", None
                    )
                    dict_out["physical_pixel_size_y_unit"] = pixels.get(
                        "PhysicalSizeYUnit", None
                    )
                    dict_out["physical_pixel_size_x"] = pixels.get(
                        "PhysicalSizeX", None
                    )
                    dict_out["physical_pixel_size_y"] = pixels.get(
                        "PhysicalSizeY", None
                    )
            else:
                logger.error(f"Could not find required metadata keys in {tif.filename}")

    return dict_out


def extract_metadata_from_tiff_tags(tif, dict_out):
    """
    Extract metadata from TIFF tags, specifically looking for channel information
    in ImageDescription tag.

    Args:
        tif: TiffFile object
        dict_out: Dictionary to store the extracted metadata

    Returns:
        dict: Updated dictionary with extracted metadata
    """
    if (
        hasattr(tif.pages[0], "tags")
        and ("ImageDescription" in tif.pages[0].tags)
        and hasattr(tif.pages[0].tags["ImageDescription"], "value")
    ):
        import json

        val = tif.pages[0].tags["ImageDescription"].value
        resolution_x, resolution_y = get_resolution_in_mm(tif)

        metadata = remove_at_symbol(
            xmltodict.parse(tif.pages[0].tags["ImageDescription"].value)
        )
        if "BTIImageMetaData" in metadata:
            metadata = metadata["BTIImageMetaData"]
            dict_out["channels"] = [metadata["ImageAcquisition"]["Channel"]["Color"]]

    return dict_out


def get_resolution_in_mm(tif):
    """
    Get the resolution in pixels per millimeter from a TIFF file.

    Args:
        tif: TiffFile object

    Returns:
        tuple: (x_resolution, y_resolution) in pixels per millimeter
    """
    tags = get_tiff_tags(tif.pages[0].tags)

    # Get resolution values
    x_resolution = tags.get("XResolution", None)
    y_resolution = tags.get("YResolution", None)
    resolution_unit = tags.get("ResolutionUnit", 2)  # Default is inches (RESUNIT_INCH)

    if x_resolution is None or y_resolution is None:
        return None, None

    # Convert fraction tuples to float values
    if isinstance(x_resolution, tuple):
        x_resolution = x_resolution[0] / x_resolution[1]
    if isinstance(y_resolution, tuple):
        y_resolution = y_resolution[0] / y_resolution[1]

    # Convert based on resolution unit
    # ResolutionUnit values: 1: none, 2: inches, 3: centimeters
    if resolution_unit == 2:  # inches
        # Convert from pixels per inch to pixels per mm
        x_resolution = x_resolution / 25.4  # 25.4 mm per inch
        y_resolution = y_resolution / 25.4
    elif resolution_unit == 3:  # cm
        # Convert from pixels per cm to pixels per mm
        x_resolution = x_resolution / 10
        y_resolution = y_resolution / 10

    return x_resolution, y_resolution


def standardize_channels(arr, current_channels):
    """
    Detect and normalize channel information based on array shape and current channel settings.

    Args:
        arr (numpy.ndarray): Image array
        current_channels (list|str|None): Current channel information

    Returns:
        list: Normalized list of channel names
        numpy.ndarray: Potentially modified image array (e.g., if alpha channel removed)
    """
    # Handle single channel cases like ['Channel:0:0']
    if current_channels == ["Channel:0:0"] or current_channels == [
        "Channel:0"
    ]:  # both are gray
        if len(arr.shape) == 3 and arr.shape[2] == 3:
            return ["red", "green", "blue"], arr
        elif len(arr.squeeze().shape) == 2:
            return ["gray"], arr

    # Handle cases where channels are None or follow Channel:X:Y pattern
    if current_channels is None or (
        isinstance(current_channels, list)
        and all(
            isinstance(c, str) and c.startswith("Channel:") for c in current_channels
        )
    ):
        if len(arr.shape) == 3:
            if arr.shape[2] == 3:
                return ["red", "green", "blue"], arr
            elif arr.shape[2] == 4:
                logger.info("Found image with alpha channel, throwing out alpha.")
                return ["red", "green", "blue"], arr[:, :, :3]
            elif arr.shape[2] == 1:
                return ["gray"], arr
        elif len(arr.squeeze().shape) == 2:
            return ["gray"], arr

    # Handle specific cases of Channel:0 or gray with RGB array
    if (
        current_channels in (["Channel:0"], ["gray"])
        and len(arr.shape) == 3
        and arr.shape[2] == 3
    ):

        if len(arr.shape) == 3 and arr.shape[2] == 3:
            if np.all(arr[:, :, 0] == arr[:, :, 1]) and np.all(
                arr[:, :, 1] == arr[:, :, 2]
            ):
                return ["gray"], arr
            return ["red", "green", "blue"], arr

    # Normalize string channels to list
    if isinstance(current_channels, str):
        return [current_channels], arr

    return current_channels, arr


def extract_channels_from_imagej_metadata(dict_out, metadata):
    """
    Extract channel information from ImageJ metadata LUTs.

    Args:
        metadata (dict): ImageJ metadata dictionary containing LUTs information

    Returns:
        list: List of RGB channel values extracted from LUTs, or None if no valid LUTs found
    """
    if metadata is None or "LUTs" not in metadata:
        return dict_out

    try:
        # Convert LUT to color rgb max value for each channel
        dict_out["channels"] = [
            np.max(lut, axis=1).tolist() for lut in metadata["LUTs"]
        ]
    except Exception as e:
        logger.error(f"Error extracting channels from ImageJ LUTs: {e}")
    return dict_out


def get_squeezed_bf_dimentions(pixel_data):
    dims_order = pixel_data.DimensionOrder
    shape_squeezed = []
    axes_squeezed = ""
    for ax in dims_order:
        if getattr(pixel_data, f"Size{ax}", 0) > 1:
            axes_squeezed += ax
            shape_squeezed.append(getattr(pixel_data, f"Size{ax}"))
    return axes_squeezed, shape_squeezed


def write_ome_tiff(
    arr,
    channels,
    tif_path,
    physical_pixel_size_x: float | None = None,
    physical_pixel_size_y: float | None = None,
    physical_pixel_unit_x: str | None = None,
    physical_pixel_unit_y: str | None = None,
):
    from pathlib import Path

    import pyometiff

    logger.debug(f"Writing OME-TIFF to {tif_path}")
    c_size = 1
    try:
        if len(arr.shape) > 2:
            c_size = arr.shape[2]

        metadata_dict = {
            "SizeX": arr.shape[0],
            "SizeY": arr.shape[1],
            "SizeC": c_size,
            "SizeT": 1,
            "SizeZ": 1,
            "Channels": {
                str(channels[i]): {
                    "Name": channels[i],
                    "SamplesPerPixel": 1,
                }
                for i in range(len(channels))
            },
        }
        if physical_pixel_size_x:
            metadata_dict["PhysicalSizeX"] = (
                float(physical_pixel_size_x)
                if not isinstance(physical_pixel_size_x, type(None))
                else None
            )
        if physical_pixel_size_y:
            metadata_dict["PhysicalSizeY"] = (
                float(physical_pixel_size_y)
                if not isinstance(physical_pixel_size_y, type(None))
                else None
            )
        if physical_pixel_unit_x:
            metadata_dict["PhysicalSizeXUnit"] = physical_pixel_unit_x
        if physical_pixel_unit_y:
            metadata_dict["PhysicalSizeYUnit"] = physical_pixel_unit_y

        # a string describing the dimension ordering
        dimension_order = "CYX"

        # Rearrange dimensions to match the dimension order
        data_to_write = np.transpose(arr, (2, 0, 1))
        # if there is a single named channel and multiple are provided, we need to do
        # max projection
        if c_size == 1:
            data_to_write = np.max(data_to_write, axis=2)
        print(data_to_write.shape)

        writer = pyometiff.OMETIFFWriter(
            fpath=Path(tif_path),
            dimension_order=dimension_order,
            array=data_to_write,
            metadata=metadata_dict,
            overwrite=True,
            explicit_tiffdata=False,
        )

        writer.write()
        writer.write_xml()
    except Exception as e:
        logger.error(f"Error writing OME-TIFF: {e}")
        return False
    logger.debug(f"OME-TIFF written to {tif_path}")
    return True


def read_specialized_image(
    tif_path,
    avoid_loading_ultra_high_res_arrays_normaly=False,
    for_thumbnail=False,
    for_interactive_zoom=False,
    bbox=None,
):
    """
    bbox: [x,y,width,height] bounding box of the region of the image data to crop
    In case of a normal file, get the original arrays and channels from the metadata
    In case of a ultra high res array, get a thumbnail array, and mark the object as ultra high res
    """
    import time

    logging.getLogger("pyvips").setLevel(logging.ERROR)

    import javabridge

    from celer_sight_ai.config import ULTRA_HIGH_RES_THRESHOLD

    IS_ULTRA_HIGH_RES = False
    IMAGE_READ = False  # whent the image bytes are read, we avoide re-reading them

    # threshold is the average of the x and y dimensions
    effective_ultra_hight_res_threshold = (
        ULTRA_HIGH_RES_THRESHOLD * ULTRA_HIGH_RES_THRESHOLD
    )

    dict_out = {}
    arr_metadata = {}  # loads while reading the image
    dict_out["number_of_images"] = None
    dict_out["number_of_slices"] = None
    dict_out["channels"] = None  # mandatory
    dict_out["number_of_channels"] = None
    dict_out["min"] = None
    dict_out["max"] = None
    dict_out["LUTs"] = None
    # for ultra high res
    dict_out["needs_pyramidal_conversion"] = False
    dict_out["size_x"] = None  # mandatory
    dict_out["size_y"] = None  # mandatory
    dict_out["image_bounding_box"] = None  # used for ultra high res
    dict_out["updated_"] = None  # new image save location in a temp folder
    dict_out["is_ultra_high_res"] = False

    IS_PYRAMIDAL = False
    IS_ULTRA_HIGH_RES = None
    IS_OME_TIFF = False
    # test if its ome tiff
    with tifffile.TiffFile(tif_path) as tif:
        if tif.is_ome:
            IS_OME_TIFF = True
            logger.debug("its ome tiff")

    # # try first to get everything with bioio, if that fails try other methods
    if not IS_OME_TIFF:
        try:
            # with config.jvm_lock:
            print("attaching to jvm")
            javabridge.attach()
            metadata_xml = config.bioformats.get_omexml_metadata(path=tif_path)
            metadata_dict = config.bioformats.omexml.OMEXML(metadata_xml)
            # extract yxc
            pixel_data = metadata_dict.image().Pixels
            dims_order = pixel_data.DimensionOrder
            # we only need to extract the image data and channels,
            # 1 series and do max projection in the Z dimentions if needed

            dict_out["size_x"] = pixel_data.SizeX
            dict_out["size_y"] = pixel_data.SizeY

            # if the image is ultra high res, dont use bioformats,
            # instead we skip here and load it iteratively with tiffslide of openslide
            if (
                pixel_data.SizeX > config.ULTRA_HIGH_RES_THRESHOLD
                or pixel_data.SizeY > config.ULTRA_HIGH_RES_THRESHOLD
            ):
                IS_ULTRA_HIGH_RES = True
            else:
                logger.debug("Image is not ultra high res, loading with bioformats")
                # Extract channels from metadata
                channels = []
                for i in range(pixel_data.channel_count):
                    channel = pixel_data.Channel(i)
                    if channel.Name:
                        channels.append(channel.Name)
                    else:
                        channels.append(f"Channel:{i}")

                # Assign channels to output dict
                dict_out["channels"] = channels

                # get the physical pixel sizes in mm
                dict_out["physical_pixel_size_x"] = pixel_data.PhysicalSizeX
                dict_out["physical_pixel_size_y"] = pixel_data.PhysicalSizeY
                dict_out["physical_pixel_unit_x"] = pixel_data.PhysicalSizeXUnit
                dict_out["physical_pixel_unit_y"] = pixel_data.PhysicalSizeYUnit

                image_file = config.bioformats.ImageReader(path=tif_path)

                if pixel_data.SizeZ > 1:
                    z_data = np.empty(
                        (
                            pixel_data.SizeZ,
                            pixel_data.SizeY,
                            pixel_data.SizeX,
                            pixel_data.SizeC,
                        )
                    )
                    for z in range(pixel_data.SizeZ):
                        logger.debug(f"Max projection along axis Z: {z}")
                        img = image_file.read(series=0, z=z, rescale=False)
                        if len(img.shape) == 2:
                            img = np.expand_dims(img, axis=2)
                        z_data[z, :, :, :] = img
                    # do max projection in the Z dimension
                    arr = np.max(z_data, axis=0)
                    dims_order = "YXC"
                else:
                    dims_order, shape_squeezed = get_squeezed_bf_dimentions(pixel_data)
                    arr = image_file.read(series=0, rescale=False)

                # if channels are found, return the image
                if dict_out["channels"]:
                    dict_out = extract_more_metadata_if_available(tif_path, dict_out)
                    dict_out["channels"], arr = standardize_channels(
                        arr, dict_out["channels"]
                    )
                    if bbox:
                        arr = crop_and_pad_image(arr, bbox)
                    return arr, dict_out
        except Exception as e:
            logger.error(f"Error loading tiff file with bioformats: {e}")
        finally:
            javabridge.detach()

    try:
        with tifffile.TiffFile(tif_path) as tif:
            # get dimenions of the first image
            print("*" * 100)
            print(tif_path)
            print("*" * 100)
            _axes_squeezed = tif.series[0]._axes_squeezed.lower()
            _shape_squeezed = tif.series[0]._shape_squeezed
            x_size = _shape_squeezed[list(_axes_squeezed).index("x")]
            y_size = _shape_squeezed[list(_axes_squeezed).index("y")]
            t_size = 0
            if "t" in _axes_squeezed:
                t_size = _shape_squeezed[list(_axes_squeezed).index("t")]

            if t_size > 1:
                return None, None
            if max([x_size, y_size]) > config.ULTRA_HIGH_RES_THRESHOLD:
                IS_ULTRA_HIGH_RES = True
                dict_out["is_ultra_high_res"] = IS_ULTRA_HIGH_RES
            dims_order = tif.series[0]._axes_squeezed
            dims_shape = tif.series[0].shape
            if tif.series[0].is_pyramidal:
                dict_out["needs_pyramidal_conversion"] = False
                IS_PYRAMIDAL = True

    except Exception as e:
        # There is an edge case that the tiff file wont load due to out of bounds error on tiff.series
        # in that case, we will load the image with bioio
        logger.error(f"Error loading tiff file with tifffile: {e}")
        logger.error("Attempting to load with asarray(0) and manually extract metadata")
        try:
            arr = tif.asarray(0)
        except Exception as e:
            logger.error(f"Error loading tiff file with asarray: {e}")
            return None, None
        if tif.ome_metadata is None:
            if len(arr.shape) == 3 and arr.shape[2] == 3:
                dict_out["channels"] = ["red", "green", "blue"]
            else:
                return None, None
        else:
            # exrtract chanenls
            dict_out = extract_ome_metadata(tif, dict_out)
            dict_out["size_x"] = arr.shape[1]
            dict_out["size_y"] = arr.shape[0]

            # curate channels
            dict_out = extract_more_metadata_if_available(tif_path, dict_out)
            dict_out["channels"], arr = standardize_channels(arr, dict_out["channels"])
            return arr, dict_out
    if IS_OME_TIFF:
        # read with pyometiff
        if not IS_ULTRA_HIGH_RES:
            # dont read image data
            arr, metadata = read_ome_tiff(tif_path)
            if arr is None or metadata is None:
                raise ValueError("Failed to load image")
            # crop the image if bbox is provided
            if bbox:
                arr = crop_and_pad_image(arr, bbox)

            dict_out.update(metadata)

            # curate channels
            dict_out = extract_more_metadata_if_available(tif_path, dict_out)
            dict_out["channels"], arr = standardize_channels(arr, dict_out["channels"])

            return arr, dict_out

    if not avoid_loading_ultra_high_res_arrays_normaly or not IS_ULTRA_HIGH_RES:
        raise ValueError("Failed to load image")
    # case of "TCZYXS" being actually "TSZYXC"
    if (
        dims_order.lower() == "tczyxs"
        and dims_shape[0] == 1
        and dims_shape[1] == 1
        and dims_shape[5] == 3
    ):
        # this is an rgb image that has wrongly been interpreted as a time series
        dims_order = "TSZYXC"

    # check if x and y are large enough to toggle IS_ULTRA_HIGH_RES variable
    # get the x and y dimensions
    if "x" in dims_order.lower():
        x_dim = dims_order.index("X")
        x_size = dims_shape[x_dim]
        dict_out["size_x"] = x_size
    if "y" in dims_order.lower():
        y_dim = dims_order.index("Y")
        y_size = dims_shape[y_dim]
        dict_out["size_y"] = y_size

    # when loading the thumbnail of a button, we need to load the array in a smarter way
    if not avoid_loading_ultra_high_res_arrays_normaly or not IS_ULTRA_HIGH_RES:
        arr = img.data
        if img.dims.Z > 1:
            arr, dims_order = max_projection(arr, dims_order)
            # do stack later
        try:
            arr = extract_YXC(arr, dims_order).squeeze()
        except Exception as e:
            logger.error(f"Error extracting YXC from {tif_path} , {e}")
            print()
        if bbox:
            arr = crop_and_pad_image(arr, bbox)

    elif IS_PYRAMIDAL:
        # load the thumbnail for the ultra high res image
        if for_thumbnail:
            arr, arr_metadata = open_preview_with_openslide_image_reader(tif_path)
        elif for_interactive_zoom and isinstance(bbox, type(None)):
            # update the scene directly
            get_deep_zoom_by_openslide(
                tif_path, viewport_bounding_box=config.viewport_bounding_box
            )
        elif not isinstance(bbox, type(None)):
            arr = crop_ultra_high_res(tif_path, tile=bbox)
        # This method is for tiff files. If the image is a tiff file, it should have been converted to .svs
        # adjust the dimensions to match openslide
        dict_out.update(arr_metadata)
    elif IS_ULTRA_HIGH_RES:
        if for_thumbnail:
            # load the thumbnail for the ultra high res image
            arr, metadata = extract_tile_data_from_tiff(tif_path, tile_bbox=None)
            dict_out.update(metadata)
            # arr, arr_metadata = open_preview_with_openslide_image_reader(tif_path)
            # This method is for tiff files. If the image is a tiff file, it should have been converted to .svs
            # Mark it for conversion here
            if (
                IS_ULTRA_HIGH_RES
                and avoid_loading_ultra_high_res_arrays_normaly is True
                and for_thumbnail is True
                and for_interactive_zoom is False
            ):
                dict_out["needs_pyramidal_conversion"] = True
        else:
            # get the exact tile
            arr, metadata = extract_tile_data_from_tiff(tif_path, tile_bbox=bbox)

    dict_out = extract_more_metadata_if_available(tif_path, dict_out)
    dict_out["channels"], arr = standardize_channels(arr, dict_out["channels"])

    if isinstance(dict_out["channels"], str):
        dict_out["channels"] = [dict_out["channels"]]
    print(arr.shape)
    return arr, dict_out


def create_large_compressed_image_from_ultra_high_res_tiled_image(
    ultra_high_res_path, temp_dir, quality=90, compress=False
):
    """
    Create a large image from a list of tile paths.

    Args:
    - ultra_high_res_path: Path to the ultra high resolution image file.

    - tile_paths: A 2D list of paths to the tile images, organized in [row][column] order.
    - output_path: Path where the final large image will be saved.
    - tile_width, tile_height: Dimensions of each tile.
    - grid_width, grid_height: The number of tiles in each dimension.
    """
    import math
    import os
    import zlib

    import pyvips

    # Open the .svs file with pyvips
    image = pyvips.Image.new_from_file(ultra_high_res_path, access="sequential")

    # Convert to RGB if it's not already (some SVS files might be CMYK or other formats)
    if image.bands == 4:  # Assuming the last band is alpha
        image = image[0:3]  # Drop the alpha channel

    # Calculate number of tiles needed
    MAX_DIMENSION = 65000  # Slightly below JPEG limit of 65500
    width = image.width
    height = image.height

    if width <= MAX_DIMENSION and height <= MAX_DIMENSION:
        # Image is small enough to save directly
        img_path = os.path.join(temp_dir, "tmp.jpg")
        image.jpegsave(img_path, Q=quality)
    else:
        # Need to tile the image
        n_cols = math.ceil(width / MAX_DIMENSION)
        n_rows = math.ceil(height / MAX_DIMENSION)

        # Create a directory for tiles
        tiles_dir = os.path.join(temp_dir, "tiles")
        os.makedirs(tiles_dir, exist_ok=True)

        # Save image as tiled pyramid TIFF instead
        img_path = os.path.join(temp_dir, "tmp.tif")
        image.tiffsave(
            img_path,
            compression="jpeg",
            Q=quality,
            pyramid=True,
            tile=True,
            tile_width=1024,
            tile_height=1024,
            bigtiff=True,
        )

    if compress:
        # Compress with zlib without having to read the whole file to memory
        with open(img_path, "rb") as f:
            compressed = zlib.compress(f.read())

        # Write the compressed data to a new file
        final_path = img_path.replace(os.path.splitext(img_path)[1], ".zip")
        with open(final_path, "wb") as f:
            f.write(compressed)
        return final_path

    return img_path


def run_with_timeout(primary_func, image_path, timeout=5):
    import queue
    import threading

    result_queue = queue.Queue()

    def function_wrapper():
        result_queue.put(primary_func(image_path))

    thread = threading.Thread(target=function_wrapper)
    thread.start()

    thread.join(timeout=timeout)

    if thread.is_alive():
        print("Image reading is taking too long.")
        try:
            thread._stop()
        except:
            pass
        return None
    else:
        print("Primary function completed within time limit.")
        return result_queue.get()  # return the result of the function


# def downsample_and_crop_tiff(filename, output_size, crop_box):
#     """
#     Downsample and crop a TIFF image.

#     :param filename: Path to the TIFF image file.
#     :param output_size: Tuple of (height, width) for the output image.
#     :param crop_box: Tuple of (start_row, end_row, start_col, end_col) for the cropping box.
#     :return: Downsampled and cropped image as a Dask array.
#     """
#     import dask
#     import dask.array as da
#     import imageio

#     # Read the image as a Dask array
#     lazy_image = dask.delayed(imageio.imread)
#     lazy_dask_image = da.from_delayed(
#         lazy_image, shape=sample.shape, dtype=sample.dtype
#     )
#     dask_image.imread.imread("raw/*.tif")

#     # Crop the image
#     start_row, end_row, start_col, end_col = crop_box
#     cropped_image = dask_image[start_row:end_row, start_col:end_col]

#     # Calculate step size for downsampling
#     crop_height, crop_width = end_row - start_row, end_col - start_col
#     output_height, output_width = output_size
#     step_size_height = max(1, crop_height // output_height)
#     step_size_width = max(1, crop_width // output_width)

#     # Downsample the image
#     downsampled_image = cropped_image[::step_size_height, ::step_size_width]

#     return downsampled_image


# def downsample_zarr(dataset_path):
#     import zarr
#     import dask
#     from skimage import exposure, img_as_ubyte

#     original = zarr.open_array(dataset_path)

#     da = dask.array.from_zarr(original)

#     transformed = dask.array.map_blocks(
#         lambda x=da: img_as_ubyte(exposure.rescale_intensity(x)), dtype="uint16"
#     )

#     print("Rescaling complete!")

#     zarr.save_array("path/you/want/for/saved.zarr", transformed)

#     print("Zarr saved!")


def extract_tile_data_from_tiff(tiff_path, tile_bbox=None, forced_resolution=None):
    # Extract a tile from the TIFF image.
    # If tile is None, the entire image is returned.

    import numpy as np
    import tifffile
    import zarr

    metadata = {}
    # Open the TIFF file
    try:
        with tifffile.TiffFile(tiff_path) as tif:
            position1_series = tif.series[0]
            logger.debug(f"zarr: {zarr}")
            position1_zarr = zarr.open(position1_series.aszarr(), mode="r")

            if not forced_resolution:
                target_size = config.IMAGE_THUMBNAIL_MAX_SIZE
            else:
                target_size = forced_resolution

            x_size = position1_series.sizes["width"]
            y_size = position1_series.sizes["height"]
            metadata["size_x"] = x_size
            metadata["size_y"] = y_size

            if isinstance(tile_bbox, type(None)):
                tile_bbox = (0, 0, x_size, y_size)

            y1 = max(0, int(tile_bbox[1]))
            y2 = min(y_size, int(tile_bbox[1]) + int(tile_bbox[3]))
            x1 = max(0, int(tile_bbox[0]))
            x2 = min(x_size, int(tile_bbox[0]) + int(tile_bbox[2]))

            # Calculate and limit downsample factors
            downsample_factor_y = max(1, min((y2 - y1) // target_size, y2 - y1))
            downsample_factor_x = max(1, min((x2 - x1) // target_size, x2 - x1))

            try:
                # Attempt to read with calculated downsample factors
                downsampled_image = position1_zarr[
                    y1:y2:downsample_factor_y, x1:x2:downsample_factor_x
                ]
            except KeyError:
                # Fallback: read full region and downsample manually
                full_region = position1_zarr[y1:y2, x1:x2]
                downsampled_image = full_region[
                    ::downsample_factor_y, ::downsample_factor_x
                ]

    except Exception as e:
        logger.error(f"Error extracting tile data from {tiff_path}: {e}")
        logger.info("Falling back to tifffile for thumbnail")
        from tiffslide import TiffSlide

        slide = TiffSlide(tiff_path)
        downsampled_image = slide.get_thumbnail((target_size, target_size))
        downsampled_image = np.array(downsampled_image)
        metadata["size_x"] = slide.dimensions[0]
        metadata["size_y"] = slide.dimensions[1]
    return downsampled_image, metadata


def interactive_untiled_tiff_preview(tiff_path, tile_bbox=None):
    """
    Function to interactively preview a portion of an untiled TIFF image.
    This method is used when the TIFF file is converting, but the user has already zoomed in on a portion of the image.
    He therfor requires to see that portion of the image in a higher resolution, but this needs to be done efficiently.
    We accomplish that through zarr and tifffile.

    Parameters:
    tiff_path (str): Path to the TIFF file.
    target_size (int, optional): The target size for the zoomed view. Default is 2500.
    cursor_pos (tuple, optional): The cursor position for the zoomed view. Default is None, which means the center of the image.
    zoom_factor (float, optional): The zoom factor for the zoomed view. Default is 1.1.

    Returns:
    downsampled_image (numpy.ndarray): The zoomed and dynamically downsampled portion of the image.
    (y1, y2, x1, x2) (tuple): The coordinates of the cropped region in the original image.

    """
    import numpy as np
    import tifffile
    import zarr
    from PyQt6 import QtGui

    if isinstance(tile_bbox, type(None)):
        return
    # Open the TIFF file
    with tifffile.TiffFile(tiff_path) as tif:
        position1_series = tif.series[0]

        # Convert to Zarr array for efficient processing
        position1_zarr = zarr.open(position1_series.aszarr(), mode="r")

        if isinstance(tile_bbox, type(None)):
            return

        target_size = 2000

        # Calculate the coordinates for the cropped region
        y1 = int(max(0, tile_bbox[1]))
        y2 = int(min(position1_zarr.shape[0], tile_bbox[1] + tile_bbox[3]))
        x1 = int(max(0, tile_bbox[0]))
        x2 = int(min(position1_zarr.shape[1], tile_bbox[0] + tile_bbox[2]))

        # Calculate the downsampling factor
        downsample_factor_y = round(max(1, (y2 - y1) // target_size))
        downsample_factor_x = round(max(1, (x2 - x1) // target_size))

        # Load and return the zoomed and dynamically downsampled portion of the image
        downsampled_image = position1_zarr[
            y1:y2:downsample_factor_y, x1:x2:downsample_factor_x
        ]

        bytesPerLine = downsampled_image.shape[1] * downsampled_image.shape[2]
        # load from numpy array
        qimage = QtGui.QImage(
            downsampled_image.copy(),
            downsampled_image.shape[1],
            downsampled_image.shape[0],
            bytesPerLine,
            QtGui.QImage.Format.Format_RGB888,
        )
        pixmap = QtGui.QPixmap.fromImage(qimage)
        # add pixmap to scene
        config.global_signals.add_partial_slide_images_to_scene_signal.emit(
            {
                "image_data": [pixmap],
                "image_bounding_box": [tile_bbox],
                "image_name": os.path.basename(tiff_path),
                "downsample": downsample,
            }
        )

        return downsampled_image, (y1, y2, x1, x2)


def reorder_array(arr, input_order, dim_sizes, output_order="TZCYX"):
    """
    Reorders a squeezed numpy array according to the given output order.

    Parameters:
    arr (numpy.ndarray): The input squeezed array.
    input_order (str): The order of dimensions in the input array (e.g., 'XYZCT').
    dim_sizes (dict): A dictionary containing the sizes of each dimension (e.g., {'X': 256, 'Y': 256, 'Z': 64, 'C': 3, 'T': 100}).
    output_order (str): The desired order of dimensions in the output array (default: 'TZCYX').

    Returns:
    numpy.ndarray: The reordered array.
    """

    # Check if input_order and output_order have the same length
    if len(input_order) != len(output_order):
        raise ValueError("input_order and output_order must have the same length")

    # Check if input_order and output_order have the same unique characters
    if set(input_order) != set(output_order):
        raise ValueError(
            "input_order and output_order must have the same unique characters"
        )

    # Initialize an empty dictionary for the current dimension indices
    current_dim_indices = {}

    # Assign the current dimension indices based on the input_order
    for i, dim in enumerate(input_order):
        current_dim_indices[dim] = i

    # Calculate the target shape based on the output_order and dim_sizes
    target_shape = tuple(dim_sizes[dim] for dim in output_order)

    # Create an empty array with the target shape
    reordered_arr = np.empty(target_shape, dtype=arr.dtype)

    # Iterate over all possible indices in the output array
    for t_idx in range(dim_sizes["T"]):
        for z_idx in range(dim_sizes["Z"]):
            for y_idx in range(dim_sizes["Y"]):
                for x_idx in range(dim_sizes["X"]):
                    for c_idx in range(dim_sizes["C"]):
                        # Get the current indices based on the input_order
                        current_indices = (
                            x_idx if "X" in current_dim_indices else 0,
                            y_idx if "Y" in current_dim_indices else 0,
                            z_idx if "Z" in current_dim_indices else 0,
                            c_idx if "C" in current_dim_indices else 0,
                            t_idx if "T" in current_dim_indices else 0,
                        )
                        reordered_indices = tuple(
                            current_indices[current_dim_indices[dim]]
                            for dim in output_order
                        )

                        # Assign the value from the input array to the output array at the reordered indices
                        reordered_arr[reordered_indices] = arr[current_indices]

    return reordered_arr


def get_optimal_crop_bbox(
    image_width,
    image_height,
    bbox,
    class_id=None,
    ideal_annotation_to_image_ratio=None,
    retain_object_ratio_from_previous_inference=False,
):
    """
    Calculate the optimal crop size.

    :param image_width: Width of the original image
    :param image_height: Height of the original image
    :param bbox: A tuple (x_min, y_min, x_max, y_max) representing the bounding box
    :param class_id: Optional class ID for specific ratio mapping
    :return: A tuple (x_min, y_min, width, height) representing the crop coordinates
    """
    bbox_width = bbox[2] - bbox[0]
    bbox_height = bbox[3] - bbox[1]
    assert image_width > bbox_width
    if ideal_annotation_to_image_ratio is None:
        ideal_annotation_to_image_ratio = (
            config.MAGIC_BOX_2_MIN_ANNOTATION_PERCENT_SIZE
            + config.MAGIC_BOX_2_MAX_ANNOTATION_PERCENT_SIZE
        ) / 2

    if retain_object_ratio_from_previous_inference:
        average_size = config.CLASS_REGISTRY_WIDTH.get(class_id, 0)
        if average_size == 0:
            average_size = (bbox_width + bbox_height) / 2
    else:
        average_size = (bbox_width + bbox_height) / 2

    crop_size = min(
        average_size / ideal_annotation_to_image_ratio, max(image_width, image_height)
    )

    # Center the crop around the bounding box
    center_x = (bbox[0] + bbox[2]) / 2
    center_y = (bbox[1] + bbox[3]) / 2

    # Initial crop coordinates
    x_min = center_x - (crop_size / 2)
    x_max = center_x + (crop_size / 2)
    y_min = center_y - (crop_size / 2)
    y_max = center_y + (crop_size / 2)

    # Final boundary checks
    x_min = max(0, x_min)
    x_max = min(image_width, x_max)
    y_min = max(0, y_min)
    y_max = min(image_height, y_max)

    # Make square while respecting image boundaries
    width = x_max - x_min
    height = y_max - y_min
    if width != height:
        # needs to be max , if we use min sometimes it crops
        # the subject.
        target_size = max(width, height)
        # Adjust to maintain center while making square
        x_adjust = (width - target_size) / 2
        y_adjust = (height - target_size) / 2

        x_min += x_adjust
        x_max -= x_adjust
        y_min += y_adjust
        y_max -= y_adjust

    return (x_min, y_min, x_max - x_min, y_max - y_min)


def crop_and_pad_image(image_array, tile, color_value=[125, 125, 125]):
    import math

    x, y, width, height = (
        math.ceil(tile[0]),
        math.ceil(tile[1]),
        math.ceil(tile[2]),
        math.ceil(tile[3]),
    )

    # Initialize padding variables
    padding_top, padding_bottom, padding_left, padding_right = 0, 0, 0, 0

    # Calculate effective width and height
    effective_width = min(width, image_array.shape[1] - max(x, 0))
    effective_height = min(height, image_array.shape[0] - max(y, 0))

    # Determine padding needs
    if x + width > image_array.shape[1]:  # Padding on the right
        padding_right = (x + width) - image_array.shape[1]

    if x < 0:  # Padding on the left
        padding_left = -x
        effective_width = min(width + x, image_array.shape[1])

    if y + height > image_array.shape[0]:  # Padding on the bottom
        padding_bottom = (y + height) - image_array.shape[0]

    if y < 0:  # Padding on the top
        padding_top = -y
        effective_height = min(height + y, image_array.shape[0])

    # Crop the image considering boundaries
    cropped_image = image_array[
        max(y, 0) : max(y, 0) + effective_height,
        max(x, 0) : max(x, 0) + effective_width,
    ]

    # Add padding
    image_with_padding = cv2.copyMakeBorder(
        cropped_image,
        math.ceil(padding_top),
        math.ceil(padding_bottom),
        math.ceil(padding_left),
        math.ceil(padding_right),
        cv2.BORDER_CONSTANT,
        value=color_value,
    )

    return image_with_padding


def crop_ultra_high_res(slide_path, tile, pad=True, resolution=1024):
    import openslide

    slide = openslide.OpenSlide(slide_path)

    x, y, width, height = tile

    # tile_as_a_percent_of_the_image = (width * height) / (slide.dimensions[0] * slide.dimensions[1])
    # Determine the appropriate level to meet the minimum resolution requirement
    level = 0
    for i, (lvl_width, lvl_height) in enumerate(slide.level_dimensions):
        level = i
        downsample = slide.level_downsamples[level]
        if (
            int(width / downsample) >= resolution
            and int(height / downsample) >= resolution
        ):
            continue
        else:
            break  # Stop when the next level does not meet the minimum resolution

    # Get the downsample rate for the selected level
    downsample = slide.level_downsamples[level]
    x_downsampled = int(x / downsample)
    y_downsampled = int(y / downsample)
    width_downsampled = int(width / downsample)
    height_downsampled = int(height / downsample)

    # Initialize padding variables
    padding_top, padding_bottom, padding_left, padding_right = 0, 0, 0, 0

    # Calculate dimensions at the selected level
    level_width, level_height = slide.level_dimensions[level]

    # Calculate effective width and height considering the image boundaries
    effective_width = min(width_downsampled, level_width - max(x_downsampled, 0))
    effective_height = min(height_downsampled, level_height - max(y_downsampled, 0))

    # Determine padding needs
    if x_downsampled + width_downsampled > level_width:  # Padding on the right
        padding_right = (x_downsampled + width_downsampled) - level_width

    if x_downsampled < 0:  # Padding on the left
        padding_left = -x_downsampled
        effective_width = min(width_downsampled + x_downsampled, level_width)

    if y_downsampled + height_downsampled > level_height:  # Padding on the bottom
        padding_bottom = (y_downsampled + height_downsampled) - level_height

    if y_downsampled < 0:  # Padding on the top
        padding_top = -y_downsampled
        effective_height = min(height_downsampled + y_downsampled, level_height)

    # Read the region considering the level and effective dimensions
    cropped_image = slide.read_region(
        (max(int(tile[0]), 0), max(int(tile[1]), 0)),
        level,
        (effective_width, effective_height),
    )
    cropped_image = np.array(cropped_image)[
        :, :, 0:3
    ]  # Convert PIL Image to NumPy array and drop alpha channel
    print("Requested tile : ", tile)
    print("Original dimentions : ", slide.dimensions)
    print("Cropped xy : ", (max(x_downsampled, 0), max(y_downsampled, 0)))
    print("Cropped width, height : ", (effective_width, effective_height))
    print("Padding : ", (padding_top, padding_bottom, padding_left, padding_right))

    # Add padding
    image_with_padding = cv2.copyMakeBorder(
        cropped_image,
        padding_top,
        padding_bottom,
        padding_left,
        padding_right,
        cv2.BORDER_CONSTANT,
        value=[0, 0, 0],
    )

    return image_with_padding


def generate_complete_spiral_tiles(
    img_width, img_height, initial_bbox, overlap, skip_lower_than_overlap=False
) -> list:
    """
    Generate tiles boxes starting from the center of the image with an overlap between the generated tiles
    Args:
    img_width: int, width of the image
    img_height: int, height of the image
    initial_bbox: list, [x, y, width, height] of the initial bounding box
    overlap: int, overlap between the tiles

    Returns:
    list of tiles boxes
    """
    # case were the image is smaller than the initial bounding box
    if img_width < initial_bbox[2] or img_height < initial_bbox[3]:
        return [
            [0, 0, max(img_width, initial_bbox[2]), max(img_height, initial_bbox[3])]
        ]

    def within_image(x, y, w, h, ov):
        return 0 < (x + w - ov) < (w + img_width - ov) and 0 < (y + h - ov) < (
            img_height + h - ov
        )

    def calculate_lines(width, line_length, initial_position, overlap):
        # Calculate the effective length of each line after the first one
        effective_length = line_length - overlap

        # Initialize count of lines on the left and right of the initial line
        lines_left = 0
        lines_right = 0

        if initial_position > 0:
            lines_left += 1
            # Calculate lines on the left side
            start_pos_left = initial_position - line_length
            while start_pos_left >= 0:
                lines_left += 1
                start_pos_left -= effective_length

        if initial_position + line_length - overlap < width:
            lines_right += 1
            # Calculate lines on the right side
            start_pos_right = initial_position + line_length
            while start_pos_right + overlap <= width:
                lines_right += 1
                start_pos_right += effective_length

        # Total lines = lines on left + initial line + lines on right
        total_lines = lines_left + 1 + lines_right

        return total_lines

    # Calculate tile width and height from the initial bounding box
    tile_width, tile_height = initial_bbox[2], initial_bbox[3]

    # Initialize variables for spiral generation
    x, y = initial_bbox[0], initial_bbox[1]  # Starting point
    dx, dy = tile_width - overlap, 0  # Initial direction
    steps = 1
    # img = np.zeros((img_height, img_width, 3), dtype=np.uint8)

    tiles = []
    visited = set()  # Keep track of visited coordinates to avoid duplication

    effective_tile_width = tile_width - overlap
    effective_tile_height = tile_height - overlap
    tot_width_lines = calculate_lines(img_width, tile_width, x, overlap)
    tot_height_lines = calculate_lines(img_height, tile_height, y, overlap)
    tot_tiles = tot_width_lines * tot_height_lines

    left_most_point = initial_bbox[0]
    right_most_point = initial_bbox[0] + tile_width
    top_most_point = initial_bbox[1]
    bottom_most_point = initial_bbox[1] + tile_height

    arm_iterations = 0  # should be a max of 2

    while len(tiles) < tot_tiles:
        if arm_iterations > 2:
            break
        arm_iterations += 1
        for _ in range(2):  # Two iterations for each spiral arm
            for step in range(steps):
                if (
                    within_image(x, y, tile_width, tile_height, overlap)
                    and (x, y) not in visited
                ):
                    arm_iterations = 0
                    left_most_point = min(left_most_point, x)
                    right_most_point = max(right_most_point, x + tile_width)
                    top_most_point = min(top_most_point, y)
                    bottom_most_point = max(bottom_most_point, y + tile_height)

                    tiles.append([x, y, tile_width, tile_height])
                    visited.add((x, y))
                    # cv2.rectangle(
                    #     img,
                    #     (int(x), int(y)),
                    #     (int(x + tile_width), int(y + tile_height)),
                    #     (255, 255, 255),
                    #     3,
                    # )
                    # cv2.imwrite("debug.jpg", img)
                    # time.sleep(0.5)
                x, y = x + dx, y + dy
            # Change direction clockwise: (right, down), (down, left), (left, up), (up, right)
            dx, dy = -dy, dx
        steps += 1  # Increase steps for each spiral loop

    # remove any tiles that have any side inside the image smaller than the overlap
    filtered_tiles = []
    if skip_lower_than_overlap:
        for tile in tiles:
            if img_width - (tile[0]) < overlap:
                # skip tile, tile too much to the right
                continue
            if img_height - (tile[1]) < overlap:
                # skip tile, tile too much to the bottom
                continue
            if (tile[0] + tile[2]) < overlap:
                # skip tile, tile too much to the left
                continue
            if (tile[1] + tile[3]) < overlap:
                # skip tile, tile too much to the top
                continue
            filtered_tiles.append(tile)
        tiles = filtered_tiles

    return tiles


# tiles = generate_complete_spiral_tiles(1000, 1912, [600, 505, 100, 100], 95)


# for x in range(1000, 5000, 57):
#     for y in range(1000, 5000, 76):
#         for s in range(300, 1000, 93):
#             start = time.time()
#             tiles = generate_complete_spiral_tiles(x, y, [600, 505, s, s], 95)
#             print(f"Time taken for {x}x{y} at {s} is {time.time() - start}")
#             print(len(tiles))


if __name__ == "__main__":
    unittest.main()
