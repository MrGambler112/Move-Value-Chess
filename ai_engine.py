#Name: AI Engine
#Programmer: Syed (Mahadi) Masuduzzaman
#Date: June 10, 2026
#Description: This file calculates AI move values, checks simple
#             opening moves, and chooses the best legal AI move.

import random
from data import POSITION_VALUES
from move_rules import get_piece_value, is_legal_move
from board_logic import (
    generate_all_legal_moves,
    make_move_on_board,
    is_square_attacked,
    copy_board,
    would_be_in_check,
)
from bookmoves import get_book_move
from game_state import get_move_history_strings


#move value multipliers
#these multipliers now follow the written documentation more closely
CAPTURE_VALUE_MULTIPLIER = 1
POSITION_TABLE_MULTIPLIER = 0
DEVELOPMENT_VALUE_MULTIPLIER = 1
POSITION_VALUE_MULTIPLIER = 1
SAFETY_VALUE_MULTIPLIER = 1
BIAS_VALUE_MULTIPLIER = 1


#text and colour helpers
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
        return 0


def get_piece_type(piece) :

    if piece == "" :
        return ""

    return piece[1]


def get_opponent_color(color) :

    if color == "white" :
        return "black"

    return "white"


#starting square checking
def is_piece_on_starting_square(piece, row, col) :

    if piece == "" :
        return False

    if piece == "wk" :
        if row == 7 and col == 4 :
            return True
    elif piece == "wq" :
        if row == 7 and col == 3 :
            return True
    elif piece == "wr" :
        if row == 7 and (col == 0 or col == 7) :
            return True
    elif piece == "wn" :
        if row == 7 and (col == 1 or col == 6) :
            return True
    elif piece == "wb" :
        if row == 7 and (col == 2 or col == 5) :
            return True
    elif piece == "wp" :
        if row == 6 :
            return True
    elif piece == "bk" :
        if row == 0 and col == 4 :
            return True
    elif piece == "bq" :
        if row == 0 and col == 3 :
            return True
    elif piece == "br" :
        if row == 0 and (col == 0 or col == 7) :
            return True
    elif piece == "bn" :
        if row == 0 and (col == 1 or col == 6) :
            return True
    elif piece == "bb" :
        if row == 0 and (col == 2 or col == 5) :
            return True
    elif piece == "bp" :
        if row == 1 :
            return True

    return False


#board simulation helpers
def build_test_board(board, piece, start_row, start_col, end_row, end_col) :

    #copy the board first so the real game board is not changed
    test_board = copy_board(board)

    #place the moving piece on the ending square
    test_board[end_row][end_col] = piece

    #clear the starting square after the move
    test_board[start_row][start_col] = ""

    return test_board


def can_piece_legally_move(test_board, start_row, start_col, end_row, end_col, color) :

    #first check the normal movement rules for the piece
    legal = is_legal_move(start_row, start_col, end_row, end_col, test_board)

    if legal == False :
        return False

    #then reject the move if it would leave the moving side in check
    in_check = would_be_in_check(
        test_board, start_row, start_col, end_row, end_col, color
    )

    if in_check == True :
        return False

    return True


def count_square_control(board, row, col, by_color) :

    control_count = 0

    #put a temporary enemy piece on the square so captures and pawn attacks
    #can be detected properly when checking protection and threats
    test_board = copy_board(board)

    if by_color == "white" :
        test_board[row][col] = "bp"
    else :
        test_board[row][col] = "wp"

    for check_row in range(8) :
        for check_col in range(8) :
            piece = test_board[check_row][check_col]

            if piece != "" :
                if piece[0] == by_color[0] :
                    same_square = check_row == row and check_col == col

                    if same_square == False :
                        legal = can_piece_legally_move(
                            test_board,
                            check_row,
                            check_col,
                            row,
                            col,
                            by_color,
                        )

                        if legal == True :
                            control_count = control_count + 1

    return control_count


#capture value section
#this section gives points for taking an enemy piece
def calculate_capture_value(board, end_row, end_col) :

    #capturing a more valuable piece should increase move value
    target_piece = board[end_row][end_col]
    return get_piece_value(target_piece)


