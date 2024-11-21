
    
def MeasureFragmentation(ImageBinary):
    import matplotlib.pyplot as plt
    import numpy as np
    from skan.pre import threshold
    from skimage import morphology
    import pandas
    import cv2
    spacing_nm  = 1

    from skan import skeleton_to_csgraph
    from skan import Skeleton, summarize,branch_statistics
    from skan import Skeleton
    import skan
    # print(skeletonObject)
    skeleton0 = morphology.skeletonize(ImageBinary)
    cv2.imshow("bin skeleton", skeleton0.astype(np.uint8)*255)
    cv2.waitKey()
    skeletonObject= skeleton_to_csgraph(skeleton0,spacing= 0.01)
    skeletonObjectInstance = skan.csr.Skeleton(skeleton0)
    dataframe = summarize(skeletonObjectInstance)
    print(np.mean(dataframe["euclidean-distance"]))
    import pandas as pd
    return np.mean(dataframe["euclidean-distance"])



if __name__ == "__main__":
    from glob import glob
    import imageio as iio
    import cv2
    import os
    # MyPath = "C:\\Users\\manos\\Documents\\myo3mtFP"

    # image_list = []
    # valid_images = [".jpg",".gif",".png",".TIF",".tif",".tiff"]
    # for f in os.listdir(MyPath):
    #     ext = os.path.splitext(f)[1]
    #     if ext.lower() not in valid_images:
    #         continue
    #     image_list.append(cv2.imread(os.path.join(MyPath,f)))

    # cv2.imshow("binary", image_list[5])
    # cv2.waitKey()
    # MeasureFragmentation(image_list[5])
    