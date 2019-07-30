import tkinter as tk
import math
import json

#delcaring heights entry widgets
LOWEST_Y = 0.97 #relative y in window for the lowest entry widget
ENTRY_HEIGHT = 0.03 
ENTRY_Y = 0.03 #relative height of entry widgets

with open('settings.json') as f: #opening the settings.json file
    settings = json.load(f)

#commands are passed here and then sent to the needed function
def process_command(event=None) -> None: 
    input_ = entry.get()
    move_history(input_, settings['indicator'])

#takes a string for log a string for the side bar, moves all strings up the history
def move_history(text: str, side: str) -> None:
    temp_r1 = text
    temp_l1 = side
    #iterating through history of text log and moving the text and side to the next
    for side, history in text_log:
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

#binding the processes command to enter
root.bind('<Return>', func=process_command)

#creating the canvas
canvas = tk.Canvas(root, height=settings['window']['height'], width=settings['window']['width'])
canvas.pack()

#getting the font tuple from the settings.json
font = (settings['font']['type'], settings['font']['size'])

#making the frame where input is displayed
input_frame = tk.Frame(root, bg='#252525')
input_frame.config()
input_frame.place(relx=0, rely=0, relwidth=0.3, relheight=1)

#making the sidebar and the main input widget
sidebar = tk.Entry(input_frame)
entry = tk.Entry(input_frame)
sidebar.config(readonlybackground='#1C1C1C', fg='#A3f774', font=font, bd=0, highlightthickness=0)
sidebar.insert(0, settings['indicator'])
sidebar.config(state='readonly')
entry.config(bg='#1C1C1C', fg='#A3f774', font=font, bd=0, highlightthickness=0)
#if invert is true in settings, history goes top (most recent) to bottom (oldest)
if settings['invert']:
    sidebar.place(relx=0, rely=0, width=25, relheight=1-LOWEST_Y)
    entry.place(x=25, rely=0, relwidth=0.95, relheight=1-LOWEST_Y)
#otherwise, history goes bottom (most recent) to top (oldest)
else:
    sidebar.place(relx=0, rely=LOWEST_Y, width=25, relheight=1-LOWEST_Y)
    entry.place(x=25, rely=LOWEST_Y, relwidth=0.95, relheight=1-LOWEST_Y)

#finding the number of entry widgets necesarry for the history log
entry_num = int(math.ceil(LOWEST_Y/ENTRY_HEIGHT))

#making the list of entry widgets in tuples for the history log
text_log = [(tk.Entry(input_frame), tk.Entry(input_frame)) for _ in range(entry_num)]
i = 1
#configuring each entry widget in the log and placing them
for side, history in text_log:
    side.config(readonlybackground='#2D2D2D', fg='#F7C974', font=font, bd=0, highlightthickness=0)
    side.config(state='readonly')
    history.config(readonlybackground='#252525', fg='#E4F774', font=font, bd=0, highlightthickness=0)
    history.config(state='readonly')
    if settings['invert']:
        side.place(relx=0, rely=i*ENTRY_Y, width=25, relheight=ENTRY_HEIGHT)
        history.place(x=25, rely=i*ENTRY_Y, relwidth=0.90, relheight=ENTRY_HEIGHT)
    else:
        side.place(relx=0, rely=LOWEST_Y-i*ENTRY_Y, width=25, relheight=ENTRY_HEIGHT)
        history.place(x=25, rely=LOWEST_Y-i*ENTRY_Y, relwidth=0.90, relheight=ENTRY_HEIGHT)
    i += 1

#making the frame for the calendar display
displayFrame = tk.Frame(root, bg='#1C1C1C')
displayFrame.place(relx=0.3, rely=0, relwidth=0.7, relheight=1)

#setting root details
root.title('Calendar')
root.minsize(500, 500)

#mainloop
root.mainloop()