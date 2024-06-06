from tkinter import *
import random

# Constants
WIDTH = 900
HEIGHT = 300
PAD_W = 10
PAD_H = 100
BALL_SPEED_UP = 1.05
BALL_MAX_SPEED = 40
BALL_RADIUS = 30
INITIAL_SPEED = 20
BALL_X_SPEED = INITIAL_SPEED
BALL_Y_SPEED = INITIAL_SPEED
PLAYER_1_SCORE = 0
PLAYER_2_SCORE = 0

# Functions
def update_score(player):
    global PLAYER_1_SCORE, PLAYER_2_SCORE
    if player == "right": 
        PLAYER_1_SCORE += 1
        c.itemconfig(p_1_text, text=PLAYER_1_SCORE)
    else:
        PLAYER_2_SCORE += 1
        c.itemconfig(p_2_text, text=PLAYER_2_SCORE)

def spawn_ball():
    global BALL_X_SPEED, BALL_Y_SPEED
    c.coords(BALL, WIDTH/2-BALL_RADIUS/2, HEIGHT/2-BALL_RADIUS/2, WIDTH/2+BALL_RADIUS/2, HEIGHT/2+BALL_RADIUS/2)
    BALL_X_SPEED = INITIAL_SPEED if random.choice([True, False]) else -INITIAL_SPEED
    BALL_Y_SPEED = random.choice([-INITIAL_SPEED, INITIAL_SPEED])

def bounce(action):
    global BALL_X_SPEED, BALL_Y_SPEED
    if action == "strike":
        BALL_Y_SPEED = random.randrange(-10, 10)
        if abs(BALL_X_SPEED) < BALL_MAX_SPEED:
            BALL_X_SPEED *= -BALL_SPEED_UP
        else:
            BALL_X_SPEED = -BALL_X_SPEED
    else:
        BALL_Y_SPEED = -BALL_Y_SPEED

def move_ball():
    ball_left, ball_top, ball_right, ball_bottom = c.coords(BALL)
    ball_center = (ball_top + ball_bottom) / 2
    
    # Move ball
    c.move(BALL, BALL_X_SPEED, BALL_Y_SPEED)
    
    # Ball collision with top and bottom
    if ball_top <= 0 or ball_bottom >= HEIGHT:
        bounce("ricochet")
    
    # Ball collision with paddles
    if ball_right >= WIDTH - PAD_W and c.coords(RIGHT_PAD)[1] <= ball_center <= c.coords(RIGHT_PAD)[3]:
        bounce("strike")
    elif ball_left <= PAD_W and c.coords(LEFT_PAD)[1] <= ball_center <= c.coords(LEFT_PAD)[3]:
        bounce("strike")
    
    # Ball out of bounds
    if ball_right >= WIDTH:
        update_score("left")
        game_over()
    elif ball_left <= 0:
        update_score("right")
        game_over()
    
    # Continue moving the ball if the game is not over
    if ball_left > 0 and ball_right < WIDTH:
        root.after(30, move_ball)

def move_paddle(event):
    paddle_speed = 20
    if event.keysym == 'w':
        if c.coords(LEFT_PAD)[1] > 0:
            c.move(LEFT_PAD, 0, -paddle_speed)
    elif event.keysym == 's':
        if c.coords(LEFT_PAD)[3] < HEIGHT:
            c.move(LEFT_PAD, 0, paddle_speed)
    elif event.keysym == 'Up':
        if c.coords(RIGHT_PAD)[1] > 0:
            c.move(RIGHT_PAD, 0, -paddle_speed)
    elif event.keysym == 'Down':
        if c.coords(RIGHT_PAD)[3] < HEIGHT:
            c.move(RIGHT_PAD, 0, paddle_speed)

def game_over():
    global BALL_X_SPEED, BALL_Y_SPEED
    BALL_X_SPEED = 0
    BALL_Y_SPEED = 0
    c.create_text(WIDTH/2, HEIGHT/2 - 20, text="Game Over", font="Arial 40", fill="red")
    play_again_button = Button(root, text="Play Again", command=play_again)
    quit_button = Button(root, text="Quit", command=root.quit)
    c.create_window(WIDTH/2, HEIGHT/2 + 20, window=play_again_button)
    c.create_window(WIDTH/2, HEIGHT/2 + 60, window=quit_button)
    root.bind('<KeyPress-p>', lambda event: play_again())
    root.bind('<KeyPress-q>', lambda event: root.quit())

def play_again():
    global PLAYER_1_SCORE, PLAYER_2_SCORE, BALL_X_SPEED, BALL_Y_SPEED
    PLAYER_1_SCORE = 0
    PLAYER_2_SCORE = 0
    c.itemconfig(p_1_text, text=PLAYER_1_SCORE)
    c.itemconfig(p_2_text, text=PLAYER_2_SCORE)
    c.delete("all")
    setup_game()
    spawn_ball()
    move_ball()

def setup_game():
    c.create_line(PAD_W, 0, PAD_W, HEIGHT, fill="white")
    c.create_line(WIDTH-PAD_W, 0, WIDTH-PAD_W, HEIGHT, fill="white")
    c.create_line(WIDTH/2, 0, WIDTH/2, HEIGHT, fill="white")

    global BALL, LEFT_PAD, RIGHT_PAD, p_1_text, p_2_text
    BALL = c.create_oval(WIDTH/2-BALL_RADIUS/2, HEIGHT/2-BALL_RADIUS/2, WIDTH/2+BALL_RADIUS/2, HEIGHT/2+BALL_RADIUS/2, fill="white")
    LEFT_PAD = c.create_line(PAD_W/2, 0, PAD_W/2, PAD_H, width=PAD_W, fill="yellow")
    RIGHT_PAD = c.create_line(WIDTH-PAD_W/2, 0, WIDTH-PAD_W/2, PAD_H, width=PAD_W, fill="yellow")

    p_1_text = c.create_text(WIDTH-WIDTH/6, PAD_H/4, text=PLAYER_1_SCORE, font="Arial 20", fill="white")
    p_2_text = c.create_text(WIDTH/6, PAD_H/4, text=PLAYER_2_SCORE, font="Arial 20", fill="white")

# Initialize game
root = Tk()
root.title("Pong")

c = Canvas(root, width=WIDTH, height=HEIGHT, background="#003300")
c.pack()

# Bind keys
root.bind('<KeyPress>', move_paddle)

# Setup and start game
setup_game()
spawn_ball()
move_ball()

root.mainloop()
