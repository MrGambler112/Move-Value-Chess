#Name: Move Rules
#Programmer: Syed (Mahadi) Masuduzzaman
#Date: June 10, 2026
#Description: This file contains the movement rules for each chess
#             piece and helper functions for move validation.

from data import PIECE_VALUES


#board helpers
def is_on_board(row, col) :

    #rows and columns must stay between 0 and 7
    if row < 0 or row > 7 :
        return False

    if col < 0 or col > 7 :
        return False

    return True


def same_colour_piece(start_row, start_col, end_row, end_col, board) :

    #get the starting piece and the piece on the destination square
    start_piece = board[start_row][start_col]
    end_piece = board[end_row][end_col]

    if end_piece == "" :
        return False

    if start_piece[0] == end_piece[0] :
        return True

    return False


#pawn movement
def pawn_move(start_row, start_col, end_row, end_col, board) :

    #pawns cannot capture their own colour
    if same_colour_piece(start_row, start_col, end_row, end_col, board) == True :
        return False

    if board[start_row][start_col] == "wp" :
        #white pawns move upward one square at a time
        if start_col == end_col :
            if end_row == start_row - 1 :
                if board[end_row][end_col] == "" :
                    return True

            if start_row == 6 and end_row == 4 :
                #white pawns may move two squares from their starting row
                if board[5][start_col] == "" :
                    if board[end_row][end_col] == "" :
                        return True

        if end_row == start_row - 1 :
            #white pawns capture diagonally
            if end_col == start_col - 1 or end_col == start_col + 1 :
                if board[end_row][end_col] != "" :
                    return True

    return False


def black_pawn_move(start_row, start_col, end_row, end_col, board) :

    #black pawns use the same logic but move downward
    if same_colour_piece(start_row, start_col, end_row, end_col, board) == True :
        return False

    if board[start_row][start_col] == "bp" :
        if start_col == end_col :
            if end_row == start_row + 1 :
                if board[end_row][end_col] == "" :
                    return True

            if start_row == 1 and end_row == 3 :
                if board[2][start_col] == "" :
                    if board[end_row][end_col] == "" :
                        return True

        if end_row == start_row + 1 :
            if end_col == start_col - 1 or end_col == start_col + 1 :
                if board[end_row][end_col] != "" :
                    return True

    return False


#straight and diagonal path checking
def rook_move(start_row, start_col, end_row, end_col, board) :

    #rooks cannot take their own colour
    if same_colour_piece(start_row, start_col, end_row, end_col, board) == True :
        return False

    #rooks must move in a straight line
    if start_row != end_row and start_col != end_col :
        return False

    if start_col == end_col :
        #check every square between the start and end row
        if end_row > start_row :
            row_change = 1
        else :
            row_change = -1

        check_row = start_row + row_change

        while check_row != end_row :
            if board[check_row][start_col] != "" :
                return False

            check_row = check_row + row_change

        return True

    if start_row == end_row :
        #check every square between the start and end column
        if end_col > start_col :
            col_change = 1
        else :
            col_change = -1

        check_col = start_col + col_change

        while check_col != end_col :
            if board[start_row][check_col] != "" :
                return False

            check_col = check_col + col_change

        return True

    return False


def bishop_move(start_row, start_col, end_row, end_col, board) :

    #bishops also cannot take their own colour
    if same_colour_piece(start_row, start_col, end_row, end_col, board) == True :
        return False

    row_difference = end_row - start_row
    col_difference = end_col - start_col

    diagonal_move = False

    #a bishop must move diagonally in either diagonal direction
    if row_difference == col_difference :
        diagonal_move = True
    elif row_difference == (col_difference * -1) :
        diagonal_move = True

    if diagonal_move == False :
        return False

    if end_row > start_row :
        row_change = 1
    else :
        row_change = -1

    if end_col > start_col :
        col_change = 1
    else :
        col_change = -1

    check_row = start_row + row_change
    check_col = start_col + col_change

    #every square between start and end must be empty
    while check_row != end_row :
        if board[check_row][check_col] != "" :
            return False

        check_row = check_row + row_change
        check_col = check_col + col_change

    return True


#piece movement
def knight_move(start_row, start_col, end_row, end_col, board) :

    #knights can jump, so only the final shape matters
    if same_colour_piece(start_row, start_col, end_row, end_col, board) == True :
        return False

    row_difference = end_row - start_row
    col_difference = end_col - start_col

    if row_difference == 2 or row_difference == -2 :
        if col_difference == 1 or col_difference == -1 :
            return True

    if row_difference == 1 or row_difference == -1 :
        if col_difference == 2 or col_difference == -2 :
            return True

    return False


def queen_move(start_row, start_col, end_row, end_col, board) :

    #queens combine rook movement and bishop movement
    if same_colour_piece(start_row, start_col, end_row, end_col, board) == True :
        return False

    if rook_move(start_row, start_col, end_row, end_col, board) == True :
        return True

    if bishop_move(start_row, start_col, end_row, end_col, board) == True :
        return True

    return False


def king_move(start_row, start_col, end_row, end_col, board) :

    #kings cannot move onto their own colour
    if same_colour_piece(start_row, start_col, end_row, end_col, board) == True :
        return False

    row_difference = end_row - start_row
    col_difference = end_col - start_col

    if row_difference < -1 or row_difference > 1 :
        return False

    if col_difference < -1 or col_difference > 1 :
        return False

    if row_difference == 0 and col_difference == 0 :
        return False

    #if all checks passed, the king moved one square or less
    return True


#main move checker
def is_legal_move(start_row, start_col, end_row, end_col, board) :

    #first reject moves that leave the board
    if is_on_board(start_row, start_col) == False :
        return False

    if is_on_board(end_row, end_col) == False :
        return False

    piece = board[start_row][start_col]
    if piece == "" :
        return False

    #identify the type of piece and send it to the correct rule function
    piece_type = piece[1]

    if piece_type == "p" :
        if piece[0] == "w" :
            return pawn_move(start_row, start_col, end_row, end_col, board)
        else :
            return black_pawn_move(start_row, start_col, end_row, end_col, board)

    elif piece_type == "r" :
        return rook_move(start_row, start_col, end_row, end_col, board)

    elif piece_type == "n" :
        return knight_move(start_row, start_col, end_row, end_col, board)

    elif piece_type == "b" :
        return bishop_move(start_row, start_col, end_row, end_col, board)

    elif piece_type == "q" :
        return queen_move(start_row, start_col, end_row, end_col, board)

    elif piece_type == "k" :
        return king_move(start_row, start_col, end_row, end_col, board)

    return False


def get_piece_value(piece) :

    #empty squares are worth zero points
    if piece == "" :
        return 0

    piece_type = piece[1]

    #return the point value used by the game scoring system
    if piece_type in PIECE_VALUES :
        return PIECE_VALUES[piece_type]

    return 0
