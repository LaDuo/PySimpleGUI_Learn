from defi import Desktop
from defi import Av2_Input
from defi import Av2_Output
from defi import Analyze
from defi import base_path1
from defi import ALL
from tkinter.messagebox import showinfo
from tkinter.messagebox import showerror
import sys
# This module is used for Unix Testing
import argparse
from datetime import datetime
import threading
import PySimpleGUI as sg
import os
import move_log
import create_folder
import get_six_msg
import judge_Frame_lose
import judge_position_offset
import judge_segment_msg
import judge_stub_offset
import judge_stub_send
import merge_av2_log
import merge_ehplog_info
import Issue_report
import delete_logs
import show_slope
import show_curv
import set_env
import copy_gcj_matchpt
import judge_Get2_clicked
# import gps_kml
import loganal


def ps():
    print('Hello World')


if __name__ == "__main__":
    if 'win' in sys.platform:
        sg.change_look_and_feel("GreenTan")

        # ---------- Menu Definition ----------- #
        menu_def = [['File', ['Change Log', 'Save', 'Propertes', 'Exit']],
                    ['Features', ['Pase', ['Special', 'Normal', ], 'Undo']],
                    ['Help', 'About...']
                    ]
        # ------------------------- 操作 log --------------------------- #
        frame1_layout = [
            [sg.Text("将Av2_Input文件夹中的log合并至Av2_Output", auto_size_text=True),
             sg.Button(button_text="Get1", button_color=('black', 'blue'), pad=(20, 3), size=(10, 1))],
            [sg.Text("从outfile.txt中提取六种消息", auto_size_text=True),
             sg.Button(button_text="Get2", button_color=('black', 'blue'), pad=(120, 3), size=(10, 1))],
            [sg.Text("将Ehplog中的ehp和loca的INFO文件合并", auto_size_text=True),
             sg.Button(button_text="Get3", button_color=('black', 'blue'), size=(10, 1), pad=(45, 3))],
            [sg.Text("提取matchpt和gcj", auto_size_text=True),
             sg.Button(button_text="Get4", button_color=('black', 'blue'), pad=(175, 3), size=(10, 1))],
        ]
        # ------------------------- 判断 log --------------------------- #
        frame2_layout = [
            [sg.Text("判断position消息的offset是否递增", auto_size_text=True),
             sg.Button(button_text="Get5", button_color=('black', 'blue'), pad=(80, 3), size=(10, 1))],
            [sg.Text("判断stub消息的offset是否递增", auto_size_text=True),
             sg.Button(button_text="Get6", button_color=('black', 'blue'), pad=(100, 3), size=(10, 1))],
            [sg.Text("判断stub消息在重构时是否发送", auto_size_text=True),
             sg.Button(button_text="Get7", button_color=('black', 'blue'), pad=(93, 3), size=(10, 1))],
            [sg.Text("判断segment消息是否重发", auto_size_text=True),
             sg.Button(button_text="Get8", button_color=('black', 'blue'), pad=(120, 3), size=(10, 1))],
            [sg.Text("判断各个消息是否丢包", auto_size_text=True),
             sg.Button(button_text="Get9", button_color=('black', 'blue'), pad=(144, 3), size=(10, 1))]
        ]
        # ------------------------- Action ---------------------------- #
        frame3_layout = [
            [sg.T("Some ohter action ", auto_size_text=True)],
            [sg.Text("生成Issue状态报表", auto_size_text=True),
             sg.Button(button_text="Do it", button_color=('black', 'blue'), pad=(173, 3), size=(10, 1))],
            [sg.Text("删除无用的log", auto_size_text=True)],
            [sg.CB('Release log'), sg.CB('Input log'), sg.CB('Output log'),
             sg.Button(button_text="Delete it", button_color=('black', 'blue'), pad=(7, 3), size=(10, 1))],
            [sg.Text("按照offset和path id的规则来显示slope", auto_size_text=True)],
            [sg.Radio("mode 2", 'RADIO1', default=True), sg.Radio("mode 3", 'RADIO1'),
             sg.Button(button_text="Show it", button_color=('black', 'blue'), pad=(135, 3), size=(10, 1)),
             sg.Button(button_text='Close show', button_color=('black', 'blue'), size=(10, 1))],
        ]

        # -------------------------- main layout ---------------------- #
        layout = [
            [sg.Menu(menu_def, tearoff=True)],
            [sg.Text('请输入即将创建的日志文件名 :', auto_size_text=True), sg.InputText(key='-IN-'),
             sg.Button(button_text="创建文件夹", button_color=('black', 'blue'), size=(10, 1)),
             sg.Button(button_text='环境检测', button_color=('black', 'red'), size=(25, 1)),
             sg.Button(button_text='环境设置', button_color=('black', 'yellow'), size=(10, 1))],
            [sg.Frame('操作 Log', frame1_layout, font='Any 12', title_color='blue', title_location='n'),
             sg.Frame('判断 Log', frame2_layout, font='Any 12', title_color='blue', title_location='n')],
            [sg.Frame("Action", frame3_layout, font='Any 12', title_color='blue', title_location='n')]
        ]

        window = sg.Window('Testing Tool', layout, default_element_size=(40, 1), grab_anywhere=False)
        window2_active = False

        # -------------------------- Call back ----------------------- #

        while True:
            # ------------------------------ 使用时间 -----------------------
            disk = os.scandir('D:')

            # --------------------------------------------------------------
            event, values = window.read()
            if event in (None, 'Exit'):
                break
            if event in 'Special':
                main_flag = False

            # ---------------------------环境检测-----------------------------------------------------
            if event in '环境检测':
                input_flag, output_flag, analyze_flag, base_flag = True, True, True, True
                strrr = ''
                if os.path.isdir(Av2_Input) and os.path.isdir(Av2_Output) \
                        and os.path.isdir(Analyze) and os.path.isdir(base_path1):
                    sg.Popup('环境检测成功，可以使用,并确保以及连接远程服务器', title='Successful')
                if not os.path.isdir(Av2_Input):
                    input_flag = False
                if not os.path.isdir(Av2_Output):
                    output_flag = False
                if not os.path.isdir(Analyze):
                    analyze_flag = False
                if not os.path.isdir(base_path1):
                    base_flag = False
                if input_flag is False:
                    strrr += 'Av2_Input'
                    strrr += '、'
                if output_flag is False:
                    strrr += 'Av2_Output'
                    strrr += '、'
                if analyze_flag is False:
                    strrr += 'Analyze'
                    strrr += '、'
                if base_flag is False:
                    strrr += 'Release Log'
                    strrr += '、'
                # print('strrr = ', strrr)
                if strrr is not '':
                    showerror(title='Failed', message='文件缺失错误，缺少以下：{}文件'.format(strrr))
            # ------------------------------------环境设置--------------------------------------------
            if event in '环境设置' and not window2_active:
                window2_active = True
                layout1 = [[sg.Text('请选择Release Log的路径'), sg.InputText(), sg.Button('Browse Folder')],
                           [sg.Button(button_text='确认')]]
                window2 = sg.Window('Win2', layout1)
            if window2_active:
                while True:
                    ev2, vals2 = window2.read()
                    filename = ''
                    if ev2 == 'Browse Folder':
                        filename = sg.PopupGetFolder(message='选择文件夹', default_path=Desktop, initial_folder=Desktop,
                                                     no_window=True)
                        print(type(filename))
                    elif ev2 in (None, '确认'):
                        ret = set_env.env_set()
                        if ret:
                            sg.Popup('设置成功', title='Successful', auto_close=True, auto_close_duration=2)
                        window2_active = False
                        if filename:
                            base_path1 = filename
                        # print('-------------:', base_path1)
                        break
                window2.close()
            # -------------------------------------创建文件夹--------------------------------------
            if event in '创建文件夹':
                file_exist = True
                rets = set_env.detect_env()
                if rets:
                    sg.Popup('缺少目录，请进行环境检测', title='提示')
                    continue
                if not values['-IN-']:
                    sg.Popup('请输入需要创建的日志文件名', title='提示')
                else:
                    map_name = values['-IN-']
                    str1 = datetime.now().strftime("%Y-%m-%d-") + map_name
                    for i in os.listdir(Analyze):
                        if str1 == str(i):
                            sg.Popup('重复命名', title='Warning')
                            file_exist = False
                            break
                    if file_exist is True:
                        create_folder.CreateMoveMerge(map_name, base_path1)
            # ----------------------------------- Menu -------------------------------------
            if event in 'Change Log':
                filename = sg.PopupGetFolder(title="Choose your file", message="请选择文件",
                                             default_path=Desktop,
                                             initial_folder=Desktop,
                                             no_window=True)

                if filename is not None:
                    move_log.delete_log(Av2_Input)
                    move_log.move_txt(filename)
                    # print('I am moving')
            if event in 'Save':
                sg.Popup('功能暂未开发', title='提示')
            if event in 'Propertes':
                sg.Popup('功能暂未开发', title='提示')
            if event in 'Undo':
                sg.Popup('未开发功能如下：'
                         '1、提取matchpt和gcj', title='Undo', auto_close=True, auto_close_duration=3)
            if event in 'Special':
                # sg.Popup('功能暂未开发', title='Special', auto_close=True, auto_close_duration=3)
                # path1 = Desktop + "\\a.csv"
                # gps_kml.csvtokml('test', Desktop, path1)
                sg.Popup('GPS转换为kml不成功', title='提示')
            if event in 'Normal':
                sg.Popup('功能暂未开发', title='Normal', auto_close=True, auto_close_duration=3)
            # ----------------------------------- Get1 --------------------------------------
            if event in 'Get1':
                if merge_av2_log.AvLog() is True:
                    showinfo(title='Success', message='merge Av2 log Successful!')
                else:
                    showerror(title='File not found', message='\n'
                                                              '请确认Av2_Input文件夹中存在日志')
            # ----------------------------------- Get2 --------------------------------------
            elif event in 'Get2':
                if get_six_msg.Sep_MSG():
                    showinfo(title='Success', message='Get six message Successful!')
                else:
                    showerror(title='File not found', message='未找到Av2_Output文件夹中的日志outfile.txt')
            # ----------------------------------- Get3 --------------------------------------
            elif event in 'Get3':
                map_name = values['-IN-']
                if not map_name:
                    showinfo(title='提示', message='请输入文件名')
                    continue
                if merge_ehplog_info.merge_info(map_name) is True:
                    ehplogs = os.listdir()
                    if 'adasis_INFO.txt' in ehplogs and 'ehp_INFO.txt' in ehplogs and 'localization_INFO.txt' in ehplogs:
                        showinfo(title='merge Ehplog INFO', message='merge ehplog info Successful!')
            # ----------------------------------- Get4 --------------------------------------
            elif event in 'Get4':
                result = copy_gcj_matchpt.detect_file_exist(Av2_Output)
                if result:
                    copy_gcj_matchpt.copy_gcj()
                    copy_gcj_matchpt.copy_matchpt()
                else:
                    sg.Popup("You didn't create a 'gcj.txt' and a 'matchpt.txt', Please click the 'Get 3' Button to get"
                             "the 'gcj.txt' and 'matchpt.txt'.")
            # ----------------------------------- Get5 --------------------------------------
            elif event in 'Get5':
                if judge_position_offset.JudgePosition():
                    showinfo(title='Success', message='Judge pos.txt completely!')
                else:
                    showerror(title='File not found', message='未找到Av2_Output文件夹中的日志pos.txt, 请点击 "Get 2"')
            # ----------------------------------- Get6 --------------------------------------
            elif event in 'Get6':
                pat_stub = 'stub.txt'
                rst = judge_Get2_clicked.detect_file_exist()
                if pat_stub not in rst:
                    judge_stub_offset.JudgeStub()
                else:
                    play = '没有在Av2_Output中找到如下{}文件'.format(pat_stub)
                    sg.Popup(play, title='Warning')
            # ----------------------------------- Get7 --------------------------------------
            elif event in 'Get7':
                pat_stub_send = 'pos_stub.txt'
                rst = judge_Get2_clicked.detect_file_exist()
                if pat_stub_send not in rst:
                    judge_stub_send.Send_Stub()
                else:
                    play = '没有在Av2_Output中找到如下{}文件'.format(pat_stub_send)
                    sg.Popup(play, title='Warning')
            # ----------------------------------- Get8 --------------------------------------
            elif event in 'Get8':
                pat_seg = 'seg.txt'
                rst = judge_Get2_clicked.detect_file_exist()
                if pat_seg not in rst:
                    judge_segment_msg.JudgeSegment()
                else:
                    play = '没有在Av2_Output中找到如下{}文件'.format(pat_seg)
                    sg.Popup(play, title='Warning')
            # ----------------------------------- Get9 --------------------------------------
            elif event in 'Get9':
                rst = judge_Get2_clicked.detect_file_exist()
                print(rst)
                # print(rst)
                if 'meta.txt' in rst or 'pos.txt' in rst or 'prl1.txt' in rst \
                        or 'prl2.txt' in rst or 'prl9.txt' in rst or 'prs1.txt' in rst \
                        or 'prs4.txt' in rst or 'seg.txt' in rst or 'stub.txt' in rst:
                    sg.Popup('缺少文件，请重新点击 "Get 2" 按钮', title='提示')
                else:
                    judge_Frame_lose.Cyclic()
            # ----------------------------------- Do it --------------------------------------
            elif event in 'Do it':
                if Issue_report.make_issue_report():
                    sg.Popup('文件生成路径：桌面')
                else:
                    sg.Popup('配置出错，请确认账号或密码正确', title='提示')
            # ----------------------------------- Delete it-----------------------------------
            elif event in 'Delete it':
                if values[1]:
                    if delete_logs.DeleteReLog():
                        sg.Popup('成功删除', title='Successful')
                    else:
                        sg.Popup('文件已删除或文件夹为空', title='Hint')
                elif values[2]:
                    if delete_logs.DeleteInputLog():
                        sg.Popup('成功删除', title='Successful')
                    else:
                        sg.Popup('文件已删除或文件夹为空', title='Hint')
                elif values[3]:
                    if delete_logs.DeleteOutputLog():
                        sg.Popup('成功删除', title='Successful')
                    else:
                        sg.Popup('文件已删除或文件夹为空', title='Hint')
            # ----------------------------------- Show it------------------------------------
            elif event in 'Show it':
                if values[4]:
                    # 备份发送
                    # show_thread = threading.Thread(target=show_slope.ROBUSNESS, args=())
                    # show_thread.start()
                    show_slope.ROBUSNESS()
                elif values[5]:
                    # 一次发送两个
                    # show_thread = threading.Thread(target=show_slope.BANDWIDTH, args=())
                    # show_thread.start()
                    show_slope.BANDWIDTH()
            # -------------------------------- Close show ------------------------------------
            elif event in 'Close show':
                # show_thread = threading.Thread(target=show_slope.close_show, args=())
                print("nothing")
            # ----------------------------------- About --------------------------------------
            if event in 'About...':
                sg.Popup(
                    "Hello, Welcome to use this test tool, I'm so sorry to tell you,that Now, we don't have more date "
                    "about "
                    "this test tool, because I didn't complete this tool, if I do it completely, I will write the way "
                    "to use "
                    "this here", text_color="black",
                    title="关于", background_color="white",
                )

        window.close()
        # print(base_path1)
    # 如果是Unix环境，则可以通过无界面方式来验证日志，该功能尚未开发完毕
    else:
        # 调用loganal.py中的函数进行验证日志
        sg.Popup('Unix Testing tool will be developed after a while')
