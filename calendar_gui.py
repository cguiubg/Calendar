import tkinter as tk, tkinter.font as TkFont
import math
import json
import datetime
import calendar_sup as sup

#delcaring heights entry widgets
LOWEST_Y = 0.97 #relative y in window for the lowest entry widget
ENTRY_HEIGHT = 0.03 
ENTRY_Y = 0.03 #relative height of entry widgets
WEEK = {'Sunday': 0, 'Monday': 1, 'Tuesday': 2, 'Wednesday': 3, 'Thursday': 4, 'Friday': 5, 'Saturday': 6}
YEAR = [(1, 'January'), (2, 'February'), (3, 'March'), (4, 'April'), (5, 'May'), (6, 'June'), (7, 'July'), (8, 'August'), (9, 'September'), (10, 'October'), (11, 'November'), (12, 'December')]

#making the sidebar and the main input widget
class Inputbar(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
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

#Main display for calendar and events
class CalendarDisplay(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.month_label = tk.Label(self, bg ='#000000', anchor='w', font=parent.month_font, padx=5)
        self.month_label.config(fg='#3D7D9F')
        self.month_label.place(relx=0, rely=0, relwidth=1, relheight=.1)
        self.days_labels = [tk.Label(self, bg='#11242F', fg='#30759F', font=parent.font, text=day) for day in WEEK.keys()]
        i = 0
        split_across = 1/7
        #builds and places top bar for days in week
        for day in self.days_labels:
            day.place(relx=split_across*i, rely=.1, relwidth=split_across, relheight=0.05)
            i += 1
        split_down = (1-.15)/6
        self.dates_list = []
        k = 0
        #builds and places 42 date squares in calender
        for i in range(6):
            for j in range(7):
                self.dates_list.append(tk.Label(self, bg='#151515', anchor='ne', justify='right', bd=2))
                self.dates_list[k].config(font=parent.cal_font, fg='#536F7B', relief=None)
                if k%7 == 0 or k%7 == 6:
                    self.dates_list[k].config(bg='#121212')
                self.dates_list[k].place(relx=j*split_across, rely=.15+i*split_down, relwidth=split_across, relheight=split_down)
                k += 1
        self.display_events(parent.display_date.month, parent.display_date.year)
        
    def display_events(self, month_index: int, year: int) -> None:
        date = datetime.datetime(year, month_index, 1)
        month = date.strftime('%B')
        year = date.strftime('%Y')
        self.month_label.config(text=date.strftime('%Y %B'))
        with open('months.json') as f:
            events_file = json.load(f)
        events = events_file[month]["years"][year]
        max_days = events_file[month]['days']
        start = WEEK[date.strftime('%A')]
        k = 0
        day_num = 1
        for _ in range(6):
            for _ in range(7):
                if k < start or k > start + max_days - 1:
                    self.dates_list[k].config(text='')
                else:
                    day_num_str = str(day_num)
                    events_in_day = events.get(day_num_str)
                    if events_in_day is not None : 
                        events_str = day_num_str + '\n' + '\n'.join(events_in_day)
                    else:
                        events_str = day_num_str + '\n'
                    self.dates_list[k].config(text=events_str)
                    day_num += 1
                k += 1
            

#parent class for two classes defined above, main frame of root
class MainApp(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        with open('settings.json') as f: #opening the settings.json file
            self.settings = json.load(f)
        self.display_date = datetime.datetime.today()
        self.config(height=self.settings['window']['height'], width=self.settings['window']['width'])
        self.font = (self.settings['font']['type'], self.settings['font']['size'])
        self.cal_font = (self.settings['font']['type'], self.settings['font']['size'] + 3)
        self.month_font = ('Arial', self.font[1]+15)
        self.inputbar = Inputbar(self, bg='#151515')
        self.calendar_display = CalendarDisplay(self, bg='#1C1C1C')
        self.inputbar.place(relx=0, rely=0, relwidth=0.25, relheight=1)
        self.calendar_display.place(relx=0.25, rely=0, relwidth=0.75, relheight=1)
        parent.bind('<Return>', func=self.update)

    #takes input from Inputbar and passes to Inputbar methods
    def update(self, event=None) -> None: 
        input_ = self.inputbar.entry.get('1.0', tk.END).split()
        update_str = sup.process(input_)
        if update_str[0] is 'c':
            date = datetime.date(update_str[2], update_str[3], 1)
            self.display_date = date
            self.calendar_display.display_events(date.month, date.year)
            self.inputbar.move_history(update_str[1], self.settings['indicator'])
            return
        else:
            self.calendar_display.display_events(self.display_date.month, self.display_date.year)
            self.inputbar.move_history(update_str[1], self.settings['indicator'])

#main
if __name__ == '__main__':
    root = tk.Tk()
    root.title('Calendar')
    root.minsize(700, 500)
    MainApp(root).pack(side="top", fill="both", expand=True)
    root.mainloop()