import threading
from celer_sight_ai import config

import time
from PyQt6 import QtCore
import logging
import traceback
import copy

logger = logging.getLogger(__name__)


class WorkerSignals(QtCore.QObject):
    finished = QtCore.pyqtSignal(str)
    error = QtCore.pyqtSignal(tuple)
    result = QtCore.pyqtSignal(object)  # can be anything
    progress = QtCore.pyqtSignal(int)


class Threader:
    active_threads = 0
    lock = threading.Lock()
    semaphore = threading.Semaphore(
        config.user_cfg["MAX_WORKERS"]
    )  # Add a semaphore with the desired max threads

    def __init__(self, target_function, args=(), kwargs={}, callback=None):
        self.target_function = target_function
        self.callback = callback
        self.args = args
        self.kwargs = kwargs
        if not config.user_cfg["USER_WORKERS"]:
            result = self.target_function(*self.args, **self.kwargs)
            if self.callback:
                self.callback(result)
            return
        self.thread = threading.Thread(target=self._run)
        with Threader.lock:
            Threader.active_threads += 1

    def _run(self):
        with Threader.semaphore:  # Acquire the semaphore
            result = self.target_function(*self.args, **self.kwargs)
        if self.callback:
            self.callback()
        with Threader.lock:
            Threader.active_threads -= 1

    def start(self):
        if not config.user_cfg["USER_WORKERS"]:
            return
        self.thread.start()

    def join(self):
        if not config.user_cfg["USER_WORKERS"]:
            return
        self.thread.join()


class ThreaderViewer:
    active_threads = 0
    lock = threading.Lock()

    def __init__(self, target_function, args=(), kwargs={}, callback=None):
        self.target_function = target_function
        self.callback = callback
        self.args = args
        self.kwargs = kwargs
        if not config.user_cfg["USER_WORKERS"]:
            result = self.target_function(*self.args, **self.kwargs)
            if self.callback:
                self.callback(result)
            return
        self.thread = threading.Thread(target=self._run)
        with ThreaderViewer.lock:
            ThreaderViewer.active_threads += 1

    def _run(self):
        result = self.target_function(*self.args, **self.kwargs)
        if self.callback:
            self.callback()

        with ThreaderViewer.lock:
            ThreaderViewer.active_threads -= 1

    def start(self):
        if not config.user_cfg["USER_WORKERS"]:
            return
        self.thread.start()

    def join(self):
        if not config.user_cfg["USER_WORKERS"]:
            return
        self.thread.join()


class workerInference:
    active_threads = 0
    lock = threading.Lock()
    # semaphore = threading.Semaphore(
    #     config.user_cfg["MAX_WORKERS"]
    # )  # Add a semaphore with the desired max threads

    def __init__(
        self, target_function, args=(), kwargs={}, callback=None, MainWindow=None
    ):
        self.MainWindow = MainWindow
        self.target_function = target_function
        self.callback = callback
        self.args = copy.copy(args)
        self.signals = WorkerSignals()
        self.kwargs = kwargs.copy()  # Important to create a copy of the kwargs dict
        self.stop_signal = threading.Event()
        # print(self.args)
        if not config.user_cfg["USER_WORKERS"]:
            result = self.target_function(*self.args, **self.kwargs)
            if self.callback:
                self.callback(result)
            return
        self.args = self.args + tuple([self.stop_signal])  # add stop signal to args
        self.thread = threading.Thread(target=self._run)
        # with workerInference.lock:
        #     workerInference.active_threads += 1

    def stop(self):
        self.stop_signal.set()

    def _run(self):
        # with Threader.semaphore:  # Acquire the semaphore
        # with workerInference.lock:
        from celer_sight_ai import config

        # workerInference.active_threads -= 1
        gotError = "Inference complete."
        # Retrieve args/kwargs here; and fire processing using them
        try:
            result = self.target_function(*self.args, **self.kwargs)
        except Exception as e:
            from celer_sight_ai import config

            gotError = "Error during inference."
            # make sure all animations stop
            for group_name in self.MainWindow.DH.BLobj.groups.keys():
                for Condition, value in self.MainWindow.DH.BLobj.groups[
                    group_name
                ].conds.items():
                    for x in range(
                        len(
                            self.MainWindow.DH.BLobj.groups[group_name]
                            .conds[Condition]
                            .images
                        )
                    ):
                        io = self.MainWindow.DH.BLobj.groups[group_name].conds[Condition].images[x]
                        config.global_signals.check_and_end_inference_animation_signal.emit(
                            {
                                "image_uuid" : io.unique_id
                            }
                        )
            # emit that we got an error
            logger.error("exception durign threaded app")
            logger.error(e)
            logger.error(f"Funciton name: {self.target_function}")
            import sys

            traceback.print_exc()
            exctype, value = sys.exc_info()[:2]
            self.signals.error.emit((exctype, value, traceback.format_exc()))
        else:
            if self.stop_signal.is_set():
                return
            self.signals.result.emit(result)  # Return the result of the processing
        finally:
            self.signals.finished.emit(gotError)  # Done
        return

    def start(self):
        if not config.user_cfg["USER_WORKERS"]:
            return
        self.thread.start()

    def join(self):
        if not config.user_cfg["USER_WORKERS"]:
            return
        self.thread.join()


