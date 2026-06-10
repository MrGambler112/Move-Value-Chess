#Name: Safety Debug Test
#Programmer: Syed (Mahadi) Masuduzzaman and Ryan Rawal
#Date: June 10, 2026
#Description: This file prints board layouts and a few debug checks
#             to help inspect AI safety value situations.

from ai_engine import calculate_safety_value
from move_rules import is_legal_move


#board printing
def print_board(board) :

    #print the board in a simple text layout for debugging
    for row in range(8) :
        row_text = ""

        for col in range(8) :
            piece = board[row][col]

            if piece == "" :
                row_text = row_text + "  . "
            else :
                row_text = row_text + " " + piece + " "

        print (row_text)


#debug test 1
print ("=== Test 1: Knight Leaving Rook Vulnerable ===")

board_1 = [
    ["br", "", "", "", "", "", "", ""],
    ["", "", "", "", "", "", "", ""],
    ["", "", "", "", "", "", "", ""],
    ["", "", "", "", "", "", "", ""],
    ["", "", "", "", "", "", "", ""],
    ["", "", "", "", "", "", "", ""],
    ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
    ["wr", "wn", "wb", "wq", "wk", "wb", "wn", "wr"],
]

print ("Board:")
print_board (board_1)
print ("")
print ("Knight b1 to a3 legal:", is_legal_move (7, 1, 5, 0, board_1))
print ("Enemy rook a8 to a1 legal:", is_legal_move (0, 0, 7, 0, board_1))
print ("Knight b1 to a1 legal:", is_legal_move (7, 1, 7, 0, board_1))
print ("")


#debug test 2
print ("=== Test 2: Clear Path for Enemy Rook ===")

board_2 = [
    ["br", "", "", "", "", "", "", ""],
    ["", "", "", "", "", "", "", ""],
    ["", "", "", "", "", "", "", ""],
    ["", "", "", "", "", "", "", ""],
    ["", "", "", "", "", "", "", ""],
    ["", "", "", "", "", "", "", ""],
    ["", "", "", "", "", "", "", ""],
    ["wr", "wn", "wb", "wq", "wk", "wb", "wn", "wr"],
]

print ("Board:")
print_board (board_2)
print ("")
print ("Enemy rook a8 to a1 legal:", is_legal_move (0, 0, 7, 0, board_2))
print ("Knight b1 to a1 legal:", is_legal_move (7, 1, 7, 0, board_2))
print (
    "Knight b1 to c3 safety value:",
    calculate_safety_value (board_2, "wn", 7, 1, 5, 2, "white"),
)
print ("")
print ("=== Debug Complete ===")
