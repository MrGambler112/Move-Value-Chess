#Name: Move Value Based Chess Engine
#Programmer: Syed (Mahadi) Masuduzzaman and Ryan Rawal
#Last Updated: June 10, 2026
#Description: This program lets the user play chess against an AI
#             that chooses the move with the best move value.

from data import STARTING_POSITION, PIECE_TEXT
from move_rules import is_legal_move
from game_state import record_capture, record_move, reset_game_state, set_player_color
from game_state import set_ai_target_score, check_ai_target_reached, check_player_target_reached
from game_state import get_player_capture_string, get_ai_capture_string
from game_state import get_player_score, get_ai_score
from game_state import set_game_result, save_match_to_file, get_lifetime_stats_string
from game_state import should_do_random_promotion, set_random_promotion_done
from game_state import get_ai_target_score, get_player_color, get_ai_color
from board_logic import is_checkmate, is_stalemate, would_be_in_check
from ai_engine import get_ai_move_info
import time
import tkinter
import random


#window setup
window = tkinter.Tk ()
window.geometry ("700x700")
window.title ("Move Value Chess")
window.resizable (False, False)
window.configure (bg = "#302E2B")

canvas = tkinter.Canvas (window, width = 700, height = 700, bg = "#302E2B")
canvas.place (x = 0, y = 0)


#board constants
SQUARE_SIZE = 60
BOARD_OFFSET_X = 110
BOARD_OFFSET_Y = 90
TIME_LIMIT = 600


#color constants
BACKGROUND = "#302E2B"
PANEL_BG = "#262421"
BOARD_LIGHT = "#EEEED2"
BOARD_DARK = "#769656"
SELECTED_SQUARE_COLOR = "#F6F669"
TEXT_COLOR = "#FFFFFF"
MUTED_TEXT = "#CFCFCF"
BUTTON_BG = "#81B64C"
BUTTON_HOVER = "#95C85A"
BUTTON_TEXT = "#FFFFFF"


#widget variables
white_timer_label = ""
black_timer_label = ""
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
new_game_button = ""
exit_button = ""
player_color_label = ""
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

    #the rank characters must be numbers before converting them
    if user_move[1].isdigit() == False :
        return [-1, -1, -1, -1]

    if user_move[3].isdigit() == False :
        return [-1, -1, -1, -1]

    #rank 8 is board row 0, so flip the number
    start_row = 8 - int(user_move[1])
    end_row = 8 - int(user_move[3])

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
                square_colour = BOARD_DARK
            else :
                square_colour = BOARD_LIGHT

            canvas.create_rectangle (x1, y1, x2, y2, fill = square_colour, outline = BOARD_DARK)

    #row numbers are shown on the left and right side of the board
    for row in range(8) :
        y_center = BOARD_OFFSET_Y + (row * SQUARE_SIZE) + (SQUARE_SIZE / 2)
        canvas.create_text (BOARD_OFFSET_X - 20, y_center, text = str(8 - row), fill = MUTED_TEXT, font = ("Arial", 10))
        canvas.create_text (BOARD_OFFSET_X + (8 * SQUARE_SIZE) + 20, y_center, text = str(8 - row), fill = MUTED_TEXT, font = ("Arial", 10))

    #column letters are shown on the top and bottom of the board
    for col in range(8) :
        x_center = BOARD_OFFSET_X + (col * SQUARE_SIZE) + (SQUARE_SIZE / 2)
        canvas.create_text (x_center, BOARD_OFFSET_Y - 15, text = col_to_letter(col), fill = MUTED_TEXT, font = ("Arial", 10))
        canvas.create_text (x_center, BOARD_OFFSET_Y + (8 * SQUARE_SIZE) + 15, text = col_to_letter(col), fill = MUTED_TEXT, font = ("Arial", 10))


#draw all the pieces from the current board position
def draw_pieces() :

    for row in range(8) :
        for col in range(8) :
            piece = STARTING_POSITION[row][col]

            if piece != "" :
                x_center = BOARD_OFFSET_X + (col * SQUARE_SIZE) + (SQUARE_SIZE / 2)
                y_center = BOARD_OFFSET_Y + (row * SQUARE_SIZE) + (SQUARE_SIZE / 2)
                canvas.create_text (x_center, y_center, text = PIECE_TEXT[piece], font = ("Arial", 34), fill = "black")


