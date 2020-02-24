from defi import pos_stub_path
from defi import Err_Stub_send
from defi import pat_Pos
from defi import pat_stub
from defi import offroad
from tkinter.messagebox import showinfo





# 验证stub是否发送
def Send_Stub():
    count = 0
    with open(pos_stub_path, 'r', encoding='utf-8') as f:
        LogList = f.readlines()
    with open(Err_Stub_send, 'w', encoding="utf-8") as file:
        for i in range(len(LogList)):
            if i == len(LogList) - 2:
                break
            j = i + 2
            k = i + 1
            # print("j = ", j, "k = ", k)
            pos1 = str(pat_Pos.findall(LogList[i]))
            pos2 = str(pat_Pos.findall(LogList[j]))
            stub = str(pat_stub.findall(LogList[k]))
            # print(type(pos1), type(offroad))
            if pos1 != "[]" and pos2 != "[]" and pos1 != offroad and pos1 != pos2:
                if stub == "[]":
                    file.write(LogList[k])
                    file.write("\n")
                    count += 1
                if count % 2 == 0:
                    file.write("\n")
    showinfo(title="Detect Stub MSG", message="检测完成")
