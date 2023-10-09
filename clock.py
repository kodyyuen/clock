import tkinter as tk
import tkinter.ttk as ttk
from datetime import datetime, timedelta
import time
import pytz
import geocoder
import os
from PIL import Image, ImageTk
import pong

# Place windows on separate screens
# https://stackoverflow.com/questions/65007441/how-to-display-two-windows-in-two-different-display-with-tkinter

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
scores = []
end_screen = False
# location = geocoder.ip('me')

def change_color(top):
    widgets = [top]
    while len(widgets) > 0:
        wid = widgets.pop(0)
        for child in wid.winfo_children():
                if isinstance(child, tk.Label):
                    child.configure(fg=TEXT_COLOR)
                child.configure(bg=BACKGROUND_COLOR)
                widgets.append(child)

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
    
    window2.after(100, update_time)

# 500 400    500 400    500 400    500 400
# 600 600    600 200    300 600    300 200
def scale_photo(img):
    w, h = img.size
    # ratio = min(1280 / w, 400 / h)
    print('vrootwidth: ', window2.winfo_width())
    print('vrootheight: ', window2.winfo_height())

    ratio = min(window2.winfo_width() / w, window2.winfo_height() / h)
    w *= ratio
    h *= ratio
    return max(1, int(w)), max(1, int(h))

def update_photo():
    if frame == 2:
        global img_num
        img_num = (img_num + 1) % len(IMG_LIST)

        img = Image.open(f'images/{IMG_LIST[img_num]}')
        img = img.resize(scale_photo(img))
        photos_img = ImageTk.PhotoImage(img)
        photos_lbl_img.configure(image=photos_img)
        photos_lbl_img.image = photos_img

    window2.after(SLIDESHOW_TIME, update_photo)

def switch_frame(event = False):
    global frame
    frame = (frame + 1) % 4

    if frame == 0:
        game_frm.grid_forget()
        t_frm.grid(row=0, column=0, sticky='nsew')
    elif frame == 1:
        t_frm.grid_forget()
        visit_frm.grid(row=0, column=0, sticky='nsew')
    elif frame == 2:
        visit_frm.grid_forget()
        photos_frm.grid(row=0, column=0, sticky='nsew')
    elif frame == 3:
        photos_frm.grid_forget()

        play_again()
        game_frm.grid(row=0, column=0, sticky='nsew')

def play_again(event = False):
    global end_screen, game
    end_screen = False
    game = pong.Game(game_frm, scores)

# Animation loop
def move_ball():
    if frame == 3:
        global end_screen
        if not game.over():
            game.draw()
        elif not end_screen:
            scores.append(game.ball.score)
            game.over_screen()
            end_screen = True
    window2.after(10, move_ball)

### WINDOW
window2 = tk.Tk()
window2.title("Time In balls2")
window2.geometry("1280x400")
window2.rowconfigure(0, weight=1, minsize=400)
window2.columnconfigure(0, weight=1, minsize=1280)

window = tk.Toplevel(window2)
window.title("Time In balls")
window.geometry("1280x400")
window.rowconfigure(0, weight=1, minsize=400)
window.columnconfigure(0, weight=1, minsize=1280)


### NATALIA TIME
n_frm = tk.Frame(master=window)
n_frm.grid(row=0, column=0, sticky='nsew')

n_lbl_date = tk.Label(master=n_frm, text=get_current_date(NAT_TZ), font=(FONT, 30, "bold"))
n_lbl_date.place(relx=.5, rely=.2, anchor=tk.CENTER)

n_lbl_time = tk.Label(master=n_frm, text=get_current_time(NAT_TZ),  font=(FONT, 70, "bold"))
n_lbl_time.place(relx=.5, rely=.5, anchor=tk.CENTER)

n_lbl_loc = tk.Label(master=n_frm, text=NAT_CITY, font=(FONT, 30, "bold"))
n_lbl_loc.place(relx=.5, rely=.8, anchor=tk.CENTER)

n_img = Image.open('test.png')
n_img = n_img.resize(tuple(int(1.5 * x) for x in n_img.size))
n_img = ImageTk.PhotoImage(n_img)
n_lbl_img = tk.Label(master=n_frm, image=n_img, borderwidth=0)
n_lbl_img.place(relx=.15, rely=.5, anchor=tk.CENTER)


### EMPTY FRAME
# empty_frm = tk.Frame(master=window)
# empty_frm.grid(row=1, column=0, sticky='nsew')


### TIM TIME
t_frm = tk.Frame(master=window2)
# t_frm.grid(row=0, column=0, sticky='nsew')

t_lbl_date = tk.Label(master=t_frm, text=get_current_date(TIM_TZ), font=(FONT, 30, "bold"))
t_lbl_date.place(relx=.5, rely=.2, anchor=tk.CENTER)

t_lbl_time = tk.Label(master=t_frm, text=get_current_time(TIM_TZ), font=(FONT, 70, "bold"))
t_lbl_time.place(relx=.5, rely=.5, anchor=tk.CENTER)

t_lbl_loc = tk.Label(master=t_frm, text=TIM_CITY, font=(FONT, 30, "bold"))
t_lbl_loc.place(relx=.5, rely=.8, anchor=tk.CENTER)

t_img = Image.open('test.png')
t_img = ImageTk.PhotoImage(t_img)
t_lbl_img = tk.Label(master=t_frm, image=t_img, borderwidth=0)
t_lbl_img.place(relx=.15, rely=.5, anchor=tk.CENTER)



### VISIT
visit_frm = tk.Frame(master=window2)

visit_lbl_time = tk.Label(master=visit_frm, text='' if VISIT_DATE < datetime.now() else time_until_visit(), font=(FONT, 40, "bold"), foreground='white')
visit_lbl_time.place(relx=.5, rely=.45, anchor=tk.CENTER)

visit_lbl_text = tk.Label(master=visit_frm, text='' if VISIT_DATE < datetime.now() else 'Until Tim Visits', font=(FONT, 50, "bold"), foreground='white')
visit_lbl_text.place(relx=.5, rely=.7, anchor=tk.CENTER)

# visit_frm.place()

### SLIDESHOW
photos_frm = tk.Frame(master=window2)
img = Image.open(f'images/{IMG_LIST[img_num]}')
img = img.resize(scale_photo(img))
photos_img = ImageTk.PhotoImage(img)
photos_lbl_img = tk.Label(master=photos_frm, image=photos_img, borderwidth=0)
photos_lbl_img.place(relx=.5, rely=.5, anchor=tk.CENTER)

# photos_frm.place()

game_frm = tk.Frame(window2)
# game_frm.rowconfigure(0, weight=1, minsize=400)
# game_frm.columnconfigure(0, weight=1, minsize=300)
# game_frm.columnconfigure(1, weight=1, minsize=900)
game = pong.Game(game_frm, scores)

# change_color(window)
change_color(window2)

#REMOVE LATER
# empty_frm.configure(bg='white')
def exit_function():
    # Put any cleanup here.  
    window2.destroy()

# window.attributes('-fullscreen', True)
# window.state('zoomed')

window2.after(100, update_time)
window2.after(SLIDESHOW_TIME, update_photo)
window2.after(100, move_ball)
switch_frame()
window.bind_all('a', switch_frame)
# window2.bind('a', switch_frame)
window.bind_all('r', play_again)
# window2.bind('r', play_again)
window.protocol('WM_DELETE_WINDOW', exit_function)
window2.mainloop()
# window2.mainloop()