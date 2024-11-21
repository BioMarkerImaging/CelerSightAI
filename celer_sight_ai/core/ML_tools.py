import sys
import logging

logger = logging.getLogger(__name__)
import os
from celer_sight_ai import config

if config.is_executable:
    sys.path.append([str(os.environ["CELER_SIGHT_AI_HOME"])])
logger.info("Before numpy import")

import numpy as np
logger.info("skimage importer in AA")
from PyQt6 import QtCore, QtGui, QtWidgets
from skimage.draw import circle_perimeter as circle
logger.info("3")
from cv2 import resize

from celer_sight_ai.core.magic_box_tools import get_largest_area
from celer_sight_ai.QtAssets.UiFiles.ExitSaveDialog import (
    Ui_Dialog as exitSaveDialog_UI,
)

class featureBuilder:
    def __init__(self):
        self.channels = 3
        self.computeChannels = [True, True, True]
        self.allFeaturesComputed = []

    def runCreateFeatures(self, channels=None, orgDf=None, MODE="Medium"):
        chUsed = channels
        import time

        self.allFeaturesComputed = []
        gaborF = featureGabor(chUsed.copy(), orgDf, "Low")
        startGabor = time.time()
        self.allFeaturesComputed.append(gaborF)
        orgDf = gaborF.run()

        GaussianGradientMagnitudeF = featureGaussianGradientMagnitude(
            channels.copy(), orgDf, "Low"
        )
        startGaussianGradientMagnitudeF = time.time()
        orgDf = GaussianGradientMagnitudeF.run()
        self.allFeaturesComputed.append(GaussianGradientMagnitudeF)
        GaussianLaplaceF = featureGaussianLaplace(chUsed.copy(), orgDf, "Low")
        # logger.info("GaussianGradientMagnitudeF: " ,time.time() - startGaussianGradientMagnitudeF )
        startGaussianLaplaceF = time.time()
        orgDf = GaussianLaplaceF.run()
        self.allFeaturesComputed.append(startGaussianLaplaceF)

        # logger.info("GaussianLaplaceF: " ,time.time() - startGaussianLaplaceF )
        SobelF = featureSobel(chUsed.copy(), orgDf, "Medium")
        startSobelF = time.time()
        orgDf = SobelF.run()
        self.allFeaturesComputed.append(SobelF)

        # logger.info("SobelF: " ,time.time() - startSobelF )
        VarianceFilterF = featureVarianceFilter(chUsed.copy(), orgDf, "Low")
        startVarianceFilterF = time.time()
        orgDf = VarianceFilterF.run()
        self.allFeaturesComputed.append(VarianceFilterF)

        logger.info("VarianceFilterF: ".format(time.time() - startVarianceFilterF))
        # DifferenceOfGaussiansF = featureDifferenceOfGaussians(channels.copy() ,orgDf , MODE )
        # startDifferenceOfGaussiansF = time.time()
        # orgDf = DifferenceOfGaussiansF.run()
        # logger.info("DifferenceOfGaussiansF: " ,time.time() - startDifferenceOfGaussiansF )
        HessianMatrixEigvalsF = featureHessianMatrixEigvals(chUsed.copy(), orgDf, "Low")
        startHessianMatrixEigvalsF = time.time()
        orgDf = HessianMatrixEigvalsF.run()
        self.allFeaturesComputed.append(HessianMatrixEigvalsF)

        logger.info(
            "HessianMatrixEigvalsF: ".format(time.time() - startHessianMatrixEigvalsF)
        )
        GaussianSmoothingF = featureGaussianSmoothing(chUsed.copy(), orgDf, "Low")
        orgDf = GaussianSmoothingF.run()
        self.allFeaturesComputed.append(GaussianSmoothingF)

        return orgDf


class featureGabor:
    def __init__(self, channels=None, orgDf=None, MODE="Medium"):
        self.orgDf = orgDf
        self.type = "Gabor"
        self.num = 0
        self.channels = channels
        self.computeChannels = [True, True, True]
        if MODE == "Medium":
            self.Medium()
        elif MODE == "Low":
            self.Low()
        elif MODE == "Ultra":
            self.Ultra()

    def Low(self):
        self.lambdaRange = [0, 2]
        self.thetaRange = [1, 3, 4, 6]
        self.sigmaRange = [0.1]
        self.gammaRange = [None]
        self.kernalSizeRange = [9]

    def Medium(self):
        self.lambdaRange = [0, 1, 2]
        self.thetaRange = [1, 2, 3, 4, 5, 6]
        self.sigmaRange = [0.1]
        self.gammaRange = [None]
        self.kernalSizeRange = [9]

    def Ultra(self):
        self.lambdaRange = [0, 1, 2]
        self.thetaRange = [1, 2, 3, 4, 5, 6]
        self.sigmaRange = [0.1]
        self.gammaRange = [None]
        self.kernalSizeRange = [7, 9, 11]

    def thetaMediumize(self, theta):
        return theta / 4.0 * np.pi

    def lambdaMediumize(self, lam):
        return lam * (np.pi / 2)

    def run(self):
        import cv2
        self.num = 0
        origWidth = self.channels[0][0].shape[1]
        origHeight = self.channels[0][0].shape[0]
        print("orig shape is ", origWidth, origHeight)
        for z in range(len(self.channels)):
            for i in range(len(self.channels[z])):
                if self.computeChannels[i]:
                    for kernalSizeRange in self.kernalSizeRange:
                        for sigmaRange in self.gammaRange:
                            for thetaRange in self.thetaRange:
                                for lambdaRange in self.lambdaRange:
                                    kernel = cv2.getGaborKernel(
                                        (kernalSizeRange, kernalSizeRange),
                                        2,
                                        self.thetaMediumize(thetaRange),
                                        self.lambdaMediumize(lambdaRange),
                                        sigmaRange,
                                        ktype=cv2.CV_32F,
                                    )
                                    tmpImg = cv2.filter2D(
                                        self.channels[z][i], cv2.CV_8UC3, kernel
                                    )
                                    if z != 0:
                                        tmpImg = resize(tmpImg, (origHeight, origWidth))
                                    self.orgDf[self.type + str(self.num)] = (
                                        tmpImg.reshape(-1)
                                    )
                                    self.num += 1
        return self.orgDf


# class featureAdaptiveThreshold():
#     def __init__(self,channels = None, orgDf = None,MODE = 'Ultra'):
#         self.orgDf = orgDf
#         self.type = 'AdaptiveThreshold'
#         self.num = 0
#         self.channels = channels
#         self.computeChannels = [True,True,True]
#         self.blockSizeRange = [0, 1,2]
#         if MODE == 'Medium':
#             self.Medium()
#         elif MODE == 'Low':
#             self.Low()
#         elif MODE == 'Ultra':
#             self.Ultra()
#     def Low(self):
#         self.blockSizeRange = [1]
#     def Medium(self):
#         self.blockSizeRange = [1,2]

#     def Ultra(self):
#         self.blockSizeRange = [0, 1,2]

#     def blockSizMediumize(self,block):
#         return (5*(block+1))+(block)

#     def run(self):
#         self.num = 0
#         origWidth = self.channels[0][0].shape[1]
#         origHeight = self.channels[0][0].shape[0]
#         # for i in range(self.channels):
#             if self.computeChannels[i]:
#                 for z in range(len(self.channels[i])):
#                         for blockSizeRange in self.blockSizeRange:
#                             self.orgDf[self.type +str(self.num)] = cv2.adaptiveThreshold(self.channels[i],255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,\
#                                 cv2.THRESH_BINARY,self.blockSizMediumize(blockSizeRange),3).reshape(-1)
#                             self.num+=1
#         return self.orgDf


class featureGaussianGradientMagnitude:
    def __init__(self, channels=None, orgDf=None, MODE="Ultra"):
        self.orgDf = orgDf
        self.type = "GaussianGradientMagnitude"
        self.num = 0
        self.channels = channels
        self.computeChannels = [True, True, True]
        self.sigmaRange = [0, 1, 2, 3, 4, 5]
        if MODE == "Medium":
            self.Medium()
        elif MODE == "Low":
            self.Low()
        elif MODE == "Ultra":
            self.Ultra()

    def Low(self):
        self.sigmaRange = [0, 3]

    def Medium(self):
        self.sigmaRange = [0, 1, 3, 5]

    def Ultra(self):
        self.sigmaRange = [0, 1, 2, 3, 4, 5]

    def sigmaMediumize(self, sigma):
        return 2 * (sigma + 1)

    def run(self):
        import cv2
        from scipy import ndimage
        self.num = 0
        origWidth = self.channels[0][0].shape[1]
        origHeight = self.channels[0][0].shape[0]
        for i in range(len(self.channels)):
            for z in range(len(self.channels[i])):
                if self.computeChannels[z]:
                    for sigmaRange in self.sigmaRange:
                        tmpImg = cv2.normalize(
                            ndimage.gaussian_gradient_magnitude(
                                self.channels[i][z],
                                sigma=self.sigmaMediumize(sigmaRange),
                            ),
                            None,
                            0,
                            255,
                            cv2.NORM_MINMAX,
                            cv2.CV_8U,
                        )
                        if i != 0:
                            tmpImg = resize(tmpImg, (origHeight, origWidth))
                        self.orgDf[self.type + str(self.num)] = tmpImg.reshape(-1)
                        self.num += 1
        return self.orgDf


class featureGaussianLaplace:
    def __init__(self, channels=None, orgDf=None, MODE="Ultra"):
        self.orgDf = orgDf
        self.type = "GaussianLaplace"
        self.num = 0
        self.channels = channels
        self.computeChannels = [True, True, True]
        self.sigmaRange = [0, 1, 2, 3, 4, 5]
        if MODE == "Medium":
            self.Medium()
        elif MODE == "Low":
            self.Low()
        elif MODE == "Ultra":
            self.Ultra()

    def Low(self):
        self.sigmaRange = [0, 3]

    def Medium(self):
        self.sigmaRange = [0, 2, 3, 5]

    def Ultra(self):
        self.sigmaRange = [0, 1, 2, 3, 4, 5]

    def sigmaMediumize(self, sigma):
        return 0.5 * (sigma + 1)

    def run(self):
        import cv2
        from scipy import ndimage
        self.num = 0
        origWidth = self.channels[0][0].shape[1]
        origHeight = self.channels[0][0].shape[0]
        for i in range(len(self.channels)):
            for z in range(len(self.channels[i])):
                if self.computeChannels[z]:
                    for sigmaRange in self.sigmaRange:
                        tmpImg = cv2.normalize(
                            ndimage.gaussian_laplace(
                                self.channels[i][z],
                                sigma=self.sigmaMediumize(sigmaRange),
                            ),
                            None,
                            0,
                            255,
                            cv2.NORM_MINMAX,
                            cv2.CV_8U,
                        )
                        if i != 0:
                            tmpImg = resize(tmpImg, (origHeight, origWidth))

                        self.orgDf[self.type + str(self.num)] = tmpImg.reshape(-1)
                        self.num += 1
        return self.orgDf


