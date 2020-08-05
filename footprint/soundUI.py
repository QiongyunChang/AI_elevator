import os
import time
import csv
import tkinter as tk
import winsound
import threading


def CloseWindow():
    for i in range(3):
        lbTime['text'] = '倒數{}秒'.format(3-i)
        time.sleep(1)
    root.destroy()


root = tk.Tk()
root.resizable(width=False, height=False)
root.title("AI elevator")
root.geometry('800x300+350+250')  # (x=350, y=250)
# voice
winsound.PlaySound(r"./sound/voice.wav", winsound.SND_FILENAME | winsound.SND_ASYNC)
# speak image
photo = tk.PhotoImage(file="./img_ui/vo.png")
imgLabel = tk.Label(root,image=photo)
imgLabel.pack(side=tk.BOTTOM)#自動對齊
lbTime = tk.Label(root, font=('微軟正黑體', 20),fg='MidnightBlue')
# countdown
lbTime.place(x=730, y=280, anchor='se')
info_label = tk.Label(root, text='開始進行聲音辨識', font=('微軟正黑體', 40))
info_label.place(x=400, y=120, anchor=tk.CENTER)
t = threading.Thread(target=CloseWindow)
t.start()
root.mainloop()