#draw the starting screen panel on top of the board area
def draw_start_screen() :

    #no overlay needed - side panel handles the setup
    return


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

    #fill the full 700 by 700 background
    canvas.create_rectangle (0, 0, 700, 700, fill = BACKGROUND, outline = "")

    #draw a top info bar and a bottom control bar
    canvas.create_rectangle (15, 10, 685, 70, fill = PANEL_BG, outline = "")
    canvas.create_rectangle (15, 610, 685, 690, fill = PANEL_BG, outline = "")

    draw_board ()
    draw_pieces ()


#start a new game from the side panel
def new_game() :

    global game_started, game_over_screen_showing, white_time, ai_time

    game_started = False
    game_over_screen_showing = False
    white_time = TIME_LIMIT
    ai_time = TIME_LIMIT
    reset_board_to_start ()
    reset_game_state ()

    hide_game_widgets ()
    show_setup_widgets ()

    status_label.configure (text = "Set target score and click Start Game.")
    refresh_display ()


#build the score label text from the current scores
def get_score_text() :

    return (
        "Player: "
        + str(get_player_score ())
        + " pts  |  AI: "
        + str(get_ai_score ())
        + " pts"
    )


#update all changing labels and the board display
def refresh_display() :

    #once the game over screen is showing, leave it alone
    if game_over_screen_showing == True :
        return

    #timer labels always show time
    if game_started == True :
        white_timer_label.configure (text = "White  " + format_time (white_time))
        black_timer_label.configure (text = "Black  " + format_time (ai_time))
    else :
        white_timer_label.configure (text = "White  10:00")
        black_timer_label.configure (text = "Black  10:00")

    #highlight the active timer
    if game_started == True and timer_running == True :
        if current_turn == "white" :
            white_timer_label.configure (fg = TEXT_COLOR)
            black_timer_label.configure (fg = MUTED_TEXT)
        else :
            white_timer_label.configure (fg = MUTED_TEXT)
            black_timer_label.configure (fg = TEXT_COLOR)

    #side panel labels update based on game state
    if game_started == True :
        score_label.configure (text = get_score_text ())
    else :
        score_label.configure (text = "")

    #turn label changes depending on who is moving
    if game_started == True :
        if current_turn == get_player_color () :
            turn_label.configure (text = "Your Turn", fg = BUTTON_BG)
        else :
            turn_label.configure (text = "AI Thinking...", fg = "#FF6B6B")
    else :
        turn_label.configure (text = "Not Started")

    #history label shows the saved lifetime record
    if game_started == True :
        info_label.configure (text = "Lifetime: " + get_lifetime_stats_string ())
    else :
        info_label.configure (text = "")

    #capture labels show everything that has been taken so far
    if game_started == True :
        player_captured_label.configure (text = "Your captures: " + get_player_capture_string ())
        ai_captured_label.configure (text = "AI captures: " + get_ai_capture_string ())
    else :
        player_captured_label.configure (text = "")
        ai_captured_label.configure (text = "")

    draw_everything ()


#move all setup widgets off screen once the real game starts
def hide_setup_widgets() :

    for widget in setup_widgets :
        widget.place (x = -500, y = -500)


def show_setup_widgets() :

    #setup widgets
    for widget in setup_widgets :
        widget.place (x = -500, y = -500)

    title_label.place (x = 235, y = 180, width = 230)
    player_color_label.place (x = 220, y = 255, width = 260)
    target_label.place (x = 275, y = 315, width = 150)
    score_entry.place (x = 305, y = 345, width = 90)
    start_button.place (x = 275, y = 395, width = 150)


def hide_game_widgets() :

    for widget in game_widgets :
        widget.place (x = -500, y = -500)


