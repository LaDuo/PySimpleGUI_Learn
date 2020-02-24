from defi import Desktop
from defi import slope_path
import os
import re
import matplotlib.pyplot as plt


# 画图
def draw(path_id, value_list=[], x=0):
    # print('In')
    print(x)
    plt.clf()
    plt.plot(range(x), value_list)
    plt.title(path_id)
    plt.show()
    # print('I am show slope')


# 模式1：一次发送两个slope
def BANDWIDTH():
    # print('-IN-')
    slope_path_id = re.compile(r'path=\d+')
    slope_value = re.compile(r'value=\d+')
    slope_value1 = re.compile(r'value1=\d+')
    slope_cyc = re.compile(r'cyclic=\d')
    slope_ofs = re.compile(r'offs=\d+')
    slope_ofs1 = re.compile(r'distance1=\d+')
    with open(slope_path, 'r', encoding="utf-8") as f:
        lir = f.readlines()

    lir_value = []
    lir_ofs = []
    for i in range(len(lir)):
        if i == len(lir) - 1:
            break
        j = i + 1
        value = str(slope_value.findall(lir[i]))
        value1 = str(slope_value1.findall(lir[i]))
        value = int(re.sub(r'\D', "", value))
        value1 = int(re.sub(r'\D', "", value1)[1:])
        offset = str(slope_ofs.findall(lir[i]))
        offset = int(re.sub(r'\D', "", offset))
        offset1 = str(slope_ofs1.findall(lir[i]))
        offset1 = int(re.sub(r'\D', "", offset1))
        path1 = str(slope_path_id.findall(lir[i]))
        path2 = str(slope_path_id.findall(lir[j]))
        path1 = int(re.sub(r'\D', "", path1))
        path2 = int(re.sub(r'\D', "", path2))

        # if offset > offset1:
        #     draw(path1, lir_value, lir_ofs)
        #     lir_value = []
        #     lir_ofs = []

        lir_value.append(value)
        lir_ofs.append(offset)
        if value1 != 0:
            lir_value.append(value1)
            lir_ofs.append(offset1)
        x = len(lir_value)
        if path1 != path2:
            draw(path1, lir_value, x)
            lir_value = []
            lir_ofs = []
    draw(path1, lir_value, x)


# 模式2：备份发送
def ROBUSNESS():
    slope_path_id = re.compile(r'path=\d+')
    slope_value = re.compile(r'value=\d+')
    # slope_value1 = re.compile(r'value1=\d+')
    # slope_cyc = re.compile(r'cyclic=\d')
    slope_ofs = re.compile(r'offs=\d+')

    with open(slope_path, 'r', encoding="utf-8") as f:
        lir = f.readlines()
    lir_value = []
    lir_ofs = []
    for i in range(len(lir)):
        if i == len(lir) - 1:
            break
        j = i + 1
        value = str(slope_value.findall(lir[i]))
        value = int(re.sub(r'\D', "", value))
        offset = str(slope_ofs.findall(lir[i]))
        offset = int(re.sub(r'\D', "", offset))
        path1 = str(slope_path_id.findall(lir[i]))
        path2 = str(slope_path_id.findall(lir[j]))
        path1 = int(re.sub(r'\D', "", path1))
        path2 = int(re.sub(r'\D', "", path2))
        if value:
            lir_value.append(value)
            lir_ofs.append(offset)
        if path1 != path2:
            draw(path1, lir_value, lir_ofs)
            lir_value = []
            lir_ofs = []
        lir_value.append(value)
        lir_ofs.append(offset)
        x = len(lir_value)
        if path1 != path2:
            draw(path1, lir_value, x)
            lir_value = []
            lir_ofs = []
    draw(path1, lir_value, x)


if __name__ == '__main__':
    BANDWIDTH()
    # ROBUSNESS()
