import threading
import tkinter
import os
import numpy as np
import tkinter.messagebox
import calendar
import tkinter.font as tkFont

from FTP_Connect import ftp_connect_fnc

window_sx = 100
window_sy = 100
window_width = 845
window_height = 550

connect_frame_sx = 15
connect_frame_sy = 15
connect_frame_width = 260
connect_frame_height = 110

control_frame_sx = 290
control_frame_sy = 15
control_frame_width = 540
control_frame_height = 110

list_frame_sx = 550
list_frame_sy = 135
list_frame_width = 280
list_frame_height = 400

graph_frame_sx = 15
graph_frame_sy = 135
graph_frame_width = 525
graph_frame_height = 400

list_select_num = -1
cur_win_width = 519
cur_win_height = 374


def temporary_folder_fnc():
    # FTP server data file download folder management
    cwd_path = os.getcwd()
    temp_path = os.path.join(cwd_path, 'temporary')

    if not os.path.isdir(temp_path):
        os.mkdir(temp_path)
    else:
        temp_list = os.listdir(temp_path)
        temp_list_num = len(temp_list)
        if temp_list_num > 0:
            for temp_n in range(0, temp_list_num):
                temp_list_path = os.path.join(temp_path, temp_list[temp_n])
                os.remove(temp_list_path)

    return temp_path


def display_data_fnc(mode, temp_path, s_time, e_time):
    # Total data file list Generation
    n, s_d = divmod(s_time, 100)
    s_y, s_m = divmod(n, 100)

    n, e_d = divmod(e_time, 100)
    e_y, e_m = divmod(n, 100)

    data_range_list = np.empty((1, 3), dtype=int)
    for cy in range(s_y, e_y + 1):
        if s_y == e_y:
            if s_m == e_m:
                cm = s_m
                for cd in range(s_d, e_d + 1):
                    new_list = np.array([[cy, cm, cd]])
                    data_range_list = np.append(data_range_list, new_list, axis=0)
            else:
                for cm in range(s_m, e_m + 1):
                    d, n = calendar.monthrange(2000 + s_y, cm)
                    if cm == s_m:
                        for cd in range(s_d, n + 1):
                            new_list = np.array([[cy, cm, cd]])
                            data_range_list = np.append(data_range_list, new_list, axis=0)
                    elif cm == e_m:
                        for cd in range(1, e_d + 1):
                            new_list = np.array([[cy, cm, cd]])
                            data_range_list = np.append(data_range_list, new_list, axis=0)
                    else:
                        for cd in range(1, n + 1):
                            new_list = np.array([[cy, cm, cd]])
                            data_range_list = np.append(data_range_list, new_list, axis=0)
        else:
            if cy == s_y:
                for cm in range(s_m, 13):
                    d, n = calendar.monthrange(2000 + s_y, cm)
                    if cm == s_m:
                        for cd in range(s_d, n + 1):
                            new_list = np.array([[cy, cm, cd]])
                            data_range_list = np.append(data_range_list, new_list, axis=0)
                    else:
                        for cd in range(1, n + 1):
                            new_list = np.array([[cy, cm, cd]])
                            data_range_list = np.append(data_range_list, new_list, axis=0)
            elif cy == e_y:
                for cm in range(1, e_m + 1):
                    d, n = calendar.monthrange(2000 + s_y, cm)
                    if cm == e_m:
                        for cd in range(1, e_d + 1):
                            new_list = np.array([[cy, cm, cd]])
                            data_range_list = np.append(data_range_list, new_list, axis=0)
                    else:
                        for cd in range(1, n + 1):
                            new_list = np.array([[cy, cm, cd]])
                            data_range_list = np.append(data_range_list, new_list, axis=0)
            else:
                for cm in range(1, 13):
                    for cd in range(1, n + 1):
                        new_list = np.array([[cy, cm, cd]])
                        data_range_list = np.append(data_range_list, new_list, axis=0)

    data_range_list = np.delete(data_range_list, [0, 0], axis=0)

    data_file_list = []
    for i in range(0, data_range_list.shape[0]):
        temp = "[Report]%04d%02d%02d.txt" % (2000 + data_range_list[i, 0], data_range_list[i, 1], data_range_list[i, 2])
        data_file_list.append(temp)

    cal_data = np.empty((1, 3), dtype=int)

    for temp_n in range(0, len(data_file_list)):
        temp_list_path = os.path.join(temp_path, data_file_list[temp_n])
        f_parts = data_file_list[temp_n]
        f_y = int(f_parts[10:12])
        f_m = int(f_parts[12:14])
        f_d = int(f_parts[14:16])

        if os.path.isfile(temp_list_path):
            with open(temp_list_path, mode="r") as file:
                cal_temp_data = np.empty((1, 3), dtype=int)
                while True:
                    read_data = file.readline()
                    if read_data:
                        read_split = read_data.split(',')
                        f_h = int(read_split[0])
                        f_m2 = int(read_split[1])
                        f_in = int(read_split[2])
                        f_out = int(read_split[3])

                        f_time = (((f_y * 100 + f_m) * 100 + f_d) * 100 + f_h) * 100 + f_m2
                        new_data = np.array([[f_time, f_in, f_out]])
                        cal_temp_data = np.append(cal_temp_data, new_data, axis=0)
                    else:
                        break
                cal_temp_data = np.delete(cal_temp_data, [0, 0], axis=0)

            cal_data = np.append(cal_data, cal_temp_data, axis=0)
        else:
            cal_temp_data = np.empty((1, 3), dtype=int)
            for ch in range(0, 25):
                for cm in range(0, 2):
                    f_h = ch
                    f_m2 = cm * 30
                    f_in = -900
                    f_out = -900

                    f_time = (((f_y * 100 + f_m) * 100 + f_d) * 100 + f_h) * 100 + f_m2
                    new_data = np.array([[f_time, f_in, f_out]])
                    cal_temp_data = np.append(cal_temp_data, new_data, axis=0)

            cal_temp_data = np.delete(cal_temp_data, [0, 0], axis=0)
            cal_data = np.append(cal_data, cal_temp_data, axis=0)

    cal_data = np.delete(cal_data, [0, 0], axis=0)

    t_data = cal_data[:, 0]

    div_num = np.power(100, mode)
    t_data_n, t_data_d = divmod(t_data, div_num)
    unique_data = np.unique(t_data_n)

    unique_data_num = len(unique_data)

    mode_cal_data = np.empty((1, 4), dtype=int)
    for i in range(0, unique_data_num):
        temp_n = np.where(t_data_n == unique_data[i])
        temp_n = np.asarray(temp_n[0])
        in_temp = cal_data[temp_n, 1]
        out_temp = cal_data[temp_n, 2]
        in_neg_temp = np.where(in_temp < 0)
        in_neg_temp = np.asarray(in_neg_temp[0])
        out_neg_temp = np.where(out_temp < 0)
        out_neg_temp = np.asarray(out_neg_temp[0])

        if in_neg_temp.size == 0:
            in_neg_state = 0
        else:
            in_neg_state = 1
            in_temp[in_neg_temp] = 0
        in_sum = np.sum(in_temp, axis=0)

        if out_neg_temp.size == 0:
            out_neg_state = 0
        else:
            out_neg_state = 1
            out_temp[out_neg_temp] = 0
        out_sum = np.sum(out_temp, axis=0)

        if in_neg_state == 1 or out_neg_state == 1:
            count_state = 1
        else:
            count_state = 0

        temp_d = np.array([[unique_data[i], in_sum, out_sum, count_state]])
        mode_cal_data = np.append(mode_cal_data, temp_d, axis=0)

    mode_cal_data = np.delete(mode_cal_data, [0, 0], axis=0)

    return mode_cal_data


