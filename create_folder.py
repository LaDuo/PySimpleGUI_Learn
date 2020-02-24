from subprocess import Popen, PIPE, STDOUT
import os
from datetime import datetime
import shutil
from defi import Analyze, Desktop, base_path1, Av2_Input, Av2_Output
from defi import Desktop
from defi import base_path1
from defi import Av2_Input
from defi import Av2_Output
from tkinter.messagebox import showinfo


def CreateMoveMerge(map_name, base_path):
    base_path1 = base_path
    # print(base_path1)
    # 创建根目录
    try:
        if not os.path.exists(Analyze):
            os.mkdir(Analyze)
            print("创建成功")
    except FileExistsError:
        print("目录已存在")
    # 创建子文件夹
    print("正在创建子文件夹")
    str1 = os.path.join(Analyze, datetime.now().strftime("%Y-%m-%d-")) + map_name
    os.makedirs(str1)
    os.mkdir(os.path.join(str1, "Av2"))
    os.mkdir(os.path.join(str1, "EHPLOG"))
    os.mkdir(os.path.join(str1, "CONFIG"))
    # print("Create folders successful")
    print("正在复制Av2log到Analyze文件夹和Av2_Input文件夹中")
    # 将Av2Simulator中的Log复制一份至Analyze文件夹和Av2_Input文件夹中
    base_path2 = Desktop + "\\Av2_Input\\"
    base_path3 = Desktop + "\\Analyze\\" + \
                 datetime.now().strftime("%Y-%m-%d-") + map_name + "\\Av2"
    alllist = os.listdir(base_path1)
    for i in alllist:
        if "_Av2数据" in i:
            oldname = os.path.join(base_path1, i)
            newname1 = os.path.join(base_path2, i)
            newname2 = os.path.join(base_path3, i)
            shutil.copyfile(oldname, newname1)  # 拷贝到Av2_Input文件夹
            shutil.copyfile(oldname, newname2)  # 拷贝到Analyze文件夹
    # 将桌面上的Av2_Input文件夹中的Av2 Log合并放置在Av2_Output文件夹中的outfile.txt中
    print("正在合并生成outfile.txt")
    files = os.listdir(Av2_Input)
    res = ""
    i = 1
    for file in files:
        if file.endswith(".txt"):
            i += 1
            title = "第%s章 %s" % (i, file[0:len(file) - 4])
            with open(Av2_Input + "\\" + file, "r", encoding='utf-8') as file:
                content = file.read()
                file.close()
            append = "\n%s\n\n%s" % (title, content)
            res += append
    dirPath_out = Av2_Output
    if not os.path.exists(dirPath_out):
        os.mkdir(dirPath_out)
    with open(dirPath_out + "\\outfile.txt", "w", encoding='utf-8') as outFile:
        outFile.write(res)
    # ----------------------------------------------------------------
    # 删除Av2Simulator中的Log文件夹中的内容
    print("正在删除Avlog")
    for j in alllist:
        if ".txt" in j:
            path = os.path.join(base_path1, j)
            os.remove(path)
    # ---------------------------------------------------------------------
    # 压缩文件
    # print("正在压缩Avlog")
    # zip_name = base_path3 + '.zip'
    # z = zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED)
    # for dirpath, dirnames, filenames in os.walk(base_path3):
    #     fpath = dirpath.replace(base_path3, '')
    #     fpath = fpath and fpath + os.sep or ''
    #     for filename in filenames:
    #         z.write(os.path.join(dirpath, filename), fpath + filename)
    # z.close()
    # ---------------------------------------------------------------------
    print("正在下载EHPLOG")
    os.chdir(Desktop)  # 自动下载EHPLOG至Analyze目录下的ALL文件夹中
    p = Popen("cmd.exe /c" + Desktop + "\\downEhp.bat", stdout=PIPE, stderr=STDOUT)
    curline = p.stdout.readline()
    while curline != b'':
        print(curline)
        curline = p.stdout.readline()
    p.wait()
    print(p.returncode)
    print("正在转移EHPLOG")
    # ---------------------------------------------------------------
    # 将Analyze目录中的ALL文件夹中的所有文件拷贝至新建的回放路线文件夹中
    src = Analyze + "\\ALL"
    dst = str1 + "\\EHPLOG"
    ALL_list = os.listdir(src)
    for i in ALL_list:
        n1 = os.path.join(src, i)
        shutil.move(n1, dst)
    # ---------------------------------------------------------------
    print("正在下载conf")
    os.chdir(Desktop) 
    # 自动下载conf至Analyze目录下的ALL文件夹中
    p = Popen("cmd.exe /c" + Desktop + "\\downconf.bat", stdout=PIPE, stderr=STDOUT)
    curline = p.stdout.readline()
    while curline != b'':
        print(curline)
        curline = p.stdout.readline()
    p.wait()
    print(p.returncode)
    print("正在转移conf")
    # ---------------------------------------------------------------
    # 将Analyze目录中的ALL文件夹中的所有文件拷贝至新建的回放路线文件夹中
    src = Analyze + "\\ALL"
    dst = str1 + "\\CONFIG"
    ALL_list = os.listdir(src)
    for i in ALL_list:
        n1 = os.path.join(src, i)
        shutil.move(n1, dst)
    showinfo(title="Create Move Download Merge", message="Success！")
