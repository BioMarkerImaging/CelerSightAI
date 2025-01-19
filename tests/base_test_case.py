import threading
import time
import unittest

from celer_sight_ai.config import start_jvm, stop_jvm


class BaseTestCase(unittest.TestCase):
    _jvm_lock = threading.Lock()
    _jvm_started = False

    @classmethod
    def setUpClass(cls):
        """Set up class-level test fixtures."""
        print("Starting JVM initialization...")
        if not cls._jvm_started:
            max_retries = 3
            for attempt in range(max_retries):
                try:
                    start_jvm()
                    cls._jvm_started = True
                    print("JVM initialization successful")
                    break
                except Exception as e:
                    print(f"JVM initialization attempt {attempt + 1} failed: {e}")
                    if attempt == max_retries - 1:
                        raise
                    time.sleep(1)  # Wait before retrying
        super().setUpClass()

    @classmethod
    def tearDownClass(cls):
        try:
            if cls._jvm_started:
                stop_jvm()
                cls._jvm_started = False
        finally:
            super().tearDownClass()
