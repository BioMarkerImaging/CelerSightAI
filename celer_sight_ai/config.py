import logging
import os
import pathlib
import queue
import sys
import threading
from enum import Enum


def stop_jvm():
    try:
        javabridge.kill_vm()
    except:
        pass


def start_jvm():
    if not javabridge.get_env():  # Check if JVM is already running

        javabridge.start_vm(class_path=bioformats.JARS, run_headless=True)
        """(From pskeshu) This is so that Javabridge doesn't spill out a lot of DEBUG messages
        during runtime.
        From CellProfiler/python-bioformats.
        """
        try:  # patch the log level to warn
            rootLoggerName = javabridge.get_static_field(
                "org/slf4j/Logger", "ROOT_LOGGER_NAME", "Ljava/lang/String;"
            )

            rootLogger = javabridge.static_call(
                "org/slf4j/LoggerFactory",
                "getLogger",
                "(Ljava/lang/String;)Lorg/slf4j/Logger;",
                rootLoggerName,
            )

            logLevel = javabridge.get_static_field(
                "ch/qos/logback/classic/Level", "WARN", "Lch/qos/logback/classic/Level;"
            )

            javabridge.call(
                rootLogger, "setLevel", "(Lch/qos/logback/classic/Level;)V", logLevel
            )
        except Exception as e:
            print(f"Failed to patch log level: {e}")


jvm_lock = threading.RLock()


logger = logging.getLogger(__name__)
is_executable = hasattr(sys, "frozen")
latest_magic_box_name = None

app_home = None

if is_executable:
    app_home = sys._MEIPASS
    # on mac os
    os.environ["CELER_SIGHT_AI_HOME"] = app_home
    logger.info("Celer Sight AI Home: " + app_home)
    sys.path.append(app_home)
    # also append the celer_sight_ai folder
    sys.path.append(os.path.join(app_home, "celer_sight_ai"))
    os.chdir(os.path.join(app_home, "celer_sight_ai"))
    if os.name == "nt":
        os.environ["JAVA_HOME"] = os.path.join(app_home, "java")
        os.environ["CP_JAVA_HOME"] = os.path.join(app_home, "java")
    else:
        os.environ["JAVA_HOME"] = os.path.join(app_home, "Home")
        os.environ["CP_JAVA_HOME"] = os.path.join(app_home, "Home")
    print(f"Java home: {os.environ['JAVA_HOME']}")
    print(f"Running from frozen executable, setting path to {app_home}")
else:
    # get parent path of the current file
    p = pathlib.Path(__file__).parent.absolute()
    os.environ["CELER_SIGHT_AI_HOME"] = str(p)
    # get parent path
    sys.path.append(str(p))

import bioformats
import javabridge

from celer_sight_ai import __version__


def dbg_image(img, bbox=None, mode: str = "xywh", rescale_image=(0, 0), points=[]):
    """
    On installations, we cannot write on disk, use this to avoid erros
    Args:
        img (np.ndarray): the image to save
        bbox (list): the bbox to draw on the image in format [x1, y1, x2, y2]
        mode (str): the mode to draw the bbox in, "xywh" or "xyxy"
        rescale_image (tuple): dimensions to resize the image to (width, height)
        points (list or np.ndarray): points to draw on the image as circles
    """
    import cv2
    import numpy as np

    if is_executable:
        return
    image_drawn = img.copy()
    if rescale_image != (0, 0):
        image_drawn = cv2.resize(image_drawn, rescale_image)
    if len(points) > 0:
        # Convert numpy array to list of points if needed
        if isinstance(points, np.ndarray):
            if points.ndim == 2 and points.shape[1] == 2:
                # Handle 2D array of points
                for point in points:
                    cv2.circle(
                        image_drawn, (int(point[0]), int(point[1])), 5, (0, 0, 255), -1
                    )
            else:
                print(f"Warning: points array has unexpected shape: {points.shape}")
        else:
            # Original behavior for list of points
            for point in points:
                color = (0, 0, 255)
                if len(point) == 3:
                    point_pos = point[:2]
                    if point[2] == 1:
                        color = (0, 0, 255)
                    else:
                        color = (0, 255, 0)
                else:
                    point_pos = point
                point_pos = (int(point_pos[0]), int(point_pos[1]))
                image_drawn = cv2.circle(image_drawn, point_pos, 5, color, -1)
    if not isinstance(bbox, type(None)):
        # draw bbox on the image

        if mode == "xywh":
            cv2.rectangle(
                image_drawn,
                (int(bbox[0]), int(bbox[1])),
                (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3])),
                (0, 255, 0),
                2,
            )
        elif mode == "xyxy":
            cv2.rectangle(
                image_drawn,
                (int(bbox[0]), int(bbox[1])),
                (int(bbox[2]), int(bbox[3])),
                (0, 255, 0),
                2,
            )

    try:
        cv2.imwrite("test.jpg", image_drawn)
    except Exception as e:
        print(f"Error saving image: {e}")


def dbg_multiple_images(images):
    # shows multiple images of the same size in a grid
    import cv2
    import numpy as np

    if is_executable:
        return False

    # Create a grid of images
    num_images = len(images)
    if num_images == 0:
        logger.error("No images provided to dbg_multiple_images")
        return False

    # Convert float images to uint8 if needed and ensure all images are 3-channel
    processed_images = []
    for img in images:
        # Handle float images
        if img.dtype == np.float32 or img.dtype == np.float64:
            # Map float values to 0-255 range
            img_normalized = (
                np.clip(img, 0, 1) * 255 if np.max(img) <= 1.0 else np.clip(img, 0, 255)
            )
            img = img_normalized.astype(np.uint8)

        # Convert grayscale to RGB if needed
        if len(img.shape) == 2 or (len(img.shape) == 3 and img.shape[2] == 1):
            img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
        elif len(img.shape) == 3 and img.shape[2] == 4:  # Handle RGBA
            img = cv2.cvtColor(img, cv2.COLOR_RGBA2BGR)

        processed_images.append(img)

    # Determine the number of rows and columns for the grid
    num_rows = int(np.ceil(np.sqrt(num_images)))
    num_cols = int(np.ceil(num_images / num_rows))

    # Create a new image to hold the grid
    grid_size = (
        num_cols * processed_images[0].shape[1],
        num_rows * processed_images[0].shape[0],
    )
    grid_image = np.zeros((grid_size[1], grid_size[0], 3), dtype=np.uint8)

    # Fill the grid with the images
    for i, img in enumerate(processed_images):
        row = i // num_cols
        col = i % num_cols
        grid_image[
            row * img.shape[0] : (row + 1) * img.shape[0],
            col * img.shape[1] : (col + 1) * img.shape[1],
        ] = img

    # Save the grid image to disk
    try:
        cv2.imwrite("test.jpg", grid_image)
        return True
    except Exception as e:
        logger.error(f"Error saving grid image: {e}")
        return False


def unregister_url_scheme():
    if os.name == "nt":
        import winreg

        try:
            # Delete the entire CelerSight key and all its subkeys
            winreg.DeleteKey(
                winreg.HKEY_CURRENT_USER,
                r"Software\Classes\CelerSight\shell\open\command",
            )
            winreg.DeleteKey(
                winreg.HKEY_CURRENT_USER, r"Software\Classes\CelerSight\shell\open"
            )
            winreg.DeleteKey(
                winreg.HKEY_CURRENT_USER, r"Software\Classes\CelerSight\shell"
            )
            winreg.DeleteKey(winreg.HKEY_CURRENT_USER, r"Software\Classes\CelerSight")
            print("URL scheme unregistered successfully")
        except OSError as e:
            print(f"Failed to unregister URL scheme: {e}")
    elif os.name == "posix":
        # Remove the plist file on macOS
        plist_path = os.path.expanduser(
            "~/Library/Preferences/com.BioMarkerImaging.CelerSight.plist"
        )
        try:
            if os.path.exists(plist_path):
                os.remove(plist_path)
                print("URL scheme unregistered successfully")
        except Exception as e:
            print(f"Failed to unregister URL scheme: {e}")


