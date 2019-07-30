import tkinter as tk, tkinter.font as tkFont
import math

HEIGHT = 700
WIDTH = 1000

LOWHEIGHT = 0.97
ENTRYHEIGHT = 0.030

FONT = ('Menlo', 12)
INDICATOR = ' λ:'

top_down = False

def process_command(event=None):
    input_ = entry.get()
    move_command_up(input_)

def move_command_up(string: str):
    temp_r1 = string
    temp_l1 = INDICATOR
    for text_l, text_r in text_list:
        text_l.config(state=tk.NORMAL)
        text_r.config(state=tk.NORMAL)
        temp_l2 = text_l.get()
        temp_r2 = text_r.get()
        text_l.delete(0, tk.END)
        text_r.delete(0, tk.END)
        text_l.insert(0, temp_l1)
        text_r.insert(0, temp_r1)
        text_l.config(state='readonly')
        text_r.config(state='readonly')
        temp_l1 = temp_l2
        temp_r1 = temp_r2
    entry.delete(0, tk.END)

root = tk.Tk()

canvas = tk.Canvas(root, height=HEIGHT, width=WIDTH)
canvas.pack()

input_frame = tk.Frame(root)
input_frame.place(relx=0, rely=0, relwidth=0.3, relheight=1)

root.bind('<Return>', func=process_command)

entry_aux = tk.Entry(input_frame)
entry = tk.Entry(input_frame)
entry_aux.config(readonlybackground='#1C1C1C', fg='#A3f774', font=FONT, bd=0, highlightthickness=0)
entry_aux.insert(0, INDICATOR)
entry_aux.config(state='readonly')
entry.config(bg='#1C1C1C', fg='#A3f774', font=FONT, bd=0, highlightthickness=0)
if top_down:
    entry_aux.place(relx=0, rely=0, relwidth=0.10, relheight=1-LOWHEIGHT)
    entry.place(relx=0.10, rely=0, relwidth=0.90, relheight=1-LOWHEIGHT)
else:
    entry_aux.place(relx=0, rely=LOWHEIGHT, relwidth=0.10, relheight=1-LOWHEIGHT)
    entry.place(relx=0.10, rely=LOWHEIGHT, relwidth=0.90, relheight=1-LOWHEIGHT)

entry_num = int(math.ceil(LOWHEIGHT/ENTRYHEIGHT))

text_list = [(tk.Entry(input_frame), tk.Entry(input_frame)) for _ in range(entry_num)]
i = 1

for text_l, text_r in text_list:
    text_l.config(readonlybackground='#2D2D2D', fg='#F7C974', font=FONT, bd=0, highlightthickness=0)
    text_l.config(state='readonly')
    text_r.config(readonlybackground='#252525', fg='#E4F774', font=FONT, bd=0, highlightthickness=0)
    text_r.config(state='readonly')
    if top_down:
        text_r.place(relx=0.1, rely=i*ENTRYHEIGHT, relwidth=0.90, relheight=ENTRYHEIGHT)
        text_l.place(relx=0, rely=i*ENTRYHEIGHT, relwidth=0.10, relheight=ENTRYHEIGHT)
    else:
        text_r.place(relx=0.1, rely=LOWHEIGHT-i*ENTRYHEIGHT, relwidth=0.90, relheight=ENTRYHEIGHT)
        text_l.place(relx=0, rely=LOWHEIGHT-i*ENTRYHEIGHT, relwidth=0.10, relheight=ENTRYHEIGHT)
    i += 1

displayFrame = tk.Frame(root, bg='#1C1C1C')
displayFrame.place(relx=0.3, rely=0, relwidth=0.7, relheight=1)

root.resizable(height=False, width=False)
root.title('Calendar')
root.mainloop()