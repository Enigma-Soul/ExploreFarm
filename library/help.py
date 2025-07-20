def help(cmd):
    if len(cmd) == 1:
        print("可用命令列表：")
        print("help : 查看帮助")
        print("build: 编译资源包")
        print("exit : 退出程序")
        print("set  : 放置某物")
        print("lr   : 列出可用农作物")
        print("clear: 清空配置")
        print("func : 快捷指令组")
    elif len(cmd) > 1:
        if cmd[1] == "help":
            print("用法: help [(命令)]")
            print("查看帮助")
        elif cmd[1] == "build":
            print("用法: build")
            print("编译资源包")
        elif cmd[1] == "exit":
            print("用法: exit")
            print("退出程序")
        elif cmd[1] == "set":
            print("用法: set [name] [type] [path] [num]")
            print("放置某件实物")
            print("可用type:")
            print("hoe   : 锄头   bone_meal   : 骨粉")
            print("bucket: 铁桶   water_bucket: 水桶")
            print("land  : 土地   water       : 水源")
            print("farmland: 耕地 farmland_moist: 湿润耕地")
            print("seeds:sth : 种子 (详细见下文)")
            print("可用seeds为资源包所带")
            print("crop(__选填Json__)")
            print("括号内必须为Json!!!")
            print("num 可以被省略")
            print("name 可以是- 表示留空")
            print('例: set 小麦种子 seeds:wheat({"name":"小麦"}) . 1')
        elif cmd[1] == "lr":
            print("用法: lr")
            print("列出可用农作物")
        elif cmd[1] == "clear":
            print("用法: clear")
            print("清空配置")
        elif cmd[1] == "func":
            print("用法: func [name]")
            print("运行快捷指令组")
            print("配置均在func.json文件")
        else:
            print("未知命令")
    else:
        print("未知命令")
