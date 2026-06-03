from data import STARTING_POSITION

def pawn_move(start_row, start_col, end_row, end_col, STARTING_POSITION):

    if STARTING_POSITION[start_row][start_col] == "wp":

        if start_col == end_col:

            if end_row == start_row - 1:
                return True

            if start_row == 6 and end_row == 4:
                return True

    return False




def rook_move():
    pass

def knight_move():
    pass

def bishop_move():
    pass

def queen_move():
    pass

def king_move():
    pass
