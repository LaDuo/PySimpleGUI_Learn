import os
import re
import threading
from tkinter.messagebox import showinfo, showwarning, showerror
from tkinter import Tk
from tkinter import Frame, StringVar
from tkinter import END, Label, Entry, Button, Text, Menu
import shutil
import time
import matplotlib.pyplot as plt
from datetime import datetime

# from subprocess import Popen, PIPE, STDOUT


# 此文件用于添加定义、变量
Desktop = os.path.join(os.path.expanduser('~'), "Desktop")
Av2_log = Desktop + "\\Av2_Output\\outfile.txt"
Av2_Input = Desktop + "\\Av2_Input"
Av2_Output = Desktop + "\\Av2_Output"
Analyze = Desktop + "\\Analyze"
ALL = os.path.join(Analyze, 'ALL')
dis = 8191
# --------------------------------------------------------
base_path1 = "D:\\test\\Release\\log\\"  # Av2数据所在路径     重点关注   Av2数据路径需要根据电脑配置更改
# --------------------------------------------------------
global model

# MSG ERR Path
Err_Position = os.path.join(Av2_Output, "Err_Pos.txt")  # 打印Av2Log中的Position的offset异常
Err_Stub_ofs = os.path.join(Av2_Output, "Err_Stub_ofs.txt")
Err_Stub_send = os.path.join(Av2_Output, "Err_Stub_send.txt")
Err_Segment = os.path.join(Av2_Output, "Err_Segment.txt")
Err_cyclic = os.path.join(Av2_Output, "Err_cyclic.txt")
cyclic_pos = os.path.join(Av2_Output, "cyclic_pos.txt")
cyclic_stub = os.path.join(Av2_Output, "cyclic_stub.txt")
cyclic_seg = os.path.join(Av2_Output, "cyclic_seg.txt")
cyclic_prl1 = os.path.join(Av2_Output, "cyclic_prl1.txt")
cyclic_prl2 = os.path.join(Av2_Output, "cyclic_prl2.txt")
cyclic_prl9 = os.path.join(Av2_Output, "cyclic_prl9.txt")
cyclic_prs1 = os.path.join(Av2_Output, "cyclic_prs1.txt")
cyclic_prs4 = os.path.join(Av2_Output, "cyclic_prs4.txt")
cyclic_meta = os.path.join(Av2_Output, "cyclic_meta.txt")

# MSG path
stub_position = os.path.join(Av2_Output, "sub&position.txt")
stub_path = os.path.join(Av2_Output, "stub.txt")
meta_path = os.path.join(Av2_Output, "meta.txt")
seg_path = os.path.join(Av2_Output, "seg.txt")
pos_path = os.path.join(Av2_Output, "pos.txt")
prl1_path = os.path.join(Av2_Output, "prl1.txt")
prl2_path = os.path.join(Av2_Output, "prl2.txt")
prl7_path = os.path.join(Av2_Output, "prl7.txt")
prl9_path = os.path.join(Av2_Output, "prl9.txt")
prs1_path = os.path.join(Av2_Output, "prs1.txt")
prs4_path = os.path.join(Av2_Output, "prs4.txt")
pos_stub_path = os.path.join(Av2_Output, "pos_stub.txt")
slope_path = os.path.join(Av2_Output, "slope.txt")
curv_path = os.path.join(Av2_Output, "prs1.txt")
pos_seg_path = os.path.join(Av2_Output, "pos_seg.txt")
gcj_Inspector = "D:\\test\\old_dateBase\\DatabaseInspector\\gcj.csv"
match_Inspector = "D:\\test\\old_dateBase\\DatabaseInspector\\match.csv"

list_ehp = []
list_ada = []
list_loc = []
Err = []
listtt = []

list_items = [1, 2, 3, 4]

pattern_time = re.compile(r'\d+-\d+ \d+:\d+:\d+\.\d+')
pattern_ofs = re.compile(r'ofs=\d+,')
pattern_path = re.compile(r'path=\d+,')
pattern_speed = re.compile(r'speed=\d+,')
pat_stub = re.compile(r'Stub: path=0,')
pat_Stub = re.compile(r'Stub: path=\d+')
pat_sub = re.compile(r'subPath=\d+')
pat_Pos = re.compile(r'Position: path=\d+')
pat_Pro_Long1 = re.compile(r'Profile Long: type=1')
pat_Pro_Long2 = re.compile(r'Profile Long: type=2')
pat_Pro_Long7 = re.compile(r'Profile Long: type=7')
pat_Pro_Long9 = re.compile(r'Profile Long: type=9')
pat_Pro_Sht1 = re.compile(r'Profile Short: type=1')
pat_Pro_Sht4 = re.compile(r'Profile Short: type=4')
pat_Meta = re.compile(r'Metadata')
pat_Seg = re.compile(r'Segment: ')
pat_time = re.compile(r'\d+-\d+ \d+:\d+:\d+\.\d+')
po = re.compile(r'path=\d+')
short = re.compile(r'Profile Short: type=4')
av_slope_v = re.compile(r'value=\d+')
av_slope_v1 = re.compile(r'value1=\d+')
eh_slope_v = re.compile(r'v0:\s\d{3}')
eh_slope_v1 = re.compile(r'v1:\s\d{3}')

# stub message RE
stub_path_id = re.compile(r'path=\d+')
stub_offset = re.compile(r'ofs=\d+')
stub_last = re.compile(r'isLastStubAtOffset=\w+')
offroad = "['Position: path=2']"

# segment message RE
seg_path_id = re.compile(r'path=\d+')
seg_offset = re.compile(r'ofs=\d+')
seg_bridge = re.compile(r'isBridge=av2_true')
cyclic = re.compile(r'cyclic=\d')

# InfluxDB
data_route = "D:\\test\\InfluxDBdata"

# profile short slope
slope_path_id = re.compile(r'path=\d+')
slope_value = re.compile(r'value=\d+')
slope_value1 = re.compile(r'value1=\d+')
slope_ofs = re.compile(r'offs=\d+')
slope_dis = re.compile(r'distance1=\d+')
