import re
import matplotlib.pyplot as plt

can_qian = "D:\\tmp\\HQ对比测试数据\\HQ-slop-curv-画图对比数据\\can_qian.txt"
can_hou = "D:\\tmp\\HQ对比测试数据\\HQ-slop-curv-画图对比数据\\can_hou.txt"
can_rest = "D:\\tmp\\HQ对比测试数据\\HQ-slop-curv-画图对比数据\\can_rest.txt"

pc_qian = "D:\\tmp\\HQ对比测试数据\\HQ-slop-curv-画图对比数据\\pc_qian.txt"
pc_hou = "D:\\tmp\\HQ对比测试数据\\HQ-slop-curv-画图对比数据\\pc_hou.txt"
pc_rest = "D:\\tmp\\HQ对比测试数据\\HQ-slop-curv-画图对比数据\\pc_rest.txt"

slop = re.compile(r'slop:\d+')
curv = re.compile(r'curv:\d+')


def read_data(path1, path2):
    with open(path1, 'r', encoding='utf-8') as f:
        lir1 = f.readlines()
    with open(path2, 'r', encoding='utf-8') as f:
        lir2 = f.readlines()
    sl1, sl2 = [], []
    for i in lir1:
        s = "".join(slop.findall(str(i)))
        # c = "".join(curv.findall(str(i)))
        sl1.append(s[5:8])
        # cu.append(c[5:8])
    for i in lir2:
        s = "".join(slop.findall(str(i)))
        # c = "".join(curv.findall(str(i)))
        sl2.append(s[5:8])
        # cu.append(c[5:8])
    len1 = len(sl1)
    len2 = len(sl2)
    points_num = 100
    times = int(len(sl1) / points_num) + 1
    for i in range(times):
        s, e = i * points_num, (i + 1) * points_num
        draw(sl1[s:e], sl2[s:e])


def draw(sl1, sl2):
    plt.title('slop')
    # 获取每个slop组的长度作为x轴
    x1 = len(sl1)
    x2 = len(sl2)
    lis_x1 = range(x1)
    lis_x2 = range(x2)
    plt.plot(lis_x1, sl1, 'r', label=u'can', linewidth=6)
    plt.plot(lis_x2, sl2, 'black', label=u'pc', linewidth=3)
    plt.legend()
    plt.show()


if __name__ == '__main__':
    read_data(can_qian, pc_qian)
