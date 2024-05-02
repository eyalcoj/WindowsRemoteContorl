
import threading

from src.data_saver.data_saver import DataSaver


class SecuredDataSaver(DataSaver):

    def __init__(self):
        super().__init__()
        self.lock = threading.Lock()

    def get_value(self, key):
        with self.lock:  # Ensure that the lock is always released
            return super().get_value(key)

    def get_keys(self):
        with self.lock:
            return super().get_keys()

    def set_value(self, key, value):
        with self.lock:
            super().set_value(key, value)

    def remove(self, key):
        with self.lock:
            super().remove(key)