class FunctionThread1(QtCore.QThread):
    function_finished = QtCore.pyqtSignal()

    def __init__(self, func, *args, **kwargs):
        super(FunctionThread1, self).__init__()
        self.func = func
        self.args = args
        self.kwargs = kwargs

    def run(self):
        self.func(*self.args, **self.kwargs)
        self.function_finished.emit()


class FunctionThread2(QtCore.QThread):
    function_finished = QtCore.pyqtSignal()

    def __init__(self, func, *args, **kwargs):
        super(FunctionThread2, self).__init__()
        self.func = func
        self.args = args
        self.kwargs = kwargs

    def run(self):
        self.func(*self.args, **self.kwargs)
        self.function_finished.emit()


class MultiThreader:
    active_threads = 0
    lock = threading.Lock()
    from celer_sight_ai import config

    # semaphore = threading.Semaphore(config.user_cfg["MAX_WORKERS"])

    def __init__(self, target_functions, objects, callback=None):
        self.threads = []
        # if config.user_cfg["USER_WORKERS"]:
        #     for target_function, obj in zip(target_functions, objects):
        #         result = target_function(obj)
        #         if callback:
        #             callback(result)
        #     return
        for target_function, obj in zip(target_functions, objects):
            thread = threading.Thread(
                target=self._run, args=(target_function, obj, callback)
            )
            self.threads.append(thread)
        #     with MultiThreader.lock:
        #         MultiThreader.active_threads += 1

    def _run(self, target_function, obj, callback):
        # with MultiThreader.semaphore:
        result = target_function(obj)
        if callback:
            callback(result)
        # with MultiThreader.lock:
        #     MultiThreader.active_threads -= 1

    def start(self):
        # if not config.user_cfg["USER_WORKERS"]:
        #     return
        for thread in self.threads:
            thread.start()

    def join(self):
        if not config.user_cfg["USER_WORKERS"]:
            return
        for thread in self.threads:
            thread.join()


class RacerThread:
    cancel_previous_func2_event = threading.Event()

    def __init__(
        self,
        func1,
        func2,
        func1_args=(),
        func1_kwargs={},
        func2_args=(),
        func2_kwargs={},
    ):
        self.func1 = func1
        self.func2 = func2
        self.func1_args = func1_args
        self.func1_kwargs = func1_kwargs
        self.func2_args = func2_args
        self.func2_kwargs = func2_kwargs
        self.func1_completed = False
        self.func2_completed = False
        self.t2 = None
        self.stop_event = threading.Event()

    def wrapper_func1(self):
        self.func1(*self.func1_args, **self.func1_kwargs)
        self.func1_completed = True

    def wrapper_func2(self):
        try:
            self.func2(*self.func2_args, **self.func2_kwargs)
        finally:
            self.func2_completed = True

    def cancel_previous_func2(self):
        RacerThread.cancel_previous_func2_event.set()
        RacerThread.cancel_previous_func2_event.clear()

    def run(self):
        self.cancel_previous_func2()

        t1 = threading.Thread(target=self.wrapper_func1)
        self.t2 = threading.Thread(target=self.wrapper_func2, daemon=True)

        t1.start()
        self.t2.start()

        while t1.is_alive() and self.t2.is_alive():
            if self.func2_completed or RacerThread.cancel_previous_func2_event.is_set():
                # Terminate func1
                return
            time.sleep(0.001)

        # Join both threads
        t1.join()
        if not RacerThread.cancel_previous_func2_event.is_set():
            self.t2.join()


if __name__ == "__main__":
    pass