def calculate_static_position_value(piece, row, col) :

    #each piece type has a table of how good every square is
    piece_type = get_piece_type(piece)

    if piece_type == "" :
        return 0

    if piece_type in POSITION_VALUES :
        return POSITION_VALUES[piece_type][row][col]

    return 0


#position table value section
#this section is currently neutralized so the engine follows the
#documented move value formula more closely
def calculate_position_table_bonus(piece, start_row, start_col, end_row, end_col) :

    #compare the starting square value to the ending square value
    start_value = calculate_static_position_value(piece, start_row, start_col)
    end_value = calculate_static_position_value(piece, end_row, end_col)

    return end_value - start_value


#position value section
#this section checks whether the moved piece attacks, protects,
#or reaches useful squares after it has already been developed
def calculate_position_value(board, piece, start_row, start_col, end_row, end_col, color) :

    piece_type = get_piece_type(piece)

    if piece_type == "" :
        return 0

    if is_piece_on_starting_square(piece, start_row, start_col) == True :
        return 0

    test_board = build_test_board(board, piece, start_row, start_col, end_row, end_col)
    opponent = get_opponent_color(color)
    threat_count = 0
    protected_count = 0
    attacker_count = 0

    #count how many enemy pieces the moved piece threatens from its new square
    for check_row in range(8) :
        for check_col in range(8) :
            target_piece = test_board[check_row][check_col]

            if target_piece != "" :
                if target_piece[0] == opponent[0] :
                    legal = can_piece_legally_move(
                        test_board,
                        end_row,
                        end_col,
                        check_row,
                        check_col,
                        color,
                    )

                    if legal == True :
                        threat_count = threat_count + 1

    #count how many friendly pieces protect the moved piece on its new square
    protected_count = count_square_control(test_board, end_row, end_col, color)

    #count how many enemy pieces threaten the moved piece on its new square
    attacker_count = count_square_control(test_board, end_row, end_col, opponent)

    #position value = enemy pieces threatened + protected count - attacker count
    return threat_count + protected_count - attacker_count


#development value section
#this section rewards moving pieces off their starting squares
#when that move helps them control more useful squares
def calculate_development_value(board, piece, start_row, start_col, end_row, end_col, color) :

    piece_type = get_piece_type(piece)

    if piece_type == "" :
        return 0

    if is_piece_on_starting_square(piece, start_row, start_col) == False :
        return 0

    test_board = build_test_board(board, piece, start_row, start_col, end_row, end_col)
    squares_controlled = 0

    #count how many useful squares the piece would control after developing
    for check_row in range(8) :
        for check_col in range(8) :
            same_square = check_row == end_row and check_col == end_col

            if same_square == False :
                legal = can_piece_legally_move(
                    test_board,
                    end_row,
                    end_col,
                    check_row,
                    check_col,
                    color,
                )

                if legal == True :
                    end_piece = test_board[check_row][check_col]
                    blocked = False

                    if end_piece != "" :
                        if end_piece[0] == piece[0] :
                            blocked = True

                    if blocked == False :
                        squares_controlled = squares_controlled + 1

    #use the total controlled squares directly as the development value
    return squares_controlled


#safety value section
#this section punishes moves that leave stronger friendly pieces exposed
def get_attackers_of_square(board, row, col, by_color) :

    attackers = []
    color_prefix = by_color[0]

    #search the full board for enemy pieces that attack the target square
    for check_row in range(8) :
        for check_col in range(8) :
            piece = board[check_row][check_col]

            if piece != "" :
                if piece[0] == color_prefix :
                    legal = is_legal_move(check_row, check_col, row, col, board)

                    if legal == True :
                        attackers.append([check_row, check_col])

    return attackers


def can_friendly_piece_defend_attackers(board, row, col, friendly_color, attackers) :

    friendly_prefix = friendly_color[0]

    #check if any friendly piece can capture one of the attackers
    for check_row in range(8) :
        for check_col in range(8) :
            piece = board[check_row][check_col]

            if piece != "" :
                if piece[0] == friendly_prefix :
                    same_piece = check_row == row and check_col == col

                    if same_piece == False :
                        for attacker in attackers :
                            attacker_row = attacker[0]
                            attacker_col = attacker[1]
                            legal = is_legal_move(
                                check_row,
                                check_col,
                                attacker_row,
                                attacker_col,
                                board,
                            )

                            if legal == True :
                                return True

    return False


