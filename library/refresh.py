from threading import Thread
from time import sleep
from math import floor
from os.path import exists

class refresh:
    def __init__(self,lnk,config,tools):
        self.lnk = lnk
        self.config = config
        self.tools = tools

    def run(self):
        T = Thread(target=self.refresh_lunch)
        T.start()


    def refresh_lunch(self):
        cnt = 0
        while True:
            try:
                self.refresh()
            except Exception as e:
                cnt += 1
                print(f"Refresh 已报错 {e}")
                print(f"这是Refresh的第{cnt}次报错")
                print("1秒钟后进行重新启动")
                sleep(1)


    def format(self,percent):
        return str(round(percent * 100, 2))

    def refresh(self,need_break = False):
        def check(path,type):
            if not exists(path):
                return False
            try:
                data = self.tools.data(i)
                return self.tools.raw_type(data["type"]) == type
            except:
                return False
        while True:
            for i in self.config["farmland"]: # 糖
                if not check(i,"farmland"):
                    continue
                data = self.tools.data(i)
                if ":" in data["type"]:
                    crop = self.tools.seeds(data)
                else:
                    continue

                data["nbt"]["now"] += 1 / data["nbt"]["speed"]
                percent = data["nbt"]["now"] / data["nbt"]["total"]

                # 得到每个图片所需的百分比
                agree_percent = 1 / (self.config["seeds"][crop] - 1)

                
                if percent < 1:
                    p = floor(percent / agree_percent)
                    self.lnk.change(data["path"], icon=f"{crop}\\{p}.ico",
                                    description=f"一个种着已经熟了{self.format(percent)}%的{crop}的农田",argv=f"ef{self.tools.encode(data)}")

                else:
                    data["nbt"]["now"] = data["nbt"]["total"]
                    p = self.config["seeds"].get(crop) - 1
                    self.lnk.change(data["path"], icon=f"{crop}\\{p}.ico",
                                    description=f"一个种着熟透了的的{crop}的农田")
            for i in self.config["farmland_moist"]:  # 糖
                if not check(i,"farmland_moist"):
                    print(1)
                    continue
                data = self.tools.data(i)
                if ":" in data["type"]:
                    crop = self.tools.seeds(data)
                else:
                    continue

                data["nbt"]["now"] += 1 / data["nbt"]["speed"]
                percent = data["nbt"]["now"] / data["nbt"]["total"]

                # 得到每个图片所需的百分比
                agree_percent = 1 / (self.config["seeds"][crop] - 1)

                if percent < 1:
                    p = floor(percent / agree_percent)
                    self.lnk.change(data["path"], icon=f"{crop}\\_{p}.ico",
                                    description=f"一个种着已经熟了{self.format(percent)}%的{crop}的农田",argv=f"ef{self.tools.encode(data)}")

                else:
                    data["nbt"]["now"] = data["nbt"]["total"]
                    p = self.config["seeds"].get(crop) - 1
                    self.lnk.change(data["path"], icon=f"{crop}\\_{p}.ico",
                                    description=f"一个种着熟透了的的{crop}的农田")
            if need_break:
                break
            sleep(1)