#Name: Move Value Based Chess Engine
#Programmer: Syed (Mahadi) Masuduzzaman
#Date: June 10, 2026
#Description: This program lets the user play chess against an AI
#             that chooses the move with the best move value.

from data import STARTING_POSITION, PIECE_TEXT
from move_rules import is_legal_move
import game_state
from game_state import record_capture, record_move, reset_game_state, set_player_color
from game_state import set_ai_target_score, check_ai_target_reached, check_player_target_reached
from game_state import get_player_capture_string, get_ai_capture_string
from game_state import get_player_score, get_ai_score
from game_state import set_game_result, save_match_to_file, get_lifetime_stats_string
from game_state import should_do_random_promotion, set_random_promotion_done
from board_logic import is_checkmate, is_stalemate, would_be_in_check
from ai_engine import get_ai_move_info
import time
import tkinter
import random


#window setup
window = tkinter.Tk ()
window.geometry ("700x700")
window.title ("Move Value Based Chess Engine")
window.attributes ("-topmost", True)
window.update_idletasks ()
window.attributes ("-topmost", False)
window.focus_force ()

canvas = tkinter.Canvas (window, width = 700, height = 700, bg = "white")


#board constants
SQUARE_SIZE = 60
BOARD_OFFSET_X = 110
BOARD_OFFSET_Y = 100
TIME_LIMIT = 600


#widget variables
white_timer_label = ""
ai_timer_label = ""
turn_label = ""
info_label = ""
score_label = ""
player_captured_label = ""
ai_captured_label = ""
status_label = ""
score_entry = ""
move_entry = ""
start_button = ""
move_button = ""
exit_button = ""
setup_widgets = []
game_widgets = []


#game variables
game_started = False
timer_running = True
white_time = TIME_LIMIT
ai_time = TIME_LIMIT
current_turn = "white"
last_time = time.time ()
game_over_screen_showing = False


#column letter conversion
def col_to_letter(col) :

    if col == 0 :
        return "A"
    elif col == 1 :
        return "B"
    elif col == 2 :
        return "C"
    elif col == 3 :
        return "D"
    elif col == 4 :
        return "E"
    elif col == 5 :
        return "F"
    elif col == 6 :
        return "G"
    elif col == 7 :
        return "H"
    else :
        return "?"


#convert lowercase input letters to uppercase
def to_upper_case(letter) :

    if letter == "a" :
        return "A"
    elif letter == "b" :
        return "B"
    elif letter == "c" :
        return "C"
    elif letter == "d" :
        return "D"
    elif letter == "e" :
        return "E"
    elif letter == "f" :
        return "F"
    elif letter == "g" :
        return "G"
    elif letter == "h" :
        return "H"
    else :
        return letter


#column letter back to board number
def letter_to_col(letter) :

    if letter == "A" :
        return 0
    elif letter == "B" :
        return 1
    elif letter == "C" :
        return 2
    elif letter == "D" :
        return 3
    elif letter == "E" :
        return 4
    elif letter == "F" :
        return 5
    elif letter == "G" :
        return 6
    elif letter == "H" :
        return 7
    else :
        return -1


#format seconds into mm:ss for the timer labels
def format_time(seconds_left) :

    minutes = seconds_left // 60
    seconds = seconds_left % 60

    if minutes < 10 :
        minute_text = "0" + str(minutes)
    else :
        minute_text = str(minutes)

    if seconds < 10 :
        second_text = "0" + str(seconds)
    else :
        second_text = str(seconds)

    return minute_text + ":" + second_text


#convert move text like E2E4 into board coordinates
def convert_input_to_coords(user_move) :

    if len(user_move) != 4 :
        return [-1, -1, -1, -1]

    #make the file letters uppercase before converting
    user_move = (
        to_upper_case(user_move[0])
        + to_upper_case(user_move[1])
        + to_upper_case(user_move[2])
        + to_upper_case(user_move[3])
    )

    start_col = letter_to_col(user_move[0])
    end_col = letter_to_col(user_move[2])

    if start_col < 0 or start_col > 7 :
        return [-1, -1, -1, -1]

    if end_col < 0 or end_col > 7 :
        return [-1, -1, -1, -1]

    #rank 8 is board row 0, so flip the number
    try :
        start_row = 8 - int(user_move[1])
        end_row = 8 - int(user_move[3])
    except :
        return [-1, -1, -1, -1]

    if start_row < 0 or start_row > 7 :
        return [-1, -1, -1, -1]

    if end_row < 0 or end_row > 7 :
        return [-1, -1, -1, -1]

    return [start_row, start_col, end_row, end_col]


