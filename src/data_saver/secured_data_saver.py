
import threading

from src.data_saver.data_saver import DataSaver


class SecuredDataSaver(DataSaver):

    def __init__(self):
        super().__init__()
        self.event = threading.Event()
        self.event.set()
        self.lock = threading.Lock()

    def get_value(self, key):
        self.event.wait()
        return super().get_value(key)

    def get_keys(self):
        self.event.wait()
        return super().get_keys()

    def set_value(self, key, value):
        self.lock.acquire()
        self.event.clear()
        super().set_value(key, value)
        self.lock.release()
        self.event.set()

    def remove(self, key):
        self.lock.acquire()
        self.event.clear()
        super().remove(key)
        self.lock.release()
        self.event.set()

