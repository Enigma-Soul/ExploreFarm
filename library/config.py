from json import loads,dumps
from os.path import exists

class Config:
    def __init__(self,config_path = "./config.json"):
        self.config_path = config_path
        self.config = self.load()
    def load(self):
        if exists(self.config_path):
            with open(self.config_path,'r',encoding='utf-8') as f:
                return loads(f.read())
        else:
            print(exists(self.config_path))
            print(self.config_path)
            self.config = {}
            self.save()
            return {}
    def save(self):
        with open(self.config_path,'w',encoding='utf-8') as f:
            f.write(dumps(self.config,ensure_ascii=False,indent=4))
            f.close()
        return None


def is_json(str):
    try:
        loads(str)
        return True
    except Exception as e:
        return False