#put all pieces back to the normal chess starting position
def reset_board_to_start() :

    starting_board = [
        ["br", "bn", "bb", "bq", "bk", "bb", "bn", "br"],
        ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
        ["", "", "", "", "", "", "", ""],
        ["", "", "", "", "", "", "", ""],
        ["", "", "", "", "", "", "", ""],
        ["", "", "", "", "", "", "", ""],
        ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
        ["wr", "wn", "wb", "wq", "wk", "wb", "wn", "wr"],
    ]

    for row in range(8) :
        for col in range(8) :
            STARTING_POSITION[row][col] = starting_board[row][col]


#draw the 8 by 8 checkerboard and labels
def draw_board() :

    for row in range(8) :
        for col in range(8) :
            x1 = BOARD_OFFSET_X + (col * SQUARE_SIZE)
            y1 = BOARD_OFFSET_Y + (row * SQUARE_SIZE)
            x2 = x1 + SQUARE_SIZE
            y2 = y1 + SQUARE_SIZE

            if (row + col) % 2 == 0 :
                square_colour = "grey"
            else :
                square_colour = "white"

            canvas.create_rectangle (x1, y1, x2, y2, fill = square_colour, outline = "black")

    #row numbers are shown on the left and right side of the board
    for row in range(8) :
        y_center = BOARD_OFFSET_Y + (row * SQUARE_SIZE) + (SQUARE_SIZE / 2)
        canvas.create_text (BOARD_OFFSET_X - 20, y_center, text = str(8 - row), fill = "black")
        canvas.create_text (BOARD_OFFSET_X + 500, y_center, text = str(8 - row), fill = "black")

    #column letters are shown on the top and bottom of the board
    for col in range(8) :
        x_center = BOARD_OFFSET_X + (col * SQUARE_SIZE) + (SQUARE_SIZE / 2)
        canvas.create_text (x_center, BOARD_OFFSET_Y - 20, text = col_to_letter(col), fill = "black")
        canvas.create_text (x_center, BOARD_OFFSET_Y + 500, text = col_to_letter(col), fill = "black")


#draw all the pieces from the current board position
def draw_pieces() :

    for row in range(8) :
        for col in range(8) :
            piece = STARTING_POSITION[row][col]

            if piece != "" :
                x_center = BOARD_OFFSET_X + (col * SQUARE_SIZE) + (SQUARE_SIZE / 2)
                y_center = BOARD_OFFSET_Y + (row * SQUARE_SIZE) + (SQUARE_SIZE / 2)
                canvas.create_text (x_center, y_center, text = PIECE_TEXT[piece], font = ("Arial", 32), fill = "black")


#draw the starting screen panel on top of the board area
def draw_start_screen() :

    #cover the full canvas so the setup screen looks separate from the game board
    canvas.create_rectangle (0, 0, 700, 700, fill = "lightyellow", outline = "lightyellow")

    #top banner for the title area
    canvas.create_rectangle (70, 55, 630, 155, fill = "white", outline = "black", width = 2)

    #main setup panel in the center
    canvas.create_rectangle (145, 180, 555, 535, fill = "cornsilk", outline = "black", width = 2)

    #bottom helper panel
    canvas.create_rectangle (170, 555, 530, 625, fill = "white", outline = "black", width = 2)


#random promotion helpers
def get_ai_pawn_positions() :

    pawn_positions = []

    #find every black pawn still on the board
    for row in range(8) :
        for col in range(8) :
            if STARTING_POSITION[row][col] == "bp" :
                pawn_positions.append([row, col])

    return pawn_positions


def get_random_promotion_piece() :

    promotion_number = random.randrange(1, 5)

    if promotion_number == 1 :
        return "bq"
    elif promotion_number == 2 :
        return "br"
    elif promotion_number == 3 :
        return "bb"
    else :
        return "bn"


