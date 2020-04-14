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



def pop_(lir_val = [], lir_ofs = [], lir_path = []):
    tmp_path = []
    tmp_val = []
    tmp_ofs = []
    len_val = len(lir_val)
    len_ofs = len(lir_ofs)
    len_path = len(lir_path)
#     print(len_val, len_ofs, len_path)
    cnt = 200
    for i in range(len_path):
        #最后一组数据画图
        if i == len_path - 1:
            print("IN")
            len_tmp = len(tmp_val)
            print("len_tmp = ", len_tmp)
            len_1 = len_tmp/cnt
            len_2 = len_tmp%cnt
            print("len_1 = ", len_1)
            print("len_2 = ", len_2)
            if len_2 > 0 and len_2 != len_tmp:
                len_1 = int(len_1) + 1
            elif len_2 == len_tmp:
                len_1 = 1
            if len_tmp > 200:
                points_num = 200
                for j in range(len_1):
                    s, e = j * points_num, (j + 1) * points_num
                    if e <= len_tmp:
                        draw(tmp_path[0], tmp_val[s:e], tmp_ofs[s:e])
                    else:
                        draw(tmp_path[0], tmp_val[s:len_tmp], tmp_ofs[s:len_tmp])
                tmp_path = []
                tmp_val = []
                tmp_ofs = []
            elif 0 < len_tmp <= 200:
#                 print("-IN-")
                draw(tmp_path[0], tmp_val[0:len_tmp], tmp_ofs[0:len_tmp])
                tmp_path = []
                tmp_val = []
                tmp_ofs = []
            break
        
        j = i + 1
        if lir_path[i] == lir_path[j]:
            tmp_path.append(lir_path[i])
            tmp_val.append(lir_val[i])
            tmp_ofs.append(lir_ofs[i])
        elif lir_path[i] != lir_path[j]:
            tmp_path.append(lir_path[i])
            tmp_val.append(lir_val[i])
            tmp_ofs.append(lir_ofs[i])
#             print("path id = ", lir_path[i], lir_path[j])
            len_tmp = len(tmp_val)
            len_1 = len_tmp/cnt
            len_2 = len_tmp%cnt
            if len_2 > 0:
                len_1 = int(len_1) + 1
#             print("len_1 = ", len_1)
            if len_tmp > 200:
                points_num = 200
                for j in range(len_1):
                    s, e = j * points_num, (j + 1) * points_num
                    if e <= len_tmp:
                        draw(tmp_path[0], tmp_val[s:e], tmp_ofs[s:e])
                    else:
                        draw(tmp_path[0], tmp_val[s:len_tmp], tmp_ofs[s:len_tmp])
                tmp_path = []
                tmp_val = []
                tmp_ofs = []
            elif 0 < len_tmp <= 200:
                draw(tmp_path[0], tmp_val[0:len_tmp], tmp_ofs[0:len_tmp])
                tmp_path = []
                tmp_val = []
                tmp_ofs = []

    
            
    
    
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
    with open(slope_path, 'r', encoding="utf-8") as f:
        lir = f.readlines()
    lir_value = []
    lir_ofs = []
    lir_path = []
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
        
        #将value和offset和path加入列表
        lir_value.append(value)
        lir_ofs.append(offset)
        lir_path.append(path1)
        if value1 != 0:
            lir_path.append(path1)
            lir_value.append(value1)
            lir_ofs.append(offset1)

    count = 0
    len_ofs = len(lir_ofs)
    len_val = len(lir_value)
            
    #将slope的offset递增
    for x in range(len_ofs):
        if x == len_ofs - 1:
            break
        y = x + 1
        while lir_ofs[y] < lir_ofs[x]:
            count = 1
            lir_ofs[y] += count * 8191
    pop_(lir_value, lir_ofs, lir_path) 




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
    lir_path = []
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
        #将value和offset和path加入列表
        lir_value.append(value)
        lir_ofs.append(offset)
        lir_path.append(path1)
    count = 0
    len_ofs = len(lir_ofs)
    len_val = len(lir_value)    
    #将slope的offset递增
    for x in range(len_ofs):
        if x == len_ofs - 1:
            break
        y = x + 1
        while lir_ofs[y] < lir_ofs[x]:
            count = 1
            lir_ofs[y] += count * 8191
    pop_(lir_value, lir_ofs, lir_path) 


#if __name__ == '__main__':
#     BANDWIDTH()
#     ROBUSNESS()
