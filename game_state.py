#Name: Game State
#Programmer: Syed (Mahadi) Masuduzzaman
#Last Updated: June 10, 2026
#Description: This file stores the changing match information such as
#             captures, scores, move history, and saved match stats.

from data import PIECE_VALUES, PIECE_TEXT
import time
import random


#game data
player_captures = []
ai_captures = []
player_score = 0
ai_score = 0
move_history = []
game_status = "playing"
player_color = "white"
ai_color = "black"
ai_target_score = 10
move_count = 0
random_promotion_done = False
random_promotion_turn = 0
game_result = ""


#piece helpers
def get_capture_points(piece) :

    #only real pieces have point values
    if piece == "" :
        return 0

    piece_type = piece[1]

    if piece_type in PIECE_VALUES :
        return PIECE_VALUES[piece_type]

    return 0


def get_piece_symbol(piece) :

    #convert internal piece codes into the board symbols used by labels
    if piece in PIECE_TEXT :
        return PIECE_TEXT[piece]

    return "?"


#score and move recording
def record_capture(captured_piece, capturing_color) :

    global player_score, ai_score, player_captures, ai_captures

    if captured_piece == "" :
        return

    #convert the captured piece into points
    points = get_capture_points(captured_piece)

    #save the captured piece in the correct list and update the score
    if capturing_color == "white" :
        player_captures.append(captured_piece)
        player_score = player_score + points
    else :
        ai_captures.append(captured_piece)
        ai_score = ai_score + points


def record_move(start_row, start_col, end_row, end_col, piece, captured) :

    global move_count

    #store the full move information for history and opening book use
    move_history.append([start_row, start_col, end_row, end_col, piece, captured])
    move_count = move_count + 1


def get_last_move() :

    if len(move_history) == 0 :
        return []

    return move_history[-1]


#reset and setup
def reset_game_state() :

    global player_captures, ai_captures, player_score, ai_score
    global move_history, game_status, move_count, random_promotion_done
    global random_promotion_turn, game_result

    #clear all changing match information back to fresh-game values
    player_captures = []
    ai_captures = []
    player_score = 0
    ai_score = 0
    move_history = []
    game_status = "playing"
    move_count = 0
    random_promotion_done = False
    random_promotion_turn = random.randrange(6, 17)
    game_result = ""


def set_player_color(color) :

    global player_color, ai_color

    player_color = color

    #the AI colour is always the opposite of the player colour
    if color == "white" :
        ai_color = "black"
    else :
        ai_color = "white"


def set_ai_target_score(score) :

    #the target score is the number of points the AI needs to win
    global ai_target_score
    ai_target_score = score


def get_ai_target_score() :

    return ai_target_score


def get_player_color() :

    return player_color


def get_ai_color() :

    return ai_color


def check_ai_target_reached() :

    #if the AI has enough capture points, the AI wins immediately
    if ai_score >= ai_target_score :
        return True

    return False


def check_player_target_reached() :

    #the player can also win by reaching the same point target
    if player_score >= ai_target_score :
        return True

    return False


#random promotion helpers
def should_do_random_promotion() :

    #when the move count reaches the random turn, the promotion should happen
    if random_promotion_done == False :
        if move_count >= random_promotion_turn :
            return True

    return False


def set_random_promotion_done() :

    global random_promotion_done
    random_promotion_done = True


#board text helpers
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


def get_move_history_strings() :

    strings = []

    #convert saved row and column numbers into normal chess text
    for move in move_history :
        start_row = move[0]
        start_col = move[1]
        end_row = move[2]
        end_col = move[3]

        start_file = col_to_letter(start_col)
        start_rank = str(8 - start_row)
        end_file = col_to_letter(end_col)
        end_rank = str(8 - end_row)

        strings.append(start_file + start_rank + end_file + end_rank)

    return strings


def get_capture_string(capture_list) :

    if len(capture_list) == 0 :
        return "None"

    capture_text = ""

    #build one string of piece symbols for the label
    for piece in capture_list :
        capture_text = capture_text + get_piece_symbol(piece) + " "

    return capture_text


