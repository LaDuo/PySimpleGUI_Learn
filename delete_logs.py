from defi import base_path1
from defi import Av2_Input
from defi import Av2_Output
import os
from tkinter.messagebox import showinfo


def DeleteReLog():
    # 删除Release 中的log
    Avlog1 = os.listdir(base_path1)
    if not Avlog1:
        return
    else:
        for i in Avlog1:
            if ".txt" in i:
                path = os.path.join(base_path1, i)
                os.remove(path)
    list1 = os.listdir(base_path1)
    if not list1:
        return True
    else:
        return False


def DeleteInputLog():
    # 删除Av2_Input 中的log
    Avlog2 = os.listdir(Av2_Input)
    if not Avlog2:
        return
    else:
        for i in Avlog2:
            if ".txt" in i:
                path = os.path.join(Av2_Input, i)
                os.remove(path)
    list2 = os.listdir(base_path1)
    if not list2:
        return True
    else:
        return False

def DeleteOutputLog():
    # 删除Av_2Output 中的log
    Avlog3 = os.listdir(Av2_Output)
    if not Avlog3:
        return
    else:
        for i in Avlog3:
            if ".txt" in i:
                path = os.path.join(Av2_Output, i)
                os.remove(path)
        # showinfo(title="Delete AvLog", message="成功删除Av Log")
    list3 = os.listdir(base_path1)
    if not list3:
        return True
    else:
        return False