class viewer_gui_control(threading.Thread):
    def __init__(self):
        # Threading Init
        threading.Thread.__init__(self)

        # Window Setup
        self.window = tkinter.Tk()
        self.window.title("Swallow Counting Software Ver0.1")
        self.window.geometry("%dx%d+%d+%d" % (window_width, window_height, window_sx, window_sy))
        self.window.resizable(True, True)

        self.window.bind("<Configure>", self.window_resize_fnc)

        self.window.protocol("WM_DELETE_WINDOW", lambda: self.window_close())

        # Display fnc Delay Time Setup
        self.delay = 30

        # Font Setup
        self.font_style = tkFont.Font(family="arial", size=9)

        # self variable define
        self.input_ip = "0.0.0.0"
        self.input_port = 0
        self.input_id = "admin"
        self.input_pwd = "admin"

        # Connect Frame Setup
        self.connect_frame = tkinter.Frame(self.window, relief="ridge", bd=2)
        self.connect_frame.place(relx=connect_frame_sx / window_width,
                                 rely=connect_frame_sy / window_height,
                                 relwidth=connect_frame_width / window_width,
                                 relheight=connect_frame_height / window_height)
        # IP Input Setup
        self.ip_label_tx = tkinter.Label(self.connect_frame, text="IP", relief="flat", anchor="e", state="disabled",
                                         disabledforeground="black", font=self.font_style)
        self.ip_label_tx.place(relx=5 / connect_frame_width, rely=10 / connect_frame_height,
                               relwidth=20 / connect_frame_width, relheight=25 / connect_frame_height)

        self.ip_entry = tkinter.Entry(self.connect_frame, relief="sunken", bg="white", justify="center",
                                      font=self.font_style)
        self.ip_entry.place(relx=35 / connect_frame_width, rely=10 / connect_frame_height,
                            relwidth=100 / connect_frame_width, relheight=25 / connect_frame_height)
        self.ip_entry.insert(0, "192.168.0.16")

        # Port Input Setup
        self.port_label_tx = tkinter.Label(self.connect_frame, text="PORT", relief="flat", anchor="e", state="disabled",
                                           disabledforeground="black", font=self.font_style)
        self.port_label_tx.place(relx=150 / connect_frame_width, rely=10 / connect_frame_height,
                                 relwidth=40 / connect_frame_width, relheight=25 / connect_frame_height)

        self.port_entry = tkinter.Entry(self.connect_frame, relief="sunken", bg="white", justify="center",
                                        font=self.font_style)
        self.port_entry.place(relx=200 / connect_frame_width, rely=10 / connect_frame_height,
                              relwidth=50 / connect_frame_width, relheight=25 / connect_frame_height)
        self.port_entry.insert(0, "30000")

        # ID Input Setup
        self.id_label_tx = tkinter.Label(self.connect_frame, text="ID", relief="flat", anchor="e", state="disabled",
                                         disabledforeground="black", font=self.font_style)
        self.id_label_tx.place(relx=5 / connect_frame_width, rely=45 / connect_frame_height,
                               relwidth=20 / connect_frame_width, relheight=25 / connect_frame_height)

        self.id_entry = tkinter.Entry(self.connect_frame, relief="sunken", bg="white", justify="center",
                                      font=self.font_style)
        self.id_entry.place(relx=35 / connect_frame_width, rely=45 / connect_frame_height,
                            relwidth=100 / connect_frame_width, relheight=25 / connect_frame_height)
        self.id_entry.insert(0, "FTP_Ecogen")

        # PWD Input Setup
        self.pwd_label_tx = tkinter.Label(self.connect_frame, text="PWD", relief="flat", anchor="e", state="disabled",
                                          disabledforeground="black", font=self.font_style)
        self.pwd_label_tx.place(relx=150 / connect_frame_width, rely=45 / connect_frame_height,
                                relwidth=40 / connect_frame_width, relheight=25 / connect_frame_height)

        self.pwd_entry = tkinter.Entry(self.connect_frame, relief="sunken", bg="white", justify="center", show="*",
                                       font=self.font_style)
        self.pwd_entry.place(relx=200 / connect_frame_width, rely=45 / connect_frame_height,
                             relwidth=50 / connect_frame_width, relheight=25 / connect_frame_height)
        self.pwd_entry.insert(0, "19411")

        # FTP Connect Button Setup
        self.connect_button = tkinter.Button(self.connect_frame, text="Connect", relief="raised", font=self.font_style)
        self.connect_button.place(relx=5 / connect_frame_width, rely=80 / connect_frame_height,
                                  relwidth=245 / connect_frame_width, relheight=25 / connect_frame_height)
        self.connect_button.configure(command=lambda: self.connect_button_callback())

        # Connect Frame Setup
        self.control_frame = tkinter.Frame(self.window, relief="ridge", bd=2)
        self.control_frame.place(relx=control_frame_sx / window_width,
                                 rely=control_frame_sy / window_height,
                                 relwidth=control_frame_width / window_width,
                                 relheight=control_frame_height / window_height)

        # Start Time Control Setup
        self.start_time_label_tx = tkinter.Label(self.control_frame, text="Start Time", relief="flat", anchor="e",
                                                 state="disabled", disabledforeground="black", font=self.font_style)
        self.start_time_label_tx.place(relx=5 / control_frame_width, rely=10 / control_frame_height,
                                       relwidth=70 / control_frame_width, relheight=25 / control_frame_height)

        self.start_year_entry = tkinter.Entry(self.control_frame, relief="sunken", bg="white", justify="center"
                                              , state="disabled", font=self.font_style)
        self.start_year_entry.place(relx=85 / control_frame_width, rely=10 / control_frame_height,
                                    relwidth=60 / control_frame_width, relheight=25 / control_frame_height)
        self.start_year_entry.insert(0, "2020")

        self.start_year_label_tx = tkinter.Label(self.control_frame, text="Year", relief="flat", anchor="w",
                                                 state="disabled", disabledforeground="black", font=self.font_style)
        self.start_year_label_tx.place(relx=145 / control_frame_width, rely=10 / control_frame_height,
                                       relwidth=30 / control_frame_width, relheight=25 / control_frame_height)

        self.start_month_entry = tkinter.Entry(self.control_frame, relief="sunken", bg="white", justify="center"
                                               , state="disabled", font=self.font_style)
        self.start_month_entry.place(relx=190 / control_frame_width, rely=10 / control_frame_height,
                                     relwidth=60 / control_frame_width, relheight=25 / control_frame_height)
        self.start_month_entry.insert(0, "8")

        self.start_month_label_tx = tkinter.Label(self.control_frame, text="Month", relief="flat", anchor="w",
                                                  state="disabled", disabledforeground="black", font=self.font_style)
        self.start_month_label_tx.place(relx=250 / control_frame_width, rely=10 / control_frame_height,
                                        relwidth=40 / control_frame_width, relheight=25 / control_frame_height)

        self.start_day_entry = tkinter.Entry(self.control_frame, relief="sunken", bg="white", justify="center"
                                             , state="disabled", font=self.font_style)
        self.start_day_entry.place(relx=305 / control_frame_width, rely=10 / control_frame_height,
                                   relwidth=60 / control_frame_width, relheight=25 / control_frame_height)
        self.start_day_entry.insert(0, "1")

        self.start_day_label_tx = tkinter.Label(self.control_frame, text="Day", relief="flat", anchor="w",
                                                state="disabled", disabledforeground="black", font=self.font_style)
        self.start_day_label_tx.place(relx=365 / control_frame_width, rely=10 / control_frame_height,
                                      relwidth=40 / control_frame_width, relheight=25 / control_frame_height)

        # End Time Control Setup
        self.end_time_label_tx = tkinter.Label(self.control_frame, text="End Time", relief="flat", anchor="e",
                                               state="disabled", disabledforeground="black", font=self.font_style)
        self.end_time_label_tx.place(relx=5 / control_frame_width, rely=45 / control_frame_height,
                                     relwidth=70 / control_frame_width, relheight=25 / control_frame_height)

        self.end_year_entry = tkinter.Entry(self.control_frame, relief="sunken", bg="white", justify="center"
                                            , state="disabled", font=self.font_style)
        self.end_year_entry.place(relx=85 / control_frame_width, rely=45 / control_frame_height,
                                  relwidth=60 / control_frame_width, relheight=25 / control_frame_height)
        self.end_year_entry.insert(0, "2020")

        self.end_year_label_tx = tkinter.Label(self.control_frame, text="Year", relief="flat", anchor="w",
                                               state="disabled", disabledforeground="black", font=self.font_style)
        self.end_year_label_tx.place(relx=145 / control_frame_width, rely=45 / control_frame_height,
                                     relwidth=30 / control_frame_width, relheight=25 / control_frame_height)

        self.end_month_entry = tkinter.Entry(self.control_frame, relief="sunken", bg="white", justify="center",
                                             state="disabled", font=self.font_style)
        self.end_month_entry.place(relx=190 / control_frame_width, rely=45 / control_frame_height,
                                   relwidth=60 / control_frame_width, relheight=25 / control_frame_height)
        self.end_month_entry.insert(0, "8")

        self.end_month_label_tx = tkinter.Label(self.control_frame, text="Month", relief="flat", anchor="w",
                                                state="disabled", disabledforeground="black", font=self.font_style)
        self.end_month_label_tx.place(relx=250 / control_frame_width, rely=45 / control_frame_height,
                                      relwidth=40 / control_frame_width, relheight=25 / control_frame_height)

        self.end_day_entry = tkinter.Entry(self.control_frame, relief="sunken", bg="white", justify="center",
                                           state="disabled", font=self.font_style)
        self.end_day_entry.place(relx=305 / control_frame_width, rely=45 / control_frame_height,
                                 relwidth=60 / control_frame_width, relheight=25 / control_frame_height)
        self.end_day_entry.insert(0, "1")

        self.end_day_label_tx = tkinter.Label(self.control_frame, text="Day", relief="flat", anchor="w",
                                              state="disabled", disabledforeground="black", font=self.font_style)
        self.end_day_label_tx.place(relx=365 / control_frame_width, rely=45 / control_frame_height,
                                    relwidth=40 / control_frame_width, relheight=25 / control_frame_height)

        # Display Unit Setup
        self.display_unit_label_tx = tkinter.Label(self.control_frame, text="Display Unit", relief="flat", anchor="e",
                                                   state="disabled", disabledforeground="black", font=self.font_style)
        self.display_unit_label_tx.place(relx=5 / control_frame_width, rely=80 / control_frame_height,
                                         relwidth=70 / control_frame_width, relheight=25 / control_frame_height)

        self.year_unit_var = tkinter.IntVar()
        self.year_unit_check = tkinter.Checkbutton(self.control_frame, text="Year", variable=self.year_unit_var,
                                                   anchor="w", state="disabled", font=self.font_style)
        self.year_unit_check.place(relx=80 / control_frame_width, rely=80 / control_frame_height,
                                   relwidth=50 / control_frame_width, relheight=25 / control_frame_height)
        self.year_unit_check.configure(command=lambda: self.year_unit_check_callback())

        self.month_unit_var = tkinter.IntVar()
        self.month_unit_check = tkinter.Checkbutton(self.control_frame, text="Month", variable=self.month_unit_var,
                                                    anchor="w", state="disabled", font=self.font_style)
        self.month_unit_check.place(relx=140 / control_frame_width, rely=80 / control_frame_height,
                                    relwidth=60 / control_frame_width, relheight=25 / control_frame_height)
        self.month_unit_check.configure(command=lambda: self.month_unit_check_callback())

        self.day_unit_var = tkinter.IntVar()
        self.day_unit_check = tkinter.Checkbutton(self.control_frame, text="Day", variable=self.day_unit_var,
                                                  anchor="w", state="disabled", font=self.font_style)
        self.day_unit_check.place(relx=210 / control_frame_width, rely=80 / control_frame_height,
                                  relwidth=50 / control_frame_width, relheight=25 / control_frame_height)
        self.day_unit_check.configure(command=lambda: self.day_unit_check_callback())

        self.hour_unit_var = tkinter.IntVar()
        self.hour_unit_check = tkinter.Checkbutton(self.control_frame, text="Hour", variable=self.hour_unit_var,
                                                   anchor="w", state="disabled", font=self.font_style)
        self.hour_unit_check.place(relx=270 / control_frame_width, rely=80 / control_frame_height,
                                   relwidth=50 / control_frame_width, relheight=25 / control_frame_height)
        self.hour_unit_check.configure(command=lambda: self.hour_unit_check_callback())

        self.minute_unit_var = tkinter.IntVar()
        self.minute_unit_check = tkinter.Checkbutton(self.control_frame, text="Minute", variable=self.minute_unit_var,
                                                     anchor="w", state="disabled", font=self.font_style)
        self.minute_unit_check.place(relx=330 / control_frame_width, rely=80 / control_frame_height,
                                     relwidth=70 / control_frame_width, relheight=25 / control_frame_height)

        self.minute_unit_check.configure(command=lambda: self.minute_unit_check_callback())

        # Display Button Setup
        self.display_button = tkinter.Button(self.control_frame, text="Display", relief="raised", state="disabled",
                                             font=self.font_style)
        self.display_button.place(relx=415 / control_frame_width, rely=10 / control_frame_height,
                                  relwidth=110 / control_frame_width, relheight=90 / control_frame_height)
        self.display_button.configure(command=lambda: self.display_button_callback())

        # List Frame Setup
        self.list_frame = tkinter.Frame(self.window, relief="ridge", bd=2)
        self.list_frame.place(relx=list_frame_sx / window_width,
                              rely=list_frame_sy / window_height,
                              relwidth=list_frame_width / window_width,
                              relheight=list_frame_height / window_height)

        # Display List Setup
        self.s_position_low = 0
        self.s_position_high = 0.5

        self.list_scrollbar = tkinter.Scrollbar(self.list_frame)
        self.list_scrollbar.pack(side='right', fill='y')
        self.display_listbox = tkinter.Listbox(self.list_frame, relief="sunken", state="normal", fg="black",
                                               yscrollcommand=self.list_scrollbar.set, font=self.font_style,
                                               activestyle="none", selectmode="browse")
        self.display_listbox.place(relx=1 / list_frame_width, rely=1 / list_frame_height,
                                   relwidth=258 / list_frame_width, relheight=398 / list_frame_height)
        self.list_scrollbar.configure(command=self.display_listbox.yview)
        self.display_listbox.bind("<<ListboxSelect>>", self.list_select_fnc)
        # graph Frame Setup
        self.graph_frame = tkinter.Frame(self.window, relief="ridge", bd=2)
        self.graph_frame.place(relx=graph_frame_sx / window_width,
                               rely=graph_frame_sy / window_height,
                               relwidth=graph_frame_width / window_width,
                               relheight=graph_frame_height / window_height)

        # Video Canvas Setup
        self.display_canvas = tkinter.Canvas(self.graph_frame, relief="solid", bg="white")
        self.display_canvas.place(relx=1 / graph_frame_width, rely=1 / graph_frame_height,
                                  relwidth=523 / graph_frame_width, relheight=378 / graph_frame_height)

        self.canvas_scrollbar = tkinter.Scrollbar(self.graph_frame, orient="horizontal",
                                                  command=self.display_canvas.xview)
        self.display_canvas.config(xscrollcommand=self.canvas_scrollbar.set)
        self.canvas_scrollbar.pack(side='bottom', fill='x')

        # Window Main Loop Setup
        self.window.mainloop()

    def window_resize_fnc(self, event):
        global cur_win_width
        global cur_win_height

        if (self.display_canvas.winfo_width() != cur_win_width) or (self.display_canvas.winfo_height() != cur_win_height):
            font_rate = self.window.winfo_height() / window_height
            self.font_style = tkFont.Font(family="arial", size=int(9*font_rate))
            self.font_resize_fnc()
            cur_win_width = self.display_canvas.winfo_width()
            cur_win_height = self.display_canvas.winfo_height()
            self.display_button.invoke()

    def font_resize_fnc(self):
        # IP Input Setup
        self.ip_label_tx.configure(font=self.font_style)
        self.ip_entry.configure(font=self.font_style)

        # Port Input Setup
        self.port_label_tx.configure(font=self.font_style)
        self.port_entry.configure(font=self.font_style)

        # ID Input Setup
        self.id_label_tx.configure(font=self.font_style)
        self.id_entry.configure(font=self.font_style)

        # PWD Input Setup
        self.pwd_label_tx.configure(font=self.font_style)
        self.pwd_entry.configure(font=self.font_style)

        # FTP Connect Button Setup
        self.connect_button.configure(font=self.font_style)

        # Start Time Control Setup
        self.start_time_label_tx.configure(font=self.font_style)
        self.start_year_entry.configure(font=self.font_style)
        self.start_year_label_tx.configure(font=self.font_style)
        self.start_month_entry.configure(font=self.font_style)
        self.start_month_label_tx.configure(font=self.font_style)
        self.start_day_entry.configure(font=self.font_style)
        self.start_day_label_tx.configure(font=self.font_style)

        # End Time Control Setup
        self.end_time_label_tx.configure(font=self.font_style)
        self.end_year_entry.configure(font=self.font_style)
        self.end_year_label_tx.configure(font=self.font_style)
        self.end_month_entry.configure(font=self.font_style)
        self.end_month_label_tx.configure(font=self.font_style)
        self.end_day_entry.configure(font=self.font_style)
        self.end_day_label_tx.configure(font=self.font_style)

        # Display Unit Setup
        self.display_unit_label_tx.configure(font=self.font_style)
        self.year_unit_check.configure(font=self.font_style)
        self.month_unit_check.configure(font=self.font_style)
        self.day_unit_check.configure(font=self.font_style)
        self.hour_unit_check.configure(font=self.font_style)
        self.minute_unit_check.configure(font=self.font_style)

        # Display Button Setup
        self.display_button.configure(font=self.font_style)

        # Listbox Setup
        self.display_listbox.configure(font=self.font_style)

    def list_select_fnc(self, event):
        global list_select_num
        value = np.asarray(self.display_listbox.curselection())
        scrollbar_position = self.list_scrollbar.get()
        self.s_position_low = scrollbar_position[0]
        self.s_position_high = scrollbar_position[1]

        if value.size != 0:
            list_select_num = value[0]
            if list_select_num > 0:
                self.display_button.invoke()

    def window_close(self):
        self.window.destroy()

    def connect_button_callback(self):
        self.input_ip = self.ip_entry.get()
        self.input_port = int(self.port_entry.get())
        self.input_id = self.id_entry.get()
        self.input_pwd = self.pwd_entry.get()
        ret, data = ftp_connect_fnc(self.input_ip, self.input_port, self.input_id, self.input_pwd, 0, '', '')

        if ret == 0:
            self.start_year_entry.config(state="normal")
            self.start_year_entry.delete(0, "end")
            self.start_year_entry.insert(0, "2020")
            self.start_month_entry.config(state="normal")
            self.start_month_entry.delete(0, "end")
            self.start_month_entry.insert(0, "8")
            self.start_day_entry.config(state="normal")
            self.start_day_entry.delete(0, "end")
            self.start_day_entry.insert(0, "1")
            self.end_year_entry.config(state="normal")
            self.end_year_entry.delete(0, "end")
            self.end_year_entry.insert(0, "2020")
            self.end_month_entry.config(state="normal")
            self.end_month_entry.delete(0, "end")
            self.end_month_entry.insert(0, "8")
            self.end_day_entry.config(state="normal")
            self.end_day_entry.delete(0, "end")
            self.end_day_entry.insert(0, "1")

            self.year_unit_check.config(state="normal")
            self.year_unit_var.set(0)
            self.month_unit_check.config(state="normal")
            self.month_unit_var.set(0)
            self.day_unit_check.config(state="normal")
            self.day_unit_var.set(0)
            self.hour_unit_check.config(state="normal")
            self.hour_unit_var.set(0)
            self.minute_unit_check.config(state="normal")
            self.minute_unit_var.set(1)

            self.display_button.configure(state="normal")
        else:
            tkinter.messagebox.showerror("Error", ret)

    def year_unit_check_callback(self):
        if self.year_unit_var.get() == 1:
            self.month_unit_var.set(0)
            self.day_unit_var.set(0)
            self.hour_unit_var.set(0)
            self.minute_unit_var.set(0)

    def month_unit_check_callback(self):
        if self.month_unit_var.get() == 1:
            self.year_unit_var.set(0)
            self.day_unit_var.set(0)
            self.hour_unit_var.set(0)
            self.minute_unit_var.set(0)

    def day_unit_check_callback(self):
        if self.day_unit_var.get() == 1:
            self.year_unit_var.set(0)
            self.month_unit_var.set(0)
            self.hour_unit_var.set(0)
            self.minute_unit_var.set(0)

    def hour_unit_check_callback(self):
        if self.hour_unit_var.get() == 1:
            self.year_unit_var.set(0)
            self.month_unit_var.set(0)
            self.day_unit_var.set(0)
            self.minute_unit_var.set(0)

    def minute_unit_check_callback(self):
        if self.minute_unit_var.get() == 1:
            self.year_unit_var.set(0)
            self.month_unit_var.set(0)
            self.day_unit_var.set(0)
            self.hour_unit_var.set(0)

    def display_button_callback(self):
        global list_select_num

        start_year = self.start_year_entry.get()
        start_year = int(start_year[2:4])
        start_month = int(self.start_month_entry.get())
        start_day = int(self.start_day_entry.get())

        end_year = self.end_year_entry.get()
        end_year = int(end_year[2:4])
        end_month = int(self.end_month_entry.get())
        end_day = int(self.end_day_entry.get())

        if self.minute_unit_var.get() == 1:
            display_mode = 0
        elif self.hour_unit_var.get() == 1:
            display_mode = 1
        elif self.day_unit_var.get() == 1:
            display_mode = 2
        elif self.month_unit_var.get() == 1:
            display_mode = 3
        else:
            display_mode = 4

        # start time > end time check

        err1 = 0
        if start_year > 99:
            err1 = 1
        else:
            if start_month < 0 or start_month > 12:
                err1 = 1
            else:
                d, n = calendar.monthrange(start_year + 2000, start_month)
                if start_day > n:
                    err1 = 1

        err2 = 0
        if end_year > 99:
            err2 = 1
        else:
            if end_month < 0 or end_month > 12:
                err2 = 1
            else:
                d, n = calendar.monthrange(end_year + 2000, end_month)
                if end_day > n:
                    err2 = 1

        start_time = start_year * 10000 + start_month * 100 + start_day
        end_time = end_year * 10000 + end_month * 100 + end_day

        err3 = 0
        if start_time > end_time:
            err3 = 1

        if err1 == 1 or err2 == 1 or err3 == 1:
            tkinter.messagebox.showerror("Error", "Selected Date is Wrong!!")
        else:
            # File Download Folder Initialization
            temporary_path = temporary_folder_fnc()

            # File Download
            ret, data = ftp_connect_fnc(self.input_ip, self.input_port, self.input_id, self.input_pwd, 0, '', '')
            if ret == 0:
                list_len = len(data)
                for n in range(0, list_len):
                    file_parts = data[n]
                    file_h = file_parts[0:8]
                    file_y = int(file_parts[10:12])
                    file_m = int(file_parts[12:14])
                    file_d = int(file_parts[14:16])

                    if file_h == '[Report]':
                        start_time = start_year * 10000 + start_month * 100 + start_day
                        end_time = end_year * 10000 + end_month * 100 + end_day
                        file_time = file_y * 10000 + file_m * 100 + file_d

                        if (file_time >= start_time) and (file_time <= end_time):
                            ret, file_data = ftp_connect_fnc(self.input_ip, self.input_port, self.input_id,
                                                             self.input_pwd
                                                             , 1, temporary_path, file_parts)
                        else:
                            # user selected time range over, no process
                            pass
                    else:
                        # list file name format error, no process
                        pass
            else:
                # FTP Connect Fail, Retry request
                tkinter.messagebox.showerror("Error", ret)
                pass

            # Data Loading
            start_time = start_year * 10000 + start_month * 100 + start_day
            end_time = end_year * 10000 + end_month * 100 + end_day

            ret_data = display_data_fnc(display_mode, temporary_path, start_time, end_time)

            if ret_data.size == 0:
                # none data : list & graph clear
                self.display_listbox.delete(0, 'end')
                pass
            else:
                self.display_listbox.delete(0, 'end')

                list_value = "{0:^2}{1:^7}{0:^3}{2:^20}{0:^5}{3:^8}{0:^5}{4:^10}".\
                    format(" ", "Index", "Start Time", "In", "Out")
                self.display_listbox.insert(0, list_value)
                self.display_listbox.itemconfig(0, foreground="Blue")

                for i in range(0, ret_data.shape[0]):
                    time_temp = ret_data[i, 0]
                    if display_mode == 0:
                        n, minute_d = divmod(time_temp, 100)
                        n, hour_d = divmod(n, 100)
                        n, day_d = divmod(n, 100)
                        year_d, month_d = divmod(n, 100)
                        time_decode = "[%02d.%02d.%02d] %02d:%02d" % (year_d, month_d, day_d, hour_d, minute_d)
                    elif display_mode == 1:
                        n, hour_d = divmod(time_temp, 100)
                        n, day_d = divmod(n, 100)
                        year_d, month_d = divmod(n, 100)
                        time_decode = "[%02d.%02d.%02d] %02d:--" % (year_d, month_d, day_d, hour_d)
                    elif display_mode == 2:
                        n, day_d = divmod(time_temp, 100)
                        year_d, month_d = divmod(n, 100)
                        time_decode = "[%02d.%02d.%02d] --:--" % (year_d, month_d, day_d)
                    elif display_mode == 3:
                        year_d, month_d = divmod(time_temp, 100)
                        time_decode = "[%02d.%02d.--] --:--" % (year_d, month_d)
                    else:
                        year_d = time_temp
                        time_decode = "[%02d.--.--] --:--" % year_d

                    # self.display_listbox.insert(i+1, "  %05d     %16s     %06d      %06d"
                    #                             % (i+1, time_decode, ret_data[i, 1], ret_data[i, 2]))
                    list_value = " {0:^7}{1:^20}{2:^8}{3:^10}".format("%05d" % (i + 1), time_decode,
                                                                      "%06d" % ret_data[i, 1],
                                                                      "%06d" % ret_data[i, 2])
                    self.display_listbox.insert(i + 1, list_value)

                    if ret_data[i, 3] == 1:
                        self.display_listbox.itemconfig(i+1, foreground="red")
                    else:
                        self.display_listbox.itemconfig(i+1, foreground="black")

                self.display_listbox.config(command=self.display_listbox.yview_moveto(self.s_position_low))
                self.display_listbox.selection_set(list_select_num, list_select_num)

                # graph display
                self.display_canvas.delete("all")

                canvas_w_temp = 519
                canvas_h_temp = 374

                canvas_h_cur = self.display_canvas.winfo_height()
                canvas_w_cur = self.display_canvas.winfo_width()

                x_margin = 50
                y_margin = 50

                canvas_x_origin = canvas_w_cur - x_margin
                canvas_y_origin = canvas_h_cur - y_margin

                count_max = np.max([np.max(ret_data[:, 1]), np.max(ret_data[:, 2])])
                count_num = ret_data.shape[0] * 2

                y_rate = (canvas_h_temp - y_margin - 5) / count_max

                if y_rate > 1:
                    y_rate = 1
                    count_max = canvas_h_temp - y_margin - 5

                resize_y_rate = canvas_y_origin / (canvas_h_temp-y_margin)
                resize_x_rate = canvas_x_origin / (canvas_w_temp-x_margin)

                n1, d1 = divmod(count_max, 50)
                n2, d2 = divmod(n1, 6)
                if n1 < 6:
                    gap_value = 50
                else:
                    gap_value = 50 * n2

                y_grid_gap = (gap_value*y_rate) * resize_y_rate

                if count_num > 64:
                    x_range = 7
                else:
                    x_range = round((64*7) / count_num)
                    d, n = divmod(x_range, 2)
                    if n == 0:
                        x_range = x_range - 1

                x_range = x_range * resize_x_rate

                y_ref = canvas_y_origin
                x_cur = x_margin

                for i in range(0, ret_data.shape[0]):
                    if list_select_num-1 == i:
                        select_sx = x_cur + 1
                        select_ex = x_cur + x_range*2 + 1
                        self.display_canvas.create_rectangle(select_sx, 0, select_ex, canvas_h_cur,
                                                             fill="yellow2", outline='yellow2')
                        self.display_listbox.activate(i)

                    bar_in_sx = x_cur + 1
                    bar_in_ex = bar_in_sx + x_range
                    bar_in_y = ret_data[i, 1] * y_rate * resize_y_rate
                    x_cur = bar_in_ex
                    self.display_canvas.create_rectangle(bar_in_sx, y_ref - 1 - bar_in_y, bar_in_ex, y_ref,
                                                         fill="red", outline='red')

                    if i == 0:
                        self.display_canvas.create_text(x_cur, y_ref + 10,
                                                        fill="black", font="Times 10 italic bold", text=i + 1)
                    else:
                        d, n = divmod(i + 1, 10)
                        if n == 0:
                            self.display_canvas.create_text(x_cur, y_ref + 10,
                                                            fill="black", font="Times 10 italic bold", text=i + 1)

                    bar_out_sx = x_cur + 1
                    bar_out_ex = bar_out_sx + x_range
                    bar_out_y = ret_data[i, 2] * y_rate * resize_y_rate
                    x_cur = bar_out_ex
                    self.display_canvas.create_rectangle(bar_out_sx, y_ref - 1 - bar_out_y, bar_out_ex, y_ref,
                                                         fill="blue", outline='blue')

                self.display_canvas.create_line(x_margin, y_ref, x_cur + 10, y_ref, fill='black', width=2)
                self.display_canvas.create_line(x_margin, y_ref, x_margin, 0, fill='black', width=2)
                for i in range(1, 10):
                    if y_ref - (y_grid_gap * i) > 5:
                        self.display_canvas.create_line(x_margin, y_ref - (y_grid_gap * i),
                                                        x_cur + 10, y_ref - (y_grid_gap * i), fill='black',
                                                        dash=(4, 4), width=1)
                        y_label = round(gap_value * i)
                        self.display_canvas.create_text(x_margin - 20, y_ref - (y_grid_gap * i) - 5,
                                                        fill="black", font="Times 10 italic bold", text=y_label)
                    else:
                        break

                self.display_canvas.configure(scrollregion=self.display_canvas.bbox("all"))


if __name__ == '__main__':
    gui_h = viewer_gui_control()
    gui_h.daemon = True
    gui_h.start()