def do_random_ai_promotion() :

    #only run the twist one time in the whole game
    if should_do_random_promotion() == False :
        return

    pawn_positions = get_ai_pawn_positions()

    #if no AI pawns are left, just mark the twist as used
    if len(pawn_positions) == 0 :
        set_random_promotion_done()
        return

    #choose one remaining AI pawn at random
    chosen_index = random.randrange(0, len(pawn_positions))
    chosen_pawn = pawn_positions[chosen_index]
    pawn_row = chosen_pawn[0]
    pawn_col = chosen_pawn[1]

    #promote the pawn into a stronger black piece
    STARTING_POSITION[pawn_row][pawn_col] = get_random_promotion_piece()
    set_random_promotion_done()


#redraw the board after any move or timer update
def draw_everything() :

    #do not redraw the board on top of the game over screen
    if game_over_screen_showing == True :
        return

    canvas.delete ("all")
    draw_board ()
    draw_pieces ()

    #while the game has not started yet, keep the setup panel visible
    if game_started == False :
        draw_start_screen ()


#build the score label text from the current scores
def get_score_text() :

    return (
        "Player: "
        + str(get_player_score ())
        + " pts  |  AI: "
        + str(get_ai_score ())
        + " pts  |  Target: "
        + str(game_state.ai_target_score)
    )


#update all changing labels and the board display
def refresh_display() :

    #once the game over screen is showing, leave it alone
    if game_over_screen_showing == True :
        return

    if game_started == True :
        score_label.configure (text = get_score_text ())
    else :
        score_label.configure (text = "")

    #turn label changes depending on who is moving
    if current_turn == game_state.player_color :
        turn_label.configure (text = "Your turn", fg = "blue")
    elif game_started == True :
        turn_label.configure (text = "AI thinking...", fg = "red")
    else :
        turn_label.configure (text = "")

    #history label shows the saved lifetime record
    if game_started == True :
        info_label.configure (text = "History: " + get_lifetime_stats_string ())
    else :
        info_label.configure (text = "")

    #capture labels show everything that has been taken so far
    if game_started == True :
        player_captured_label.configure (text = "Your captures: " + get_player_capture_string ())
        ai_captured_label.configure (text = "AI captures: " + get_ai_capture_string ())
    else :
        player_captured_label.configure (text = "")
        ai_captured_label.configure (text = "")

    #timer labels are updated every refresh
    if game_started == True :
        white_timer_label.configure (text = "You: " + format_time (white_time))
        ai_timer_label.configure (text = "AI: " + format_time (ai_time))
    else :
        white_timer_label.configure (text = "")
        ai_timer_label.configure (text = "")

    draw_everything ()


#move all setup widgets off screen once the real game starts
def hide_setup_widgets() :

    for widget in setup_widgets :
        widget.place (x = -500, y = -500)


def hide_game_widgets() :

    for widget in game_widgets :
        widget.place (x = -500, y = -500)


def show_game_widgets() :

    #put both timers at the far ends so the player and AI times are easy to compare
    white_timer_label.place (x = 15, y = 10, width = 110)
    ai_timer_label.place (x = 575, y = 10, width = 110)

    #use separate rows for score, turn, and history so they do not touch the board labels
    score_label.place (x = 180, y = 10, width = 340)
    turn_label.place (x = 290, y = 38, width = 120)
    info_label.place (x = 225, y = 62, width = 250)

    #keep the captures on the left and the move controls centered below the board
    player_captured_label.place (x = 25, y = 620, width = 140)
    ai_captured_label.place (x = 25, y = 642, width = 140)
    status_label.place (x = 235, y = 620, width = 230)
    move_entry.place (x = 270, y = 652, width = 80)
    move_button.place (x = 360, y = 648, width = 45)


def hide_all_widgets() :

    #hide setup widgets
    hide_setup_widgets ()

    #hide normal game widgets
    hide_game_widgets ()


#close the program window after the game is over
def close_window(event) :

    window.destroy ()


def close_window_button() :

    window.destroy ()