def calculate_safety_value(board, piece, start_row, start_col, end_row, end_col, color) :

    piece_type = get_piece_type(piece)

    if piece_type == "" :
        return 0

    moving_piece_value = get_piece_value(piece)
    test_board = build_test_board(board, piece, start_row, start_col, end_row, end_col)
    opponent = get_opponent_color(color)
    penalty = 0

    #look for friendly pieces that become too exposed after this move
    for check_row in range(8) :
        for check_col in range(8) :
            friendly_piece = test_board[check_row][check_col]

            if friendly_piece != "" :
                if friendly_piece[0] == piece[0] :
                    is_moved_piece = check_row == end_row and check_col == end_col

                    if is_moved_piece == False :
                        attackers = get_attackers_of_square(
                            test_board, check_row, check_col, opponent
                        )

                        #only punish the move if a more valuable piece is left hanging
                        if len(attackers) > 0 :
                            friendly_value = get_piece_value(friendly_piece)

                            if friendly_value > moving_piece_value :
                                defended = can_friendly_piece_defend_attackers(
                                    test_board,
                                    check_row,
                                    check_col,
                                    color,
                                    attackers,
                                )

                                if defended == False :
                                    penalty = penalty + (
                                        friendly_value - moving_piece_value
                                    )

    return penalty


#random tie break section
#this section slightly changes equal moves so the AI is less repetitive
def get_random_tie_break() :

    tie_break_num = random.randrange(1, 21)

    if tie_break_num == 1 :
        return -0.10
    elif tie_break_num == 2 :
        return -0.09
    elif tie_break_num == 3 :
        return -0.08
    elif tie_break_num == 4 :
        return -0.07
    elif tie_break_num == 5 :
        return -0.06
    elif tie_break_num == 6 :
        return -0.05
    elif tie_break_num == 7 :
        return -0.04
    elif tie_break_num == 8 :
        return -0.03
    elif tie_break_num == 9 :
        return -0.02
    elif tie_break_num == 10 :
        return -0.01
    elif tie_break_num == 11 :
        return 0.01
    elif tie_break_num == 12 :
        return 0.02
    elif tie_break_num == 13 :
        return 0.03
    elif tie_break_num == 14 :
        return 0.04
    elif tie_break_num == 15 :
        return 0.05
    elif tie_break_num == 16 :
        return 0.06
    elif tie_break_num == 17 :
        return 0.07
    elif tie_break_num == 18 :
        return 0.08
    elif tie_break_num == 19 :
        return 0.09

    return 0.10


#final move value section
#this section combines all value types into one move score:
#capture value, position table bonus, development or position value,
#safety penalty, and a small random tie break
def calculate_move_value(board, start_row, start_col, end_row, end_col, color, use_random_tie_break = True) :

    #start from zero and add or subtract each factor one at a time
    piece = board[start_row][start_col]
    value = 0

    #capture value
    #taking a stronger piece gives more points
    capture_value = calculate_capture_value(board, end_row, end_col)
    capture_value = capture_value * CAPTURE_VALUE_MULTIPLIER
    value = value + capture_value

    #piece square value
    #moving to a better square adds value
    position_table_bonus = calculate_position_table_bonus(
        piece, start_row, start_col, end_row, end_col
    )
    position_table_bonus = position_table_bonus * POSITION_TABLE_MULTIPLIER
    value = value + position_table_bonus

    #development or position value
    #newly developed pieces use development value,
    #while already developed pieces use position value
    on_starting_square = is_piece_on_starting_square(piece, start_row, start_col)

    if on_starting_square == True :
        development_value = calculate_development_value(
            board, piece, start_row, start_col, end_row, end_col, color
        )
        development_value = development_value * DEVELOPMENT_VALUE_MULTIPLIER
        value = value + development_value
    else :
        position_value = calculate_position_value(
            board, piece, start_row, start_col, end_row, end_col, color
        )
        position_value = position_value * POSITION_VALUE_MULTIPLIER
        value = value + position_value

    #safety penalty
    #bad exposing moves lose value here
    safety_value = calculate_safety_value(
        board, piece, start_row, start_col, end_row, end_col, color
    )
    safety_value = safety_value * SAFETY_VALUE_MULTIPLIER
    value = value - safety_value

    #random tie break
    #used only to separate very close or equal moves
    if use_random_tie_break == True :
        value = value + get_random_tie_break()

    return value


