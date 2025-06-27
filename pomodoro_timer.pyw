import tkinter as tk
import math

# ---------------------------- CONSTANT ------------------------------- #
TOTAL_SECONDS = 25 * 60

# ---------------------------- STATE ------------------------------- #
timer_id = None        # after() handle
remaining = TOTAL_SECONDS
running = False        # is timer active?

# ---------------------------- RESET ------------------------------- #
def reset_timer():
    global timer_id, remaining, running
    if timer_id:
        window.after_cancel(timer_id)
        timer_id = None
    remaining = TOTAL_SECONDS
    running = False
    canvas.itemconfig(timer_text, text="25:00")
    start_button.config(text="Start")

# ---------------------------- TOGGLE START/PAUSE ------------------------------- #
def toggle_timer():
    global running
    if running:
        # pause
        window.after_cancel(timer_id)
        start_button.config(text="Start")
        running = False
    else:
        # start or resume
        start_button.config(text="Pause")
        running = True
        count_down()

# ---------------------------- COUNTDOWN ------------------------------- #
def count_down():
    global remaining, timer_id, running
    mins, secs = divmod(remaining, 60)
    canvas.itemconfig(timer_text, text=f"{mins:02d}:{secs:02d}")
    if remaining > 0 and running:
        remaining -= 1
        timer_id = window.after(1000, count_down)
    else:
        # finished
        running = False
        start_button.config(text="Start")

# ---------------------------- UI SETUP ------------------------------- #
window = tk.Tk()
window.title("Pomofocus")
window.config(padx=100, pady=50, bg="#e65065")  # Pink-red background

# Define colors
GREEN       = "#9bdeac"
WHITE       = "#ffffff"
PINK_RED    = "#e65065"  # Unified background color
TEXT_COLOR  = WHITE
BUTTON_TEXT = PINK_RED
BUTTON_BG   = WHITE

# Center everything in one column
window.columnconfigure(0, weight=1)

# Title
title_label = tk.Label(
    window,
    text="Pomodoro",
    fg=TEXT_COLOR,
    bg=PINK_RED,
    font=("Arial Rounded MT Bold", 50)
)
title_label.grid(column=0, row=0, pady=(0, 20))

# Timer canvas
canvas = tk.Canvas(
    window,
    width=600,
    height=200,
    bg=PINK_RED,
    highlightthickness=0
)
canvas.grid(column=0, row=1)

# Create timer_text at center
timer_text = canvas.create_text(
    0, 0,
    text="25:00",
    fill=TEXT_COLOR,
    font=("Arial Rounded MT Bold", 105, "bold")
)

def center_text(event=None):
    w = canvas.winfo_width()
    h = canvas.winfo_height()
    canvas.coords(timer_text, w/2, h/2)

canvas.bind("<Configure>", center_text)
canvas.after(1, center_text)

# Start/Pause button
start_button = tk.Button(
    window,
    text="Start",
    highlightthickness=0,
    command=toggle_timer,
    font=("Arial Rounded MT Bold", 20, "bold"),
    padx=20,
    pady=10,
    bg=BUTTON_BG,
    fg=BUTTON_TEXT
)
start_button.grid(column=0, row=2, pady=20)

# Reset button
reset_button = tk.Button(
    window,
    text="Reset",
    highlightthickness=0,
    command=reset_timer,
    font=("Arial Rounded MT Bold", 12),
    bg=BUTTON_BG,
    fg=BUTTON_TEXT
)
reset_button.grid(column=0, row=3)

window.mainloop()