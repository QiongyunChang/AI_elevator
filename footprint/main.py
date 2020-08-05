# 整合code
import os
import csv
import first_handDect # 開始辨識介面
import face_allIn_final0 # 臉部辨識
import recognizer_final  # 手部辨識 + 聲音辨識
import tkinter as tk
import winsound
import threading
import pyttsx3
from datetime import datetime
import time
import sys

# 自動關閉視窗
def CloseWindow():
    for i in range(3):
        time.sleep(3)
    root.destroy()

# 自動關閉視窗2
def CloseWindow2():
    for i in range(5):
        time.sleep(1)
    root2.destroy()

# 打招呼
def SayHi(txt):
    engine = pyttsx3.init()
    # 語速控制
    rate = engine.getProperty('rate')
    engine.setProperty('rate', rate - 50)
    #engine.setProperty('voice', "com.apple.speech.synthesis.voice.mei-jia") # 設置聲音
    engine.say(txt)
    engine.runAndWait()

if __name__ == '__main__':
    # 開始介面
    first_handDect # 一開始辨識介面
    # 臉部辨識人名
    Name = face_allIn_final0.test()
    if Name != "No Data":
        # 介面顯示--請問要去幾樓
        root = tk.Tk()
        root.resizable(width=False, height=False)
        # Hifloor(str)
        root.title("AI elevator")
        root.geometry('800x300+350+250')  # (x=350, y=250)
        Hi_label = tk.Label(root, font=('微軟正黑體', 30), fg='MidnightBlue')
        Hi_label['text'] = 'Hi !  {} '.format(Name)
        Hi_label.place(x=460, y=150, anchor='se')
        info_label = tk.Label(root, text='請說明想前往的樓層', font=('微軟正黑體', 32))
        info_label.place(x=600, y=200, anchor='se')
        wait_ti = tk.Label(root, font=('微軟正黑體', 20), fg='Black', text='等待鏡頭開啟...')
        # countdown
        wait_ti.place(x=760, y=290, anchor='se')
        SayHi(Name+"您好")  # 跟進入者打招呼
        winsound.PlaySound(r".\sound\floor.wav", winsound.SND_FILENAME | winsound.SND_ASYNC)
        t = threading.Thread(target=CloseWindow)
        t.start()
        root.mainloop()

        Floor = recognizer_final.mainwork() # 樓層

        # 介面顯示--幾樓
        root2 = tk.Tk()
        root2.resizable(width=False, height=False)
        # Hifloor(str)
        root2.title("AI elevator")
        root2.geometry('800x300+350+250')  # (x=350, y=250)
        floor_show = tk.Label(root2, font=('微軟正黑體', 90), fg='MidnightBlue')
        floor_show['text'] = '{} '.format(Floor)
        floor_show.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        SayHi(str(Floor) + "樓")
        t = threading.Thread(target=CloseWindow2)
        t.start()
        root2.mainloop()


        # 足跡紀錄(寫成csv)
        today = datetime.now()
        date = today.strftime('%Y-%m-%d')  # 日期
        timee = time.strftime('%H:%M:%S')  # 時間
        # 二維表格
        table = [
            [Name, Floor, date, timee],
        ]
        # 足跡資料儲存
        with open('footprint.csv', 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)
            # 寫入二維表格
            writer.writerows(table)
        print("END")
        # 結束程式
        sys.exit()
    else:
        # 導入註冊頁面
        os.system('python take_a_shot.py')