#show the final game over screen and save the match
def show_game_over(result, reason, player_score, ai_score_value) :

    global game_over_screen_showing

    game_over_screen_showing = True
    set_game_result (result)
    save_match_to_file (white_time, ai_time)
    hide_all_widgets ()

    #cover the full window with a clean ending screen
    canvas.delete ("all")
    canvas.create_rectangle (0, 0, 700, 700, fill = "lightyellow", outline = "lightyellow")
    canvas.create_rectangle (70, 55, 630, 155, fill = "white", outline = "black", width = 2)
    canvas.create_rectangle (120, 185, 580, 545, fill = "cornsilk", outline = "black", width = 2)
    canvas.create_rectangle (170, 585, 530, 645, fill = "white", outline = "black", width = 2)

    if result == "win" :
        title = "You Win!"
        title_colour = "lightgreen"
    elif result == "lose" :
        title = "You Lose!"
        title_colour = "red"
    else :
        title = "Draw!"
        title_colour = "yellow"

    score_text = "Player: " + str(player_score) + " pts   AI: " + str(ai_score_value) + " pts"
    result_text = "Game Over"

    #the top banner shows the main ending title
    canvas.create_text (350, 105, text = result_text, font = ("Arial", 28, "bold"), fill = "black")

    #the center panel shows the winner, reason, and score summary
    canvas.create_text (350, 245, text = title, font = ("Arial", 34, "bold"), fill = title_colour)
    canvas.create_text (350, 315, text = reason, font = ("Arial", 16), fill = "black", width = 360)
    canvas.create_text (350, 390, text = score_text, font = ("Arial", 18, "bold"), fill = "black")
    canvas.create_text (350, 445, text = "Lifetime: " + get_lifetime_stats_string (), font = ("Arial", 16), fill = "black")

    #show a normal button so the window does not close right away
    exit_button.place (x = 310, y = 595)


#end the game, stop the timers, and show the ending screen
def finish_game(result, reason, status_text, turn_text) :

    global timer_running, game_started

    timer_running = False
    game_started = False

    status_label.configure (text = status_text)
    turn_label.configure (text = turn_text, fg = "red")

    show_game_over (result, reason, get_player_score (), get_ai_score ())


#check if the side whose turn it is has been checkmated or stalemated
def check_current_side_game_over(side_to_check) :

    if is_checkmate(STARTING_POSITION, side_to_check) == True :
        if side_to_check == game_state.player_color :
            finish_game ("lose", "Checkmate! The AI checkmated your King.", "Game Over - Checkmate", "Checkmate! AI wins!")
        else :
            finish_game ("win", "Checkmate! You checkmated the AI King.", "Game Over - Checkmate", "Checkmate! You win!")

        return True

    if is_stalemate(STARTING_POSITION, side_to_check) == True :
        finish_game ("draw", "Stalemate! No legal moves available.", "Game Over - Stalemate", "Stalemate! Draw!")
        return True

    return False


#check all non-timer ways the game can end
def check_game_over() :

    if check_current_side_game_over(current_turn) == True :
        return True

    #the player can also win if they reach the target score first
    if check_player_target_reached() == True :
        finish_game ("win", "You reached the target score of " + str(game_state.ai_target_score) + " points!", "Game Over - Player reached target", "You reached the target!")
        return True

    #the AI also wins if it reaches the target score
    if check_ai_target_reached() == True :
        finish_game ("lose", "AI reached the target score of " + str(game_state.ai_target_score) + " points!", "Game Over - AI reached target", "AI wins! Target score reached!")
        return True

    return False


#decide the winner if a timer reaches zero
def handle_timeout() :

    player_score = get_player_score ()
    ai_score_value = get_ai_score ()

    if player_score > ai_score_value :
        finish_game ("win", "Time's up! You had more points than the AI.", "Game Over - Time", "Time's up!")
    elif ai_score_value > player_score :
        finish_game ("lose", "Time's up! The AI had more points than you.", "Game Over - Time", "Time's up!")
    else :
        finish_game ("draw", "Time's up! Both players had equal points.", "Game Over - Time", "Time's up!")


