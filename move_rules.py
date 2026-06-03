from data import STARTING_POSITION

def same_colour_piece(start_row, start_col, end_row, end_col, STARTING_POSITION):

    start_piece = STARTING_POSITION[start_row][start_col]
    end_piece = STARTING_POSITION[end_row][end_col]

    if end_piece == "":
        return False

    if start_piece[0] == end_piece[0]:
        return True

    return False

def pawn_move(start_row, start_col, end_row, end_col, STARTING_POSITION):

    if same_colour_piece(start_row, start_col, end_row, end_col, STARTING_POSITION) == True:
        return False

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

def black_pawn_move(start_row, start_col, end_row, end_col, STARTING_POSITION):

    if same_colour_piece(start_row, start_col, end_row, end_col, STARTING_POSITION) == True:
        return False

    if STARTING_POSITION[start_row][start_col] == "bp":

        if start_col == end_col:
            if end_row == start_row + 1:
                if STARTING_POSITION[end_row][end_col] == "":
                    return True

            if start_row == 1 and end_row == 3:
                if STARTING_POSITION[2][start_col] == "":
                    if STARTING_POSITION[end_row][end_col] == "":
                        return True

        if end_row == start_row + 1:
            if end_col == start_col - 1 or end_col == start_col + 1:
                if STARTING_POSITION[end_row][end_col] != "":
                    return True

    return False

def rook_move(start_row, start_col, end_row, end_col, STARTING_POSITION):

    if same_colour_piece(start_row, start_col, end_row, end_col, STARTING_POSITION) == True:
        return False    

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

def knight_move(start_row, start_col, end_row, end_col, STARTING_POSITION):

    if same_colour_piece(start_row, start_col, end_row, end_col, STARTING_POSITION) == True:
        return False

    row_difference = end_row - start_row
    col_difference = end_col - start_col

    if row_difference == 2 or row_difference == -2:
        if col_difference == 1 or col_difference == -1:
            return True

    if row_difference == 1 or row_difference == -1:
        if col_difference == 2 or col_difference == -2:
            return True

    return False

def bishop_move(start_row, start_col, end_row, end_col, STARTING_POSITION):

    if same_colour_piece(start_row, start_col, end_row, end_col, STARTING_POSITION) == True:
        return False

    row_difference = end_row - start_row
    col_difference = end_col - start_col

    if row_difference == col_difference:
        diagonal_move = True

    elif row_difference == (col_difference * -1):
        diagonal_move = True

    else:
        diagonal_move = False

    if diagonal_move == False:
        return False
    

    if end_row > start_row:
        row_change = 1
    else:
        row_change = -1

    if end_col > start_col:
        col_change = 1
    else:
        col_change = -1

    check_row = start_row + row_change
    check_col = start_col + col_change

    while check_row != end_row:
        if STARTING_POSITION[check_row][check_col] != "":
            return False

        check_row = check_row + row_change
        check_col = check_col + col_change

    return True

def queen_move(start_row, start_col, end_row, end_col, STARTING_POSITION):

    if same_colour_piece(start_row, start_col, end_row, end_col, STARTING_POSITION) == True:
        return False

    if rook_move(start_row, start_col, end_row, end_col, STARTING_POSITION) == True:
        return True

    if bishop_move(start_row, start_col, end_row, end_col, STARTING_POSITION) == True:
        return True

    return False

def king_move(start_row, start_col, end_row, end_col, STARTING_POSITION):

    if same_colour_piece(start_row, start_col, end_row, end_col, STARTING_POSITION) == True:
        return False

    row_difference = end_row - start_row
    col_difference = end_col - start_col

    if row_difference < -1:
        return False

    if row_difference > 1:
        return False

    if col_difference < -1:
        return False

    if col_difference > 1:
        return False

    if row_difference == 0 and col_difference == 0:
        return False

    return True
