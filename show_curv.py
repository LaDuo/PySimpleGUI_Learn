from defi import Desktop
from defi import curv_path, dis
import os
import re
import matplotlib.pyplot as plt


# 画图
def draw(path_id, value_list=[], offset_list=[]):
    plt.clf()
    plt.plot(offset_list, value_list)
    plt.scatter(offset_list, value_list, marker='d', c='red')
    plt.grid(axis='both', c='black')
    plt.title(path_id)
    for a, b in zip(offset_list, value_list):
        plt.text(a, b, b, ha='right', va='bottom', fontsize=10)
    plt.show()
    # print('I am show slope')


# 模式3：一次发送两个slope
def BANDWIDTH():
    flag = False
    # print('-IN-')
    slope_path_id = re.compile(r'path=\d+')
    slope_value = re.compile(r'value=\d+')
    slope_value1 = re.compile(r'value1=\d+')
    slope_cyc = re.compile(r'cyclic=\d')
    slope_ofs = re.compile(r'offs=\d+')
    slope_ofs1 = re.compile(r'distance1=\d+')
    with open(curv_path, 'r', encoding="utf-8") as f:
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
        offset1 = int(offset1[12:-2])
        path1 = str(slope_path_id.findall(lir[i]))
        path2 = str(slope_path_id.findall(lir[j]))
        path1 = int(re.sub(r'\D', "", path1))
        path2 = int(re.sub(r'\D', "", path2))


        lir_value.append(value)
        lir_ofs.append(offset)
        if value1 != 0:
            lir_value.append(value1)
            lir_ofs.append(offset1)
        # if path1 != path2:
        #     draw(path1, lir_value, lir_ofs)
        #     lir_value = []
        #     lir_ofs = []
    count = 0
    # 根据offset画每一个curv点
    # for x in range(len(lir_ofs)):
    #     if x == len(lir_ofs) - 1:
    #         break
    #     y = x + 1
    #     while lir_ofs[y] < lir_ofs[x]:
    #         count = 1
    #         lir_ofs[y] += count * 8191
    #     count = 0
    points_num = 100
    times = int(len(lir_ofs) / points_num) + 1
    for i in range(times):
        s, e = i * points_num, (i + 1) * points_num
        draw(path1, lir_value[s:e], lir_ofs[s:e])


# 模式2：备份发送
def ROBUSNESS():
    slope_path_id = re.compile(r'path=\d+')
    slope_value = re.compile(r'value=\d+')
    # slope_value1 = re.compile(r'value1=\d+')
    # slope_cyc = re.compile(r'cyclic=\d')
    slope_ofs = re.compile(r'offs=\d+')

    with open(curv_path, 'r', encoding="utf-8") as f:
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


def close_show():
    plt.close()


if __name__ == '__main__':
    BANDWIDTH()
    # ROBUSNESS()