def get_player_capture_string() :

    return get_capture_string(player_captures)


def get_ai_capture_string() :

    return get_capture_string(ai_captures)


def get_player_score() :

    return player_score


def get_ai_score() :

    return ai_score


#game result
def set_game_result(result) :

    #save the final result string so it can be written to the save file
    global game_result
    game_result = result


def get_game_result() :

    return game_result


#saving match history
def build_moves_line() :

    move_strings = get_move_history_strings()
    moves_line = ""

    if len(move_strings) > 0 :
        moves_line = move_strings[0]
        index = 1

        #add commas between each move for the save file
        while index < len(move_strings) :
            moves_line = moves_line + ", " + move_strings[index]
            index = index + 1

    return moves_line


def get_result_text() :

    #turn the saved result code into clearer file text
    if game_result == "win" :
        return "Player Win"
    elif game_result == "lose" :
        return "AI Win"
    elif game_result == "draw" :
        return "Draw"
    else :
        return "Unknown"


def format_time_left(seconds_left) :

    #show saved time in the same mm:ss style that the GUI uses
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


def build_match_block(player_time_left, ai_time_left) :

    date_time = time.strftime("%Y-%m-%d %H:%M")
    moves_line = build_moves_line()

    match_block = ""
    match_block = match_block + "MATCH DATE: " + date_time + "\n"
    match_block = match_block + "RESULT: " + get_result_text() + "\n"
    match_block = match_block + "PLAYER SCORE: " + str(player_score) + "\n"
    match_block = match_block + "AI SCORE: " + str(ai_score) + "\n"
    match_block = match_block + "PLAYER TIME LEFT: " + format_time_left(player_time_left) + "\n"
    match_block = match_block + "AI TIME LEFT: " + format_time_left(ai_time_left) + "\n"
    match_block = match_block + "MOVES PLAYED: " + moves_line + "\n"
    match_block = match_block + "\n"

    return match_block


def save_match_to_file(player_time_left, ai_time_left) :

    #save the match using labeled lines so each value is easy to read
    history_file = open("chess_history.txt", "a")
    history_file.write(build_match_block(player_time_left, ai_time_left))
    history_file.close()

    #after saving the match, update lifetime totals too
    lifetime = load_lifetime_stats()

    if game_result == "win" :
        lifetime[0] = lifetime[0] + 1
    elif game_result == "lose" :
        lifetime[1] = lifetime[1] + 1
    elif game_result == "draw" :
        lifetime[2] = lifetime[2] + 1

    save_lifetime_stats(lifetime)


#lifetime stats
def load_lifetime_stats() :

    wins = 0
    losses = 0
    draws = 0

    #open the lifetime file from the same folder as the program
    lifetime_file = open("chess_lifetime.txt", "r")
    line = lifetime_file.readline().strip()

    #read each line and place the values into wins, losses, and draws
    while line != "" :
        parts = line.split()

        if len(parts) == 2 :
            if parts[0] == "WINS" :
                wins = int(parts[1])
            elif parts[0] == "LOSSES" :
                losses = int(parts[1])
            elif parts[0] == "DRAWS" :
                draws = int(parts[1])

        line = lifetime_file.readline().strip()

    lifetime_file.close()

    return [wins, losses, draws]


def save_lifetime_stats(lifetime) :

    #overwrite the lifetime file with the newest totals
    lifetime_file = open("chess_lifetime.txt", "w")
    lifetime_file.write("WINS " + str(lifetime[0]) + "\n")
    lifetime_file.write("LOSSES " + str(lifetime[1]) + "\n")
    lifetime_file.write("DRAWS " + str(lifetime[2]) + "\n")
    lifetime_file.close()


def get_lifetime_stats_string() :

    #turn the lifetime list into one short display string
    lifetime = load_lifetime_stats()

    return (
        "W: "
        + str(lifetime[0])
        + " L: "
        + str(lifetime[1])
        + " D: "
        + str(lifetime[2])
    )
