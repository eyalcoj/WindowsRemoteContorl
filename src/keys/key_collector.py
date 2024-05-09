from pynput.keyboard import Listener, KeyCode
import queue


class KeyCollector:
    shared_listener = None
    listeners_queue = []

    def __init__(self):
        self.is_start = False
        self.key_queue = queue.Queue()
        if KeyCollector.shared_listener is None:
            KeyCollector.shared_listener = Listener(on_press=self._on_press_shared)
            KeyCollector.shared_listener.start()

    def _on_press_shared(self, key):
        try:
            key_value = key.char
        except AttributeError:
            key_value = key.name

        for q in list(KeyCollector.listeners_queue):
            q.put(key_value)

    def start_listening(self):
        if self.key_queue not in KeyCollector.listeners_queue:
            KeyCollector.listeners_queue.append(self.key_queue)

    def stop_listening(self):
        if self.key_queue in KeyCollector.listeners_queue:
            KeyCollector.listeners_queue.remove(self.key_queue)

    def get_queue(self):
        return self.key_queue

    @staticmethod
    def stop_all():
        if KeyCollector.shared_listener is not None:
            KeyCollector.shared_listener.stop()
            KeyCollector.shared_listener.join()
            KeyCollector.shared_listener = None
        KeyCollector.listeners_queue.clear()
