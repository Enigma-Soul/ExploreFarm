from library import build_icons
from library import config
from library import lnk
from library import help
from library import open_with
from library import refresh
from library.tools import Tools
from sys import argv
from os.path import abspath, dirname,exists,join


class Main:
    def __init__(self):
        self.config = config.Config()
        self.build_result = None
        self.running_path = dirname(abspath(__file__))
        self.check_config()
        self.lnk = lnk.Lnk(self.running_path+"\\proxy_main.bat", self.running_path+"\\icons")
        self.tools = Tools(self.lnk)
        self.fresh = refresh.refresh(self.lnk,self.config,self.tools)
        self.open = open_with.open_with(self.lnk, self.config, self.running_path, self.tools,self.fresh)


        self.func = config.Config("func.json")


    def build(self):
        build_tools = build_icons.build_icons(self.running_path+"\\assets", self.running_path+"\\resourcepacks", self.running_path+"\\temp", self.running_path+"\\icons", [])
        self.build_result = build_tools.build()
        self.config.update({"seeds": self.build_result})

    def check_config(self):
        keys = list(self.config.keys())
        if not self.build_result:
            self.build()
        if "farmland" not in keys:
            self.config["farmland"] = []
        if "farmland_moist" not in keys:
            self.config["farmland_moist"] = []
        self.config["seeds"] = self.build_result



    def set(self, name, type, path, num, nbt=None):
        if nbt is None:
            nbt = {}
        # 调成path
        path = abspath(path)

        for i in range(int(num)):


            icon_path = f"{type}.ico"
            if name == "-":
                new_name = ""
                if int(num) != 1:
                    new_name += f"{i + 1}"
                else:
                    new_name = str(i)
            else:
                new_name = name
                if int(num) != 1:
                    new_name += f"_{str(i + 1)}"

            data = self.tools.encode({"type": type, "path":join(path,new_name+".lnk"),"nbt": nbt})
            if type == "hoe":
                self.lnk.create(new_name, path, f"ef{data}", "一个小锄头", icon_path)
            elif type == "bucket":
                self.lnk.create(new_name, path, f"ef{data}", "一个铁桶", icon_path)
            elif type == "water_bucket":
                self.lnk.create(new_name, path, f"ef{data}", "一个水桶", icon_path)
            elif type == "land":
                self.lnk.create(new_name, path, f"ef{data}", "一块土地", icon_path)
            elif type == "water":
                self.lnk.create(new_name, path, f"ef{data}", "水源", icon_path)
            elif type == "farmland":
                self.lnk.create(new_name, path, f"ef{data}", "一块耕地", icon_path)
            elif type == "farmland_moist":
                self.lnk.create(new_name, path, f"ef{data}", "湿润耕地", icon_path)
            elif type == "bone_meal":
                self.lnk.create(new_name, path, f"ef{data}", "骨粉", icon_path)
            elif len(type) >= 6 and type[0:6] == "seeds:":
                self.lnk.create(new_name, path, f"ef{data}", f"{type[6:]} 种子", f"{type[6:]}\\seeds.ico")
            else:
                print(f"未知type:{type}")
                return None
        return None

    def run(self):
        cmds = argv[1:]
        datas = []

        if cmds[0][0:2] != "ef":
            return False
        else:
            datas += [self.tools.decode(cmds[0])]

        # 转换所有为 Data
        for i in cmds[1:]:
            if exists(i):
                try:
                    data = self.tools.decode(self.lnk.read(i)["arguments"])
                    if data != {}:
                        # 强制同步 path 字段
                        if data["path"] != i:
                            data["path"] = i
                            self.lnk.change(i, f"ef{self.tools.encode(data)}")
                        else:
                            # 即使一致，也强制写入，防止丢失
                            self.lnk.change(i, f"ef{self.tools.encode(data)}")
                        datas.append(data)
                    else:
                        continue
                except Exception as e:
                    print(f"Error processing lnk file {i}: {e}")
                    continue
        del cmds
        self.open.run(datas)

        return True

    def cmd(self):
        self.fresh.run()

        def run_cmd(command):
            if len(command) == 0:
                return None

            if command[0] == "help":
                help.help(command)
            elif command[0] == "build":
                self.build()
            elif command[0] == "exit":
                exit()
            elif command[0] == "set":
                if len(command) < 4:
                    print("用法: set [name] [type] [path] [(num)]")
                else:
                    if len(command) == 4:
                        command += ["1"]

                    # 得到NBT
                    if "(" in command[2] and ")" in command[2]:
                        nbt = command[2].split("(")[1].split(")")[0]
                    else:
                        nbt = "{}"
                    if config.is_dict(nbt):
                        nbt = self.tools.decode(nbt)
                    else:
                        nbt = {}

                    command[2] = command[2].split("(")[0]

                    if command[2][0:6] == "seeds:":
                        seed = command[2].split(":")
                        if seed[1] in self.config["seeds"]:
                            self.set(command[1], command[2], command[3], command[4], nbt)
                        else:
                            print("无效的种子")
                    elif command[2] in ["hoe", "bucket", "water_bucket", "land", "water", "farmland",
                                        "farmland_moist","bone_meal"]:
                        self.set(command[1], command[2], command[3], command[4],nbt)
                    else:
                        print(f"未知物品 {command[2]}")
            elif command[0] == "clear":
                self.config.clear()
                self.check_config()

            elif command[0] == "func":
                for i in self.func.get(command[1]):

                    if i[0:4] != "func":
                        run_cmd(i.split(" "))
                    else:
                        print("[!] func里不能调用func")
            elif command[0] == "":
                pass
            else:
                print(f"未知命令 {command[0]}")

        while True:
            cmd = input(f"{self.running_path} Farm ~$")
            run_cmd(cmd.split(" "))





if __name__ == '__main__':
    main = Main()
    if len(argv) == 1:
        main.cmd()
    else:
        main.run()
