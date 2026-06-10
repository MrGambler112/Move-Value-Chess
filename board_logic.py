#Name: Board Logic
#Programmer: Syed (Mahadi) Masuduzzaman
#Date: June 10, 2026
#Description: This file contains helper functions for board copying,
#             attack checking, and full legal move generation.

from move_rules import is_legal_move


#colour helpers
def get_opponent_color(color) :

    if color == "white" :
        return "black"

    return "white"


#board copying
def copy_board(board) :

    new_board = []

    #copy every square one row at a time
    for row in range(8) :
        new_row = []

        for col in range(8) :
            new_row.append(board[row][col])

        new_board.append(new_row)

    return new_board


#king searching
def find_king(board, color) :

    king_code = color[0] + "k"

    #search the board until the correct king is found
    for row in range(8) :
        for col in range(8) :
            if board[row][col] == king_code :
                return [row, col]

    return [-1, -1]


#attack checking
def is_square_attacked(board, row, col, by_color) :

    by_prefix = by_color[0]

    #if any enemy piece has a legal move to the square, the square is attacked
    for check_row in range(8) :
        for check_col in range(8) :
            piece = board[check_row][check_col]

            if piece != "" :
                if piece[0] == by_prefix :
                    if is_legal_move(check_row, check_col, row, col, board) == True :
                        return True

    return False


def is_in_check(board, color) :

    #find the king first, then test whether the enemy attacks that square
    king_pos = find_king(board, color)
    king_row = king_pos[0]
    king_col = king_pos[1]

    if king_row == -1 :
        return False

    opponent = get_opponent_color(color)
    return is_square_attacked(board, king_row, king_col, opponent)


#move testing
def make_move_on_board(board, start_row, start_col, end_row, end_col) :

    #save the captured piece before it is overwritten
    captured_piece = board[end_row][end_col]

    #move the piece and empty the starting square
    board[end_row][end_col] = board[start_row][start_col]
    board[start_row][start_col] = ""

    return captured_piece


def would_be_in_check(board, start_row, start_col, end_row, end_col, color) :

    #test the move on a copied board so the real board is not changed
    test_board = copy_board(board)
    test_board[end_row][end_col] = test_board[start_row][start_col]
    test_board[start_row][start_col] = ""

    return is_in_check(test_board, color)


#game ending states
def is_checkmate(board, color) :

    #checkmate means the king is in check and no legal move can escape
    if is_in_check(board, color) == False :
        return False

    legal_moves = generate_all_legal_moves(board, color)
    if len(legal_moves) == 0 :
        return True

    return False


def is_stalemate(board, color) :

    #stalemate means no legal move exists, but the king is not in check
    if is_in_check(board, color) == True :
        return False

    legal_moves = generate_all_legal_moves(board, color)
    if len(legal_moves) == 0 :
        return True

    return False


#move generation
def generate_all_legal_moves(board, color) :

    legal_moves = []
    color_prefix = color[0]

    #check every piece of the chosen colour
    for start_row in range(8) :
        for start_col in range(8) :
            piece = board[start_row][start_col]

            if piece != "" :
                if piece[0] == color_prefix :
                    #for each piece, test every possible ending square
                    for end_row in range(8) :
                        for end_col in range(8) :
                            same_square = start_row == end_row and start_col == end_col

                            if same_square == False :
                                legal = is_legal_move(
                                    start_row, start_col, end_row, end_col, board
                                )

                                if legal == True :
                                    #a legal move is only kept if it does not leave the king in check
                                    in_check = would_be_in_check(
                                        board,
                                        start_row,
                                        start_col,
                                        end_row,
                                        end_col,
                                        color,
                                    )

                                    if in_check == False :
                                        legal_moves.append(
                                            [start_row, start_col, end_row, end_col]
                                        )

    return legal_moves


def count_legal_moves(board, color) :

    moves = generate_all_legal_moves(board, color)
    return len(moves)
