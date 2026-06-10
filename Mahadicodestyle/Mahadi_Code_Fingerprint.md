# Mahadi's Code Fingerprint
## How You Know It's Written by Mahadi

---

## 1. FILE HEADER BLOCK

Every file starts with this exact comment structure:

```python
#Name: <Program Name>
#Programmer: Syed (Mahadi) Masuduzzaman
#Date: <Date>
#Description: <Description that spans
#             multiple lines indented like this>
```

The description ALWAYS wraps to a second line with `#` aligned under the text of line 1.
Seen in: `Canadian Resource Calculator.py`, `mahadi_guesser.py`, `mahadi_inventory.py`, `mahadi_orderer.py`, `mahadi_widget.py`, `Mahadi_ree.py`

---

## 2. SPACING QUIRK - THE MAHADI SPACE

You put a space BEFORE the opening parenthesis in function calls and control structures:

```python
print ("Hello")           # not print("Hello")
input ("What is the name? ")
int (input("How many? "))
float(input("Enter value: "))
window.geometry ("700x700")
canvas.create_rectangle (60, 200, 600, 600)
```

This is CONSISTENT across ALL files. It's your most recognizable signature.

Also applies to `if` statements:
```python
if (yestea) :
if (user_input != -1) :
while (another_day == "y") :
```

Spaces before parentheses in `if` and `while`, AND a space before the colon.

---

## 3. COLON SPACING

```python
if (condition) :       # space before colon
while (condition) :    # space before colon
def function_name() :  # space before colon (in assignments)
```

In the chess project (later work), the colon spacing tightens up:
```python
def col_to_letter(col):
def draw_board():
```

This shows evolution - the space-colon pattern is your beginner habit that you later dropped.

---

## 4. SECTION COMMENTS - HOW YOU ORGANIZE CODE

You use `#Section Name` as a header, then code underneath. NO blank line after the comment sometimes, blank line other times:

```python
#Production amounts
china = 270000
usa = 45000

#input from user of how many tonnes (metric ton) Canada should mine in year

canada = float(input("How many tonnes..."))
```

The comment style is ALWAYS lowercase (except proper nouns):
```python
#loading gear into Inventory
#loading from input manually
#loading from txt file
#validations for proper format
#Search item
#Managing the inventory
#displaying information
#main function to run the program
```

Comments are descriptive and explain WHAT the section does, not WHY.

---

## 5. VARIABLE NAMING

### snake_case everywhere:
```python
player_name
canada_percentage
item_line
gear_description
camping_inventory
load_choice
change_amount
```

### Boolean variables - two patterns:

**Pattern A: `yes` prefix (assignments)**
```python
yestea = False
yesslushie = False
yesteapearls = False
yesslushiepearls = False
```

**Pattern B: `is_` prefix (later code)**
```python
is_valid = True
is_good = False
is_moved_piece = ...
```

### Constants are UPPER_CASE:
```python
TEA_PRICE = 1.50
SLUSHIE_PRICE = 3.25
PEARL_PRICE = 0.60
TAX_RATE = 0.13
DELAY_SECONDS = 0.3
DESCR_START_COL = 50
DESCR_WRAP_WIDTH = 30
```

---

## 6. THE IF/ELIF CHAIN PATTERN

You LOVE long if/elif/else chains. You NEVER use dictionaries for lookup when you can write elif:

```python
# How Mahadi converts column to letter:
def col_to_letter(col):
    if col == 0:
        return "A"
    elif col == 1:
        return "B"
    elif col == 2:
        return "C"
    elif col == 3:
        return "D"
    elif col == 4:
        return "E"
    elif col == 5:
        return "F"
    elif col == 6:
        return "G"
    elif col == 7:
        return "H"
    else:
        return "?"
```

This appears in `main.py`, `game_state.py`, AND `ai_engine.py` - you copied it 3 times.
A dictionary would be 2 lines. You prefer the explicit elif chain.

### Also in mahadi_guesser.py:
```python
if choice == 0:
    answer = "toyota"
    hint = "Japan"
elif choice == 1:
    answer = "maserati"
    hint = "Italy"
elif choice == 2:
    answer = "ford"
    hint = "United States"
```

### And the tie_break in ai_engine.py:
```python
if tie_break_num == 1:
    tie_break = -0.10
elif tie_break_num == 2:
    tie_break = -0.09
elif tie_break_num == 3:
    tie_break = -0.08
# ... 17 more elif branches
```

This is THE Mahadi pattern. When in doubt, use more elif.

---

## 7. EXPLICIT COMPARISON STYLE

You ALWAYS compare explicitly instead of using Python truthiness:

```python
# Mahadi writes:
if piece == "":           # not: if not piece:
if user_answer == answer: # not: if user_answer == answer:
if item_position == -1:   # not: if item_position == -1:
if len(legal_moves) == 0: # not: if not legal_moves:
if is_valid == True:      # not: if is_valid:
if same_square == False:  # not: if not same_square:
if on_starting_square == True:
if in_check == False:
if blocked == False:
```