def dbg_polygon(
    polygon_vertices,
    image_shape,
) -> bool:

    # Writes a polygon to disk as a binary mask image.

    # Args:
    #     polygon_vertices (List[np.ndarray]): List of vertex arrays where first array is the outer polygon
    #                                         and subsequent arrays are holes
    #     output_path (str): Path where the mask should be saved
    #     image_shape (Tuple[int, int]): Shape of the output mask (height, width)

    # Returns:
    #     bool: True if successful, False otherwise

    # Example:
    #     write_polygon_as_mask(mask_obj.get_array(), 'path/to/mask.png', (512, 512))

    import cv2
    import numpy as np
    from skimage.draw import polygon

    if is_executable:
        return False
    try:
        # Create empty mask
        mask = np.zeros(image_shape, dtype=np.uint8)

        if not polygon_vertices or len(polygon_vertices) == 0:
            logger.error("No polygon vertices provided")
            return False

        # Draw outer polygon
        outer_poly = np.array(polygon_vertices[0])
        rr, cc = polygon(outer_poly[:, 0], outer_poly[:, 1], shape=image_shape)
        mask[rr, cc] = 1

        # Draw holes if they exist
        for hole in polygon_vertices[1:]:
            hole = np.array(hole)
            rr, cc = polygon(hole[:, 0], hole[:, 1], shape=image_shape)
            mask[rr, cc] = 0

        # Save mask to disk
        cv2.imwrite("test.jpg", mask * 255)
        return True

    except Exception as e:
        logger.error(f"Error writing polygon mask to disk: {e}")
        return False


def register_url_scheme():
    if os.name == "nt":
        import winreg

        try:
            # Check if the key already exists
            try:
                with winreg.OpenKey(
                    winreg.HKEY_CURRENT_USER,
                    r"Software\Classes\CelerSight",
                    0,
                    winreg.KEY_READ,
                ) as existing_key:
                    # Key exists, no need to register again
                    return
            except OSError:
                # Key doesn't exist, proceed with registration
                pass

            # Register URL scheme
            with winreg.CreateKey(
                winreg.HKEY_CURRENT_USER, r"Software\Classes\CelerSight"
            ) as key:
                winreg.SetValue(key, "", winreg.REG_SZ, "URL:CelerSight Protocol")
                winreg.SetValueEx(key, "URL Protocol", 0, winreg.REG_SZ, "")

                with winreg.CreateKey(key, r"shell\open\command") as cmd_key:
                    if hasattr(sys, "frozen"):
                        app_path = sys.executable
                    else:
                        app_path = os.path.join(
                            os.path.dirname(__file__), "Celer Sight AI.py"
                        )
                    cmd_path = f'"{app_path}" "--url" "%1"'
                    winreg.SetValue(cmd_key, "", winreg.REG_SZ, cmd_path)

        except Exception as e:
            print(f"Failed to register URL scheme: {e}")

    elif os.name == "posix":
        import plistlib

        # macOS - User level registration
        plist_path = os.path.expanduser(
            "~/Library/Preferences/com.BioMarkerImaging.CelerSight.plist"
        )

        # Check if plist already exists and contains the URL scheme
        if os.path.exists(plist_path):
            try:
                with open(plist_path, "rb") as fp:
                    existing_plist = plistlib.load(fp)
                    for url_type in existing_plist.get("CFBundleURLTypes", []):
                        if "CelerSight" in url_type.get("CFBundleURLSchemes", []):
                            # URL scheme already registered
                            return
            except Exception:
                pass

        # Register URL scheme
        plist_data = {
            "CFBundleURLTypes": [
                {
                    "CFBundleURLName": "com.BioMarkerImaging.CelerSight",
                    "CFBundleURLSchemes": ["CelerSight"],
                }
            ]
        }

        try:
            with open(plist_path, "wb") as fp:
                plistlib.dump(plist_data, fp)
        except Exception as e:
            print(f"Failed to register URL scheme: {e}")


def add_open_slide_and_vips_to_sys(test_imports=False):
    import os

    open_slide_path_lib = None
    open_slide_path_bin = None
    # if is frozen
    if is_executable:
        open_slide_path_lib = os.path.join(
            os.environ.get("CELER_SIGHT_AI_HOME"), "open_slide_libs/bin"
        )
        open_slide_path_bin = os.path.join(
            os.environ.get("CELER_SIGHT_AI_HOME"), "open_slide_libs/bin"
        )
        vipshome = os.path.join(os.environ.get("CELER_SIGHT_AI_HOME"), "vips_libs/bin")
    else:

        if os.environ.get("CELER_SIGHT_TESTING") == "true":
            extra_libs_path = "extra_libs"
        else:
            extra_libs_path = "../extra_libs"

        if os.name == "posix":
            open_slide_path = os.path.join(
                os.environ.get("CELER_SIGHT_AI_HOME"),
                f"{extra_libs_path}/open_slide_mac/bin",
            )
            vipshome = os.path.join(
                os.environ.get("CELER_SIGHT_AI_HOME"), f"{extra_libs_path}/vips_mac/bin"
            )

        elif os.name == "nt":
            open_slide_path_bin = os.path.join(
                os.environ.get("CELER_SIGHT_AI_HOME"),
                f"{extra_libs_path}/open_slide_win/bin",
            )
            open_slide_path_lib = os.path.join(
                os.environ.get("CELER_SIGHT_AI_HOME"),
                f"{extra_libs_path}/open_slide_win/lib",
            )
            vipshome = os.path.join(
                os.environ.get("CELER_SIGHT_AI_HOME"),
                f"{extra_libs_path}/vips_libs/bin",
            )
        if os.name == "posix":
            if "DYLD_LIBRARY_PATH" in os.environ:
                os.environ["DYLD_LIBRARY_PATH"] = (
                    open_slide_path + os.pathsep + os.environ.get("DYLD_LIBRARY_PATH")
                )
            else:
                os.environ["DYLD_LIBRARY_PATH"] = open_slide_path
        elif os.name == "nt":
            if "PATH" in os.environ:
                os.environ["PATH"] = (
                    open_slide_path_bin + os.pathsep + os.environ.get("PATH")
                )
            else:
                os.environ["PATH"] = open_slide_path_bin
    os.environ["PATH"] = vipshome + os.pathsep + os.environ["PATH"]
    import os

    if hasattr(os, "add_dll_directory"):
        with os.add_dll_directory(open_slide_path_bin):
            import openslide
    if test_imports:
        import openslide
        import pyvips


i = 0  # number that goes up to 1000000 to allow for trully unique uuids


def get_unique_id():
    import uuid

    global i
    i += 1
    return str(uuid.uuid4()) + str(i)


add_open_slide_and_vips_to_sys()

ram_image = None  # Image loaded to ram for quickly updating the UI
ram_image_path = None  # Path to the image loaded to ram, needed to double check if the current image is the correctly loaded image

track_annotation_map = {}  # map of track id to annotation id
load_main_scene_read_image = False
print("Imported version: " + __version__)
APP_NAME = "celer_sight_ai"
APP_VERSION = __version__
MODULE_DIR = pathlib.Path(__file__).resolve().parent

model_versions = {
    "specialized": "1",
    "general_decoder": "1",
    "general_encoder": "1",
}


cloud_classes = []  # a list of class items that are retrieved from the server

# classes that need a representative image to be applied to the category
categories_that_need_thumbnail = []


from celer_sight_ai.configHandle import getLocal

print("Imported getLocal")
APP_DATA_PATH = getLocal()

TRUSTERD_ROOT_SRC = os.path.join(APP_DATA_PATH, "root.json")

TARGET_DIR = os.path.join(APP_DATA_PATH, "update_cache", "targets")

METADATA_DIR = os.path.join(APP_DATA_PATH, "update_cache", "metadata")


TRUSTED_ROOT_DST = os.path.join(METADATA_DIR, "root.json")

# IS_SMALL_SCREEN  --> is generated when the MainWindow is created
IS_SMALL_SCREEN = False

#  infinity loader button settings
BUTTON_HEIGHT = 85
BUTTON_WIDTH = 85
BUTTON_SPACING = 3
BUTTON_PADDING_LEFT = 0
BUTTON_PADDING_TOP = 3
BUTTON_COLS = 3
IMAGE_PREVIEW_TOP_PAD = (
    2500  # spacing to load buttons past the top of the image preview viewport
)

#  button preview image size
BUTTON_THUMBNAIL_MIN_SIZE = 129  # minimum size for each side of the thumbnail

IMAGE_PREVIEW_BOTTOM_PAD = 2500  # same for bottom
IMAGE_PREVIEW_BUFFER = 2000  # buffer from top or buttom
IMAGE_THUMBNAIL_MAX_SIZE = 1200
IMAGE_THUMBNAIL_JPEG_QUALITY = 60

