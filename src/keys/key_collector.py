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
        # time.sleep(0.1)
        """Handles key press events by adding the key or its name to the queue if collecting is enabled."""
        if self.collecting:
            try:
                self.key_queue.put(key.char)
            except AttributeError:
                self.key_queue.put(key.name)


    def start_listening(self):
        """Enables key collection."""
        self.collecting = True

    def stop_listening(self):
        """Disables key collection."""
        self.collecting = False

    def get_queue(self):
        """Returns the queue of pressed keys."""
        return self.key_queue

    def stop(self):
        """Stops the listener permanently."""
        self.listener.stop()