You write `== True` and `== False` instead of just using the boolean directly. This appears EVERYWHERE in your code.

---

## 8. LOOP STYLE

### While loops with manual increment:
```python
i = 0
while i < len(camping_inventory) and item_position == -1:
    if camping_inventory[i][1] == item_code_input:
        item_position = i
    i = i + 1
```

You use `i = i + 1` not `i += 1` (in assignments). Later code uses `+=`.

### For loops:
```python
for i in measurements:
    print(i)

for i in qualitypass:
    passsum += i

for row in range(8):
    for col in range(8):
        piece = board[row][col]
```

---

## 9. RETURN VALUE PATTERN

Functions return early or at the end. You use the pattern:

```python
def find_item(camping_inventory, item_code_input):
    item_position = -1
    i = 0
    while i < len(camping_inventory) and item_position == -1:
        if camping_inventory[i][1] == item_code_input:
            item_position = i
        i = i + 1
    return item_position
```

And for boolean validators:
```python
def is_whole_number(input_number):
    is_valid = True
    if not input_number.isdigit():
        is_valid = False
    return is_valid
```

You set a default, flip it if condition met, return it.

---

## 10. VALIDATION STYLE

Validation is done through long sequential if blocks:

```python
def validate_item(item_name, item_code, amount_input, max_amount_input):
    is_valid = True

    if is_valid:
        if len(item_name) > 15:
            print("Error: Item name must be 15 characters or less.")
            is_valid = False

    if is_valid:
        if len(item_code) != 2:
            print("Error: Item code must be exactly 2 characters.")
            is_valid = False

    if is_valid:
        if not is_whole_number(amount_input):
             print("Error: Amount must be a whole number.")
             is_valid = False
```

Each check is wrapped in `if is_valid:` so checks stop after the first failure.
This is YOUR validation pattern. It appears multiple times.

---

## 11. PRINT STYLE

### Comma-separated prints (assignments):
```python
print ("Canada is ranked #1 with", canada_rounded, "percent of the world supply\n")
print ("\nTo purchase", ndvalue, "tonnes of Neodymium, it will cost approximately: ", price1, "dollars\n")
```

### f-strings (later code):
```python
print (f"\n{teas} teas: {teacost:.2f} dollars")
print (f"The average converted measure is: {convertedaverage}")
```

### String concatenation in display:
```python
display_left = "    " + item_name + " " + item_code + " " + str(current_amount)
```

### Newline at end of print:
You often end print statements with `\n`:
```python
print ("Welcome to The Auto Guesser where you must guess the correct companies"
        " according to their countries of origin\n")
```

---

## 12. INPUT PROMPT STYLE

Input prompts end with `?: ` (question mark, colon, space):

```python
input("How many tonnes of rare earth metals should Canada mine in a year?: ")
input("Do you want to load from inventory.txt? (y/n): ")
input("What is the item? ")
input("How much would you like to add? ")
input("Before we begin, what is your name?: ")
```

The `?: ` ending is signature Mahadi.

---

## 13. GUI STYLE (tkinter)

### Window setup pattern:
```python
window = tkinter.Tk()
window.geometry("700x700")
window.title("Title Here")
window.attributes("-topmost", True)
window.update_idletasks()
window.attributes("-topmost", False)
window.focus_force()
```

This EXACT sequence appears in `mahadi_orderer.py`, `mahadi_widget.py`, `test.py`, and `main.py`.
The `-topmost` toggle is to force the window to appear on top, then release.

### Canvas animation pattern:
```python
canvas = tkinter.Canvas(window, width=700, height=700, bg="white")
for frame in range(70):
    canvas = tkinter.Canvas(window, width=700, height=700, bg="white")
    # draw stuff
    canvas.pack()
    canvas.update()
    time.sleep(0.03)
    canvas.destroy()
```

You recreate the canvas every frame instead of using `canvas.delete("all")`.
In main.py you evolved to `canvas.delete("all")` which is better.

---

## 14. FILE I/O STYLE

Manual open/close, NO context managers:

```python
inventory_file = open("inventory.txt", "r")
item_line = inventory_file.readline().strip()
while item_line != "":
    # process
    item_line = inventory_file.readline().strip()
inventory_file.close()
```

You read line by line with `while line != "":` pattern.
You NEVER use `with open(...) as f:` - always manual close.

---

## 15. FUNCTION STRUCTURE

### Blank line after def:
```python
def add_items() :

    #create empty list to hold all gear
    camping_inventory = []
```

There's always a blank line after the function definition, then a comment, then code.

### Functions are organized top-to-bottom by dependency:
1. Helper functions first (validate, find, load)
2. Main logic functions (manage_inventory)
3. Display functions (print_item)
4. main() at the bottom

---

## 16. MAIN FUNCTION PATTERN

