import collections
import itertools
import logging

import numpy as np
import scyjava


from celer_sight_ai.gui.Utilities.java_handle import jimport

from celer_sight_ai.io.image_formats import (
    MD_SIZE_S,
    MD_SIZE_C,
    MD_SIZE_Z,
    MD_SIZE_T,
    MD_SIZE_Y,
    MD_SIZE_X,
    BIOFORMATS_IMAGE_EXTENSIONS,
)

# from ..reader import Reader

import re

builtin_readers = {
    "imageio_reader": "ImageIOReader",
    "ngff_reader": "NGFFReader",
    "bioformats_reader": "BioformatsReader",
    "gcs_reader": "GcsReader",
}
# All successfully loaded reader classes. Maps name:class
ALL_READERS = dict()
# Reader classes that failed to load. Maps name:exception str
BAD_READERS = dict()
# Active reader classes (ALL_READERS that aren't disabled by user). Maps name:class
AVAILABLE_READERS = dict()

ZARR_FILETYPE = re.compile(r"(?<=\.zarr)", flags=re.IGNORECASE)


import uuid

from abc import ABC, abstractmethod

import numpy


class Reader(ABC):
    """
    Derive from this abstract Reader class to create your own image reader in Python

    You need to implement the methods below in the derived class.

    Use this block of text to describe your reader to the user.
    """

    def __init__(self, image_file):
        """
        Your init should define a variable_revision_number representing the reader version.
        Defining reader_name also allows you to register the reader with a custom name,
        otherwise it'll match the class name.
        """
        from celer_sight_ai import config

        self.file = image_file
        self.id = config.get_unique_id()

    @property
    @abstractmethod
    def supported_filetypes(self):
        # This should be a class property. Give the reader a set of supported filetypes (extensions).
        pass

    @property
    @abstractmethod
    def supported_schemes(self):
        # This should be a class property. Give the reader a set of supported schemes (e.g. file, https, s3, ...).
        pass

    @property
    @abstractmethod
    def variable_revision_number(self):
        # This should be a class property. Give the reader a version number (int).
        pass

    @property
    @abstractmethod
    def reader_name(self):
        # This should be a class property. Give the reader a human-readable name (string).
        pass

    @abstractmethod
    def read(
        self,
        series=None,
        index=None,
        c=None,
        z=None,
        t=None,
        rescale=True,
        xywh=None,
        wants_max_intensity=False,
        channel_names=None,
    ):
        """Read a single plane from the image file. Mimics the Bioformats API
        :param c: read from this channel. `None` = read color image if multichannel
            or interleaved RGB.
        :param z: z-stack index
        :param t: time index
        :param series: series for ``.flex`` and similar multi-stack formats
        :param index: if `None`, fall back to ``zct``, otherwise load the indexed frame
        :param rescale: `True` to rescale the intensity scale to 0 and 1; `False` to
                  return the raw values native to the file.
        :param xywh: a (x, y, w, h) tuple
        :param wants_max_intensity: if `False`, only return the image; if `True`,
                  return a tuple of image and max intensity
        :param channel_names: provide the channel names for the OME metadata

        Should return a data array with channel order X, Y, (C)
        """
        return None

    def read_volume(
        self,
        series=None,
        c=None,
        z=None,
        t=None,
        rescale=True,
        xywh=None,
        wants_max_intensity=False,
        channel_names=None,
    ):
        """Read a series of planes from the image file. Mimics the Bioformats API
        :param c: read from this channel. `None` = read color image if multichannel
            or interleaved RGB.
        :param z: z-stack index
        :param t: time index
        n.b. either z or t should be "None" to specify which channel to read across.
        :param series: series for ``.flex`` and similar multi-stack formats
        :param rescale: `True` to rescale the intensity scale to 0 and 1; `False` to
                  return the raw values native to the file.
        :param xywh: a (x, y, w, h) tuple
        :param wants_max_intensity: if `False`, only return the image; if `True`,
                  return a tuple of image and max intensity
        :param channel_names: provide the channel names for the OME metadata

        Should return a data array with channel order Z, X, Y, (C)
        """
        raise NotImplementedError(
            f"This reader ({self.reader_name}) does not support 3D reading."
        )

    @classmethod
    @abstractmethod
    def supports_format(cls, image_file, allow_open=False, volume=False):
        """This function needs to evaluate whether a given ImageFile object
        can be read by this reader class.

        Return value should be an integer representing suitability:
        -1 - 'I can't read this at all'
        1 - 'I am the one true reader for this format, don't even bother checking any others'
        2 - 'I am well-suited to this format'
        3 - 'I can read this format, but I might not be the best',
        4 - 'I can give it a go, if you must'

        The allow_open parameter dictates whether the reader is permitted to read the file when
        making this decision. If False the decision should be made using file extension only.
        Any opened files should be closed before returning. For now readers are selected with
        allow_open disabled, but this may change in the future.

        The volume parameter specifies whether the reader will need to return a 3D array.
        ."""
        return -1

    @classmethod
    def clear_cached_readers(cls):
        # This should clear any cached reader objects if your class stores unused readers.
        pass

    @classmethod
    def supports_url(cls):
        # This function defines whether the reader class supports reading data directly from a URL.
        # If False, CellProfiler will download compatible web-based images to a temporary directory.
        # If True, the reader will be passed the source URL.
        return False

    @abstractmethod
    def close(self):
        # If your reader opens a file, this needs to release any active lock,
        pass

    @abstractmethod
    def get_series_metadata(self):
        """Should return a dictionary with the following keys:
        Key names are in cellprofiler_core.constants.image
        MD_SIZE_S - int reflecting the number of series
        MD_SIZE_X - list of X dimension sizes, one element per series.
        MD_SIZE_Y - list of Y dimension sizes, one element per series.
        MD_SIZE_Z - list of Z dimension sizes, one element per series.
        MD_SIZE_C - list of C dimension sizes, one element per series.
        MD_SIZE_T - list of T dimension sizes, one element per series.
        MD_SERIES_NAME - [Optional] list of human-readable series names, one string per series.
                                    Must not contain '|' as this is used as a separator for storage.
        """
        pass

    @staticmethod
    def get_settings():
        """
        This function should return a list of settings objects configurable
        by the reader class. Each entry is a tuple. This list should not
        include the default '.enabled' key, used to disable readers.

        Tuple Format: (config key, name, description, type, default)

        config key - A name for the key in internal storage.
        Slashes should not be used in key names. The reader's name will
        be prefixed automatically.

        name - a human-readable name to be shown to the user

        description - extra text to describe the setting

        type - one of str, bool, float or int. These types are supported by
        wx config files.

        default - value to use if no existing config exists

        :return: list of setting tuples
        """
        return []

    @staticmethod
    def find_scale_to_match_bioformats(data):
        """
        When we're rescaling we'll usually want to match the output from BioFormats.
        skimage.exposure.rescale_intensity would normally work beautifully, but
        python-bioformats did things differently. To rescale with that system we
        divide by the max possible value determined by the image format.

        This utility function will look at an array and return the correct max value to
        divide the array by.
        """
        if data.dtype in (numpy.int8, numpy.uint8):
            return 255
        elif data.dtype in (numpy.int16, numpy.uint16):
            return 65535
        elif data.dtype == numpy.int32:
            return 2**32 - 1
        elif data.dtype == numpy.uint32:
            return 2**32
        else:
            return 1


