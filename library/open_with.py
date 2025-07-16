from os import listdir, remove
from os.path import abspath, dirname, join, basename


class open_with:
    def __init__(self, lnk, lnk_uid, config, running_path):
        self.lnk = lnk
        self.lnk_uid = lnk_uid
        self.config = config
        self.running_path = running_path

    def __get_uid_by_file(self, file):
        return self.lnk.read(file)["arguments"][2:]

    def __get_type_by_uid(self, uid):
        return self.lnk_uid.get(uid)["type"]

    def __get_full_path_by_uid(self, uid):
        return self.lnk_uid.get(uid)["path"]

    def __get_path_by_uid(self, uid):
        return dirname(self.lnk_uid.get(uid)["path"])

    def __get_nbt_by_uid(self, uid):
        return self.lnk_uid.get(uid)["nbt"]

    def __change_type(self, uid, new_type, new_nbt):
        self.lnk_uid.data[uid]["type"] = new_type
        self.lnk_uid.data[uid]["nbt"] = new_nbt
        description = ""
        icon = join(self.running_path, "icons")
        if "hoe" == self.get_raw_type(new_type):
            description = "一把锄头"
            icon = join(icon, "hoe.ico")
        elif "bucket" == self.get_raw_type(new_type) and "water_bucket" not in new_type:
            description = "一个桶"
            icon = join(icon, "bucket.ico")
        elif "water_bucket" == self.get_raw_type(new_type):
            description = "一个水桶"
            icon = join(icon, "water_bucket.ico")
        elif "farmland" == self.get_raw_type(new_type):
            if ":" in new_type:
                description = f"一块{new_type.split(':')[1]}耕地"
                icon = join(icon, f"{new_type.split(':')[1]}\\0.ico")
            else:
                description = "一块耕地"
                icon = join(icon, "farmland.ico")
        elif "farmland_moist" == self.get_raw_type(new_type):
            if ":" in new_type:
                description = f"湿润的{new_type.split(':')[1]}耕地"
                icon = join(icon, f"{new_type.split(':')[1]}\\_0.ico")
            else:
                description = "湿润耕地"
                icon = join(icon, "farmland_moist.ico")
        elif "land" == self.get_raw_type(new_type):
            description = "一块土地"
            icon = join(icon, "dirt.ico")
        elif "water" == self.get_raw_type(new_type):
            description = "水源"
            icon = join(icon, "water.ico")
        elif "seeds" == self.get_raw_type(new_type):
            if ":" in new_type:
                description = f"{new_type.split(':')[1]}种子"
                icon = join(icon, f"{new_type.split(':')[1]}\\seeds.ico")
        self.lnk.change(self.__get_full_path_by_uid(uid), description=description, icon=icon)
        self.config.save()

    def __water(self, master_uid):
        for j in listdir(self.__get_path_by_uid(master_uid)):
            j_uid = self.__get_uid_by_file(join(dirname(self.lnk_uid.get(master_uid)["path"]), j))
            if "farmland" == self.get_raw_type(self.__get_type_by_uid(j_uid)):
                if ":" in self.__get_type_by_uid(j_uid):
                    self.__change_type(j_uid, "farmland_moist:" + self.__get_type_by_uid(j_uid).split(":")[1],
                                       self.__get_nbt_by_uid(j_uid))
                else:
                    self.__change_type(j_uid, "farmland_moist", self.__get_nbt_by_uid(j_uid))


    def get_raw_type(self, type):
        return type.split(":")[0]

    def __plant_seeds(self, farmland_uid, seeds_uids):
        farmland_path = self.__get_path_by_uid(farmland_uid)
        farm_dirs = listdir(farmland_path)
        been = True if ":" in self.get_raw_type(farmland_uid) else False
        cnt = 0
        for seed_uid in seeds_uids:
            seed_path = self.__get_full_path_by_uid(seed_uid)
            if not seed_path or not self.__get_uid_by_file(seed_path):
                continue
            if cnt >= len(farm_dirs):
                break
            farm_type = ""
            if "farmland" == self.get_raw_type(self.__get_type_by_uid(self.__get_uid_by_file(join(farmland_path, farm_dirs[cnt])))):
                farm_type = "farmland"
            else:
                farm_type = "farmland_moist"

            if been:
                if ":" not in self.__get_type_by_uid(self.__get_uid_by_file(farm_dirs[cnt])):
                    print(seed_uid,
                          farm_type + ":" + self.__get_type_by_uid(self.__get_uid_by_file(seed_path)).split(":")[1],
                          self.__get_nbt_by_uid(self.__get_uid_by_file(join(farmland_path, farm_dirs[cnt]))))
                    self.__change_type(seed_uid,
                                       farm_type+":" + self.__get_type_by_uid(self.__get_uid_by_file(seed_path)).split(":")[1],
                                       self.__get_nbt_by_uid(self.__get_uid_by_file(join(farmland_path, farm_dirs[cnt]))))
                    cnt += 1
                    remove(seed_path)
                    self.config.config.pop(seed_uid)
                    self.lnk_uid.pop(seed_uid)
                    self.config.save()
            else:
                if ":" not in self.__get_type_by_uid(farmland_uid):
                    print(seed_uid,
                                       farm_type+":"+self.__get_type_by_uid(self.__get_uid_by_file(seed_path)).split(":")[1],
                                       self.__get_nbt_by_uid(self.__get_uid_by_file(join(farmland_path, farm_dirs[cnt]))))
                    self.__change_type(seed_uid,
                                       farm_type+":"+self.__get_type_by_uid(self.__get_uid_by_file(seed_path)).split(":")[1],
                                       self.__get_nbt_by_uid(self.__get_uid_by_file(join(farmland_path, farm_dirs[cnt]))))
                been = True
                for j in range(len(farm_dirs)):
                    if farm_dirs[j] == basename(seed_path):
                        farm_dirs.pop(j)
                        break
                remove(seed_path)
                self.config.config["lnk"].pop(seed_uid)
                self.lnk_uid.pop(seed_uid)
                self.config.save()


    def run(self, uids):
        if len(uids) == 0:
            return self
        print("[*] Before ================")
        for i in uids:
            print(
                f"{i}  {basename(self.__get_full_path_by_uid(i))}  {self.__get_type_by_uid(i)} {self.__get_nbt_by_uid(i)}")
        print("[*] Before ================")

        master = uids[0]
        master_type = self.__get_type_by_uid(master)

        print(master_type)

        if "hoe" == self.get_raw_type(master_type):
            for i in uids[1:]:
                if "land" == self.get_raw_type(self.__get_type_by_uid(i)):
                    self.__change_type(i, "farmland", self.__get_nbt_by_uid(i))
        elif "bucket" == self.get_raw_type(master_type):
            for i in uids[1:]:
                if "water" == self.get_raw_type(self.__get_type_by_uid(i)):
                    self.__change_type(master, "water_bucket", self.__get_nbt_by_uid(i))
                    break
        elif "water_bucket" == self.get_raw_type(master_type):
            for i in uids[1:]:
                if "farmland" == self.get_raw_type(self.__get_type_by_uid(i)):
                    if ":" in self.__get_type_by_uid(i):
                        self.__change_type(i, "farmland_moist:" + self.__get_type_by_uid(i).split(":")[1],
                                           self.__get_nbt_by_uid(i))
                    else:
                        self.__change_type(i, "farmland_moist", self.__get_nbt_by_uid(i))
        elif "land" == self.get_raw_type(master_type):
            for i in uids[1:]:
                if "hoe" == self.get_raw_type(self.__get_type_by_uid(i)):
                    self.__change_type(master, "farmland", self.__get_nbt_by_uid(i))
        elif "water" == self.get_raw_type(master_type):
            for i in uids[1:]:
                if "bucket" == self.get_raw_type(self.__get_type_by_uid(i)):
                    self.__change_type(i, "water_bucket", self.__get_nbt_by_uid(i))
        elif "farmland" == self.get_raw_type(master_type):
            for i in uids[1:]:
                if "water_bucket" == self.get_raw_type(self.__get_type_by_uid(i)):
                    self.__water(master)
                elif "seeds" == self.get_raw_type(self.__get_type_by_uid(i)):
                    if ":" not in master_type:
                        self.__plant_seeds(master, [i])
        elif "farmland_moist" == self.get_raw_type(master_type):
            for i in uids[1:]:
                if "water_bucket" == self.get_raw_type(self.__get_type_by_uid(i)):
                    self.__water(master)
                elif "seeds" == self.get_raw_type(self.__get_type_by_uid(i)):
                    if ":" not in master_type:
                        self.__plant_seeds(master, [i])
        elif "bone_meal" == self.get_raw_type(master_type):
            for i in uids[1:]:
                pass
        elif "seeds" == self.get_raw_type(master_type):
            for i in uids[1:]:
                if "farmland" == self.get_raw_type(self.__get_type_by_uid(i)):
                    self.__plant_seeds(i, [master])
                elif "farmland_moist" == self.get_raw_type(self.__get_type_by_uid(i)):
                    if ":" not in master_type:
                        self.__plant_seeds(i, [master])
        else:
            print(f"未知type:{master_type}")

        print("[*] After ================")
        for i in uids:
            if self.lnk_uid.check(i):
                print(
                    f"{i}  {basename(self.__get_full_path_by_uid(i))}  {self.__get_type_by_uid(i)} {self.__get_nbt_by_uid(i)}")

        print("[*] After ================")