#move a piece on the board and record captures and move history
def make_real_move(start_row, start_col, end_row, end_col, moving_color) :

    piece = STARTING_POSITION[start_row][start_col]
    captured = STARTING_POSITION[end_row][end_col]

    #record the capture before the square is overwritten
    if captured != "" :
        record_capture (captured, moving_color)

    #move the piece on the live board
    STARTING_POSITION[end_row][end_col] = piece
    STARTING_POSITION[start_row][start_col] = ""

    #save the move so the opening book and history file can use it
    record_move (start_row, start_col, end_row, end_col, piece, captured)


#let the AI choose and play one move
def do_ai_turn() :

    global current_turn, last_time

    if game_started == False :
        return

    if timer_running == False :
        return

    #at a random point in the game, one AI pawn is promoted
    do_random_ai_promotion()

    #get the AI move from the AI engine
    ai_result = get_ai_move_info (STARTING_POSITION, game_state.ai_color)
    ai_move = ai_result[0]

    if ai_move == [] :
        status_label.configure (text = "AI has no legal moves!")
        return

    #play the AI move on the real board
    make_real_move (ai_move[0], ai_move[1], ai_move[2], ai_move[3], game_state.ai_color)

    current_turn = game_state.player_color
    last_time = time.time ()

    refresh_display ()

    if check_game_over() == True :
        return

    status_label.configure (text = "Your move")


#start a fresh new game from the setup screen
def start_game() :

    global game_started, timer_running, current_turn, white_time, ai_time, last_time, game_over_screen_showing

    target_text = score_entry.get ()

    #use the typed score if valid, otherwise default to 10
    if target_text.isdigit() == True :
        target_score = int(target_text)

        if target_score < 1 :
            target_score = 10
    else :
        target_score = 10

    #reset all game information
    set_ai_target_score (target_score)
    reset_game_state ()
    reset_board_to_start ()
    set_player_color ("white")

    #reset timers and turn order
    game_started = True
    game_over_screen_showing = False
    timer_running = True
    current_turn = game_state.player_color
    white_time = TIME_LIMIT
    ai_time = TIME_LIMIT
    last_time = time.time ()

    hide_setup_widgets ()
    exit_button.place (x = -500, y = -500)
    show_game_widgets ()
    status_label.configure (text = "Your move")
    info_label.configure (text = "Target: AI needs " + str(game_state.ai_target_score) + " points to win")

    refresh_display ()


#handle the player's move entry from the text box
def submit_move() :

    global current_turn, last_time

    if game_started == False :
        status_label.configure (text = "Game not started yet!")
        return

    if timer_running == False :
        status_label.configure (text = "Game is over!")
        return

    if current_turn != game_state.player_color :
        status_label.configure (text = "Not your turn!")
        return

    user_move = move_entry.get ()
    move_entry.delete (0, tkinter.END)

    #convert the typed move into board coordinates
    coords = convert_input_to_coords (user_move)
    start_row = coords[0]
    start_col = coords[1]
    end_row = coords[2]
    end_col = coords[3]

    if start_row == -1 :
        status_label.configure (text = "Invalid format! Use E2E4")
        return

    piece = STARTING_POSITION[start_row][start_col]

    #player must select a real piece
    if piece == "" :
        status_label.configure (text = "No piece at that square!")
        return

    #player must move only their own colour
    if piece[0] != game_state.player_color[0] :
        status_label.configure (text = "That is not your piece!")
        return

    #the move must follow piece movement rules
    if is_legal_move(start_row, start_col, end_row, end_col, STARTING_POSITION) == False :
        status_label.configure (text = "Illegal move!")
        return

    #the move also cannot leave the player's king in check
    if would_be_in_check(STARTING_POSITION, start_row, start_col, end_row, end_col, game_state.player_color) == True :
        status_label.configure (text = "Move leaves king in check!")
        return

    #play the move, then switch to the AI turn
    make_real_move (start_row, start_col, end_row, end_col, game_state.player_color)

    current_turn = game_state.ai_color
    last_time = time.time ()

    refresh_display ()

    if check_game_over() == True :
        return

    #small pause so the user can see their move before the AI responds
    status_label.configure (text = "AI is moving...")
    window.update ()
    time.sleep (0.3)

    do_ai_turn ()


