from hashlib import md5


class UID:
    def __init__(self):
        self.cnt = 0
        self.data = {}

    def __get_hash(self,num):
        _hash = "None"
        first = True
        while _hash in list(self.data.keys()) or first:
            first = False
            self.cnt += 1
            _hash = md5(num.to_bytes(8, byteorder='big', signed=False)).hexdigest()
        return _hash

    def load(self, data):
        __doc__: dict
        self.data = data
        if "cnt" in list(self.data.keys()):
            self.cnt = data["cnt"]
            self.data.pop("cnt")
        else:
            self.cnt = len(data)
        return self
    def save(self):
        return self.data

    def push(self,data):
        _hash = self.__get_hash(self.cnt)
        self.data[_hash] = data
        return _hash
    def pop(self,_hash):
        self.data.pop(_hash)
        return self
    def get(self,_hash):
        return self.data[_hash]
    def clean(self):
        self.data = {}
        self.cnt = 0
        return self
    def get_data(self):
        return self.data
    def get_hash_list(self):
        return list(self.data.keys())
    def update(self,key,data):
        self.data[key] = data
        self.save()
        return self
    def check(self,_hash):
        return _hash in list(self.data.keys())