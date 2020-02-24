import threading
import os
from tkinter.messagebox import showinfo
from defi import Av2_Output
from defi import stub_path, cyclic_stub
from defi import pos_path, cyclic_pos
from defi import seg_path, cyclic_seg
from defi import prl1_path, cyclic_prl1
from defi import prl2_path, cyclic_prl2
from defi import prl9_path, cyclic_prl9
from defi import prs1_path, cyclic_prs1
from defi import prs4_path, cyclic_prs4
from defi import meta_path, cyclic_meta
from defi import cyclic


# meta_flag = False
# pos_flag = False
# pos_stub_flag = False
# prl1_flag = False
# prl2_flag = False
# prl9_flag = False
# prs1_flag = False
# prs4_flag = False
# seg_flag = False
# slope_flag = False
# stub_flag = False
#
#
# def detect():
#     listt = os.listdir(Av2_Output)
#     for i in listt:
#         if meta


def Cyclic():
    # stub msg
    t1 = threading.Thread(target=thread_cyc, args=(stub_path, cyclic_stub))
    t1.start()
    # position msg
    t2 = threading.Thread(target=thread_cyc, args=(pos_path, cyclic_pos))
    t2.start()
    # segment msg
    t3 = threading.Thread(target=thread_cyc, args=(seg_path, cyclic_seg))
    t3.start()
    # profile long type 1
    t4 = threading.Thread(target=thread_cyc, args=(prl1_path, cyclic_prl1))
    t4.start()
    # profile long type 2
    t5 = threading.Thread(target=thread_cyc, args=(prl2_path, cyclic_prl2))
    t5.start()
    # profile long type 9
    t6 = threading.Thread(target=thread_cyc, args=(prl9_path, cyclic_prl9))
    t6.start()
    # profile short type 1
    t7 = threading.Thread(target=thread_cyc, args=(prs1_path, cyclic_prs1))
    t7.start()
    # profile short type 4
    t8 = threading.Thread(target=thread_cyc, args=(prs4_path, cyclic_prs4))
    t8.start()
    # Metadata
    t9 = threading.Thread(target=thread_cyc, args=(meta_path, cyclic_meta))
    t9.start()
    showinfo(title="丢包判断", message="判断结束")


def thread_cyc(route, path):
    with open(route, 'r', encoding="utf-8") as file:
        lir = file.readlines()
    print(threading.current_thread().getName(), "+", route)
    with open(path, 'w', encoding="utf-8") as f:
        for i in range(len(lir)):
            if i == len(lir) - 1:
                break
            j = i + 1
            mode1 = str(cyclic.findall(lir[i]))
            mode2 = str(cyclic.findall(lir[j]))
            if mode1 == "['cyclic=0']":
                if mode2 != "['cyclic=1']":
                    f.write(lir[j])
                    f.write("\n")
            elif mode1 == "['cyclic=1']":
                if mode2 != "['cyclic=2']":
                    f.write(lir[j])
                    f.write("\n")
            elif mode1 == "['cyclic=2']":
                if mode2 != "['cyclic=3']":
                    f.write(lir[j])
                    f.write("\n")
            elif mode1 == "['cyclic=3']":
                if mode2 != "['cyclic=0']":
                    f.write(lir[j])
                    f.write("\n")
