# Simple pong game - don't let the ball hit the bottom!
# KidsCanCode - Intro to Programming
from tkinter import *
import random

# Define ball properties and functions
class Ball:
    def __init__(self, canvas, color, size, paddle):
        self.canvas = canvas
        self.paddle = paddle
        self.id = canvas.create_oval(10, 10, size, size, fill=color)
        self.canvas.move(self.id, 245, 100)
        self.xspeed = random.randrange(-3,3)
        self.yspeed = -1
        self.hit_bottom = False
        self.score = 0

    def draw(self):
        self.canvas.move(self.id, self.xspeed, self.yspeed)
        pos = self.canvas.coords(self.id)
        # print(pos)
        if pos[1] <= 0:
            self.yspeed = 3
        if pos[3] >= 400:
            self.hit_bottom = True
        if pos[0] <= 0:
            self.xspeed = 3
        if pos[2] >= 500:
            self.xspeed = -3
        if self.hit_paddle(pos):
            self.yspeed = -3
            self.xspeed = random.randrange(-3,3)
            self.score += 1

    def hit_paddle(self, pos):
        paddle_pos = self.canvas.coords(self.paddle.id)
        if pos[2] >= paddle_pos[0] and pos[0] <= paddle_pos[2]:
            if pos[3] >= paddle_pos[1] and pos[3] <= paddle_pos[3]:
                return True
        return False

# Define paddle properties and functions
class Paddle:
    def __init__(self, canvas, color):
        self.canvas = canvas
        self.id = canvas.create_rectangle(0,0, 100, 10, fill=color)
        self.canvas.move(self.id, 200, 300)
        self.xspeed = 0
        self.canvas.bind_all('<KeyPress-Left>', self.move_left)
        self.canvas.bind_all('<KeyPress-Right>', self.move_right)

    def draw(self):
        self.canvas.move(self.id, self.xspeed, 0)
        pos = self.canvas.coords(self.id)
        if pos[0] <= 0:
            self.xspeed = 0
        if pos[2] >= 500:
            self.xspeed = 0

    def move_left(self, evt):
        self.xspeed = -2
    def move_right(self, evt):
        self.xspeed = 2

class Game:
    def __init__(self, master, scores):
        self.canvas = Canvas(master, width=500, height=400, bd=0, bg='papaya whip')
        self.label = self.canvas.create_text(5, 5, anchor=NW, text="Score: 0")
        self.scoreboard = Text(master, width=30, height=20)
        self.paddle = Paddle(self.canvas, 'red')
        self.ball = Ball(self.canvas, 'blue', 25, self.paddle)
        self.scores = scores
        self.update_scoreboard()
        # self.scoreboard.grid(row=0, column=0)
        # self.canvas.grid(row=0, column=1)
        self.scoreboard.place(relx=.15, rely=.5, anchor=CENTER)
        self.canvas.place(relx=.5, rely=.5, anchor=CENTER)

    def draw(self):
        self.paddle.draw()
        self.ball.draw()
        self.canvas.itemconfig(self.label, text="Score: "+str(self.ball.score))

    def over(self):
        return self.ball.hit_bottom
    
    def over_screen(self):
        self.canvas.create_text(250,75,text="GAME OVER",font=("Helvetica",30))
        self.canvas.create_text(250,150,text=f'NEW HIGH SCORE: {self.ball.score}' if self.ball.score > self.scores[0] else f'SCORE: {self.ball.score}',font=("Helvetica",30))
        self.canvas.create_text(250,225,text="PRESS R TO PLAY AGAIN",font=("Helvetica",30))
        self.update_scoreboard()
    
    def update_scoreboard(self):
        self.scores.sort(reverse=True)
        self.scoreboard.delete("1.0", END)
        self.scoreboard.insert(END, "Rank     Name     Score")
        for i in range(0, len(self.scores)):
            self.scoreboard.insert(END, f'\n {i + 1}    worm girl     {self.scores[i]}')

# Create window and canvas to draw on
# tk = Tk()
# tk.title("Ball Game")
# canvas = Canvas(tk, width=500, height=400, bd=0, bg='papaya whip')
# canvas.pack()
# label = canvas.create_text(5, 5, anchor=NW, text="Score: 0")
# tk.update()
# paddle = Paddle(canvas, 'blue')
# ball = Ball(canvas, 'red', 25, paddle)

# # Animation loop
# while ball.hit_bottom == False:
#     ball.draw()
#     paddle.draw()
#     canvas.itemconfig(label, text="Score: "+str(ball.score))
#     tk.update_idletasks()
#     tk.update()
#     time.sleep(0.01)

# # Game Over
# go_label = canvas.create_text(250,200,text="GAME OVER",font=("Helvetica",30))
# tk.update()