ULTRA_HIGH_RES_THRESHOLD = 4000

ZOOM_OUT_REZ = 2500  # aim for this resolution on zoom out on ultra high res
SETTINGS_ORG = "BioMarkerImaging"
SETTINGS_APP = "CelerSight"
CLOUD_CATEGORIES_FILE = "model_configs/cloud_categories.json"
LOCAL_CATEGORIES_FILE = "model_configs/local_categories.json"
CATEGORY_REFRESH_INTERVAL = 86400  # 24 hours in seconds

MODEL_UNAVAILABLE_MESSAGE = (
    "Model unavailable, try re-downloading assets (restart the app)."
)


def make_sure_local_dirs_exist():
    if not os.path.exists(TARGET_DIR):
        os.makedirs(TARGET_DIR)
    if not os.path.exists(METADATA_DIR):
        os.makedirs(METADATA_DIR)
    if not os.path.exists(
        os.path.dirname(os.path.join(APP_DATA_PATH, CLOUD_CATEGORIES_FILE))
    ):
        os.makedirs(os.path.dirname(os.path.join(APP_DATA_PATH, CLOUD_CATEGORIES_FILE)))
    if not os.path.exists(
        os.path.dirname(os.path.join(APP_DATA_PATH, LOCAL_CATEGORIES_FILE))
    ):
        os.makedirs(os.path.dirname(os.path.join(APP_DATA_PATH, LOCAL_CATEGORIES_FILE)))


make_sure_local_dirs_exist()

# If file is in this format, open with opencv
NON_SPECIALIZED_IMAGE_FORMATS = [
    ".jpeg",
    ".jpg",
    ".png",
    ".bmp",
    ".tiff",
    ".tif",
    ".webp",
    ".pgm",
    ".ppm",
    ".tga",
    ".jfif",
    ".exr",
    ".hdr",
]
# use bioformats for these formats
# TODO: update to support more formats here
SPECIALIZED_FORMATS = [
    ".tif",
    ".tiff",
]
# If the image is these format and high resolution open with tiffslide
TIFFSLIDE_FORMATS = [".svs", ".tif", ".tiff", ".ndpi", ".scn"]
# if image is these format and does not open with tiffslide, open with openslide
OPENSLIDE_FORMATS = [
    ".ndpi",
    ".svs",  # slide
    ".dcm",
    ".scn",
    ".mrxs",  # slide
    ".tiff",
    ".vms",  # slide
    ".vmu",
    ".bif",
    ".svslide",  # slide
    ".tif",
]
ALL_ACCEPTED_FORMATS = (
    NON_SPECIALIZED_IMAGE_FORMATS + TIFFSLIDE_FORMATS + OPENSLIDE_FORMATS
)

# TILE IMAGE SETTINGS
IS_TILE_SIZE = 3750  # if the image is larger than that on any size, its tilled
DEEPZOOM_TILE_SIZE = 256 * 6

tiles_in_use = []  # list of tile coordinates  that are cached in scene
_deepzoom_pixmaps = (
    []
)  # key: tile_id, value: (graphics_item, bbox, downsample, order, image_name)
_deepzoom_order_counter = 0  # counter for the order of the tiles
_deepzoom_cache_size = 0  # size of the cache in bytes
current_photo_viewer = None

Z_VALUE_BACKGROUND = -9999
Z_VALUE_BACKGROUND_IMAGE = (
    -9000
)  # this can be a normal image or  the background in a pyramidal image


HIGH_RES_SCENE_LAST_UPDATED_POS = None  # last updated position of the high res scene
HIGH_RES_SCENE_POSITION_THRESHOLD = (
    0.001  # in percent of the pixels of the last updated position
)
HIGH_RES_SCENE_LAST_UPDATED_ZOOM = None  # last updated zoom of the high res scene
# obtained with self.transform().m11() at the add_partial_slide_images_to_scene method
HIGH_RES_SCENE_ZOOM_THRESHOLD = 0.001  # in percent of the zoom of the last updated zoom
ULTRA_HIGH_RES_COMPRESSION_QUALITY = 0.99
CURRENT_SAVE_FILE = None  # if we save during the current session or
# load a file, its path will appear here, ctrl + s saves here
VIEWPORT_MIN_RESOLUTION = (
    2000  # minimum resolution to display on ultra high resolution images
)
MAX_DEEPZOOM_OBJECTS = 45
ZOOM_DOWNSAMPLE_THRESHOLDS = {
    "very_high": (2.0, 1.0),  # zoom >= 2.0, downsample = 1.0
    "high": (1.0, 2.0),  # zoom >= 1.0, downsample = 2.0
    "medium": (0.5, 4.0),  # zoom >= 0.5, downsample = 4.0
    "low": (0.25, 8.0),  # zoom >= 0.25, downsample = 8.0
    "very_low": (0.0, 16.0),  # zoom < 0.25, downsample = 16.0
}


### Interactive Magic Tools ###

MAGIC_BOX_1_RESOLUTION = 320
MAGIC_BOX_2_RESOLUTION = 1024
MAGIC_BOX_2_MIN_ANNOTATION_PERCENT_SIZE = 0.06  # the bounding box of the subject of interest is this size compared to the image crop
MAGIC_BOX_2_MAX_ANNOTATION_PERCENT_SIZE = 0.10
MAGIC_BOX_PREDICTOR_UPSCALE = 1  # upscale of 2 means 2x the resolution in x and y

CLASS_REGISTRY_WIDTH = {}  # a register of class_id : annotation_width

## Config file
from celer_sight_ai.MultiChannellImports import (
    ChannelPickerSignals,
    global_vars,
    userAttributesClass,
)

cloud_categories = (
    None  # all possible categories from the server (usually with trained models)
)

supercategory = None  # experiment category, worm , cells, etc, used in online inference
viewport_bounding_box = None  # bounding box of the viewport, constantly updated
# viewport needs to be accessed from threads
extra_mask_items_threshold = 20

# Dictionary to hold the queues for each register
registers = {}

# Dictionary to hold the thread pools (list of threads) for each register
thread_pools = {}

# Lock to manage access to registers and thread_pools
lock = threading.Lock()

max_concurrent_jobs_registers = 2


def threaded_with_registers(register_name):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Ensure the register exists in the dictionaries
            if user_cfg["USER_WORKERS"]:
                with lock:
                    if register_name not in registers:
                        registers[register_name] = queue.Queue()
                        thread_pools[register_name] = []

                    # Start threads if not at max capacity
                    if len(thread_pools[register_name]) < max_concurrent_jobs_registers:
                        for _ in range(
                            max_concurrent_jobs_registers
                            - len(thread_pools[register_name])
                        ):
                            t = threading.Thread(
                                target=worker_for_register, args=(register_name,)
                            )
                            t.daemon = True
                            t.start()
                            thread_pools[register_name].append(t)

                    # Add the job to the queue
                    registers[register_name].put((func, args, kwargs))
            else:
                return func(*args, **kwargs)

        return wrapper

    return decorator


def worker_for_register(register_name):
    while True:
        try:
            if registers[register_name].empty():
                break
            func, args, kwargs = registers[register_name].get(
                timeout=7
            )  # Adjust timeout as needed
            try:
                func(*args, **kwargs)
            finally:
                registers[
                    register_name
                ].task_done()  # Call task_done() only once after processing
        except queue.Empty:
            break
        except Exception as e:
            logger.error(e)
            break
    # Clean up threads list when done
    with lock:
        thread_pools[register_name] = [
            t for t in thread_pools[register_name] if t.is_alive()
        ]


def threaded(func):
    from functools import wraps

    from celer_sight_ai.core.threader import Threader

    @wraps(func)
    def wrapper(*args, **kwargs):
        if user_cfg["USER_WORKERS"]:
            t = Threader(target_function=func, args=args, kwargs=kwargs)
            t.daemon = True
            t.start()
        else:
            return func(*args, **kwargs)

    return wrapper


def q_threaded(func):
    from celer_sight_ai.core.threader import Threader

    @wraps(func)
    def wrapper(*args, **kwargs):
        if user_cfg["USER_WORKERS"]:

            class Worker(QtCore.QThread):
                def run(self):
                    func(*args, **kwargs)

            t = Worker()
            t.daemon = True
            t.start()

            # Store the QThread object in the function's __dict__ attribute
            func.__dict__.setdefault("_threads", []).append(t)
        else:
            return func(*args, **kwargs)

    return wrapper


