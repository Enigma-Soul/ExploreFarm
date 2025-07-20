from PIL import Image
from shutil import copy,rmtree
from os import listdir, makedirs, remove, walk, path

class build_icons:
    def __init__(self, assets_path, resourcepacks_path, temp_path, icon_path,older):
        # 预定义
        self.ico_size = 256



        self.icon_path = icon_path
        self.assets_path = assets_path
        self.resourcepacks_path = resourcepacks_path
        self.temp_path = temp_path
        self.older = older

    def remove(self,all=False):
        if path.exists(self.temp_path):
            rmtree(self.temp_path)
        if path.exists(self.icon_path) and all:
            rmtree(self.icon_path)

    def __copy_pngs(self):
        def copy_folder(folder):
            # 得到文件
            dirs = []
            for i in walk(folder, topdown=True):
                for file in i[2]:
                    file_path = path.join(i[0], file)
                    dirs += [file_path]
            # 复制文件
            for file in dirs:
                if file.endswith(".png"):
                    destination_file = file.replace(folder, self.temp_path)
                    destination_dir = path.dirname(destination_file)
                    # 确保目标文件夹存在
                    if not path.exists(destination_dir):
                        makedirs(destination_dir)
                    # 如果目标文件已存在，则删除它
                    if path.exists(destination_file):
                        remove(destination_file)
                    # 复制文件
                    copy(file, destination_file)

        # 复制assets
        copy_folder(self.assets_path)
        # 复制resourcepacks
        for i in self.older:
            if path.exists(path.join(self.resourcepacks_path, i)):
                copy_folder(path.join(self.resourcepacks_path, i))


    def build(self):
        def png2ico(pngs,save_path=""):
            img = Image.new("RGBA",(256,256),(0,0,0,0))
            for i in pngs:
                t = Image.open(path.join(self.temp_path,f"{i}.png"))
                t = t.resize((256,256),Image.NEAREST)
                t = t.convert("RGBA")
                img.paste(t,(0,0),t)
            if save_path == "":
                save_path = pngs[-1]
            dirs = self.icon_path
            for i in save_path.split("\\")[:-1]:
                dirs = path.join(dirs,i)
            if not path.exists(dirs):
                makedirs(dirs)
            img.save(path.join(self.icon_path,f"{save_path}.ico"),format="ICO", sizes=[(self.ico_size, self.ico_size)])


        self.remove(True)
        self.__copy_pngs()
        if not path.exists(self.icon_path):
            makedirs(self.icon_path)



        # 开始Build
        ## 骨粉
        png2ico(["bone_meal"])
        ## 水
        png2ico(["water"])
        ## 耕地
        png2ico(["farmland"])
        ## 湿润耕地
        png2ico(["farmland_moist"])
        ## 桶
        png2ico(["bucket"])
        ## 水桶
        png2ico(["water_bucket"])
        ## 锄头
        png2ico(["hoe"])
        ## 土地
        png2ico(["land"])
        ## 农作物
        crops={}
        for crop in listdir(self.temp_path+"\\crops"):
            i = 0
            for i in range(len(listdir(self.temp_path+"\\crops\\"+crop))):
                if path.exists(self.temp_path+"\\crops\\"+crop+"\\"+str(i)+".png"):
                    ## 耕地
                    png2ico(["farmland", f"crops\\{crop}\\{i}"], f"{crop}\\{i}")
                    ## 湿润耕地
                    png2ico(["farmland_moist", f"crops\\{crop}\\{i}"], f"{crop}\\_{i}")
            if i == 0:
                # 作废
                rmtree(f"{self.icon_path}\\{crop}")
                print(f"[!] {crop} 缺少了农作物图片")

            if path.exists(self.temp_path+"\\crops\\"+crop+"\\seeds.png"):
                ## 种子
                png2ico([f"crops\\{crop}\\seeds"], f"{crop}\\seeds")
            else:
                # 作废
                rmtree(f"{self.icon_path}\\{crop}")
                print(f"[!] {crop} 缺少了种子图片")
            crops[crop] = i

        self.remove()
        return crops
