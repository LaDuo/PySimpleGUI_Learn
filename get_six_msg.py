from tkinter.messagebox import showinfo
from defi import Av2_log, stub_path, pat_Stub, pos_path, pat_Pos, seg_path, pat_Seg, prl1_path, pat_Pro_Long1, \
    prl2_path, pat_Pro_Long2, prl9_path, prs1_path, pat_Pro_Long9, pat_Pro_Sht4, prs4_path, pat_Pro_Sht1, pat_Meta, \
    pos_stub_path, slope_path, av_slope_v, short, pat_stub, meta_path
import re
import threading
import os.path


def action(route, pat, ):
    with open(Av2_log, 'r', encoding="utf-8") as file:
        lists = file.readlines()
    pats = re.compile(pat)
    with open(route, 'w', encoding="utf-8") as file:
        for i in range(len(lists)):
            n = pats.findall(lists[i])
            if n:
                file.write(lists[i])


# 创建多线程，调用action函数，进行日志文件的处理
def Sep_MSG():
    if os.path.exists(Av2_log):
        with open(Av2_log, 'r', encoding="utf-8") as file:
            lists = file.readlines()

        # stub msg
        t1 = threading.Thread(target=action, args=(stub_path, pat_Stub,))
        t1.start()
        # position msg
        t2 = threading.Thread(target=action, args=(pos_path, pat_Pos,))
        t2.start()
        # segment msg
        t3 = threading.Thread(target=action, args=(seg_path, pat_Seg,))
        t3.start()
        # profile long type 1
        t4 = threading.Thread(target=action, args=(prl1_path, pat_Pro_Long1,))
        t4.start()
        # profile long type 2
        t5 = threading.Thread(target=action, args=(prl2_path, pat_Pro_Long2,))
        t5.start()
        # profile long type 9
        t6 = threading.Thread(target=action, args=(prl9_path, pat_Pro_Long9,))
        t6.start()
        # profile short type 1
        t7 = threading.Thread(target=action, args=(prs1_path, pat_Pro_Sht1,))
        t7.start()
        # profile short type 4
        t8 = threading.Thread(target=action, args=(prs4_path, pat_Pro_Sht4,))
        t8.start()
        # Metadata
        t9 = threading.Thread(target=action, args=(meta_path, pat_Meta,))
        t9.start()
        with open(pos_stub_path, 'w', encoding="utf-8") as file:
            for i in range(len(lists)):
                a = pat_stub.findall(lists[i])
                b = pat_Pos.findall(lists[i])
                if a:
                    file.write(str(lists[i]))
                elif b:
                    file.write(str(lists[i]))

        with open(slope_path, 'w', encoding="utf-8") as file:
            for i in range(len(lists)):
                a = av_slope_v.findall(lists[i])
                b = short.findall(lists[i])
                if a and b:
                    file.write(str(lists[i]))
        # showinfo(title="提取MSG", message="成功提取各个MSG！")
        return True
    else:
        return False
