# Code DNA - Actual Examples from Mahadi's Files

## Example 1: The Column Converter (appears 3 times)

### In main.py:219-238
```python
def to_upper_case(letter):
    if letter == "a":
        return "A"
    elif letter == "b":
        return "B"
    elif letter == "c":
        return "C"
    elif letter == "d":
        return "D"
    elif letter == "e":
        return "E"
    elif letter == "f":
        return "F"
    elif letter == "g":
        return "G"
    elif letter == "h":
        return "H"
    else:
        return letter
```

### In main.py:241-260
```python
def letter_to_col(letter):
    if letter == "A":
        return 0
    elif letter == "B":
        return 1
    elif letter == "C":
        return 2
    elif letter == "D":
        return 3
    elif letter == "E":
        return 4
    elif letter == "F":
        return 5
    elif letter == "G":
        return 6
    elif letter == "H":
        return 7
    else:
        return -1
```

### In ai_engine.py:16-34 (exact same function)
```python
def letter_to_col(letter):
    if letter == "A":
        return 0
    elif letter == "B":
        return 1
    elif letter == "C":
        return 2
    elif letter == "D":
        return 3
    elif letter == "E":
        return 4
    elif letter == "F":
        return 5
    elif letter == "G":
        return 6
    elif letter == "H":
        return 7
    else:
        return 0
```

**Mahadi pattern**: Copy-paste the same elif chain. A dictionary would be 2 lines.

---

## Example 2: Boolean Comparison (pervasive)

### From board_logic.py:34
```python
if is_legal_move(r, c, row, col, board) == True:
```

### From board_logic.py:75
```python
if is_in_check(board, color) == False:
```

### From ai_engine.py:73
```python
if on_starting_square == True:
    return 0
```

### From ai_engine.py:105
```python
if in_check == False:
    threat_count = threat_count + 1
```

### From main.py:342
```python
if is_checkmate(STARTING_POSITION, "white") == True:
```

### From main.py:544
```python
if (is_legal_move(start_row, start_col, end_row, end_col, STARTING_POSITION) == False):
```

**Mahadi pattern**: Never trust a boolean directly. Always `== True` or `== False`.

---

## Example 3: The Input Prompt Signature

```python
# Canadian Resource Calculator.py:21
canada = float(input("How many tonnes of rare earth metals should Canada mine in a year?: "))

# mahadi_guesser.py:18
player_name = input("Before we begin, what is your name?: ")

# mahadi_inventory.py:17
load_choice = input ("Do you want to load from inventory.txt? (y/n): ")

# mahadi_inventory.py:38
item_line = input ("What is the item? ")

# mahadi_inventory.py:202
item_code_input = input ("What is the item code? ")

# mahadi_orderer.py:43
server_name = input ("What is the server name?: ")

# mahadi_widget.py:50
maxgood = float(input("\nWhat is the MAXIMUM good measure?: "))
```

**Mahadi pattern**: Input prompts end with `?: ` or at least `?`.

---

## Example 4: Section Comment Style

### From mahadi_inventory.py
```python
#Loading gear into Inventory

def add_items() :

    #create empty list to hold all gear
    camping_inventory = []

    #ask user if they want to load from file or input manually
    load_choice = input ("Do you want to load from inventory.txt? (y/n): ")

    #loading information from inventory.txt
    if load_choice == "y" :

    #inputting user information manually
    else :
```

### From mahadi_widget.py
```python
#Lists
measurements = []
qualitypass = []

#Boolean Variables
value = True

#Strings and Integer Variables
maxgood = 0

#Widget Measures
print ("-----------------------------------------------------")

#loop to continue getting user input for more measurements
while (user_input != -1) :

#sorting passed and failed values of measurement
for i in measurements :
```

**Mahadi pattern**: `#lowercase section header` with no blank line before code.

---

## Example 5: Validation Chain

