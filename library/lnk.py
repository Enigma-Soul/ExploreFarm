import pylnk3
from os.path import join,exists,abspath
from os import remove,makedirs
from shutil import copyfile
class Lnk:
    def __init__(self, target_file, icon_path):
        self.target_file = target_file
        self.icon_path = icon_path

    def create(self,name,path,argv,description,icon):
        path = abspath(path)
        if not exists(path):
            makedirs(path)
        lnk = pylnk3.for_file(
            target_file=self.target_file,
            lnk_name=path+"\\"+name+'.lnk',
            arguments=argv,
            description=description,
            icon_file=join(self.icon_path,icon),
            icon_index=0,
            work_dir=None,
            window_mode='Minimized'
        )
        lnk.save()
    def read(self,path):
        lnk = pylnk3.Lnk(path)
        return {
            'path':lnk.path,
            'working_dir':lnk.working_dir,
            'description':lnk.description,
            'arguments':lnk.arguments,
            'icon':lnk.icon
        }
    def change(self,path,argv=None,description=None,icon=None,temp="./temp.lnk"):
        if exists(temp):
            remove(temp)
        lnk = pylnk3.Lnk(path)

        if argv:
            new_arguments = argv
        else:
            new_arguments = lnk.arguments
        if description:
            new_description = description
        else:
            new_description = lnk.description
        if icon:
            new_icon = icon
        else:
            new_icon = lnk.icon
        pylnk3.for_file(
            target_file=self.target_file,
            lnk_name=temp,
            arguments=new_arguments,
            description=new_description,
            icon_file=join(self.icon_path,new_icon),
            icon_index=0,
            work_dir=None,
            window_mode='Minimized'
            )
        lnk.save()
        copyfile(temp,path)
        remove(temp)

    def delete(self,path):
        remove(path)

