#Name: Chess Data
#Programmer: Syed (Mahadi) Masuduzzaman
#Last Updated: June 10, 2026
#Description: This file stores the starting board, piece text, piece
#             values, and position value tables used by the game.


#starting board
#these are the internal two-letter piece codes used throughout the program
STARTING_POSITION = [
    ["br", "bn", "bb", "bq", "bk", "bb", "bn", "br"],
    ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
    ["", "", "", "", "", "", "", ""],
    ["", "", "", "", "", "", "", ""],
    ["", "", "", "", "", "", "", ""],
    ["", "", "", "", "", "", "", ""],
    ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
    ["wr", "wn", "wb", "wq", "wk", "wb", "wn", "wr"],
]


#piece symbols for drawing on the board
PIECE_TEXT = {
    "bp": "♟",
    "br": "♜",
    "bn": "♞",
    "bb": "♝",
    "bq": "♛",
    "bk": "♚",
    "wp": "♙",
    "wr": "♖",
    "wn": "♘",
    "wb": "♗",
    "wq": "♕",
    "wk": "♔",
}


#piece point values
PIECE_VALUES = {
    "p": 1, #pawn
    "n": 3, #knight
    "b": 3, #bishop
    "r": 5, #rook
    "q": 9, #queen
    "k": 0, #king
}


#position values for pawns
POSITION_VALUES_PAWN = [
    [0, 0, 0, 0, 0, 0, 0, 0],
    [5, 5, 5, 5, 5, 5, 5, 5],
    [1, 1, 2, 3, 3, 2, 1, 1],
    [0, 0, 1, 3, 3, 1, 0, 0],
    [0, 0, 1, 2, 2, 1, 0, 0],
    [0, 0, 0, 1, 1, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
]


#position values for knights
POSITION_VALUES_KNIGHT = [
    [0, 1, 2, 2, 2, 2, 1, 0],
    [1, 2, 3, 3, 3, 3, 2, 1],
    [2, 3, 4, 4, 4, 4, 3, 2],
    [2, 3, 4, 5, 5, 4, 3, 2],
    [2, 3, 4, 5, 5, 4, 3, 2],
    [2, 3, 4, 4, 4, 4, 3, 2],
    [1, 2, 3, 3, 3, 3, 2, 1],
    [0, 1, 2, 2, 2, 2, 1, 0],
]


#position values for bishops
POSITION_VALUES_BISHOP = [
    [0, 0, 1, 1, 1, 1, 0, 0],
    [0, 1, 2, 2, 2, 2, 1, 0],
    [1, 2, 3, 3, 3, 3, 2, 1],
    [1, 2, 3, 4, 4, 3, 2, 1],
    [1, 2, 3, 4, 4, 3, 2, 1],
    [1, 2, 3, 3, 3, 3, 2, 1],
    [0, 1, 2, 2, 2, 2, 1, 0],
    [0, 0, 1, 1, 1, 1, 0, 0],
]


#position values for rooks
POSITION_VALUES_ROOK = [
    [2, 2, 2, 3, 3, 2, 2, 2],
    [2, 3, 3, 3, 3, 3, 3, 2],
    [1, 2, 2, 2, 2, 2, 2, 1],
    [1, 2, 2, 2, 2, 2, 2, 1],
    [1, 2, 2, 2, 2, 2, 2, 1],
    [1, 2, 2, 2, 2, 2, 2, 1],
    [2, 3, 3, 3, 3, 3, 3, 2],
    [2, 2, 2, 3, 3, 2, 2, 2],
]


#position values for queens
POSITION_VALUES_QUEEN = [
    [0, 1, 1, 1, 1, 1, 1, 0],
    [1, 2, 3, 3, 3, 3, 2, 1],
    [1, 3, 4, 4, 4, 4, 3, 1],
    [1, 3, 4, 5, 5, 4, 3, 1],
    [1, 3, 4, 5, 5, 4, 3, 1],
    [1, 3, 4, 4, 4, 4, 3, 1],
    [1, 2, 3, 3, 3, 3, 2, 1],
    [0, 1, 1, 1, 1, 1, 1, 0],
]


#position values for kings
POSITION_VALUES_KING = [
    [1, 1, 0, 0, 0, 0, 1, 1],
    [1, 1, 0, 0, 0, 0, 1, 1],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [1, 1, 0, 0, 0, 0, 1, 1],
    [1, 1, 0, 0, 0, 0, 1, 1],
]


#all position value tables
#the AI looks up a table by piece type when it checks square quality
POSITION_VALUES = {
    "p": POSITION_VALUES_PAWN,
    "n": POSITION_VALUES_KNIGHT,
    "b": POSITION_VALUES_BISHOP,
    "r": POSITION_VALUES_ROOK,
    "q": POSITION_VALUES_QUEEN,
    "k": POSITION_VALUES_KING,
}
