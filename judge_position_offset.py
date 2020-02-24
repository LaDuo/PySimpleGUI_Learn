import re
from tkinter.messagebox import showwarning, showinfo
from defi import pos_path, pattern_ofs, pattern_path, Err, Err_Position
import os.path

def JudgePosition():
    if os.path.exists(pos_path):
        flag = 0
        try:
            with open(pos_path, 'r', encoding="utf-8") as file:
                tmp = file.readlines()
            flag = 1
        except FileNotFoundError:
            showwarning(title="Warning", message=" <pos.txt>  File not found")
        if flag == 1:
            for i in range(len(tmp)):
                if i == len(tmp) - 1:
                    break
                j = i + 1
                ofs1 = str(pattern_ofs.findall(tmp[i]))
                ofs2 = str(pattern_ofs.findall(tmp[j]))
                path1 = str(pattern_path.findall(tmp[i]))
                path2 = str(pattern_path.findall(tmp[j]))
                ofs1 = int(re.sub(r'\D', "", ofs1))
                ofs2 = int(re.sub(r'\D', "", ofs2))
                path1 = int(re.sub(r'\D', "", path1))
                path2 = int(re.sub(r'\D', "", path2))
                # 相同path id情况下，offset递增，反之打印（忽略path id不同的情况）
                if path1 == 0:
                    continue
                if (path1 == path2) and (ofs2 >= ofs1):
                    continue
                elif (path1 == path2) and (ofs2 < ofs1):
                    Err.append(str(tmp[i]))
                    Err.append(str(tmp[j]))
                    Err.append('\n')
            with open(Err_Position, 'w', encoding="utf-8") as file:
                for i in range(len(Err)):
                    file.write(str(Err[i]))
                    file.write("\n")
            # showinfo(title="提示", message="judge position offset Successful！")
        return True
    else:
        return False