class featureSobel:
    def __init__(self, channels=None, orgDf=None, MODE="Ultra"):
        self.orgDf = orgDf
        self.type = "Sobel"
        self.num = 0
        self.channels = channels
        self.computeChannels = [True, True, True]

        if MODE == "Medium":
            self.Medium()
        elif MODE == "Low":
            self.Low()
        elif MODE == "Ultra":
            self.Ultra()

    def Low(self):
        self.sigmaRange = [1]

    def Medium(self):
        self.sigmaRange = [0, 2]

    def Ultra(self):
        self.sigmaRange = [0, 1, 2]

    def run(self):
        origWidth = self.channels[0][0].shape[1]
        origHeight = self.channels[0][0].shape[0]
        for i in range(len(self.channels)):
            for z in range(len(self.channels[i])):
                tmpImg = doSobel(
                    self.channels[i][z]
                )  # cv2.Mediumize(*255, None, 0, 255, cv2.NORM_MINMAX, cv2.CV_8U)
                tmpImg = (tmpImg * 255).astype(np.uint8)
                if i != 0:
                    tmpImg = resize(tmpImg, (origHeight, origWidth))
                self.orgDf[self.type + str(self.num)] = tmpImg.reshape(-1)
        return self.orgDf


class featureVarianceFilter:
    def __init__(self, channels=None, orgDf=None, MODE="Ultra"):
        self.orgDf = orgDf
        self.type = "VarianceFilter"
        self.num = 0
        self.channels = channels
        self.computeChannels = [True, True, True]
        self.sigmaRange = [0, 1, 2]
        if MODE == "Medium":
            self.Medium()
        elif MODE == "Low":
            self.Low()
        elif MODE == "Ultra":
            self.Ultra()

    def Low(self):
        self.sigmaRange = [1]

    def Medium(self):
        self.sigmaRange = [0, 1, 2, 3, 4]

    def Ultra(self):
        self.sigmaRange = [0, 1, 2, 3, 4, 5]

    def sigmaMediumize(self, sigma):
        return ((sigma * 2) + 1) * 3

    def run(self):
        import skimage
        import cv2
        self.num = 0
        origWidth = self.channels[0][0].shape[1]
        origHeight = self.channels[0][0].shape[0]
        for i in range(len(self.channels)):
            for z in range(len(self.channels[i])):
                if self.computeChannels[z]:
                    for sigmaRange in self.sigmaRange:
                        tmpImg = cv2.normalize(
                            self.variance_filter(
                                self.channels[i][z], self.sigmaMediumize(sigmaRange)
                            ),
                            None,
                            0,
                            255,
                            cv2.NORM_MINMAX,
                            cv2.CV_8U,
                        )
                        if i != 0:
                            tmpImg = resize(tmpImg, (origHeight, origWidth))
                        self.orgDf[self.type + str(self.num)] = tmpImg.reshape(-1)

                        self.num += 1
        return self.orgDf

    def variance_filter(self, img, VAR_FILTER_SIZE):
        """
        this filter is usefull for getting scratch features
        """
        from scipy import ndimage
        img = img.astype(np.float)

        rows, cols = img.shape[0], img.shape[1]
        win_rows, win_cols = VAR_FILTER_SIZE, VAR_FILTER_SIZE
        win_mean = ndimage.uniform_filter(img, (win_rows, win_cols))
        win_sqr_mean = ndimage.uniform_filter(img**2, (win_rows, win_cols))
        win_var = win_sqr_mean - win_mean**2
        return win_var


class featureDifferenceOfGaussians:
    def __init__(self, channels=None, orgDf=None, MODE="qiality"):
        self.orgDf = orgDf
        self.type = "DifferenceOfGaussians"
        self.num = 0
        self.channels = channels
        self.computeChannels = [True, True, True]
        self.lowSigmaRange = [0, 1, 2, 3]
        self.highSigmaRange = [1, 2, 3, 4, 5, 6]
        self.a = 1
        if MODE == "Medium":
            self.Medium()
        elif MODE == "Low":
            self.Low()
        elif MODE == "Ultra":
            self.Ultra()

    def Low(self):
        self.lowSigmaRange = [1]
        self.highSigmaRange = [3]

    def Medium(self):
        self.lowSigmaRange = [0, 2]
        self.highSigmaRange = [1, 6]

    def Ultra(self):
        self.lowSigmaRange = [0, 1, 3]
        self.highSigmaRange = [1, 2, 4, 6]

    def lowSigmMediumize(self, lowSig):
        return self.a * (lowSig + 2)

    def HighSigmaMediumize(self, HighSig):
        return ((HighSig + 1) * (1.6 * (HighSig + 2))) * self.a

    def run(self):
        import skimage
        import cv2
        self.num = 0
        for i in range(len(self.channels)):
            if self.computeChannels[i]:
                for lowSigma in self.lowSigmaRange:
                    for highSigma in self.highSigmaRange:
                        self.orgDf[self.type + str(self.num)] = cv2.Mediumize(
                            skimage.filters.difference_of_gaussians(
                                self.channels[i],
                                self.lowSigmMediumize(lowSigma),
                                high_sigma=self.HighSigmaMediumize(highSigma),
                            ),
                            None,
                            0,
                            255,
                            cv2.NORM_MINMAX,
                            cv2.CV_8U,
                        ).reshape(-1)
                        self.num += 1

        return self.orgDf


class featureGaussianSmoothing:
    def __init__(self, channels=None, orgDf=None, MODE="qiality"):
        self.orgDf = orgDf
        self.type = "GaussianSmoothing"
        self.num = 0
        self.channels = channels
        self.computeChannels = [True, True, True]
        self.sigmaRange = [0, 1, 2, 3]
        if MODE == "Medium":
            self.Medium()
        elif MODE == "Low":
            self.Low()
        elif MODE == "Ultra":
            self.Ultra()

    def Low(self):
        self.sigmaRange = [1, 3, 7, 10]

    def Medium(self):
        self.sigmaRange = [1, 3, 5, 6, 8, 10]

    def Ultra(self):
        self.sigmaRange = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

    def sigmMediumize(self, lowSig):
        return lowSig

    def run(self):
        import skimage
        self.num = 0
        origWidth = self.channels[0][0].shape[1]
        origHeight = self.channels[0][0].shape[0]
        for i in range(len(self.channels)):
            for z in range(len(self.channels[i])):
                if self.computeChannels[z]:
                    for lowSigma in self.sigmaRange:
                        tmpImg = skimage.filters.gaussian(
                            self.channels[i][z], sigma=self.sigmMediumize(lowSigma)
                        )
                        if i != 0:
                            tmpImg = resize(tmpImg, (origHeight, origWidth))
                        self.orgDf[self.type + str(self.num)] = tmpImg.reshape(-1)

                        self.num += 1

        return self.orgDf


class featureHessianMatrixEigvals:
    def __init__(self, channels=None, orgDf=None, MODE="Ultra"):
        self.orgDf = orgDf
        self.type = "HessianMatrixEigvals"
        self.num = 0
        self.channels = channels
        self.computeChannels = [True, True, True]
        self.sigmaRange = [0, 1, 2, 3]
        if MODE == "Medium":
            self.Medium()
        elif MODE == "Low":
            self.Low()
        elif MODE == "Ultra":
            self.Ultra()

    def Low(self):
        self.sigmaRange = [1]

    def Medium(self):
        self.sigmaRange = [0, 3]

    def Ultra(self):
        self.sigmaRange = [0, 1, 2, 3]

    def sigmaMediumize(self, lowSig):
        return (lowSig * 3) + 0.1

    def run(self):
        import skimage
        import cv2
        self.num = 0
        origWidth = self.channels[0][0].shape[1]
        origHeight = self.channels[0][0].shape[0]
        for i in range(len(self.channels)):
            for z in range(len(self.channels[i])):
                if self.computeChannels[z]:
                    for sigma in self.sigmaRange:
                        H_elems = skimage.feature.hessian_matrix(
                            self.channels[i][z], sigma=self.sigmaMediumize(sigma)
                        )
                        final = skimage.feature.hessian_matrix_eigvals(H_elems)[0]

                        tmpImg = cv2.normalize(
                            final, None, 0, 255, cv2.NORM_MINMAX, cv2.CV_8U
                        )
                        if i != 0:
                            tmpImg = resize(tmpImg, (origHeight, origWidth))
                        self.orgDf[self.type + str(self.num)] = tmpImg.reshape(-1)
                        self.num += 1

        return self.orgDf


class BioML_class:
    def __init__(
        self,
        model=None,
        modelLib=None,
        iterations=None,
        lr=None,
        depth=None,
        BioML_Version=None,
        organism=None,
        experitment=None,
        rezDivizor=None,
        trainedLabels=None,
        totalLabels=None,
    ):
        self.model = model
        self.modelLib = "sklearn"  # can be skl or catboost
        self.modelType = "RandomForestClassifier"
        self.iterations = 2
        self.lr = 1
        self.depth = 2
        self.BioML_Version = "1"  # this is for making usre that the filters match
        self.organism = "cell"
        self.experiment = "scratch"
        self.rezDivizor = 1
        self.trainedLabels = None  # trainedLabel Data
        self.totalLabels = 2  # up to 2 labels, 0,1....
        self.optimizedModel = None


class ML_ContRun_DialogUi(exitSaveDialog_UI):
    def __init__(self, MainWindow=None):
        self.MainWindow = MainWindow
        self.myDialog = QtWidgets.QDialog()
        self.setupUi(self.myDialog)
        self.myDialog.setFixedWidth(355)
        # self.myDialog.setParent(MainWindow)
        self.label.setText(
            "We generated the new mask for you,\ndo you want to keep it?"
        )
        self.pushButton.setText("Yes")
        self.pushButton_2.setText("Improve")
        self.pushButton_3.setMinimumWidth(60)
        self.pushButton_3.setText("No, dont ask again")
        self.pushButton_3.setMinimumWidth(120)
        self.MainWindow.viewer.ML_brush_tool_object.inferenceUsingLastModel()

        self.pushButton.clicked.connect(lambda: self.infNew())
        self.pushButton_2.clicked.connect(lambda: self.ImproveModel())
        self.pushButton_3.clicked.connect(lambda: self.discardModel())
        self.myDialog.show()

    def infNew(self):
        self.myDialog.close()

    def ImproveModel(self):
        self.MainWindow.viewer.ML_brush_tool_draw_training_mode = "RETRAIN"
        self.MainWindow.actionRF_MODE.trigger()
        self.myDialog.close()

    def discardModel(self):
        self.myDialog.close()
        self.MainWindow.viewer.ML_brush_tool_draw_training_mode = "Medium"
        self.MainWindow.viewer.ML_brush_tool_draw_continous_inference = False
        self.MainWindow.clearRF_CELLS_markers(withImage=False)
        self.MainWindow.viewer.ModelLoadedLabel.deleteLater()


