import unittest
import numpy as np
import tifffile
import os
import javabridge
import bioformats
import tempfile
import logging
import xmltodict
import pyometiff
from pathlib import Path

logger = logging.getLogger(__name__)


class TestWriteReadImage(unittest.TestCase):
    def setUp(self):
        # Create test data
        self.temp_dir = tempfile.mkdtemp()
        self.test_data = np.ones((100, 100, 3), dtype=np.uint8)
        self.test_data[:, :, 0] *= 255
        self.test_data[:, :, 1] *= 175
        self.test_data[:, :, 2] *= 0

        self.channel_names = ["custom_red", "custom_green", "custom_blue"]
        self.test_file = os.path.join(self.temp_dir, "test.tiff")
        # remove the file if it exists
        if os.path.exists(self.test_file):
            os.remove(self.test_file)
        # Start Java VM for bioformats
        javabridge.start_vm(class_path=bioformats.JARS, run_headless=True)

    def tearDown(self):
        # Clean up temp files and stop Java VM
        if os.path.exists(self.test_file):
            os.remove(self.test_file)
        os.rmdir(self.temp_dir)
        javabridge.kill_vm()

    def test_write_tiff_read_bioformats(self):
        """Test writing with tifffile and reading with bioformats"""
        FIELD_FLUOR = "Fluor"
        # Create OME-XML metadata

        # Verify file exists
        self.assertTrue(os.path.exists(self.test_file))

        # Add verification using OMETIFFReader
        reader = pyometiff.OMETIFFReader(fpath=Path(self.test_file))
        ome_data = reader.read()
        ome_metadata = reader.metadata

        # Verify dimensions match
        self.assertEqual(ome_data.shape, (1, 1, 3, 100, 100))  # ZTCYX order

        # Verify channel names
        for i, channel_name in enumerate(self.channel_names):
            self.assertEqual(
                ome_metadata["Channels"][channel_name]["Name"],
                channel_name,
                f"Channel name mismatch for channel {i}",
            )

        # Verify physical sizes
        self.assertEqual(float(ome_metadata["PhysicalSizeX"]), 0.88)
        self.assertEqual(ome_metadata["PhysicalSizeXUnit"], "µm")
        self.assertEqual(float(ome_metadata["PhysicalSizeY"]), 0.88)
        self.assertEqual(ome_metadata["PhysicalSizeYUnit"], "µm")
        self.assertEqual(float(ome_metadata["PhysicalSizeZ"]), 3.3)
        self.assertEqual(ome_metadata["PhysicalSizeZUnit"], "µm")

        # Verify data content matches (need to reshape to match original)
        np.testing.assert_array_equal(ome_data.reshape(100, 100, 3), self.test_data)

        try:
            # Read with bioformats
            reader = bioformats.ImageReader(path=self.test_file)
            read_data = reader.read(rescale=False)

            # Get metadata and print it for debugging
            metadata = bioformats.get_omexml_metadata(path=self.test_file)
            print("Raw OME-XML metadata:")
            print(metadata)
            metadata_dict = bioformats.omexml.OMEXML(metadata)

            pixel_data = metadata_dict.image().Pixels

            # Verify dimensions match
            self.assertEqual(read_data.shape, self.test_data.shape)
            self.assertEqual(pixel_data.SizeX, self.test_data.shape[1])
            self.assertEqual(pixel_data.SizeY, self.test_data.shape[0])
            self.assertEqual(pixel_data.SizeC, self.test_data.shape[2])

            # Add explicit checks for other dimension sizes
            self.assertEqual(pixel_data.SizeT, 1, "Time dimension should be 1, not 3")
            self.assertEqual(pixel_data.SizeZ, 1, "Z dimension should be 1")
            self.assertEqual(
                pixel_data.channel_count,
                self.test_data.shape[2],
                f"Expected {self.test_data.shape[2]} channels but got {pixel_data.channel_count}",
            )

            # Verify physical sizes
            self.assertEqual(float(pixel_data.PhysicalSizeX), 0.88)
            self.assertEqual(pixel_data.PhysicalSizeXUnit, "µm")
            self.assertEqual(float(pixel_data.PhysicalSizeY), 0.88)
            self.assertEqual(pixel_data.PhysicalSizeYUnit, "µm")
            self.assertEqual(float(pixel_data.PhysicalSizeZ), 3.3)
            self.assertEqual(pixel_data.PhysicalSizeZUnit, "µm")

            # Verify data content matches
            np.testing.assert_array_equal(read_data, self.test_data)

            # Print channel information for debugging
            for i in range(len(self.channel_names)):
                channel = pixel_data.Channel(i)
                print(f"Channel {i}:")
                print(f"ID: {channel.ID}")
                print(f"Name: {channel.Name}")
                print(f"SamplesPerPixel: {channel.SamplesPerPixel}")
                print("---")

        except Exception as e:
            self.fail(f"Failed to read with bioformats: {str(e)}")
        finally:
            if "reader" in locals():
                reader.close()


if __name__ == "__main__":
    unittest.main()
