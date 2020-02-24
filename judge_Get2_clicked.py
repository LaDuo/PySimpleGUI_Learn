import os
from defi import Av2_Output

meta_flag = False
pos_flag = False
pos_stub_flag = False
prl1_flag = False
prl2_flag = False
prl9_flag = False
prs1_flag = False
prs4_flag = False
seg_flag = False
slope_flag = False
stub_flag = False


# 检测文件是否存在，若不存在，则返回字符串，表示丢失文件
def detect_file_exist():
    global seg_flag, meta_flag, pos_flag, prl1_flag, \
        prl2_flag, prl9_flag, prs1_flag, prs4_flag, slope_flag, stub_flag
    strr = ''
    lists = os.listdir(Av2_Output)
    for i in lists:
        if 'meta.txt' in i:
            meta_flag = True
        elif 'pos.txt' in i:
            pos_flag = True
        elif 'pos_stub.txt' in i:
            pos_stub_flag = True
        elif 'prl1.txt' in i:
            prl1_flag = True
        elif 'prl2.txt' in i:
            prl2_flag = True
        elif 'prl9.txt' in i:
            prl9_flag = True
        elif 'prs1.txt' in i:
            prs1_flag = True
        elif 'prs4.txt' in i:
            prs4_flag = True
        elif 'seg.txt' in i:
            seg_flag = True
        elif 'slope.txt' in i:
            slope_flag_flag = True
        elif 'stub.txt' in i:
            stub_flag = True

    for i in lists:
        if not meta_flag:
            strr += 'meta.txt、'
            meta_flag = True
        elif not pos_flag:
            strr += 'pos.txt、'
            pos_flag = True
        elif not prl1_flag:
            strr += 'prl1.txt、'
            prl1_flag = True
        elif not prl2_flag:
            strr += 'prl2.txt、'
            prl2_flag = True
        elif not prl9_flag:
            strr += 'prl9.txt、'
            prl9_flag = True
        elif not prs1_flag:
            strr += 'prs1.txt、'
            prs1_flag = True
        elif not prs4_flag:
            strr += 'prs4.txt、'
            prs4_flag = True
        elif not seg_flag:
            strr += 'seg.txt、'
            seg_flag = True
        elif not stub_flag:
            strr += 'stub.txt、'
            stub_flag = True
    # print(strr)
    return strr
