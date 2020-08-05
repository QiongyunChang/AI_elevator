import tkinter as tk
import winsound
import time
import threading
def autoClose():
    for i in range(3):
        time.sleep(1)
    root.destroy()

def facedectUI():
    # 介面開始
    root.title("AI elevator")
    winsound.PlaySound(r"./sound/facedect.wav", winsound.SND_FILENAME | winsound.SND_ASYNC)
    root.geometry('800x300+350+250') # (x=350, y=250)
    root.resizable(width=False, height=False)
    info_label = tk.Label(root, text='開始進行人臉辨識', font=('微軟正黑體', 50))
    info_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

root = tk.Tk()
facedectUI()
photo = tk.PhotoImage(file="./img_ui/face.png")#speak image
imgLabel = tk.Label(root,image=photo)
imgLabel.pack(side=tk.BOTTOM)#自動對齊
lbTime = tk.Label(root, font=('微軟正黑體', 20),fg='MidnightBlue',text='等待鏡頭開啟...')
# countdown
lbTime.place(x=760, y=290, anchor='se')
t = threading.Thread(target=autoClose)
t.start()
root.mainloop()
