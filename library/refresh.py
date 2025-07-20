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

            if cnt %100 == 0:
                print(f"[!] Refresh 进程已经重启了 {cnt} 次")
                print(f"[!] 正在重新启动")


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
            flag = False
            self.config.load()
            for i in self.config["farmland"]: # 糖
                if not check(i,"farmland"):
                    continue
                flag = True
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
                    continue
                flag = True
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
            if not flag:
                sleep(1)
                raise TypeError("没有检测到农田 正在重新启动")
            if need_break:
                break
            sleep(1)