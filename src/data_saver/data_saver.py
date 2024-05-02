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
            del self.dict[key]

    def __str__(self):
        text = ""
        text += "dict:"
        for key, value in self.dict.items():
            text += f"\n\tkey: {key}, value: {value}"
        return text

