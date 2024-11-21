from PyQt6 import QtCore, QtGui, QtWidgets
import traceback

import logging

logger = logging.getLogger(__name__)


class WorkerSignals(QtCore.QObject):
    finished = QtCore.pyqtSignal(str)
    error = QtCore.pyqtSignal(tuple)
    result = QtCore.pyqtSignal(object)  # can be anything
    progress = QtCore.pyqtSignal(int)


# drop
class Worker(QtCore.QRunnable):
    """
    Worker thread

    """

    mysignals = WorkerSignals()

    def __init__(self, fn, *args, **kwargs):
        super(Worker, self).__init__()
        logger.info(f"Worker started with function: {fn}")
        logger.info("worker args are ".format(*args))
        logger.info("kwarfs are ".format(**kwargs))

        # Store constructor arguments (re-used for processing)
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.signals = WorkerSignals()

        # Add the callback to our kwargs
        self.kwargs["progress_callback"] = self.signals.progress

    @QtCore.pyqtSlot()
    def run(self):
        """
        our runner functionos that returns the resulted values.
        """
        gotError = False
        # Retrieve args/kwargs here; and fire processing using them
        try:
            result = self.fn(*self.args, **self.kwargs)
        except Exception as e:
            gotError = True
            logger.error("exception durign threaded app")
            logger.error(e)
            logger.error(f"Funciton name: {self.fn}")
            import sys

            traceback.print_exc()
            exctype, value = sys.exc_info()[:2]
            self.signals.error.emit((exctype, value, traceback.format_exc()))
        else:
            self.signals.result.emit(result)  # Return the result of the processing
        # finally:
        #     self.signals.finished.emit("An error occured")  # Done
        return


class workerInference(QtCore.QRunnable):
    """
    Worker thread for inferencing only
    Needs to be a separate function to handle errors correctly

    """

    mysignals = WorkerSignals()

    def __init__(self, fn, *args, **kwargs):
        super(workerInference, self).__init__()
        logger.info("worker args are ".format(*args))
        logger.info("kwarfs are ".format(**kwargs))
        print(args)
        print(kwargs)
        # Store constructor arguments (re-used for processing)
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.signals = WorkerSignals()

        # Add the callback to our kwargs
        self.kwargs["progress_callback"] = self.signals.progress

    @QtCore.pyqtSlot()
    def run(self):
        """
        our runner functionos that returns the resulted values.
        """
        gotError = "Inference complete."
        # Retrieve args/kwargs here; and fire processing using them
        try:
            result = self.fn(*self.args, **self.kwargs)
        except Exception as e:
            from celer_sight_ai import config

            gotError = "Error during inference."
            # emit that we got an error
            logger.error("exception durign threaded app")
            logger.error(e)
            logger.error(f"Funciton name: {self.fn}")
            import sys

            traceback.print_exc()
            exctype, value = sys.exc_info()[:2]
            self.signals.error.emit((exctype, value, traceback.format_exc()))
        else:
            self.signals.result.emit(result)  # Return the result of the processing
        finally:
            self.signals.finished.emit(gotError)  # Done
        return


class Worker_LogIn(QtCore.QRunnable):
    """
    Worker thread

    """

    mysignals = WorkerSignals()

    def __init__(self, fn, *args, **kwargs):
        super(Worker, self).__init__()

        # Store constructor arguments (re-used for processing)
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.signals = WorkerSignals()

        # Add the callback to our kwargs
        self.kwargs["progress_callback"] = self.signals.progress

    @QtCore.pyqtSlot()
    def run(self):
        """
        our runner functionos that returns the resulted values.
        """
        gotError = ""
        # Retrieve args/kwargs here; and fire processing using them
        try:
            result = self.fn(*self.args, **self.kwargs)
        except Exception as e:
            print(e)
            logger.error(e)
            gotError = "Error during login."

        else:
            self.signals.result.emit(result)  # Return the result of the processing
        finally:
            self.signals.finished.emit(gotError)  # Done
        return


class LoopThread(QtCore.QThread):
    def __init__(self, subreddits):
        QtCore.QThread.__init__(self)
        self.subreddits = subreddits

    def __del__(self):
        self.wait()

    def run(self):
        self.subreddits
