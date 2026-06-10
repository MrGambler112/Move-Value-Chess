#Name: Safety Test
#Programmer: Syed (Mahadi) Masuduzzaman
#Date: June 10, 2026
#Description: This file runs simple console tests for the AI safety
#             value function using a few sample board positions.

from ai_engine import calculate_safety_value


#test helpers
def print_test_result(test_name, board, piece, start_row, start_col, end_row, end_col, color) :

    print ("========================================")
    print (test_name)

    #run the chosen test move through the safety value function
    safety_value = calculate_safety_value(
        board, piece, start_row, start_col, end_row, end_col, color
    )

    print ("Safety value:", safety_value)
    print ("")


#test 1
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

print_test_result (
    "Test 1: Knight leaves rook vulnerable",
    board_1,
    "wn",
    7,
    1,
    5,
    2,
    "white",
)


#test 2
board_2 = [
    ["br", "", "", "", "", "", "", ""],
    ["", "", "", "", "", "", "", ""],
    ["", "", "", "", "", "", "", ""],
    ["", "", "", "", "", "", "", ""],
    ["", "", "", "", "", "", "", ""],
    ["", "", "", "", "", "", "", ""],
    ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
    ["wr", "wn", "wb", "wq", "wk", "wb", "wn", "wr"],
]

print_test_result (
    "Test 2: Rook is protected",
    board_2,
    "wn",
    7,
    1,
    5,
    2,
    "white",
)


#test 3
board_3 = [
    ["", "", "", "", "", "", "", ""],
    ["", "", "", "", "", "", "", ""],
    ["", "", "", "", "", "", "", ""],
    ["", "", "", "", "", "", "", ""],
    ["", "", "", "", "", "", "", ""],
    ["", "", "", "", "", "", "", ""],
    ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
    ["wr", "wn", "wb", "wq", "wk", "wb", "wn", "wr"],
]

print_test_result (
    "Test 3: Pawn move",
    board_3,
    "wp",
    6,
    4,
    4,
    4,
    "white",
)


#test 4
board_4 = [
    ["", "", "", "", "", "", "", ""],
    ["", "", "", "", "", "", "", ""],
    ["", "", "", "", "", "", "", ""],
    ["", "", "", "", "", "", "", ""],
    ["", "", "", "", "", "", "", ""],
    ["", "", "", "", "", "", "", ""],
    ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
    ["wr", "wn", "wb", "wq", "wk", "wb", "wn", "wr"],
]

print_test_result (
    "Test 4: Queen move",
    board_4,
    "wq",
    7,
    3,
    3,
    7,
    "white",
)


#test 5
board_5 = [
    ["", "", "", "", "", "", "", ""],
    ["", "", "", "", "", "", "", ""],
    ["", "", "", "", "", "", "", ""],
    ["", "", "", "", "", "", "", ""],
    ["", "", "", "", "", "", "", ""],
    ["", "", "", "", "", "", "", ""],
    ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
    ["wr", "wn", "wb", "wq", "wk", "wb", "wn", "wr"],
]

print_test_result (
    "Test 5: Knight leaves bishop",
    board_5,
    "wn",
    7,
    1,
    5,
    3,
    "white",
)

print ("========================================")
print ("All safety tests complete")
