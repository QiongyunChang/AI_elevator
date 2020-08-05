import os
import time
import csv
import tkinter as tk
import winsound
import threading
from tkinter import *
from PIL import Image, ImageTk


def CloseWindow():
    for i in range(3):
        time.sleep(1)
    root.destroy()





root = tk.Tk()
root.resizable(width=False, height=False)
root.title("AI elevator")
#root.geometry('800x800+350+250')  # (x=350, y=250)
# info_label = tk.Label(root, text='人臉辨識已通過', font=('微軟正黑體', 40))
# info_label.place(x=400, y=120, anchor=tk.CENTER)
# canvas = Canvas(width = 800, height = 500)
# # canvas.pack(expand = YES, fill = BOTH)
# # gif1 = PhotoImage(file = 'tick.gif')
# # canvas.create_image(50, 10, image = gif1, anchor = NW)


frames = [PhotoImage(file='tick.gif',format = 'gif -index %i' %(i)) for i in range(100)]

def update(ind):

    frame = frames[ind]
    ind += 1
    label.configure(image=frame)
    root.after(100, update, ind)
label = Label(root)
label.pack()
root.after(0, update, 0)
t = threading.Thread(target=CloseWindow)
t.start()
root.mainloop()