### From mahadi_inventory.py:120-166
```python
def validate_item(item_name, item_code, amount_input, max_amount_input) :

    is_valid = True

    #check if item name length is 15 characters or less
    if is_valid :
        if len(item_name) > 15 :
            print ("Error: Item name must be 15 characters or less.")
            is_valid = False

    #check if the item code is exactly 2 characters
    if is_valid :
        if len(item_code) != 2 :
            print ("Error: Item code must be exactly 2 characters.")
            is_valid = False

    #check that amount is a whole number
    if is_valid :
        if not is_whole_number(amount_input) :
             print ("Error: Amount must be a whole number.")
             is_valid = False

    #check amount is in range 0 to 999
    if is_valid :
        if not 0 <= int(amount_input) <= 999 :
            print ("Error: Amount must be between 0 and 999.")
            is_valid = False

    #check that max amount is a whole number
    if is_valid :
        if not is_whole_number(max_amount_input) :
            print ("Error: Max amount must be a whole number.")
            is_valid = False

    #check max amount is in range 1 to 999
    if is_valid :
        if not 1 <= int(max_amount_input) <= 999 :
            print ("Error: Max amount must be between 1 and 999.")
            is_valid = False

    #check amount does not exceed max amount
    if is_valid :
        if int(amount_input) > int(max_amount_input) :
            print ("Error: Amount cannot be greater than max amount.")
            is_valid = False

    return is_valid
```

**Mahadi pattern**: Sequential `if is_valid :` blocks. Each check depends on previous passing.

---

## Example 6: The Tkinter Window Block

### From mahadi_widget.py:169-175
```python
window = tkinter.Tk ()
window.geometry ("700x700")
window.title ("The Widgermidger Quality Control Visualizer")
window.attributes ("-topmost", True)
window.update_idletasks ()
window.attributes ("-topmost", False)
window.focus_force ()
```

### From main.py:32-38
```python
window = tkinter.Tk()
window.geometry("700x750")
window.title("Move Value Based Chess Engine")
window.attributes("-topmost", True)
window.update_idletasks()
window.attributes("-topmost", False)
window.focus_force()
```

**Mahadi pattern**: The `-topmost` True/False toggle. Appears in 4 files.

---

## Example 7: File Reading Pattern

### From mahadi_inventory.py:77-117
```python
def load_from_file(camping_inventory) :

    inventory_file = open("inventory.txt", "r")
    item_line = inventory_file.readline().strip()

    while item_line != "" :

        gear_description = inventory_file.readline().strip()

        item_parts = item_line.split()

        if len(item_parts) == 4 :

            item_name = item_parts[0]
            item_code = item_parts[1]
            amount_input = item_parts[2]
            max_amount_input = item_parts[3]

            if validate_item(item_name, item_code, amount_input, max_amount_input) :

                if len(gear_description) > 100 :
                    gear_description = gear_description[:100]

                camping_inventory.append([item_name, item_code, int(amount_input),
                                          int(max_amount_input), gear_description])

        else :
            print ("Error: Invalid line in file, expected 4 fields.")

        item_line = inventory_file.readline().strip()

    inventory_file.close()
```

**Mahadi pattern**: Manual open, readline in while loop, close at end. Never `with open()`.

---

## Example 8: The main() Function

### From mahadi_inventory.py:340-363
```python
def main() :

    print ("The Inventory")
    print ("Manage your camping gear inventory\n")


#loading inventory

    print ("Loading Inventory")

    camping_inventory = add_items()

    print ("\nInventory loaded with", len(camping_inventory), "item(s).")

#managing inventory

    manage_inventory(camping_inventory)

    print ("\nGood Camping")


main()

input ()
```

**Mahadi pattern**: `main()` defined, called, then `input ()` at the very end.

---

## Example 9: String Concatenation (No .join())

### From game_state.py:189-194
```python
move_strings = get_move_history_strings()
moves_line = ""
if len(move_strings) > 0:
    moves_line = move_strings[0]
    i = 1
    while i < len(move_strings):
        moves_line = moves_line + "," + move_strings[i]
        i = i + 1
```

### From game_state.py:266
```python
return (
    "W: " + str(lifetime[0]) + " L: " + str(lifetime[1]) + " D: " + str(lifetime[2])
)
```

### From main.py:306-313
```python
score_text = (
    "Player: "
    + str(player_score)
    + " pts  |  AI: "
    + str(ai_score)
    + " pts  |  Target: "
    + str(game_state.ai_target_score)
)
```

**Mahadi pattern**: String concatenation with `+`. Never `.join()`.

---

## Example 10: Explicit Increment

### From mahadi_guesser.py:72
```python
i = i + 1
```

### From mahadi_inventory.py:191
```python
i = i + 1
```

### From ai_engine.py:106
```python
threat_count = threat_count + 1
```

### From ai_engine.py:125
```python
adjustments = adjustments - 1
```

**Mahadi pattern**: `x = x + 1` not `x += 1` (especially in early code).