#bias value section
#this section checks the player's best reply and slightly lowers
#AI moves that allow a dangerous response
def simulate_player_best_response(
    board,
    ai_move_start_row,
    ai_move_start_col,
    ai_move_end_row,
    ai_move_end_col,
    ai_color,
) :

    #after the AI move, find the strongest reply the player could make
    player_color = get_opponent_color(ai_color)
    sim_board = copy_board(board)

    make_move_on_board(
        sim_board,
        ai_move_start_row,
        ai_move_start_col,
        ai_move_end_row,
        ai_move_end_col,
    )

    player_moves = generate_all_legal_moves(sim_board, player_color)

    if len(player_moves) == 0 :
        return 0

    best_response_value = -999999

    #check every player response and keep the highest value one
    for move in player_moves :
        start_row = move[0]
        start_col = move[1]
        end_row = move[2]
        end_col = move[3]

        move_value = calculate_move_value(
            sim_board, start_row, start_col, end_row, end_col, player_color, False
        )

        if move_value > best_response_value :
            best_response_value = move_value

    return best_response_value


def calculate_bias_value(board, start_row, start_col, end_row, end_col, color) :

    #subtract a little from moves that allow a strong player response
    player_best_response = simulate_player_best_response(
        board, start_row, start_col, end_row, end_col, color
    )

    player_best_response = player_best_response * BIAS_VALUE_MULTIPLIER

    if player_best_response > 5 :
        return player_best_response * 0.5
    elif player_best_response > 3 :
        return player_best_response * 0.3

    return 0


def get_full_move_value(board, start_row, start_col, end_row, end_col, color) :

    #base value is the move itself before looking ahead
    base_value = calculate_move_value(board, start_row, start_col, end_row, end_col, color)

    #bias value is subtracted if the player has a strong answer
    bias_value = calculate_bias_value(board, start_row, start_col, end_row, end_col, color)

    return base_value - bias_value


#move choosing
def choose_best_move(board, legal_moves, color) :

    if len(legal_moves) == 0 :
        return [[], -999999]

    best_move = []
    best_value = -999999

    #compare every legal move and keep the move with the highest value
    for move in legal_moves :
        start_row = move[0]
        start_col = move[1]
        end_row = move[2]
        end_col = move[3]

        move_value = get_full_move_value(
            board, start_row, start_col, end_row, end_col, color
        )

        if move_value > best_value :
            best_value = move_value
            best_move = move

    return [best_move, best_value]


#ai move output
def get_ai_move_info(board, ai_color) :

    #generate legal moves first so any returned book move can be checked
    legal_moves = generate_all_legal_moves(board, ai_color)

    if len(legal_moves) == 0 :
        return [[], "no_moves"]

    #try opening book moves first before calculating everything
    move_history_strings = get_move_history_strings()
    book_result = get_book_move(move_history_strings)
    book_move = book_result[0]
    book_name = book_result[1]

    if book_move != "" :
        start_col = letter_to_col(book_move[0])
        start_row = 8 - int(book_move[1])
        end_col = letter_to_col(book_move[2])
        end_row = 8 - int(book_move[3])

        book_coords = [start_row, start_col, end_row, end_col]

        #only use the opening move if it is really legal on the board
        if book_coords in legal_moves :
            return [book_coords, "book: " + book_name]

    #if there is no book move, calculate the best normal move
    best_result = choose_best_move(board, legal_moves, ai_color)
    best_move = best_result[0]
    best_value = best_result[1]

    return [best_move, "move_value: " + str(round(best_value, 2))]
