import os
from tkinter.messagebox import showinfo
from defi import Desktop
from defi import Av2_log
from defi import Av2_Input


# Desktop = os.path.join(os.path.expanduser('~'), "Desktop")
# Av2_log = Desktop + "\\Av2_Output\\outfile.txt"
# Av2_Input = Desktop + "\\Av2_Input"


# 将桌面上的Av2_Input文件夹中的Av2 Log合并放置在Av2_Output文件夹中的outfile.txt中
def AvLog():
    files = os.listdir(Av2_Input)
    files.sort(key=lambda x: int(x[-12:-10]))
    # print(files)
    res = ""
    i = 1
    flag = True
    if not files:
        return False
    else:
        for file in files:
            if file.endswith(".txt"):
                i += 1
                print("file = ", file)
                title = "第%s章 %s" % (i, file[0:len(file) - 4])
                with open(Av2_Input + "\\" + file, "r", encoding='utf-8') as file:
                    content = file.read()
                append = "\n%s\n\n%s" % (title, content)
                res += append
            else:
                flag = False
                print("No file")
                break
        with open(Av2_log, "w", encoding='utf-8') as outFile:
            outFile.write(res)
    if flag is True:
        return True
    # showinfo(title="合并Av Log到outfile文件！", message="合并成功！")


if __name__ == '__main__':
    AvLog()