class ML_RF(object):
    def __init__(
        self, input_image=None, ForgroundHint=None, backgroundHint=None, MainWindow=None
    ):
        self.image = input_image
        self.backgroundHint = backgroundHint
        self.forgroundHint = ForgroundHint
        if not isinstance(self.backgroundHint, (np.ndarray, np.generic)):
            self.backgroundHint = np.zeros(
                (self.image.shape[0], self.image.shape[1]), dtype=np.uint8
            )
        if not isinstance(self.forgroundHint, (np.ndarray, np.generic)):
            self.forgroundHint = np.zeros(
                (self.image.shape[0], self.image.shape[1]), dtype=np.uint8
            )

        self.ShrinkEdges = False
        self.MainWindow = MainWindow
        self.FeaturesCalculated = False
        self.ModelIterations = None
        self.ModelDepth = None
        self.ML_RF_Version = "1"
        self.myf = None  # feature builder
        self.ModelLearningRate = None
        self.currentModel = "cell"
        from celer_sight_ai import config

        gl = config.global_signals
        an = self.MainWindow.new_analysis_object
        logger.info("gl is ".format(gl.area))
        logger.info(
            "an is ".format(self.MainWindow.new_analysis_object.area_map["scratch"])
        )
        self.featureModel = self.getFeaturesSingle
        self.fillHoles = False
        self.areaOfInt = gl.area
        self.assayType = an.area_map["scratch"]
        if gl.area == an.area_map["scratch"]:
            logger.info("test pass an gl")
            self.currentModel = "scratch"
            self.resDiv = 15
            self.featureModel = self.getFeaturesWoundHeal
            self.prepModel = self.prepImageForFeatureExtraction_wound_healing
        self.ShrinkEdges = True  # to shring so that we large mask that touches edges doesnt behave weird
        self.fillHoles = True
        self.resDiv = 2
        # if self.MainWindow.viewer.QuickTools.HighResolutionCELLS_RM_checkbox_2.isChecked():
        #     self.resDiv = 1
        self.prepModel = self.prepImageForFeatureExtraction
        self.myPixelClassifier = self.getClassifier()

        from celer_sight_ai import config

        config.global_signals.addToML_Canvas_FG.connect(self.placeDrawingFG_ML)
        config.global_signals.addToML_Canvas_BG.connect(self.placeDrawingBG_ML)
        config.global_signals.update_ML_BitMapScene.connect(self.updateSceneML_BitMap)

    def updateSceneML_BitMap(self):
        import cv2
        # refreshes the green and red view
        import qimage2ndarray

        canvas = np.zeros(
            (
                self.MainWindow.viewer.ML_brush_tool_draw_foreground_array.shape[0],
                self.MainWindow.viewer.ML_brush_tool_draw_foreground_array.shape[1],
                3,
            )
        )

        canvas[:, :, 1] = (
            self.MainWindow.viewer.ML_brush_tool_draw_foreground_array.astype(np.uint8)
            * 255
        )
        canvas[:, :, 0] = (
            self.MainWindow.viewer.ML_brush_tool_draw_background_array.astype(np.uint8)
            * 255
        )

        pixMap = QtGui.QPixmap.fromImage(qimage2ndarray.array2qimage(canvas))
        totalMask = cv2.bitwise_or(
            self.MainWindow.viewer.ML_brush_tool_draw_foreground_array.astype(np.uint8),
            self.MainWindow.viewer.ML_brush_tool_draw_background_array.astype(np.uint8),
        )
        pixMap.setMask(
            QtGui.QPixmap.fromImage(qimage2ndarray.array2qimage(totalMask - 1))
        )
        self.MainWindow.viewer._scene.addPixmap(pixMap)

    def updateCurrentLabels(self, forGround, backGround):
        self.backgroundHint = backGround
        self.forgroundHint = forGround
        if not isinstance(self.backgroundHint, (np.ndarray, np.generic)):
            self.backgroundHint = np.zeros(
                (self.image.shape[0], self.image.shape[1]), dtype=np.uint8
            )
        if not isinstance(self.forgroundHint, (np.ndarray, np.generic)):
            self.forgroundHint = np.zeros(
                (self.image.shape[0], self.image.shape[1]), dtype=np.uint8
            )

    def getClassifier(self):
        from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier

        # Initialize CatBoostClassifier

        self.ModelIterations = 10
        self.ModelLearningRate = 0.2
        self.ModelDepth = 4
        # return CatBoostClassifier(iterations=self.ModelIterations,
        #                             learning_rate=self.ModelLearningRate,
        #                             depth=self.ModelDepth)

        import lightgbm as lgb

        max_depth = self.MainWindow.pg1_ML_advanced_depth_spinbox.value()
        # clf = CatBoostClassifier( iterations=5)
        logger.info(
            "learning_rate is %d ", self.MainWindow.pg1_ML_advanced_lr_spinbox.value()
        )
        logger.info("max_depth is %d ", max_depth)
        logger.info(
            "n_estimators is %d ",
            self.MainWindow.pg1_ML_advanced_estimators_spinbox.value(),
        )

        clf = lgb.LGBMClassifier(
            num_leaves=int((2 ^ (max_depth)) * 0.65),
            max_depth=max_depth,  # LGBMClassifier
            random_state=314,
            silent=True,
            metric="None",
            n_jobs=4,
            n_estimators=self.MainWindow.pg1_ML_advanced_estimators_spinbox.value(),
            colsample_bytree=0.9,
            subsample=0.9,
            learning_rate=self.MainWindow.pg1_ML_advanced_lr_spinbox.value(),
        )
        return clf

        # return CatBoostClassifier( iterations=400)
        # learning_rate=0.2,max_depth=3 ,l2_leaf_reg = 1,border_count = 20\
        #     ,random_state = 15)
        # return RandomForestClassifier(\
        #     n_estimators = 200,n_jobs=-1)

    def getResDiv(self):
        # if self.MainWindow.viewer.QuickTools.HighResolutionCELLS_RM_checkbox_2.isChecked():
        #     return 1
        if self.areaOfInt == self.assayType:
            # wound heal
            return 2
        else:
            return 2

    def getFilters(self):
        config.global_signals.PreProcessingLabeUpdatelSignal.emit()
        from sklearn.model_selection import train_test_split
        import time
        import numpy as np
        import cv2
        import pandas as pd
        from skimage.transform import rescale, resize, downscale_local_mean

        img = self.image.copy()
        df, rbgImage = self.prepModel(img + 1)
        # else:

        df = self.featureModel(df, rbgImage, img)
        self.currentFeatures = df
        self.FeaturesCalculated = True

    def update_MODE_ML(self):
        img = self.image.copy()
        df, rbgImage = self.prepModel(img + 1)
        df = self.featureModel(df, rbgImage, img)
        self.currentFeatures = df

    def trainNormal(self):
        from sklearn.model_selection import train_test_split
        import time
        import numpy as np
        import cv2
        import skimage
        import pandas as pd
        from skimage.transform import rescale, resize, downscale_local_mean
        import pickle

        if self.FeaturesCalculated == False:
            start = time.time()
            img = self.image.copy()
            df, rbgImage = self.prepModel(img + 1)

            # else:
            startCompute = time.time()
            df = self.featureModel(df, rbgImage, img)
            logger.info("time to compute = ", time.time() - startCompute)
        else:
            if "Labels" in self.currentFeatures.columns:
                df = self.currentFeatures.drop(labels=["Labels"], axis=1).copy()
            else:
                df = self.currentFeatures.copy()
        start = time.time()
        startCompute = time.time()
        logger.info("time to compute = ", time.time() - startCompute)

        self.labeledImage = np.zeros(
            (self.backgroundHint.shape[0], self.backgroundHint.shape[1]), dtype=np.uint8
        )
        self.labeledImage[self.backgroundHint] = 1
        self.labeledImage[self.forgroundHint] = 2

        labeled_img_org = self.labeledImage
        orgShape1 = labeled_img_org.shape[0]
        orgShape2 = labeled_img_org.shape[1]
        labeled_img_org = resize(
            labeled_img_org,
            (
                labeled_img_org.shape[0] // self.getResDiv(),
                labeled_img_org.shape[1] // self.getResDiv(),
            ),
        )

        labeled_img_org = (labeled_img_org * 255).astype(np.uint8)
        labeled_img1 = labeled_img_org.reshape(-1)
        PrevDf = df.copy()
        df["Labels"] = labeled_img1
        df = df[(df.Labels == 1) | (df.Labels == 2)]
        logger.info("cols are: ")
        for col in df.columns:
            logger.info(col)
        if self.MainWindow.viewer.ML_brush_tool_draw_training_mode == "NORMAL":
            self.MainWindow.prevDf_RF = df.copy()
        if self.MainWindow.viewer.ML_brush_tool_draw_training_mode == "RETRAIN":
            logger.info("RETRAINING")
            logger.info(df.shape[0])
            logger.info(self.MainWindow.prevDf_RF_Trained.shape[0])

            df = pd.concat([df, self.MainWindow.prevDf_RF_Trained])
            self.MainWindow.prevDf_RF = df.copy()

        # logger.info("dataframe finaly is ",df)
        # Define the dependent variable that needs to be predicted (labels)
        Y = df["Labels"].to_numpy()
        # Define the independent variables
        X = df.drop(labels=["Labels"], axis=1).to_numpy()

        # Split data into train and test to verify accuracy after fitting the model.
        # from sklearn.model_selection import train_test_split
        # X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.1, random_state=42)

        X_train = X
        y_train = Y

        # RANDOM FOREST
        import time

        model_RF = self.myPixelClassifier

        config.global_signals.trainingLabelUpdateSignal.emit()
        startSKLEARN = time.time()
        # Train the model on training data
        # X_train_PCA, myPCA = self.doPCA(X_train)

        model_RF.fit(X_train, y_train.astype(np.float))
        config.global_signals.spawnLoadedMLModelSignal.emit()
        config.global_signals.predictingLabeUpdatelSignal.emit()
        logger.info("train took ".format(time.time() - startSKLEARN))

        # Test prediction on testing data.
        # prediction_test_RF = model_RF.predict(X_test)#
        self.MainWindow.viewer.ML_brush_tool_draw_last_model = model_RF
        # df_Feature ,  rbgImage= self.prepModel(img)

        # if useMulticore == True:
        #     # Time the code below.
        #     num_cpus = psutil.cpu_count(logical=False)
        #     # ray.init(num_cpus=num_cpus)
        #     # Start 4 tasks in parallel.
        #     result_ids = []
        #     Shared_Image = ray.put(rbgImage)
        #     Shared_df= ray.put(df_Feature)
        #     for i in range(4):
        #         result_ids.append(getFeatures.remote(Shared_df, Shared_Image,i))
        #     df_list = ray.get(result_ids)  # [0, 1, 2, 3]
        #     # for i in range(5):
        #     #     logger.info("now iterator is ",_)
        #     #     ray.get([getFeatures.remote(Shared_df, Shared_df,i) for i in range(num_cpus)])
        #     # dfPred = self.getFeatures(df_Feature , rbgImage)
        #     dfPred = pd.concat(df_list, axis=1)
        # else:
        #     dfPred = getFeaturesSingle(df_Feature ,  rbgImage)
        dfPred = PrevDf
        beforePred = time.time()
        # predictPCA = myPCA.transform( dfPred)
        # logger.info(dfPred)

        prediction_test_RF = model_RF.predict(dfPred)  # img.copy().reshape(-1))
        logger.info("time to predict: ".format(time.time() - beforePred))
        logger.info(prediction_test_RF)

        # # Convert into ONNX format
        # from skl2onnx import convert_sklearn
        # from skl2onnx.common.data_types import FloatTensorType,Int32TensorType
        # outArrayPred = dfPred.to_numpy().astype(np.float)
        # initial_type = [('float_input', FloatTensorType([None, outArrayPred.shape[1]]))]

        # onx = convert_sklearn(model_RF, initial_types=initial_type,target_opset=11)
        # with open("rf_iris.onnx", "wb") as f:
        #     f.write(onx.SerializeToString())

        # # Compute the prediction with ONNX Runtime
        # import onnxruntime as rt
        # import numpy
        # import torch

        # sess = rt.InferenceSession("rf_iris.onnx")
        # sess.set_providers(['DmlExecutionProvider'])
        # input_name = sess.get_inputs()[0].name
        # label_name = sess.get_outputs()[0].name
        # startONNX = time.time()
        # pred_onx = sess.run([label_name], {input_name: dfPred.to_numpy().astype(np.float32)})[0]

        # logger.info('to predict onnx took ', time.time() - startONNX)

        prediction_test_RF = prediction_test_RF.reshape(
            labeled_img_org.shape[0], labeled_img_org.shape[1]
        )
        prediction_test_RF_F = prediction_test_RF - 1

        prediction_test_RF_F = (prediction_test_RF_F * 255).astype(np.uint8)
        # cv2.imshow("dasda",prediction_test_RF_F)
        # cv2.waitKey()
        kernel = np.ones((3, 3), np.uint8)
        # if self.MainWindow.viewer.QuickTools.clearIsletsCELLS_RM_checkbox.isChecked():
        # prediction_test_RF_F = cv2.erode(prediction_test_RF_F,kernel,iterations = 1)
        # prediction_test_RF_F = cv2.dilate(prediction_test_RF_F,kernel,iterations =1)

        prediction_test_RF_F = resize(prediction_test_RF_F, (orgShape1, orgShape2))
        if self.ShrinkEdges == True:  # for woundhealing
            prediction_test_RF_F = cv2.rectangle(
                prediction_test_RF_F,
                (0, 0),
                (prediction_test_RF_F.shape[1], prediction_test_RF_F.shape[0]),
                (0),
                2,
            ).astype(np.uint8)
        if self.fillHoles == True:
            from scipy import ndimage

            prediction_test_RF_F = ndimage.binary_fill_holes(prediction_test_RF_F)
        logger.info("current model is")
        if self.currentModel == "scratch":
            logger.info("IT IS SRATCJ")
            prediction_test_RF_F = (
                get_largest_area(prediction_test_RF_F) * 255
            ).astype(np.uint8)

        logger.info("final time is ", time.time() - start)
        listAllMasks = []
        startControur = time.time()
        contours = skimage.measure.find_contours(prediction_test_RF_F, 0.8)
        if self.currentModel == "scratch":
            startLen = 0
            for cont in contours:
                inLen = len(cont)
                if inLen > startLen:
                    finalCont = cont
                    startLen = inLen

            appr_hand = skimage.measure.approximate_polygon(
                np.asarray(finalCont), tolerance=1.2
            ).astype(np.uint16)

            listAllMasks.append(
                QtGui.QPolygonF([QtCore.QPointF(p[1], p[0]) for p in appr_hand])
            )
        else:
            for i in range(len(contours)):
                new_hand = skimage.measure.approximate_polygon(
                    np.asarray(contours[i]), tolerance=1.2
                ).astype(np.uint16)
                new_hand = skimage.measure.subdivide_polygon(
                    new_hand, degree=2, preserve_ends=True
                )
                new_hand = skimage.measure.subdivide_polygon(
                    new_hand, degree=2, preserve_ends=True
                )
                new_hand = skimage.measure.subdivide_polygon(
                    new_hand, degree=2, preserve_ends=True
                )

                appr_hand = skimage.measure.approximate_polygon(
                    new_hand, tolerance=1.2
                ).astype(np.uint16)

                listAllMasks.append(
                    QtGui.QPolygonF([QtCore.QPointF(p[1], p[0]) for p in appr_hand])
                )

        self.MainWindow.viewer.ML_brush_tool_draw_continous_inference = True
        self.MainWindow.viewer.makeAllGraphicItemsNonSelectable()

        return listAllMasks

    def train_light(self):
        from celer_sight_ai.io.lightbgm_handle import train_light_model

        # convert to one image starting from label 1,the background, 2 is forground
        train_light_model(self.image.copy(), self.forgroundHint, self.backgroundHint)

    def doPCA(self, X_train):
        from sklearn.preprocessing import StandardScaler

        # import  as PCA
        scaler = StandardScaler()
        scaler.fit(X_train)
        X_train = scaler.transform(X_train)
        print
        import sklearn
        import sklearn.decomposition

        pca = sklearn.decomposition.PCA(n_components=45)
        pca.fit(X_train)
        X_train = pca.transform(X_train)
        return X_train, pca

    def improveTrainedModel(self):
        import skimage
        from sklearn.model_selection import train_test_split
        import time
        import numpy as np
        import cv2
        import pandas as pd
        from skimage.transform import rescale, resize, downscale_local_mean

        if self.FeaturesCalculated == False:
            start = time.time()
            img = self.image.copy()
            df, rbgImage = self.prepModel(img + 1)

            # else:
            startCompute = time.time()
            df = self.featureModel(df, rbgImage, img)
            logger.info("time to compute = ", time.time() - startCompute)
        else:
            df = self.currentFeatures
        self.labeledImage = np.zeros(
            (self.backgroundHint.shape[0], self.backgroundHint.shape[1]), dtype=np.uint8
        )
        self.labeledImage[self.backgroundHint] = 1
        self.labeledImage[self.forgroundHint] = 2

        labeled_img_org = self.labeledImage
        orgShape1 = labeled_img_org.shape[0]
        orgShape2 = labeled_img_org.shape[1]
        labeled_img_org = resize(
            labeled_img_org,
            (
                labeled_img_org.shape[0] // self.getResDiv(),
                labeled_img_org.shape[1] // self.getResDiv(),
            ),
        )

        labeled_img_org = (labeled_img_org * 255).astype(np.uint8)
        labeled_img1 = labeled_img_org.reshape(-1)
        PrevDf = df.copy()

        # get only the values that we need to the dataframe
        df["Labels"] = labeled_img1
        df = df[(df.Labels == 1) | (df.Labels == 2)]

        self.prevDf = df.copy()
        # Define the dependent variable that needs to be predicted (labels)
        Y = df["Labels"].values
        # Define the independent variables
        X = df.drop(labels=["Labels"], axis=1)

        # Split data into train and test to verify accuracy after fitting the model.
        from sklearn.model_selection import train_test_split

        X_train, X_test, y_train, y_test = train_test_split(
            X, Y, test_size=0.2, random_state=42
        )

        # X_train = Y
        # y_train = X
        # RANDOM FOREST
        from sklearn.ensemble import RandomForestClassifier
        import time

        model_RF = self.myPixelClassifier

        # Train the model on training data
        model_RF.fit(X_train, y_train)
        config.global_signals.spawnLoadedMLModelSignal.emit()
        logger.info("time to train: ".format(time.time() - start))
        # Test prediction on testing data.
        # prediction_test_RF = model_RF.predict(X_test)#
        self.MainWindow.viewer.ML_brush_tool_draw_last_model = model_RF
        df_Feature, rbgImage = self.prepModel(img)

        # if useMulticore == True:
        #     # Time the code below.
        #     num_cpus = psutil.cpu_count(logical=False)
        #     # ray.init(num_cpus=num_cpus)
        #     # Start 4 tasks in parallel.
        #     result_ids = []
        #     Shared_Image = ray.put(rbgImage)
        #     Shared_df= ray.put(df_Feature)
        #     for i in range(4):
        #         result_ids.append(getFeatures.remote(Shared_df, Shared_Image,i))
        #     df_list = ray.get(result_ids)  # [0, 1, 2, 3]
        #     # for i in range(5):
        #     #     logger.info("now iterator is ",_)
        #     #     ray.get([getFeatures.remote(Shared_df, Shared_df,i) for i in range(num_cpus)])
        #     # dfPred = self.getFeatures(df_Feature , rbgImage)
        #     dfPred = pd.concat(df_list, axis=1)
        # else:
        #     dfPred = getFeaturesSingle(df_Feature ,  rbgImage)
        dfPred = PrevDf
        beforePred = time.time()
        prediction_test_RF = model_RF.predict(dfPred)  # img.copy().reshape(-1))
        logger.info("time to predict: ".format(time.time() - beforePred))

        prediction_test_RF = prediction_test_RF.reshape(
            labeled_img_org.shape[0], labeled_img_org.shape[1]
        )
        prediction_test_RF_F = prediction_test_RF - 1
        # if not self.currentModel == 'scratch':

        if self.currentModel == "scratch":
            prediction_test_RF_F = (
                get_largest_area(prediction_test_RF_F) * 255
            ).astype(np.uint8)
            # prediction_test_RF_F = (prediction_test_RF_F * 255).astype(np.uint8)

        kernel = np.ones((3, 3), np.uint8)

        # if self.MainWindow.viewer.QuickTools.clearIsletsCELLS_RM_checkbox.isChecked():
        #     prediction_test_RF_F = cv2.erode(prediction_test_RF_F,kernel,iterations = 1)
        #     prediction_test_RF_F = cv2.dilate(prediction_test_RF_F,kernel,iterations =1)

        prediction_test_RF_F = resize(prediction_test_RF_F, (orgShape1, orgShape2))
        if self.ShrinkEdges == True:  # for woundhealing
            prediction_test_RF_F = cv2.rectangle(
                prediction_test_RF_F,
                (0, 0),
                (prediction_test_RF_F.shape[1], prediction_test_RF_F.shape[0]),
                (0),
                2,
            ).astype(np.uint8)
        if self.fillHoles == True:
            from scipy import ndimage

            prediction_test_RF_F = ndimage.binary_fill_holes(prediction_test_RF_F)
        logger.info("final time is ".format(time.time() - start))
        listAllMasks = []
        startControur = time.time()
        contours = skimage.measure.find_contours(
            prediction_test_RF_F,
            0.8,
            fully_connected="high",
            positive_orientation="high",
        )
        logger.info("contours take: ".format(time.time() - startControur))
        startControur = time.time()
        if self.currentModel == "scratch":
            startLen = 0
            for cont in contours:
                inLen = len(cont)
                if inLen > startLen:
                    finalCont = cont
                    startLen = inLen
            appr_hand = skimage.measure.approximate_polygon(
                np.asarray(finalCont), tolerance=1
            ).astype(np.uint16)
            listAllMasks.append(
                QtGui.QPolygonF([QtCore.QPointF(p[1], p[0]) for p in appr_hand])
            )
        else:
            for i in range(len(contours)):
                appr_hand = skimage.measure.approximate_polygon(
                    np.asarray(contours[i]), tolerance=1.2
                ).astype(np.uint16)
                listAllMasks.append(
                    QtGui.QPolygonF([QtCore.QPointF(p[1], p[0]) for p in appr_hand])
                )

        logger.info("islets took".fromat(time.time() - startControur))
        self.MainWindow.viewer.ML_brush_tool_draw_continous_inference = True
        self.MainWindow.viewer.makeAllGraphicItemsNonSelectable()
        return listAllMasks

    def inferenceUsingLastModel(self):
        import cv2
        import skimage
        # does inf on the current image using last model
        origImage = (
            self.MainWindow.DH.BLobj.groups["default"]
            .conds[self.MainWindow.DH.BLobj.get_current_condition()]
            .getImage(self.MainWindow.current_imagenumber)
            .copy()
        )

        orgShape11 = origImage.shape[0]
        orgShape22 = origImage.shape[1]

        orgShape1 = origImage.shape[0] // self.getResDiv()
        orgShape2 = origImage.shape[1] // self.getResDiv()

        df_Feature, rbgImage = self.prepModel(origImage + 1)
        df = self.featureModel(df_Feature, rbgImage, origImage)

        prediction_test_RF = (
            self.MainWindow.viewer.ML_brush_tool_draw_last_model.predict(df_Feature)
        )
        prediction_test_RF = prediction_test_RF.reshape(orgShape1, orgShape2)
        prediction_test_RF_F = prediction_test_RF - 1
        prediction_test_RF_F = (prediction_test_RF_F * 255).astype(np.uint8)
        kernel = np.ones((3, 3), np.uint8)
        prediction_test_RF_F = cv2.erode(prediction_test_RF_F, kernel, iterations=1)
        prediction_test_RF_F = cv2.dilate(prediction_test_RF_F, kernel, iterations=1)

        if self.currentModel == "scratch":
            prediction_test_RF_F = (
                get_largest_area(prediction_test_RF_F) * 255
            ).astype(np.uint8)

        prediction_test_RF_F = resize(prediction_test_RF_F, (orgShape11, orgShape22))
        if self.ShrinkEdges == True:  # for woundhealing
            prediction_test_RF_F = cv2.rectangle(
                prediction_test_RF_F,
                (0, 0),
                (prediction_test_RF_F.shape[1], prediction_test_RF_F.shape[0]),
                (0),
                2,
            ).astype(np.uint8)
            # prediction_test_RF_F = get_largest_area(prediction_test_RF_F)*255
        if self.fillHoles == True:
            from scipy import ndimage

            prediction_test_RF_F = ndimage.binary_fill_holes(prediction_test_RF_F)
        listAllMasks = []

        contours = skimage.measure.find_contours(prediction_test_RF_F, 0.8)
        if self.currentModel == "scratch":
            startLen = 0
            for cont in contours:
                inLen = len(cont)
                if inLen > startLen:
                    finalCont = cont
                    startLen = inLen
            appr_hand = skimage.measure.approximate_polygon(
                np.asarray(finalCont), tolerance=1.2
            ).astype(np.uint16)
            listAllMasks.append(
                QtGui.QPolygonF([QtCore.QPointF(p[1], p[0]) for p in appr_hand])
            )
        else:
            for i in range(len(contours)):
                appr_hand = skimage.measure.approximate_polygon(
                    np.asarray(contours[i]), tolerance=1.2
                ).astype(np.uint16)
                listAllMasks.append(
                    QtGui.QPolygonF([QtCore.QPointF(p[1], p[0]) for p in appr_hand])
                )
        self.MainWindow.DH.BLobj.groups["default"].conds[
            self.MainWindow.DH.BLobj.get_current_condition()
        ].images[self.MainWindow.current_imagenumber].clearMasks()
        for mask1 in listAllMasks:
            from celer_sight_ai import config

            config.global_signals.create_annotation_object_signal.emit(
                {
                    "treatment_uuid": self.MainWindow.DH.BLobj.get_current_image_uuid(),
                    "array": [mask1],
                    "image_uuid": self.MainWindow.DH.BLobj.get_current_image_uuid(),
                    "class_id": self.MainWindow.custom_class_list_widget.currentItemWidget().text(),
                    # None,  # TODO: needs to be changed
                }
            )

        # self.MainWindow.DH.BLobj.groups['default'].conds[self.MainWindow.DH.BLobj.get_current_condition()].images[self.MainWindow.current_imagenumber].addMasksBulk(listAllMasks)
        self.MainWindow.viewer.makeAllGraphicItemsNonSelectable()

        return

    def prepImageForFeatureExtraction(self, img):
        import pandas as pd
        import cv2
        from scipy import ndimage

        img = resize(
            img, (img.shape[0] // self.getResDiv(), img.shape[1] // self.getResDiv())
        )
        img = (img * 255).astype(np.uint8)

        r, g, b = cv2.split(img)
        rbgImage = [r, g, b]
        img2 = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Save original image pixels into a data frame. This is our Feature #1.
        img2 = img.reshape(-1)

        imgR = rbgImage[0].reshape(-1)
        imgG = rbgImage[1].reshape(-1)
        imgB = rbgImage[2].reshape(-1)

        df = pd.DataFrame()

        df["Original R"] = imgR
        df["Original G"] = imgG
        df["Original B"] = imgB

        return df, rbgImage

    def placeDrawingFG_ML(self, MasterList=[]):
        """
        This function puts the Qpoints on their place along with the widgets
        """
        # for Condition, value in self.MainWindowRef.DH.BLobj.groups['default'].conds.items():
        #     for x in range(len(self.MainWindowRef.DH.BLobj.groups['default'].conds[Condition])):
        #         image = self.MainWindowRef.DH.BLobj.groups['default'].conds[Condition][x]
        logger.info("placeDrawingFG_ML RUNS")

        imID = MasterList[0]
        Condition = MasterList[1]
        Mask = MasterList[2]
        # className = MasterList[3]
        # clear out the bg mask:
        self.MainWindow.viewer.ML_brush_tool_draw_background_array[Mask] = False

        # draw on fg mask
        self.MainWindow.viewer.ML_brush_tool_draw_foreground_array[Mask] = True

    def placeDrawingBG_ML(self, MasterList=[]):
        """
        This function puts the Qpoints on their place along with the widgets
        """
        # for Condition, value in self.MainWindowRef.DH.BLobj.groups['default'].conds.items():
        #     for x in range(len(self.MainWindowRef.DH.BLobj.groups['default'].conds[Condition])):
        #         image = self.MainWindowRef.DH.BLobj.groups['default'].conds[Condition][x]
        logger.info("placeDrawingFG_ML RUNS")
        import skimage

        imID = MasterList[0]
        Condition = MasterList[1]
        Mask = MasterList[2]
        # clear out the fg mask:
        self.MainWindow.viewer.ML_brush_tool_draw_foreground_array[Mask] = False

        # draw on bg mask
        self.MainWindow.viewer.ML_brush_tool_draw_background_array[Mask] = True

    def prepImageForFeatureExtraction_wound_healing(self, img):
        import cv2
        import pandas as pd
        from scipy import ndimage

        img = resize(
            img, (img.shape[0] // self.getResDiv(), img.shape[1] // self.getResDiv())
        )
        img = (img * 255).astype(np.uint8)

        # r , g , b =  cv2.split(img)
        # rbgImage = [r,g,b]
        img2_ORIG = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Save original image pixels into a data frame. This is our Feature #1.
        img2 = img2_ORIG.copy().reshape(-1)

        df = pd.DataFrame()
        df["Original"] = img2

        return df, img2_ORIG

    def saveBioMLModel(self):
        import sklearn
        import catboost
        import pickle

        # if self.MainWindow.viewer.ML_brush_tool_draw_last_model:
        #     model = self.MainWindow.viewer.ML_brush_tool_draw_last_model
        # else:
        #     raise ValueError("No model detected, make sure that you have labeled an image")
        # if isinstance(self.myPixelClassifier, sklearn.ensemble.forest.RandomForestClassifier):
        #     modelLib = 'sklearn'
        #     modelType = 'RandomForestClassifier'
        # elif isinstance(self.myPixelClassifier, catboost.CatBoostClassifier):
        #     modelLib = 'catboost'
        #     modelType = 'CatBoostClassifier'
        # else:
        #     raise("Not supported Loaded Model")
        # iterations = self.ModelIterations
        # lr = self.ModelLearningRate
        # depth = self.ModelDepth
        # BioML_Version = self.ML_RF_Version

        # if  self.currentModel == 'cells':
        #     organism = 'cells'
        #     experitment = 'generic'
        # elif self.currentModel == 'scratch':
        #     organism = 'cells'
        #     experitment = self.currentModel
        # else:
        #     raise ValueError("Could not figure out type of expiriment, please save your work and restart.")
        # # rezDivizor

        # def wrapBioMLModel
        modelContainer = {}
        modelContainer["featureBuilder"] = self.myf
        modelContainer["allFeatures"] = self.MainWindow.prevDf_RF_Trained
        # pickle save location

        # save model as a dict with model and labels included
        locationToSave = QtWidgets.QFileDialog.getSaveFileName(
            self.MainWindow, "Load styles file", filter=".pkl"
        )
        # dictModel = {'model':self.MainWindow.viewer.ML_brush_tool_draw_last_model\
        #     , 'labels':}
        pickle.dump(modelContainer, open(locationToSave[0], "wb"))


    def getFeaturesWoundHeal(self, df, rbgImage, origImage):
        import time
        import cv2
        # Generate Gabor features
        num = 1  # To count numbers up in order to give Gabor features a lable in the data frame
        kernels = []
        logger.info("WOUND HEALIGG GET FEATURES")

        for i in range(3):
            for theta in range(6):  # Define number of thetas
                theta = theta / 4.0 * np.pi
                for lamda in np.arange(0, np.pi, np.pi / 2):  # Range of wavelengths
                    gabor_label = "Gabor" + str(
                        num
                    )  # Label Gabor columns as Gabor1, Gabor2, etc.
                    ksize = 9
                    kernel = cv2.getGaborKernel(
                        (ksize, ksize), 2, theta, lamda, 0.1, 0, ktype=cv2.CV_32F
                    )
                    kernels.append(kernel)
                    # Now filter the image and add values to a new column
                    fimg = cv2.filter2D(rbgImage[i], cv2.CV_8UC3, kernel)
                    filtered_img = fimg.reshape(-1)
                    # logger.info("filtered_img ".format(filtered_img.shape))
                    df[gabor_label] = (
                        filtered_img  # Labels columns as Gabor1, Gabor2, etc.
                    )
                    num += 1  # Increment for gabor column label

        for i in range(3):
            for y in range(6):
                th3 = cv2.adaptiveThreshold(
                    rbgImage[i],
                    255,
                    cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                    cv2.THRESH_BINARY,
                    (5 * (y + 1)) + (y),
                    2,
                )
                filtered_img = th3.reshape(-1)
                # logger.info("filtered_img ".format(filtered_img.shape))

                # gabor_label = "AdaptiveThresh" +str(num)

                df[gabor_label] = filtered_img  # Labels columns as Gabor1, Gabor2, etc.
                num += 1

        resizeBy = 2
        contrast = 4
        varrbgImage = cv2.cvtColor(origImage, cv2.COLOR_BGR2GRAY)
        # varrbgImage = cv2.convertScaleAbs(varrbgImage, alpha=contrast, beta=-(contrast*(100)))
        # myimg = cv2.medianBlur(myimg,101)

        # GrayImage = cv2.cvtColor(varrbgImage,cv2.COLOR_GRAY2RGB)
        # GrayImageOrig = GrayImage.copy()
        GrayImage = resize(
            varrbgImage,
            (
                varrbgImage.shape[0] // self.getResDiv(),
                varrbgImage.shape[1] // self.getResDiv(),
            ),
        )
        for i in range(5):
            gabor_label = "variance" + str(num)
            # logger.info(i)
            # logger.info(GrayImage.shape)
            final = variance_filter(GrayImage, (i + 1) * 3)
            filtered_img = final.reshape(-1)
            # logger.info("filtered_img ", filtered_img.shape)
            df[gabor_label] = filtered_img  # Labels columns as Gabor1, Gabor2, etc.
            num += 1  # Increment for gabor column label

        return df  # ,img2_ORIG

    def on_pg1_ML_EXCLUDE_QUALITY_COMBOBOX_change(self):
        # when we change the quality of ML model, ask user if he would like to procceed, delete models up to now.
        ct = self.MainWindow.pg1_ML_EXCLUDE_QUALITY_COMBOBOX.currentText()
        # self.WarnWindow =
        #  WarningUi(errorCode = "Could not load file, maybe corrupted.", title = "Error")

    def getFeaturesSingle(self, df, rgbImage, origImage=None, multiRez=4):
        import time

        # Generate Gabor features
        num = 1  # To count numbers up in order to give Gabor features a lable in the data frame
        kernels = []
        logger.info("id1")
        id1 = time.time()

        self.myf = featureBuilder()
        if self.MainWindow.pg1_ML_EXCLUDE_QUALITY_COMBOBOX.currentText() == "High":
            mode = "High"
        if self.MainWindow.pg1_ML_EXCLUDE_QUALITY_COMBOBOX.currentText() == "Ultra":
            mode = "Ultra"
        if self.MainWindow.pg1_ML_EXCLUDE_QUALITY_COMBOBOX.currentText() == "Low":
            mode = "Low"
        if self.MainWindow.pg1_ML_EXCLUDE_QUALITY_COMBOBOX.currentText() == "Medium":
            mode = "Medium"

        rbgImage_multiRez = []
        for i in range(multiRez):
            if i == 0:
                rbgImage_multiRez.append(rgbImage)
                continue
            else:
                tmpArray = []
                for z in range(len(rgbImage)):
                    resizeFactor = i + 1
                    tmpArray.append(
                        resize(
                            rgbImage[z],
                            (
                                rgbImage[z].shape[0] // resizeFactor,
                                rgbImage[z].shape[1] // resizeFactor,
                            ),
                        )
                    )
                rbgImage_multiRez.append(tmpArray)

        df = self.myf.runCreateFeatures(rbgImage_multiRez, df, MODE=mode)

        # for i in range(3):
        #     for theta in range(6):   #Define number of thetas
        #         theta = theta / 4. * np.pi
        #         for lamda in np.arange(0, np.pi, np.pi / 2):   #Range of wavelengths
        #             gabor_label = "Gabor" +str(num)  #Label Gabor columns as Gabor1, Gabor2, etc.
        #             logger.info(gabor_label)
        #             ksize=9
        #             kernel = cv2.getGaborKernel((ksize, ksize), 2, theta, lamda, 0.1, 0, ktype=cv2.CV_32F)
        #             kernels.append(kernel)
        #             #Now filter the image and add values to a new column
        #             fimg = cv2.filter2D(rbgImage[i], cv2.CV_8UC3, kernel)
        #             # cv2.imshow("gab", fimg)
        #             # cv2.waitKey()
        #             filtered_img = fimg.reshape(-1)
        #             logger.info("filtered_img ", filtered_img.shape)
        #             df[gabor_label] = filtered_img  #Labels columns as Gabor1, Gabor2, etc.
        #             num += 1  #Increment for gabor column label
        # logger.info("fid 1 takes ", time.time()-id1)
        # id2 = time.time()
        # for i in range(3):
        #     for y in range(6):
        #         th3 = cv2.adaptiveThreshold(rbgImage[i],255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,\
        #             cv2.THRESH_BINARY,(5*(y+1))+(y),2)
        #         filtered_img = th3.reshape(-1)
        #         logger.info("filtered_img ", filtered_img.shape)

        #         gabor_label = "AdaptiveThresh" +str(num)
        #         logger.info(gabor_label)

        #         df[gabor_label] = filtered_img  #Labels columns as Gabor1, Gabor2, etc.
        #         num += 1
        # logger.info("fid 2 takes ", time.time()-id2)
        # id3 = time.time()

        # for i in range(3):
        #     for y in range(5):
        #         result = ndimage.gaussian_laplace(rbgImage[i], sigma=0.5*(y+1))
        #         # cv2.imshow('laplace',result)
        #         # cv2.waitKey()
        #         filtered_img = result.reshape(-1)
        #         gabor_label = "LablaceGaussian" +str(num)
        #         logger.info(gabor_label)

        #         df[gabor_label] = filtered_img  #Labels columns as Gabor1, Gabor2, etc.
        #         num += 1
        # logger.info("fid 3 takes ", time.time()-id3)
        # id4 = time.time()

        # for i in range(3):
        #     for y in range(3):

        #         result = ndimage.gaussian_gradient_magnitude(rbgImage[i], sigma=2.5*(y+1))
        #         # cv2.imshow("gradient gauseian", result)
        #         # cv2.waitKey()
        #         filtered_img = result.reshape(-1)
        #         gabor_label = "GaussianGradient" +str(num)

        #         df[gabor_label] = filtered_img  #Labels columns as Gabor1, Gabor2, etc.
        #         num += 1
        # # logger.info("fid 4 takes ", time.time()-id4)
        # id5 = time.time()

        # for i in range(3):
        #     result = doSobel(rbgImage[i])
        #     filtered_img = result.reshape(-1)
        #     gabor_label = "Sobel" +str(num)
        #     logger.info(gabor_label)

        #     df[gabor_label] = filtered_img  #Labels columns as Gabor1, Gabor2, etc.
        #     num += 1
        # logger.info("fid 5 takes ", time.time()-id5)
        # resizeBy = 2
        # contrast =4
        # # GrayImage = cv2.cvtColor(origImage, cv2.COLOR_BGR2GRAY)

        # # GrayImage = (resize(GrayImage, (GrayImage.shape[0] // self.resDiv, GrayImage.shape[1] // self.resDiv),
        # #                 anti_aliasing=False)*255).astype(np.uint8)
        # for i in range(3):
        #     for x in range(3):
        #         gabor_label = "variance" +str(num)
        #         logger.info(x)
        #         final = variance_filter(rbgImage[i],((x*2)+1)*3)
        #         # _, final = cv2.threshold(final, 30, 31, cv2.THRESH_BINARY )
        #         # final = scipy.ndimage.morphology.binary_fill_holes(final)*255
        #         # cv2.imshow("variacne", final)
        #         # cv2.waitKey()
        #         filtered_img = final.reshape(-1)
        #         logger.info("filtered_img ", filtered_img.shape)
        #         df[gabor_label] = filtered_img  #Labels columns as Gabor1, Gabor2, etc.
        #         num += 1  #Increment for gabor column label
        # low_sigma = 1
        # for z in range(3):
        #     for i in range(4):
        #         for x in range(2):
        #             gabor_label = "difference_of_gaussians" +str(num)
        #             imOut = skimage.filters.difference_of_gaussians(rbgImage[z], low_sigma * (i+2) ,high_sigma = ((x+1)*(1.6*(i+2))) * low_sigma )
        #             # cv2.imshow('dif of gaussian' , imOut)
        #             # cv2.waitKey()
        #             filtered_img = imOut.reshape(-1)
        #             df[gabor_label] = filtered_img
        #             num += 1

        return df


def doSobel(im):
    from scipy import ndimage

    dx = ndimage.sobel(im, 0)  # horizontal derivative
    dy = ndimage.sobel(im, 1)  # vertical derivative
    mag = np.hypot(dx, dy)  # magnitude

    myMax = np.max(mag)
    if myMax == None or myMax == 0:
        return mag
    mag *= 255.0 / np.max(mag)  # Mediumize (Q&D)

    return mag


def variance_filter(img, VAR_FILTER_SIZE):
    """
    this filter is usefull for getting scratch features
    """
    from scipy import ndimage
    img = img.astype(np.float)

    rows, cols = img.shape[0], img.shape[1]
    win_rows, win_cols = VAR_FILTER_SIZE, VAR_FILTER_SIZE
    win_mean = ndimage.uniform_filter(img, (win_rows, win_cols))
    win_sqr_mean = ndimage.uniform_filter(img**2, (win_rows, win_cols))
    win_var = win_sqr_mean - win_mean**2
    return win_var


class Grab_cut_tool(object):
    """
    Class for handling mainly the Threshold adjustment and Grabcut function
    """

    suffix = ".jpg"

    # from scipy.cluster.vq import *
    def __init__(self, input_image=None):
        self.input_image = input_image
        self.height = None  # of the cut
        self.width = None  # of the cut
        self.running = False  # if we are currently grabcutting
        self.brush_state = "plus"  # or "minus" or move?
        # self.input_mask =

    def resize_array(self, input_array):
        return input_array[:] // self.reduced_by

    def resize_up(self, image, original_shape_1, original_shape_2):
        return resize(
            image * 255,
            (original_shape_1, original_shape_2),
            anti_aliasing=True,
            preserve_range=True,
        )

    def resize_down(self, image):
        return resize(
            image,
            (image.shape[0] // self.reduced_by, image.shape[1] // self.reduced_by),
            anti_aliasing=True,
            preserve_range=True,
        )

    def threshold_adjuster(self, img):
        import scipy.ndimage as ndi
        import skimage
        from skimage.transform import rescale, resize, downscale_local_mean

        """

        This function finds the threshold to be fed as a Probable Forground to the Grab Cut tool

        maybe i can do eq then utsu thresh then watershed with graph cut and emit everyhing that is touching to end, orr count it as buckground?

        """
        self.shape_0_original = img.shape[0]
        self.shape_1_original = img.shape[1]
        self.reduced_by = 2  # aa_tool.detail_value

        # resize image by a specific number ti makes calculations easier meaybe improve acuratcy too
        self.resized_image = resize(
            img, (img.shape[0] // self.reduced_by, img.shape[1] // self.reduced_by)
        )

        th3 = None
        return th3

    def grab_cut_v2(
        self,
        threshed_image,
        aa_tool,
        xstart,
        ystart,
        xfinish,
        yfinish,
        supplied_mask=[],
        supplied_mask__bool=False,
    ):
        import cv2
        self.reduced_by = aa_tool.detail_value

        """"
        now i need a new image with the above dimentions, and paste
        
        """
        self.xstart_reduced = xstart // self.reduced_by
        self.ystart_reduced = ystart // self.reduced_by
        self.xfinish_reduced = xfinish // self.reduced_by
        self.yfinish_reduced = yfinish // self.reduced_by

        # place bnounds in correct position
        self.x1 = min(self.xstart_reduced, self.xfinish_reduced)
        self.x2 = max(self.xstart_reduced, self.xfinish_reduced)
        self.y1 = min(self.ystart_reduced, self.yfinish_reduced)
        self.y2 = max(self.ystart_reduced, self.yfinish_reduced)

        # If bounds are out of frame, correct
        if self.x1 < 0:
            self.x1 = 0
        if self.x2 > threshed_image.shape[0]:
            self.x2 = threshed_image.shape[0]
        if self.y1 < 0:
            self.y1 = 0
        if self.y2 < threshed_image.shape[1]:
            self.y2 = threshed_image.shape[1]

        mask = np.zeros(self.resized_image.shape[:2], np.uint8)
        mask[self.x1 : self.x2, self.y1 : self.y2] = cv2.GC_PR_FGD
        if supplied_mask__bool == False:
            pass

        else:
            supplied_mask_resized = self.resize_down(supplied_mask)
            mask[supplied_mask_resized == cv2.GC_FGD] = cv2.GC_FGD
            mask[supplied_mask_resized == cv2.GC_BGD] = (
                cv2.GC_BGD
            )  # supplied_mask_resized

        # cv2.imshow("not thinned",mask*70)
        # cv2.waitKey(0)
        # mask[:,:] = 0
        # mask[self.x1:self.x2,self.y1:self.y2] = tmp_mask_1[self.x1:self.x2,self.y1:self.y2]
        # perform parthial thinning:

        bgdModel = np.zeros((1, 65), np.float64)
        fgdModel = np.zeros((1, 65), np.float64)
        rect = (self.x1, self.y1, self.y2 - self.y1, self.x2 - self.x1)
        iteration = 2

        # self.resized_image = skimage.exposure.equalize_adapthist(img)*255

        self.resized_image = self.resized_image.astype(np.uint8)

        mean_val = 100  # np.mean(self.resized_image[np.where(mask==cv2.GC_PR_FGD)])

        import skimage
        import scipy

        logger.info("ok before")
        final_mask, bgdModel, fgdModel = cv2.grabCut(
            self.resized_image,
            mask.copy(),
            None,
            bgdModel,
            fgdModel,
            iteration,
            cv2.GC_INIT_WITH_MASK,
        )
        logger.info("ok after")

        final_mask = np.where((final_mask == 2) | (final_mask == 0), 0, 1).astype(
            "uint8"
        )
        final_mask = self.get_largerst_area(final_mask)
        try:
            self.TmpMiniMask = scipy.ndimage.morphology.binary_fill_holes(
                final_mask
            ).astype(
                int
            )  # TmpMIni mask so that we can grab it to the label
        except Exception as e:
            logger.info(e)
        final_mask = resize(
            self.TmpMiniMask.copy() * 255,
            (self.shape_0_original, self.shape_1_original),
        )

        return final_mask

    def grab_cut(
        self,
        threshed_image,
        aa_tool,
        xstart,
        ystart,
        xfinish,
        yfinish,
        supplied_mask=[],
        supplied_mask__bool=False,
    ):
        """
        TODO: we need to select only the ROI and feed it to the
        the close and fill image operator so that only the worm
        of interest is fild, then we need to add the ROI and the
        whole image added together
        """
        self.reduced_by = aa_tool.detail_value
        from skimage.morphology import binary_closing, disk
        from skimage.transform import rescale, resize, downscale_local_mean
        import scipy.ndimage as nd
        import cv2
        from skimage.morphology import medial_axis, skeletonize, thin

        # self.reduced_by =2
        self.xstart_reduced = xstart // self.reduced_by
        self.ystart_reduced = ystart // self.reduced_by
        self.xfinish_reduced = xfinish // self.reduced_by
        self.yfinish_reduced = yfinish // self.reduced_by

        # mask = self.input_mask

        """"
        now i need a new image with the above dimentions, and paste
        
        """
        if xstart > xfinish and yfinish > ystart:
            self.x1 = self.ystart_reduced
            self.x2 = self.yfinish_reduced
            self.y1 = self.xfinish_reduced
            self.y2 = self.xstart_reduced
        elif xstart > xfinish and yfinish < ystart:
            self.x1 = self.yfinish_reduced
            self.x2 = self.ystart_reduced
            self.y1 = self.xfinish_reduced
            self.y2 = self.xstart_reduced
        elif xstart < xfinish and yfinish > ystart:
            self.x1 = self.ystart_reduced
            self.x2 = self.yfinish_reduced
            self.y1 = self.xstart_reduced
            self.y2 = self.xfinish_reduced
        elif xstart < xfinish and yfinish < ystart:
            self.x1 = self.yfinish_reduced
            self.x2 = self.ystart_reduced
            self.y1 = self.xstart_reduced
            self.y2 = self.xfinish_reduced
        else:
            return []

        ROI_mask = threshed_image[self.x1 : self.x2, self.y1 : self.y2].copy()

        # Close and fill image operator:
        strel = disk(4)
        I_closed = binary_closing(ROI_mask, strel)
        I_closed_filled = nd.morphology.binary_fill_holes(I_closed)

        # cv2.imshow("filed holes",I_closed_filled.astype(np.uint8)*255)
        # cv2.waitKey(0)

        # try cv2 grab cut here:
        threshed_image_ROI = np.zeros(self.resized_image.shape[:2], np.uint8)
        threshed_image_ROI[self.x1 : self.x2, self.y1 : self.y2] = (
            I_closed_filled.astype(np.uint8) * 255
        )
        mask = np.zeros(self.resized_image.shape[:2], np.uint8)
        logger.info(I_closed_filled.shape)
        logger.info(mask.shape)
        # PR_BG:
        mask[self.x1 : self.x2, self.y1 : self.y2] = cv2.GC_PR_BGD
        threshed_image_ROI = threshed_image_ROI.astype(np.uint8) * 255
        # kernel = np.ones((3,3),np.uint8)
        # threshed_image_ROI_core = thin(threshed_image_ROI, max_iter=40) # the scaleton of FG
        # threshed_image_ROI_core = cv2.dilate(threshed_image_ROI_core.astype(np.uint8),kernel,iterations = 1)
        # PR_FG:
        if supplied_mask__bool == False:
            mask[threshed_image_ROI >= 1] = cv2.GC_PR_FGD
            # mask[threshed_image_ROI_core>= 1 ]= cv2.GC_FGD
        else:
            # it needs to be resized down since the other are also resized down
            # cv2.imshow("not thinned",supplied_mask*70)
            # cv2.waitKey(0)
            # TODO: needs fix also fix to bae able to go out of bounds without closing
            mask[threshed_image_ROI >= 1] = cv2.GC_PR_FGD
            # mask[threshed_image_ROI_core>= 1 ]= cv2.GC_FGD
            supplied_mask_resized = self.resize_down(supplied_mask)

            mask[supplied_mask_resized == cv2.GC_FGD] = cv2.GC_FGD
            mask[supplied_mask_resized == cv2.GC_BGD] = (
                cv2.GC_BGD
            )  # supplied_mask_resized

        # cv2.imshow("not thinned",mask*70)
        # cv2.waitKey(0)
        # mask[:,:] = 0
        # mask[self.x1:self.x2,self.y1:self.y2] = tmp_mask_1[self.x1:self.x2,self.y1:self.y2]
        # perform parthial thinning:

        bgdModel = np.zeros((1, 65), np.float64)
        fgdModel = np.zeros((1, 65), np.float64)
        rect = (self.x1, self.y1, self.y2 - self.y1, self.x2 - self.x1)
        iteration = 1

        # self.resized_image = skimage.exposure.equalize_adapthist(img)*255

        self.resized_image = self.resized_image.astype(np.uint8)

        mean_val = 100  # np.mean(self.resized_image[np.where(mask==cv2.GC_PR_FGD)])
        logger.info("mean is ", mean_val)
        import skimage
        import scipy

        final_mask, bgdModel, fgdModel = cv2.grabCut(
            self.resized_image,
            mask.copy(),
            rect,
            bgdModel,
            fgdModel,
            iteration,
            cv2.GC_INIT_WITH_MASK,
        )
        # except:
        #     logger.info("grab cut is not running")

        final_mask = np.where((final_mask == 2) | (final_mask == 0), 0, 1).astype(
            "uint8"
        )
        final_mask = self.get_largerst_area(final_mask)
        try:
            self.TmpMiniMask = scipy.ndimage.morphology.binary_fill_holes(
                final_mask
            ).astype(
                int
            )  # TmpMIni mask so that we can grab it to the label
        except Exception as e:
            logger.info(e)
        final_mask = resize(
            self.TmpMiniMask.copy() * 255,
            (self.shape_0_original, self.shape_1_original),
        )

        return final_mask

    def get_largerst_area(self, input_mask):
        import skimage
        from skimage import measure

        labels_mask = measure.label(input_mask)
        regions = measure.regionprops(labels_mask)
        regions.sort(key=lambda x: x.area, reverse=True)
        if len(regions) > 1:
            for rg in regions[1:]:
                labels_mask[rg.coords[:, 0], rg.coords[:, 1]] = 0
        labels_mask[labels_mask != 0] = 1
        return labels_mask

    @staticmethod
    def convertPoints2BndBox(points):
        xmin = float("inf")
        ymin = float("inf")
        xmax = float("-inf")
        ymax = float("-inf")
        for p in points:
            x = p[0]
            y = p[1]
            xmin = min(x, xmin)
            ymin = min(y, ymin)
            xmax = max(x, xmax)
            ymax = max(y, ymax)

        # Martin Kersner, 2015/11/12
        # 0-valued coordinates of BB caused an error while
        # training faster-rcnn object detector.
        if xmin < 1:
            xmin = 1

        if ymin < 1:
            ymin = 1

        return (int(xmin), int(ymin), int(xmax), int(ymax))

    @staticmethod
    def resultSave(save_path, image_np):
        import cv2
        cv2.imwrite(save_path, image_np)

    @staticmethod
    def bbox2(img):
        """
        A function that returns the boudning box of the bool mask input
        """
        rows = np.any(img, axis=1)
        cols = np.any(img, axis=0)
        xmin, xmax = np.where(rows)[0][[0, -1]]
        ymin, ymax = np.where(cols)[0][[0, -1]]

        return xmin, xmax, ymin, ymax

    def get_largest_cc(self, binary):
        import scipy.ndimage.measurements as measure

        """ Get the largest connected component in the foreground. """
        cc, n_cc = measure.label(binary)
        max_n = -1
        max_area = 0
        for n in range(1, n_cc + 1):
            area = np.sum(cc == n)
            if area > max_area:
                max_area = area
                max_n = n
        largest_cc = cc == max_n
        return largest_cc



def findPeaksOptimizer(image, mask, min_distance=6, num_peaks=5):
    from skimage.feature import peak_local_max
    import scipy
    COMPLETE = False
    xy = peak_local_max(
        image, min_distance=min_distance, num_peaks=num_peaks, labels=mask
    )  # , indices=False)#,labels = mask)
    if len(xy) == 0:
        return []
    xy = xy.tolist()
    popZERO = False
    while COMPLETE == False:
        limitSizeCloseness = 7
        logger.info(xy)
        allDistMat = scipy.spatial.distance.cdist(
            np.asarray(xy), np.asarray(xy), "euclidean"
        ).astype(np.uint32)
        allDist = np.unique(allDistMat.copy().ravel()).astype(np.uint32)
        logger.info(allDist)
        logger.info(xy)
        if all(allDist) > limitSizeCloseness or popZERO == True:
            COMPLETE = True
            continue
        # only keep small numbers to delete
        allDist = [x for x in allDist if x < limitSizeCloseness]
        # logger.info("all dist is ", allDist)
        import time

        # time.sleep(0.5)
        for i in range(len(allDist)):
            occMat = np.where(allDistMat == allDist[i])
            logger.info(allDistMat)
            logger.info("occMat is ", occMat)
            toSkip = False
            for x in range(len(occMat[0])):
                logger.info("i is ", i)
                logger.info("x is ", x)
                if toSkip == True:
                    logger.info("continuing")
                    continue
                if occMat[0][x] == occMat[1][x]:
                    logger.info("continueing2")
                    continue
                xy.pop(occMat[0][x])
                toSkip = True
            if toSkip == False:
                popZERO = True
        # logger.info(allDistMat)
        logger.info("final xy is", xy)
    return xy


def cropImageToProportions(image, xmin, xmax, ymin, ymax):
    import cv2
    if len(image.shape) == 3:
        image = image[ymin:ymax, xmin:xmax, :]
        return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    elif len(image.shape) == 2:
        return image[ymin:ymax, xmin:xmax]


def GetPointsFromQPolygonF(polygonF):
    """
    Generates an (N,2) shaped array from a QPolygonF where N is the number of polygons
    """
    import numpy as np

    Startinglist = []
    xList = []
    yList = []
    boundingBox = [0, 0, 0, 0]
    for Point in polygonF:
        Startinglist.append([Point.y(), Point.x()])
        xList.append(Point.x())
        yList.append(Point.y())
    boundingBox[0] = int(np.min(xList))
    boundingBox[1] = int(np.max(xList))
    boundingBox[2] = int(np.min(yList))
    boundingBox[3] = int(np.max(yList))
    logger.info(boundingBox)
    return np.asarray(Startinglist), boundingBox


def CellsSplitterSearch(image, maskPOL, seedNum=4):
    import skimage
    import cv2
    maskPOL, boundingBox = np.asarray(GetPointsFromQPolygonF(maskPOL))
    resultF = np.zeros((image.shape[0], image.shape[1]), dtype=np.uint8)

    mask = skimage.draw.polygon2mask(
        (image.shape[0], image.shape[1]), np.asarray(maskPOL, dtype=np.uint16)
    )
    image = cropImageToProportions(
        image, boundingBox[0], boundingBox[1], boundingBox[2], boundingBox[3]
    )
    mask = cropImageToProportions(
        mask, boundingBox[0], boundingBox[1], boundingBox[2], boundingBox[3]
    ).astype(np.uint8)
    image = 255 - image
    # substract background
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (25, 25))
    image = cv2.morphologyEx(image, cv2.MORPH_TOPHAT, kernel)
    # init Vars
    min_distance = 4
    num_peaks = seedNum
    xy = []
    min_distanceD = min_distance
    num_peaksD = num_peaks
    while not len(xy) == seedNum:
        xy = findPeaksOptimizer(
            image, mask, min_distance=min_distanceD, num_peaks=num_peaksD
        )
        if len(xy) == 0:
            min_distanceD = 2
            num_peaksD = seedNum
        if min_distanceD == 1:
            min_distanceD += 20
        if num_peaksD == seedNum * 3:
            num_peaksD = seedNum
        if len(xy) < seedNum:
            min_distanceD = min_distanceD - 1
            num_peaksD = num_peaksD + 1
        if len(xy) > seedNum:
            min_distanceD = min_distanceD + 1
            if seedNum <= num_peaksD:
                num_peaksD = num_peaksD - 1

    finalMask = np.zeros(mask.shape, dtype=np.uint8)

    label = 0
    imageCanvas = image.copy()
    for values in xy:
        label += 1
        rr, cc = circle(values[0], values[1], 3)
        imageCanvas[rr, cc] = 255
        finalMask[values[0], values[1]] = label

    # cv2.imshow("tmpWindow",image)
    # cv2.waitKey()
    from scipy import ndimage as ndi

    distance = ndi.distance_transform_edt(imageCanvas)
    from skimage.segmentation import watershed, random_walker

    xy = ndi.label(np.asarray(xy))

    result = random_walker(image, finalMask)
    result = (result).astype(np.uint8)

    mask = cv2.bitwise_not(mask * 255).astype(bool)

    result[mask] = 0

    listAllMasks = []
    for i in range(seedNum):
        resultFtmp = resultF.copy()
        tmpImage = np.zeros(mask.shape, dtype=np.uint8)
        tmpImage[result == i + 1] = 255
        resultFtmp[boundingBox[2] : boundingBox[3], boundingBox[0] : boundingBox[1]] = (
            tmpImage
        )

        contours = skimage.measure.find_contours(resultFtmp, 0.8)
        for x in range(len(contours)):
            appr_hand = skimage.measure.approximate_polygon(
                np.asarray(contours[x]), tolerance=1.2
            ).astype(np.uint16)
            listAllMasks.append(
                QtGui.QPolygonF([QtCore.QPointF(p[1], p[0]) for p in appr_hand])
            )

    return listAllMasks


def watershedWithSeeds(maskOrig, maskSeeds):
    from scipy import ndimage as ndi
    from skimage.segmentation import watershed
    from skimage.feature import peak_local_max

    # Now we want to separate the two objects in image
    # Generate the markers as local maxima of the distance to the background
    distance = ndi.distance_transform_edt(maskOrig)

    coords = peak_local_max(distance, footprint=np.ones((3, 3)), labels=maskSeeds)
    mask = np.zeros(distance.shape, dtype=bool)
    mask[tuple(coords.T)] = True
    markers, _ = ndi.label(mask)
    labels = watershed(-distance, markers, mask=maskOrig).astype(np.uint8)
    return labels


def CellsSplitter(image, maskPOL, seeds=[]):
    import skimage
    import cv2
    maskPOL, boundingBox = np.asarray(GetPointsFromQPolygonF(maskPOL))
    resultF = np.zeros((image.shape[0], image.shape[1]), dtype=np.uint8)

    mask = skimage.draw.polygon2mask(
        (image.shape[0], image.shape[1]), np.asarray(maskPOL, dtype=np.uint16)
    )

    image = cropImageToProportions(
        image, boundingBox[0], boundingBox[1], boundingBox[2], boundingBox[3]
    )
    mask = cropImageToProportions(
        mask, boundingBox[0], boundingBox[1], boundingBox[2], boundingBox[3]
    ).astype(np.uint8)
    logger.info("seeds prior", seeds)
    logger.info("bounign box ", boundingBox)
    for i in range(len(seeds)):
        seeds[i] = [seeds[i][0] - boundingBox[0], seeds[i][1] - boundingBox[2]]
    logger.info("seeds afetr ", seeds)
    image = 255 - image
    # substract background
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (25, 25))
    image = cv2.morphologyEx(image, cv2.MORPH_TOPHAT, kernel)
    min_distance = 4
    min_distanceD = min_distance
    finalMask = np.zeros(mask.shape, dtype=np.uint8)
    label = 0
    imageCanvas = image.copy()
    for values in seeds:
        label += 1
        rr, cc = circle(int(values[1]), int(values[0]), 3)
        imageCanvas[rr, cc] = 255
        finalMask[int(values[1]), int(values[0])] = label
    # distance = ndi.distance_transform_edt(imageCanvas)
    # xy = ndi.label(np.asarray(xy))

    result = watershedWithSeeds(image, finalMask)
    result = (result).astype(np.uint8)

    mask = cv2.bitwise_not(mask * 255).astype(bool)

    result[mask] = 0

    listAllMasks = []
    for i in range(len(seeds)):
        resultFtmp = resultF.copy()
        tmpImage = np.zeros(mask.shape, dtype=np.uint8)
        tmpImage[result == i + 1] = 255
        resultFtmp[boundingBox[2] : boundingBox[3], boundingBox[0] : boundingBox[1]] = (
            tmpImage
        )

        contours = skimage.measure.find_contours(resultFtmp, 0.8)
        for x in range(len(contours)):
            appr_hand = skimage.measure.approximate_polygon(
                np.asarray(contours[x]), tolerance=1.2
            ).astype(np.uint16)
            listAllMasks.append(
                QtGui.QPolygonF([QtCore.QPointF(p[1], p[0]) for p in appr_hand])
            )

    return listAllMasks


if __name__ == "__main__":
    pass