#run the timers once every second
def update_timers() :

    global white_time, ai_time, last_time

    if timer_running == True and game_started == True :
        now = time.time ()
        passed_seconds = int(now - last_time)

        if passed_seconds > 0 :
            last_time = now

            #only the side whose turn it is loses time
            if current_turn == game_state.player_color :
                white_time = white_time - passed_seconds

                if white_time <= 0 :
                    white_time = 0
                    refresh_display ()
                    handle_timeout ()

            elif current_turn == game_state.ai_color :
                ai_time = ai_time - passed_seconds

                if ai_time <= 0 :
                    ai_time = 0
                    refresh_display ()
                    handle_timeout ()

    refresh_display ()
    window.after (1000, update_timers)


#top status labels
white_timer_label = tkinter.Label (window, text = "You: 10:00", font = ("Arial", 14), fg = "black", bg = "white")
game_widgets.append (white_timer_label)

ai_timer_label = tkinter.Label (window, text = "AI: 10:00", font = ("Arial", 14), fg = "black", bg = "white")
game_widgets.append (ai_timer_label)

turn_label = tkinter.Label (window, text = "Welcome!", font = ("Arial", 12), fg = "blue", bg = "white")
game_widgets.append (turn_label)

info_label = tkinter.Label (window, text = "", font = ("Arial", 10), fg = "green", bg = "white")
game_widgets.append (info_label)

score_label = tkinter.Label (window, text = "Player: 0 pts  |  AI: 0 pts  |  Target: 10", font = ("Arial", 11), fg = "purple", bg = "white")
game_widgets.append (score_label)

player_captured_label = tkinter.Label (window, text = "Your captures: None", font = ("Arial", 9), fg = "blue", bg = "white")
game_widgets.append (player_captured_label)

ai_captured_label = tkinter.Label (window, text = "AI captures: None", font = ("Arial", 9), fg = "red", bg = "white")
game_widgets.append (ai_captured_label)

status_label = tkinter.Label (window, text = "Set target score and click Start", font = ("Arial", 10), fg = "green", bg = "white")
game_widgets.append (status_label)


#setup screen labels and controls
title_label = tkinter.Label (window, text = "Move Value Chess", font = ("Arial", 20, "bold"), bg = "lightyellow")
title_label.place (x = 230, y = 85)
setup_widgets.append (title_label)

set_score_label = tkinter.Label (window, text = "Set AI Target Score", font = ("Arial", 14), bg = "lightyellow")
set_score_label.place (x = 250, y = 235)
setup_widgets.append (set_score_label)

instructions_label = tkinter.Label (window, text = "Enter how many points the AI needs to win.\nDefault is 10 points.", font = ("Arial", 10), bg = "lightyellow")
instructions_label.place (x = 215, y = 285)
setup_widgets.append (instructions_label)

score_entry = tkinter.Entry (window, width = 10, font = ("Arial", 16))
score_entry.insert (0, "10")
score_entry.place (x = 303, y = 360)
setup_widgets.append (score_entry)

start_button = tkinter.Button (window, text = "Start Game", font = ("Arial", 14), bg = "lightgreen")
start_button.place (x = 270, y = 425)
setup_widgets.append (start_button)

moves_label = tkinter.Label (window, text = "Enter moves like E2E4\nWhite moves first and AI plays black.", font = ("Arial", 10), bg = "lightyellow")
moves_label.place (x = 225, y = 575)
setup_widgets.append (moves_label)


#move entry controls under the board
canvas.place (x = 0, y = 0)

move_entry = tkinter.Entry (window, width = 10)
game_widgets.append (move_entry)

move_button = tkinter.Button (window, text = "Move")
game_widgets.append (move_button)

exit_button = tkinter.Button (window, text = "Exit", width = 8)
exit_button.place (x = -500, y = -500)


#connect buttons to their functions
start_button.configure (command = start_game)
move_button.configure (command = submit_move)
exit_button.configure (command = close_window_button)


#draw the starting screen and begin the timer loop
hide_game_widgets ()
refresh_display ()
window.after (1000, update_timers)
window.mainloop ()
