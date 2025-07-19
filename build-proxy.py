from os.path import abspath, dirname


def main(_debug_):
    print("[INFO] Building")
    workdir = dirname(abspath(__file__))
    with open("proxy_main.bat","w",encoding="utf-8") as f:
        f.write("@echo off\n")
        f.write(f"cd /d {workdir}\n")
        f.write("python main.py %*\n")
        if _debug_:
            f.write("pause\n")
        f.close()
    print("[INFO] Success")


if __name__ == '__main__':
    _debug_ = False
    main(_debug_)