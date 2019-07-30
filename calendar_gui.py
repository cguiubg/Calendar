import tkinter as tk
import math
import json

LOWHEIGHT = 0.97
ENTRYHEIGHT = 0.030

with open('settings.json') as f:
    settings = json.load(f)

def process_command(event=None):
    input_ = entry.get()
    move_command_up(input_)

def move_command_up(string: str):
    temp_r1 = string
    temp_l1 = settings['indicator']
    for side, history in text_list:
        side.config(state=tk.NORMAL)
        history.config(state=tk.NORMAL)
        temp_l2 = side.get()
        temp_r2 = history.get()
        side.delete(0, tk.END)
        history.delete(0, tk.END)
        side.insert(0, temp_l1)
        history.insert(0, temp_r1)
        side.config(state='readonly')
        history.config(state='readonly')
        temp_l1 = temp_l2
        temp_r1 = temp_r2
    entry.delete(0, tk.END)

root = tk.Tk()

canvas = tk.Canvas(root, height=settings['window']['height'], width=settings['window']['width'])
canvas.pack()

font = (settings['font']['type'], settings['font']['size'])

input_frame = tk.Frame(root, bg='#252525')
input_frame.config()
input_frame.place(relx=0, rely=0, relwidth=0.3, relheight=1)

root.bind('<Return>', func=process_command)

sidebar = tk.Entry(input_frame)
entry = tk.Entry(input_frame)
sidebar.config(readonlybackground='#1C1C1C', fg='#A3f774', font=font, bd=0, highlightthickness=0)
sidebar.insert(0, settings['indicator'])
sidebar.config(state='readonly')
entry.config(bg='#1C1C1C', fg='#A3f774', font=font, bd=0, highlightthickness=0)
if settings['invert']:
    sidebar.place(relx=0, rely=0, width=25, relheight=1-LOWHEIGHT)
    entry.place(x=25, rely=0, relwidth=0.90, relheight=1-LOWHEIGHT)
else:
    sidebar.place(relx=0, rely=LOWHEIGHT, width=25, relheight=1-LOWHEIGHT)
    entry.place(x=25, rely=LOWHEIGHT, relwidth=0.90, relheight=1-LOWHEIGHT)

entry_num = int(math.ceil(LOWHEIGHT/ENTRYHEIGHT))

text_list = [(tk.Entry(input_frame), tk.Entry(input_frame)) for _ in range(entry_num)]
i = 1
for side, history in text_list:
    side.config(readonlybackground='#2D2D2D', fg='#F7C974', font=font, bd=0, highlightthickness=0)
    side.config(state='readonly')
    history.config(readonlybackground='#252525', fg='#E4F774', font=font, bd=0, highlightthickness=0)
    history.config(state='readonly')
    if settings['invert']:
        side.place(relx=0, rely=i*ENTRYHEIGHT, width=25, relheight=ENTRYHEIGHT)
        history.place(x=25, rely=i*ENTRYHEIGHT, relwidth=0.90, relheight=ENTRYHEIGHT)
    else:
        side.place(relx=0, rely=LOWHEIGHT-i*ENTRYHEIGHT, width=25, relheight=ENTRYHEIGHT)
        history.place(x=25, rely=LOWHEIGHT-i*ENTRYHEIGHT, relwidth=0.90, relheight=ENTRYHEIGHT)
    i += 1

displayFrame = tk.Frame(root, bg='#1C1C1C')
displayFrame.place(relx=0.3, rely=0, relwidth=0.7, relheight=1)

# root.resizable(height=False, width=False)
root.title('Calendar')
root.mainloop()