LOGGER = logging.getLogger(__name__)

# bioformats returns 2 for these, imageio reader returns 3
SUPPORTED_EXTENSIONS = {".tiff", ".tif", ".ome.tif", ".ome.tiff"}
SEMI_SUPPORTED_EXTENSIONS = BIOFORMATS_IMAGE_EXTENSIONS
# TODO: disabled until CellProfiler/CellProfiler#4684 is resolved
# SUPPORTED_SCHEMES = {'file', 'http', 'https', 'ftp', 'ftps', 'omero', 's3'}
SUPPORTED_SCHEMES = {"file", "http", "https", "ftp", "ftps", "s3"}


class BioformatsReader(Reader):
    """
    Reads a variety of image formats using the bio-formats library.

    This reader is Java-based.
    """

    reader_name = "Bio-Formats"
    variable_revision_number = 1
    supported_filetypes = BIOFORMATS_IMAGE_EXTENSIONS
    supported_schemes = SUPPORTED_SCHEMES

    def __init__(self, image_file):
        self._reader = None
        self._is_file_open = False
        super().__init__(image_file)

    def get_reader(self):
        if self._reader is None:
            ImageReader = jimport("loci.formats.ImageReader")
            self._reader = ImageReader()
            self._is_file_open = False
            scyjava.when_jvm_stops(
                lambda: self._reader.close() if self._reader is not None else None
            )

        return self._reader

    def _ensure_file_open(self):
        if not self._is_file_open:
            self.get_reader().setId(self.file)
            self._is_file_open = True

    def read(
        self,
        series=None,
        index=None,
        c=None,
        z=0,
        t=0,
        rescale=True,
        xywh=None,
        wants_max_intensity=False,
        channel_names=None,
        XYWH=None,
    ):
        """Read a single plane from the image file.
        :param c: read from this channel. `None` = read color image if multichannel
            or interleaved RGB.
        :param z: z-stack index
        :param t: time index
        :param series: series for ``.flex`` and similar multi-stack formats
        :param index: if `None`, fall back to ``zct``, otherwise load the indexed frame
        :param rescale: `True` to rescale the intensity scale to 0 and 1; `False` to
                  return the raw values native to the file.
        :param xywh: a (x, y, w, h) tuple
        :param wants_max_intensity: if `False`, only return the image; if `True`,
                  return a tuple of image and max intensity
        :param channel_names: provide the channel names for the OME metadata
        :param XYWH: a (x, y, w, h) tuple
        """
        self._ensure_file_open()

        FormatTools = jimport("loci.formats.FormatTools")
        ChannelSeparator = jimport("loci.formats.ChannelSeparator")
        if series is not None:
            self._reader.setSeries(series)

        if XYWH is not None:
            assert isinstance(XYWH, tuple) and len(XYWH) == 4, "Invalid XYWH tuple"
            openBytes_func = lambda x: self._reader.openBytes(
                x, XYWH[0], XYWH[1], XYWH[2], XYWH[3]
            )
            width, height = XYWH[2], XYWH[3]
        else:
            openBytes_func = self._reader.openBytes
            width, height = self._reader.getSizeX(), self._reader.getSizeY()

        # FIXME instead of np.frombuffer use scyjava.to_python, ideally that wraps memory
        pixel_type = self._reader.getPixelType()
        little_endian = self._reader.isLittleEndian()
        if pixel_type == FormatTools.INT8:
            dtype = np.int8
            scale = 255
        elif pixel_type == FormatTools.UINT8:
            dtype = np.uint8
            scale = 255
        elif pixel_type == FormatTools.UINT16:
            dtype = "<u2" if little_endian else ">u2"
            scale = 65535
        elif pixel_type == FormatTools.INT16:
            dtype = "<i2" if little_endian else ">i2"
            scale = 65535
        elif pixel_type == FormatTools.UINT32:
            dtype = "<u4" if little_endian else ">u4"
            scale = 2**32
        elif pixel_type == FormatTools.INT32:
            dtype = "<i4" if little_endian else ">i4"
            scale = 2**32 - 1
        elif pixel_type == FormatTools.FLOAT:
            dtype = "<f4" if little_endian else ">f4"
            scale = 1
        elif pixel_type == FormatTools.DOUBLE:
            dtype = "<f8" if little_endian else ">f8"
            scale = 1
        max_sample_value = self._reader.getMetadataValue("MaxSampleValue")
        if max_sample_value is not None:
            try:
                scale = scyjava.to_python(max_sample_value)
            except:
                LOGGER.warning(
                    "WARNING: failed to get MaxSampleValue for image. Intensities may be improperly scaled."
                )
        if index is not None:
            image = np.frombuffer(openBytes_func(index), dtype)
            if len(image) / height / width in (3, 4):
                n_channels = int(len(image) / height / width)
                if self._reader.isInterleaved():
                    image.shape = (height, width, n_channels)
                else:
                    image.shape = (n_channels, height, width)
                    image = image.transpose(1, 2, 0)
            else:
                image.shape = (height, width)
        elif self._reader.isRGB() and self._reader.isInterleaved():
            index = self._reader.getIndex(z, 0, t)
            image = np.frombuffer(openBytes_func(index), dtype)
            image.shape = (height, width, self._reader.getSizeC())
            if image.shape[2] > 3:
                image = image[:, :, :3]
        elif c is not None and self._reader.getRGBChannelCount() == 1:
            index = self._reader.getIndex(z, c, t)
            image = np.frombuffer(openBytes_func(index), dtype)
            image.shape = (height, width)
        elif self._reader.getRGBChannelCount() > 1:
            n_planes = self._reader.getRGBChannelCount()
            rdr = ChannelSeparator(self._reader)
            planes = [
                scyjava.to_python(
                    (
                        rdr.openBytes(rdr.getIndex(z, i, t))
                        if XYWH is None
                        else rdr.openBytes(
                            rdr.getIndex(z, i, t), XYWH[0], XYWH[1], XYWH[2], XYWH[3]
                        )
                    ),
                    dtype,
                )
                for i in range(n_planes)
            ]

            if len(planes) > 3:
                planes = planes[:3]
            elif len(planes) < 3:
                # > 1 and < 3 means must be 2
                # see issue #775
                planes.append(np.zeros(planes[0].shape, planes[0].dtype))
            image = np.dstack(planes)
            image.shape = (height, width, 3)
        elif self._reader.getSizeC() > 1:
            images = [
                np.frombuffer(openBytes_func(self._reader.getIndex(z, i, t)), dtype)
                for i in range(self._reader.getSizeC())
            ]
            image = np.dstack(images)
            image.shape = (height, width, self._reader.getSizeC())
            if not channel_names is None:
                metadata = self._reader.getMetadataStore()
                for i in range(self._reader.getSizeC()):
                    index = self._reader.getIndex(z, 0, t)
                    channel_name = metadata.getChannelName(index, i)
                    if channel_name is None:
                        channel_name = metadata.getChannelID(index, i)
                    channel_names.append(channel_name)
        elif self._reader.isIndexed():
            # TODO can we use ChannelFiller, which automatically expands channels if they
            # are "true" color and does nothing if they are "false" (e.g. applied color table)?
            #
            # The image data is indexes into a color lookup-table
            # But sometimes the table is the identity table and just generates
            # a monochrome RGB image
            #
            index = self._reader.getIndex(z, 0, t)
            image = np.frombuffer(openBytes_func(index), dtype)
            lut = None
            if pixel_type in (FormatTools.INT16, FormatTools.UINT16):
                lut = self._reader.get16BitLookupTable()
            else:
                lut = self._reader.get8BitLookupTable()
            if lut is not None:
                lut = np.array([d for d in lut]).transpose()
            image.shape = (height, width)
            if (lut is not None) and not np.all(
                lut == np.arange(lut.shape[0])[:, np.newaxis]
            ):
                image = lut[image, :]
        else:
            index = self._reader.getIndex(z, 0, t)
            image = np.frombuffer(openBytes_func(index), dtype)
            image.shape = (height, width)

        if rescale:
            image = image.astype(np.float32) / float(scale)
        if wants_max_intensity:
            return image, scale
        return image

    def read_volume(
        self,
        series=None,
        c=None,
        z=None,
        t=None,
        rescale=True,
        xywh=None,
        wants_max_intensity=False,
        channel_names=None,
    ):
        # Whether a volume has planes stored in the z or t axis is often ambiguous.
        # If z-size > 1 we'll use z, else we'll use t. Otherwise user should choose
        # an axis to split in Images.
        bf_reader = self.get_reader()
        self._ensure_file_open()
        if series is None:
            series = 0
        bf_reader.setSeries(series)
        z_len = 0
        if z is None:
            z_len = bf_reader.getSizeZ()
            z_range = range(z_len)
        else:
            z_range = [z]
        if t is None:
            if z_len > 1:
                t_range = range(1)
            else:
                t_range = range(bf_reader.getSizeT())
        else:
            t_range = [t]
        image_stack = []
        for z_index, t_index in itertools.product(z_range, t_range):
            data = self.read(
                series=series,
                c=c,
                z=z_index,
                t=t_index,
                rescale=rescale,
                XYWH=xywh,
                wants_max_intensity=False,
                channel_names=channel_names,
            )
            image_stack.append(data)
        return np.stack(image_stack)

    @classmethod
    def supports_format(cls, image_file, allow_open=False, volume=False):
        """This function needs to evaluate whether a given ImageFile object
        can be read by this reader class.

        Return value should be an integer representing suitability:
        -1 - 'I can't read this at all'
        1 - 'I am the one true reader for this format, don't even bother checking any others'
        2 - 'I am well-suited to this format'
        3 - 'I can read this format, but I might not be the best',
        4 - 'I can give it a go, if you must'

        The allow_open parameter dictates whether the reader is permitted to read the file when
        making this decision. If False the decision should be made using file extension only.
        Any opened files should be closed before returning.

        The volume parameter specifies whether the reader will need to return a 3D array.
        ."""
        if image_file.scheme not in SUPPORTED_SCHEMES:
            return -1
        if image_file.scheme == "omero":
            return 1
        if image_file.full_extension in SUPPORTED_EXTENSIONS:
            return 2
        if not allow_open:
            if image_file.file_extension in SEMI_SUPPORTED_EXTENSIONS:
                return 3
            return -1

    def close(self):
        # If your reader opens a file, this needs to release any active lock,
        if self._reader is not None and scyjava.jvm_started():
            self._reader.close()
            self._reader = None

    def get_series_metadata(self):
        """Should return a dictionary with the following keys:
        Key names are in cellprofiler_core.constants.image
        MD_SIZE_S - int reflecting the number of series
        MD_SIZE_X - list of X dimension sizes, one element per series.
        MD_SIZE_Y - list of Y dimension sizes, one element per series.
        MD_SIZE_Z - list of Z dimension sizes, one element per series.
        MD_SIZE_C - list of C dimension sizes, one element per series.
        MD_SIZE_T - list of T dimension sizes, one element per series.
        MD_SERIES_NAME - list of series names, one element per series.
        """
        meta_dict = collections.defaultdict(list)
        self._ensure_file_open()
        reader = self.get_reader()
        series_count = reader.getSeriesCount()
        meta_dict[MD_SIZE_S] = series_count
        for i in range(series_count):
            reader.setSeries(i)
            meta_dict[MD_SIZE_C].append(reader.getSizeC())
            meta_dict[MD_SIZE_Z].append(reader.getSizeZ())
            meta_dict[MD_SIZE_T].append(reader.getSizeT())
            meta_dict[MD_SIZE_Y].append(reader.getSizeY())
            meta_dict[MD_SIZE_X].append(reader.getSizeX())
        return meta_dict
