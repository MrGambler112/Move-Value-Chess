from data import STARTING_POSITION

def pawn_move(start_row, start_col, end_row, end_col, STARTING_POSITION):

    if STARTING_POSITION[start_row][start_col] == "wp":

        if start_col == end_col:
            if end_row == start_row - 1:
                if STARTING_POSITION[end_row][end_col] == "":
                    return True

            if start_row == 6 and end_row == 4:
                if STARTING_POSITION[5][start_col] == "":
                    if STARTING_POSITION[end_row][end_col] == "":
                        return True

        if end_row == start_row - 1:
            if end_col == start_col - 1 or end_col == start_col + 1:
                if STARTING_POSITION[end_row][end_col] != "":
                    return True

    return False


def rook_move(start_row, start_col, end_row, end_col, STARTING_POSITION):

    if start_row != end_row and start_col != end_col:
        return False

    if start_col == end_col:

        if end_row > start_row:
            row_change = 1
        else:
            row_change = -1

        check_row = start_row + row_change

        while check_row != end_row:
            if STARTING_POSITION[check_row][start_col] != "":
                return False

            check_row = check_row + row_change

        return True

    if start_row == end_row:

        if end_col > start_col:
            col_change = 1
        else:
            col_change = -1

        check_col = start_col + col_change

        while check_col != end_col:
            if STARTING_POSITION[start_row][check_col] != "":
                return False

            check_col = check_col + col_change

        return True

    return False

def knight_move():
    pass

def bishop_move():
    pass

def queen_move():
    pass

def king_move():
    pass