def show_game_widgets() :

    #timers stay inside the top bar
    white_timer_label.place (x = 25, y = 24, width = 140)
    black_timer_label.place (x = 535, y = 24, width = 140)

    #top information row
    score_label.place (x = 205, y = 18, width = 290)
    turn_label.place (x = 280, y = 42, width = 140)

    #bottom control row
    player_captured_label.place (x = 25, y = 620, width = 180)
    ai_captured_label.place (x = 25, y = 642, width = 180)
    info_label.place (x = 225, y = 620, width = 250)
    status_label.place (x = 225, y = 642, width = 250)
    move_entry.place (x = 495, y = 620, width = 85)
    move_button.place (x = 590, y = 618, width = 50)
    new_game_button.place (x = 525, y = 648, width = 115)


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

    #keep the board visible with final position
    #show game over info in the side panel area
    if result == "win" :
        title = "You Win!"
        title_color = BUTTON_BG
    elif result == "lose" :
        title = "You Lose!"
        title_color = "#FF6B6B"
    else :
        title = "Draw!"
        title_color = "#FFD700"

    score_text = "Player: " + str(player_score) + " pts  AI: " + str(ai_score_value) + " pts"

    #draw dark overlay on the board area only
    canvas.create_rectangle (35, 55, 615, 645, fill = "#1A1A1A", outline = "")
    canvas.create_text (325, 180, text = "Game Over", font = ("Arial", 28, "bold"), fill = TEXT_COLOR)
    canvas.create_text (325, 260, text = title, font = ("Arial", 34, "bold"), fill = title_color)
    canvas.create_text (325, 340, text = reason, font = ("Arial", 14), fill = MUTED_TEXT)
    canvas.create_text (325, 410, text = score_text, font = ("Arial", 18, "bold"), fill = TEXT_COLOR)
    canvas.create_text (325, 460, text = "Lifetime: " + get_lifetime_stats_string (), font = ("Arial", 14), fill = MUTED_TEXT)

    exit_button.configure (bg = BUTTON_BG, fg = BUTTON_TEXT)
    exit_button.place (x = 265, y = 550, width = 120)


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
        if side_to_check == get_player_color () :
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
        finish_game ("win", "You reached the target score of " + str(get_ai_target_score ()) + " points!", "Game Over - Player reached target", "You reached the target!")
        return True

    #the AI also wins if it reaches the target score
    if check_ai_target_reached() == True :
        finish_game ("lose", "AI reached the target score of " + str(get_ai_target_score ()) + " points!", "Game Over - AI reached target", "AI wins! Target score reached!")
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


#make the AI pause for a few seconds before choosing a move
def wait_for_ai_think_time() :

    global ai_time, last_time

    #pick a simple random wait so the AI does not move instantly every turn
    think_seconds = random.randrange(4, 8)
    status_label.configure (text = "AI is thinking...")
    window.update_idletasks ()
    time.sleep (think_seconds)

    #subtract the time the AI spent "thinking" from the AI clock
    ai_time = ai_time - think_seconds

    if ai_time < 0 :
        ai_time = 0

    #reset the timer base so the scheduled timer update does not subtract it again
    last_time = time.time ()
    refresh_display ()

    if ai_time == 0 :
        handle_timeout ()
        return False

    return True


#let the AI choose and play one move
def do_ai_turn() :

    global current_turn, last_time

    if game_started == False :
        return

    if timer_running == False :
        return

    #let the AI wait a random number of seconds before moving
    if wait_for_ai_think_time() == False :
        return

    #at a random point in the game, one AI pawn is promoted
    do_random_ai_promotion()

    #get the AI move from the AI engine
    ai_result = get_ai_move_info (STARTING_POSITION, get_ai_color ())
    ai_move = ai_result[0]

    if ai_move == [] :
        status_label.configure (text = "AI has no legal moves!")
        return

    #play the AI move on the real board
    make_real_move (ai_move[0], ai_move[1], ai_move[2], ai_move[3], get_ai_color ())

    current_turn = get_player_color ()
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
    current_turn = get_player_color ()
    white_time = TIME_LIMIT
    ai_time = TIME_LIMIT
    last_time = time.time ()

    hide_setup_widgets ()
    exit_button.place (x = -500, y = -500)
    show_game_widgets ()
    status_label.configure (text = "Your move")

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

    if current_turn != get_player_color () :
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
    if piece[0] != get_player_color ()[0] :
        status_label.configure (text = "That is not your piece!")
        return

    #the move must follow piece movement rules
    if is_legal_move(start_row, start_col, end_row, end_col, STARTING_POSITION) == False :
        status_label.configure (text = "Illegal move!")
        return

    #the move also cannot leave the player's king in check
    if would_be_in_check(STARTING_POSITION, start_row, start_col, end_row, end_col, get_player_color ()) == True :
        status_label.configure (text = "Move leaves king in check!")
        return

    #play the move, then switch to the AI turn
    make_real_move (start_row, start_col, end_row, end_col, get_player_color ())

    current_turn = get_ai_color ()
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
            if current_turn == get_player_color () :
                white_time = white_time - passed_seconds

                if white_time <= 0 :
                    white_time = 0
                    refresh_display ()
                    handle_timeout ()

            elif current_turn == get_ai_color () :
                ai_time = ai_time - passed_seconds

                if ai_time <= 0 :
                    ai_time = 0
                    refresh_display ()
                    handle_timeout ()

    refresh_display ()
    window.after (1000, update_timers)


