import os
from tkinter.messagebox import showerror, showinfo
import shutil
from defi import Desktop
from defi import Analyze
from defi import Av2_Input
from defi import Av2_Output
# Desktop = os.path.join(os.path.expanduser('~'), "Desktop")
# Analyze = os.path.join(Desktop, "Analyze")
# Av2_Input = os.path.join(Desktop, "Av2_Input")
# Av2_Output = os.path.join(Desktop, "Av2_Output")


def make_path(str1, str2):
    return os.path.join(str1, str2)


def delete_log(path):
    list1 = os.listdir(path)
    for i in list1:
        print("It's removing file {}".format(i))
        try:
            os.remove(make_path(Av2_Input, i))
        except FileNotFoundError as err:
            print(err)


# 将传入的path中的文件夹复制到Av2_Input文件夹中
def move_txt(path):
    print(path)
    list1 = os.listdir(path)
    for i in list1:
        # print(i)
        try:
            shutil.copyfile(make_path(path, i), make_path(Av2_Input, i))
        except FileNotFoundError as err:
            showerror(title="File Not Found", message="文件不存在\n"
                                                      "请确认选择的文件夹中包含有日志")
            break
    print('End')