import cProfile
import io
import pstats
import time
from queue import SimpleQueue
from threading import Lock, Thread

group_locks = {}
group_queues = {}
group_running = {}
group_stop_flags = {}


def group_task(group_name):
    """
    Decorator to manage task execution within a named group, ensuring that only one task runs at a time per group.
    If a new task is added while another is running, the currently running task is stopped and replaced with the new one.

    Args:
        group_name (str): The name of the task group.

    Returns:
        function: The wrapped function with task queue management.

    Usage:
        @group_task('my_group')
        def my_function():
            # Function implementation
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            import time
            import uuid

            if group_name not in group_locks:
                group_locks[group_name] = Lock()
                group_queues[group_name] = []
                group_running[group_name] = False
                group_stop_flags[group_name] = False
            # Set stop flag for currently running task
            if group_running[group_name]:
                group_stop_flags[group_name] = True
            task_uuid = get_unique_id()
            # Queue the new task
            group_queues[group_name].insert(0, (func, args, kwargs, task_uuid))

            # Start the task thread if not already running
            while True:
                if not group_queues[group_name]:
                    if group_running[group_name] == True:
                        group_stop_flags[group_name] = True
                        while group_running[group_name]:
                            time.sleep(0.04)
                    break
                # if group_running[group_name]:
                # check if the task is first in queue, otherwise pop from the end and exit
                if len(group_queues) and task_uuid != group_queues[group_name][0][3]:
                    # If the last added item is not first, remove it and exit
                    group_queues[group_name].pop()
                    return
                # # time.sleep(0.04)
                # continue
                with group_locks[group_name]:
                    if len(group_queues[group_name]):
                        # check if the task is first in queue
                        if task_uuid != group_queues[group_name][0][3]:
                            # If the last added item is not first, remove it and exit
                            group_queues[group_name].pop()  # remove the last element
                            break

                    #############
                    ## RUN TASK##
                    #############

                    group_running[group_name] = True
                    if not group_stop_flags[group_name]:
                        func_to_run = func
                    else:
                        func_to_run, args, kwargs, running_task_uuid = group_queues[
                            group_name
                        ][0]
                    group_queues[group_name] = []
                    try:
                        # Run the task if the stop flag is not set
                        if not group_stop_flags[group_name]:
                            func_to_run(*args, **kwargs)
                    except Exception as e:
                        # Handle exceptions here
                        logger.error(e)
                        pass
                    finally:
                        # Check if the queue is empty or if the stop flag is set for the next task
                        group_running[group_name] = False
                        group_stop_flags[group_name] = False

                    # task_thread = Thread(target=run_task, args=(group_name,))
                    # task_thread.start()
                    break

        return wrapper

    return decorator


from functools import wraps

# Initialize the pool as None to start with
pool = None


def multiprocessed(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if pool is None:
            raise RuntimeError("Multiprocessing pool has not been initialized.")
        result = pool.apipe(func, *args, **kwargs)
        return result.get()

    return wrapper


def get_latest_file_version(root, filename):
    """
    Searches for the latest version of a file 'filename' in root directory
    The filename is f'filename_{version}.extention (extention is optional)
    """
    import re

    # Create a regex pattern to match the filename with version and optional extension
    pattern = re.compile(f"{filename}_([0-9]+)(\..*)?$")

    # Initialize the latest version to -1
    latest_version = -1
    if not os.path.exists(root):
        return None
    # Iterate over all files in the root directory
    for file in os.listdir(root):
        match = pattern.match(file)
        # If the file matches the pattern
        if match:
            # Extract the version number from the match
            version = int(match.group(1))
            # If this version is greater than the latest version found so far
            if version > latest_version:
                # Update the latest version
                latest_version = version

    # If no version of the file was found
    if latest_version == -1:
        return None

    # Return the latest version of the file
    return f"{filename}_{latest_version}"


def is_admin():
    if user_attributes and hasattr(user_attributes, "is_admin"):
        return user_attributes.is_admin
    return False


print("Imported MultiChannellImports")

global global_params
global user_attributes
global_signals = ChannelPickerSignals()
global_params = global_vars()
user_attributes = userAttributesClass()

client = None  # client for the server, instantiate during log in.

inference_buffer = 0
inference_threads = []  # store inference threads here to be able to stop them
stop_inference = False  # flag to stop inference
STARTED_RETRIEVAL = (
    False  # whether or not we are retriving inference results from the server
)

experiment_config = None

contribing_data = False  # while the user is contributing , sending data, its True
USER_CONFIG_LOADED = False

SHOW_CLASSES = True

MBX_INPUT_WIDTH = 320
MBX_INPUT_HEIGHT = 320

import tempfile

# create temp dir for cache
cache_dir_object = tempfile.TemporaryDirectory()
cache_dir = cache_dir_object.name
# add permissions to the cache dir
os.chmod(cache_dir, 0o777)


def get_cache_unique_file_path(filename):
    import uuid

    from celer_sight_ai import config

    filename = os.path.basename(filename)
    if os.path.exists(os.path.join(cache_dir, filename)):
        # create a random name subdir and add it there
        subdir = os.path.join(cache_dir, str(config.get_unique_id()))
        os.makedirs(subdir)
        out_file_name = os.path.join(subdir, filename)
    else:
        out_file_name = os.path.join(cache_dir, filename)
    return out_file_name


def add_to_cache_dir(unique_file_path):
    # make sure the file transfer has unique name
    import shutil
    import uuid

    filename = os.path.basename(unique_file_path)
    dest_path = get_cache_unique_file_path(filename)
    shutil.copy(unique_file_path, dest_path)
    return dest_path


# delete it when the program exits
import atexit
import shutil

atexit.register(cache_dir_object.cleanup)
atexit.register(shutil.rmtree, cache_dir)
home_selection_step = (
    0  # 0: select organism, 1: select part, 2: celer sight main window
)


def get_user_settings():
    import yaml

    user_settings_path = os.path.join(
        os.environ.get("CELER_SIGHT_AI_HOME"), "user_settings.yml"
    )
    # if its frozen, check if user settings exist on the local dir
    if is_executable:
        user_settings_local_dir = os.path.join(getLocal(), "user_settings.yml")
        if not os.path.exists(user_settings_local_dir) and os.path.exists(
            user_settings_path
        ):
            # copy the user settings to the home directory
            # without copying permissions
            os.makedirs(os.path.dirname(user_settings_local_dir), exist_ok=True)
            shutil.copyfile(user_settings_path, user_settings_local_dir)
        with open(user_settings_local_dir) as f:
            return yaml.load(f, Loader=yaml.FullLoader)
    else:
        if os.environ.get("CELER_SIGHT_ALTERNATIVE_SETTINGS", None):
            # This case is almost always used for testing
            with open(os.environ.get("CELER_SIGHT_ALTERNATIVE_SETTINGS")) as f:
                return yaml.load(f, Loader=yaml.FullLoader)
        else:
            # Normal case for development
            if os.path.exists(user_settings_path):
                with open(user_settings_path) as f:
                    return yaml.load(f, Loader=yaml.FullLoader)


import pathlib

from PyQt6 import QtCore

# if "FORGET_PAST_CELER_SIGHT" in os.environ.keys(): then delete all QtCore.QSettings
if "FORGET_PAST_CELER_SIGHT" in os.environ.keys():
    settings = QtCore.QSettings("BioMarkerImaging", "CelerSight")
    settings.clear()
else:
    settings = QtCore.QSettings("BioMarkerImaging", "CelerSight")


class UserConfig:
    def __init__(self, config):
        self._user_cfg = config

    def __getitem__(self, key):
        return self._user_cfg[key]

    def __setitem__(self, key, value):
        self._user_cfg[key] = value

    def __repr__(self):
        return self._user_cfg.__repr__()

    def __str__(self):
        return self._user_cfg.__str__()

    def __getattr__(self, key):
        return self._user_cfg[key]

    def __setattr__(self, key, value):
        if key == "_user_cfg":
            self.__dict__["_user_cfg"] = value
        else:
            self._user_cfg[key] = value

    def __delattr__(self, key):
        del self._user_cfg[key]

    def get(self, key, default=None):
        """
        Get a value from the config, returning default if the key doesn't exist.

        Args:
            key: The key to look up
            default: The value to return if key is not found (defaults to None)

        Returns:
            The value associated with key if it exists, otherwise default
        """
        return self._user_cfg.get(key, default)


visible_channel_cache = {}


def update_visible_channel_cache(channel_name, is_checked):
    visible_channel_cache[channel_name] = is_checked


def get_visible_channel_cache(channel_name, non_cached_value):
    if channel_name in visible_channel_cache:
        return visible_channel_cache[channel_name]
    return non_cached_value


def load_user_settings():
    """
    Loads user settings to config
    """
    is_executable = hasattr(sys, "frozen")
    user_cfg_settings = get_user_settings()
    if not is_executable:  # if in developer mode
        # for debbuging purposes if OVERRIDE_DEV_MODE_CELER_SIGHT is set in the environment
        # treat the system as if it is in production mode
        if "OVERRIDE_DEV_MODE_CELER_SIGHT" in os.environ.keys():
            for k, v in user_cfg_settings["production"].items():
                user_cfg_settings[k] = v
            is_executable = True
        # otherwise use the dev settings
        else:
            for k, v in user_cfg_settings["developer"].items():
                user_cfg_settings[k] = v
    else:
        # production mode
        for k, v in user_cfg_settings["production"].items():
            user_cfg_settings[k] = v
    user_cfg = UserConfig(user_cfg_settings)
    return user_cfg, user_cfg_settings


if not USER_CONFIG_LOADED:
    # user_cfg_settings = get_user_settings()
    USER_CONFIG_LOADED = True
    user_cfg, user_cfg_settings = load_user_settings()

# TODO: update the full list from FluoFinder
channel_colors = {
    "red": (255, 0, 0),
    "green": (0, 255, 0),
    "blue": (0, 0, 255),
    "yellow": (255, 255, 0),
    "cyan": (0, 255, 255),
    "magenta": (255, 0, 255),
    "white": (255, 255, 255),
    "dapi": (0, 0, 255),
    "fitc": (0, 255, 0),
    "tritc": (255, 0, 0),
    "cy5": (255, 255, 0),
    "cy3": (0, 255, 255),
    "cy7": (255, 0, 255),
    "cy5.5": (255, 255, 255),
    "cy3.5": (0, 0, 0),
    "af488": (0, 255, 0),
    "af594": (255, 0, 0),
    "af647": (255, 255, 0),
    "af750": (0, 255, 255),
    "af405": (255, 0, 255),
    "af488": (255, 255, 255),
    "af555": (0, 0, 255),
    "fgw": (255, 0, 0),
    "fbw": (0, 255, 0),
    "gfp": (0, 255, 0),
    "yfp": (255, 255, 0),
    "rfp": (255, 0, 0),
    "dsred": (255, 0, 0),
    "texas red": (255, 0, 0),
    "texas_red": (255, 0, 0),
}
print("Config set!")
bright_colors = [
    (0, 255, 0, 100),  # \ green
    (255, 255, 0, 100),  # yellow
    (255, 0, 0, 100),  # red
    (0, 0, 255, 100),  # blue
    (255, 0, 255, 100),  # magenta
    (0, 255, 255, 100),  # cyan
    (255, 255, 255, 100),  # white
    (255, 128, 0, 100),  # orange
    (128, 0, 255, 100),  # purple
    (0, 128, 255, 100),  # light blue
    (128, 255, 0, 100),  # light green
    (128, 128, 128, 100),  # gray
    (0, 0, 0, 100),  # black
]


def ch_as_str(ch):
    if isinstance(ch, list):
        # Convert RGB list to tuple for comparison
        rgb_tuple = tuple(ch[:3])  # Take first 3 values (RGB, ignore alpha if present)

        # Search through channel_colors for matching RGB values
        for color_name, color_rgb in channel_colors.items():
            if rgb_tuple == color_rgb[:3]:
                return color_name.capitalize()

        # If no exact match found, return RGB as string
        return f"RGB{rgb_tuple}"
    else:
        return str(ch)


class MagicToolModes(Enum):
    MAGIC_BOX_ROI_GENERIC = 0
    MAGIC_BOX_ROI_FINETUNE = 1
    MAGIC_BOX_WITH_PREDICT = 2
    MAGIC_POINT_ROI = 3  # not implemented
    MAGIC_POINT_ROI_WITH_PREDICT = 4  # not implemented


default_experiment_config = {
    "REMOVE_EDGE_ANNOTATIONS": False,
    "REMOVE_EDGE_ANNOTATION_PERCENT": 0.4,  #  The percentage of the pixels of the total Width / Height to use to remove annotations
    "REMOVE_HOLES": True,
    "REMOVE_HOLES_PERCENT": 20,  # any hole with area less than this value (refence is total mask area) will get deleted
}


def progress_hook(bytes_downloaded: int, bytes_expected: int):
    from PyQt6 import QtWidgets

    progress_percent = (float(bytes_downloaded) / float(bytes_expected)) * 100
    print(f"\r{progress_percent:.1f}%", end="")
    global_signals.update_progress_bar_progress_signal.emit(
        {"percent": int(progress_percent)}
    )
    QtWidgets.QApplication.processEvents()
    if progress_percent >= 100:
        global_signals.start_progress_bar_signal.emit(
            {
                "title": "Applying update, please wait as it might take a while.",
                "message": "Validating update",
                "modal": True,
                "percent": 100,
            }
        )
        print("Done")
        QtWidgets.QApplication.processEvents()


def get_update_client():
    import platform

    from celer_sight_ai.configHandle import getServerLogAddress

    logger.info("Getting update client")

    platform_version = None
    if sys.platform.startswith("win"):
        import platform

        architecture = platform.machine()
        # for arm version
        if architecture.lower().startswith("arm"):
            platform_version = "windows_arm"
        else:
            platform_version = "windows_x86"

    elif platform.system() == "Darwin":
        architecture = platform.machine()
        if architecture == "arm64":
            platform_version = "mac_arm"
        else:
            platform_version = "mac_x86"
    try:
        import json

        from tufup.client import Client

        from celer_sight_ai import configHandle

        pre = None
        override_app_install_dir = None
        override_target_dir = None
        override_target_base_url = None
        override_metadata_base_url = None
        override_metadata_dir = None
        override_app_version = None
        root_json_file_path = None

        if os.environ.get("CELER_SIGHT_UPDATE_CONFIG"):
            user_cfg = json.loads(os.environ.get("CELER_SIGHT_UPDATE_CONFIG"))
            override_app_install_dir = user_cfg.get("override_app_install_dir")
            override_target_dir = user_cfg.get("override_target_dir")
            override_target_base_url = user_cfg.get("override_target_base_url")
            override_metadata_base_url = user_cfg.get("override_metadata_base_url")
            override_metadata_dir = user_cfg.get("override_metadata_dir")
            override_app_version = user_cfg.get("override_app_version")
            root_json_file_path = user_cfg.get("root_json_file_path")

        is_executable = hasattr(sys, "frozen")
        logger.info(f"Is executable {is_executable}")

        # if in production use
        if is_executable:
            if os.environ.get("CELER_SIGHT_UPDATE_HOST"):
                update_host = os.environ.get("CELER_SIGHT_UPDATE_HOST")
                # during production and not testing
                METADATA_BASE_URL = f"{update_host}/metadata/"
                TARGET_BASE_URL = f"{update_host}/targets/"
            else:

                # during production and not testing
                METADATA_BASE_URL = f"{getServerLogAddress()}/api/v1/update/{platform_version}/metadata/"
                TARGET_BASE_URL = (
                    f"{getServerLogAddress()}/api/v1/update/{platform_version}/targets/"
                )
        else:
            METADATA_BASE_URL = "http://localhost:8000/repository/metadata/"
            TARGET_BASE_URL = "http://localhost:8000/repository/targets/"
        logger.info(f"URLs - Metadata: {METADATA_BASE_URL}, Target: {TARGET_BASE_URL}")

        if os.name == "posix":
            # on mac Celer Sight AI HOME is Celer Sight AI.app/Contents/MacOS
            INSTALL_DIR = str(
                os.path.dirname(os.path.dirname(os.environ["CELER_SIGHT_AI_HOME"]))
            )
        else:
            INSTALL_DIR = str(os.path.dirname(os.environ["CELER_SIGHT_AI_HOME"]))

        if not override_app_install_dir and not is_executable:
            logger.warning(
                "Cannot update in developer mode, please run the executable or specify an installation directory"
            )
            return False
        INSTALL_DIR = (
            override_app_install_dir if override_app_install_dir else INSTALL_DIR
        )
        if override_app_version:
            APP_VERSION = override_app_version
        else:
            APP_VERSION = __version__
        # The app must ensure dirs exist
        logger.info(f"Initial INSTALL_DIR: {INSTALL_DIR}")
        for dir_path in [INSTALL_DIR, METADATA_DIR, TARGET_DIR]:
            if isinstance(dir_path, str):
                dir_path = pathlib.Path(dir_path)
                dir_path.mkdir(exist_ok=True, parents=True)

        # Make sure that the root.json file exists inside the metadata directory
        if not os.path.exists(os.path.join(METADATA_DIR, "root.json")):
            logger.info("Could not find root.json file in the metadata directory")
            # remove everything except from the root.json file
            for file in os.listdir(METADATA_DIR):
                if file != "root.json":
                    os.remove(os.path.join(METADATA_DIR, file))
            # if root.json file path is provided, copy it to the metadata directory
            if root_json_file_path:
                shutil.copy(
                    root_json_file_path, os.path.join(METADATA_DIR, "root.json")
                )
            # otherwise, retrieve over the network
            else:
                import requests

                try:
                    # Download the root.json file from the server
                    root_json_url = (
                        configHandle.getServerLogAddress()
                        + f"/api/v1/update/get_root_json/{platform_version}"
                    )
                    root_json_file_path = os.path.join(METADATA_DIR, "root.json")
                    resp = requests.get(root_json_url)
                    if resp.status_code == 200:
                        dict_file = resp.json()["root_json"]
                        with open(root_json_file_path, "w") as f:
                            f.write(json.dumps(dict_file))
                    else:
                        raise Exception(
                            f"Failed to download root.json file from {root_json_url}"
                        )
                except Exception as e:
                    logger.error(f"Failed to retrieve root.json: {str(e)}")
                    return False

        # if install dir is None, if is_executable, use the exe parent path
        logger.info(sys.executable)
        logger.info(os.path.dirname(sys.executable))
        logger.info(INSTALL_DIR)
        if not INSTALL_DIR:
            if is_executable:
                INSTALL_DIR = os.path.dirname(sys.executable)
            else:
                raise Exception("Installation directory is not set")

        # debug all input variables
        logger.info(f"pre: {pre}")
        logger.info(f"skip_confirmation: {APP_NAME}")
        logger.info(f"INSTALL_DIR: {INSTALL_DIR}")
        logger.info(f"METADATA_DIR: {METADATA_DIR}")
        logger.info(f"TARGET_DIR: {TARGET_DIR}")
        logger.info(f"APP_VERSION: {APP_VERSION}")
        logger.info(f"root_json_file_path: {root_json_file_path}")
        logger.info(
            f"override_metadata_base_url: {override_metadata_base_url if override_metadata_base_url else METADATA_BASE_URL}"
        )
        logger.info(
            f"override_target_base_url: {override_target_base_url if override_target_base_url else TARGET_BASE_URL}"
        )
        logger.info(
            f"override_target_dir: {override_target_dir if override_target_dir else TARGET_DIR}"
        )
        logger.info(
            f"override_metadata_dir: {override_metadata_dir if override_metadata_dir else METADATA_DIR}"
        )
        logger.info(
            f"override_app_version: {override_app_version if override_app_version else APP_VERSION}"
        )
        if is_executable:
            import tufup

            pid = os.getpid()
            # write a temp file in local dir to store the pid
            pid_file = os.path.join(APP_DATA_PATH, "temp", f"{pid}.txt")
            os.makedirs(os.path.dirname(pid_file), exist_ok=True)
            # remove all contents of the directory
            for f in os.listdir(os.path.dirname(pid_file)):
                os.remove(os.path.join(os.path.dirname(pid_file), f))
            with open(pid_file, "w") as f:
                f.write(str(pid))

            restart_app = True
            if (
                os.environ.get("CELER_SIGHT_NO_RELUNCH_AFTER_UPDATE", "").lower()
                == "true"
            ):
                restart_app = False
            logger.info(f"restart app after update  : {restart_app}")

        # Create client with logging
        try:
            logger.info("Creating update client...")
            metadata_url = (
                override_metadata_base_url
                if override_metadata_base_url
                else METADATA_BASE_URL
            )
            target_url = (
                override_target_base_url
                if override_target_base_url
                else TARGET_BASE_URL
            )
            target_dir = override_target_dir if override_target_dir else TARGET_DIR

            client = Client(
                app_name=APP_NAME,
                app_install_dir=INSTALL_DIR,
                current_version=APP_VERSION,
                metadata_dir=METADATA_DIR,
                metadata_base_url=metadata_url,
                target_dir=target_dir,
                target_base_url=target_url,
                refresh_required=False,
            )
            logger.info("Successfully created update client")
            return client
        except Exception as e:
            logger.error(f"Failed to create update client: {str(e)}")
            return False
    except Exception as e:
        logger.error(f"Unexpected error in get_update_client: {str(e)}")
        return False
    # Perform update
    # new_update = client.check_for_updates()
    return client


@threaded
def check_for_update():
    from celer_sight_ai import config

    logger.info("Checking for updates")
    try:
        client = get_update_client()
        if not client:
            logger.info("ERROR: Failed to create update client")
            return

        update_available = client.check_for_updates()
        logger.info(f"Update check result: {update_available}")

        if update_available:
            update_celer_sight_ai()
        else:
            logger.info("No updates available")

    except Exception as e:
        import traceback

        logger.info(f"Update check failed: {str(e)}")
        logger.info(traceback.format_exc())
        global_signals.errorSignal.emit(f"Update check failed: {str(e)}")


@threaded
def update_celer_sight_ai():
    import ctypes
    import os
    import platform
    import subprocess
    import sys
    import time

    from PyQt6 import QtWidgets

    logger.info("Starting update process")
    try:
        # Determine platform
        current_platform = sys.platform
        logger.info(f"Current platform: {current_platform}")

        app_path = None

        if current_platform.startswith("darwin"):
            # macOS specific code
            app_path = "/Applications/Celer Sight AI.app"
            logger.info(f"Application path: {app_path}")

            # Now that sandboxing is removed, check if we have write access
            if not os.access(app_path, os.W_OK):
                logger.info(
                    f"No write access to application directory at {app_path}, requesting permissions"
                )

                # Try to make the directory writable
                try:
                    cmd = [
                        "osascript",
                        "-e",
                        f"""
                        tell application "System Events"
                            activate
                            display dialog "Celer Sight AI needs administrator privileges to complete the update installation." buttons {{"Cancel", "Continue"}} default button "Continue" with icon caution with title "Celer Sight AI Update"
                            if button returned of result is "Continue" then
                                do shell script "chmod -R u-w ''{app_path}''" with administrator privileges
                            else
                                error "User cancelled"
                            end if
                        end tell
                        """,
                    ]

                    process = subprocess.Popen(
                        cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
                    )
                    stdout, stderr = process.communicate()

                    logger.info(f"Permission command stdout: {stdout}")
                    logger.info(f"Permission command stderr: {stderr}")
                    logger.info(f"Permission command exit code: {process.returncode}")

                    if process.returncode != 0:
                        raise subprocess.CalledProcessError(
                            process.returncode, cmd, stdout, stderr
                        )

                    logger.info("Successfully updated permissions")

                except subprocess.CalledProcessError as e:
                    logger.error(f"Failed to get permissions: {e}")
                    logger.error(f"Command output: {e.output}")
                    logger.error(f"Command stderr: {e.stderr}")

                    global_signals.errorSignal.emit(
                        "Unable to get permissions to update. Please try updating manually or contact support."
                    )
                    return
        elif current_platform.startswith("win"):
            # Windows specific code
            # For Windows, admin access may not be required if the application is installed in a user-writable location
            app_path = os.path.dirname(sys.executable)
            logger.info(f"Application path: {app_path}")

            if not os.access(app_path, os.W_OK):
                logger.info(
                    f"No write access to application directory at {app_path}, checking for admin privileges"
                )

                # Check if running as admin
                try:
                    is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0
                except Exception as e:
                    logger.error(f"Failed to check admin status: {e}")
                    is_admin = False

                if not is_admin:
                    logger.info("Not running as admin, cannot proceed with update")
                    global_signals.errorSignal.emit(
                        "Update requires administrator privileges. Please run the application as administrator."
                    )
                    return
                else:
                    logger.info("Running as admin, proceeding with update")
        else:
            logger.error(f"Unsupported platform: {current_platform}")
            global_signals.errorSignal.emit("Unsupported platform for update")
            return

        # Start the update process
        global_signals.start_progress_bar_signal.emit(
            {
                "title": "Downloading Update",
                "message": "Downloading new version...",
                "modal": True,
                "percent": 0,
            }
        )

        client = get_update_client()
        if not client:
            logger.error("Failed to create update client")
            global_signals.errorSignal.emit("Failed to initialize update process")
            return

        update_available = client.check_for_updates()
        if not update_available:
            logger.info("No updates available")
            global_signals.successSignal.emit(
                "You are already using the latest version."
            )
            global_signals.complete_progress_bar_signal.emit()
            return

        logger.info("Update available, starting download and apply process")

        try:
            if current_platform.startswith("win"):
                client.download_and_apply_update(
                    skip_confirmation=True,
                    progress_hook=progress_hook,
                    purge_dst_dir=False,
                    exclude_from_purge=None,
                    robocopy_options=(
                        "/e",  # include subdirectories, even if empty
                        "/move",  # deletes files and dirs from source dir after they've been copied
                        "/v",  # verbose (show what is going on)
                        "/w:2",  # set retry-timeout (default is 30 seconds)
                        "/r:3",  # retry 3 times on failed copies
                        # multithreading
                        "/mt:8",
                        # reduce log spam
                        "/NFL",
                        "/NDL",
                        "/NJH",
                        "/NJS",
                        "/NC",
                        "/NS",
                    ),
                    log_file_name=os.path.join(APP_DATA_PATH, "install.log"),
                )
            else:
                client.download_and_apply_update(
                    skip_confirmation=True,
                    progress_hook=progress_hook,
                    purge_dst_dir=False,
                    exclude_from_purge=None,
                    log_file_name=os.path.join(APP_DATA_PATH, "install.log"),
                )
        except SystemExit as e:
            logger.info(f"Update completed with exit code: {getattr(e, 'code', 0)}")

            # For macOS, optionally restore permissions
            if current_platform.startswith("darwin"):
                try:
                    cmd = [
                        "osascript",
                        "-e",
                        f"do shell script \"chmod -R u-w '{app_path}'\" with administrator privileges",
                    ]
                    subprocess.run(cmd, check=True)
                    logger.info("Successfully restored permissions")
                except subprocess.CalledProcessError as e:
                    logger.warning(f"Failed to restore permissions: {e}")

            global_signals.loading_dialog_signal_close.emit()
            global_signals.successSignal.emit(
                "Update completed successfully. Please restart Celer Sight AI."
            )
            # Close the application
            global_signals.close_celer_sight_signal.emit()
            sys.exit(0)

        except Exception as e:
            logger.error(f"Update failed: {str(e)}")
            global_signals.errorSignal.emit(
                f"Update failed: {str(e)}\nPlease try again later or contact support."
            )
            return

    except Exception as e:
        logger.error(f"Update process encountered an error: {str(e)}")
        global_signals.errorSignal.emit(
            f"Update failed: {str(e)}\nPlease try again. /n You can download the update manualy from www.BioMarkerImaging.com or contact support."
        )
    finally:
        global_signals.complete_progress_bar_signal.emit()


# adapted from instanseg
markers_info = {
    "GITR": {"Subcellular Location": "Cytoplasm"},
    "IDO": {"Subcellular Location": "Nucleus"},
    "Ki67": {"Subcellular Location": "Nucleus"},
    "Foxp3": {"Subcellular Location": "Nucleus"},
    "CD8": {"Subcellular Location": "Nucleus"},
    "DAPI": {"Subcellular Location": "Nucleus"},
    "panCK": {"Subcellular Location": "Cytoplasm"},
    "Autofluorescence": {"Subcellular Location": "Cytoplasm"},
    "CD40-L": {"Subcellular Location": "Nucleus"},
    "PD-1": {"Subcellular Location": "Cytoplasm"},
    "CD40": {"Subcellular Location": "Cytoplasm"},
    "PD-L1": {"Subcellular Location": "Cytoplasm"},
    "PD1": {"Subcellular Location": "Nucleus"},
    "PDL1": {"Subcellular Location": "Cytoplasm"},
    "PD-L2": {"Subcellular Location": "Cytoplasm"},
    "CD30": {"Subcellular Location": "Cytoplasm"},
    "MHC-I": {"Subcellular Location": "Cytoplasm"},
    "MUM1": {"Subcellular Location": "Nucleus"},
    "Hoechst": {"Subcellular Location": "Nucleus"},
    "Class-II": {"Subcellular Location": "Cytoplasm"},
    "ICOS": {"Subcellular Location": "Nucleus"},
    "CTLA4": {"Subcellular Location": "Nucleus"},
    "TCF1": {"Subcellular Location": "Nucleus"},
    "panCK+CK7+CAM5.2": {"Subcellular Location": "Cytoplasm"},
    "LAG3": {"Subcellular Location": "Cytoplasm"},
    "CD68": {"Subcellular Location": "Cytoplasm"},
    "CD4": {"Subcellular Location": "Cytoplasm"},
    "CD163": {"Subcellular Location": "Cytoplasm"},
    "P63": {"Subcellular Location": "Nucleus"},
    "Arg-1": {"Subcellular Location": "Cytoplasm"},
    "CD11b": {"Subcellular Location": "Nucleus"},
    "MHC-II": {"Subcellular Location": "Cytoplasm"},
    "CK": {"Subcellular Location": "Cytoplasm"},
    "DAPI1": {"Subcellular Location": "Nucleus"},
    "NA": {"Subcellular Location": "Cytoplasm"},
    "DAPI2": {"Subcellular Location": "Nucleus"},
    "CD3": {"Subcellular Location": "Cytoplasm"},
    "CD20": {"Subcellular Location": "Cytoplasm"},
    "DAPI3": {"Subcellular Location": "Nucleus"},
    "PanCK": {"Subcellular Location": "Cytoplasm"},
    "DAPI4": {"Subcellular Location": "Nucleus"},
    "CD21": {"Subcellular Location": "Cytoplasm"},
    "CD31": {"Subcellular Location": "Cytoplasm"},
    "DAPI5": {"Subcellular Location": "Nucleus"},
    "CD45RO": {"Subcellular Location": "Cytoplasm"},
    "CD11c": {"Subcellular Location": "Cytoplasm"},
    "DAPI6": {"Subcellular Location": "Nucleus"},
    "HLA-DR": {"Subcellular Location": "Cytoplasm"},
    "DAPI7": {"Subcellular Location": "Nucleus"},
}

markers_info_gpt = {
    "CD66B": {
        "Cellular Location": "Granulocytes",
        "Subcellular Location": "Membrane/Cytoplasm",
        "Role": "Granulocyte marker",
        "Application": "Identify and quantify granulocytes in tissues",
    },
    "CD68": {
        "Cellular Location": "Macrophages",
        "Subcellular Location": "Membrane/Cytoplasm",
        "Role": "General macrophage marker",
        "Application": "Identify and quantify macrophages in tissues",
    },
    "CK7": {
        "Cellular Location": "Epithelial cells",
        "Subcellular Location": "Cytoplasm",
        "Role": "Cytokeratin marker for epithelial cells",
        "Application": "Identify and visualize epithelial cells in tissues",
    },
    "CTLA4": {
        "Cellular Location": "T cells",
        "Subcellular Location": "Membrane/Cytoplasm",
        "Role": "Negative regulator of T cell activation",
        "Application": "Study T cell activation and immune regulation",
    },
    "FOXP3": {
        "Cellular Location": "Regulatory T cells (Tregs)",
        "Subcellular Location": "Nucleus",
        "Role": "Transcription factor for Tregs",
        "Application": "Identify and quantify regulatory T cells in tissues",
    },
    "GITR": {
        "Cellular Location": "T cells",
        "Subcellular Location": "Membrane/Cytoplasm",
        "Role": "T cell activation marker",
        "Application": "Study T cell activation and immune responses",
    },
    "GZMB": {
        "Cellular Location": "Cytotoxic T cells, NK cells",
        "Subcellular Location": "Cytoplasm",
        "Role": "Serine protease in cytotoxic cells",
        "Application": "Assess cytotoxic activity of T cells and NK cells",
    },
    "ICOS": {
        "Cellular Location": "Activated T cells",
        "Subcellular Location": "Membrane/Cytoplasm",
        "Role": "Co-stimulatory molecule on T cells",
        "Application": "Identify activated T cells in the tissue",
    },
    "IDO": {
        "Cellular Location": "Macrophages, dendritic cells",
        "Subcellular Location": "Cytoplasm",
        "Role": "Indoleamine 2,3-dioxygenase; immune suppressor",
        "Application": "Assess immunosuppressive environment in tissues",
    },
    "ARG-1": {
        "Cellular Location": "Myeloid cells",
        "Subcellular Location": "Cytoplasm",
        "Role": "Urea cycle; associated with M2 macrophages",
        "Application": "Identify M2 macrophages in the tumor microenvironment",
    },
    "CD11B": {
        "Cellular Location": "Myeloid cells",
        "Subcellular Location": "Membrane",
        "Role": "Adhesion molecule for immune cell interactions",
        "Application": "Myeloid cell marker in immunohistochemistry",
    },
    "CD138": {
        "Cellular Location": "Plasma cells",
        "Subcellular Location": "Membrane",
        "Role": "Plasma cell marker",
        "Application": "Identify and quantify plasma cells, often in hematologic malignancies",
    },
    "CD163": {
        "Cellular Location": "Macrophages",
        "Subcellular Location": "Membrane/Cytoplasm",
        "Role": "M2 macrophage marker",
        "Application": "Identify M2 macrophages in tissue sections",
    },
    "CD20": {
        "Cellular Location": "B cells",
        "Subcellular Location": "Membrane",
        "Role": "B cell marker",
        "Application": "Identify and quantify B cells in tissues, especially in lymphomas",
    },
    "CD3": {
        "Cellular Location": "T cells",
        "Subcellular Location": "Membrane/Cytoplasm",
        "Role": "T cell marker",
        "Application": "Identify and quantify T cells in tissues",
    },
    "CD30": {
        "Cellular Location": "B and T cells",
        "Subcellular Location": "Membrane/Cytoplasm",
        "Role": "Marker for lymphoma, especially Hodgkin's lymphoma",
        "Application": "Used in the diagnosis of lymphomas",
    },
    "CD4": {
        "Cellular Location": "Helper T cells",
        "Subcellular Location": "Membrane/Cytoplasm",
        "Role": "Helper T cell marker",
        "Application": "Identify and quantify helper T cells in tissues",
    },
    "CD40": {
        "Cellular Location": "B cells, dendritic cells",
        "Subcellular Location": "Membrane",
        "Role": "Important in B cell activation",
        "Application": "Study B cell function and activation",
    },
    "CD40L": {
        "Cellular Location": "Activated T cells",
        "Subcellular Location": "Membrane/Cytoplasm",
        "Role": "Critical for B cell activation",
        "Application": "Study T cell-B cell interactions",
    },
    "KI67": {
        "Cellular Location": "Nuclei",
        "Subcellular Location": "Nucleus",
        "Role": "Proliferation marker",
        "Application": "Assess cell proliferation rate in tissues",
    },
    "LAG3": {
        "Cellular Location": "Activated T cells",
        "Subcellular Location": "Membrane/Cytoplasm",
        "Role": "Immune checkpoint receptor",
        "Application": "Study immune checkpoint regulation",
    },
    "MHC-I": {
        "Cellular Location": "Nucleated cells",
        "Subcellular Location": "Membrane",
        "Role": "Major histocompatibility complex class I",
        "Application": "Antigen presentation to CD8+ T cells",
    },
    "MHC-II": {
        "Cellular Location": "Antigen-presenting cells",
        "Subcellular Location": "Membrane",
        "Role": "Major histocompatibility complex class II",
        "Application": "Antigen presentation to CD4+ T cells",
    },
    "MUM1": {
        "Cellular Location": "B cells, plasma cells",
        "Subcellular Location": "Nucleus",
        "Role": "B cell and plasma cell marker",
        "Application": "Identify and quantify B cells and plasma cells in tissues",
    },
    "P63": {
        "Cellular Location": "Basal and squamous epithelial cells",
        "Subcellular Location": "Nucleus",
        "Role": "Epithelial cell marker",
        "Application": "Identify and visualize basal and squamous epithelial cells",
    },
    "PANCK": {
        "Cellular Location": "Epithelial cells",
        "Subcellular Location": "Cytoplasm",
        "Role": "Pan-cytokeratin marker for epithelial cells",
        "Application": "Identify and visualize epithelial cells in tissues",
    },
    "PAX8": {
        "Cellular Location": "Certain epithelial cells",
        "Subcellular Location": "Nucleus",
        "Role": "Transcription factor",
        "Application": "Marker for certain epithelial tissues, including ovarian and thyroid",
    },
    "PD-1": {
        "Cellular Location": "Activated T cells",
        "Subcellular Location": "Membrane/Cytoplasm",
        "Role": "Immune checkpoint receptor",
        "Application": "Study immune checkpoint regulation",
    },
    "PD-L1": {
        "Cellular Location": "Tumor cells, immune cells",
        "Subcellular Location": "Membrane",
        "Role": "Programmed Death-Ligand 1",
        "Application": "Assess expression in tumor microenvironment, response to immunotherapy",
    },
    "PD-L2": {
        "Cellular Location": "Tumor cells, immune cells",
        "Subcellular Location": "Membrane",
        "Role": "Programmed Death-Ligand 2",
        "Application": "Assess expression in tumor microenvironment, response to immunotherapy",
    },
    "TCF1": {
        "Cellular Location": "T cells",
        "Subcellular Location": "Nucleus",
        "Role": "Transcription factor",
        "Application": "Regulator of T cell development and function",
    },
    "TOX": {
        "Cellular Location": "T cells",
        "Subcellular Location": "Nucleus",
        "Role": "Transcription factor",
        "Application": "Regulator of T cell exhaustion and dysfunction",
    },
    "VISTA": {
        "Cellular Location": "Immune cells",
        "Subcellular Location": "Membrane/Cytoplasm",
        "Role": "Immune checkpoint receptor",
        "Application": "Study immune checkpoint regulation",
    },
    "CD8": {
        "Cellular Location": "Cytotoxic T cells",
        "Subcellular Location": "Membrane/Cytoplasm",
        "Role": "Cytotoxic T cell marker",
        "Application": "Identify and quantify cytotoxic T cells in tissues",
    },
    "DAPI": {
        "Cellular Location": "Nuclei",
        "Subcellular Location": "Nucleus",
        "Role": "DNA-binding dye for cell nuclei",
        "Application": "Stain cell nuclei for visualization in microscopy",
    },
    "HOECHST": {
        "Cellular Location": "Nuclei",
        "Subcellular Location": "Nucleus",
        "Role": "DNA-binding dye for cell nuclei",
        "Application": "Stain cell nuclei for visualization in microscopy",
    },
    "SOX10": {
        "Cellular Location": "Neural crest-derived cells",
        "Subcellular Location": "Nucleus",
        "Role": "Transcription factor",
        "Application": "Marker for neural crest-derived cells, especially in neuroectodermal tumors",
    },
    "CD21": {
        "Cellular Location": "B cells, follicular dendritic cells",
        "Subcellular Location": "Membrane",
        "Role": "Complement receptor 2",
        "Application": "Identify B cells and follicular dendritic cells in lymphoid tissues",
    },
    "CD31": {
        "Cellular Location": "Endothelial cells",
        "Subcellular Location": "Membrane",
        "Role": "Platelet endothelial cell adhesion molecule (PECAM-1)",
        "Application": "Marker for endothelial cells and angiogenesis",
    },
    "CD3E": {
        "Cellular Location": "T cells",
        "Subcellular Location": "Membrane/Cytoplasm",
        "Role": "Part of the T cell receptor complex",
        "Application": "Identify and quantify T cells in tissues",
    },
    "CD45RO": {
        "Cellular Location": "Memory T cells",
        "Subcellular Location": "Membrane/Cytoplasm",
        "Role": "Memory T cell marker",
        "Application": "Identify and quantify memory T cells in tissues",
    },
    "HLA-DR": {
        "Cellular Location": "Antigen-presenting cells",
        "Subcellular Location": "Membrane",
        "Role": "Major histocompatibility complex class II",
        "Application": "Antigen presentation to CD4+ T cells",
    },
    "Autofluorescence": {
        "Cellular Location": "N/A",
        "Subcellular Location": "N/A",
        "Role": "N/A",
        "Application": "N/A",
    },
}


if __name__ == "__main__":
    from multiprocessing import freeze_support

    freeze_support()
    pass
