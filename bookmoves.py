#Name: Opening Book
#Programmer: Syed (Mahadi) Masuduzzaman
#Date: June 10, 2026
#Description: This file stores a few opening patterns and returns a
#             matching AI opening move when one is found.


#opening lines
#each opening is stored as:
#["opening name", [["player move", "ai move"], ["player move", "ai move"]]]
openings = [
    ["King's Pawn (Italian Game)", [["E2E4", "E7E5"], ["G1F3", "B8C6"], ["F1C4", "F8C5"]]],
    ["Sicilian Defense", [["E2E4", "C7C5"], ["G1F3", "B8C6"], ["D2D4", "C5D4"]]],
    ["French Defense", [["E2E4", "E7E6"], ["D2D4", "D7D5"], ["B1C3", "F8B4"]]],
    ["Caro-Kann Defense", [["E2E4", "C7C6"], ["D2D4", "D7D5"], ["B1C3", "D5E4"]]],
    ["Queen's Gambit", [["D2D4", "D7D5"], ["C2C4", "E7E6"], ["B1C3", "G8F6"]]],
    ["King's Indian Defense", [["D2D4", "G8F6"], ["C2C4", "G7G6"], ["B1C3", "F8G7"]]],
]


#history checking
def does_opening_match(move_history, opening_moves) :

    match = True
    move_pair_index = 0

    #check both the player's past moves and the AI's past moves
    while move_pair_index < len(opening_moves) and match == True :
        player_history_index = move_pair_index * 2
        ai_history_index = player_history_index + 1

        if player_history_index < len(move_history) :
            expected_player_move = opening_moves[move_pair_index][0]
            actual_player_move = move_history[player_history_index]

            if expected_player_move != actual_player_move :
                match = False

        if ai_history_index < len(move_history) and match == True :
            expected_ai_move = opening_moves[move_pair_index][1]
            actual_ai_move = move_history[ai_history_index]

            if expected_ai_move != actual_ai_move :
                match = False

        move_pair_index = move_pair_index + 1

    return match


#book move lookup
def get_book_move(move_history) :

    #no opening can match if no moves have been played yet
    if len(move_history) == 0 :
        return ["", ""]

    #check each stored opening one at a time
    for opening in openings :
        opening_name = opening[0]
        opening_moves = opening[1]

        if does_opening_match(move_history, opening_moves) == True :
            next_ai_index = len(move_history) // 2

            #if the opening still has an AI reply available, use it
            if next_ai_index < len(opening_moves) :
                ai_move = opening_moves[next_ai_index][1]
                return [ai_move, opening_name]

    return ["", ""]
