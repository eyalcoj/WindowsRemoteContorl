from queue import Queue
from pynput.keyboard import Listener


class KeyCollector:
    def __init__(self):
        self.key_queue = Queue()
        self.listener = None

    def __create_listener(self):
        # Create a new listener instance
        print("befor1")
        # self.listener = Listener(on_press=self.on_press)
        self.listener = Listener()
        print("after1")

    def on_press(self, key):
        # Add the key pressed to the queue
        try:
            # Try to get the char attribute if it exists (for letter keys)
            self.key_queue.put(key.char)
        except AttributeError:
            # If it's a special key without a char attribute, use its name
            self.key_queue.put(key.name)

    def start_listening(self):
        if not self.listener or not self.listener.is_alive():
            self.__create_listener()
            self.listener.start()

    def stop_listening(self):
        if self.listener.is_alive():
            self.listener.stop()
            self.listener.join()

    def get_queue(self):
        return self.key_queue
