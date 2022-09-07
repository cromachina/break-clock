import math
import tkinter as tk
from datetime import datetime

import schedule

# Escape key to quit
# Left click to dismiss alarm
# Right click to drag the window

def create_alarm_schedule():
    schedule.every().hour.at(':00').do(start_alarm)
    schedule.every().hour.at(':30').do(start_alarm)

compact_mode = False
alarm_flash_duration_mins = 5
smooth_second = False
smooth_minute = True
window_opacity = 0.9
window_always_on_top = True
window_hide_menu_bar = True
alarm_color = '#ff3333'
face_color = 'black'
face_background_color = 'gray75'
second_color = 'black'
minute_color = 'blue'
hour_color = 'blue'

win = tk.Tk()
win.geometry('100x100-0-0')
win.overrideredirect(window_hide_menu_bar)
win.attributes('-topmost', window_always_on_top)
win.attributes('-alpha', window_opacity)

canvas = tk.Canvas(win, width=100, height=100, background=face_background_color)
canvas.pack(fill=tk.BOTH, expand=True)
center = (50, 50)
alarm_running = False

def draw_hand(value, length, width, color, start_length=0):
    value = (value * math.tau) - (math.pi / 2)
    x = math.cos(value)
    y = math.sin(value)
    line = canvas.create_line(start_length * x, start_length * y, length * x, length * y, width=width, fill=color)
    canvas.move(line, *center)

def draw_hour_tick(value):
    draw_hand(value / 12, 45, 2, face_color, 40)

def draw_large_clock():
    win.geometry('100x100')
    now = datetime.now()
    if alarm_running and now.second % 2 == 0:
            canvas.create_rectangle(0, 0, 100, 100, fill=alarm_color)
    # Draw clock face
    canvas.create_text(50, 10, text="12", font='bold', fill=face_color)
    canvas.create_text(90, 50, text="3", font='bold', fill=face_color)
    canvas.create_text(50, 90, text="6", font='bold', fill=face_color)
    canvas.create_text(10, 50, text="9", font='bold', fill=face_color)
    for h in range(12):
        if h % 3 != 0:
            draw_hour_tick(h)
    # Draw date
    canvas.create_text(50, 35, text=now.strftime('%Y/%m/%d'), justify='center', fill=face_color)
    canvas.create_text(50, 60, text=now.strftime('%a'), justify='center', fill=face_color)
    canvas.create_text(50, 75, text=now.strftime('%p'), justify='center', fill=face_color)
    # Draw clock hands
    second = now.second / 60
    if smooth_second:
        second += now.microsecond / 1000000 / 60
    minute = now.minute / 60
    if smooth_minute:
        minute += second / 60
    draw_hand((now.hour / 12) + (minute / 12), 30, 2, hour_color)
    draw_hand(minute, 50, 2, minute_color)
    draw_hand(second, 50, 1, second_color)

def draw_compact_clock():
    win.geometry('100x24')
    now = datetime.now()
    if alarm_running and now.second % 2 == 0:
        canvas.create_rectangle(0, 0, 100, 100, fill=alarm_color)
    canvas.create_text(50, 12, text=now.strftime('%I:%M:%S %p %a'), justify='center', fill=face_color)

def draw_loop():
    canvas.delete(tk.ALL)
    if compact_mode:
        draw_compact_clock()
    else:
        draw_large_clock()
    win.after(200, draw_loop)

def dismiss_alarm():
    global alarm_running
    alarm_running = False

def start_alarm():
    global alarm_running
    alarm_running = True
    win.after(1000 * 60 * alarm_flash_duration_mins, dismiss_alarm)

def check_schedule_loop():
    schedule.run_pending()
    win.after(1000, check_schedule_loop)

def change_mode():
    global compact_mode
    compact_mode = not compact_mode

win.bind('<Button-1>', lambda _: dismiss_alarm())
win.bind('<Escape>', lambda _: win.quit())
win.bind('q', lambda _: change_mode())

class MakeDraggable():
    def __init__(self, window):
        self.window = window
        window.bind('<ButtonPress-3>', self.start_move)
        window.bind('<B3-Motion>', self.do_move)

    def start_move(self, event):
        self.x = event.x
        self.y = event.y

    def do_move(self, event):
        dx = event.x - self.x
        dy = event.y - self.y
        x = self.window.winfo_x() + dx
        y = self.window.winfo_y() + dy
        self.window.geometry(f'+{x}+{y}')

MakeDraggable(win)
draw_loop()
create_alarm_schedule()
check_schedule_loop()
tk.mainloop()
