from defi import seg_path
from defi import seg_path_id
from defi import seg_offset
from defi import seg_bridge
from defi import cyclic
from defi import Err_Segment
import re
from tkinter.messagebox import showerror


# 验证Segment日志
def JudgeSegment():
    flag = 0
    lir2 = []
    cyc = []
    bri = []
    try:
        with open(seg_path, 'r', encoding="utf-8") as f:
            lir = f.readlines()
            flag = 1
    except FileNotFoundError:
        showerror(title="Warning!", message=" <seg.txt> File not found")
        flag = 0
    if flag == 1:
        for i in range(len(lir)):
            if i == len(lir) - 1:
                break
            j = i + 1
            id1 = seg_path_id.findall(lir[i])
            id2 = seg_path_id.findall(lir[j])
            ofs1 = str(seg_offset.findall(lir[i]))
            ofs2 = str(seg_offset.findall(lir[j]))
            ofs1 = int(re.sub(r'\D', "", ofs1))
            ofs2 = int(re.sub(r'\D', "", ofs2))
            bridge = seg_bridge.findall(lir[i])
            cyclic1 = str(cyclic.findall(lir[i]))
            cyclic1 = int(re.sub(r'\D', "", cyclic1))
            cyclic2 = str(cyclic.findall(lir[j]))
            cyclic2 = int(re.sub(r'\D', "", cyclic2))
            if bridge:
                bri.append(lir[i])
            if id1 == id2:
                if ofs2 < ofs1:
                    lir2.append(lir[i])
            if cyclic1 == 0:
                if cyclic2 != 1:
                    cyc.append(lir[j])

            if cyclic1 == 1:
                if cyclic2 != 2:
                    cyc.append(lir[j])

            if cyclic1 == 2:
                if cyclic2 != 3:
                    cyc.append(lir[j])

            if cyclic1 == 3:
                if cyclic2 != 0:
                    cyc.append(lir[j])

        count = 0
        # 每组问题
        with open(Err_Segment, 'w', encoding="utf-8") as f:
            for n in range(len(lir2)):
                f.write(lir2[n])
                count += 1
                if count == 2:
                    count = 0
                    f.write("======================\n")
