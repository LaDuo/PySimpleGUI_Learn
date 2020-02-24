from defi import stub_path
from defi import stub_path_id
from defi import stub_offset
from defi import stub_last
from defi import Err_Stub_ofs
from tkinter.messagebox import showerror, showinfo
import re



# 验证stub日志
def JudgeStub():
    flag = 0
    lir2 = []
    try:
        with open(stub_path, 'r', encoding="utf-8") as file:
            lir = file.readlines()
        flag = 1
    except FileNotFoundError:
        showerror(title="Warning!", message=" <stub.txt> File not found")
    if flag == 1:
        for i in range(len(lir)):
            if i == len(lir) - 1:
                break
            j = i + 1
            id1 = stub_path_id.findall(lir[i])
            id2 = stub_path_id.findall(lir[j])
            ofs1 = str(stub_offset.findall(lir[i]))
            ofs2 = str(stub_offset.findall(lir[j]))
            ofs1 = int(re.sub(r'\D', "", ofs1))
            ofs2 = int(re.sub(r'\D', "", ofs2))
            last1 = stub_last.findall(lir[i])
            last2 = stub_last.findall(lir[j])
            if id1 == id2:
                if ofs1 == ofs2:
                    if last1 == "true":
                        lir2.append("last1==true -->" + lir[i])
                        lir2.append("last1==true -->" + lir[j])
                elif ofs1 < ofs2:
                    if last1 == "false":
                        lir2.append("last1==false-->" + lir[i])
                        lir2.append("last1==false-->" + lir[j])
                else:
                    if ofs1 >= 7000:
                        continue
                    else:
                        lir2.append("ofs1 > ofs2 -->" + lir[i])
                        lir2.append("ofs1 > ofs2 -->" + lir[j])
        count = 0
        # 每组问题
        with open(Err_Stub_ofs, 'w', encoding="utf-8") as f:
            for n in range(len(lir2)):
                f.write(lir2[n])
                count += 1
                if count == 2:
                    count = 0
                    f.write("======================\n")
        showinfo(title="提示", message="judge stub offset Successful!")
