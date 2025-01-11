import unittest
import threading
from celer_sight_ai.config import start_jvm, stop_jvm


class BaseTestCase(unittest.TestCase):
    _jvm_lock = threading.Lock()
    _jvm_started = False

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        with cls._jvm_lock:
            if not cls._jvm_started:
                start_jvm()
                cls._jvm_started = True

    @classmethod
    def tearDownClass(cls):
        with cls._jvm_lock:
            if cls._jvm_started:
                stop_jvm()
                cls._jvm_started = False
        super().tearDownClass()
