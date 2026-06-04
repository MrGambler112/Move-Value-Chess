from data import STARTING_POSITION, PIECE_TEXT
from move_rules import pawn_move, rook_move, bishop_move, queen_move, king_move, knight_move
import tkinter
import time


#window config
window = tkinter.Tk ()
window.geometry ("700x700")  #Dimensions in pixels
window.title ("Move Value Based Chess Engine")
window.attributes ("-topmost", True)
window.update_idletasks ()
window.attributes ("-topmost", False)
window.focus_force ()

#canvas widget in window
canvas = tkinter.Canvas (window, width = 700, height = 700, bg = "white")


selected_row = -1
selected_col = -1
SQUARE_SIZE = 60

def draw_board ():
    for row in range (8):
        for col in range (8):
            x1 = col * SQUARE_SIZE +  60
            y1 = row * SQUARE_SIZE + 60
            x2 = x1 + SQUARE_SIZE
            y2 = y1 + SQUARE_SIZE

            if ((row + col) % 2 == 0):
                COLOUR_1 = "grey"
            else:
                COLOUR_1 = "white"

            canvas.create_rectangle (x1, y1, x2, y2, fill = COLOUR_1, outline = "black")

            
    for row in range(8):
         y_center = row * SQUARE_SIZE + 60 + SQUARE_SIZE / 2
         canvas.create_text(40, y_center, text=str(8 - row), fill="black")
         canvas.create_text(560, y_center, text=str(8 - row), fill="black")
                 
                 
    for col in range(8):
        x_center = col * SQUARE_SIZE + 60 + SQUARE_SIZE / 2
        canvas.create_text(x_center, 40, text=chr(65 + col), fill="black") 
        canvas.create_text(x_center, 560, text=chr(65 + col), fill="black") 

                
def draw_pieces():
    for row in range(8):
        for col in range(8):
            piece = STARTING_POSITION[row][col]

            if (piece != ""):
                x_center = col * SQUARE_SIZE + 60 + SQUARE_SIZE / 2
                y_center = row * SQUARE_SIZE + 60 + SQUARE_SIZE / 2
                canvas.create_text(x_center, y_center, text=PIECE_TEXT[piece], font=("Arial", 32), fill="black")

def submit_move():
    global current_turn, last_time
    user_move = move_entry.get()

    if user_move[0] == "A":
        start_col = 0
    elif user_move[0] == "B":
        start_col = 1
    elif user_move[0] == "C":
        start_col = 2
    elif user_move[0] == "D":
        start_col = 3
    elif user_move[0] == "E":
        start_col = 4
    elif user_move[0] == "F":
        start_col = 5
    elif user_move[0] == "G":
        start_col = 6
    elif user_move[0] == "H":
        start_col = 7

    if user_move[2] == "A":
        end_col = 0
    elif user_move[2] == "B":
        end_col = 1
    elif user_move[2] == "C":
        end_col = 2
    elif user_move[2] == "D":
        end_col = 3
    elif user_move[2] == "E":
        end_col = 4
    elif user_move[2] == "F":
        end_col = 5
    elif user_move[2] == "G":
        end_col = 6
    elif user_move[2] == "H":
        end_col = 7

    start_row = 8 - int(user_move[1])
    end_row = 8 - int(user_move[3])

    legal_move = pawn_move(
        start_row,
        start_col,
        end_row,
        end_col,
        STARTING_POSITION
    )

    piece = STARTING_POSITION[start_row][start_col]

    legal_move = False

    if piece == "wp":
        legal_move = pawn_move(start_row, start_col, end_row, end_col, STARTING_POSITION)

    elif piece == "wr" or piece == "br":
        legal_move = rook_move(start_row, start_col, end_row, end_col, STARTING_POSITION)

    elif piece == "wb" or piece == "bb":
        legal_move = bishop_move(start_row, start_col, end_row, end_col, STARTING_POSITION)

    elif piece == "wq" or piece == "bq":
        legal_move = queen_move(start_row, start_col, end_row, end_col, STARTING_POSITION)

    elif piece == "wk" or piece == "bk":
        legal_move = king_move(start_row, start_col, end_row, end_col, STARTING_POSITION)

    elif piece == "wn" or piece == "bn":
        legal_move = knight_move(start_row, start_col, end_row, end_col, STARTING_POSITION)

    if legal_move == True:
        STARTING_POSITION[end_row][end_col] = STARTING_POSITION[start_row][start_col]
        STARTING_POSITION[start_row][start_col] = ""

        # Switch turn
        if current_turn == "white":
            current_turn = "black"
            turn_label.config(text="Black's turn", fg="black")
        else:
            current_turn = "white"
            turn_label.config(text="White's turn", fg="blue")
        last_time = time.time()

    draw_everything()

canvas.pack()

# Timer setup — 10-minute countdown for each player
TIME_LIMIT = 600  # 10 minutes in seconds
white_time = TIME_LIMIT
black_time = TIME_LIMIT
current_turn = "white"  # white moves first
timer_running = True

white_timer_label = tkinter.Label(window, text="White: 10:00", font=("Arial", 14), fg="black")
white_timer_label.place(x=60, y=10)
black_timer_label = tkinter.Label(window, text="Black: 10:00", font=("Arial", 14), fg="black")
black_timer_label.place(x=500, y=10)
turn_label = tkinter.Label(window, text="White's turn", font=("Arial", 12), fg="blue")
turn_label.place(x=290, y=35)

last_time = time.time()

def update_timers():
    global white_time, black_time, current_turn, last_time, timer_running
    if not timer_running:
        window.after(1000, update_timers)
        return

    now = time.time()
    delta = int(now - last_time)
    last_time = now

    if current_turn == "white":
        white_time -= delta
        if white_time <= 0:
            white_time = 0
            timer_running = False
            turn_label.config(text="Black wins! (White ran out of time)", fg="red")
    else:
        black_time -= delta
        if black_time <= 0:
            black_time = 0
            timer_running = False
            turn_label.config(text="White wins! (Black ran out of time)", fg="red")

    w_min = white_time // 60
    w_sec = white_time % 60
    b_min = black_time // 60
    b_sec = black_time % 60

    white_timer_label.config(text=f"White: {w_min:02d}:{w_sec:02d}")
    black_timer_label.config(text=f"Black: {b_min:02d}:{b_sec:02d}")

    window.after(1000, update_timers)

update_timers()

move_entry = tkinter.Entry(window, width=10)
move_entry.place(x=290, y=650)

move_button = tkinter.Button(window, text="Move", command=submit_move)
move_button.place(x=370, y=646)

def draw_everything():
    canvas.delete("all")
    draw_board()
    draw_pieces()

draw_everything()
window.mainloop()