import shutil
import os
from defi import Av2_Output

matchpt = Av2_Output + "\\matchpt.txt"
matchpt_last = Av2_Output + "\\matchpt.csv"
gcj = Av2_Output + "\\gcj1.txt"
gcj_last = Av2_Output + "\\gcj.csv"



# 判断日志文件是否存在
def detect_file_exist(path_log):
    gcj_flag = False
    matchpt_flag = False
    lists = os.listdir(path_log)
    for i in lists:
        if 'gcj.txt' in str(i) and not gcj_flag:
            gcj_flag = True
        if 'matchpt.txt' in str(i) and not matchpt_flag:
            matchpt_flag = True
        if gcj_flag and matchpt_flag:
            break
    if gcj_flag and matchpt_flag:
        return True
    else:
        return False

# 深度搜索指定目录下的文件
def pyscandirs(path, strrrrr):
    folders = []
    global result, flag
    for entry in os.scandir(path):
        if entry.is_dir() and not entry.name.startswith('$'):
            folders.append(entry.path)
    for folder in folders:
        # print(folder)
        if str(folder).endswith(strrrrr) and folders and not flag:
            result += folder
            flag = True
        pyscandirs(folder, strrrrr)
    return result

# 将处理过后的gcj日志文件复制到指定目录中
def copy_gcj():
    str1 = 'DataBaseInspector'
    result = pyscandirs('D:\\Test', str1)
    if result:
        os.rename(gcj, gcj_last)
        shutil.copyfile(gcj_last, result)

# 将处理过后的gcj日志文件复制到指定目录中
def copy_matchpt():
    str1 = 'DataBaseInspector'
    result = pyscandirs('D:\\Test', str1)
    if result:
        os.rename(matchpt, matchpt_last)
        shutil.copyfile(matchpt_last, result)
