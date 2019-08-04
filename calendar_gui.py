import tkinter as tk, tkinter.font as TkFont
import math
import json
import copy

#delcaring heights entry widgets
LOWEST_Y = 0.97 #relative y in window for the lowest entry widget
ENTRY_HEIGHT = 0.03 
ENTRY_Y = 0.03 #relative height of entry widgets
WEEK = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']

class Inputbar(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        #making the sidebar and the main input widget
        self.sidebar = tk.Entry(self)
        self.entry = tk.Text(self)
        self.sidebar.config(readonlybackground='#536F7B', fg='#11242F', font=parent.font, bd=0, highlightthickness=0)
        self.sidebar.insert(0, parent.settings['indicator'])
        self.sidebar.config(state='readonly')
        self.entry.config(bg='#536F7B', fg='#11242F', font=parent.font, bd=0, highlightthickness=0)
        self.entry.config(insertbackground='#11242F', blockcursor=True, wrap='none')
        #if invert is true in settings, history goes top (most recent) to bottom (oldest)
        if parent.settings['invert']:
            self.sidebar.place(relx=0, rely=0, width=25, relheight=1-LOWEST_Y)
            self.entry.place(x=25, rely=0, relwidth=0.93, relheight=1-LOWEST_Y)
        #otherwise, history goes bottom (most recent) to top (oldest)
        else:
            self.sidebar.place(relx=0, rely=LOWEST_Y, width=25, relheight=1-LOWEST_Y)
            self.entry.place(x=25, rely=LOWEST_Y, relwidth=0.93, relheight=1-LOWEST_Y)
        self.entry.focus_set()
        #finding the number of entry widgets necesarry for the history log
        entry_num = int(math.ceil(LOWEST_Y/ENTRY_HEIGHT))

        #making the list of entry widgets in tuples for the history log
        self.text_log = [(tk.Entry(self), tk.Entry(self)) for _ in range(entry_num)]
        i = 1
        #configuring each entry widget in the log and placing them
        for side, history in self.text_log:
            side.config(readonlybackground='#11242F', fg='#536F7B', font=parent.font, bd=0, highlightthickness=0)
            side.config(state='readonly')
            history.config(readonlybackground='#151515', fg='#536F7B', font=parent.font, bd=0, highlightthickness=0)
            history.config(state='readonly')
            if parent.settings['invert']:
                side.place(relx=0, rely=i*ENTRY_Y, width=25, relheight=ENTRY_HEIGHT)
                history.place(x=25, rely=i*ENTRY_Y, relwidth=0.90, relheight=ENTRY_HEIGHT)
            else:
                side.place(relx=0, rely=LOWEST_Y-i*ENTRY_Y, width=25, relheight=ENTRY_HEIGHT)
                history.place(x=25, rely=LOWEST_Y-i*ENTRY_Y, relwidth=0.90, relheight=ENTRY_HEIGHT)
            i += 1
        
        #takes a string for log a string for the side bar, moves all strings up the history
    def move_history(self, text: str, side: str) -> None:
        temp_r1 = text
        temp_l1 = side
        #iterating through history of text log and moving the text and side to the next
        for side, history in self.text_log:
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
        self.entry.delete('1.0', tk.END)

class CalendarDisplay(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.month_label = tk.Label(self, bg ='#000000', text='July 2019', anchor='w', font=parent.month_font, padx=5)
        self.month_label.config(fg='#3D7D9F')
        self.month_label.place(relx=0, rely=0, relwidth=1, relheight=.1)
        self.days_labels = [tk.Label(self, bg='#11242F', fg='#30759F', font=parent.font, text=day) for day in WEEK]
        i = 0
        split_across = 1/7
        for day in self.days_labels:
            day.place(relx=split_across*i, rely=.1, relwidth=split_across, relheight=0.05)
            i += 1
        split_down = (1-.15)/6
        dates_list = []
        k = 0
        for i in range(6):
            for j in range(7):
                dates_list.append(tk.Label(self, bg='#151515', anchor='ne', justify='right', bd=2))
                dates_list[k].config(text=k, font=parent.cal_font, fg='#536F7B', relief=None)
                if k%7 == 0 or k%7 == 6:
                    dates_list[k].config(bg='#121212')
                dates_list[k].place(relx=j*split_across, rely=.15+i*split_down, relwidth=split_across, relheight=split_down)
                k += 1

class MainApp(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        with open('settings.json') as f: #opening the settings.json file
            self.settings = json.load(f)
        self.config(height=self.settings['window']['height'], width=self.settings['window']['width'])
        self.font = (self.settings['font']['type'], self.settings['font']['size'])
        self.cal_font = (self.settings['font']['type'], self.settings['font']['size'] + 3)
        self.month_font = ('Arial', self.font[1]+15)
        self.inputbar = Inputbar(self, bg='#151515')
        self.calendar_display = CalendarDisplay(self, bg='#1C1C1C')
        self.inputbar.place(relx=0, rely=0, relwidth=0.25, relheight=1)
        self.calendar_display.place(relx=0.25, rely=0, relwidth=0.75, relheight=1)
        parent.bind('<Return>', func=self.handle_command)

    def handle_command(self, event=None) -> None: 
        input_ = self.inputbar.entry.get('1.0', tk.END)
        self.inputbar.move_history(input_, self.settings['indicator'])

if __name__ == '__main__':
    root = tk.Tk()
    root.title('Calendar')
    root.minsize(700, 500)
    MainApp(root).pack(side="top", fill="both", expand=True)
    root.mainloop()