#timer labels above and below the board
board_center_x = BOARD_OFFSET_X + (8 * SQUARE_SIZE // 2)

black_timer_label = tkinter.Label (window, text = "Black  10:00", font = ("Arial", 18, "bold"), fg = MUTED_TEXT, bg = PANEL_BG)
black_timer_label.place (x = board_center_x - 80, y = 12, width = 160)

white_timer_label = tkinter.Label (window, text = "White  10:00", font = ("Arial", 18, "bold"), fg = MUTED_TEXT, bg = PANEL_BG)
white_timer_label.place (x = board_center_x - 80, y = 655, width = 160)


#side panel labels and controls
TITLE_FONT = ("Arial", 20, "bold")
LABEL_FONT = ("Arial", 11)
BUTTON_FONT = ("Arial", 11, "bold")

title_label = tkinter.Label (window, text = "Move Value\nChess", font = ("Arial", 22, "bold"), fg = TEXT_COLOR, bg = PANEL_BG)
setup_widgets.append (title_label)

player_color_label = tkinter.Label (window, text = "You are playing as White", font = ("Arial", 12), fg = TEXT_COLOR, bg = PANEL_BG)
setup_widgets.append (player_color_label)

target_label = tkinter.Label (window, text = "AI Target Score", font = ("Arial", 10), fg = MUTED_TEXT, bg = PANEL_BG)
setup_widgets.append (target_label)

score_entry = tkinter.Entry (window, width = 8, font = ("Arial", 12))
score_entry.insert (0, "10")
setup_widgets.append (score_entry)

start_button = tkinter.Button (window, text = "Start Game", font = ("Arial", 12, "bold"), bg = BUTTON_BG, fg = BUTTON_TEXT)
setup_widgets.append (start_button)


#game widgets (visible during the game)
turn_label = tkinter.Label (window, text = "Not Started", font = ("Arial", 13, "bold"), fg = TEXT_COLOR, bg = PANEL_BG)
game_widgets.append (turn_label)

score_label = tkinter.Label (window, text = "", font = ("Arial", 10), fg = MUTED_TEXT, bg = PANEL_BG)
game_widgets.append (score_label)

player_captured_label = tkinter.Label (window, text = "", font = ("Arial", 9), fg = MUTED_TEXT, bg = PANEL_BG)
game_widgets.append (player_captured_label)

ai_captured_label = tkinter.Label (window, text = "", font = ("Arial", 9), fg = MUTED_TEXT, bg = PANEL_BG)
game_widgets.append (ai_captured_label)

info_label = tkinter.Label (window, text = "", font = ("Arial", 9), fg = MUTED_TEXT, bg = PANEL_BG)
game_widgets.append (info_label)

status_label = tkinter.Label (window, text = "Set target score and click Start Game.", font = ("Arial", 11), fg = MUTED_TEXT, bg = PANEL_BG)
game_widgets.append (status_label)

move_entry = tkinter.Entry (window, width = 10, font = ("Arial", 11))
game_widgets.append (move_entry)

move_button = tkinter.Button (window, text = "Move", font = BUTTON_FONT, bg = BUTTON_BG, fg = BUTTON_TEXT)
game_widgets.append (move_button)

new_game_button = tkinter.Button (window, text = "New Game", font = BUTTON_FONT, bg = "#525250", fg = MUTED_TEXT, command = new_game)
game_widgets.append (new_game_button)

exit_button = tkinter.Button (window, text = "Exit", font = BUTTON_FONT, bg = "#525250", fg = MUTED_TEXT, command = close_window_button)
exit_button.place (x = -500, y = -500)


#connect buttons to their functions
start_button.configure (command = start_game)
move_button.configure (command = submit_move)


#show the side panel and begin the timer loop
hide_game_widgets ()
show_setup_widgets ()
refresh_display ()
window.after (1000, update_timers)
window.mainloop ()
