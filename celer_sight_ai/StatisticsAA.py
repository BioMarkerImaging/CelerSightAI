from PyQt6 import QtCore, QtGui, QtWidgets

import logging

logger = logging.getLogger(__name__)


class StatisticalAnalysisClass(QtWidgets.QWidget):
    ToTextEditSignal = QtCore.pyqtSignal(object)

    def __init__(self, dataframe=None):
        super(StatisticalAnalysisClass, self).__init__()
        self.dataframe = dataframe
        self.NDcheck = "kolmogorov"  # or it could be shapiro
        self.KTestPValues = {}
        self.alpha = 0.01
        self.ComparisonsCheck = []  # a list of already done comparisons
        self.KTestBothBool = (
            True  # both of the Conditons need to be normal distribution to do 2 kstest
        )
        self.significansPairs = []

    def tTestProcess(self):
        import numpy as np
        import pandas as pd
        import scipy

        raise NotImplementedError("t-Test not implemented yet")
        AddedValue = 1  # The value that makes sure we get all combinations
        # return

        # Get all the unique values and put them in a list to comapie

        self.ComparisonsCheck = self.dataframe["condition"].unique().tolist()

        # logger.info("startingg to test for normality")
        self.NDcheck = "kolmogorov"
        if self.NDcheck == "kolmogorov":
            # self.ToTextEditSignal.emit("Checking normal Distribution:\n")

            df1 = self.dataframe.set_index("condition", drop=False)
            df2 = df1.copy()

            # Compute all k test values to determine if we are moving forward

            # self.KolmogorovSmirnov1S(df1)

            for x in range(len(self.ComparisonsCheck)):
                if len(self.ComparisonsCheck) - AddedValue == 0:
                    continue
                for y in range(len(self.ComparisonsCheck) - AddedValue):
                    index1 = self.ComparisonsCheck[x]
                    index2 = self.ComparisonsCheck[y + AddedValue]
                    # if self.KTestBothBool == True:
                    #     logger.info(index1)
                    #     logger.info(index2)
                    #     if self.KTestPValues.get(index1)> self.alpha or self.KTestPValues.get(index2)>self.alpha:
                    #         pass #TODO: needs to be continue if we testing
                    Ar1 = np.asarray(df1.loc[index1, "values"])
                    Ar2 = np.asarray(df2.loc[index2, "values"])

                    StrToEmit = str(str(index1) + " against " + str(index2) + ".\n")
                    self.ToTextEditSignal.emit(StrToEmit)
                    try:
                        self.KolmogorovSmirnov2S(Ar1, Ar2)
                    except:
                        pass
                    a, pttest = scipy.stats.ttest_ind(Ar1, Ar2, equal_var=False)
                    StrToEmit = str(
                        index1 + " against " + index2 + " => " + str(pttest)
                    )
                    if pttest <= 0.05:
                        self.significansPairs.append((index1, index2))
                    self.ToTextEditSignal.emit(StrToEmit)

                AddedValue += 1
            if self.KTestBothBool == True:
                self.ToTextEditSignal.emit(
                    "\nComparisons with low ktest pvalues may have been filted out"
                )

    def KolmogorovSmirnov1S(self, df1):
        # normality test for all samples
        return
        # import numpy as np
        # from scipy import stats
        # for name in self.ComparisonsCheck:
        #     Ar1 = np.asarray(df1.loc[name,'values']).astype(np.uint32)
        #     logger.info(Ar1)
        #     p = self.kstest_wrapper(Ar1)
        #     # D, p = stats.kstest(Ar1, 'norm')
        #     logger.info("p is ", p )
        #     # logger.info("d os ,",D)
        #     self.KTestPValues[name]= p
        #     StrToEmit = str('The ks-test p value for '+ str(name)+' is '+ str(p))
        #     self.ToTextEditSignal.emit(StrToEmit)

    def kstest_wrapper(
        self,
        data,
        dist="norm",
        ignoreNaN=True,
        args=None,
        N=20,
        alternative="two-sided",
        mode="approx",
    ):
        import numpy as np
        from scipy import stats
        from scipy.stats import norm

        """ Kolmogorov-Smirnov Test, """
        if ignoreNaN:
            nonans = np.invert(np.isnan(data))  # test for NaN's
            if np.sum(nonans) < 3:
                return np.NaN  # return, if less than 3 non-NaN's
            data = data[nonans]  # remove NaN's
        if args is None:
            args = ()

        logger.info("transformed date is , ", np.expand_dims(data, axis=1))
        xaxis = np.arange(len(data + 1)).astype(
            np.uint32
        )  # createan array for x axis of the histogram
        finaldata = np.concatenate(
            (np.expand_dims(np.sort(data), axis=1), np.expand_dims(xaxis, axis=1)),
            axis=1,
        )
        logger.info("final data is", finaldata)
        data = np.hstack([np.repeat(x, int(f)) for x, f in finaldata])

        loc, scale = norm.fit(data)
        # create a normal distribution with loc and scale
        n = norm(loc=loc, scale=scale)
        D, pval = stats.kstest(
            data, n.cdf, args=args, N=N, alternative=alternative, mode=mode
        )
        del D
        return pval

    def KolmogorovSmirnov2S(self, Ar1, Ar2):
        # normality test for 2 samples
        from scipy import stats

        logger.info("first array is ", Ar1)
        logger.info("second array is", Ar2)
        stat, p = stats.ks_2samp(Ar1, Ar2)
        # interpret
        if p > self.alpha:
            StrToEmit = str(
                "p is : " + str(p) + ".\nSample looks Gaussian (fail to reject H0)"
            )
            logger.info("Sample looks Gaussian (fail to reject H0)")
            # self.ToTextEditSignal.emit(StrToEmit)
        else:
            StrToEmit = str(
                "p is : " + str(p) + ".\nSample does not look Gaussian (reject H0)"
            )
            logger.info("Sample does not look Gaussian (reject H0)")
            # self.ToTextEditSignal.emit(StrToEmit)
