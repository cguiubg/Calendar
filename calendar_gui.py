import tkinter as tk, tkinter.font as TkFont
import math
import json
import copy

#delcaring heights entry widgets
LOWEST_Y = 0.97 #relative y in window for the lowest entry widget
ENTRY_HEIGHT = 0.03 
ENTRY_Y = 0.03 #relative height of entry widgets

with open('settings.json') as f: #opening the settings.json file
    settings = json.load(f)

#commands are passed here and then sent to the needed function
def handle_command(event=None) -> None: 
    input_ = entry.get()
    if('august' in input_):
        month_label.config(text='august')
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
root.bind('<Return>', func=handle_command)

#creating the canvas
canvas = tk.Canvas(root, height=settings['window']['height'], width=settings['window']['width'])
canvas.pack()

#getting the font tuple from the settings.json
font = (settings['font']['type'], settings['font']['size'])
cal_font = (settings['font']['type'], settings['font']['size'] + 3)

#making the frame where input is displayed
input_frame = tk.Frame(root, bg='#151515')
input_frame.config()
input_frame.place(relx=0, rely=0, relwidth=0.25, relheight=1)

#making the sidebar and the main input widget
sidebar = tk.Entry(input_frame)
entry = tk.Entry(input_frame)
sidebar.config(readonlybackground='#536F7B', fg='#11242F', font=font, bd=0, highlightthickness=0)
sidebar.insert(0, settings['indicator'])
sidebar.config(state='readonly')
entry.config(bg='#536F7B', fg='#11242F', font=font, bd=0, highlightthickness=0)
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
    side.config(readonlybackground='#11242F', fg='#536F7B', font=font, bd=0, highlightthickness=0)
    side.config(state='readonly')
    history.config(readonlybackground='#151515', fg='#536F7B', font=font, bd=0, highlightthickness=0)
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
displayFrame.place(relx=0.25, rely=0, relwidth=0.75, relheight=1)

print(TkFont.families())
month_font = ('Geeza Pro', font[1]+15)
month_label = tk.Label(displayFrame, bg ='#000000', text='July 2019', anchor='w', font=month_font, padx=5)
month_label.config(fg='#2D6D96')
month_label.place(relx=0, rely=0, relwidth=1, relheight=.1)

week = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']

days_labels = [tk.Label(displayFrame, bg='#11242F', fg='#30759F', font=font, text=day) for day in week]
i = 0
split_across = 1/7
for day in days_labels:
    day.place(relx=split_across*i, rely=.1, relwidth=split_across, relheight=0.05)
    i += 1

split_down = (1-.15)/6
dates_list = []

k = 0
for i in range(6):
    for j in range(7):
        dates_list.append(tk.Label(displayFrame, bg='#151515', anchor='ne', justify='right', bd=2))
        dates_list[k].config(text=k, font=cal_font, fg='#536F7B', relief=None)
        if k%7 == 0 or k%7 == 6:
            dates_list[k].config(bg='#121212')
        dates_list[k].place(relx=j*split_across, rely=.15+i*split_down, relwidth=split_across, relheight=split_down)
        k += 1

#setting root details
root.title('Calendar')
root.minsize(700, 500)

#mainloop
root.mainloop()