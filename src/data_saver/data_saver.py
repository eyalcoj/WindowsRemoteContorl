class DataSaver:
    def __init__(self):
        self.dict = dict()

    def set_value(self, key, value):
        self.dict.update({key: value})

    def get_value(self, key):
        value = self.dict.get(key)
        return value

    def get_keys(self):
        return list(self.dict.keys())

    def remove(self, key):
        if self.dict.get(key):
            self.dict.pop(key)
