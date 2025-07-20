from os import listdir, remove
from os.path import dirname, join, basename
from json import dumps

class open_with:
    def __init__(self, lnk, config, running_path,tools,refresh):
        self.lnk = lnk
        self.config = config
        self.running_path = running_path
        self.tools = tools
        self.refresh = refresh

    def __change_type(self, data, new_type, new_nbt):
        data["type"] = new_type
        data["nbt"].update(new_nbt)
        description = ""
        icon = join(self.running_path, "icons")
        if "hoe" == self.tools.raw_type(new_type):
            description = "一把锄头"
            icon = join(icon, "hoe.ico")
        elif "bucket" == self.tools.raw_type(new_type) and "water_bucket" not in new_type:
            description = "一个桶"
            icon = join(icon, "bucket.ico")
        elif "water_bucket" == self.tools.raw_type(new_type):
            description = "一个水桶"
            icon = join(icon, "water_bucket.ico")
        elif "farmland" == self.tools.raw_type(new_type):
            if ":" in new_type:
                description = f"一块{new_type.split(':')[1]}耕地"
                icon = join(icon, f"{new_type.split(':')[1]}\\0.ico")
            else:
                description = "一块耕地"
                icon = join(icon, "farmland.ico")
        elif "farmland_moist" == self.tools.raw_type(new_type):
            if ":" in new_type:
                description = f"湿润的{new_type.split(':')[1]}耕地"
                icon = join(icon, f"{new_type.split(':')[1]}\\_0.ico")
            else:
                description = "湿润耕地"
                icon = join(icon, "farmland_moist.ico")
        elif "land" == self.tools.raw_type(new_type):
            description = "一块土地"
            icon = join(icon, "dirt.ico")
        elif "water" == self.tools.raw_type(new_type):
            description = "水源"
            icon = join(icon, "water.ico")
        elif "seeds" == self.tools.raw_type(new_type):
            if ":" in new_type:
                description = f"{new_type.split(':')[1]}种子"
                icon = join(icon, f"{new_type.split(':')[1]}\\seeds.ico")

        arguments = "ef"+self.tools.encode({"type":new_type,"path":data["path"],"nbt":data["nbt"]})
        self.lnk.change(data["path"], description=description, icon=icon,argv=arguments)

    def __water(self, master_data):
        for j in listdir(dirname(master_data["path"])):
            j_data = self.tools.data(join(dirname(master_data["path"]), j))
            if "farmland" == self.tools.raw_type(j_data["type"]):
                if ":" in j_data["type"]:
                    self.__change_type(j_data, f"farmland_moist:{self.tools.seeds(j_data)}",j_data["nbt"])
                else:
                    self.__change_type(j_data, "farmland_moist",j_data["nbt"])


                # 更新 farmland 列表
                farmland_list = self.config.get("farmland", [])
                if not isinstance(farmland_list, list):
                    farmland_list = []
                if j_data.get("path") in farmland_list:
                    farmland_list.remove(j_data["path"])
                self.config["farmland"] = farmland_list


                # 更新 farmland_moist 列表
                moist_list = self.config.get("farmland_moist", [])
                if not isinstance(moist_list, list):
                    moist_list = []
                moist_list.append(j_data["path"])
                self.config["farmland_moist"] = moist_list






    def __plant_seeds(self, farmland_data, seeds_data):
        def plant_one(farmland, seed):
            name = ""
            if "farmland" == self.tools.raw_type(farmland["type"]):
                name = "farmland"
            else:
                name = "farmland_moist"

            # 取出当前列表，如果没有就初始化为 []
            current_list = self.config.get(name, [])
            if not isinstance(current_list, list):
                current_list = []
            current_list += [farmland["path"]]
            self.config[name] = current_list



            # TODO Nbt修改种植速度等 增加资源包
            self.__change_type(
                farmland, f"{name}:{self.tools.seeds(seed)}",
                {"total":100,"speed":1,"now":0})

            path = seed["path"]
            remove(path)



        farmland_path = dirname(farmland_data["path"])
        farm_lnks = listdir(farmland_path)
        been = True if ":" in farmland_data["type"] else False
        cnt = 0

        for seed in seeds_data:
            if cnt >= len(farm_lnks):
                break
            if been:
                flag = False
                for i in farm_lnks:
                    i_type = self.tools.type(join(farmland_path, i))
                    if "farmland" == self.tools.raw_type(i_type) or "farmland_moist" == self.tools.raw_type(i_type):
                        if ":" not in i_type:
                            plant_one(self.tools.data(join(farmland_path, i)), seed)
                            cnt += 1
                            flag = True
                            break

                if not flag:
                    return
            else:
                if ":" not in farmland_data["type"]:
                    plant_one(farmland_data, seed)

                been = True
                for j in range(len(farm_lnks)):
                    if farm_lnks[j] == basename(farmland_data["path"]):
                        farm_lnks.pop(j)
                        break



    def run(self, datas):
        if len(datas) == 0:
            return self

        for i in datas:
            print(f"{i["path"]}  {i["type"]} {i["nbt"]}")
        print("[*] Raws ========================================")

        master = datas[0]
        master_type = master["type"]

        if "hoe" == self.tools.raw_type(master_type):
            for i in datas[1:]:
                if "land" == self.tools.raw_type(i["type"]):
                    self.__change_type(i, "farmland", i["nbt"])
        elif "bucket" == self.tools.raw_type(master_type):
            for i in datas[1:]:
                if "water" == self.tools.raw_type(i["type"]):
                    self.__change_type(master, "water_bucket", i["nbt"])
                    break
        elif "water_bucket" == self.tools.raw_type(master_type):
            for i in datas[1:]:
                if "farmland" == self.tools.raw_type(i["type"]):
                    if ":" in i["type"]:
                        self.__change_type(i, "farmland_moist:" + i["type"].split(":")[1],
                                           i["nbt"])
                    else:
                        self.__change_type(i, "farmland_moist", i["nbt"])
            self.__change_type(master, "bucket", master["nbt"])
        elif "land" == self.tools.raw_type(master_type):
            for i in datas[1:]:
                if "hoe" == self.tools.raw_type(i["type"]):
                    self.__change_type(master, "farmland", i["nbt"])
        elif "water" == self.tools.raw_type(master_type):
            for i in datas[1:]:
                if "bucket" == self.tools.raw_type(i["type"]):
                    self.__change_type(i, "water_bucket", i["nbt"])
        elif "farmland" == self.tools.raw_type(master_type):
            for i in datas[1:]:
                if "water_bucket" == self.tools.raw_type(i["type"]):
                    self.__water(master)
                    self.__change_type(i,"bucket",master["nbt"])
                elif "seeds" == self.tools.raw_type(i["type"]):
                    self.__plant_seeds(master, datas[datas.index(i):])
                    break
                elif "bone_meal" == self.tools.raw_type(i["type"]):
                    if ":" in master_type:
                        nbt = master["nbt"]
                        nbt["now"] += 20
                        self.__change_type(master, new_type="farmland:"+self.tools.seeds(master), new_nbt=nbt)
                        remove(i["path"])
        elif "farmland_moist" == self.tools.raw_type(master_type):
            for i in datas[1:]:
                if "water_bucket" == self.tools.raw_type(i["type"]):
                    self.__water(master)
                    self.__change_type(i, "bucket", master["nbt"])
                elif "seeds" == self.tools.raw_type(i["type"]):
                    self.__plant_seeds(master, datas[datas.index(i):])
                    break
                elif "bone_meal" == self.tools.raw_type(i["type"]):
                    if ":" in master_type:
                        nbt = master["nbt"]
                        nbt["now"] += 20
                        self.__change_type(master, new_type="farmland_moist:"+self.tools.seeds(master), new_nbt=nbt)
                        remove(i["path"])
        elif "seeds" == self.tools.raw_type(master_type):
            for i in datas[1:]:
                if "farmland" == self.tools.raw_type(i["type"]):
                    self.__plant_seeds(master, datas[datas.index(i):])
                    break
                elif "farmland_moist" == self.tools.raw_type(i["type"]):
                    self.__plant_seeds(master, datas[datas.index(i):])
                    break
        else:
            print(f"未知type:{master_type}")


        self.refresh.refresh(True)