```python
def main() :
    print ("The Inventory")
    print ("Manage your camping gear inventory\n")

    print ("Loading Inventory")
    camping_inventory = add_items()
    print ("\nInventory loaded with", len(camping_inventory), "item(s).")

    manage_inventory(camping_inventory)
    print ("\nGood Camping")

main()

input ()
```

- `main()` defined near the bottom
- Called immediately after definition
- Ends with `input ()` to keep console open
- `input ()` has a space before the parentheses (your signature)

---

## 17. LIST OPERATIONS

```python
# Building lists manually:
camping_inventory.append([item_name, item_code, int(amount_input),
                          int(max_amount_input), gear_description])

# Accessing nested list items:
gear_item = camping_inventory[item_position]
item_name = gear_item[0]
item_code = gear_item[1]
current_amount = gear_item[2]

# Sorting:
measurements.sort()

# Slicing:
convertedmeasures = measurements[actualmeasures:-(actualmeasures)]
```

---

## 18. ERROR HANDLING

Minimal. You print error messages and continue:

```python
else:
    print("Error: Please enter all 4 fields on one line.")
    print("Format: name code amount max_amount")
```

The only `try/except` in your code is in `main.py`:
```python
try:
    target = int(score_text)
    if target < 1:
        target = 10
except:
    target = 10
```

Bare `except:` - catches everything, no specific exception type.

---

## 19. BOOLEAN FLAGS

You use boolean flags to control loop flow:

```python
correct = True
while correct:
    user_answer = input(...)
    if user_answer == answer:
        correct = False
    if i == max_guesses:
        correct = False
```

```python
yestea = False
if (teas > 0):
    yestea = True
```

---

## 20. THE `== True` / `== False` HABIT

This is THE most consistent thing across ALL your code:

```python
if is_checkmate(STARTING_POSITION, "white") == True:
if is_stalemate(STARTING_POSITION, "white") == False:
if on_starting_square == True:
if in_check == False:
if game_started == False:
if timer_running == True:
if legal == True:
if blocked == False:
```

You never write `if is_checkmate(...)`. Always `== True` or `== False`.

---

## 21. COMMENT PLACEMENT

Comments go ABOVE the line they describe, always:

```python
#canada's rank (global placement)
if canada_percentage > china_percentage:

#receipt random number
receiptnumber = random.randrange(10, 1000)

#Receipt
print ("\n----------------------------------------\n")
```

Inline comments are rare. You prefer line-above comments.

---

## 22. MAGIC NUMBERS

You hardcode numbers directly in logic:

```python
teacost = teas * TEA_PRICE
teapearlcost = numteapearls * PEARL_PRICE

# But also:
price1 = round(ndvalue * 221100, 1)  # 221100 hardcoded
price2 = round(dyvalue * 930700, 1)  # 930700 hardcoded

# In the chess engine:
if start_row == 6 and end_row == 4:  # pawn double move
if start_row == 1 and end_row == 3:  # black pawn double move
```

Constants exist for SOME values but not all.

---

## 23. CODE DUPLICATION

You copy-paste code blocks with minor modifications:

- `col_to_letter()` appears in main.py, game_state.py, ai_engine.py
- `to_upper_case()` in main.py repeats the same logic 8 times
- The check_game_over() logic is duplicated for white and black
- The timer update logic for player and AI is nearly identical

You prefer explicit repetition over abstraction.

---

## 24. STRING BUILDING

```python
# Simple concatenation:
score_text = "Player: " + str(player_score) + " pts   AI: " + str(ai_score) + " pts"

# Or building line by line:
moves_line = move_strings[0]
i = 1
while i < len(move_strings):
    moves_line = moves_line + "," + move_strings[i]
    i = i + 1
```

No `.join()` usage. Manual concatenation with `+`.

---

## 25. INDENTATION AND WHITESPACE

- 4 spaces for indentation (consistent)
- Blank lines between functions
- Sometimes extra blank lines between sections
- Spaces around operators: `total = canada + china + usa`
- Spaces after commas in function calls: `print("a", "b", "c")`

---

## SUMMARY: THE MAHADI SIGNATURE

If you see these in a Python file, it's Mahadi's code:

1. Space before parentheses: `print ()`, `input ()`, `if (x) :`
2. Long if/elif chains instead of dictionaries
3. `== True` and `== False` everywhere
4. Section comments in lowercase: `#loading from file`
5. Header block with Name/Programmer/Date/Description
6. `?: ` ending on input prompts
7. Manual file open/close
8. `i = i + 1` instead of `i += 1`
9. Boolean `yes` prefix variables: `yestea`, `yesslushie`
10. Canvas recreation in animation loops
11. `input ()` at the end of every program
12. Explicit validation with sequential `if is_valid:` blocks
13. Early return with sentinel values (`item_position = -1`)
14. String concatenation instead of f-strings
15. Bare `except:` for error handling
