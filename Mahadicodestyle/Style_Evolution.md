# Style Evolution - How Mahadi's Code Changed Over Time

## Phase 1: Early Assignments (March 2026)
Files: `Canadian Resource Calculator.py`, `Mahadi_ree.py`, `mahadi_guesser.py`

### Characteristics:
- Pure linear execution, no functions
- Space before colon: `if (x) :`
- `print ()` with space
- Comma-separated print output
- `i = i + 1` manual increment
- Long elif chains for everything
- `input ()` at end of file
- No error handling
- Global variables only

```python
# Typical early Mahadi code:
print ("Canadian Resource Global Placement\n")

china = 270000
usa = 45000

canada = float(input("How many tonnes...?: "))

if canada_percentage > china_percentage:
    print ("Canada is ranked #1 with", canada_rounded, "percent...")
elif canada_percentage > usa_percentage:
    print ("Canada is ranked #2 with", canada_rounded, "percent...")
```

---

## Phase 2: Function-Based Programs (March-April 2026)
Files: `mahadi_inventory.py`, `mahadi_orderer.py`, `mahadi_widget.py`

### What changed:
- Functions introduced: `def function_name() :`
- Still space before colon in function definitions
- Validation functions with `is_valid` pattern
- Boolean variables: `yestea`, `yesslushie`
- File I/O with manual open/close
- Constants introduced: `TEA_PRICE`, `TAX_RATE`
- Section comments: `#loading from file`
- `main()` function pattern appears
- Tkinter GUI introduced
- f-strings start appearing alongside comma prints
- `+= ` operator starts being used

```python
# Typical mid-phase Mahadi code:
def add_items() :

    #create empty list to hold all gear
    camping_inventory = []

    load_choice = input ("Do you want to load from inventory.txt? (y/n): ")

    if load_choice == "y" :
        print ("\nLoading inventory from inventory.txt...")
        load_from_file(camping_inventory)
    else :
        load_from_input(camping_inventory)

    return camping_inventory
```

---

## Phase 3: Chess Engine (May-June 2026)
Files: `main.py`, `board_logic.py`, `ai_engine.py`, `game_state.py`, `move_rules.py`, `data.py`, `bookmoves.py`

### What changed:
- Space before colon DROPPED: `def col_to_letter(col):`
- `print()` without space (mostly)
- `== True` / `== False` becomes universal
- Functions are well-organized across files
- Import statements at top
- Module-based architecture
- Complex nested loops for board analysis
- `canvas.delete("all")` instead of canvas recreation
- Still uses elif chains (never switched to dictionaries)
- Still manual string concatenation
- Still `i = i + 1` in some places
- Still bare `except:` for error handling
- Still `input ()` with space at end of some files

```python
# Typical late-phase Mahadi code:
def is_square_attacked(board, row, col, by_color):

    by_prefix = by_color[0]

    for r in range(8):
        for c in range(8):
            piece = board[r][c]
            if piece != "":
                if piece[0] == by_prefix:
                    if is_legal_move(r, c, row, col, board) == True:
                        return True

    return False
```

---

## What NEVER Changed (Your Core Signatures)

1. `== True` / `== False` - Used from first file to last
2. Long elif chains - Never adopted dictionaries for lookup
3. Section comments in lowercase - `#loading from file`
4. String concatenation with `+` - Never switched to `.join()`
5. Manual increment `i = i + 1` - Still appears in late code
6. Explicit variable initialization before use
7. Boolean flags for loop control
8. Minimal error handling
9. `input ()` with space (in assignments)
10. Space before `(` in function calls (in assignments)

---

## What Dropped Off

| Pattern | Assignments | Chess Engine |
|---------|------------|--------------|
| Space before `(` in print | `print ("x")` | `print("x")` |
| Space before `:` | `if (x) :` | `if x:` |
| `input ()` at end | Yes | No |
| `i = i + 1` | Universal | Mixed with `+=` |
| Comma-separated prints | Common | Rare (f-strings) |
| No functions | Linear code | Modular |

---

## Key Insight

Your code evolved in STRUCTURE (functions, modules, file organization) but your CORE HABITS (== True, elif chains, explicit comparisons) stayed the same. The fundamentals of how you think about code didn't change - you just learned to organize it better.
