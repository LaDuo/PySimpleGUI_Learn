from defi import Analyze
from defi import list_ehp
from defi import list_ada
from defi import list_loc
from defi import Av2_Output
import re
import os
from tkinter.messagebox import showerror
import PySimpleGUI as sg


# 可以添加一个进度条
# 合并EHPLOG中adasisApp、ehrizonApp、localizationApp的INFO文件
def merge_info(map_name):
    ehplog = os.listdir(Analyze)
    for i in ehplog:
        if i.endswith(map_name):
            str1 = str(i)
    str1 = os.path.join(Analyze, str1)
    folder = str1 + "\\EHPLOG"
    print(folder)

    try:
        list_Info = os.listdir(folder)
    except FileNotFoundError as e:
        showerror(title='File not found', message='未找到Ehplog！')
        return False
    for i in list_Info:
        if i.startswith("eho") and "INFO" in i and "Nebu" in i:
            list_ehp.append(i)
        if i.startswith("ada") and "INFO" in i and "Nebu" in i:
            list_ada.append(i)
            list_ada.append(i)
        if i.startswith("loc") and "INFO" in i and "Nebu" in i:
            list_loc.append(i)
    # adasis_INFO.txt
    ada_result = Av2_Output + "\\adasis_INFO.txt"
    file = open(ada_result, 'w')
    for a in list_ada:
        path = folder + "\\" + a
        for line in open(path):
            file.write(line)
        file.write("\n")
    file.close()
    # ehp_INFO.txt
    ehp_result = Av2_Output + "\\ehp_INFO.txt"
    file = open(ehp_result, 'w')
    for a in list_ehp:
        path = folder + "\\" + a
        for line in open(path):
            file.write(line)
        file.write("\n")
    file.close()
    # localization_INFO.txt
    loc_result = Av2_Output + "\\localization_INFO.txt"
    file = open(loc_result, 'w')
    for a in list_loc:
        path = folder + "\\" + a
        for line in open(path):
            file.write(line)
        file.write("\n")
    file.close()
    # 提取matchpt,gcj
    pattern = re.compile(r'matchpt,\d+\.\d+,\d+\.\d+')
    path_mapmatch = Av2_Output + "\\localization_INFO.txt"
    matchpt = Av2_Output + "\\matchpt.txt"
    gcj = Av2_Output + "\\gcj1.txt"
    with open(path_mapmatch, 'r', encoding="utf-8") as f:
        match = f.readlines()
    with open(matchpt, 'w', encoding='utf-8') as f:
        for i in range(len(match)):
            m = pattern.findall(match[i])
            if m:
                n = str(m)
                f.write(n[2:-2])
                f.write('\n')
    pattern = re.compile(r'gcj1,\d+\.\d+,\d+\.\d+')
    path_mapmatch = Av2_Output + "\\localization_INFO.txt"
    with open(path_mapmatch, 'r', encoding="utf-8") as f:
        match = f.readlines()
    with open(gcj, 'w', encoding='utf-8') as f:
        for i in range(len(match)):
            m = pattern.findall(match[i])
            if m:
                n = str(m)
                f.write(n[2:-2])
                f.write('\n')
    return True
