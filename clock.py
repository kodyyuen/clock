import tkinter as tk
import tkinter.ttk as ttk
from datetime import datetime, timedelta
import time
import pytz
import geocoder
import os
from PIL import Image, ImageTk

# Timezones
# https://gist.github.com/heyalexej/8bf688fd67d7199be4a1682b3eec7568
NAT_TZ = "Europe/Madrid"
NAT_CITY = "Barcelona"
TIM_TZ = "America/New_York"
TIM_CITY = "Boston"
VISIT_DATE = datetime(2023, 10, 22)
SLIDESHOW_TIME = 2000 # in ms
BACKGROUND_COLOR = "#3f3e3e"
TEXT_COLOR = "white"
FONT = "Arial" # https://stackoverflow.com/questions/39614027/list-available-font-families-in-tkinter
IMG_LIST = os.listdir('./images')
img_num = 0
frame = -1
# location = geocoder.ip('me')

def change_color():
    window.configure(bg=BACKGROUND_COLOR)
    for frm in window.winfo_children():
        frm.configure(bg=BACKGROUND_COLOR)
        for wid in frm.winfo_children():
            wid.configure(bg=BACKGROUND_COLOR, fg=TEXT_COLOR)

def get_current_time(loc):
    return datetime.now(pytz.timezone(loc)).strftime("%#I:%M:%S %p")

def get_current_date(loc):
    return datetime.now(pytz.timezone(loc)).strftime("%A, %B %#d")

def time_until_visit():
    td = VISIT_DATE - datetime.now()
    delta = time.gmtime(td.total_seconds())
    return f'{td.days} days, ' + format(time.strftime('%#H hours, %#M minutes, %#S seconds', delta))

def update_time():
    n_lbl_time['text'] = get_current_time(NAT_TZ)
    if frame == 0:
        t_lbl_time['text'] = get_current_time(TIM_TZ)
    elif frame == 1:
        if VISIT_DATE < datetime.now():
            visit_lbl_text['text'] = ''
            visit_lbl_time['text'] = 'Tim is here!'
            visit_lbl_time.configure(font=(FONT, 80, "bold"))
            visit_lbl_time.place(relx=.5, rely=.5, anchor=tk.CENTER)
        else:
            visit_lbl_time['text'] = time_until_visit()
    
    window.after(100, update_time)

# 500 400    500 400    500 400    500 400
# 600 600    600 200    300 600    300 200
def scale_photo(img):
    w, h = img.size
    ratio = min(1280 / w, 400 / h)
    w *= ratio
    h *= ratio
    return int(w), int(h)

def update_photo():
    global img_num
    img_num = (img_num + 1) % len(IMG_LIST)

    img = Image.open(f'images/{IMG_LIST[img_num]}')
    img = img.resize(scale_photo(img))
    photos_img = ImageTk.PhotoImage(img)
    photos_lbl_img.configure(image=photos_img)
    photos_lbl_img.image = photos_img

    window.after(SLIDESHOW_TIME, update_photo)

def switch_frame(event = False):
    global frame
    frame = (frame + 1) % 3

    if frame == 0:
        photos_frm.grid_forget()
        t_frm.grid(row=2, column=0, sticky='nsew')
    elif frame == 1:
        t_frm.grid_forget()
        visit_frm.grid(row=2, column=0, sticky='nsew')
    else:
        visit_frm.grid_forget()
        photos_frm.grid(row=2, column=0, sticky='nsew')


### WINDOW
window = tk.Tk()
window.title("Time In balls")
window.geometry("1280x960")
window.rowconfigure([0, 2], minsize=400)
window.rowconfigure(1, minsize=160)
window.columnconfigure(0, minsize=1280)


### NATALIA TIME
n_frm = tk.Frame(master=window)
n_frm.grid(row=0, column=0, sticky='nsew')

n_lbl_date = tk.Label(master=n_frm, text=get_current_date(NAT_TZ), font=(FONT, 30, "bold"), foreground='white')
n_lbl_date.place(relx=.5, rely=.2, anchor=tk.CENTER)

n_lbl_time = tk.Label(master=n_frm, text=get_current_time(NAT_TZ),  font=(FONT, 70, "bold"), foreground='white')
n_lbl_time.place(relx=.5, rely=.5, anchor=tk.CENTER)

n_lbl_loc = tk.Label(master=n_frm, text=NAT_CITY, font=(FONT, 30, "bold"), foreground='white')
n_lbl_loc.place(relx=.5, rely=.8, anchor=tk.CENTER)

n_img = Image.open('test.png')
n_img = n_img.resize(tuple(int(1.5 * x) for x in n_img.size))
n_img = ImageTk.PhotoImage(n_img)
n_lbl_img = tk.Label(master=n_frm, image=n_img, borderwidth=0)
n_lbl_img.place(relx=.15, rely=.5, anchor=tk.CENTER)


### EMPTY FRAME
empty_frm = tk.Frame(master=window)
empty_frm.grid(row=1, column=0, sticky='nsew')


### TIM TIME
t_frm = tk.Frame(master=window)

t_lbl_date = tk.Label(master=t_frm, text=get_current_date(TIM_TZ), font=(FONT, 30, "bold"), foreground='white')
t_lbl_date.place(relx=.5, rely=.2, anchor=tk.CENTER)

t_lbl_time = tk.Label(master=t_frm, text=get_current_time(TIM_TZ), font=(FONT, 70, "bold"), foreground='white')
t_lbl_time.place(relx=.5, rely=.5, anchor=tk.CENTER)

t_lbl_loc = tk.Label(master=t_frm, text=TIM_CITY, font=(FONT, 30, "bold"), foreground='white')
t_lbl_loc.place(relx=.5, rely=.8, anchor=tk.CENTER)

t_img = Image.open('test.png')
t_img = ImageTk.PhotoImage(t_img)
t_lbl_img = tk.Label(master=t_frm, image=t_img, borderwidth=0)
t_lbl_img.place(relx=.15, rely=.5, anchor=tk.CENTER)


### VISIT
visit_frm = tk.Frame(master=window)

visit_lbl_time = tk.Label(master=visit_frm, text='' if VISIT_DATE < datetime.now() else time_until_visit(), font=(FONT, 40, "bold"), foreground='white')
visit_lbl_time.place(relx=.5, rely=.45, anchor=tk.CENTER)

visit_lbl_text = tk.Label(master=visit_frm, text='' if VISIT_DATE < datetime.now() else 'Until Tim Visits', font=(FONT, 50, "bold"), foreground='white')
visit_lbl_text.place(relx=.5, rely=.7, anchor=tk.CENTER)


### SLIDESHOW
photos_frm = tk.Frame(master=window)
img = Image.open(f'images/{IMG_LIST[img_num]}')
img = img.resize(scale_photo(img))
photos_img = ImageTk.PhotoImage(img)
photos_lbl_img = tk.Label(master=photos_frm, image=photos_img, borderwidth=0)
photos_lbl_img.place(relx=.5, rely=.5, anchor=tk.CENTER)


change_color()

#REMOVE LATER
empty_frm.configure(bg='white')

window.after(100, update_time)
window.after(SLIDESHOW_TIME, update_photo)
switch_frame()
window.bind('a', switch_frame)
window.mainloop()