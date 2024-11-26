import time

start = time.time()
import javabridge
import bioformats

javabridge.start_vm(class_path=bioformats.JARS, run_headless=True)
print("Time to import bioformats", time.time() - start)

path = "/Users/mchaniotakis/Downloads/rep neuronal mitophagy 2-10-23 d4/unc-43 ua d4/unc-43_ua_1_gfp.tif"
img = bioformats.ImageReader(path=path)
img_data = img.read(series=0, rescale=False)
metadata_xml = bioformats.get_omexml_metadata(path=path)
metadata_dict = bioformats.omexml.OMEXML(metadata_xml)
dimention_order = metadata_dict.image().Pixels.get_dimension_order()

javabridge.kill_vm()
