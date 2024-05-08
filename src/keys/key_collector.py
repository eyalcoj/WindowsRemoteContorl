import time
from queue import Queue
from pynput.keyboard import Listener


class KeyCollector:
    def __init__(self):
        self.key_queue = Queue()
        self.listener = Listener(on_press=self.on_press)
        self.collecting = False
        self.listener.start()

    def on_press(self, key):
        """this method is collecting the presses of the user"""
        if self.collecting:
            try:
                self.key_queue.put(key.char)
            except AttributeError:
                self.key_queue.put(key.name)

    def start_listening(self):
        self.collecting = True

    def stop_listening(self):
        self.collecting = False

    def get_queue(self):
        return self.key_queue

    def stop(self):
        self.listener.stop()
