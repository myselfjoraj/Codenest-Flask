class HashMap:
    def __init__(self):
        self.map = {}

    def put(self, key, value1, value2, value3):
        self.map[key] = (value1, value2, value3)

    def get(self, key):
        return self.map.get(key)

    def remove(self, key):
        if key in self.map:
            del self.map[key]

    def contains_key(self, key):
        return self.get(key) is not None

    def size(self):
        return len(self.map)
